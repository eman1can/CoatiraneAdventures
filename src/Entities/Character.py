import random

class Character:
    def __init__(self, index, name, displayname, id, rank, health, defense, physicalattack, magicalattack, magicalpoints, strength, magic, endurance, dexterity, agility, slideimage, previewimage, fullimage, moves):
        super().__init__()
        self.name = name
        self.first = False
        self.index = index
        self.image = slideimage
        self.displayname = displayname
        self.previewimage = previewimage
        self.fullimage = fullimage
        self.sprite = None
        self.hasAttributeScreen = False
        self.id = id
        self.moves = moves
        # print(str(self.moves))
        self.currentRank = 1

        self.exphealthtotal = 0
        self.expmptotal = 0
        self.expdeftotal = 0
        self.expstrtotal = 0
        self.expmagtotal = 0
        self.expagitotal = 0
        self.expdextotal = 0
        self.expendtotal = 0

        try:
            self.ranks = Rank.loadWeights('chars/ranks/' + id + '.txt', id, rank, [health, magicalpoints, defense, strength, magic, agility, dexterity, endurance])
        except FileNotFoundError:
            self.ranks = Rank.loadWeights('chars/ranks/base.txt', id, rank, [health, magicalpoints, defense, strength, magic, agility, dexterity, endurance])
        caps = self.ranks.pop()
        self.totalCaps = []
        for x in caps:
            self.totalCaps.append(float(x))
        self.updateCharValues()
            # self.ranks = Grid.loadgrids('grids/base.txt', rank)
        # for x in range(len(rank)):
        #     if not rank[x] == 0:
        #         self.ranks.append(Rank(x, ))
    def printstats(self):
        pass
        # print("Total Health: " + str(self.totalHealth))
        # print("Total MP: " + str(self.totalMP))
        # print("Total Defense: " + str(self.totalDefense))
        # print("Total Strength: " + str(self.totalStrength))
        # print("Total Magic: " + str(self.totalMagic))
        # print("Total Agiliity: " + str(self.totalAgility))
        # print("Total Dexterity: " + str(self.totalDexterity))
        # print("Total Endurance: " + str(self.totalEndurance))
        # print("Rank Health: " + str(self.ranks[self.currentRank-1].rankhealth))
        # print("Rank MP: " + str(self.ranks[self.currentRank - 1].rankmagicalpoints))
        # print("Rank Defense: " + str(self.ranks[self.currentRank - 1].rankdefense))
        # print("Rank Strength: " + str(self.ranks[self.currentRank - 1].rankstrength))
        # print("Rank Magic: " + str(self.ranks[self.currentRank - 1].rankmagic))
        # print("Rank Agility: " + str(self.ranks[self.currentRank - 1].rankagility))
        # print("Rank Dexterity: " + str(self.ranks[self.currentRank - 1].rankdexterity))
        # print("Rank Endurance: " + str(self.ranks[self.currentRank-1].rankendurance))


    def updateCharValues(self):
        self.totalPhysicalAttack = 0
        self.totalMagicalAttack = 0
        self.totalDefense = 0
        self.totalHealth = 0
        self.totalMP = 0
        self.totalStrength = 0
        self.totalMagic = 0
        self.totalAgility = 0
        self.totalDexterity = 0
        self.totalEndurance = 0

        self.exphealthtotal = 0
        self.expmptotal = 0
        self.expdeftotal = 0
        self.expstrtotal = 0
        self.expmagtotal = 0
        self.expagitotal = 0
        self.expdextotal = 0
        self.expendtotal = 0

        for x in self.ranks:
            values = x.getRankStats()
            self.totalHealth += values[0]
            self.totalMP += values[1]
            self.totalDefense += values[2]
            self.totalPhysicalAttack += values[3]
            self.totalMagicalAttack += values[4]
            self.totalStrength += values[3]
            self.totalMagic += values[4]
            self.totalAgility += values[5]
            self.totalDexterity += values[6]
            self.totalEndurance += values[7]

            self.totalHealth += values[8]
            self.totalMP += values[9]
            self.totalDefense += values[10]
            self.totalPhysicalAttack += values[11]
            self.totalMagicalAttack += values[12]
            self.totalStrength += values[11]
            self.totalMagic += values[12]
            self.totalAgility += values[13]
            self.totalDexterity += values[14]
            self.totalEndurance += values[15]

            self.exphealthtotal += values[8]
            self.expmptotal += values[9]
            self.expdeftotal += values[10]
            self.expstrtotal += values[11]
            self.expmagtotal += values[12]
            self.expagitotal += values[13]
            self.expdextotal += values[14]
            self.expendtotal += values[15]
        '''
        Attribute Scales. Used for scoring:
        S: 1-4500
        A: 1-3200
        D: 1-3200
        E: 1-3200
        Character Attributes
        Base Attributes: Hp 33 Mp 13 S 1.75 A 5.5 D 4.4 E 4.6
        Rank 1-10
        Rank Breaking will add a 10% multiplier to the scores for that rank, but in attribute skill and slot scores
        Level Attribute Caps: (Difference between rank / amount of attribute slots is added at each slot release for that rank)
        1:  Hp 102  Mp 19  S 7      A 19    D 14.6  E 15.4
        2:  Hp 228  Mp 29  S 21.25  A 41.5  D 31.6  E 33.4
        3:  Hp 438  Mp 43  S 49     A 73    D 55.4  E 58.6
        4:  Hp 732  Mp 61  S 94.75  A 113.5 D 86    E 91
        5:  Hp 1110 Mp 83  S 163    A 163   D 123.4 E 130.6
        6:  Hp 1572 Mp 109 S 238.25 A 221.5 D 167.6 E 177.4
        7:  Hp 2118 Mp 139 S 385    A 289   D 218.6 E 231.4
        8:  Hp 2748 Mp 173 S 547.75 A 365.5 D 276.4 E 292.6
        9:  Hp 3462 Mp 211 S 751    A 451   D 341   E 361
        10: Hp 4260 Mp 253 S 999.25 A 545.5 D 412.4 E 436.6
        
        Level Attribute Slots: (Amount, Weight, Total_Points): (Unlocks Attribute Caps & Adds base amount to character. Requres Gems & experience to unlock)
        1: S 3 A 2 D 2 E 2
           S 3 A 3 D 2 E 2
           S 9 A 6 D 4 E 4
        2: S 5 A 4 D 3 E 4
           S 9 A 8 D 5 E 7
           S 45 A 32 D 4 E 4
        3:
        4:
        5:
        6:
        7:
        8:
        9:
        10:
        
        
        
        '''

    def getindex(self):
        return self.index

    def getRank(self, rankNum):
        return self.ranks[rankNum - 1]

    def generateSpeed(self):
        return random.randint(int(self.totalAgility*.85*21), int(self.totalAgility*21))

    def rankup(self):
        if self.currentRank < 10:
            self.currentRank += 1
            self.ranks[self.currentRank-1].unlocked = True
        else:
            raise Exception("Character at max rank")

    def rankbreak(self):
        if not self.ranks[self.currentRank-1].broken:
            self.ranks[self.currentRank-1].breakRank()
        else:
            raise Exception("Character already rank broken")

    def getcharacter(self):
        return self.name

    def getfullimage(self):
        return self.fullimage

    def getsprite(self):
        return self.sprite

    def getname(self):
        return self.name

    def getdisplayname(self):
        return self.displayname

    def getimage(self):
        return self.image

    def getpreviewimage(self):
        return self.previewimage

    def getfullimage(self):
        return self.fullimage

    def getid(self):
        return self.id

    def getmove(self, movenum):
        return self.moves[movenum]

    def equals(self, char):
        if (self.getid() == char.getid()):
            return True
        else:
            return False

class Rank:
    def __init__(self, rank, grid, unlocked, broken, rankstats, maxs):
        self.strengthMax = float(maxs[0])
        self.magicMax = float(maxs[1])
        self.agilityMax = float(maxs[2])
        self.dexterityMax = float(maxs[3])
        self.enduranceMax = float(maxs[4])
        self.expHpCap = float(maxs[9])
        self.expMpCap = float(maxs[10])
        self.expDefCap = float(maxs[11])
        self.expStrCap = float(maxs[5])
        # self.expMagCap = maxs[11]
        self.expAgiCap = float(maxs[6])
        self.expDexCap = float(maxs[7])
        self.expEndCap = float(maxs[8])
        self.broken = False

        self.rankhealth = 0
        self.rankmagicalpoints = 0
        self.rankdefense = 0
        self.rankstrength = 0
        self.rankmagic = 0
        self.rankagility = 0
        self.rankdexterity = 0
        self.rankendurance = 0

        self.exphealth = 0
        self.expmagicalpoints = 0
        self.expdefense = 0
        self.expstrength = 0
        self.expmagic = 0
        self.expagility = 0
        self.expdexterity = 0
        self.expendurance = 0

        self.exphealthraw = 0
        self.expmagicalpointsraw = 0
        self.expdefenseraw = 0
        self.expstrengthraw = 0
        self.expmagicraw = 0
        self.expagilityraw = 0
        self.expdexterityraw = 0
        self.expenduranceraw = 0


        self.rankhealthraw = float(rankstats[0])
        self.rankmagicalpointsraw = float(rankstats[1])
        self.rankdefenseraw = float(rankstats[2])
        self.rankstrengthraw = float(rankstats[3])
        self.rankmagicraw = float(rankstats[4])
        self.rankagilityraw = float(rankstats[5])
        self.rankdexterityraw = float(rankstats[6])
        self.rankenduranceraw = float(rankstats[7])

        self.rankhealthtotal = 0
        self.rankmagicalpointstotal = 0
        self.rankdefensetotal = 0
        self.rankstrengthtotal = 0
        self.rankmagictotal = 0
        self.rankagilitytotal = 0
        self.rankdexteritytotal = 0
        self.rankendurancetotal = 0

        self.calcvalues()
        self.unlocked = unlocked
        self.broken = broken
        self.brkinc = 1.13
        self.rankNum = rank
        self.grid = grid
        self.grid.count()

    def updateValues(self, hp, mp, defen, str, mag, agi, dex, end):
        self.rankhealthraw += hp
        self.rankmagicalpointsraw += mp
        self.rankdefenseraw += defen
        self.rankstrengthraw += str
        self.rankmagicraw += mag
        self.rankagilityraw += agi
        self.rankdexterityraw += dex
        self.rankenduranceraw += end
        self.calcvalues()

    def updateexpValues(self, hp, mp, defen, str, mag, agi, dex, end):
        self.exphealthraw += hp
        self.expmagicalpointsraw += mp
        self.expdefenseraw += defen
        self.expstrengthraw += str
        self.expmagicraw += mag
        self.expagilityraw += agi
        self.expdexterityraw += dex
        self.expenduranceraw += end
        self.calcexpvalues()

    def calcvalues(self):
        if self.broken:
            mul = self.brkinc
        else:
            mul = 1
        self.rankhealth = self.rankhealthraw * mul
        self.rankmagicalpoints = self.rankmagicalpointsraw * mul
        self.rankdefense = self.rankdefenseraw * mul
        self.rankstrength = self.rankstrengthraw * mul
        self.rankmagic = self.rankmagicraw * mul
        self.rankagility = self.rankagilityraw * mul
        self.rankdexterity = self.rankdexterityraw * mul
        self.rankendurance = self.rankenduranceraw * mul
        self.calctotalvalues()
    def calcexpvalues(self):
        if self.broken:
            mul = self.brkinc
        else:
            mul = 1
        self.exphealth = self.exphealthraw * mul
        self.expmagicalpoints = self.expmagicalpointsraw * mul
        self.expdefense = self.expdefenseraw * mul
        self.expstrength = self.expstrengthraw * mul
        self.expmagic = self.expmagicraw * mul
        self.expagility = self.expagilityraw * mul
        self.expdexterity = self.expdexterityraw * mul
        self.expendurance = self.expenduranceraw * mul
        self.calctotalvalues()
    def calctotalvalues(self):
        self.rankhealthtotal = self.exphealth + self.rankhealth
        self.rankmagicalpointstotal = self.expmagicalpoints + self.rankmagicalpoints
        self.rankdefensetotal = self.expdefense + self.rankdefense
        self.rankstrengthtotal = self.expstrength + self.rankstrength
        self.rankmagictotal = self.expmagic + self.rankmagic
        self.rankagilitytotal = self.expagility + self.rankagility
        self.rankdexteritytotal = self.expdexterity + self.rankdexterity
        self.rankendurancetotal = self.expendurance + self.rankendurance
    # def setWeights(self, SW, AW, DW, EW):
    #     self.grid.SW = SW
    #     self.grid.AW = AW
    #     self.grid.DW = DW
    #     self.grid.EW = EW
    #     self.calculate()

    def getRankStats(self):
        self.calcvalues()
        return [self.rankhealth, self.rankmagicalpoints, self.rankdefense, self.rankstrength, self.rankmagic,
                self.rankagility, self.rankdexterity, self.rankendurance, self.exphealth, self.expmagicalpoints,
                self.expdefense, self.expstrength, self.expmagic, self.expagility, self.expdexterity, self.expendurance]

    def breakRank(self):
        print("Rank breaking")
        self.broken = True
        self.calcvalues()
        self.calcexpvalues()


    @staticmethod
    def loadWeights(filename, id, ranknums, basevalues):
        file = open(filename)
        try:
            grids = Grid.loadgrids('chars/grids/' + id + '.txt')
        except FileNotFoundError:
            grids = Grid.loadgrids('chars/grids/base.txt')
        ranks = []
        count = 1
        print("Loading Weights & girds")
        for x in file:
            values = x[:-1].split(' ', -1)
            print("Loaded: " + str(values))
            if not count == 11:
                if ranknums[count-1] == 1:
                    unlocked = True
                    broken = False
                elif ranknums[count-1] == 2:
                    unlocked = True
                    broken = True
                else:
                    unlocked = False
                    broken = False
                if count == 1:
                    actvalues = basevalues
                else:
                    actvalues = [0, 0, 0, 0, 0, 0, 0, 0]
                rank = Rank(count, grids[count-1], unlocked, broken, actvalues, values)
                count+=1
                ranks.append(rank)
            else:
                ranks.append(values)
        return ranks



    # def calculate(self):
    #     self.S = self.grid.S * self.grid.SW
    #     self.A = self.grid.A * self.grid.AW
    #     self.D = self.grid.D * self.grid.DW
    #     self.E = self.grid.E * self.grid.EW
    #     self.SBrk = int(self.S * self.brkinc)
    #     self.ABrk = int(self.A * self.brkinc)
    #     self.DBrk = int(self.D * self.brkinc)
    #     self.EBrk = int(self.E * self.brkinc)
    #
    # def getStats(self):
    #     return [self.S, self.A, self.D, self.E, self.SBrk, self.ABrk, self.DBrk, self.EBrk]

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

class Scale:
    threshSSS = 1.30
    threshSS = 1.10
    threshS = 0.95
    threshA = 0.85
    threshB = 0.77
    threshC = 0.66
    threshD = 0.55
    threshE = 0.44
    @staticmethod
    def getScale(value, max):
        val = value/max
        if val > Scale.threshSSS:
            return "SSS"
        elif val > Scale.threshSS:
            return "SS"
        elif val > Scale.threshS:
            return "S"
        elif val > Scale.threshA:
            return "A"
        elif val > Scale.threshB:
            return "B"
        elif val > Scale.threshC:
            return "C"
        elif val > Scale.threshD:
            return "D"
        elif val > Scale.threshE:
            return "E"
        else:
            return "F"

    @staticmethod
    def getScale_as_number(value, max):
        val = value / max
        if val > Scale.threshSSS:
            return 1.3
        elif val > Scale.threshSS:
            return 1.1
        elif val > Scale.threshS:
            return 1
        elif val > Scale.threshA:
            return 1
        elif val > Scale.threshB:
            return .8
        elif val > Scale.threshC:
            return .6
        elif val > Scale.threshD:
            return .4
        elif val > Scale.threshE:
            return .2
        else:
            return 0


    @staticmethod
    def getScaleAsImagePath(value, max):
        val = value / max
        # print(str(value) + " " + str(max) + " " + str(val))
        # print(str(Scale.threshA) + str(val > Scale.threshA))
        if val > Scale.threshSSS:
            # print("return scale SSS")
            return 'res/GradeSSS.png'
        elif val > Scale.threshSS:
            # print("return scale SS")
            return 'res/GradeSS.png'
        elif val > Scale.threshS:
            # print("return scale S")
            return 'res/GradeS.png'
        elif val > Scale.threshA:
            # print("return scale A")
            return 'res/GradeA.png'
        elif val > Scale.threshB:
            # print("return scale B")
            return 'res/GradeD.png'
        elif val > Scale.threshC:
            # print("return scale C")
            return 'res/GradeC.png'
        elif val > Scale.threshD:
            # print("return scale D")
            return 'res/GradeD.png'
        elif val > Scale.threshE:
            # print("return scale E")
            return 'res/GradeE.png'
        else:
            # print("return scale F")
            return 'res/GradeF.png'

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