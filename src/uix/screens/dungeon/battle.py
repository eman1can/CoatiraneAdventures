# Project Imports
from game import skill
from refs import Refs
from spine.animation.animationstate import AnimationState, AnimationStateAdapter
from spine.animation.animationstatedata import AnimationStateData
from spine.skeleton.skeletonrenderer import SkeletonRenderer

# UIX Imports
from uix.modules.screen import Screen

# Kivy Imports
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty, StringProperty, BoundedNumericProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout

# Standard Library Imports
import random

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class ParallaxBackground(RelativeLayout):
    def __init__(self, **kwargs):
        self.source = 'screens/dungeon_battle/background.png'
        super().__init__(**kwargs)


class Encounter:
    def __init__(self, old_encounter, distance, **kwargs):
        if old_encounter is None:
            self.encounter_x = distance
        else:
            self.encounter_x = old_encounter.get_x() + distance

    def get_x(self):
        return self.encounter_x


class CharacterHud(RelativeLayout):
    special_amount = BoundedNumericProperty(0, min=0, max=1000)  # 0 → 1000

    index = NumericProperty(0)

    health = NumericProperty(0)
    health_max = NumericProperty(1000)
    mana = NumericProperty(0)
    mana_max = NumericProperty(1000)
    character_img_src = StringProperty('')

    moves = ListProperty([])

    def __init__(self, **kwargs):
        self.register_event_type('on_open_mhud')
        super().__init__(**kwargs)

    def set_character(self, character):
        self.character_img_src = character.get_image('preview')
        self.health = character.get_health()
        self.health_max = character.get_health()
        self.mana = character.get_mana()
        self.mana_max = character.get_mana()

    def on_open_mhud(self):
        pass

    def on_touch_hover(self, touch):
        return False


class MoveHud(RelativeLayout):
    selected_move = ObjectProperty(None, allownone=True)
    move_hud_open = BooleanProperty(False)

    hint_x = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_moves(self, move_list):
        self.ids.move_select.clear_widgets()
        for move in move_list:
            button = MoveButton(font_name='Gabriola', move=move, font_size=self.height * 0.35, hud_instance=self)
            self.ids.move_select.add_widget(button)
        self.ids.label.text = move_list[0].name
        self.selected_move = move_list[0]

    def open_move_hud(self, instance):
        if self.move_hud_open:
            return
        print("Open the move hud")
        self.move_hud_open = True
        self.ids.current_move.opacity = 0
        self.ids.move_select.opacity = 1

    def close_move_hud(self, selected_move):
        print("Close the move hud")
        self.move_hud_open = False
        self.ids.current_move.opacity = 1
        self.ids.move_select.opacity = 0
        self.selected_move = selected_move
        self.ids.label.text = selected_move.name


class BattleHud(RelativeLayout):

    def __init__(self, **kwargs):
        self.register_event_type('on_turn')
        super().__init__(**kwargs)

        self.get_a_hud = {}
        for index, character in enumerate(Refs.gc.get_current_party()):
            if character is None or index >= 8:
                continue
            #id=f'hud_{index}',
            chud = CharacterHud(size_hint=(0.113, 0.221), pos_hint={'x': 0.05 * (index + 1) + index * 0.221, 'y': 0.025})
            mhud = MoveHud(size_hint=(1, 0.05), pos_hint={'y': 0.025 + 0.221 * 0.96}, hint_x=0.05 * (index + 1) + index * 0.221)
            # id=f'mhud_{index}',
            moves = [character.get_skill(0), character.get_skill(3), character.get_skill(4), character.get_skill(5), character.get_skill(6)]

            chud.set_character(character)
            chud.bind(on_open_mhud=mhud.open_move_hud)

            mhud.set_moves(moves)

            # TODO Make it so that only one mhud can be only at one time
            #   IDEA: Mhud manager as the layer widget

            self.get_a_hud[character] = (chud, mhud)
            self.add_widget(chud)
            self.add_widget(mhud)

    def take_turn(self):
        self.dispatch('on_turn')

    def on_turn(self):
        pass

    def get_hud(self, character):
        return self.get_a_hud[character]


class EnemyHealth(RelativeLayout):
    max = NumericProperty(100)
    value = NumericProperty(0)


class MoveButton(Button):
    move = ObjectProperty(None, allownone=True)
    hud_instance = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.path = 'buttons/'

    def on_move(self, instance, new_move):
        self.text = new_move.name

    def on_release(self):
        if self.opacity == 0:
            return
        self.hud_instance.close_move_hud(self.move)


class FloorAnnouncement(Image):
    name = StringProperty('')

    def fade_out(self, duration):
        anim = Animation(opacity=0, duration=duration * 0.5)
        Clock.schedule_once(lambda dt: self.start_fading(anim), duration * 0.5)

    def start_fading(self, anim):
        anim.start(self)


class HitListener(AnimationStateAdapter):
    def __init__(self):
        self.callback = None

    def set_callback(self, callback_function):
        self.callback = callback_function

    def event(self, trackIndex, event):
        print("event:", event.getData().getName().strip())
        if event.getData().getName().strip() == 'hit':
            if self.callback is not None:
                self.callback()


class BattleAnimation(Label):
    def on_touch_hover(self, touch):
        return False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0

    def appear(self):
        self.opacity = 1

    def fade_out(self, duration):
        anim = Animation(opacity=0, duration=duration * 0.5)
        Clock.schedule_once(lambda dt: self.start_fading(anim, duration), duration * 0.5)

    def start_fading(self, anim, duration):
        anim.start(self)
        Clock.schedule_once(lambda dt: self.remove(), duration * 0.5)

    def remove(self):
        if self.parent is None:
            print("ERROR")
            return
        self.parent.remove_widget(self)


class NumberAnimation(BattleAnimation):
    def __init__(self, number, **kwargs):
        super().__init__(**kwargs)
        self.text = str(number)
        self.color = 1, 1, 1, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'


class BlockAnimation(BattleAnimation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Block'
        self.color = 0.22, 0.22, 0.61, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'


class EvadeAnimation(BattleAnimation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Evade'
        self.color = 0.45, 0.68, 0.68, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'


class CriticalAnimation(BattleAnimation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Critical'
        self.color = 0.6, 0.22, 0.22, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'


class PenetrationAnimation(BattleAnimation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Penetration'
        self.color = 0.56, 0.56, 0.56, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'


class CounterAnimation(BattleAnimation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Counter'
        self.color = 0.76, 0.43, 0.18, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'


class SkeletonPosition(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)


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


class DungeonBattle(Screen):
    level_num = NumericProperty(1)
    is_boss = BooleanProperty(False)

    screen_width = NumericProperty(0)
    screen_height = NumericProperty(0)

    # position = BoundedNumericProperty(0, min=0, max=MAXIMUM_SCREEN_WIDTH)

    moving = BooleanProperty(False)
    in_encounter = BooleanProperty(False)
    direction = NumericProperty(-1)

    auto_move_enabled = BooleanProperty(False)
    auto_battle_enabled = BooleanProperty(False)

    # move_velocity = NumericProperty(0)

    # actual_x = NumericProperty(0)

    def __init__(self, level, boss, config, **kwargs):
        self.dungeon_config = config
        self.level_num = level
        self.is_boss = boss
        super().__init__(**kwargs)

        # Declare variables
        self._keyboard = None
        self.speed = 1
        self.in_encounter = False
        self.showing_announcement = True
        self.moving = False

        self.skeleton_renderer = SkeletonRenderer()

        self.floor = Refs.gc['floors'][self.level_num - 1]
        self.max_screen_width = Refs.app.width * 8

        # Establish parts
        self.parallax = ParallaxBackground()
        self.ids.parallax_layer.add_widget(self.parallax)

        self.encounter_num = self.floor.generateEncounterNumber()
        self.distance = self.max_screen_width * 0.9 / self.encounter_num

        self.entities = {}

        self.enemy_type_skeletons = []

        self.characters = {}
        self.enemies = {}

        self.encounters = []
        self.encounter = None
        self.enemy_types = []
        self.encounter_identifier = 0

        for i in range(self.encounter_num):
            types, enemies = self.floor.generateEnemies()
            for type in types:
                if type not in self.enemy_types:
                    self.enemy_types.append(type)
            self.encounters.append(enemies)

        self.skel_poses = []
        self.skel_run_poses = []
        self.skeletonX, self.skeletonY = Refs.app.width / 2, Refs.app.height / 3
        self.screen_width, self.screen_height = Refs.app.width, Refs.app.height

        self.skel_poses.append(SkeletonPosition(x=self.skeletonX, y=self.skeletonY))
        self.skel_poses.append(SkeletonPosition(x=self.skeletonX + 75, y=self.skeletonY - 150))
        self.skel_poses.append(SkeletonPosition(x=self.skeletonX + 175, y=self.skeletonY - 75))
        self.skel_poses.append(SkeletonPosition(x=self.skeletonX + 300, y=self.skeletonY))
        self.skel_poses.append(SkeletonPosition(x=self.skeletonX + 375, y=self.skeletonY - 150))
        self.skel_poses.append(SkeletonPosition(x=self.skeletonX + 475, y=self.skeletonY - 75))
        self.skel_poses.append(SkeletonPosition(x=self.skeletonX + 600, y=self.skeletonY))
        self.skel_poses.append(SkeletonPosition(x=self.skeletonX + 675, y=self.skeletonY - 150))

        self.gaps = [75, 175, 300, 375, 475, 600, 675]
        self.enemy_positions = [[self.skeletonX - 100, self.skeletonY - 150],
                                [self.skeletonX - 200, self.skeletonY],
                                [self.skeletonX - 300, self.skeletonY + 150],
                                [self.skeletonX - 250, self.skeletonY - 150],
                                [self.skeletonX - 350, self.skeletonY],
                                [self.skeletonX - 450, self.skeletonY + 150],
                                [self.skeletonX - 400, self.skeletonY - 150],
                                [self.skeletonX - 500, self.skeletonY],
                                [self.skeletonX - 600, self.skeletonY + 150],
                                [self.skeletonX - 550, self.skeletonY - 150],
                                [self.skeletonX - 650, self.skeletonY],
                                [self.skeletonX - 750, self.skeletonY + 150]]
        self.direction = -1
        self.directions = [self.direction,
                           self.direction,
                           self.direction,
                           self.direction,
                           self.direction,
                           self.direction,
                           self.direction]
        self.move_with = [True, True, True, True, True, True, True]
        self.canvases = []
        self.canvases_enemy = []

        self.actual_x = 0

    def set_config(self, config):
        if 'auto_move_enabled' in config:
            self.auto_move_enabled = config['auto_move_enabled']
        if 'auto_battle_enabled' in config:
            self.auto_move_enabled = config['auto_battle_enabled']

    def on_auto_move(self):
        self.auto_move_enabled = True
        self.moving = True
        Clock.unschedule(self.idle_animation)
        Clock.schedule_interval(self.move_left, 1 / 60)

    def on_auto_move_cancel(self):
        self.auto_move_enabled = False
        self.moving = False
        Clock.unschedule(self.move_left)
        self.setup_moving(0)

    def on_auto_battle(self):
        pass

    def on_auto_battle_cancel(self):
        pass

    def on_pre_enter(self, *args):
        self.characters = Refs.gc.load_party_skeletons()
        self.load_encounter_states()

        # TODO: Make canvases be added in order of back to front.
        #   Find proper alignment first

        for i in range(len(self.characters)):
            canvas = InstructionGroup()
            self.canvases.append(canvas)
            self.ids.skeleton_layer.canvas.add(canvas)

        # for i in range(len(self.enemies)):
        #     canvas = InstructionGroup()
        #     self.canvases_enemy.append(canvas)
        #     self.ids.skeleton_layer.canvas.add(canvas)

        # for skeleton in self.skeletons:
        #     self.current_animations.append('idle_side')

    def load_encounter_states(self, pop=False):

        self.encounter = Encounter(self.encounter, self.distance)

        if pop:
            self.encounters.pop(0)
        print("You will encounter ", len(self.encounters[0]), "enemies")
        return
        for enemy in self.encounters[0]:
            for i, etype in enumerate(self.enemy_types):
                if enemy.get_name() == etype.name:
                    skeleton = etype.load_skeleton()
                    data = AnimationStateData(skeleton.getData())
                    data.setDefaultMix(0.25)
                    state = AnimationState(data)
                    state.setAnimation(0, "idle", True)
                    skeleton.setSkin(skeleton.getData().getSkins()[0].getName())
                    self.enemies[enemy] = (state, skeleton)
                    break

    def on_enter(self, *args):

        self._keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

        # TODO Play Floor animation
        duration = 1.5
        self.ids.floor_announcement.fade_out(duration)
        Clock.schedule_once(self.setup_moving, duration)
        Clock.schedule_interval(self.render, 1 / 60)

    def setup_moving(self, dt):
        self.showing_announcement = False
        Clock.schedule_once(self.idle_animation, random.randint(25, 40))

    def on_leave(self, *args):
        Clock.unschedule(self.render)
        self.on_keyboard_closed()

    def on_keyboard_closed(self):
        print('My keyboard have been closed!')
        if self._keyboard is None:
            return
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard.unbind(on_key_up=self.on_keyboard_up)
        self._keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print('The key', keycode, 'have been pressed')
        if self.in_encounter or self.showing_announcement or self.auto_move_enabled:
            return
        if keycode[1] == 'a':
            if not self.moving or self.moving and self.direction != -1:
                if self.moving:
                    if self.direction == 1:
                        Clock.unschedule(self.move_right)
                if self.actual_x < self.max_screen_width:
                    self.moving = True
                    self.direction = -1
                    Clock.schedule_interval(self.move_left, 1 / 60)
        elif keycode[1] == 'd':
            if not self.moving or self.moving and self.direction != 1:
                if self.moving:
                    if self.direction == -1:
                        Clock.unschedule(self.move_left)
                # print("Check:", self.actual_x)
                if self.actual_x > 0:
                    self.moving = True
                    self.direction = 1
                    Clock.schedule_interval(self.move_right, 1 / 60)
        return True

    def on_keyboard_up(self, keyboard, keycode):
        if self.in_encounter or self.showing_announcement or self.auto_move_enabled:
            return
        # print('The key', keycode, 'have been released')
        if keycode[1] == 'a':
            if self.moving and self.direction == -1:
                Clock.unschedule(self.move_left)
                self.moving = False
        elif keycode[1] == 'd':
            if self.moving and self.direction == 1:
                Clock.unschedule(self.move_right)
                self.moving = False

    def move_right(self, dt):
        # print(self.actual_x)

        if self.actual_x >= 10:
            self.actual_x -= 10
            # Update other skeleton positions and directions
            index = 0
            for character, (state, skeleton) in self.characters.items():
                if index == 0:
                    index += 1
                    continue
                direction = self.directions[index - 1]
                dif = self.skeletonX - self.skel_poses[index].x
                if self.gaps[index - 1] > dif:
                    if self.move_with[index - 1]:
                        state.setAnimation(0, 'idle_side', True)
                    self.move_with[index - 1] = False
                    # The skeleton is too far to the right
                    self.skel_poses[index].x -= 10
                    dif -= 10
                    if self.gaps[index - 1] < dif:
                        # The skeleton is now too far left, correct it
                        self.skel_poses[index].x = self.skeletonX - self.gaps[index - 1]
                if self.gaps[index - 1] == dif:
                    # Skeleton is in correct position
                    if direction != 1:
                        self.directions[index - 1] = 1
                        skeleton.setFlipX(True)
                    if not self.move_with[index - 1]:
                        self.move_with[index - 1] = True
                        state.setAnimation(0, 'run_side', True)
                index += 1

        # else:
        #     Clock.unschedule(self.move_right)
        #     self.moving = False
        #     for character, (state, skeleton) in self.characters.items():
        #         state.setAnimation(0, 'idle_side', True)
        # Clock.schedule_once(self.idle_animation, random.randint(10, 25))

    def move_left(self, dt):
        if self.showing_announcement:
            return

        if self.actual_x <= self.max_screen_width - 10:
            self.actual_x += 10
            # Update other skeleton positions and directions
            index = 0
            for character, (state, skeleton) in self.characters.items():
                if index == 0:
                    index += 1
                    continue
                direction = self.directions[index - 1]
                dif = self.skel_poses[index].x - self.skeletonX
                if self.gaps[index - 1] > dif:
                    if self.move_with[index - 1]:
                        state.setAnimation(0, 'idle_side', True)
                    self.move_with[index - 1] = False
                    # The skeleton is too far to the left
                    self.skel_poses[index].x += 10
                    dif += 10
                    if self.gaps[index - 1] < dif:
                        # The skeleton is now too far right, correct it
                        self.skel_poses[index].x = self.skeletonX + self.gaps[index - 1]
                if self.gaps[index - 1] == dif:
                    # Skeleton is in correct position
                    if direction != -1:
                        self.directions[index - 1] = -1
                        skeleton.setFlipX(False)
                    if not self.move_with[index - 1]:
                        self.move_with[index - 1] = True
                        state.setAnimation(0, 'run_side', True)
                index += 1

        # else:
        #     Clock.unschedule(self.move_left)
        #     self.moving = False
        #     for character, (state, skeleton) in self.characters.items():
        #         state.setAnimation(0, 'idle_side', True)
        # Clock.schedule_once(self.idle_animation, random.randint(10, 25))

    def on_direction(self, *args):
        [*self.characters.values()][0][1].setFlipX(self.direction == 1)

    def on_moving(self, *args):
        if self.moving:
            index = 0
            for character, (state, skeleton) in self.characters.items():
                if index != 0:
                    if self.move_with[index - 1]:
                        state.setAnimation(0, 'run_side', True)
                else:
                    state.setAnimation(0, 'run_side', True)
                index += 1
            Clock.unschedule(self.idle_animation)
        else:
            if not self.in_encounter:
                for character, (state, skeleton) in self.characters.items():
                    state.setAnimation(0, 'idle_side', True)
                Clock.schedule_once(self.idle_animation, random.randint(10, 25))

    def on_move_velocity(self, *args):
        pass

    def idle_animation(self, *args):
        index = random.randint(0, len(self.characters) - 1)
        state = [*self.characters.values()][index][0]
        state.setAnimation(0, 'idle_action', False)
        state.addAnimation(0, 'idle_front', True, 0)
        Clock.schedule_once(self.idle_animation, random.randint(5, 15))

    def render(self, delta):
        delta = min(delta, 0.032) * self.speed

        index = 0
        for character, (state, skeleton) in self.characters.items():
            skeleton.update(delta)
            state.update(delta)
            state.apply(skeleton)
            skeleton.setPosition(self.skel_poses[index].x, self.skel_poses[index].y)
            skeleton.updateWorldTransform()
            self.skeleton_renderer.draw(self.canvases[index], skeleton)
            index += 1

        # for skeleton in self.skeletons:
        #     skeleton.update(delta)
        #
        # for i, state in enumerate(self.states):
        #     state.update(delta)
        #     state.apply(self.skeletons[i])
        #
        # for i, skeleton in enumerate(self.skeletons):
        #     skeleton.setPosition(self.skel_poses[i].x, self.skel_poses[i].y)

        # for i, skeleton in enumerate(self.skeletons):
        #     skeleton.updateWorldTransform()
        #     self.skeleton_renderer.draw(self.canvases[i], skeleton)

        difference = self.encounter.encounter_x - self.actual_x
        if difference <= self.screen_width + 100:
            if difference < 200 and not self.in_encounter:
                if self.direction == -1:
                    self.moving = False
                    self.in_encounter = True
                    Clock.unschedule(self.move_left)
                    Clock.unschedule(self.move_right)
                    Clock.unschedule(self.idle_animation)
                    self.run_encounter()

            # for enemy in self.enemy_skeletons:
            #     enemy.update(delta)
            #
            # for i, state in enumerate(self.enemy_states):
            #     state.update(delta)
            #     state.apply(self.enemy_skeletons[i])
            #
            # for i, enemy in enumerate(self.enemy_skeletons):
            #     # print(f"Show enemy at ({self.enemy_positions[i][0] - difference}, {self.enemy_positions[i][1]})")
            #     enemy.setPosition(self.enemy_positions[i][0] - difference, self.enemy_positions[i][1])
            #
            # for i, enemy in enumerate(self.enemy_skeletons):
            #     enemy.updateWorldTransform()
            #     self.skeleton_renderer.draw(self.canvases_enemy[i], enemy)

            index = 0
            for enemy, (state, skeleton) in self.enemies.items():
                skeleton.update(delta)
                state.update(delta)
                state.apply(skeleton)
                skeleton.setPosition(self.enemy_positions[index][0] - difference, self.enemy_positions[index][1])
                skeleton.updateWorldTransform()
                self.skeleton_renderer.draw(self.canvases_enemy[index], skeleton)
                index += 1

    def run_encounter(self):
        self.skel_run_poses = []
        for pos in self.skel_poses:
            self.skel_run_poses.append((pos.x, pos.y))

        battle_positions = [(self.screen_width * 0.6, self.screen_height * 0.6), (self.screen_width * 0.68, self.screen_height * 0.53), (self.screen_width * 0.76, self.screen_height * 0.46), (self.screen_width * 0.84, self.screen_height * 0.39), (0, 0), (0, 0), (0, 0), (0, 0)]
        anims = []
        time = 0
        index = 0
        for character, (state, skeleton) in self.characters.items():
            entry = state.setAnimation(0, 'encount', False)
            state.addAnimation(0, 'idleBattle', True, 0)
            time = entry.endTime
            anim = Animation(x=battle_positions[index][0], duration=time) & (Animation(y=battle_positions[index][1] * 1.25, duration=time / 2) + Animation(y=battle_positions[index][1], duration=time / 2))
            anims.append((anim, self.skel_poses[index]))
            index += 1

        for anim, skelPos in anims:
            anim.start(skelPos)

        self.get_health = {}
        index = 0
        for enemy, (state, skeleton) in self.enemies.items():
            health = EnemyHealth(size_hint=(0.05, 0.00625), pos_hint={'center_x': skeleton.getX() / self.screen_width, 'top': skeleton.getY() / self.screen_height}, value=enemy.get_health(), max=enemy.get_health())
            self.get_health[enemy] = health
            self.ids.battle_hud.add_widget(health)
            index += 1
        Clock.schedule_once(lambda dt: self.play_intro_animations(), time)

    def play_bustup_animation(self, character, callback):
        skills = character.get_skills()
        bustup = BustupPreview(size_hint=(0.221, 0.2), name=skills[0].name, name2=skills[1].name if skills[1] is not None else '', name3=skills[2].name if skills[2] is not None else '', character_source=character.bustup_image_source)
        bustup.pos = self.screen_width, self.screen_height * 0.76
        self.ids.animation_layer.add_widget(bustup)
        animation = Animation(x=self.screen_width * 0.779, duration=2.5, t='out_expo') + Animation(opacity=0, duration=0.375)
        animation.start(bustup)
        Clock.schedule_once(lambda dt: self.ids.animation_layer.remove_widget(bustup), 3)
        Clock.schedule_once(callback, 3)

    def play_intro_animations(self):
        # Play support intro animation
        support_characters = Refs.gc.get_current_party()[8:]
        bustup_queue = []
        for character in support_characters:
            if character is None:
                continue
            skills = character.get_skills()
            bustup = BustupPreview(size_hint=(0.221, 0.2), name=skills[0].name, name2=skills[1].name if skills[1] is not None else '', name3=skills[2].name if skills[2] is not None else '', character_source=character.bustup_image_source)
            bustup.opacity = 0
            bustup.pos = self.screen_width, self.screen_height * 0.76
            self.ids.animation_layer.add_widget(bustup)
            bustup_queue.append(bustup)
        animation = Animation(x=self.screen_width * 0.779, duration=2.5, t='out_expo') + Animation(opacity=0, duration=0.375)
        self.start_intro_animations(bustup_queue, animation)

    def start_intro_animations(self, queue, animation):
        if len(queue) > 0:
            bustup = queue.pop(0)
            bustup.opacity = 1
            animation.start(bustup)
            Clock.schedule_once(lambda dt: self.ids.animation_layer.remove_widget(bustup), 3)
        else:
            Clock.schedule_once(lambda dt: self.play_intro_animations2(), 0)
            return
        count = 0
        while len(queue) > 0 and count < 3:
            bustup = queue.pop(0)
            bustup.opacity = 1
            bustup.y -= self.screen_height * (0.24 * (count + 1))
            animation.start(bustup)
            Clock.schedule_once(lambda dt: self.ids.animation_layer.remove_widget(bustup), 3)
            count += 1
        if len(queue) > 0:
            Clock.schedule_once(lambda dt: self.start_intro_animations(queue, animation), 3)
        else:
            Clock.schedule_once(lambda dt: self.play_intro_animations2(), 3)

    def play_intro_animations2(self):
        # Play enemy intro animations
        previews = []
        for enemy, (state, skeleton) in self.enemies.items(): # 0.05, 0.0296 - pos_hint={'center_x': skeleton.getX() / self.screen_width, 'top': skeleton.getY() / self.screen_height}
            preview = EnemyNamePreview(size_hint=(0.1, 0.089), pos_hint={'center_x': skeleton.getX() / self.screen_width, 'center_y': skeleton.getY() / self.screen_height}, name=enemy.get_name(), rank=enemy.get_rank())
            self.ids.animation_layer.add_widget(preview)
            previews.append(preview)
        Clock.schedule_once(lambda dt: self.hide_previews(previews), 2)

    def hide_previews(self, previews):
        animation = Animation(opacity=0, duration=0.5)
        for preview in previews:
            animation.start(preview)
        Clock.schedule_once(lambda dr: self.remove_previews(previews), 0.5)

    def remove_previews(self, previews):
        for preview in previews:
            self.ids.animation_layer.remove_widget(preview)
        self.show_hud()

    def on_turn(self):

        get_move = {}

        selected_moves = []
        for child in self.ids.battle_hud.children:
            if isinstance(child, MoveHud):
                selected_moves.append(child.selected_move)

        turn_order = []

        index = 0
        # TODO Fix special order jumping
        for character in self.characters.keys():
            get_move[character] = selected_moves[index]
            if selected_moves[index].type == skill.SPECIAL:
                insert = 0
                for entity in turn_order:
                    if character.get_agility(in_battle=True) > entity.get_agility(in_battle=True):
                        break
                    insert += 1
                turn_order.insert(insert, character)
            index += 1

        # calculate enemy moves
        index = 0
        for enemy in self.enemies.keys():
            get_move[enemy] = enemy.moves[0]
            # enemy special at front
            index += 1

        # Calculate the turn order
        for enemy in self.enemies.keys():
            insert = 0
            for entity in turn_order:
                if enemy.get_agility(in_battle=True) > entity.get_agility(in_battle=True):
                    break
                insert += 1
            turn_order.insert(insert, enemy)

        for character in self.characters.keys():
            insert = 0
            for entity in turn_order:
                if character.get_agility(in_battle=True) > entity.get_agility(in_battle=True):
                    break
                insert += 1
            turn_order.insert(insert, character)

        # TODO - Shuffle when same AGI

        # Go through each entity and execute turn
        entity = turn_order.pop(0)
        self.turn_stage_1(entity, turn_order, get_move)

    def handle_move(self, entity, move, counter_target=None):
        # TODO handle applying effects
        entity.update_mana_battle(move.mana_cost)
        move.uses += 1

        if move.has_effect:
            for effect in move.get_effects():
                if effect.target_type == skill.SELF:
                    entity.apply_effect(effect)
                elif effect.target_type == skill.ALL_ALLIES:
                    if entity in self.characters:
                        for sentity in self.characters.keys():
                            if sentity.is_dead() or entity == sentity:
                                continue
                            sentity.apply_effect(effect)
                    else:
                        for sentity in self.enemies.keys():
                            if sentity.is_dead() or entity == sentity:
                                continue
                            sentity.apply_effect(effect)

        targets = None
        if move.target == skill.ALL_ALLIES:
            # Buff Move
            # TODO All Allies
            print("Target all allies")
            pass
        elif move.target == skill.SELF:
            # Buff move
            # TODO Self
            print("Target self")
            pass
        elif move.target == skill.ALL_FOES:
            # Attack All Foes
            # TODO ALL Foes
            targets = self.get_targets(entity)
        elif move.target == skill.ONE_FOE:
            # Attack a random Foe
            if counter_target is None:
                targets = [self.get_targets(entity, True)]
            else:
                targets = [counter_target]

        info = {}
        for target in targets:
            info[target] = TargetInfo()

            self.calculate_attack(entity, target, info, move)

            if info[target].death and info[target].counter:
                info[target].counter = False
        return True, targets, info

    def play_move_animation(self, entity, move):
        # TODO Play Animation
        if entity in self.characters:
            state = self.characters[entity][0]
        else:
            state = self.enemies[entity][0]

        entry = state.setAnimation(0, move.anim_id, False)
        # TODO handle moving skeleton pos on special
        state.addAnimation(0, entity.get_idle_animation(), True, entry.endTime)
        return entry, entry.endTime

    def create_markers(self, targets, info):
        for target in targets:
            if target in self.characters:
                tstate, tskeleton = self.characters[target]
            else:
                tstate, tskeleton = self.enemies[target]

            x_pos = random.randrange(25, 75) / 100 * tskeleton.getWidth() + tskeleton.getX() - tskeleton.getWidth() / 2
            y_pos = random.randrange(25, 75) / 100 * tskeleton.getHeight() + tskeleton.getY()
            # TODO Fix maker positioning and make focal around random point
            target.addMarker('damage', NumberAnimation(round(info[target].damage), font_size=self.screen_height * 0.05, size_hint=(0.1, 0.05), pos_hint={'center_x': x_pos / self.screen_width, 'y': y_pos / self.screen_height}))
            if info[target].penetration:
                target.addMarker('penetration', PenetrationAnimation(font_size=self.screen_height * 0.05, size_hint=(0.075, 0.0375), pos_hint={'right': x_pos / self.screen_width, 'top': y_pos / self.screen_height}))
            if info[target].critical:
                target.addMarker('critical', CriticalAnimation(font_size=self.screen_height * 0.05, size_hint=(0.075, 0.0375), pos_hint={'x': x_pos / self.screen_width - 0.0125, 'top': y_pos / self.screen_height - 0.0375}))
            if info[target].block:
                target.addMarker('block', BlockAnimation(font_size=self.screen_height * 0.05, size_hint=(0.075, 0.0375), pos_hint={'right': x_pos / self.screen_width, 'top': y_pos / self.screen_height - 0.0375 * 2}))
            if info[target].evade:
                target.addMarker('evade', EvadeAnimation(font_size=self.screen_height * 0.05, size_hint=(0.075, 0.0375), pos_hint={'x': x_pos / self.screen_width, 'top': y_pos / self.screen_height - 0.0375 * 2}))
            if info[target].counter:
                target.addMarker('counter', CounterAnimation(font_size=self.screen_height * 0.05, size_hint=(0.075, 0.0375), pos_hint={'center_x': x_pos / self.screen_width, 'top': y_pos / self.screen_height - 0.0375 * 2.75}))

            target.addMarkersToWindow(self.ids.animation_layer)
            info[target].tstate = tstate

    def add_death_animation(self, death, target, tstate, time):
        if not death:
            tstate.addAnimation(0, target.get_idle_animation(), True, time)
            return 0
        if target in self.characters:
            tentry = tstate.addAnimation(0, 'death', False, time)
            return tentry.endTime
        else:
            tstate.clearTrack(0)
            # Fade time is 1.5 * timeScale
            anim = Animation(opacity=0, duration=1)
            anim2 = Animation(a=0, duration=1)
            anim2.start(self.enemies[target][1].clear_color)  # Fade out enemy canvas
            anim.start(self.get_health[target])
            return 1

    def play_damage_animation(self, block, evade, tstate):
        if block or evade:
            return 0

        entry = tstate.setAnimation(0, 'damage', False)
        return entry.endTime

    def handle_hit(self, entity, targets, move, info, next_stage):
        ttime = 0
        for target in targets:
            if target.is_dead():
                continue
            target.showMarkers()

            if self.handle_damage(target, entity, move, info):
                next_stage = lambda dt: self.turn_stage_4(target not in self.characters)

            time = self.play_damage_animation(info[target].block, info[target].evade, info[target].tstate)
            time += self.add_death_animation(info[target].death, target, info[target].tstate, time)
            target.fadeOutMarkers(max(time, 0.75))
            ttime = max(ttime, max(time, 0.75))

        Clock.schedule_once(next_stage, max(ttime, 0.75))

    def get_next_stage(self, turn_order, get_move, counter_check=False, entity=None, targets=None, info=None):
        if counter_check:
            counters = []
            for target in targets:
                if not info[target].counter:
                    continue
                counters.append(target)
            return lambda dt: self.turn_stage_2(entity, counters, turn_order, get_move)
        if len(turn_order) > 0:
            entity = turn_order.pop(0)
            return lambda dt: self.turn_stage_1(entity, turn_order, get_move)
        return lambda dt: self.turn_stage_3(turn_order, get_move)

    def turn_stage_1(self, entity, turn_order, get_move):
        if entity.is_dead():
            Clock.schedule_once(self.get_next_stage(turn_order, get_move), 0)
            return

        move = get_move[entity]

        print("Processing move", move.name, "for entity", entity.name)

        # TODO Handle multiple targets
        attacking, targets, info = self.handle_move(entity, move)

        entry, time = self.play_move_animation(entity, move)

        if attacking:
            adapter = HitListener()

            self.create_markers(targets, info)

            next_stage = self.get_next_stage(turn_order, get_move, True, entity, targets, info)
            adapter.set_callback(lambda: self.handle_hit(entity, targets, move, info, next_stage))
            entry.setListener(adapter)
        # TODO handle non-attacking move

    def turn_stage_2(self, target, entities, turn_order, get_move):

        if len(entities) <= 0:
            Clock.schedule_once(self.get_next_stage(turn_order, get_move), 0)
            return

        entity = entities.pop(0)
        if entity.is_dead():
            self.turn_stage_2(target, entities, turn_order, get_move)
            return

        move = entity.get_skill(1)
        if move is None:
            move = entity.get_skill(0)

        print("Processing counter move", move.name, "for entity", entity.name)
        attacking, targets, info = self.handle_move(entity, move, target)
        for target in targets:
            info[target].counter = False

        entry, time = self.play_move_animation(entity, move)

        if attacking:
            adapter = HitListener()

            self.create_markers(targets, info)

            if len(entities) <= 0:
                next_stage = self.get_next_stage(turn_order, get_move)
            else:
                def next_stage(dt): self.turn_stage_2(target, entities, turn_order, get_move)
            adapter.set_callback(lambda: self.handle_hit(entity, targets, move, info, next_stage))
            entry.setListener(adapter)
        # TODO handle non-attacking move

    def turn_stage_3(self, turn_order, get_move):
        # End of turn effect stage
        print("Starting EOT Stage")
        # Apply EOT effects
        # Reduce all effect duration by 1 turn
        # Change moves avaliable based on mana
        for character in self.characters:
            character.update_status_effects()
        for enemy in self.enemies:
            enemy.update_status_effects()
        return

        # Go to the next entity in the turn order

    def turn_stage_4(self, win):
        if win:
            for character, (state, skeleton) in self.characters.items():
                if character.is_dead():
                    continue
                entry = state.setAnimation(0, 'victory', False)
                state.addAnimation(0, 'victory_loop', True, entry.endTime)
                self.ids.status_button.disabled = False
        else:
            pass
        # End encounter
        #   Play win animations----
        #   Show exp and item gain from encounter
        #       TODO There are no exp levels, so this would only show items gained and used.
        #       This should wait until items are implemented
        #   wait for screen click to move back to battle
        #   TODO Add button on win. On Failure, show fial animation and go back to main dungeon screen on floor 1. Items and weapons need to be reset. Handle later.
        #   TODO load next encounter states & go back to battle run

    def return_to_run(self):
        self.ids.status_button.disabled = True

        if len(self.encounters) == 1:
            # TODO Won the whole fight
            screen, made = self.root.create_screen('dungeon_result', list(self.characters.keys()), self.level_num)
            screen.dungeon_config['auto_move_enabled'] = self.auto_move_enabled
            screen.dungeon_config['auto_battle_enabled'] = self.auto_battle_enabled
            self.root.display_screen(screen, True, False)
        else:
            self.hide_hud()

            anims = []
            time = 0
            index = 0
            for character, (state, skeleton) in self.characters.items():
                if character.is_dead() and skeleton.clear_color.a != 0:
                    anim2 = Animation(a=0, duration=max(0.75, time))
                    anim2.start(skeleton.clear_color)
                    index += 1
                    continue
                entry = state.setAnimation(0, 'encount', False)
                character.set_animation_idle(add=True, delay=entry.endTime, loop=True)
                time = entry.endTime
                anim = Animation(x=self.skel_run_poses[index][0], duration=time) & (Animation(y=self.skel_run_poses[index][1] * 1.25, duration=time / 2) + Animation(y=self.skel_run_poses[index][1], duration=time / 2))
                anims.append((anim, self.skel_poses[index]))
                index += 1

            for anim, skelPos in anims:
                anim.start(skelPos)

            for enemy, health in self.get_health.items():
                health.parent.remove_widget(health)
            self.get_health = {}

            count = len(self.enemies)
            self.enemies = {}
            self.load_encounter_states(True)
            for i in range(max(len(self.enemies) - count, 0)):
                canvas = InstructionGroup()
                self.canvases_enemy.append(canvas)
                self.ids.skeleton_layer.canvas.add(canvas)
            self.in_encounter = False
            if self.auto_move_enabled:
                Clock.schedule_interval(self.move_left, 1 / 60)

    def calculate_attack(self, entity, target, info, move):
        attack = entity.get_attack(move.affect) * move.power
        print("\nAttack:", attack)
        defense = target.get_defense()
        print("Defense:", defense)
        entity_effects = entity.get_status_effects()
        target_effects = target.get_status_effects()

        # TODO calculate applied boosts & detrements

        # TODO target damage modifiersk
        if skill.PHYSICAL_RESIST in target_effects and (move.affect == skill.PHYSICAL or move.affect == skill.HYBRID):
            for effect in target_effects[skill.PHYSICAL_RESIST]:
                defense *= 1 + effect.st[0]
                print("Defense *=", effect.st[0])
        if skill.MAGICAL_RESIST in target_effects and (move.affect == skill.MAGICAL or move.affect == skill.HYBRID):
            for effect in target_effects[skill.MAGICAL_RESIST]:
                defense *= 1 + effect.st[0]
                print("Defense *=", effect.st[0])

        # If penetration, defense → 0
        t_chance = (max(min(entity.get_strength(in_battle=True) / target.get_strength(in_battle=True), 1), 0) + max(min(entity.get_agility(in_battle=True) / target.get_agility(in_battle=True), 1), 0)) / 4
        if skill.PENETRATION in entity_effects:
            for effect in entity_effects[skill.PENETRATION]:
                t_chance *= 1 + effect.st[0]
                print("Penetration t_chance *=", effect.st[0])
        t_chance = min(t_chance, 1)
        f_chance = 1 - t_chance

        penetration = random.choices([True, False], weights=[t_chance, f_chance])[0]

        if penetration:
            defense = 0
            print("Defense: → 0")

        if attack > defense:
            multiplier = 0.999463 * pow(1.00054, attack - defense)
            print("Multiplier: ", multiplier)
            attack = attack * multiplier
            print("Attack:", attack)
            damage = random.normalvariate(attack, attack * 0.1)
            print("Damage:", damage)
        else:
            divider = 0.999463 * pow(1.00054, defense - attack)
            print("Divider: ", divider)
            attack = attack / divider
            print("Attack:", attack)
            damage = random.normalvariate(attack, attack * 0.1)
            print("Damage:", damage)

        # If critical, gen crit on normal dist and multiply
        t_chance = max(min(entity.get_strength(in_battle=True) / target.get_strength(in_battle=True), 1), 0) / 2
        if skill.CRITICAL in entity_effects:
            for effect in entity_effects:
                t_chance *= 1 + effect.st[0]
        t_chance = min(t_chance, 1)
        if penetration:
            t_chance = min(t_chance * 1.20, 1)
        f_chance = 1 - t_chance

        critical = random.choices([True, False], weights=[t_chance, f_chance])[0]
        if critical:
            damage *= random.normalvariate(2.5, 0.375)
            print("Damage:", damage)

        # calculate elemental boost
        if skill.boost(move.type, target.type):
            damage *= random.normalvariate(2, 0.25)
        if skill.fboost(move.type, target.type):
            damage /= random.normalvariate(2, 0.25)

        if skill.DAMAGE in entity_effects:
            for effect in entity_effects:
                damage *= 1 + effect.st[0]

        # TODO calculate target damage up

        # If block, half damage
        t_chance = (max(min(entity.get_endurance(in_battle=True) / target.get_endurance(in_battle=True), 1), 0) + max(min(entity.get_agility(in_battle=True) / target.get_agility(in_battle=True), 1), 0)) / 4
        if skill.BLOCK_CHANCE in target_effects:
            for effect in target_effects:
                t_chance *= 1 + effect.st[0]
        t_chance = min(t_chance, 1)
        f_chance = 1 - t_chance

        block = random.choices([True, False], weights=[t_chance, f_chance])[0]
        if block:
            damage /= 2

        # If evade, damage * 0.25
        if not block:
            t_chance = max(min(entity.get_dexterity(in_battle=True) / target.get_dexterity(in_battle=True), 1), 0) / 2
            if skill.EVADE_CHANCE in target_effects:
                for effect in entity_effects[skill.EVADE_CHANCE]:
                    t_chance *= 1 + effect.st[0]
            t_chance = min(t_chance, 1)
        else:
            t_chance = 0
        f_chance = 1 - t_chance
        evade = random.choices([True, False], weights=[t_chance, f_chance])[0]
        if evade:
            damage *= 0.25

        if skill.PHYSICAL_NULL in target_effects and (move.affect == skill.PHYSICAL or move.affect == skill.HYBRID):
            target_effects[skill.PHYSICAL_NULL].pop(0)
            if len(target_effects[skill.PHYSICAL_NULL]) == 0:
                del target_effects[skill.PHYSICAL_NULL]
            damage = 0
        elif skill.MAGICAL_NULL in target_effects and (move.affect == skill.MAGICAL or move.affect == skill.HYBRID):
            target_effects[skill.MAGICAL_NULL].pop(0)
            if len(target_effects[skill.MAGICAL_NULL]) == 0:
                del target_effects[skill.MAGICAL_NULL]
            damage = 0

        # calculate counter
        t_chance = (max(min(entity.get_dexterity(in_battle=True) / target.get_dexterity(in_battle=True), 1), 0) + max(min(entity.get_agility(in_battle=True) / target.get_agility(in_battle=True), 1), 0)) / 4
        if evade:
            t_chance = min(t_chance * 1.20, 1)
        if skill.EVADE_CHANCE in target_effects:
            for effect in target_effects[skill.EVADE_CHANCE]:
                t_chance *= 1 + effect.st[0]
        t_chance = min(t_chance, 1)
        f_chance = 1 - t_chance

        counter = random.choices([True, False], weights=[t_chance, f_chance])[0]

        info[target].damage = damage
        info[target].penetration = penetration
        info[target].critical = critical
        info[target].block = block
        info[target].evade = evade
        info[target].counter = counter

    def handle_damage(self, entity, target, move, info):
        print("Damage: ", info[entity].damage)

        entity.update_health_battle(info[entity].damage)
        # Apply Foes and Foe one effects
        if move.has_effect:
            for effect in move.get_effects():

                # handle cause effect
                if effect.type == skill.CAUSE_EFFECT:
                    # Check if type is already applied. Cannot have multiple types
                    valid = True
                    if skill.STATUS_EFFECT in entity.get_status_effects():
                        for status_effect in entity.get_status_effects()[skill.STATUS_EFFECT]:
                            if status_effect.type == effect.st[0]:
                                valid = False
                                break
                    if not valid:
                        continue

                    t_chance = effect.st[2]
                    f_chance = 1 - t_chance
                    if random.choices([True, False], weights=[t_chance, f_chance])[0]:
                        # Do avoid stuff
                        affect = skill.create_status_effect(effect.st[0], effect.st[1], target)
                    continue

                if effect.target_type == skill.ONE_FOE:
                    entity.apply_effect(effect)
                elif effect.target_type == skill.ALL_FOES:
                    if entity in self.characters:
                        for entity in self.characters.keys():
                            if entity.is_dead():
                                continue
                            entity.apply_effect(effect)
                    else:
                        for entity in self.enemies.keys():
                            if entity.is_dead():
                                continue
                            entity.apply_effect(effect)
        # Handle skill increases & special gain

        if entity in self.characters:
            chud = self.ids.battle_hud.get_hud(entity)[0]
            chud.health -= info[entity].damage
            if chud.health <= 0:
                info[entity].death = True
                print("This entity has died")
                count = 0
                for character in self.characters:
                    if not character.is_dead():
                        break
                    count += 1
                if count == len(self.characters):
                    return True
        else:
            ehud = self.get_health[entity]
            ehud.value -= info[entity].damage
            if ehud.value <= 0:
                info[entity].death = True
                print("This entity has died")
                count = 0
                for enemy in self.enemies:
                    if not enemy.is_dead():
                        break
                    count += 1
                if count == len(self.enemies):
                    return True

    def get_targets(self, entity, single=False):
        if entity in self.characters:
            size = len(self.enemies)
            targets = [*self.enemies]
        else:
            size = len(self.characters)
            targets = [*self.characters]
        for target in targets:
            if target.is_dead():
                targets.remove(target)
                size -= 1
        if single:
            target_index = random.randint(0, size - 1)
            return targets[target_index]
        return targets

    def show_hud(self):
        self.ids.battle_hud.opacity = 1

    def hide_hud(self):
        self.ids.battle_hud.opacity = 0

    def show_assist_anims(self, anims):
        for anim, wid in anims:
            anim.start(wid)
