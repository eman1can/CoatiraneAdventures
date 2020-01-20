import random
import math
from kivy.properties import NumericProperty, ObjectProperty, ReferenceListProperty, StringProperty, BooleanProperty, ListProperty
from kivy.uix.image import Image
from kivy.uix.widget import WidgetBase, Widget
from src.modules.Screens.FilledCharacterPreview import FilledCharacterPreview
from src.modules.Screens.SquareCharacterPreview import SquareCharacterPreview
from src.modules.Screens.CharacterAttributeScreens.CharacterAttributeScreen import CharacterAttributeScreen
from src.entitites.Character.Scale import Scale

class Character(WidgetBase):
    health_base = NumericProperty(0)
    mana_base = NumericProperty(0)
    strength_base = NumericProperty(0)
    magic_base = NumericProperty(0)
    endurance_base = NumericProperty(0)
    dexterity_base = NumericProperty(0)
    agility_base = NumericProperty(0)

    name = StringProperty(None)
    display_name = StringProperty(None)
    id = StringProperty(None)
    _is_support = BooleanProperty(False)
    index = NumericProperty(0)

    slide_image_source = StringProperty(None)
    slide_support_image_source = StringProperty(None)
    preview_image_source = StringProperty(None)
    full_image_source = StringProperty(None)
    program_type = StringProperty(None)

    current_rank = NumericProperty(1)
    current_health = NumericProperty(0)

    def __init__(self, rank, type, moves, familias, **kwargs):
        super().__init__(**kwargs)

        # Experimental
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
        self.element = 'light'

        self.equipment = Equipment()

        # End Experimental

        self.moves = moves
        if type == 0:
            self.type = 'Magical'
        elif type == 1:
            self.type = 'Physical'
        elif type == 2:
            self.type = 'Balance'
        elif type == 3:
            self.type = 'Defensive'
        else:
            self.type = 'Healer'

        try:
            self.ranks = Rank.load_weights("../save/char_load_data/" + self.program_type + '/ranks/' + self.id + '.txt', self.id, rank, self.program_type)
        except FileNotFoundError:
            self.ranks = Rank.load_weights("../save/char_load_data/" + self.program_type + '/ranks/base.txt', self.id, rank, self.program_type)

        self.slide_image = Image(source=self.slide_image_source, allow_stretch=True, size_hint=(None, None))
        if self._is_support:
            self.slide_support_image = Image(source=self.slide_support_image_source, allow_stretch=True, size_hint=(None, None))
        self.preview_image = Image(source=self.preview_image_source, allow_stretch=True, size_hint=(None, None))
        self.full_image = Image(source=self.full_image_source, allow_stretch=True, size_hint=(None, None))

    def load_elements(self): #MAINSCREEN preview size pos is_select, has_screen, char, support, is_support, new_instance
        self.select_widget = FilledCharacterPreview(is_select=True, is_support=self._is_support, character=self, size_hint_x=None)
        self.select_square_widget = SquareCharacterPreview(is_select=True, character=self, is_support=self._is_support)
        self.attr_screen = CharacterAttributeScreen(char=self) #char preview name size pos

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

    def get_rank(self, rankNum):
        return self.ranks[rankNum - 1]

    def rank_up(self):
        if self.current_rank < 10:
            self.current_rank += 1
            self.ranks[self.current_rank - 1].unlocked = True
        else:
            raise Exception("Character at max rank")

    def rank_break(self):
        if not self.ranks[self.current_rank - 1].broken:
            self.ranks[self.current_rank - 1].break_rank()
        else:
            raise Exception("Character already rank broken")

    def get_full_image(self, new_image_instance):
        if new_image_instance:
            return Image(source=self.full_image_source, allow_stretch=True, keep_ratio=True)
        if self.full_image.parent is not None:
            self.full_image.parent.slide_image_loaded = False
            index = 0
            for child in self.full_image.parent.children:
                if child == self.full_image:
                    self.full_image.parent.children[index] = Widget()
                    self.full_image.parent.children[index].id = 'image_standin_full'
                index += 1
            self.full_image.parent = None
            # self.slide_image.parent.remove_widget(self.slide_image)
        return self.full_image

    def get_slide_image(self, new_image_instance):
        if new_image_instance:
            return Image(source=self.slide_image_source, allow_stretch=True, keep_ratio=True)
        if self.slide_image.parent is not None:
            self.slide_image.parent.slide_image_loaded = False
            index = 0
            for child in self.slide_image.parent.children:
                if child == self.slide_image:
                    self.slide_image.parent.children[index] = Widget()
                    self.slide_image.parent.children[index].id = 'image_standin_slide'
                index += 1
            self.slide_image.parent = None
        return self.slide_image

    def get_slide_support_image(self, new_image_instance):
        if new_image_instance:
            return Image(source=self.slide_support_image_source, allow_stretch=True, keep_ratio=True)
        if self.slide_support_image.parent is not None:
            self.slide_support_image.parent.slide_support_image_loaded = False
            index = 0
            for child in self.slide_support_image.parent.children:
                if child == self.slide_support_image:
                    self.slide_support_image.parent.children[index] = Widget()
                    self.slide_support_image.parent.children[index].id = 'image_standin_slide'
                index += 1
            self.slide_support_image.parent = None
        return self.slide_support_image

    def get_preview_image(self, new_image_instance):
        if new_image_instance:
            return Image(source=self.preview_image_source, allow_stretch=True, keep_ratio=True)
        if self.preview_image.parent is not None:
            self.preview_image.parent.preview_image_loaded = False
            index = 0
            for child in self.preview_image.parent.children:
                if child == self.preview_image:
                    self.preview_image.parent.children[index] = Widget()
                    self.preview_image.parent.children[index].id = 'image_standin_preview'
                index += 1
            self.preview_image.parent = None
        return self.preview_image

    def get_select_widget(self):
        if self.select_widget is None:
            raise Exception("Character was not fully loaded!")

        if self.select_widget.parent is not None:
            # self.select_widget.parent.select_widget_loaded = False
            index = 0
            for child in self.select_widget.parent.children:
                if child == self.select_widget:
                    self.select_widget.parent.children[index] = Widget()
                    self.select_widget.parent.children[index].id = 'widget_standin'
                index += 1
            self.select_widget.parent = None
        return self.select_widget

    def get_select_square_widget(self):
        if self.select_square_widget is None:
            raise Exception("Character was not fully loaded!")

        if self.select_square_widget.parent is not None:
            # self.select_widget.parent.select_widget_loaded = False
            index = 0
            for child in self.select_square_widget.parent.children:
                if child == self.select_square_widget:
                    self.select_square_widget.parent.children[index] = Widget()
                    self.select_square_widget.parent.children[index].id = 'widget_standin'
                index += 1
            self.select_square_widget.parent = None
        return self.select_square_widget

    def get_attr_screen(self):
        if self.attr_screen is None:
            raise Exception("Character was not fully loaded!")

        if self.attr_screen.parent is not None:
            index = 0
            for child in self.attr_screen.parent.children:
                if child == self.attr_screen:
                    self.attr_screen.parent.children[index] = Widget()
                    self.attr_screen.parent.children[index].id = 'widget_standin'
                index += 1
            self.attr_screen.parent = None
        return self.attr_screen

    def get_sprite(self):
        return self.sprite

    def get_name(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def get_id(self):
        return self.id

    def get_move(self, movenum):
        return self.moves[movenum]

    def get_phyatk(self, rank=0):
        return self.get_strength(rank) + self.equipment.get_phyatk()

    def get_magatk(self, rank=0):
        return self.get_magic(rank) + self.equipment.get_magatk()

    def get_defense(self, rank=0):
        return self.get_endurance(rank) + self.equipment.get_defense()

    def get_health(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_health()
        health = self.health_base + self.equipment.get_health()
        for rank in self.ranks:
            if rank.unlocked:
                health += rank.get_health()
        return health

    def get_mana(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_mana()
        mana = self.mana_base + self.equipment.get_mana()
        for rank in self.ranks:
            if rank.unlocked:
                mana += rank.get_mana()
        return mana

    def get_strength(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_strength()
        strength = self.strength_base + self.equipment.get_strength()
        for rank in self.ranks:
            if rank.unlocked:
                strength += rank.get_strength()
        return strength

    def get_strength_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_strength(rank), 999)

    def get_magic(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_magic()
        magic = self.magic_base + self.equipment.get_magic()
        for rank in self.ranks:
            if rank.unlocked:
                magic += rank.get_magic()
        return magic

    def get_magic_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_magic(rank), 999)

    def get_endurance(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_endurance()
        endurance = self.endurance_base + self.equipment.get_endurance()
        for rank in self.ranks:
            if rank.unlocked:
                endurance += rank.get_endurance()
        return endurance

    def get_endurance_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_endurance(rank), 999)

    def get_dexterity(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_dexterity()
        dexterity = self.dexterity_base + self.equipment.get_dexterity()
        for rank in self.ranks:
            if rank.unlocked:
                dexterity += rank.get_dexterity()
        return dexterity

    def get_dexterity_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_dexterity(rank), 999)

    def get_agility(self, rank=0):
        if rank > 0:
            return self.get_rank(rank).get_agility()
        agility = self.agility_base + self.equipment.get_agility()
        for rank in self.ranks:
            if rank.unlocked:
                agility += rank.get_agility()
        return agility

    def get_agility_rank(self, rank=0):
        return Scale.get_scale_as_image_path(self.get_agility(rank), 999)

    def get_score(self):
        return self.score


class Rank(WidgetBase):
    ability_max = NumericProperty(999)
    health_max = NumericProperty(999)
    mana_max = NumericProperty(299)

    # Defense is endurance
    # Attack is Strength / Magic / Both

    health = NumericProperty(0)
    mana = NumericProperty(0)

    strength = NumericProperty(0)
    strength_board = NumericProperty(0)
    magic = NumericProperty(0)
    magic_board = NumericProperty(0)
    endurance = NumericProperty(0)
    endurance_board = NumericProperty(0)
    dexterity = NumericProperty(0)
    dexterity_board = NumericProperty(0)
    agility = NumericProperty(0)
    agility_board = NumericProperty(0)

    def __init__(self, rank, grid, unlocked, broken, **kwargs):
        super().__init__(**kwargs)
        self.unlocked = unlocked
        self.broken = broken
        self.rankNum = rank
        self.grid = grid
        self.brkinc = 1.13

        self.grid.count()

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

    def break_rank(self):
        print("Rank breaking")
        self.broken = True


    @staticmethod
    def load_weights(filename, id, ranknums, program_type):
        file = open(filename)
        try:
            grids = Grid.loadgrids("../save/char_load_data/" + program_type + "/grids/" + id + ".txt")
        except FileNotFoundError:
            grids = Grid.loadgrids("../save/char_load_data/" + program_type + "/grids/base.txt")
        ranks = []
        count = 1
        # print("Loading Weights & girds")
        for level in range(0, 10):
            unlocked = True
            broken = True
            ranks.append(Rank(count, grids[count - 1], unlocked, broken))
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


class Equipment(WidgetBase):
    weapon = ObjectProperty(None, allownone=True)
    necklace = ObjectProperty(None, allownone=True)
    bracelet = ObjectProperty(None, allownone=True)
    helmet = ObjectProperty(None, allownone=True)
    vambraces = ObjectProperty(None, allownone=True)
    gloves = ObjectProperty(None, allownone=True)
    chest = ObjectProperty(None, allownone=True)
    leggings = ObjectProperty(None, allownone=True)
    boots = ObjectProperty(None, allownone=True)
    items = ReferenceListProperty(weapon, necklace, bracelet, helmet, vambraces, gloves, chest, leggings, boots)
    types = ListProperty(['weapon', 'necklace', 'bracelet', 'helmet', 'vambraces', 'gloves', 'chest', 'leggings', 'boots'])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_type(self, type):

        return self.items[self.types.index(type)]

    def get_health(self):
        health = 0
        for item in self.items:
            if item is not None:
                health += item.get_health()
        return health

    def get_mana(self):
        mana = 0
        for item in self.items:
            if item is not None:
                mana += item.get_mana()
        return mana

    def get_phyatk(self):
        atk = 0
        for item in self.items:
            if item is not None:
                atk += item.get_phyatk()
        return atk

    def get_magatk(self):
        atk = 0
        for item in self.items:
            if item is not None:
                atk += item.get_magatk()
        return atk

    def get_defense(self):
        defense = 0
        for item in self.items:
            if item is not None:
                defense += item.get_defense()
        return defense

    def get_strength(self):
        strength = 0
        for item in self.items:
            if item is not None:
                strength += item.get_strength()
        return strength

    def get_magic(self):
        magic = 0
        for item in self.items:
            if item is not None:
                magic += item.get_magic()
        return magic

    def get_endurance(self):
        endurance = 0
        for item in self.items:
            if item is not None:
                endurance += item.get_endurance()
        return endurance

    def get_dexterity(self):
        dexterity = 0
        for item in self.items:
            if item is not None:
                dexterity += item.get_dexterity()
        return dexterity

    def get_agility(self):
        agility = 0
        for item in self.items:
            if item is not None:
                agility += item.get_agility()
        return agility


class Equipment_Item:
    def __init__(self, name, id, type, values):
        self.name = name
        self.id = id
        self.type = type
        self.values = values

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_health(self):
        return self.values[0]

    def get_mana(self):
        return self.values[1]

    def get_phyatk(self):
        return self.values[2]

    def get_magatk(self):
        return self.values[3]

    def get_defense(self):
        return self.values[4]

    def get_strength(self):
        return self.values[5]

    def get_magic(self):
        return self.values[6]

    def get_endurance(self):
        return self.values[7]

    def get_dexterity(self):
        return self.values[8]

    def get_agility(self):
        return self.values[9]

    def get_durability(self):
        return self.values[10]

    def get_durability_current(self):
        return self.values[11]



class Grid:
    def __init__(self, grid, weights):
        self.grid = grid
        self.S = 0
        self.M = 0
        self.A = 0
        self.D = 0
        self.E = 0
        self.SW = weights[0]
        self.MW = weights[1]
        self.AW = weights[2]
        self.DW = weights[3]
        self.EW = weights[4]

    def getGrid(self):
        return self.grid

    def count(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == 'S':
                    self.S += 1
                elif self.grid[r][c] == 'A':
                    self.A += 1
                elif self.grid[r][c] == 'D':
                    self.D += 1
                elif self.grid[r][c] == 'E':
                    self.E += 1

    @staticmethod
    def loadgrids(filename):
        file = open(filename)
        grids = []
        for x in file:
            grid = []
            values = x[:-2].split(" ", -1)
            rankNum = int(values[0])
            length = int(values[1])
            strengthw = int(values[2])
            magicw = int(values[3])
            agilityw = int(values[4])
            dexterityw = int(values[5])
            endurancew = int(values[6])
            weights = [strengthw, magicw, agilityw, dexterityw, endurancew]
            values = values[7:]
            rowNum = 0
            for y in range(length):
                row = []
                for x in range(length):
                    row.append( str( values[ rowNum * int( length ) + x ] ) )
                grid.append(list(row))
                rowNum += 1
            grids.append(Grid(grid, weights))
        return grids
    #update grids to be loaded at the same time as characters, and for base weights to be loaded into the first star. Add label updates to the preview screen. finish configuring the rank updates on the rank label
    #add the experience counter, cost function, cost preview, and stat experience window and stats. centralize characterstrength updates into the character class and by rank. with an update function
    #add a testing rank up button and rank break button to test changes
    #implement basic console fighting during delve to test the combar system. on that note. make the combat system.
    #Make sure to load maximum values unto the character load process.


class Move:
    def __init__(self, name, cover, truename, type, power, effects):
        self.name = name
        self.cover = cover
        self.truename = truename
        self.type = type
        if power == "Low":
            self.powerMin = .15
            self.powerMax = .25
        elif power == "Mid":
            self.powerMin = .35
            self.powerMax = .55
        elif power == "High":
            self.powerMin = .75
            self.powerMax = 1.00
        elif power == "Ultra":
            self.powerMin = .95
            self.powerMax = 1.20
        self.powerString = power
        self.effects = effects

    def generateDamage(self, strength, magic):
        if self.type == 0:
            attack = strength
        else:
            attack = magic
        print("Min: " + str(int(attack * self.powerMin)) + "Max: " + str(int(attack * self.powerMax)))
        damage = random.randint(int(attack * self.powerMin), int(attack*self.powerMax))
        return damage

    def getname(self):
        # print(str(self.cover))
        if self.cover:
            return self.truename
        else:
            return self.name
    @staticmethod
    def getmove(moveArray, moveName):
        # print("Finding move " + moveName)
        for x in moveArray:
            # print(str(x.getname()))
            if x.getname() == moveName:
                # print("Found Move")
                return x
        return None

class Attack:
    def __init__(self, name, ttype, type, damage):
        self.name = name
        self.ttype = ttype
        self.type = type
        self.damage = damage
        if self.ttype == 0:
            self.ttypeS = "Foe"
        else:
            self.ttypeS = "Foes"

    def generateDamage(self, power):
        percent = random.randint(0, 19) + 1
        damage = percent / 14.0 * (power * ((self.damage+1.0)/3.4))
        if self.ttype == 1:
            damage * 0.8
        return damage

    def findfoe(self, numoffoes):
        return random.randint(0, numoffoes)
    #attack Name
    #attack targeting type
    #attack type 0 - foe 1 - foes
    #attack damage 0 - Low 1 - Mid 2 - High 3 - Ultra 0-4,5-9,10-14,15-20

    #attack elemental type
    #attack special effects
    #makeattack(power, type, effects) returns damage