# Project Imports
from game.skill import ALLIES, ATTACK, CAUSE_EFFECT, FOE, FOES, SELF
from kivy.graphics import Color, Line
from kivy.lang import Builder
from refs import Refs
from game.floor import ENTRANCE, EXIT, SAFE_ZONES

# Standard Library Imports
from random import randint, uniform

# Kivy Imports
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

# KV Import
from loading.kv_loader import load_kv

# UIX Imports
from spine.skeleton.skeletonloader import SkeletonLoader
from spine.skeleton.skeletonrenderer import SkeletonRenderer
from uix.modules.headers import dungeon_header, time_header_simple
from uix.modules.screen import Screen
from uix.screens.dungeon.lwf_renderer import LWFRenderer, load_texture
from uix.screens.dungeon.marker import Marker
from uix.screens.dungeon.parallax_background import ParallaxBackground

load_kv(__name__)


move_name_source = """
Image:
    source: 'dungeon/move_bubble_background.png'
    Label:
        id: label
        font_name: 'Gabriola'
        font_size: root.height * 0.7
        text: 'Tres Piercer'
        size_hint: None, None
        size: root.width, root.height * 0.8
        pos: root.x, root.y + root.height * 0.2
"""


class Encounter:
    def __init__(self, old_encounter, distance, **kwargs):
        if old_encounter is None:
            self.encounter_x = distance
        else:
            self.encounter_x = old_encounter.get_x() + distance

    def get_x(self):
        return self.encounter_x


class EnemyHealth(RelativeLayout):
    max = NumericProperty(100)
    health = NumericProperty(0)
    mana = NumericProperty(0)  # This is only for hud updates not crashing


class FloorAnnouncement(Image):
    name = StringProperty('')

    def fade_out(self, duration):
        anim = Animation(opacity=0, duration=duration * 0.5)
        Clock.schedule_once(lambda dt: self.start_fading(anim), duration * 0.5)

    def start_fading(self, anim):
        anim.start(self)


class TargetInfo:
    def __init__(self):
        self.damage = 0
        self.death = False
        self.penetration = False
        self.critical = False
        self.block = False
        self.evade = False
        self.counter = False

        self.tstate = None


class BustupPreview(RelativeLayout):
    name = StringProperty('')
    name2 = StringProperty('')
    name3 = StringProperty('')
    character_source = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EnemyNamePreview(RelativeLayout):
    name = StringProperty('')
    rank = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ActionFlag(RelativeLayout):
    text = StringProperty('')
    background_color = ListProperty([1, 1, 1, 1])
    left = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.register_event_type('on_action')
        super().__init__(**kwargs)

    def on_action(self):
        pass


class DungeonBattle(Screen):
    level_num = NumericProperty(1)
    # is_boss = BooleanProperty(False)

    fade_interval = NumericProperty(1)
    battle_flash_alpha = NumericProperty(0)
    boss_warning_alpha = NumericProperty(0)

    auto_move_enabled = BooleanProperty(False)
    auto_battle_enabled = BooleanProperty(False)

    def __init__(self, level, boss, config, **kwargs):
        self.enemy_huds = {}
        # self.dungeon_config = config
        self.level_num = level
        # self.is_boss = boss

        # Base Variables
        self._keys = []
        self._party_speed = 5

        # Non-Battle Variables
        self.speed = 1
        self._direction = -1
        self.showing_announcement = True

        # Setup floor map
        self.floor_data = Refs.gc.get_floor_data()
        self._mapping_enabled = self.floor_data.party_has_perk('mapping')
        self.floor_map = self.floor_data.get_floor_map()
        self.battle_data = self.floor_data.get_battle_data()

        # Setup background
        self.parallax = None

        self.lwf_renderer = None

        # Setup characters
        self._skeleton_loader = SkeletonLoader()
        self._skeleton_renderer = SkeletonRenderer()
        self._last_animation = None
        self._result = None

        width, height = Refs.app.width, Refs.app.height
        self.character_positions = [
            (0.5 * width, 0.333 * height),
            (0.5 * width, 0.333 * height),
            (0.5 * width, 0.333 * height),
            (0.5 * width, 0.333 * height),
            (0.5 * width, 0.333 * height),
            (0.5 * width, 0.333 * height),
            (0.5 * width, 0.333 * height),
            (0.5 * width, 0.333 * height),
        ]

        self.character_battle_positions = [
            (0.615 * width, 0.515 * height),
            (0.685 * width, 0.480 * height),
            (0.760 * width, 0.445 * height),
            (0.840 * width, 0.410 * height)
        ]
        self.enemy_positions = [
            (0.250 * width, 0.500 * height),
            (0.150 * width, 0.475 * height),
            (0.200 * width, 0.400 * height),
            (0.300 * width, 0.325 * height),
        ]

        self.enemy_party = 0.175 * width, 0.425 * height
        self.char_party = 0.7275 * width, 0.410 * height
        self.action_flags = {}

        # Boss Warning
        self._fade_in = True
        self._fade_time = 0
        self._fade_update = None
        self._exit_distance = 10000

        super().__init__(**kwargs)
        self.boss_encounter = False

    def on_kv_post(self, base_widget):
        self.setup_data()

    def setup_data(self):
        self.parallax = ParallaxBackground(self.floor_data)
        self.parallax.bind(on_move=self.on_node_update)
        self.ids.parallax_background.clear_widgets()
        self.ids.parallax_foreground.clear_widgets()
        self.parallax.set_background_layer(self.ids.parallax_background)
        self.parallax.set_foreground_layer(self.ids.parallax_foreground)
        self.ids.battle_background.opacity = 0
        self.ids.battle_foreground.opacity = 0
        self.ids.twirl_widget.effects[0].bind(on_update=self.twirl_update)
        self.ids.twirl_widget.effects[0].bind(on_end=self.twirl_end)
        self.ids.animation_layer.opacity = 0
        self.ids.battle_hud.bind(on_toggle_icons=self.toggle_icons)
        self.ids.map_overlay.opacity = 0
        self.ids.map_action_flags.opacity = 0
        self.ids.fullscreen_map.opacity = 0
        self.ids.map_options.opacity = 0
        self.lwf_renderer = LWFRenderer(self.ids.animation_layer)

        characters = self.floor_data.get_characters()
        avg_speed = 0
        for index, character in enumerate(characters):
            character.load_skeleton(self._skeleton_loader)
            character.set_position(*self.character_positions[index])
            self.ids.battle_hud.huds[character].set_character(character, self.lwf_renderer)
            avg_speed += character.get_agility()
        avg_speed /= len(characters)
        avg_speed /= 200
        avg_speed = min(max(avg_speed, 5), 50)
        self._party_speed = avg_speed

    def on_enter(self, *args):
        Refs.app.bind_keyboard(on_key_down=self.on_keyboard_down, on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1 / 30)
        Clock.schedule_interval(self.update_time_header, 5)
        if not self.floor_data.is_in_encounter():
            self.ids.floor_announcement.fade_out(1.5)
            Clock.schedule_once(self.setup_after_fade, 1.5)
            if self._exit_distance < 2000 and self._fade_update is None:
                self._fade_update = Clock.schedule_interval(self.fade_update, 1 / 30)
        else:
            self.ids.twirl_widget.effects[0].resume()
            # self.update_screen_for_encounter()

    def on_leave(self, *args):
        Refs.app.unbind_keyboard(on_key_down=self.on_keyboard_down, on_key_up=self.on_keyboard_up)
        Clock.unschedule(self.update_time_header)
        if self._fade_update is not None:
            self._fade_update.cancel()
            self._fade_update = None

    def update_time_header(self, dt):
        self.ids.time_header.text = time_header_simple()

    def update_dungeon_header(self):
        self.ids.dungeon_header.text = dungeon_header(self._direction)

    def setup_after_fade(self, dt):
        self.showing_announcement = False
        # update the map
        self.refresh_map()
        self.process_action_flags(True)
        self.ids.battle_hud.opacity = 1
        if self._mapping_enabled:
            self.ids.map_overlay.opacity = 1
            self.ids.map_action_flags = 1
            self.ids.fullscreen_map.opacity = 1
            self.ids.map_options.opacity = 1
        self.ids.info_hud.opacity = 1
        self.ids.inventory.opacity = 1
        if self._exit_distance < 2000 and self._fade_update is None:
            self._fade_update = Clock.schedule_interval(self.fade_update, 1 / 30)

    def refresh_map(self):
        if self._mapping_enabled:
            if self.floor_map.get_enabled():
                self.ids.map_overlay.opacity = 1
                self.ids.map_overlay.text = self.floor_map.get_text(False)
                self.ids.map_scatter.set_text(self.floor_map.get_text(False, 200))
                return
        self.ids.map_overlay.opacity = 0

    def set_config(self, config):
        if 'auto_move_enabled' in config:
            self.auto_move_enabled = config['auto_move_enabled']
        if 'auto_battle_enabled' in config:
            self.auto_move_enabled = config['auto_battle_enabled']

    # def on_auto_move(self):
    #     self.auto_move_enabled = True
    #     self.moving = True
    #     Clock.unschedule(self.characters.idle_animation)
    #     Clock.schedule_interval(self.move_left, 1 / 30)
    #
    # def on_auto_move_cancel(self):
    #     self.auto_move_enabled = False
    #     self.moving = False
    #     Clock.unschedule(self.move_left)
    #     self.setup_moving(0)
    #
    # def on_auto_battle(self):
    #     pass
    #
    # def on_auto_battle_cancel(self):
    #     pass

    # Keyboard functions
    def on_keyboard_down(self, keyboard, key_name, text, modifiers):
        if self.floor_data.is_in_encounter() or self.showing_announcement or self.auto_move_enabled:
            return
        if key_name.startswith('move'):
            if key_name not in self._keys:
                if len(self._keys) == 0:
                    Clock.schedule_interval(self.move_update, 1 / 30)
                self._keys.append(key_name)
            return True
        if key_name == 'map':
            self.on_fullscreen_map()
            return True
        if key_name == 'options':
            self.on_map_options()
            return True
        if key_name == 'inventory':
            self.on_inventory()
            return True
        if key_name == 'primary_action':
            if self.floor_map.is_marker(ENTRANCE):
                self.on_ascend(None)
            elif self.floor_map.is_marker(EXIT):
                self.on_descend(None)
            elif self.floor_map.is_marker(SAFE_ZONES):
                if self.floor_data.is_activated_safe_zone():
                    self.on_rest(None)
                else:
                    self.on_create_safe_zone(None)
            return True

    def on_keyboard_up(self, keyboard, key_name):
        if self.floor_data.is_in_encounter():
            self._keys.clear()
            return
        if key_name.startswith('move'):
            if key_name in self._keys:
                self._keys.remove(key_name)
                self.update_key(key_name)
                if len(self._keys) == 0:
                    Clock.unschedule(self.move_update)
                    self.stop_animation()
            return True

    def update_key(self, key_name):
        if key_name == 'move_up':
            if self.parallax.update(0, 1, self._party_speed):
                self.movement_update()
                return 2
            else:
                self.stop_animation()
                return -1
        elif key_name == 'move_left':
            if self.parallax.update(-1, 0, self._party_speed):
                self.movement_update()
                return 0
            else:
                self.stop_animation()
                return -1
        elif key_name == 'move_down':
            if self.parallax.update(0, -1, self._party_speed):
                self.movement_update()
                return 1
            else:
                self.stop_animation()
                return -1
        elif key_name == 'move_right':
            if self.parallax.update(1, 0, self._party_speed):
                self.movement_update()
                return 3
            else:
                self.stop_animation()
                return -1
        return -1

    # Update functions
    def toggle_icons(self, instance):
        for hud in self.enemy_huds.values():
            hud.ids.icon_tray.opacity = 1 - hud.ids.icon_tray.opacity

    def update(self, dt):
        dt *= self.ids.battle_hud.time_scale
        canvas = self.ids.skeleton_layer.canvas
        canvas.clear()
        characters = self.floor_data.get_characters()
        canvas.add(Color(1, 0, 0, 1))
        for character in characters:
            if character.visible():
                character.update(dt)
                if character.opacity > 0:
                    # x, y = character.get_position()
                    # width, height = character.get_skeleton().getSize()
                    # canvas.add(Line(points=(x - width / 2, y, x + width / 2, y, x + width / 2, y + height, x - width / 2, y + height, x - width / 2, y), width=3))
                    self._skeleton_renderer.draw(canvas, character.get_skeleton())
        if self.battle_data is not None:
            entities = self.battle_data.get_enemies()
            for entity in entities:
                if entity.visible():
                    entity.update(dt)
                    if entity.opacity > 0:
                        # x, y = entity.get_position()
                        # width, height = entity.get_skeleton().getSize()
                        # canvas.add(Line(points=(x - width / 2, y, x + width / 2, y, x + width / 2, y + height, x - width / 2, y + height, x - width / 2, y), width=3))
                        self._skeleton_renderer.draw(canvas, entity.get_skeleton())
        if self.floor_data.is_in_encounter():
            self.lwf_renderer.update(dt)
        # Decrease safe zone timers
        #

    def move_update(self, dt):
        directions = []
        for key_name in self._keys:
            if key_name == 'move_down' and 'move_up' in self._keys:
                continue
            if key_name == 'move_up' and 'move_down' in self._keys:
                continue
            if key_name == 'move_left' and 'move_right' in self._keys:
                continue
            if key_name == 'move_right' and 'move_left' in self._keys:
                continue
            directions.append(self.update_key(key_name))
        if len(directions) == 1:
            direction = directions[0]
        elif 0 in directions:
            direction = 0
        else:
            direction = 3
        if direction != self._direction:
            self.animate(direction)
            self._direction = direction
            self.ids.dungeon_header.text = dungeon_header(direction)

        # Exit / Boss Distance
        exit_distance = self.floor_map.exit_distance(*self.parallax.get_pos_info())
        if exit_distance < 4000:
            if self._fade_update is None:
                self._fade_update = Clock.schedule_interval(self.fade_update, 1 / 30)
            self.fade_interval = ((exit_distance - 1400) / 3600) * 2 + 0.25
        elif self._fade_update is not None:
            self.boss_warning_alpha = 0
            self._fade_update.cancel()
            self._fade_update = None

    def fade_update(self, dt):
        self._fade_time = min(self._fade_time + dt, self.fade_interval)
        fade_percent = self._fade_time / self.fade_interval
        if self._fade_in:
            self.boss_warning_alpha = 1 * fade_percent
        else:
            self.boss_warning_alpha = 1 - 1 * fade_percent

        if self._fade_in and self.boss_warning_alpha >= 1:
            self._fade_in = False
        elif not self._fade_in and self.boss_warning_alpha <= 0:
            self._fade_in = True
        else:
            return
        self._fade_time = 0

    # We have moved across a node
    def on_node_update(self, background, direction):
        self.floor_data.progress_by_direction(direction)
        self.ids.map_overlay.text = self.floor_map.get_text(False)
        self.ids.map_scatter.set_text(self.floor_map.get_text(False, 200))
        self.process_action_flags()

    def process_action_flags(self, create=False):
        is_entrance = self.floor_map.is_marker(ENTRANCE)
        is_exit = self.floor_map.is_marker(EXIT)
        is_safe_zone = self.floor_map.is_marker(SAFE_ZONES)
        activated_safe_zone = self.floor_data.is_activated_safe_zone()

        adventurers_able = len(self.floor_data.get_able_characters()) > 0

        if create:
            self.action_flags[ENTRANCE] = None
            self.action_flags[EXIT] = None
            self.action_flags[SAFE_ZONES] = None
            self.action_flags['rest'] = None
            self.action_flags['dig'] = None
            self.action_flags['mine'] = None

        if adventurers_able:
            if self.action_flags['dig'] is None and Refs.gc.get_inventory().has_shovel():
                self.ids.action_flags.add_widget(self.action_flags['dig'])
                self.action_flags['dig'] = ActionFlag(text='[Q] Dig')
                self.action_flags['dig'].bind(on_action=self.on_dig)
            if self.action_flags['mine'] is None and Refs.gc.get_inventory().has_pickaxe():
                self.action_flags['mine'] = ActionFlag(text='[E] Mine')
                self.action_flags['mine'].bind(on_action=self.on_mine)
                self.ids.action_flags.add_widget(self.action_flags['mine'])
        else:
            if self.action_flags['dig'] is not None:
                self.ids.action_flags.remove_widget(self.action_flags['dig'])
                self.action_flags['dig'] = None
            if self.action_flags['mine'] is not None:
                self.ids.action_flags.remove_widget(self.action_flags['mine'])
                self.action_flags['mine'] = None

        if is_entrance:
            self.action_flags[ENTRANCE] = ActionFlag(text='[F] Ascend')
            self.action_flags[ENTRANCE].bind(on_action=self.on_ascend)
            self.ids.action_flags.add_widget(self.action_flags[ENTRANCE])
        elif self.action_flags[ENTRANCE] is not None:
            self.ids.action_flags.remove_widget(self.action_flags[ENTRANCE])
            self.action_flags[ENTRANCE] = None

        if is_exit:
            self.action_flags[EXIT] = ActionFlag(text='[F] Descend')
            self.action_flags[EXIT].bind(on_action=self.on_descend)
            self.ids.action_flags.add_widget(self.action_flags[EXIT])
        elif self.action_flags[EXIT] is not None:
            self.ids.action_flags.remove_widget(self.action_flags[EXIT])
            self.action_flags[EXIT] = None

        if is_safe_zone:
            if activated_safe_zone:
                self.action_flags['rest'] = ActionFlag(text='[F] Rest')
                self.action_flags['rest'].bind(on_action=self.on_rest)
                self.ids.action_flags.add_widget(self.action_flags['rest'])
            else:
                self.action_flags[SAFE_ZONES] = ActionFlag(text='[F] Create Safe Zone')
                self.action_flags[SAFE_ZONES].bind(on_action=self.on_create_safe_zone)
                self.ids.action_flags.add_widget(self.action_flags[SAFE_ZONES])
        elif self.action_flags[SAFE_ZONES] is not None:
            self.ids.action_flags.remove_widget(self.action_flags[SAFE_ZONES])
            self.action_flags[SAFE_ZONES] = None
        elif self.action_flags['rest'] is not None:
            self.ids.action_flags.remove_widget(self.action_flags['rest'])
            self.action_flags['rest'] = None

        for index, flag in enumerate(self.action_flags.values()):
            if flag is None:
                continue
            flag.size_hint = 0.175, 0.05
            flag.pos_hint = {'center_y': 0.9 - 0.075 * index}

    def on_inventory(self):
        if Refs.gp.is_popup_open('inventory'):
            Refs.gp.close_popup('inventory')
        else:
            Refs.gp.display_popup(self, 'inventory')

    def on_map_options(self):
        if not self._mapping_enabled:
            return
        if Refs.gp.is_popup_open('map_options'):
            Refs.gp.close_popup('map_options')
        else:
            Refs.gp.display_popup(self, 'map_options')

    def on_fullscreen_map(self):
        if not self._mapping_enabled:
            return
        new_opacity = 1 - self.ids.map.opacity
        self.ids.map.opacity = new_opacity
        self.ids.map.disabled = not self.ids.map.disabled
        self.ids.map_action_flags = new_opacity
        self.ids.action_flags.opacity = 1 - new_opacity

    def on_dig(self, instance):
        inventory = Refs.gc.get_inventory()
        tool = inventory.get_current_shovel()
        self.tool_action(tool, 'shovel', 'dig')

    def on_mine(self, instance):
        inventory = Refs.gc.get_inventory()
        tool = inventory.get_current_pickaxe()
        self.tool_action(tool, 'pickaxe', 'mine')

    def on_ascend(self, instance):
        Refs.gp.display_popup(self, 'dm_confirm', current_floor=self.level_num, on_confirm=lambda *args: self.do_ascend())

    def do_ascend(self):
        if self.level_num == 1:
            Refs.gs.display_screen('dungeon_result', True, False)
        else:
            Refs.gs.display_screen('dungeon_main', True, False, level=self.level_num, boss=False, locked=True)

    def on_descend(self, instance):
        Refs.gp.display_popup(self, 'dm_confirm', on_confirm=lambda *args: self.do_descend())

    def do_descend(self):
        pass

    def on_create_safe_zone(self, instance):
        pos = self.action_flags[SAFE_ZONES].pos_hint
        self.ids.action_flags.remove_widget(self.action_flags[SAFE_ZONES])
        self.action_flags[SAFE_ZONES] = None
        self.action_flags['rest'] = ActionFlag(text='[F] Rest', size_hint=(0.175, 0.05), pos_hint=pos)
        self.action_flags['rest'].bind(on_action=self.on_rest)
        self.ids.action_flags.add_widget(self.action_flags['rest'])

        inventory = Refs.gc.get_inventory()
        tool = inventory.get_current_harvesting_knife()
        self.tool_action(tool, 'knife', 'create_safe_zone')

    def tool_action(self, tool, tool_name, action):
        if tool is None:
            error_text = f'You have no {tool_name} selected!'
            Refs.gp.display_popup(self, 'error', error_text)
            return
        elif tool.get_hardness() < self.floor_data.get_floor().get_hardness():
            error_text = f'Your {tool_name} is not hard enough to affect this level!'
            Refs.gp.display_popup(self, 'error', error_text)
            return

        tool.remove_durability(Refs.gc.get_random_wear_amount() * 7.5)

        index = randint(0, len(self.floor_data.get_able_characters()) - 1)
        character = self.floor_data.get_able_characters()[index]
        character.take_action(Refs.gc.get_stamina_weight() + 1)

        self.floor_data.increase_stat(character.get_index(), 2, Refs.gc.get_random_stat_increase())

        if action == 'mine' or action == 'dig':
            self.floor_data.increase_rest_count(-2)
            # Refs.gp.display_popup(self, 'dungeon_resource_result', action, character.get_id())
        else:
            self.floor_data.activate_safe_zone()

    def on_rest(self, instance):
        for character in self.floor_data.get_characters():
            character.rest()
            self.ids.battle_hud.huds[character].stamina = character.get_stamina()
        Refs.gc.get_calendar().fast_forward(30)
        self.update_time_header(0)
        self.floor_data.decrease_safe_zones()
        self.floor_data.increase_rest_count()
        if not self.floor_data.is_activated_safe_zone():
            pos = self.action_flags['rest'].pos_hint
            self.ids.action_flags.remove_widget(self.action_flags['rest'])
            self.action_flags['rest'] = None
            self.action_flags[SAFE_ZONES] = ActionFlag(text='[F] Create Safe Zone', size_hint=(0.175, 0.05), pos_hint=pos)
            self.action_flags[SAFE_ZONES].bind(on_action=self.on_create_safe_zone)
            self.ids.action_flags.add_widget(self.action_flags[SAFE_ZONES])

    # Small movement update
    def movement_update(self):
        # Decrease stamina and increase agility
        # Check for asleep adventurers
        all_asleep = True
        for character in self.floor_data.get_characters():
            if character.is_dead():
                continue
            # Node walk is 1-5. Movement walk is node walk /83.3 or *0.012
            if not character.is_asleep():
                self.floor_data.increase_stat(character.get_index(), 5, Refs.gc.get_random_stat_increase() * 0.012)
                character.walk((Refs.gc.get_stamina_weight() + 1) * 0.012)
                self.ids.battle_hud.huds[character].stamina = character.get_stamina()
            all_asleep &= character.is_asleep()

        if all_asleep:
            self.showing_announcement = True
            self.show_failure()

        if self.floor_map.is_marker(EXIT) and not self.floor_data.get_floor().is_boss_defeated():
            # Show boss encounter
            self.floor_data.generate_boss_encounter()
            self.start_boss_encounter()
        else:
            # Encounter chance should be ~0.15 per node / 0.0018 per movement
            x, y = self.floor_map.get_current_node()
            if not all_asleep:
                if (x, y) not in self.floor_data.get_activated_safe_zones() and not self.floor_map.is_marker(EXIT):
                    chance = 0.18
                    node = None
                    for enemy_id in self.floor_data.get_floor().get_enemies().keys():
                        if self.floor_map.is_marker(enemy_id):
                            node = enemy_id
                            chance += 0.6
                            break
                    chance += 0.24 * self.floor_data.get_rest_count()
                    if uniform(0, 99) <= min(99, chance):
                        self.floor_data.generate_encounter(node, int(max(0, 100 - chance) / 50))
                        if node is not None:
                            # If we are standing on a node, and we get that enemy generated, reduce positions counter
                            for enemy in self.floor_data.get_battle_data().get_enemies():
                                if enemy.get_id() == node:
                                    if self.floor_data.party_has_perk('hunter'):
                                        self.floor_map.decrease_node_counter(2)
                                    else:
                                        self.floor_map.decrease_node_counter(1)
                                    break
                        self.start_encounter()

    # Animation Functions
    def animate(self, direction):
        flip_x = False
        if direction == 0:
            animation = 'run_side'
        elif direction == 3:
            animation = 'run_side'
            flip_x = True
        elif direction == 1:
            animation = 'run_front'
        elif direction == 2:
            animation = 'run_back'
        else:
            self.stop_animation()
            return

        self._last_animation = animation
        for character in self.floor_data.get_able_characters():
            character.set_flip_x(flip_x)
            character.set_animation(animation, loop=True)

    def set_animation_idle(self):
        if self._last_animation is not None and 'idle' in self._last_animation:
            return

        if self._last_animation is None:
            animation_name = 'idle_side'
        elif self._last_animation.startswith('walk_'):
            animation_name = 'idle_' + self._last_animation[5:]
        elif self._last_animation.startswith('run_'):
            animation_name = 'idle_' + self._last_animation[4:]
        else:
            animation_name = 'idle_side'

        self._last_animation = animation_name
        for character in self.floor_data.get_able_characters():
            character.set_animation(animation_name, loop=True)

    def play_encount_animations(self, to_battle=True):
        time = 0
        for index, character in enumerate(self.battle_data.get_characters()):
            if character is None:
                continue
            # Refs.log(f'{character.get_full_name()} enters the battle!')

            encount = character.set_animation('encount', False)
            encount_time = encount.endTime / self.ids.battle_hud.time_scale
            time = max(encount_time, time)

            if to_battle:
                self.character_positions[index] = character.get_position()
                x_anim = Animation(x=self.character_battle_positions[index][0], duration=encount_time)
                y_up_anim = Animation(y=self.character_battle_positions[index][1] * 1.25, duration=encount_time * 0.5)
                y_down_anim = Animation(y=self.character_battle_positions[index][1], duration=encount_time * 0.5)
            else:
                x_anim = Animation(x=self.character_positions[index][0], duration=encount_time)
                y_up_anim = Animation(y=self.character_positions[index][1] * 1.25, duration=encount_time * 0.5)
                y_down_anim = Animation(y=self.character_positions[index][1], duration=encount_time * 0.5)
            anim = x_anim & (y_up_anim + y_down_anim)
            anim.start(character)
        return time

    def show_enemies(self):
        entity_duration = 0.5 / self.ids.battle_hud.time_scale
        label_duration = 0.2 / self.ids.battle_hud.time_scale
        delay_duration = 1 / self.ids.battle_hud.time_scale
        fade_out_duration = 0.02 / self.ids.battle_hud.time_scale

        show_enemy = Animation(opacity=1, duration=entity_duration)
        enemies = self.battle_data.get_enemies()
        for entity in enemies:
            show_enemy.start(entity)

            move_name = Builder.load_string(move_name_source)
            move_name.size_hint = (0.1, 0.36 * 0.129)
            move_name.pos_hint = {'center_x': entity.x / Refs.app.width, 'y': (entity.y + entity.height * 0.8) / Refs.app.height}
            move_name.opacity = 0
            self.ids[entity.get_id()] = move_name
            self.ids.hud_layer.add_widget(move_name)
        fade_in_labels = Animation(duration=entity_duration) + Animation(opacity=1, duration=label_duration) + Animation(duration=delay_duration)
        fade_in_labels.start(self.ids.enemy_health)
        fade_in_labels += Animation(opacity=0, duration=fade_out_duration)
        fade_in_labels.start(self.ids.enemy_names)
        for character in self.floor_data.get_characters():
            character.set_animation('idleBattle', add=True, loop=True)

            move_name = Builder.load_string(move_name_source)
            move_name.size_hint = (0.1, 0.36 * 0.129)
            move_name.pos_hint = {'center_x': character.x / Refs.app.width, 'y': (character.y + character.height * 0.8) / Refs.app.height}
            move_name.opacity = 0
            self.ids[character.get_id()] = move_name
            self.ids.hud_layer.add_widget(move_name)
        return True

    def show_assist_animations(self):
        supports = [s for s in self.battle_data.get_supporters() if s is not None]
        assist_lwf = self._play_assist_lwf(supports)
        # Show the hud
        if assist_lwf is None:
            self.show_hud()
        else:
            assist_lwf.add_event_handler('end', lambda movie, button: self.show_hud())
            assist_lwf.add_event_handler('end', lambda movie, button: self.lwf_renderer.destroy_lwf('Assist Cutin'))

    def _play_assist_lwf(self, supports):
        assist_lwf = None
        assist_name = [None, '810000006', '810000007', '810000008', '810000009'][len(supports)]
        if assist_name is not None:
            def load_assist_texture(filename, path):
                if filename.startswith('lwf_img_replace_character_'):
                    index = int(filename[27])
                    filename = supports[index - 1].get_image('bustup')
                    path = ''
                elif filename.startswith('lwf_img_replace_skill_name_'):
                    index = int(filename[28])
                    skill_name = supports[index - 1].get_support_skill().get_name()
                    filename = f'res/assist_labels/{skill_name}.png'
                    path = ''
                return load_texture(filename, path)

            assist_lwf = self.lwf_renderer.register_lwf(f'{assist_name}/{assist_name}.lwf', 'Assist Cutin', load_assist_texture)
            assist_lwf.scale_for_width(Refs.app.width, Refs.app.height)
            assist_lwf.property.move(0, Refs.app.height)
            # lwf.add_event_handler('assist_skill_voice_1', )  # Add handler for assist voice. Maybe.
        # Show Assist Debuff and Buff Animations
        animation_queue, effect_queue, icon_queue = self.calculate_assist_effects(supports)
        for entity, icons in icon_queue.items():
            if entity.is_character():
                icon_tray = self.ids.battle_hud.huds[entity].ids.icon_tray
            else:
                icon_tray = self.enemy_huds[entity].ids.icon_tray
            icon_tray.apply_icons(icons)
        return assist_lwf

    def show_hud(self):
        self.ids.battle_hud.opacity = 1
        self.ids.battle_hud.enter_battle()
        self.ids.enemy_health.opacity = 1
        for character in self.battle_data.get_characters():
            character.set_in_battle(True)
            self.ids.battle_hud.huds[character].in_battle = True

    def stop_animation(self):
        self._direction = -1
        self._last_animation = None
        self.set_animation_idle()

    # Working Functions
    def start_encounter(self):
        # Refresh time scale
        # if self.ids.battle_hud.ids.toggle_time_scale.state == 'down':
        #     self.ids.battle_hud.time_scale = 1.5
        # Stop Movement
        self.stop_animation()
        Clock.unschedule(self.move_update)
        # Add enemies to skeleton layer
        self.battle_data = self.floor_data.get_battle_data()
        self.ids.hud_layer.opacity = 1
        self.ids.enemy_health.opacity = 0
        self.ids.enemy_names.opacity = 0
        self.ids.icons.opacity = 0

        for character in self.floor_data.get_able_characters()[4:]:
            character.set_invisible()

        enemies = self.battle_data.get_enemies()
        self.enemy_huds = {}
        for index, entity in enumerate(enemies):
            entity.load_skeleton(self._skeleton_loader)
            entity.opacity = 0
            x, y = self.enemy_positions[index]
            entity.set_position(x, y)
            width, height = Refs.app.width, Refs.app.height
            health = EnemyHealth(size_hint=(0.1, 0.1), pos_hint={'center_x': x / width, 'y': y / height}, health=entity.get_health(), max=entity.get_health())
            name = EnemyNamePreview(size_hint=(0.1, 0.089), pos_hint={'center_x': x / width, 'y': y / height + 0.0125}, name=entity.get_name())
            self.enemy_huds[entity] = health
            self.ids.enemy_health.add_widget(health)
            self.ids.enemy_names.add_widget(name)

        # Reset the targeting of enemies
        self.ids.battle_hud.target_specified = False
        self.ids.battle_hud.set_targeting(len(self.battle_data.get_characters()), enemies[0])

        # Start Intro animations
        self.ids.twirl_widget.effects[0].tintr = True
        self.ids.twirl_widget.effects[0].play(self.ids.battle_hud.time_scale)

    def start_boss_encounter(self):
        self.boss_encounter = True
        self.start_encounter()

    def twirl_update(self, instance):
        if self.boss_encounter:
            if self.floor_data.is_in_encounter():
                self.ids.twirl_widget.effects[0].pause()
                self.manager.display_screen('dungeon_main', True, False, boss=True, locked=True)
                self.update_screen_for_encounter()
        else:
            self.update_screen_for_encounter()
        self._last_animation = None

    def update_screen_for_encounter(self):
        disabled = self.floor_data.is_in_encounter()
        opacity = int(disabled)

        if self._mapping_enabled:
            self.ids.map_overlay.opacity = 1 - opacity
        self.ids.info_hud.opacity = 1 - opacity
        self.ids.info_hud.disabled = disabled
        self.ids.inventory.opacity = 1 - opacity
        self.ids.inventory.disabled = disabled
        self.ids.parallax_background.opacity = 1 - opacity
        self.ids.parallax_foreground.opacity = 1 - opacity
        self.ids.battle_background.opacity = opacity
        self.ids.battle_foreground.opacity = opacity
        self.ids.animation_layer.opacity = opacity

        if disabled:
            if self._fade_update is not None:
                self._fade_update.cancel()
                self._fade_update = None
        elif self._exit_distance < 2000 and self._fade_update is None:
            self._fade_update = Clock.schedule_interval(self.fade_update, 1 / 30)

        self.ids.battle_hud.opacity = 1 - opacity
        self.ids.battle_hud.disabled = not disabled
        if not disabled:
            self.ids.battle_hud.leave_battle()
            for character in self.battle_data.get_characters():
                if character is None:
                    continue
                character.set_in_battle(False)
                self.ids.battle_hud.huds[character].in_battle = False
        for hud in self.ids.battle_hud.huds.values():
            hud.hide_overlays()
        self.ids.result_hud.opacity = 0
        self.ids.result_hud.disabled = True

        self._last_animation = 'idle_side'
        for character in self.floor_data.get_able_characters()[:4]:
            character.set_flip_x(False)
            character.set_animation('idle_side', loop=True)

    def twirl_end(self, instance):
        if self.floor_data.is_in_encounter():
            time = self.play_encount_animations()
            self.floor_data.get_characters()[0].add_event_handler('jumpEnd', 'show_enemies', lambda track, event: self.show_enemies())
            Clock.schedule_once(lambda dt: self.show_assist_animations(), time)
        elif self.boss_encounter:
            self.boss_encounter = False
            self.manager.display_screen('dungeon_main', True, False, level=self.level_num, boss=False, locked=True)

    def calculate_assist_effects(self, supports):
        animation_queue = []
        effect_queue = []
        icon_queue = {}
        for support in supports:
            if support is None:
                continue
            skill = support.get_support_skill()
            animations, effects, icons = self.battle_data.use_support_ability(support, skill)
            animation_queue += animations
            effect_queue += effects
            for entity in icons.keys():
                if entity not in icon_queue:
                    icon_queue[entity] = []
                icon_queue[entity] += icons[entity]
        return animation_queue, effect_queue, icon_queue

    def on_turn(self):
        self.ids.battle_hud.ids.active.disabled = True
        self.ids.battle_hud.ids.move_hud.hide_move_labels()
        for enemy in self.battle_data.get_enemies():
            if enemy.is_dead():
                continue
            enemy.select_skill()
        targeted = {}
        characters = self.battle_data.get_characters()
        for index, enemy in enumerate(self.ids.battle_hud.characters_targeting):
            targeted[characters[index]] = enemy
        self._result, animation_queue = self.battle_data.make_turn(targeted)
        self.play_animation(animation_queue, 0)

    def end_turn(self):
        self.ids.battle_hud.ids.active.disabled = False
        self.ids.battle_hud.ids.move_hud.show_move_labels()
        for character, hud in self.ids.battle_hud.huds.items():
            if character.is_dead():
                continue
            hud.ids.icon_tray.update_icons(character)
            hud.show_overlays()

        for enemy, hud in self.enemy_huds.items():
            if enemy.is_dead():
                continue
            hud.ids.icon_tray.update_icons(enemy)

        if self._result is not None:
            if self._result:
                self.show_results()
            else:
                self.show_failure()

    def harvest(self, instance):
        knife = Refs.gc.get_inventory().get_current_harvesting_knife()
        knife.remove_durability(Refs.gc.get_random_wear_amount())

        character = self.floor_data.get_able_characters()[randint(0, len(self.floor_data.get_able_characters()) - 1)]
        character.take_action(Refs.gc.get_stamina_weight() + 1)
        self.floor_data.increase_stat(character.get_index(), 2, Refs.gc.get_random_stat_increase())

        item_counts = {}
        for enemy in self.battle_data.get_enemies():
            drops = Refs.gc['enemies'][enemy.get_base_id()].generate_drop(enemy.get_boost(), knife.get_hardness())
            for (drop_id, drop_count) in drops:
                item = Refs.gc.find_item(drop_id)
                if item not in item_counts:
                    item_counts[item] = 0
                item_counts[item] += drop_count
        self.battle_data.set_dropped_items(item_counts)
        self.ids.result_hud.set_items_obtained(item_counts)

    def show_results(self):
        if self.boss_encounter:
            floor = self.floor_data.get_floor()
            floor.defeat_boss()
            floor.generate_respawn_time()
        # Play Victory Animations for characters
        for character in self.floor_data.get_characters():
            if character.is_dead() or character.is_asleep():
                character.set_invisible()
                continue
            character.set_animation('victory')
            character.set_animation('victory_loop', add=True, loop=True)
            self.lwf_renderer.get_lwf(f'{character.get_id()}_active').set_invisible()
            effect_type = character.get_status_effect()
            if effect_type is not None:
                self.lwf_renderer.get_lwf(f'{character.get_id()}_status_effect_{effect_type}').set_invisible()
                self.lwf_renderer.destroy_lwf(f'{character.get_id()}_status_effect_{effect_type}')
            # Remove any status effect lwfs
        # Hide Battle Hud
        self.ids.battle_hud.opacity = 0
        self.ids.battle_hud.disabled = True
        for hud in self.ids.battle_hud.huds.values():
            hud.hide_overlays()
        # Hide Enemy Healths
        self.ids.enemy_health.opacity = 0
        # Show Inventory
        self.ids.inventory.opacity = 1
        self.ids.inventory.disabled = False
        # Show Enemies Defeated and bind harvest
        self.ids.result_hud.opacity = 1
        self.ids.result_hud.disabled = False
        enemies = {}
        for enemy in self.battle_data.get_enemies():
            enemies[enemy.get_name()] = 1
        self.ids.result_hud.set_enemies_defeated(enemies)
        inventory = Refs.gc.get_inventory()
        if inventory.has_harvesting_knife() is None:
            self.ids.result_hud.disable_harvest()
        else:
            self.ids.result_hud.enable_harvest()
        self.ids.result_hud.bind(on_harvest=self.harvest)
        self.ids.result_hud.bind(on_continue=self.end_encounter)

    def show_failure(self):
        # Hide Battle Hud
        self.ids.battle_hud.opacity = 0
        self.ids.battle_hud.disabled = True
        for hud in self.ids.battle_hud.huds.values():
            hud.hide_overlays()
        # Hide Enemy Healths
        self.ids.enemy_health.opacity = 0
        self.ids.lose_screen.disabled = False
        self.ids.lose_screen.opacity = 1
        self.ids.lose_button.disabled = False
        background_fade_in = Animation(opacity=0.5, duration=1, t='in_expo') + Animation(opacity=1, duration=2, t='out_expo')
        label_fade_in = Animation(opacity=1, duration=3, t='out_expo')
        button_fade_in = Animation(duration=1) + Animation(opacity=1, duration=2, t='in_expo')
        background_fade_in.start(self.ids.lose_background)
        label_fade_in.start(self.ids.lose_label)
        button_fade_in.start(self.ids.lose_button)

    def load_save(self):
        for node in self.floor_data.get_explored():
            self.floor_map.hide_node(node)
        self.floor_map.clear_current_node()

        floor_id = str(self.floor_data.get_floor().get_id())
        save = Refs.gc['save']
        self.floor_map.load_node_exploration(save['map_node_data'][floor_id], save['map_node_counters'][floor_id])

        Refs.gc.reset_floor_data()

        Refs.gs.display_screen('dungeon_main', True, False, level=0, boss=False)

    def refresh_harvest(self):
        inventory = Refs.gc.get_inventory()
        if inventory.has_harvesting_knife() is None:
            self.ids.result_hud.disable_harvest()
        else:
            self.ids.result_hud.enable_harvest()

    def end_encounter(self, instance):
        self.enemy_huds = {}
        self.ids.enemy_health.clear_widgets()
        self.ids.enemy_names.clear_widgets()

        duration = 0.2 / self.ids.battle_hud.time_scale
        anim = Animation(opacity=0, duration=duration)
        anim.start(self.ids.result_hud)
        Clock.schedule_once(lambda dt: self.ids.result_hud.reset(),duration)
        self.floor_data.end_encounter()
        self.ids.battle_hud.characters_targeting = []

        # Play Encounter Animation and animate characters back into floor positions
        time = self.play_encount_animations(False)
        def play_twirl(time_scale):
            self.ids.twirl_widget.effects[0].tintr = False
            self.ids.twirl_widget.effects[0].play(time_scale)
        Clock.schedule_once(lambda dt, s=self.ids.battle_hud.time_scale: play_twirl(s), time)
        self.ids.battle_hud.time_scale = 1
        # clear icon tray
        for hud in self.ids.battle_hud.huds.values():
            hud.ids.icon_tray.clear_icons()

    def update_hud(self, animation):
        # Update Mana
        skill = None
        if 'skill' in animation:
            skill = animation['skill']
        entity = animation['entity']
        type = animation['type']

        if entity.is_character():
            hud = self.ids.battle_hud.huds[entity]
            hud.special_amount = entity.get_special_amount()
            if type not in ('health_rot', 'health_dot'):
                hud.mana -= entity.get_mana_cost(skill)

        # Update health for targets
        for target in animation['targets']:
            # Get huds
            if target.is_character():
                hud = self.ids.battle_hud.huds[target]
            else:
                hud = self.enemy_huds[target]

            # if animation['type'] == 'ailment_cure':
            #     # Clear status effects
            #     effect_lwf, type = hud.get_status_effect_lwf()
            #     target.set_status_effect(None)
            #     if effect_lwf is not None:
            #         effect_lwf.set_invisible()
            #         hud.set_status_effect_lwf(None, -1)
            #         self.lwf_renderer.destroy_lwf(f'{target.get_id()}_status_effect')
                # Clear status effects from tray

            # Update icons
            if 'icons' in animation:
                icons = animation['icons']
                icon_tray = hud.ids.icon_tray
                icon_tray.apply_icons(icons)

            # Health and Mana Updates
            target_marker = animation['markers'][target][0]
            if target_marker is None:
                continue
            damage_type, damage = target_marker
            if damage_type in ('damage', 'crit_damage', 'dot'):
                hud.health -= damage
            elif damage_type in ('health',):
                hud.health += damage
            elif damage_type in ('mana',):
                hud.mana -= damage
            else:
                print('Unimplemented HUD update')

    def replace_hud(self, dead_index, dead_character, replacement_character):
        hud = self.ids.battle_hud.huds[replacement_character]
        replacement_index = hud.index
        hud.in_battle = True
        hud.index = dead_index
        hud.pos_hint = {'x': 0.002 + 0.102 * dead_index, 'y': 0.005}

        other_hud = self.ids.battle_hud.huds[dead_character]
        other_hud.pos_hint = {'x': 0.002 + 0.102 * replacement_index, 'y': 0.005}
        other_hud.index = replacement_index

        self.floor_data.swap_character_order(dead_character, replacement_character)
        self.ids.battle_hud.ids.move_hud.replace_character(dead_index, replacement_character)
        dead_character.set_invisible()

    def show_markers(self, animation):
        for target in animation['targets']:
            markers = animation['markers'][target]
            if markers[0] is not None:
                damage_type, damage = markers[0]
                self.ids.marker_layer.add_widget(Marker(75, self.ids.battle_hud.time_scale, type=damage_type, value=int(damage), height=40, size_hint=(None, None), pos_hint={'center_x': (target.x) / Refs.app.width, 'y': (target.y + 200) / Refs.app.height}))
                if damage_type in ('damage', 'crit_damage') and damage > 0:
                    target.set_animation('damage')
            death = False
            for index, marker in enumerate(markers[1:]):
                if marker == 'counter' and animation['is_counter']:
                    continue
                if marker.startswith('death'):
                    if target.is_character():
                        hud_index = int(marker.split('_')[1])
                        target.set_animation('death', add=True)
                        self.ids.battle_hud.huds[target].handle_death()
                        self.ids.battle_hud.huds[target].in_battle = False
                        target.set_in_battle(False)
                        self.ids.battle_hud.handle_death(hud_index)
                        if target.has_status_effect():
                            self.lwf_renderer.destroy_lwf(f'{target.get_id()}_status_effect')
                    else:
                        self.enemy_huds[target].opacity = 0
                        anim = Animation(opacity=0, duration=0.2 / self.ids.battle_hud.time_scale)
                        anim.start(target)
                        anim.start(self.enemy_huds[target])

                        death_lwf = self.lwf_renderer.register_lwf('812109104/812109104.lwf', f'{target.get_id()}_death', load_texture)
                        scale = Refs.app.width / 1920 * 10
                        death_lwf.scale_for_width(scale, scale)
                        death_lwf.property.move_to(*target.get_position())
                        death_lwf.add_event_handler('end', lambda movie, button, t=target: self.lwf_renderer.destroy_lwf(f'{t.get_id()}_death'))
                        self.ids.battle_hud.handle_enemy_death(self.battle_data.get_enemies(), target)

                    death = True
                else:
                    self.ids.marker_layer.add_widget(Marker(75, self.ids.battle_hud.time_scale, type=marker, height=40, size_hint=(None, None), pos_hint={'center_x': (target.x) / Refs.app.width, 'y': (target.y + 160 - 40 * index) / Refs.app.height}))
            if not death:
                # effect, idle =
                # effect = target.get_status_effect_type()
                # if effect:
                #     Refs.log(f'Show effect after damage')
                    # self.show_status_effect(target, effect, 0)
                    # idle = 'status_ailment'
                    # Clock.schedule_once(lambda dt, t=target: status_lwf.set_visible(), 0.1 / self.ids.battle_hud.time_scale)
                target.set_animation(target.get_idle_animation(), add=True, loop=True)

    def create_status_effect_lwf(self, entity, effect_type):
        types = {27: '810000021', 28: '810000033', 29: '810000034', 30: '810000022', 31: '810000023', 32: '810000024', 33: '810000026', 34: '810000031', 35: '810000024'}
        specific_name = f'{entity.get_id()}_status_effect_{effect_type}'

        effect_lwf = self.lwf_renderer.register_lwf(f'{types[effect_type]}/{types[effect_type]}.lwf', specific_name, load_texture)
        scale = Refs.app.width / 1920 * 10
        effect_lwf.scale_for_width(scale, scale)
        x, y = entity.get_position()
        w, h = entity.get_skeleton().getSize()
        effect_lwf.property.move_to(x, y + h / 3)
        effect_lwf.add_event_handler('end', lambda movie, button: self.lwf_renderer.destroy_lwf(specific_name))
        return effect_lwf

    # def show_status_effect(self, entity, effect_type, time):
    #     hud = self.ids.battle_hud.huds[entity]
    #     status_lwf, etype = hud.get_status_effect_lwf()
    #     # effect_type = entity.get_status_effect()
    #     if status_lwf and etype != effect_type:
    #         self.lwf_renderer.destroy_lwf(f'{entity.get_id()}_status_effect')
    #         status_lwf = None
    #     if not status_lwf:
    #         self.create_status_effect_lwf(entity)
    #     status_lwf, type = hud.get_status_effect_lwf()
    #     status_lwf.set_visible()
    #     Clock.schedule_once(lambda dt, s=status_lwf: s.set_visible(), time)

    def play_animation(self, queue, index, debug=False):
        if debug:
            Refs.log(f'Play animation {index}')
        animation = queue[index]
        entity = animation['entity']

        fade_in_duration = 0.1 / self.ids.battle_hud.time_scale
        show_duration = 0.5 / self.ids.battle_hud.time_scale
        fade_out_duration = 0.1 / self.ids.battle_hud.time_scale

        if animation['type'] in ('attack', 'cause_effect', 'heal', 'ailment_cure'):
            # Hide status LWF
            effect_type = entity.get_status_effect()
            effect_lwf = None
            if effect_type is not None:
                effect_lwf = self.lwf_renderer.get_lwf(f'{entity.get_id()}_status_effect_{effect_type}')
                effect_lwf.set_invisible()
            # Attack Animation
            entity.set_animation(animation['skill'].get_animation_name())
            entity.set_animation(entity.get_idle_animation(), loop=True, add=True)

            # Move Name Animation
            attack_name = animation['skill'].get_animation_path()
            self.ids[entity.get_id()].ids.label.text = animation['skill'].get_name()
            anim = Animation(opacity=1, duration=fade_in_duration) + Animation(duration=show_duration) + Animation(opacity=0, duration=fade_out_duration)
            anim.start(self.ids[entity.get_id()])

            # Create LWF
            name = f'{entity.get_id()}_attack_{randint(1, 1000000)}'
            attack_lwf = self.lwf_renderer.register_lwf(f'{attack_name}/{attack_name}.lwf', name, load_texture)
            def set_lwf_visible(track, event):
                attack_lwf.set_visible()
                return True
            entity.add_event_handler('hit', 'attack_hit', set_lwf_visible)
            scale = Refs.app.width / 1920 * 10
            attack_lwf.scale_for_width(scale, scale)

            stype = animation['skill'].get_type()
            starget = animation['skill'].get_target()
            target = animation['targets'][0]

            # if effect and debug:
            #     Refs.log(f'Show effect after taking attack')

            # The party animations need to be moved to the center of the screen!
            if attack_name.startswith('8121045') or attack_name.startswith('8121043'):
                width, height = Refs.app.width, Refs.app.height
                attack_lwf.property.move_to(width * 0.5, height * 0.5)
            elif starget == FOE:
                attack_lwf.property.move_to(*target.get_position())
            elif starget == SELF:
                attack_lwf.property.move_to(*entity.get_position())
            elif starget == FOES:
                if entity.is_character():
                    attack_lwf.property.move_to(*self.enemy_party)
                else:
                    attack_lwf.property.move_to(*self.char_party)
            else:
                if entity.is_character():
                    attack_lwf.property.move_to(*self.char_party)
                else:
                    attack_lwf.property.move_to(*self.enemy_party)

            # Do we need to target the right side of the screen
            if entity.is_enemy() and starget in (FOE, FOES) or (entity.is_character() and starget in (SELF, ALLIES)):  #
                attack_lwf.property.scale(-1, 1)
            attack_lwf.set_invisible()

            attack_lwf.add_event_handler('common_hit', lambda movie, button: self.update_hud(animation))
            attack_lwf.add_event_handler('common_hit', lambda movie, button: self.show_markers(animation))
            if len(queue) > index + 1:
                attack_lwf.add_event_handler('end', lambda movie, button: self.play_animation(queue, index + 1))
            else:
                attack_lwf.add_event_handler('end', lambda movie, button: self.end_turn())
            if effect_lwf is not None and not entity.is_dead():
                attack_lwf.add_event_handler('end', lambda movie, button, el=effect_lwf: el.set_visible())
            attack_lwf.add_event_handler('end', lambda movie, button: self.lwf_renderer.destroy_lwf(name))
        elif animation['type'] == 'health_rog':  # 810000027
            heal_lwf = self.lwf_renderer.register_lwf(f'810000027/810000027.lwf', f'{entity.get_id()}_heal_rog', load_texture)
            scale = Refs.app.width / 1920 * 10
            heal_lwf.scale_for_width(scale, scale)
            heal_lwf.property.move_to(*entity.get_position())
            if entity.is_enemy():
                heal_lwf.property.scale(-1, 1)

            heal_lwf.add_event_handler('hit', lambda movie, button: self.update_hud(animation))
            heal_lwf.add_event_handler('hit', lambda movie, button: self.show_markers(animation))

            if len(queue) > index + 1:
                if queue[index + 1]['type'] == 'health_rog':
                    self.play_animation(queue, index + 1)
                else:
                    heal_lwf.add_event_handler('end', lambda movie, button: self.play_animation(queue, index + 1))
                heal_lwf.add_event_handler('end', lambda movie, button: self.lwf_renderer.destroy_lwf(f'{entity.get_id()}_heal_rog'))
            else:
                heal_lwf.add_event_handler('end', lambda movie, button: self.end_turn())
                heal_lwf.add_event_handler('end', lambda movie, button: self.lwf_renderer.destroy_lwf(f'{entity.get_id()}_heal_rog'))
        elif animation['type'] == 'mana_rog':
            mana_lwf = self.lwf_renderer.register_lwf(f'810000027/810000027.lwf', f'{entity.get_id()}_mana_rog', load_texture)
            scale = Refs.app.width / 1920 * 10
            mana_lwf.scale_for_width(scale, scale)
            mana_lwf.property.move_to(*entity.get_position())
            if entity.is_enemy():
                mana_lwf.property.scale(-1, 1)

            mana_lwf.add_event_handler('hit', lambda movie, button: self.update_hud(animation))
            mana_lwf.add_event_handler('hit', lambda movie, button: self.show_markers(animation))

            if len(queue) > index + 1:
                if queue[index + 1]['type'] == 'mana_rog':
                    self.play_animation(queue, index + 1)
                else:
                    mana_lwf.add_event_handler('end', lambda movie, button: self.play_animation(queue, index + 1))
                mana_lwf.add_event_handler('end', lambda movie, button: self.lwf_renderer.destroy_lwf(f'{entity.get_id()}_mana_rog'))
            else:
                mana_lwf.add_event_handler('end', lambda movie, button: self.end_turn())
                mana_lwf.add_event_handler('end', lambda movie, button: self.lwf_renderer.destroy_lwf(f'{entity.get_id()}_mana_rog'))
        elif animation['type'] == 'health_dot':
            self.update_hud(animation)
            self.show_markers(animation)

            duration = 0.3 / self.ids.battle_hud.time_scale

            if len(queue) > index + 1:
                if queue[index + 1]['type'] == 'health_dot':
                    self.play_animation(queue, index + 1)
                else:
                    Clock.schedule_once(lambda dt: self.play_animation(queue, index + 1), duration)
            else:
                Clock.schedule_once(lambda dt: self.end_turn(), duration)
        elif animation['type'] == 'enter_battle':
            load_duration = 0.05
            enter_duration = 1.25 / self.ids.battle_hud.time_scale
            leave_duration = 0.3 / self.ids.battle_hud.time_scale
            total_duration = load_duration + enter_duration + leave_duration
            hud_indicies = animation['hud_index'].split('_')
            for entity_index, entity in enumerate(animation['entities']):
                replacement = animation['targets'][entity_index]
                hud_index = int(hud_indicies[entity_index])

                x, y = entity.get_position()
                enter_duration = x / Refs.app.width / 0.548 / self.ids.battle_hud.time_scale
                x1 = Refs.app.width * 1.25
                replacement.set_position(x1, y)
                replacement.set_animation('run_side', loop=True)
                replacement.set_flip_x(False)
                replacement.set_visible()
                replacement.set_in_battle(True)

                enter_animation = Animation(duration=load_duration) + Animation(x=x, duration=enter_duration)
                leave_animation = Animation(duration=enter_duration) + Animation(opacity=0, duration=leave_duration)

                enter_animation.start(replacement)
                leave_animation.start(entity)
                # Move huds around
                # replacement.set_animation(replacement.get_idle_animation(), loop=True)
                Clock.schedule_once(lambda dt, r=replacement: r.set_animation(r.get_idle_animation(), loop=True), enter_duration)
                # if effect:
                #     Refs.log(f'Show effect after enter battle')

                Clock.schedule_once(lambda dt, h=hud_index, e=entity, r=replacement: self.replace_hud(h, e, r), enter_duration)

                first_enemy = None
                enemies = self.battle_data.get_alive_enemies()
                if len(enemies) > 0:
                    first_enemy = enemies[0]
                self.ids.battle_hud.update_targeting_from_replacement(hud_index, first_enemy)

            supports = []
            for replacement in animation['targets']:
                if replacement.get_support() is not None:
                    supports.append(replacement.get_support())

            # Play assist animations and apply effects
            if len(supports) == 0:
                if len(queue) > index + 1:
                    Clock.schedule_once(lambda dt: self.play_animation(queue, index + 1), total_duration)
                else:
                    Clock.schedule_once(lambda dt: self.end_turn(), total_duration)
            else:
                def play_support_animation(dt):
                    assist_lwf = self._play_assist_lwf(supports)
                    if len(queue) > index + 1:
                        assist_lwf.add_event_handler('end', lambda movie, button: self.play_animation(queue, index + 1))
                    else:
                        assist_lwf.add_event_handler('end', lambda movie, button: self.end_turn())
                    assist_lwf.add_event_handler('end', lambda movie, button: self.lwf_renderer.destroy_lwf('Assist Cutin'))
                Clock.schedule_once(play_support_animation, enter_duration)
        elif animation['type'] == 'set_status_effect':
            Refs.log(f'Show Status Effect applied to {entity.get_name()}')

            hud = self.ids.battle_hud.huds[entity]
            effect_lwf, effect_type = hud.get_status_effect_lwf()

            if effect_lwf is not None and effect_type != animation['effect']:
                effect_lwf.set_invisible()
                self.lwf_renderer.destroy_lwf(f'{entity.get_id()}_status_effect_{effect_type}')
                effect_lwf = None
            if effect_lwf is None:
                effect_lwf = self.create_status_effect_lwf(entity, animation['effect'])
            effect_lwf.set_visible()
            hud.set_status_effect_lwf(effect_lwf, animation['effect'])
            hud.ids.icon_tray.apply_icons([str(animation['effect'])])
            entity.set_status_effect(animation['effect'])
            entity.set_animation(entity.get_idle_animation(), loop=True)

            if len(queue) > index + 1:
                self.play_animation(queue, index + 1)
            else:
                self.end_turn()
        elif animation['type'] == 'end_status_effect':
            Refs.log(f'Remove Status Effect from {entity.get_name()}')
            # We just want to hide the status effect; Destroy happens on battle end
            hud = self.ids.battle_hud.huds[entity]
            effect_lwf, effect_type = hud.get_status_effect_lwf()
            if effect_lwf is not None:
                effect_lwf.set_invisible()
                entity.set_status_effect(None)
                entity.set_animation(entity.get_idle_animation(), loop=True)
                hud.ids.icon_tray.remove_icons([str(effect_type)])

            if len(queue) > index + 1:
                self.play_animation(queue, index + 1)
            else:
                self.end_turn()
        else:
            Refs.log(f'{queue[index:]}', 'error', 'Battle')
            Refs.log(f'Unimplemented animation type {animation["type"]}', 'error', 'Battle')

