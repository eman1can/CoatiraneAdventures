from game.effect import AGILITY, DEFENSE, DEXTERITY, ENDURANCE, MAGIC, MAGICAL_ATTACK, PHYSICAL_ATTACK, STRENGTH
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
        physical_attack = self._physical_attack
        if PHYSICAL_ATTACK in self._status_effects:
            physical_attack_effects = self._status_effects[PHYSICAL_ATTACK]
            for effect in physical_attack_effects:
                physical_attack *= 1 + effect.get_amount()
        return physical_attack

    def get_magical_attack(self):
        magical_attack = self._magical_attack
        if MAGICAL_ATTACK in self._status_effects:
            magical_attack_effects = self._status_effects[MAGICAL_ATTACK]
            for effect in magical_attack_effects:
                magical_attack *= 1 + effect.get_amount()
        return magical_attack

    def get_defense(self):
        defense = self._defense
        if DEFENSE in self._status_effects:
            defense_effects = self._status_effects[DEFENSE]
            for effect in defense_effects:
                defense *= 1 + effect.get_amount()
        return defense

    def get_strength(self):
        strength = self._strength
        if STRENGTH in self._status_effects:
            strength_effects = self._status_effects[STRENGTH]
            for effect in strength_effects:
                strength *= 1 + effect.get_amount()
        return strength

    def get_magic(self):
        magic = self._magic
        if MAGIC in self._status_effects:
            magic_effects = self._status_effects[MAGIC]
            for effect in magic_effects:
                magic *= 1 + effect.get_amount()
        return magic

    def get_endurance(self):
        endurance = self._endurance
        if ENDURANCE in self._status_effects:
            endurance_effects = self._status_effects[ENDURANCE]
            for effect in endurance_effects:
                endurance *= 1 + effect.get_amount()
        return endurance

    def get_dexterity(self):
        dexterity = self._dexterity
        if DEXTERITY in self._status_effects:
            dexterity_effects = self._status_effects[DEXTERITY]
            for effect in dexterity_effects:
                dexterity *= 1 + effect.get_amount()
        return dexterity

    def get_agility(self):
        agility = self._agility
        if AGILITY in self._status_effects:
            agility_effects = self._status_effects[AGILITY]
            for effect in agility_effects:
                agility *= 1 + effect.get_amount()
        return agility

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

    def apply_effect(self, effect_type, effect):
        if effect_type not in self._status_effects:
            self._status_effects[effect_type] = []
        self._status_effects[effect_type].append(effect)

    def clear_negative_effects(self):
        for effects in self._status_effects.values():
            dead_effects = []
            for effect in effects:
                if effect.get_amount() < 0:
                    dead_effects.append(effect)
            for dead_effect in dead_effects:
                effects.remove(dead_effect)

    def get_effects(self):
        return self._status_effects

    def update_effects(self, delta=1):
        for effects in self._status_effects.values():
            dead_effects = []
            for effect in effects:
                effect.reduce_duration(delta)
                if effect.get_duration() < 0:
                    dead_effects.append(effect)
            for dead_effect in dead_effects:
                effects.remove(dead_effect)
