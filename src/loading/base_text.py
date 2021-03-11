from kivy.resources import resource_find
from loading.base import CALoader, CURRENT_INDEX, STARTING_CURRENT_INDEX, STARTING_TOTAL_INDEX


class TextCALoader(CALoader):
    def load_base_values(self):
        file = open(resource_find('data/loading_' + self.program_type + '.txt'), "r")
        index = 0
        for x in file:
            if index == 0:
                opt = x[:-1].split(',')
                self.max_values.append(int(opt[CURRENT_INDEX]))
                self.curr_values.append(STARTING_TOTAL_INDEX)
                for y in range(STARTING_TOTAL_INDEX, int(opt[CURRENT_INDEX]) + STARTING_TOTAL_INDEX):
                    self.messages.append(opt[y])
            else:
                if x.startswith('#'):
                    break
                self.max_values.append(int(x))
                self.curr_values.append(STARTING_CURRENT_INDEX)
            index += 1

    def show_bars(self):
        pass

    def update_outer(self):
        self._console.set_loading_progress('outer', 'Loading Data', self.curr_values[CURRENT_INDEX], self.max_values[CURRENT_INDEX])
        self.update_inner()

    def update_inner(self):
        if self.curr_values[CURRENT_INDEX] <= self.max_values[CURRENT_INDEX]:
            self._console.set_loading_progress('inner', self.messages[self.curr_values[CURRENT_INDEX] - STARTING_TOTAL_INDEX], self.curr_values[self.curr_values[CURRENT_INDEX]], self.max_values[self.curr_values[CURRENT_INDEX]])

    def load_game(self, console, save_slot):
        self._console = console
        super().load_game(save_slot)
