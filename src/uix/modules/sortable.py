# Project Imports
# Kivy Imports
from kivy.properties import BooleanProperty, ListProperty, OptionProperty

from refs import Refs


class Sortable(object):
    previews_sort = ListProperty(None)
    values_sort = ListProperty([])
    ascending = BooleanProperty(True)
    sort_type = OptionProperty('Strength', options=['Strength', 'Magic', 'Endurance', 'Dexterity', 'Agility',
                                           'Phy. Atk', 'Mag. Atk', 'Defense', 'Health', 'Mana',
                                           'Party', 'Rank', 'Name', 'Score', 'Worth'])
    no_sort = BooleanProperty(False)

    # Sorting Types:
    # strength, magic, endurance
    # dexterity, agility, health
    # mana, phyatk, magatk
    # defense, Party, Rank
    # Name, Score, Worth
    def __init__(self, **kwargs):
        self.register_event_type('on_after_sort')
        super().__init__(**kwargs)
        self._ascending = None
        self._sort_type = None

    def sort(self):
        self.no_sort = True
        self._previews_sort = self.previews_sort
        self.quick_sort(0, len(self.values_sort) - 1)
        self.no_sort = False
        self.dispatch('on_after_sort')

    def quick_sort(self, start, end):
        if start < end:
            index = self.partition(start, end)

            self.quick_sort(start, index - 1)
            self.quick_sort(index + 1, end)

    def partition(self, start, end):
        i = start - 1  # index of element to move
        pivot = self.values_sort[end]  # pivot

        for j in range(start, end):  # Check against elements

            # If current element obeys order change
            if self.values_sort[j] <= pivot and not self.ascending or self.values_sort[j] >= pivot and self.ascending:
                # increment index of element
                i = i + 1
                self.values_sort[i], self.values_sort[j] = self.values_sort[j], self.values_sort[i]
                self.previews_sort[i], self.previews_sort[j] = self.previews_sort[j], self.previews_sort[i]
        self.values_sort[i + 1], self.values_sort[end] = self.values_sort[end], self.values_sort[i + 1]
        self.previews_sort[i + 1], self.previews_sort[end] = self.previews_sort[end], self.previews_sort[i + 1]
        return i + 1

    def on_ascending(self, instance, ascending):
        if self.ascending == self._ascending:
            return
        self._ascending = ascending
        self.sort()

    def on_previews(self, instance, preview):
        if self.no_sort or len(self.previews_sort) != len(self.values_sort):
            return
        self.sort()

    def on_values(self, instance, values):
        if self.no_sort or len(self.previews_sort) != len(self.values_sort):
            return
        self.sort()

    def on_sort_type(self, instance, sort_type):
        if sort_type == self._sort_type:
            return
        self._sort_type = sort_type

        # Change Value Array
        self.no_sort = True
        self.values_sort = self.get_values()
        self.no_sort = False
        self.sort()

    def force_update_values(self):
        self.no_sort = True
        self.values_sort = self.get_values()
        self.no_sort = False
        self.sort()

    def get_values(self):
        values = []
        for preview in self.previews_sort:
            if self.sort_type == 'Strength':
                value = preview['character'].get_strength()
            elif self.sort_type == 'Magic':
                value = preview['character'].get_magic()
            elif self.sort_type == 'Endurance':
                value = preview['character'].get_endurance()
            elif self.sort_type == 'Dexterity':
                value = preview['character'].get_dexterity()
            elif self.sort_type == 'Agility':
                value = preview['character'].get_agility()
            elif self.sort_type == 'Health':
                value = preview['character'].get_health()
            elif self.sort_type == 'Mana':
                value = preview['character'].get_mana()
            elif self.sort_type == 'Phy. Atk':
                value = preview['character'].get_physical_attack()
            elif self.sort_type == 'Mag. Atk':
                value = preview['character'].get_magical_attack()
            elif self.sort_type == 'Defense':
                value = preview['character'].get_defense()
            elif self.sort_type == 'Party':
                value = Refs.gc.get_party_index(preview['character'])
            elif self.sort_type == 'Rank':
                value = preview['character'].get_current_rank()
            elif self.sort_type == 'Name':
                value = preview['character'].get_name()
            elif self.sort_type == 'Score':
                value = preview['character'].get_score()
            elif self.sort_type == 'Worth':
                value = preview['character'].get_worth()
            else:
                value = None
            values.append(value)
        return values

    def on_after_sort(self):
        pass
