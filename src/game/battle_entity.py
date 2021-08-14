from game.effect import AFFLICTIONS, AGILITY, CONDITION, COUNTER_TYPES, DEFENSE, DEXTERITY, DURATION_TYPES, EFFECT_TYPES, ENDURANCE, MAGIC, MAGICAL_ATTACK, PHYSICAL_ATTACK, RECURRING_CHANCE, STAT_TYPES, STRENGTH, TIME_LENGTH
from game.skill import MAGICAL, PHYSICAL, DARK, EARTH, FIRE, LIGHT, THUNDER, WATER, WIND, element_modifier
from kivy.properties import NumericProperty

from kivy.event import EventDispatcher
from refs import Refs
from spine.animation.animationstate import AnimationState
from spine.animation.animationstatedata import AnimationStateData


class BattleEntity(EventDispatcher):
    x = NumericProperty(0)
    y = NumericProperty(0)
    opacity = NumericProperty(1)

    def __init__(self, base, **kwargs):
        super().__init__(**kwargs)

        self._status_effects = {}
        self._status_effect = None
        self._markers = {}
        self._battle_health = 0
        self._selected_skill = 0
        self._battle_mana = 0
        self._base = base
        self.height = 0
        self._visible = True

    def __getattr__(self, item):
        return getattr(self._base, item)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def get_battle_health(self):
        return self._battle_health

    def is_dead(self):
        return self._battle_health <= 0.0

    def get_battle_mana(self):
        return self._battle_mana

    def decrease_health(self, damage):
        self._battle_health -= damage

    def decrease_mana(self, mana_cost):
        self._battle_mana -= mana_cost

    def get_attack(self, attack_type):
        if attack_type == PHYSICAL:
            return self.get_physical_attack()
        elif attack_type == MAGICAL:
            return self.get_magical_attack()
        else:
            return (self.get_physical_attack() + self.get_magical_attack()) / 2

    def get_physical_attack(self):
        physical_attack = self._physical_attack - self._strength + self.get_strength()
        return self._get_boosted_stat(PHYSICAL_ATTACK, physical_attack)

    def get_magical_attack(self):
        magical_attack = self._magical_attack - self._magic + self.get_magic()
        return self._get_boosted_stat(MAGICAL_ATTACK, magical_attack)

    def get_defense(self):
        return self._get_boosted_stat(DEFENSE, self._defense)

    def get_strength(self):
        return self._get_boosted_stat(STRENGTH, self._strength)

    def get_magic(self):
        return self._get_boosted_stat(MAGIC, self._magic)

    def get_endurance(self):
        return self._get_boosted_stat(ENDURANCE, self._endurance)

    def get_agility(self):
        return self._get_boosted_stat(AGILITY, self._agility)

    def get_dexterity(self):
        return self._get_boosted_stat(DEXTERITY, self._dexterity)

    def _get_boosted_stat(self, stat_type, stat):
        return stat * (1 + min(max(self.get_total_boost(stat_type), 0), 1))

    def get_total_boost(self, stat_type):
        amount = 0
        if stat_type not in self._status_effects:
            return amount
        for effect in self._status_effects[stat_type].values():
            amount += effect.get_amount()
        return amount

    def get_idle_animation(self):
        return ''

    def add_marker(self, marker_id, marker):
        self._markers[marker_id] = marker

    def add_markers_to_window(self, window):
        for marker_id, marker in self._markers.items():
            window.add_widget(marker)

    def show_markers(self):
        for marker_id, marker in self._markers.items():
            marker.appear()

    def fade_out_markers(self, fade_time):
        for marker_id, marker in self._markers.items():
            marker.fade_out(fade_time)
        self._markers = {}

    def apply_effect(self, effect_id, effect_type, effect):
        if effect_type not in self._status_effects:
            self._status_effects[effect_type] = {}
        if effect_id in self._status_effects[effect_type]:
            if effect_type in EFFECT_TYPES:
                Refs.log(f'Do not apply {EFFECT_TYPES[effect_type][effect.get_amount()]} to {self.get_name()}', tag='BattleEntity')
            elif effect_type in STAT_TYPES:
                Refs.log(f'Apply diminishing {STAT_TYPES[effect_type]} to {self.get_name()}', tag='BattleEntity')
            elif effect_type in COUNTER_TYPES:
                Refs.log(f'Apply diminishing {COUNTER_TYPES[effect_type]} to {self.get_name()}', tag='BattleEntity')
            elif effect_type in DURATION_TYPES:
                Refs.log(f'Apply diminishing {DURATION_TYPES[effect_type]} to {self.get_name()}', tag='BattleEntity')
            else:
                Refs.log(f'Unknown status effect, {effect_type}', 'error', 'BattleEntity')
        else:
            if effect_type in EFFECT_TYPES:
                name = EFFECT_TYPES[effect_type][effect.get_amount()]
                Refs.log(f'Apply effect {name} to {self.get_name()}', tag='BattleEntity')
                for (sub_effect_type, sub_effect) in effect.build(effect_type).items():
                    if sub_effect_type != CONDITION:
                        sub_effect.set_info(None, name)
                    self._apply_effect(name, sub_effect_type, sub_effect)
            elif effect_type in STAT_TYPES:
                Refs.log(f'Apply effect {STAT_TYPES[effect_type]} to {self.get_name()}', tag='BattleEntity')
            elif effect_type in COUNTER_TYPES:
                Refs.log(f'Apply effect {COUNTER_TYPES[effect_type]} to {self.get_name()}', tag='BattleEntity')
            elif effect_type in DURATION_TYPES:
                Refs.log(f'Apply effect {DURATION_TYPES[effect_type]} to {self.get_name()}', tag='BattleEntity')
            else:
                Refs.log(f'Unknown status effect, {effect_type}', 'error', 'BattleEntity')
            self._apply_effect(effect_id, effect_type, effect)

    def _apply_effect(self, effect_id, effect_type, effect):
        if effect_type not in self._status_effects:
            self._status_effects[effect_type] = {}
        self._status_effects[effect_type][effect_id] = effect

    def has_status_effect(self):
        return self._status_effect is not None

    def get_status_effect(self):
        return self._status_effect

    def set_status_effect(self, effect):
        self._status_effect = effect

    def get_status_effect_type(self):
        for effect_type in self._status_effects.keys():
            if effect_type in EFFECT_TYPES:
                return effect_type
        return None

    def clear_negative_effects(self):
        animations = []
        for effect_type, effects in self._status_effects.items():
            if effect_type == CONDITION:
                continue
            dead_effects = []
            for effect_name, effect in effects.items():
                if effect.get_amount() < 0:
                    dead_effects.append(effect_name)
                if effect_type in EFFECT_TYPES:
                    animations.append({'entity': self, 'type': f'end_status_effect', 'effect': effect_type})
                    dead_effects.append(effect_name)
            for dead_effect in dead_effects:
                Refs.log(f'Remove dead effect {dead_effect} from {self.get_name()}', tag='BattleEntity')
                effects.pop(dead_effect)
        return animations

    def clear_effects(self):
        self._status_effects = {}

    def get_effects(self):
        return self._status_effects

    def reduce_effect_amount(self, effect_type, delta):
        list(self._status_effects[effect_type].values())[0].reduce_amount(delta)

    def update_effects(self, delta=1):
        Refs.log(f'Update effects for {self.get_name()}', tag='BattleEntity')
        dead_effect_types = []
        for effect_type, effects in self._status_effects.items():
            if effect_type == CONDITION:
                continue
            dead_effects = []
            if effect_type in STAT_TYPES:
                for effect_name, effect in effects.items():
                    if effect.get_duration() <= 0:
                        continue
                    Refs.log(f'{STAT_TYPES[effect_type]} -= {delta} turns')
                    effect.reduce_duration(delta)
                    if effect.get_duration() <= 0:
                        dead_effects.append(effect_name)
            elif effect_type in COUNTER_TYPES:
                for effect_name, effect in effects.items():
                    if effect.get_amount() <= 0:
                        dead_effects.append(effect_name)
            elif effect_type in DURATION_TYPES:
                for effect_name, effect in effects.items():
                    Refs.log(f'{STAT_TYPES[effect_type]} -= {delta} turns')
                    effect.reduce_duration(delta)
                    if effect.get_duration() <= 0:
                        dead_effects.append(effect_name)
            elif effect_type in EFFECT_TYPES:
                pass
            for dead_effect in dead_effects:
                Refs.log(f'Remove dead effect {dead_effect} from {self.get_name()}', tag='BattleEntity')
                effects.pop(dead_effect)
            if len(effects) == 0:
                dead_effect_types.append(effect_type)

        for dead_effect_type in dead_effect_types:
            self._status_effects.pop(dead_effect_type)

        return self.update_counting_status_effect()

    def update_counting_status_effect(self):
        return self.update_status_effects([RECURRING_CHANCE, TIME_LENGTH])

    def update_recurring_status_effect(self):
        return self.update_status_effects([AFFLICTIONS])

    def update_status_effects(self, types):
        animations = []

        # Evaluate condition
        if CONDITION not in self._status_effects:
            return animations

        dead_effects = []

        # Update condition and get dead effects
        conditions = self._status_effects[CONDITION]
        for effect_name in conditions.keys():
            condition = conditions[effect_name]
            if condition.get_type() in types:
                Refs.log(f'Update afflictions for {effect_name}')
                if self.reduce_condition(conditions, condition, effect_name):
                    dead_effects.append(effect_name)

        # Remove status effect for every dead_effect
        remove_types = []
        for effect_type in EFFECT_TYPES:
            if effect_type not in self._status_effects:
                continue
            remove_effects = []
            for effect_name in dead_effects:
                for effect_id, effect in self._status_effects[effect_type].items():
                    if effect_name != EFFECT_TYPES[effect_type][effect.get_amount()]:
                        continue
                    remove_effects.append(effect_id)
            for effect_id in remove_effects:
                animations.append({'entity': self, 'type': f'end_status_effect', 'effect': effect_type})
                self._status_effects[effect_type].pop(effect_id)
            if len(self._status_effects[effect_type]) == 0:
                remove_types.append(effect_type)
        for effect_type in remove_types:
            self._status_effects.pop(effect_type)

        # For every effect, remove sub-effects
        remove_types = []
        for effect_type, effects in self._status_effects.items():
            for dead_effect in dead_effects:
                if dead_effect in effects:
                    effects.pop(dead_effect)
            if len(self._status_effects[effect_type]) == 0:
                remove_types.append(effect_type)
        for effect_type in remove_types:
            self._status_effects.pop(effect_type)
        return animations

    def reduce_condition(self, conditions, condition, effect_name):
        result = condition.reduce()
        Refs.log(f'Reduced condition counter for {effect_name} - {condition}')
        if result:
            Refs.log('Condition Complete')
            if condition.get_child():
                Refs.log('Going to next child')
                conditions[effect_name] = condition.get_child()
                return False
            else:
                Refs.log('Destroying status effect')
                return True
        return False

    def element_modifier(self, element):
        return element_modifier(self._base.get_element(), element)

    def get_skeleton(self):
        if self._skeleton is None:
            Refs.log("Skeleton is not yet loaded!", 'error')
            return
        return self._skeleton

    def get_animation_state(self):
        if self._animation_state is None:
            Refs.log("Skeleton is not yet loaded!", 'error')
            return
        return self._animation_state

    def add_event_handler(self, event_name, key, handler):
        self._animation_state.add_event_handler(event_name, key, handler)

    def remove_event_handler(self, event_name, key):
        self._animation_state.remove_event_handler(event_name, key)

    def update(self, delta):
        self._skeleton.update(delta)
        self._animation_state.update(delta)
        self._animation_state.apply(self._skeleton)
        self._skeleton.setPosition(self.x, self.y)
        self._skeleton.updateWorldTransform()

    def load_skeleton(self, skeleton_loader, scale=1):
        self._skeleton = skeleton_loader.load_skeleton(self.get_skeleton_path(), False, scale)
        self._skeleton.setWidth(self._skeleton.getData().getWidth() * scale)
        self._skeleton.setHeight(self._skeleton.getData().getHeight() * scale)
        data = AnimationStateData(self._skeleton.getData())
        # data.setDefaultMix(0.75)
        self._animation_state = AnimationState(data)
        self._skeleton.setSkin(self._skeleton.getData().getSkins()[0].getName())
        self.set_animation_idle(loop=True)
        self.height = self._skeleton.getHeight()
        return self._animation_state, self._skeleton

    def set_flip_x(self, flip):
        self._skeleton.setFlipX(flip)

    def set_invisible(self):
        self._visible = False

    def set_visible(self):
        self._visible = True

    def visible(self):
        return self._visible

    def set_animation(self, animation, add=False, track=0, loop=False, delay=0):
        if not add:
            return self._animation_state.setAnimation(track, animation, loop)
        else:
            return self._animation_state.addAnimation(track, animation, loop, delay)

    def set_animation_idle(self, add=False, track=0, loop=False, delay=0):
        self.set_animation(self.get_idle_animation(), add, track, loop, delay)

    def get_attack_animation(self, skill):
        return 'attack'

    def get_selected_skill_index(self):
        return self._selected_skill