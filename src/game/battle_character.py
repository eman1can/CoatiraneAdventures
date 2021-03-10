from game.battle_entity import BattleEntity


# Change character instance to a battle character
from game.status_effect import AGILITY, DEFENSE, DEXTERITY, ENDURANCE, MAGIC, MAGICAL_ATTACK, PHYSICAL_ATTACK, STRENGTH
from spine.animation.animationstate import AnimationState
from spine.animation.animationstatedata import AnimationStateData


def create_battle_character(character, support):
    # character.__class__ = BattleCharacter
    return BattleCharacter(character, support)


class BattleCharacter(BattleEntity):
    def __init__(self, character, support):
        # BattleEntity.__init__(self)
        # self.refresh_stats()
        self._in_battle = False
        self._skeleton = None
        self._animation_state = None
        self._character = character
        self._support = support
        self._selected_skill = character.get_skill(0)
        super().__init__()
        self._bhealth = self._character.get_health()
        self._bmana = self._character.get_mana()

    # def rollback(self):
    #     self.__class__ = Character

    def c(self):
        return self._character

    def get_id(self):
        return self._character.get_id()

    def get_name(self):
        return self._character.get_name()

    def get_health(self):
        return self._character.get_health()

    def get_mana(self):
        return self._character.get_mana()

    def is_character(self):
        return True

    def is_enemy(self):
        return False

    def get_idle_animation(self):
        if self._in_battle:
            return 'idleBattle'
        return 'idle_side'

    def load_skeleton(self, loader):
        self._skeleton = loader.load_skeleton(self._character.get_skeleton_path(), False, 0.125)
        self._skeleton.setWidth(self._skeleton.getData().getWidth() * 0.125)
        self._skeleton.setHeight(self._skeleton.getData().getHeight() * 0.125)
        data = AnimationStateData(self._skeleton.getData())
        data.setDefaultMix(0.25)
        self._animation_state = AnimationState(data)
        self._skeleton.setSkin(self._skeleton.getData().getSkins()[0].getName())
        self.set_animation_idle(loop=True)
        self.reset_battle_effects()
        return self._animation_state, self._skeleton

    def reset_battle_effects(self):
        self._status_effects = {}
        self._markers = {}
        self._bhealth = self._character.health
        self._bmana = self._character.mana

    def get_skeleton(self):
        if self._skeleton is None:
            print("Skeleton is not yet loaded!")
            return
        return self._skeleton

    def set_animation_idle(self, add=False, track=0, loop=False, delay=0):
        if not add:
            self._animation_state.setAnimation(track, self.get_idle_animation(), loop)
        else:
            self._animation_state.addAnimation(track, self.get_idle_animation(), loop, delay)

    def play_idle_animation(self):
        self._animation_state.setAnimation(0, 'idle_action', False)
        self.set_animation_idle(loop=True)

    def select_skill(self, index):
        self._selected_skill = self._character.get_skill(index)

    def get_selected_skill(self):
        return self._selected_skill

    def get_skills(self):
        return self._character.get_skills()

    def get_description_recap(self):
        string = self._character.get_name()
        string += f':\n\tHealth: {self.get_battle_health()}/{self.get_health()} - Mana: {self.get_battle_mana()}/{self.get_mana()}\n\tEffects:'
        if len(self._status_effects) > 0:
            for effect in self._status_effects:
                string += f'\n\t{effect.get_description()}'
        else:
            string += '\n\tNone'
        return string

    def get_physical_attack(self):
        if self._support is not None:
            physical_attack = self._character.get_physical_attack() + self._support.get_physical_attack()
        else:
            physical_attack = self._character.get_physical_attack()
        if PHYSICAL_ATTACK in self._status_effects:
            physical_attack_effects = self._status_effects[PHYSICAL_ATTACK]
            for effect in physical_attack_effects:
                physical_attack *= 1 + effect.st[0]
        return physical_attack

    def get_magical_attack(self):
        if self._support is not None:
            magical_attack = self._character.get_magical_attack() + self._support.get_magical_attack()
        else:
            magical_attack = self._character.get_magical_attack()
        if MAGICAL_ATTACK in self._status_effects:
            magical_attack_effects = self._status_effects[MAGICAL_ATTACK]
            for effect in magical_attack_effects:
                magical_attack *= 1 + effect.st[0]
        return magical_attack

    def get_defense(self):
        if self._support is not None:
            defense = self._character.get_defense() + self._support.get_defense()
        else:
            defense = self._character.get_defense()
        if DEFENSE in self._status_effects:
            defense_effects = self._status_effects[DEFENSE]
            for effect in defense_effects:
                defense *= 1 + effect.st[0]
        return defense

    def get_strength(self):
        if self._support is not None:
            strength = self._character.get_strength() + self._support.get_strength()
        else:
            strength = self._character.get_strength()
        if STRENGTH in self._status_effects:
            strength_effects = self._status_effects[STRENGTH]
            for effect in strength_effects:
                strength *= 1 + effect.st[0]
        return strength

    def get_magic(self):
        if self._support is not None:
            magic = self._character.get_magic() + self._support.get_magic()
        else:
            magic = self._character.get_magic()
        if MAGIC in self._status_effects:
            magic_effects = self._status_effects[MAGIC]
            for effect in magic_effects:
                magic *= 1 + effect.st[0]
        return magic

    def get_endurance(self):
        if self._support is not None:
            endurance = self._character.get_endurance() + self._support.get_endurance()
        else:
            endurance = self._character.get_endurance()
        if ENDURANCE in self._status_effects:
            endurance_effects = self._status_effects[ENDURANCE]
            for effect in endurance_effects:
                endurance *= 1 + effect.st[0]
        return endurance

    def get_dexterity(self):
        if self._support is not None:
            dexterity = self._character.get_dexterity() + self._support.get_dexterity()
        else:
            dexterity = self._character.get_dexterity()
        if DEXTERITY in self._status_effects:
            dexterity_effects = self._status_effects[DEXTERITY]
            for effect in dexterity_effects:
                dexterity *= 1 + effect.st[0]
        return dexterity

    def get_agility(self):
        if self._support is not None:
            agility = self._character.get_agility() + self._support.get_agility()
        else:
            agility = self._character.get_agility()
        if AGILITY in self._status_effects:
            agility_effects = self._status_effects[AGILITY]
            for effect in agility_effects:
                agility *= 1 + effect.st[0]
        return agility

    def get_element(self):
        return self._character.get_element()

    def get_counter_skill(self):
        self._character.get_counter_skill()