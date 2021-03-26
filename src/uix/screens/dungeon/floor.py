from kivy.uix.screenmanager import FadeTransition
# KV Import
from loading.kv_loader import load_kv
from refs import Refs
from uix.screens.dungeon.battle import DungeonBattle

load_kv(__name__)


class DungeonFloor:
    def __init__(self, floorNum, direction):
        self.floor = Refs.gc.get_floors()[floorNum - 1]
        Refs.gs.transition = FadeTransition(duration=.4)
        self.encounterNumber = self.floor.generateEncounterNumber()
        self.runNumber = 1
        self.direction = direction
        print("Generated a floor run instance")
        print("\tWill run for %d encounters." % self.encounterNumber)

    def run(self):
        # print("DungeonFloor Run")
        if (self.runNumber <= self.encounterNumber):
            screen = DungeonBattle(self.runNumber == self.encounterNumber, self.runNumber, self.floor, self, name='battleScreen%d' % self.runNumber)
            if self.runNumber > 0:
                self.screenManager.goto_next_and_remove(screen)
            else:
                self.screenManager.goto_next(screen)
            screen.run()
            self.runNumber += 1
        else:
            if self.direction:
                num = self.floor.floornum + 1
            else:
                num = self.floor.floornum - 1
            self.screenManager.current = 'dungeon_main'
            self.dungeonScreen.level = num
            self.dungeonScreen.update_buttons()
            print("return to delve screen. Floor: " + str(num))
