from random import randint, uniform

from game.battle_entity import BattleEntity

# Change character instance to a battle character
from game.effect import AGILITY, DEFENSE, DEXTERITY, ENDURANCE, MAGIC, MAGICAL_ATTACK, PHYSICAL_ATTACK, STRENGTH
from game.skill import DARK, EARTH, FIRE, LIGHT, THUNDER, WATER, WIND
# from spine.animation.animationstate import AnimationState
# from spine.animation.animationstatedata import AnimationStateData


def create_battle_character(character, support):
    return BattleCharacter(character, support)


class BattleCharacter(BattleEntity):
    def __init__(self, character, support):
        self._in_battle = False
        self._skeleton = None
        self._animation_state = None
        self._character = character
        self._support = support
        self._selected_skill = character.get_skill(0)

        super().__init__()

        self._bhealth = self._character.get_health()
        self._bmana = self._character.get_mana()
        self._stamina = self._character.get_agility() + self._character.get_dexterity()
        if self._support:
            self._stamina += self._support.get_agility() + self._support.get_dexterity()
        self._stamina *= 5
        self._max_stamina = self._stamina
        self._rest_counter = 2

    def take_action(self, weight=1):
        # Taking an action reduces stamina by 3 - 10
        self.decrease_stamina(uniform(3 * weight, 10 * weight))

    def walk(self, weight=1):
        # Walking reduces stamina by 1 - 5
        self.decrease_stamina(uniform(1 * weight, 3 * weight))

    def rest(self):
        if self._stamina < 0:
            self._rest_counter -= 1
            if self._rest_counter == 0:
                self.wake_up()
            return
        self._stamina += min(uniform(20, 30), self._max_stamina - self._stamina)
        self._bhealth += min(self.get_health() * 0.15, self.get_health() - self._bhealth)
        self._bmana += min(self.get_mana() * 0.15, self.get_mana() - self._bmana)

    def wake_up(self):
        self._stamina = self._max_stamina * 0.5

    def decrease_stamina(self, amount):
        self._stamina -= amount
        if self._stamina < 0:
            self._rest_counter = 2

    def can_take_action(self):
        return self._stamina / self._max_stamina > 0.25

    def get_stamina(self):
        return self._stamina

    def get_stamina_message(self):
        if self._bhealth <= 0:
            return ' - Incapacitated'
        if self._stamina / self._max_stamina > 0.95:
            return ' - Pumped'
        elif self._stamina / self._max_stamina > 0.75:
            return ' - Awake'
        elif self._stamina / self._max_stamina > 0.50:
            return ' - Sleepy'
        elif self._stamina / self._max_stamina > 0.25:
            return ' - Tired'
        elif self._stamina > 0:
            return ' - Exhausted'
        else:
            return ' - Asleep'

    def get_stamina_modifier(self):
        if self._stamina / self._max_stamina > 0.95:
            return 1
        elif self._stamina / self._max_stamina > 0.75:
            return 1
        elif self._stamina / self._max_stamina > 0.50:
            return 0.95
        elif self._stamina / self._max_stamina > 0.25:
            return 0.85
        elif self._stamina > 0:
            return 0.5
        else:
            return 0

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

    def get_mana_cost(self, skill):
        return self._character.get_mana_cost(skill)

    def is_character(self):
        return True

    def is_enemy(self):
        return False

    def get_idle_animation(self):
        if self._in_battle:
            return 'idleBattle'
        return 'idle_side'

    # def load_skeleton(self, loader):
    #     self._skeleton = loader.load_skeleton(self._character.get_skeleton_path(), False, 0.125)
    #     self._skeleton.setWidth(self._skeleton.getData().getWidth() * 0.125)
    #     self._skeleton.setHeight(self._skeleton.getData().getHeight() * 0.125)
    #     data = AnimationStateData(self._skeleton.getData())
    #     data.setDefaultMix(0.25)
    #     self._animation_state = AnimationState(data)
    #     self._skeleton.setSkin(self._skeleton.getData().getSkins()[0].getName())
    #     self.set_animation_idle(loop=True)
    #     self.reset_battle_effects()
    #     return self._animation_state, self._skeleton

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

    def get_support(self):
        return self._support

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
            physical_attack = (self._character.get_physical_attack() + self._support.get_physical_attack()) - (self._character.get_strength() + self._support.get_strength()) + self.get_strength()
        else:
            physical_attack = self._character.get_physical_attack() - self._character.get_strength() + self.get_strength()
        return self._get_boosted_stat(PHYSICAL_ATTACK, physical_attack * self.get_stamina_modifier())

    def get_magical_attack(self):
        if self._support is not None:
            magical_attack = (self._character.get_magical_attack() + self._support.get_magical_attack()) - (self._character.get_magic() + self._support.get_magic()) + self.get_magic()
        else:
            magical_attack = self._character.get_magical_attack() - self._character.get_magic() + self.get_magic()
        return self._get_boosted_stat(MAGICAL_ATTACK, magical_attack * self.get_stamina_modifier())

    def get_defense(self):
        if self._support is not None:
            defense = self._character.get_defense() + self._support.get_defense()
        else:
            defense = self._character.get_defense()
        return self._get_boosted_stat(DEFENSE, defense * self.get_stamina_modifier())

    def get_strength(self):
        if self._support is not None:
            strength = self._character.get_strength() + self._support.get_strength()
        else:
            strength = self._character.get_strength()
        return self._get_boosted_stat(STRENGTH, strength * self.get_stamina_modifier())

    def get_magic(self):
        if self._support is not None:
            magic = self._character.get_magic() + self._support.get_magic()
        else:
            magic = self._character.get_magic()
        return self._get_boosted_stat(MAGIC, magic * self.get_stamina_modifier())

    def get_endurance(self):
        if self._support is not None:
            endurance = self._character.get_endurance() + self._support.get_endurance()
        else:
            endurance = self._character.get_endurance()
        return self._get_boosted_stat(ENDURANCE, endurance * self.get_stamina_modifier())

    def get_agility(self):
        if self._support is not None:
            agility = self._character.get_agility() + self._support.get_agility()
        else:
            agility = self._character.get_agility()
        return self._get_boosted_stat(AGILITY, agility * self.get_stamina_modifier())

    def get_dexterity(self):
        if self._support is not None:
            dexterity = self._character.get_dexterity() + self._support.get_dexterity()
        else:
            dexterity = self._character.get_dexterity()
        return self._get_boosted_stat(DEXTERITY, dexterity * self.get_stamina_modifier())

    def get_element(self):
        return self._character.get_element()

    def get_counter_skill(self):
        self._character.get_counter_skill()

    def element_modifier(self, element):
        if element == WATER:
            if self._character.get_element() == FIRE:
                return 2.0
            elif self._character.get_element() == THUNDER:
                return 0.5
        elif element == FIRE:
            if self._character.get_element() == WIND:
                return 2.0
            elif self._character.get_element() == WATER:
                return 0.5
        elif element == THUNDER:
            if self._character.get_element() == WATER:
                return 2.0
            elif self._character.get_element() == THUNDER:
                return 0.5
        elif element == WIND:
            if self._character.get_element() == EARTH:
                return 2.0
            elif self._character.get_element() == FIRE:
                return 0.5
        elif element == EARTH:
            if self._character.get_element() == THUNDER:
                return 2.0
            elif self._character.get_element() == WIND:
                return 0.5
        elif element == LIGHT:
            if self._character.get_element() == DARK:
                return 2.0
        elif element == DARK:
            if self._character.get_element() == LIGHT:
                return 2.0
        return 1.0
