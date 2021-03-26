from loading.base import CALoader, CURRENT_INDEX, LOADING_SECTIONS, STARTING_CURRENT_INDEX, STARTING_TOTAL_INDEX


class TextCALoader(CALoader):
    def load_base_values(self):
        self.max_values.append(len(LOADING_SECTIONS))
        self.curr_values.append(STARTING_TOTAL_INDEX)
        for index in range(len(LOADING_SECTIONS)):
            self.messages.append(f'Loading {LOADING_SECTIONS[index]}')
            self.curr_values.append(STARTING_CURRENT_INDEX)
            self.max_values.append(1)

    def show_bars(self):
        pass

    def update_outer(self):
        if self.curr_values[CURRENT_INDEX] == self.max_values[CURRENT_INDEX] + 1:
            self._console.update_calendar_callback()
        self._console.set_loading_progress('outer', 'Loading Data', self.curr_values[CURRENT_INDEX], self.max_values[CURRENT_INDEX])
        self.update_inner()

    def update_inner(self):
        if self.curr_values[CURRENT_INDEX] <= self.max_values[CURRENT_INDEX]:
            self._console.set_loading_progress('inner', self.messages[self.curr_values[CURRENT_INDEX] - STARTING_TOTAL_INDEX], self.curr_values[self.curr_values[CURRENT_INDEX]], self.max_values[self.curr_values[CURRENT_INDEX]])

    def load_game(self, console, save_slot):
        self._console = console
        super().load_game(save_slot)
