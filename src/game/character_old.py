__all__ = ('Character',)

# Project Imports
from refs import Refs
from .skill import Skill
from .scale import Scale
from spine.animation.animationstate import AnimationState
from spine.animation.animationstatedata import AnimationStateData

# Standard Library Imports
import math


class Character:
    def __init__(self, rank, type, element, skills, familias, **kwargs):
        # Definitions
        self.health_base = 0  # type: float
        self.mana_base = 0  # type: float
        self.strength_base = 0  # type: float
        self.magic_base = 0  # type: float
        self.endurance_base = 0  # type: float
        self.dexterity_base = 0  # type: float
        self.agility_base = 0  # type: float

        self.name = ""  # type: str
        self.display_name = ""  # type: str
        self.id = ""  # type: str
        self.skel_id = ""  # type: str
        self.skel_path = ""  # type: str
        self._is_support = False  # type: bool
        self.index = 0  # type: int

        self.slide_image_source = ""  # type: str
        self.slide_support_image_source = ""  # type: str
        self.preview_image_source = ""  # type: str
        self.full_image_source = ""  # type: str
        self.bustup_image_source = ""  # type: str

        self.current_rank = 1  # type: int
        self.current_health = 0  # type: int
        self.element = ""  # type: str
        self.type = ""  # type: str

        self.familiarities = {}  # type: dict
        self.familiarity_bonus = 0.0  # type: float

        # Load kwargs
        for kwarg, value in kwargs.items():
            if hasattr(self, kwarg):
                setattr(self, kwarg, value)
        for key in [kwarg for kwarg in kwargs if hasattr(self, kwarg)]: del kwargs[key]

        super().__init__(**kwargs)

        # Experimental - Most still need to be implemented fully
        self.familia = None
        for familia in familias:
            if familia.name == 'Hestia':
                self.familia = familia
                break
        self.race = 'Human'
        self.gender = 'Female'
        self.score = 0
        self.worth = 0
        self.high_dmg = 0
        self.floor_depth = 0
        self.monsters_slain = 0
        self.people_slain = 0

        self.equipment = Equipment()
        self.markers = {}

        self.skeleton = None
        self.animation_state = None

        self.abilities = []

        # End Experimental

        try:
            self.ranks = Rank.load_weights("../save/char_load_data/" + Refs.gc.get_program_type() + '/ranks/' + self.id + '.txt', self.id, rank, Refs.gc.get_program_type())
        except FileNotFoundError:
            self.ranks = Rank.load_weights("../save/char_load_data/" + Refs.gc.get_program_type() + '/ranks/base.txt', self.id, rank, Refs.gc.get_program_type())

        if self.skel_id is not None:
            if self.skel_id == 'no_skin':
                self.skel_path = 'characters/badass_ais/1041002011.skel'
            else:
                self.skel_path = 'characters/' + self.id + '/' + self.skel_id + '.skel'

        self.update_score()

    def update_score(self):
        score = 0
        if self.type == 'Physical':
            score += self.get_strength() / 7.5
            score += self.get_magic() / 10
            score += self.get_endurance() / 8.5
            score += self.get_dexterity() / 9
            score += self.get_agility() / 9
        elif self.type == 'Magical':
            score += self.get_strength() / 10
            score += self.get_magic() / 7.5
            score += self.get_endurance() / 10
            score += self.get_dexterity() / 9
            score += self.get_agility() / 9
        elif self.type == 'Balanced':
            score += self.get_strength() / 8.5
            score += self.get_magic() / 8.5
            score += self.get_endurance() / 9.5
            score += self.get_dexterity() / 9
            score += self.get_agility() / 9
        elif self.type == 'Defensive':
            score += self.get_strength() / 8.5
            score += self.get_magic() / 10
            score += self.get_endurance() / 7.5
            score += self.get_dexterity() / 9
            score += self.get_agility() / 9
        elif self.type == 'Healing':
            score += self.get_strength() / 10
            score += self.get_magic() / 8.5
            score += self.get_endurance() / 10
            score += self.get_dexterity() / 9
            score += self.get_agility() / 9
        self.score = score

    def is_support(self):
        return self._is_support

    def get_type(self):
        return self.type

    def get_index(self):
        return self.index

    def get_familia(self):
        return self.familia

    def get_race(self):
        return self.race

    def get_gender(self):
        return self.gender

    def get_worth(self):
        return self.worth

    def get_high_dmg(self):
        return self.high_dmg

    def get_floor_depth(self):
        return self.floor_depth

    def get_monsters_killed(self):
        return self.monsters_slain

    def get_people_killed(self):
        return self.people_slain

    def get_equipment(self):
        return self.equipment

    def get_element(self):
        return self.element

    def get_current_rank(self):
        return self.current_rank

    def get_rank(self, index):
        return self.ranks[index - 1]

    def rank_up(self):
        if self.current_rank < 10:
            self.current_rank += 1
            self.ranks[self.current_rank - 1].unlocked = True

    def rank_break(self):
        if not self.ranks[self.current_rank - 1].broken:
            self.ranks[self.current_rank - 1].break_rank(self.type)
            self.update_score()

    def get_sprite(self):
        return self.sprite

    def get_name(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def get_id(self):
        return self.id

    def get_skel_id(self):
        return self.skel_id

    def get_skills(self):
        return self.skills

        # if skill_num <= 2:
        #     print("return", self.skills[skill_num + 3].name)
        #     return self.skills[skill_num + 3]
        # if skill_num == 4:
        #     print("return", self.skills[skill_num + 2].name)
        #     return self.skills[skill_num + 2]
        # if skill_num < len(self.skills) - 1:
        #     print("return", self.skills[skill_num + 1].name)
        #     return self.skills[skill_num + 1]
        # return None

    def get_ability(self, ability_num):
        if ability_num < len(self.abilities):
            return self.abilities[ability_num]
        return None

    def get_ability_options(self, abilities):
        return abilities[:3]

    def add_ability(self, ability):
        self.abilities.append(ability)

    def get_phyatk(self, rank=0, in_battle=False):
        phyatk = self.get_strength(rank, in_battle) + self.equipment.get_phyatk()
        if not in_battle:
            return phyatk
        else:
            if Skill.PHYSICAL_ATTACK in self.status_effects:
                strengthEffects = self.status_effects[Skill.PHYSICAL_ATTACK]
                for effect in strengthEffects:
                    phyatk *= 1 + effect.st[0]
            return phyatk

    def get_magatk(self, rank=0, in_battle=False):
        magatk = self.get_magic(rank, in_battle) + self.equipment.get_magatk()
        if not in_battle:
            return magatk
        else:
            if Skill.MAGICAL_ATTACK in self.status_effects:
                strengthEffects = self.status_effects[Skill.MAGICAL_ATTACK]
                for effect in strengthEffects:
                    magatk *= 1 + effect.st[0]
            return magatk

    def get_defense(self, rank=0, in_battle=False):
        defense = self.get_endurance(rank) + self.equipment.get_defense()
        if not in_battle:
            return defense
        if Skill.DEFENSE in self.status_effects:
            defenseEffects = self.status_effects[Skill.DEFENSE]
            for effect in defenseEffects:
                defense *= 1 + effect.st[0]
        return defense

    def get_health(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_health() * self.familiarity_bonus
        health = self.health_base + self.equipment.get_health()
        for rank in self.ranks:
            if rank.unlocked:
                health += rank.get_health()
        return health * self.familiarity_bonus

    def get_mana(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_mana() * self.familiarity_bonus
        mana = self.mana_base + self.equipment.get_mana()
        for rank in self.ranks:
            if rank.unlocked:
                mana += rank.get_mana()
        return mana * self.familiarity_bonus

    def get_strength(self, rank=0, in_battle=False):
        if rank > 0:
            return self.get_rank(rank).get_strength() * self.familiarity_bonus
        strength = self.strength_base + self.equipment.get_strength()
        for rank in self.ranks:
            if rank.unlocked:
                strength += rank.get_strength()
        strength *= self.familiarity_bonus
        if not in_battle:
            return strength
        else:
            if Skill.STRENGTH in self.status_effects:
                strengthEffects = self.status_effects[Skill.STRENGTH]
                for effect in strengthEffects:
                    strength *= 1 + effect.st[0]
            return strength

    def get_strength_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_strength(rank), 999)

    def get_magic(self, rank=0, in_battle=False):
        if rank > 0:
            return self.get_rank(rank).get_magic() * self.familiarity_bonus
        magic = self.magic_base + self.equipment.get_magic()
        for rank in self.ranks:
            if rank.unlocked:
                magic += rank.get_magic()
        magic *= self.familiarity_bonus
        if not in_battle:
            return magic
        else:
            if Skill.MAGIC in self.status_effects:
                magicEffects = self.status_effects[Skill.MAGIC]
                for effect in magicEffects:
                    magic *= 1 + effect.st[0]
            return magic

    def get_magic_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_magic(rank), 999)

    def get_endurance(self, rank=0, in_battle=False):
        if rank > 0:
            return self.get_rank(rank).get_endurance() * self.familiarity_bonus
        endurance = self.endurance_base + self.equipment.get_endurance()
        for rank in self.ranks:
            if rank.unlocked:
                endurance += rank.get_endurance()
        endurance *= self.familiarity_bonus
        if not in_battle:
            return endurance
        else:
            if Skill.ENDURANCE in self.status_effects:
                enduranceEffects = self.status_effects[Skill.ENDURANCE]
                for effect in enduranceEffects:
                    endurance *= 1 + effect.st[0]
            return endurance

    def get_endurance_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_endurance(rank), 999)

    def get_dexterity(self, rank=0, in_battle=False):
        if rank > 0:
            return self.get_rank(rank).get_dexterity() * self.familiarity_bonus
        dexterity = self.dexterity_base + self.equipment.get_dexterity()
        for rank in self.ranks:
            if rank.unlocked:
                dexterity += rank.get_dexterity()
        dexterity *= self.familiarity_bonus
        if not in_battle:
            return dexterity
        else:
            if Skill.DEXTERITY in self.status_effects:
                dexterityEffects = self.status_effects[Skill.DEXTERITY]
                for effect in dexterityEffects:
                    dexterity *= 1 + effect.st[0]
            return dexterity

    def get_dexterity_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_dexterity(rank), 999)

    def get_agility(self, rank=0, in_battle=False):
        if rank > 0:
            return self.get_rank(rank).get_agility() * self.familiarity_bonus
        agility = self.agility_base + self.equipment.get_agility()
        for rank in self.ranks:
            if rank.unlocked:
                agility += rank.get_agility()
        agility *= self.familiarity_bonus
        if not in_battle:
            return agility
        else:
            if Skill.AGILITY in self.status_effects:
                agilityEffects = self.status_effects[Skill.AGILITY]
                for effect in agilityEffects:
                    agility *= 1 + effect.st[0]
            return agility

    def get_agility_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_agility(rank), 999)

    def get_score(self):
        return round(self.score, 1)

    def update_health(self, health_change, rank):
        self.ranks[rank].update_health(health_change)
        self.update_score()

    def update_mana(self, mana_change, rank):
        self.ranks[rank].update_mana(mana_change)
        self.update_score()

    def update_strength(self, strength_change, rank, board=False):
        self.ranks[rank].update_strength(strength_change, board)
        self.update_score()

    def update_magic(self, magic_change, rank, board=False):
        self.ranks[rank].update_magic(magic_change, board)
        self.update_score()

    def update_endurance(self, endurance_change, rank, board=False):
        self.ranks[rank].update_endurance(endurance_change, board)
        self.update_score()

    def update_dexterity(self, dexterity_change, rank, board=False):
        self.ranks[rank].update_dexterity(dexterity_change, board)
        self.update_score()

    def update_agility(self, agility_change, rank, board=False):
        self.ranks[rank].update_agility(agility_change, board)
        self.update_score()

    def max_stats(self):
        rank = self.get_rank(self.get_current_rank())
        rank.max_stats()
        self.update_score()

    def equip_equipment(self, slot, equipment):
        if self.equipment.get_type(slot) is not None:
            print("Item already equipped")
        else:
            self.equipment.set_type(slot, equipment)
        self.update_score()

    def unequip_equipment(self, slot):
        if self.equipment.get_type(slot) is None:
            print("There is no item equipped")
        else:
            self.equipment.set_type(slot, None)

    def update_equipment(self, slot, stat):
        self.equipment.update_type(slot, stat)

    def get_grids(self):
        return self.ranks

    def get_familiarity(self, char_id):
        if char_id in self.familiarities:
            return self.familiarities[char_id]
        return 0

    def add_familiarity(self, key, value):
        if key in self.familiarities:
            if self.familiarities[key] == 100.00:
                return
            if self.familiarities[key] + value > 100.00:
                self.familiarities[key] = 100.00
                return
            self.familiarities[key] += value
        else:
            self.familiarities[key] = value

    # def get_ability(self, rank_num):
    #     if rank_num > len(self.abilities) - 1:
    #         return None
    #     return self.abilities[rank_num - 2]

    def load_skeleton(self, skeleton_loader):
        self.skeleton = skeleton_loader.load_skeleton(self.skel_path, False, 0.125)
        self.skeleton.setWidth(self.skeleton.getData().getWidth() * 0.125)
        self.skeleton.setHeight(self.skeleton.getData().getHeight() * 0.125)
        data = AnimationStateData(self.skeleton.getData())
        data.setDefaultMix(0.25)
        self.animation_state = AnimationState(data)
        self.skeleton.setSkin(self.skeleton.getData().getSkins()[0].getName())
        self.set_animation_idle(loop=True)
        self.reset_battle_effects()
        return self.animation_state, self.skeleton

    def get_skeleton(self):
        if self.skeleton is None:
            print("Skeleton is not yet loaded!")
            return
        return self.skeleton

    def set_animation_idle(self, add=False, track=0, loop=False, delay=0):
        if not add:
            self.animation_state.setAnimation(track, 'idle_side', loop)
        else:
            self.animation_state.addAnimation(track, 'idle_side', loop, delay)

    def set_animation_idle_battle(self, add=False, track=0, loop=False, delay=0):
        if not add:
            self.animation_state.setAnimation(track, 'idleBattle', loop)
        else:
            self.animation_state.addAnimation(track, 'idleBattle', loop, delay)

    def play_idle_animation(self):
        self.animation_state.setAnimation(0, 'idle_action', False)
        self.set_animation_idle(loop=True)

    def reset_battle_effects(self):
        self.status_effects = []
        self.battle_health = self.get_health()
        self.battle_mana = self.get_mana()

    def addMarker(self, id, marker):
        self.markers[id] = marker

    def addMarkersToWindow(self, window):
        for id, marker in self.markers.items():
            window.add_widget(marker)

    def showMarkers(self):
        for id, marker in self.markers.items():
            marker.appear()

    def fadeOutMarkers(self, fade_time):
        for id, marker in self.markers.items():
            marker.fade_out(fade_time)
        self.markers = {}

    ### Possibly removing stuff below

    def get_attack(self, skill_type):
        if skill_type == Skill.PHYSICAL:
            return self.get_phyatk(in_battle=True)
        elif skill_type == Skill.MAGICAL:
            return self.get_magatk(in_battle=True)
        else:
            return (self.get_phyatk() + self.get_magatk()) / 2

    def get_health_battle(self):
        return self.battle_health

    def is_dead(self):
        return self.battle_health <= 0

    def update_health_battle(self, damage):
        self.battle_health -= damage

    def update_mana_battle(self, mana_cost):
        self.battle_mana -= mana_cost

    def get_mana_battle(self):
        return self.battle_mana

    def apply_effect(self, status_effect):
        if status_effect.type not in self.status_effects:
            self.status_effects[status_effect.type] = []
        print("Add effect:", status_effect.type, "with duration of", status_effect.duration)
        self.status_effects[status_effect.type].append(status_effect)

    def get_status_effects(self):
        return self.status_effects

    def update_status_effects(self):
        # TODO - On live battle, update by delta
        remove = []
        for effectList in self.status_effects.values():
            for effect in effectList:
                print("Effect:", effect.type, effect.duration, "→", effect.duration - 1)
                if effect.duration > 0:
                    effect.duration -= 1
                if effect.duration == 0:
                    effectList.remove(effect)
                    if len(effectList) == 0:
                        remove.append(effect.type)
        for dead_effect in remove:
            del self.status_effects[dead_effect]

    def get_idle_animation(self):
        # Change based on status effects
        return 'idleBattle'

    ### End Remove


class Rank:
    def __init__(self, rank, grid, unlocked, broken, **kwargs):
        # Definitions
        self.ability_max = 99  # type: int
        self.health_max = 99  # type: int
        self.mana_max = 99  # type: int

        self.health = 0  # type: int
        self.mana = 0  # type: int

        # Defense is endurance
        # Attack is Strength / Magic / Both

        self.strength = 0  # type: int
        self.strength_board = 0  # type: int
        self.magic = 0  # type: int
        self.magic_board = 0  # type: int
        self.endurance = 0  # type: int
        self.endurance_board = 0  # type: int
        self.dexterity = 0  # type: int
        self.dexterity_board = 0  # type: int
        self.agility = 0  # type: int
        self.agility_board = 0  # type: int

        super().__init__(**kwargs)
        self.unlocked = unlocked
        self.broken = broken
        self.index = rank
        self.grid = grid
        self.brkinc = 1.25

        # self.grid.count()
    def max_stats(self):
        self.health = self.ability_max
        self.mana = self.ability_max
        self.strength = self.ability_max
        self.magic = self.ability_max
        self.endurance = self.ability_max
        self.dexterity = self.ability_max
        self.dexterity = self.ability_max
        self.agility = self.ability_max
        for x in range(len(self.grid.grid)):
            self.grid.unlock(x)

    def get_health(self):
        return math.floor(self.health)

    def get_health_cap(self):
        return self.health_max

    def get_mana(self):
        return math.floor(self.mana)

    def get_mana_cap(self):
        return self.mana_max

    def get_ability_cap(self):
        return self.ability_max

    def get_strength(self):
        return math.floor(self.strength) + math.floor(self.strength_board)

    def get_magic(self):
        return math.floor(self.magic) + math.floor(self.magic_board)

    def get_endurance(self):
        return math.floor(self.endurance) + math.floor(self.endurance_board)

    def get_dexterity(self):
        return math.floor(self.dexterity) + math.floor(self.dexterity_board)

    def get_agility(self):
        return math.floor(self.agility) + math.floor(self.agility_board)

    def get_rank_stats(self):
        return [self.get_health(), self.get_mana(), self.get_strength(), self.get_magic(), self.get_endurance(), self.get_dexterity(), self.get_agility()]

    def break_rank(self, type):
        self.broken = True
        self.health *= self.brkinc
        if type == 'Physical':
            self.mana *= self.brkinc * 0.75
            self.strength *= self.brkinc
            self.strength_board *= self.brkinc
            self.magic *= self.brkinc * 0.75
            self.magic_board *= self.brkinc * 0.75
            self.endurance *= self.brkinc * 0.75
            self.endurance_board *= self.brkinc * 0.75
        elif type == 'Magical':
            self.mana *= self.brkinc
            self.strength *= self.brkinc * 0.75
            self.strength_board *= self.brkinc * 0.75
            self.magic *= self.brkinc
            self.magic_board *= self.brkinc
            self.endurance *= self.brkinc * 0.75
            self.endurance_board *= self.brkinc * 0.75
        elif type == 'Balanced':
            self.mana *= self.brkinc * 0.75
            self.strength *= self.brkinc * 0.9
            self.strength_board *= self.brkinc * 0.9
            self.magic *= self.brkinc * 0.9
            self.magic_board *= self.brkinc * 0.9
            self.endurance *= self.brkinc * 0.75
            self.endurance_board *= self.brkinc * 0.75
        elif type == 'Defensive':
            self.mana *= self.brkinc * 0.75
            self.strength *= self.brkinc * 0.9
            self.strength_board *= self.brkinc * 0.9
            self.magic *= self.brkinc * 0.75
            self.magic_board *= self.brkinc * 0.75
            self.endurance *= self.brkinc
            self.endurance_board *= self.brkinc
        elif type == 'Healer':
            self.mana *= self.brkinc * 0.9
            self.strength *= self.brkinc * 0.75
            self.strength_board *= self.brkinc * 0.75
            self.magic *= self.brkinc * 0.9
            self.magic_board *= self.brkinc * 0.9
            self.endurance *= self.brkinc * 0.75
            self.endurance_board *= self.brkinc * 0.75
        self.dexterity *= self.brkinc * 0.9
        self.dexterity_board *= self.brkinc * 0.9
        self.agility *= self.brkinc * 0.9
        self.agility_board *= self.brkinc * 0.9

    def update_health(self, health_change):
        if self.health + health_change < self.health_max:
            self.health += health_change

    def update_mana(self, mana_change):
        if self.mana + mana_change < self.mana_max:
            self.mana += mana_change

    def update_strength(self, strength_change, board=False):
        if board:
            self.strength_board += strength_change
            # print(self.strength_board)
        else:
            if self.strength + strength_change < self.ability_max:
                self.strength += strength_change

    def update_magic(self, magic_change, board=False):
        if board:
            self.magic_board += magic_change
        else:
            if self.magic + magic_change < self.ability_max:
                self.magic += magic_change

    def update_endurance(self, endurance_change, board=False):
        if board:
            self.endurance_board += endurance_change
        else:
            if self.endurance + endurance_change < self.ability_max:
                self.endurance += endurance_change

    def update_dexterity(self, dexterity_change, board=False):
        if board:
            self.dexterity_board += dexterity_change
        else:
            if self.dexterity + dexterity_change < self.ability_max:
                self.dexterity += dexterity_change

    def update_agility(self, agility_change, board=False):
        if board:
            self.agility_board += agility_change
        else:
            if self.agility + agility_change < self.ability_max:
                self.agility += agility_change

    @staticmethod
    def load_weights(filename, id, rank_nums, program_type):
        file = open(filename)
        try:
            grids = Grid.load_grids("../save/char_load_data/" + program_type + "/grids/" + id + ".txt")
        except FileNotFoundError:
            grids = Grid.load_grids("../save/char_load_data/" + program_type + "/grids/base.txt")
        ranks = []
        count = 1
        # print("Loading Weights & girds")
        for level in range(0, len(rank_nums)):
            unlocked = rank_nums[level] > 0
            broken = rank_nums[level] == 2
            ranks.append(Rank(count, grids[count - 1], unlocked, broken))
            count += 1
        # for x in file:
        #     values = x[:-1].split(' ', -1)
        #     print("Loaded: " + str(values))
        #     if not count == 11:
        #         if ranknums[count-1] == 1:
        #             unlocked = True
        #             broken = False
        #         elif ranknums[count-1] == 2:
        #             unlocked = True
        #             broken = True
        #         else:
        #             unlocked = False
        #             broken = False
        #         rank = Rank(count, grids[count-1], unlocked, broken)
        #         count += 1
        #         ranks.append(rank)
        #     else:
        #         ranks.append(values)
        return ranks











# class Attack:
#     def __init__(self, name, ttype, type, damage):
#         self.name = name
#         self.ttype = ttype
#         self.type = type
#         self.damage = damage
#         if self.ttype == 0:
#             self.ttypeS = "Foe"
#         else:
#             self.ttypeS = "Foes"
#
#     def generateDamage(self, power):
#         percent = random.randint(0, 19) + 1
#         damage = percent / 14.0 * (power * ((self.damage+1.0)/3.4))
#         if self.ttype == 1:
#             damage * 0.8
#         return damage
#
#     def findfoe(self, numoffoes):
#         return random.randint(0, numoffoes)
#     #attack Name
#     #attack targeting type
#     #attack type 0 - foe 1 - foes
#     #attack damage 0 - Low 1 - Mid 2 - High 3 - Ultra 0-4,5-9,10-14,15-20
#
#     #attack elemental type
#     #attack special effects
#     #makeattack(power, type, effects) returns damage