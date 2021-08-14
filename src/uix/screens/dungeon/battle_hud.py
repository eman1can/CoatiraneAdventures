from kivy.properties import BooleanProperty, BoundedNumericProperty, Clock, ListProperty, NumericProperty, ObjectProperty, StringProperty

from kivy.animation import Animation
from kivy.uix.hovertogglebutton import HoverToggleButton
from kivy.uix.relativelayout import RelativeLayout

from loading.kv_loader import load_kv
from modules.gradient import Gradient
from refs import Refs
from uix.screens.dungeon.lwf_renderer import load_texture

load_kv(__name__)


"""
The move button should show description either on a hover or an extended click
"""


class MoveButton(HoverToggleButton):
    def __init__(self, **kwargs):
        self.register_event_type('on_description')
        self.register_event_type('on_hide_description')
        super().__init__(**kwargs)

    def on_move_hover(self, x, y):
        print(x, y)
        super().on_move_hover(x, y)

    def on_enter(self):
        print('Enter')
        self.show_description()

    def on_exit(self):
        print('Exit')
        self.hide_description()

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        if self.disabled:
            return False
        if super().on_touch_down(touch):
            Clock.schedule_once(self.show_description, 0.3)
            if self.state == 'down':
                return True
        return False

    def on_touch_up(self, touch):
        if super().on_touch_up(touch):
            Clock.unschedule(self.show_description)
            self.hide_description()
            return True
        return False

    def show_description(self, dt=0):
        self.dispatch('on_description')

    def on_description(self):
        pass

    def hide_description(self):
        self.dispatch('on_hide_description')

    def on_hide_description(self):
        pass


class CharacterHud(RelativeLayout):
    special_amount = BoundedNumericProperty(0, min=0, max=10)  # 0 → 1000

    index = NumericProperty(0)

    revive = NumericProperty(0)
    revive_max = NumericProperty(10)

    stamina = NumericProperty(0)
    stamina_max = NumericProperty(1000)
    health = NumericProperty(0)
    health_max = NumericProperty(1000)
    mana = NumericProperty(0)
    mana_max = NumericProperty(1000)
    character_img_src = StringProperty('')

    in_battle = BooleanProperty(False)
    is_disabled = BooleanProperty(False)  # asleep or dead

    def __init__(self, **kwargs):
        self.register_event_type('on_toggle_move_hud')

        self.active_lwf = None
        self.select_lwf = None
        self.status_effect_lwf = None
        self.status_effect_type = None
        self.selected = True
        super().__init__(**kwargs)

    def set_character(self, character, lwf_renderer):
        self.character_img_src = character.get_image('preview')
        self.health = character.get_battle_health()
        self.health_max = character.get_health()
        self.mana = character.get_battle_mana()
        self.mana_max = character.get_mana()
        self.stamina = character.get_stamina()
        self.stamina_max = character.get_stamina_max()
        self.revive = 10 - character.get_death_rest_count()

        self.in_battle = character.in_battle()
        self.is_disabled = character.is_dead() or character.is_asleep()

        scale = Refs.app.width * 0.1 / 165 * 10
        x, y = Refs.app.width * (0.052 + self.pos_hint['x']), 0.0935 * Refs.app.height

        self.active_lwf = lwf_renderer.register_lwf('810000000/810000000.lwf', f'{character.get_id()}_active', load_texture)
        self.active_lwf.scale_for_width(scale, scale)
        self.active_lwf.set_invisible()
        self.active_lwf.property.move_to(x, y)

        self.select_lwf = lwf_renderer.register_lwf('810000001/810000001.lwf', f'{character.get_id()}_select', load_texture)
        self.select_lwf.scale_for_width(scale, scale)
        self.select_lwf.set_invisible()
        self.select_lwf.property.move_to(x, y)

    def set_status_effect_lwf(self, lwf, effect_type):
        self.status_effect_lwf = lwf
        self.status_effect_type = effect_type

    def get_status_effect_lwf(self):
        return self.status_effect_lwf, self.status_effect_type

    def on_pos_hint(self, instance, pos_hint):
        if self.active_lwf is None or self.select_lwf is None:
            return
        x, y = Refs.app.width * (0.052 + self.pos_hint['x']), 0.0935 * Refs.app.height
        self.active_lwf.property.move_to(x, y)
        self.select_lwf.property.move_to(x, y)

    def on_health(self, instance, health):
        if health <= 0:
            self.is_disabled = True

    def on_stamina(self, isntance, stamina):
        if stamina <= 0:
            self.is_disabled = True

    def generate_texture(self, type, width, max_width, height):
        if type == 'mana':
            return Gradient.horizontal(int(width), int(max_width), int(height), (147, 222, 255, 255), (255, 255, 255, 255))
        elif type == 'health':
            return Gradient.horizontal(int(width), int(max_width), int(height), (168, 255, 195, 255), (255, 255, 255, 255))
        elif type == 'special':
            return Gradient.horizontal(int(width), int(max_width), int(height), (192, 192, 192, 255), (255, 92, 86, 255))
        elif type == 'stamina':
            return Gradient.horizontal(int(width), int(max_width), int(height), (192, 192, 192, 255), (255, 127, 182, 255))

    def toggle(self):
        if self.is_disabled or not self.in_battle:
            return
        self.toggle_animations()
        self.dispatch('on_toggle_move_hud', self.index, self.special_amount >= 5)

    def toggle_animations(self):
        self.selected = not self.selected
        if not self.selected:
            self.active_lwf.set_invisible()
            self.select_lwf.set_visible()
        else:
            self.active_lwf.set_visible()
            self.select_lwf.set_invisible()

    def hide_overlays(self):
        self.select_lwf.set_invisible()
        self.active_lwf.set_invisible()
        self.selected = False

    def show_overlays(self):
        if self.is_disabled or not self.in_battle:
            return
        self.select_lwf.set_visible()

    def enable_button(self):
        if self.is_disabled or not self.in_battle:
            return
        self.ids.button.disabled = False

    def disable_button(self):
        self.ids.button.disabled = True

    def handle_death(self):
        self.disable_button()
        self.hide_overlays()
        self.ids.icon_tray.clear_icons()
        self.is_disabled = True

    def clear_icon_trays(self):
        self.ids.icon_tray.clear_icons()

    def on_in_battle(self, instance, boolean):
        if self.in_battle:
            self.show_overlays()
            self.enable_button()
        else:
            self.hide_overlays()
            self.disable_button()

    def on_toggle_move_hud(self, index, special):
        pass

    def on_touch_hover(self, touch):
        return False


class MoveHud(RelativeLayout):
    move_hud_open = BooleanProperty(False)
    index_open = NumericProperty(0)
    selected_moves = ListProperty([])
    all_moves = ListProperty([])
    dead = ListProperty([False, False, False, False])

    def __init__(self, **kwargs):
        self.register_event_type('on_move_hud_opened')
        self.register_event_type('on_move_hud_closed')
        super().__init__(**kwargs)
        self.chars = None

    def set_moves(self, move_list):
        for index, move in enumerate(move_list[:20]):
            if index % 5 == 0:
                self.selected_moves.append(move)
                self.ids[f'move_label_{int(index / 5)}'].ids.label.text = move.get_name()
                self.ids[f'move_label_{int(index / 5)}'].opacity = 1
        self.all_moves = move_list

    def hide_move_labels(self):
        for index in range(4):
            self.ids[f'move_label_{index}'].opacity = 0

    def show_move_labels(self):
        for index in range(4):
            if not self.chars[index].is_dead():
                self.ids[f'move_label_{index}'].opacity = 1

    def replace_character(self, index, character):
        self.all_moves[index * 5] = character.get_skill(0)
        self.all_moves[index * 5 + 1] = character.get_skill(1)
        self.all_moves[index * 5 + 2] = character.get_skill(3)
        self.all_moves[index * 5 + 3] = character.get_skill(5)
        self.all_moves[index * 5 + 4] = character.get_skill(7)
        self.selected_moves[index] = self.all_moves[index * 5]
        self.chars[index] = character
        self.dead[index] = False
        self.ids[f'move_label_{index}'].ids.label.text = self.selected_moves[index].get_name()

    def set_characters(self, char_list):
        self.chars = char_list

    def show_description(self, index):
        self.ids.move_bar_hover.opacity = 1
        move = self.all_moves[self.index_open * 5 + index]
        self.ids.label.text = move.get_description()

    def hide_description(self):
        self.ids.move_bar_hover.opacity = 0

    def open_move_hud(self, index, special):
        if not self.move_hud_open:
            self.move_hud_open = True
            self.ids.move_bar_full.opacity = 1
            for sub_index in range(5):
                self.ids[f'move_button_{sub_index}'].disabled = False if sub_index < 4 else not special
                self.ids[f'move_label_{sub_index}'].opacity = 0
        self.index_open = index
        selected_index = self.all_moves.index(self.selected_moves[index])
        for sub_index in range(5):
            self.ids[f'move_button_{sub_index}'].state = 'normal'
        self.ids[f'move_button_{selected_index % 5}'].state = 'down'
        self.ids.move_arrow.pos_hint = {'center_x': 0.053 + 0.102 * index}
        index *= 5
        for sub_index in range(5):
            self.ids[f'move_button_{sub_index}'].text = self.all_moves[index + sub_index].get_name()
        self.dispatch('on_move_hud_opened', self.index_open)

    def on_move_hud_opened(self, index):
        pass

    def select_move(self, number):
        self.selected_moves[self.index_open] = self.all_moves[self.index_open * 5 + number]
        self.ids[f'move_label_{self.index_open}'].text = self.selected_moves[self.index_open].get_name()
        self.chars[self.index_open].select_skill(number)

    def on_dead(self, instance, dead):
        for sub_index in range(4):
            if dead[sub_index] and len(self.all_moves) > 5 * sub_index:
                self.ids[f'move_label_{sub_index}'].opacity = 0

    def close_move_hud(self):
        self.move_hud_open = False
        self.ids.move_bar_full.opacity = 0
        self.ids.move_bar_hover.opacity = 0
        for sub_index in range(4):
            if len(self.all_moves) > 5 * sub_index and not self.dead[sub_index]:
                self.ids[f'move_label_{sub_index}'].opacity = 1
                self.ids[f'move_label_{sub_index}'].ids.label.text = self.selected_moves[sub_index].get_name()
            else:
                self.ids[f'move_label_{sub_index}'].opacity = 0
            self.ids[f'move_button_{sub_index}'].disabled = True
        self.ids.move_button_4.disabled = True
        self.dispatch('on_move_hud_closed')

    def on_move_hud_closed(self):
        pass


class BattleHud(RelativeLayout):
    in_battle = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_turn')
        self.register_event_type('on_toggle_icons')
        super().__init__(**kwargs)

        self.huds = {}

        self.inspection_entity = None

        self.characters_targeting = []
        self.target_specified = False
        self.time_scale = 1
        self._turn = 0
        self._encounter_text = ''

    def on_kv_post(self, base_widget):
        moves = []
        floor_data = Refs.gc.get_floor_data()
        self._encounter_text = f'Encounter {floor_data.get_encounters()}'
        self.ids.encounter_label.text = f'{self._encounter_text}\nTurn {self._turn}'
        characters = floor_data.get_able_characters()
        for index, character in enumerate(characters):
            character_hud = CharacterHud(size_hint=(0.1, 0.177), pos_hint={'x': 0.002 + 0.102 * index, 'y': 0.005}, index=index)
            character_hud.bind(on_toggle_move_hud=self.toggle_move_hud)
            moves.append(character.get_skill(0))
            moves.append(character.get_skill(1))
            moves.append(character.get_skill(3))
            moves.append(character.get_skill(5))
            moves.append(character.get_skill(7))
            self.huds[character] = character_hud
            self.ids.active.add_widget(character_hud)
        self.ids.move_hud.set_moves(moves)
        self.ids.move_hud.set_characters(characters)
        self.ids.move_hud.bind(on_move_hud_opened=self.display_target)
        self.ids.move_hud.bind(on_move_hud_closed=self.hide_target)

    def set_targeting(self, count, first_enemy):
        for index in range(count):
            self.characters_targeting.append(first_enemy)

    def update_targeting_from_replacement(self, index, first_enemy):
        if self.target_specified:
            return
        self.characters_targeting[index] = first_enemy

    def toggle_move_hud(self, instance, index, special):
        if self.ids.move_hud.move_hud_open and self.ids.move_hud.index_open == index:
            self.ids.move_hud.close_move_hud()
        else:
            self.ids.move_hud.open_move_hud(index, special)

    def close_move_hud(self):
        if self.ids.move_hud.move_hud_open:
            self.ids.move_hud.close_move_hud()
            list(self.huds.values())[self.ids.move_hud.index_open].toggle_animations()

    def enter_battle(self):
        self.in_battle = True
        self.ids.move_hud.opacity = 1
        self.ids.turn_button.opacity = 1
        # self.ids.encounter_label.opacity = 1
        # self.ids.toggle_time_scale.opacity = 1
        # self.ids.toggle_icons.opacity = 1
        self.ids.info.opacity = 1

    def leave_battle(self):
        self.in_battle = False
        self.ids.move_hud.opacity = 0
        self.ids.turn_button.opacity = 0
        # self.ids.encounter_label.opacity = 0
        # self.ids.toggle_time_scale.opacity = 0
        # self.ids.toggle_icons.opacity = 0
        self.ids.info.opacity = 0

    def take_turn(self):
        self.close_move_hud()
        self.dispatch('on_turn')
        self._turn += 1
        self.ids.encounter_label.text = f'{self._encounter_text}\nTurn {self._turn}'
        for hud in self.huds.values():
            hud.hide_overlays()

    def on_turn(self):
        pass

    def get_hud(self, character):
        return self.huds[character]

    def handle_death(self, index):
        self.ids.move_hud.dead[index] = True

    def toggle_icons(self):
        for hud in self.huds.values():
            hud.ids.icon_tray.opacity = 1 - hud.ids.icon_tray.opacity
        self.dispatch('on_toggle_icons')

    def toggle_time_scale(self):
        self.time_scale = 2.5 - self.time_scale

    def toggle_auto_battle(self):
        pass

    def on_toggle_icons(self):
        pass

    def on_touch_down(self, touch):
        if self.ids.active.disabled:
            return super().on_touch_down(touch)
        dx, dy = touch.pos
        floor_data = Refs.gc.get_floor_data()
        for entity in floor_data.get_characters() + floor_data.get_battle_data().get_enemies():
            x, y = entity.get_position()
            width, height = entity.get_skeleton().getSize()
            if x - width / 2 < dx < x + width / 2 and y < dy < y + height:
                self.inspection_entity = entity
                Clock.schedule_once(self.show_inspection, 0.75)
                return True
        result = super().on_touch_down(touch)
        if result is None:
            self.close_move_hud()
        return result

    def on_touch_up(self, touch):
        if self.inspection_entity is not None:
            Clock.unschedule(self.show_inspection)
            if self.inspection_entity.is_enemy():
                if self.ids.move_hud.move_hud_open:
                    # If the move hud is open, we are specifiying a single target
                    self.characters_targeting[self.ids.move_hud.index_open] = self.inspection_entity
                    self.animate_targeting_circle(self.inspection_entity)
                    self.target_specified = False
                else:
                    if not self.target_specified or self.inspection_entity != self.characters_targeting[0]:
                        self.target_specified = True
                        self.animate_targeting_circle(self.inspection_entity)
                        for index in range(len(self.characters_targeting)):
                            self.characters_targeting[index] = self.inspection_entity
                    elif self.inspection_entity == self.characters_targeting[0]:
                        self.target_specified = False
                        self.ids.targeting_circle.opacity = 0

            self.inspection_entity = None
        result = super().on_touch_up(touch)
        return result

    def display_target(self, instance, index):
        entity = self.characters_targeting[index]
        self.ids.targeting_circle.opacity = 1
        self.set_targeting_circle_pos(entity)

    def hide_target(self, instance):
        if not self.target_specified:
            self.ids.targeting_circle.opacity = 0

    def handle_enemy_death(self, enemies, dead_enemy):
        not_dead_enemies = [enemy for enemy in enemies if not enemy.is_dead()]
        if len(not_dead_enemies) == 0:
            for index in range(len(self.characters_targeting)):
                self.characters_targeting[index] = None
            if self.target_specified:
                self.target_specified = False
                self.ids.targeting_circle.opacity = 0
        else:
            if self.target_specified and self.characters_targeting[0] == dead_enemy:
                self.target_specified = False
                self.ids.targeting_circle.opacity = 0
            for index in range(len(self.characters_targeting)):
                if self.characters_targeting[index] == dead_enemy:
                    self.characters_targeting[index] = not_dead_enemies[0]

    def set_targeting_circle_pos(self, entity):
        x, y = entity.get_position()
        width, height = entity.get_skeleton().getSize()
        yoff = height / 4
        twidth, theight = Refs.app.width, Refs.app.height
        self.ids.targeting_circle.pos_hint = {'center_x': x / twidth, 'y': (y + yoff) / theight}

    def animate_targeting_circle(self, entity):
        self.set_targeting_circle_pos(entity)
        self.ids.targeting_circle.opacity = 1
        target_animation = Animation(size_hint_x=0.07, duration=0.2) + Animation(size_hint_x=0.075, duration=0.2)
        target_animation.start(self.ids.targeting_circle)

    def show_inspection(self, dt):
        if self.inspection_entity.is_dead():
            return
        Refs.gp.display_popup(self, 'inspection', self.inspection_entity)
        self.inspection_entity = None
