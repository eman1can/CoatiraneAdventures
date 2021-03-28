from game.effect import AGILITY, DEFENSE, DEXTERITY, ENDURANCE, MAGIC, MAGICAL_ATTACK, PHYSICAL_ATTACK, STAT_TYPES, STRENGTH
from game.skill import MAGICAL, PHYSICAL
from refs import Refs


class BattleEntity:
    def __init__(self):
        self._status_effects = {}
        self._markers = {}
        self._bhealth = 0
        self._bmana = 0
        self._base = None

    def get_battle_health(self):
        return self._bhealth

    def is_dead(self):
        return self.get_battle_health() <= 0.0

    def get_battle_mana(self):
        return self._bmana

    def decrease_health(self, damage):
        print(self.get_name(), self._bhealth, '→', self._bhealth-damage)
        self._bhealth -= damage

    def decrease_mana(self, mana_cost):
        self._bmana -= mana_cost

    def get_attack(self, attack_type):
        if attack_type == PHYSICAL:
            return self.get_physical_attack()
        elif attack_type == MAGICAL:
            return self.get_magical_attack()
        else:
            return (self.get_physical_attack() + self.get_magical_attack()) / 2

    def get_physical_attack(self):
        physical_attack = self._physical_attack - self._strength + self.get_strength()
        print(self.get_name(), 'Physical attack', physical_attack, 'boosted to', self._get_boosted_stat(PHYSICAL_ATTACK, physical_attack))
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

    def load_skeleton(self):
        skeleton = Refs.gc.skel_loader.load_skeleton(self._base._skeleton_path, False, Refs.gc.skeleton_scale)
        skeleton.setWidth(skeleton.getData().getWidth() * Refs.gc.skeleton_scale)
        skeleton.setHeight(skeleton.getData().getHeight() * Refs.gc.skeleton_scale)
        skeleton.setSkin(skeleton.getData().getSkins()[0].getName())
        return skeleton

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

    def apply_effect(self, name, effect_type, effect):
        if effect_type not in self._status_effects:
            self._status_effects[effect_type] = {}
        self._status_effects[effect_type][name] = effect

    def clear_negative_effects(self):
        for effects in self._status_effects.values():
            dead_effects = []
            for effect_name, effect in effects.items():
                if effect.get_amount() < 0:
                    dead_effects.append(effect_name)
            for dead_effect in dead_effects:
                effects.pop(dead_effect)

    def clear_effects(self):
        self._status_effects = {}

    def get_effects(self):
        return self._status_effects

    def reduce_effect_amount(self, effect_type, delta):
        list(self._status_effects[effect_type].values())[0].reduce_amount(delta)

    def update_effects(self, delta=1):
        dead_effect_types = []
        for effect_type, effects in self._status_effects.items():
            if effect_type in STAT_TYPES:
                dead_effects = []
                for effect_name, effect in effects.items():
                    if effect.get_duration() <= 0:
                        continue
                    effect.reduce_duration(delta)
                    if effect.get_duration() <= 0:
                        dead_effects.append(effect_name)
                for dead_effect in dead_effects:
                    effects.pop(dead_effect)
            if len(effects) == 0:
                dead_effect_types.append(effect_type)
        for dead_effect_type in dead_effect_types:
            self._status_effects.pop(dead_effect_type)
