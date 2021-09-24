from random import uniform

from game.battle_entity import BattleEntity

# Change character instance to a battle character
from game.effect import AGILITY, DEFENSE, DEXTERITY, ENDURANCE, MAGIC, MAGICAL_ATTACK, PHYSICAL_ATTACK, STRENGTH
from refs import Refs


def create_battle_character(character, support):
    return BattleCharacter(character, support)


class BattleCharacter(BattleEntity):
    def __init__(self, character, support):
        self._in_battle = False
        self._support = support

        super().__init__(character)

        self._selected_skill = 0

        self._battle_health = self.get_health()
        self._battle_mana = self.get_mana()
        self._stamina = self._base.get_agility() + self._base.get_dexterity()
        if self._support:
            self._stamina += self._support.get_agility() + self._support.get_dexterity()
        self._stamina *= 5
        self._max_stamina = self._stamina
        self._rest_counter = 2
        self._death_rest_counter = 10
        self._special_amount = 0

    def is_character(self):
        return True

    def is_enemy(self):
        return False

    def set_in_battle(self, battle):
        self._in_battle = battle

    def in_battle(self):
        return self._in_battle

    def is_asleep(self):
        return self._stamina <= 0

    def get_death_rest_count(self):
        return self._death_rest_counter

    def load_skeleton(self, skeleton_loader, scale=1):
        super().load_skeleton(skeleton_loader, Refs.gc.get_skeleton_scale() * scale)

    def get_special_amount(self):
        return self._special_amount

    def increase_special_amount(self, amount):
        self._special_amount = min(10, self._special_amount + amount)

    def take_action(self, weight=1):
        # Taking an action reduces stamina by 3 - 10
        self.decrease_stamina(uniform(3 * weight, 10 * weight))

    def walk(self, weight=1):
        # Walking reduces stamina by 1 - 5
        self.decrease_stamina(uniform(1 * weight, 3 * weight))

    def rest(self):
        if self.is_dead():
            self._death_rest_counter -= 1
            if self._death_rest_counter == 0:
                self.wake_up()
                self._battle_health = min(self.get_health() * 0.05, self.get_health() - self._battle_health)
            return
        elif self._stamina < 0:
            self._rest_counter -= 1
            if self._rest_counter == 0:
                self.wake_up()
            return
        self._stamina += min(uniform(20, 30), self._max_stamina - self._stamina)
        self._battle_health += min(self.get_health() * 0.10, self.get_health() - self._battle_health)
        self._battle_mana += min(self.get_mana() * 0.10, self.get_mana() - self._battle_mana)

    def wake_up(self):
        self._stamina = self._max_stamina * 0.5

    def decrease_stamina(self, amount):
        self._stamina -= amount
        if self._stamina < 0:
            self._rest_counter = 2

    def decrease_health(self, damage):
        super().decrease_health(damage)
        if self._battle_health < 0:
            self._stamina = 0

    def can_take_action(self):
        return self._stamina / self._max_stamina > 0.25

    def get_stamina(self):
        return self._stamina

    def get_stamina_max(self):
        return self._max_stamina

    def get_stamina_message(self):
        if self._battle_health <= 0:
            return ' - Incapacitated'
        if self._stamina / self._max_stamina >= 0.95:
            return ' - Pumped'
        elif self._stamina / self._max_stamina >= 0.75:
            return ' - Awake'
        elif self._stamina / self._max_stamina >= 0.50:
            return ' - Sleepy'
        elif self._stamina / self._max_stamina >= 0.25:
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

    def get_idle_animation(self):
        if self._in_battle:
            if self.has_status_effect():
                return 'status_ailment'
            return 'idleBattle'
        return 'idle_side'

    def play_idle_animation(self):
        self._animation_state.setAnimation(0, 'idle_action', False)
        self.set_animation_idle(add=True, loop=True)

    def select_skill(self, index):
        self._selected_skill = index

    def get_selected_skill(self):
        return self._base.get_skills()[self._selected_skill]

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
            physical_attack = (self._base.get_physical_attack() + self._support.get_physical_attack()) - (self._base.get_strength() + self._support.get_strength()) + self.get_strength()
        else:
            physical_attack = self._base.get_physical_attack() - self._base.get_strength() + self.get_strength()
        return self._get_boosted_stat(PHYSICAL_ATTACK, physical_attack * self.get_stamina_modifier())

    def get_magical_attack(self):
        if self._support is not None:
            magical_attack = (self._base.get_magical_attack() + self._support.get_magical_attack()) - (self._base.get_magic() + self._support.get_magic()) + self.get_magic()
        else:
            magical_attack = self._base.get_magical_attack() - self._base.get_magic() + self.get_magic()
        return self._get_boosted_stat(MAGICAL_ATTACK, magical_attack * self.get_stamina_modifier())

    def get_defense(self):
        if self._support is not None:
            defense = self._base.get_defense() + self._support.get_defense()
        else:
            defense = self._base.get_defense()
        return self._get_boosted_stat(DEFENSE, defense * self.get_stamina_modifier())

    def get_strength(self):
        if self._support is not None:
            strength = self._base.get_strength() + self._support.get_strength()
        else:
            strength = self._base.get_strength()
        return self._get_boosted_stat(STRENGTH, strength * self.get_stamina_modifier())

    def get_magic(self):
        if self._support is not None:
            magic = self._base.get_magic() + self._support.get_magic()
        else:
            magic = self._base.get_magic()
        return self._get_boosted_stat(MAGIC, magic * self.get_stamina_modifier())

    def get_endurance(self):
        if self._support is not None:
            endurance = self._base.get_endurance() + self._support.get_endurance()
        else:
            endurance = self._base.get_endurance()
        return self._get_boosted_stat(ENDURANCE, endurance * self.get_stamina_modifier())

    def get_agility(self):
        if self._support is not None:
            agility = self._base.get_agility() + self._support.get_agility()
        else:
            agility = self._base.get_agility()
        return self._get_boosted_stat(AGILITY, agility * self.get_stamina_modifier())

    def get_dexterity(self):
        if self._support is not None:
            dexterity = self._base.get_dexterity() + self._support.get_dexterity()
        else:
            dexterity = self._base.get_dexterity()
        return self._get_boosted_stat(DEXTERITY, dexterity * self.get_stamina_modifier())
