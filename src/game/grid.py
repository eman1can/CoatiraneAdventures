class Grid:
    def __init__(self, index, grid, unlocked, amounts):
        self.index = index
        self._grid = grid
        self._unlocked = unlocked
        self.amounts = amounts

    def get_grid(self):
        return self.grid, self.unlocked

    def unlock(self, index):
        if self.unlocked[index] == 1:
            pass
        else:
            self.unlocked[index] = 1

    @staticmethod
    def load_grids(filename):
        file = open(filename)
        grids = []
        for x in file:
            grid = []
            ugrid = []
            values = x[:-1].split(" ", -1)
            rank_num = int(values[0])
            length = int(values[1])
            strength = int(values[2])
            magic = int(values[3])
            agility = int(values[4])
            dexterity = int(values[5])
            endurance = int(values[6])
            amounts = [strength, magic, agility, dexterity, endurance]
            values = values[7:]
            row_index = 0
            for y in range(length):
                row = []
                urow = []
                for x in range(length):
                    row.append(str(values[row_index * int(length) + x]))
                    urow.append(0)
                grid.append(list(row))
                ugrid.append(urow)
                row_index += 1
            grids.append(Grid(rank_num, grid, ugrid, amounts))
        return grids
    #update grids to be loaded at the same time as characters, and for base weights to be loaded into the first star. Add label updates to the preview screen. finish configuring the rank updates on the rank label
    #add the experience counter, cost function, cost preview, and stat experience window and stats. centralize characterstrength updates into the character class and by rank. with an update function
    #add a testing rank up button and rank break button to test changes
    #implement basic console fighting during delve to test the combar system. on that note. make the combat system.
    #Make sure to load maximum values unto the character load process.