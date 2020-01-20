from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from src.modules.HTButton import HTButton


class Sortable(object):
    previews_sort = ListProperty(None)
    values_sort = ListProperty(None)
    ascending = BooleanProperty(True)
    sort_type = StringProperty('Strength')
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
        index = 0
        for preview in self.previews_sort:
            value = 0
            if self.sort_type =='Strength':
                value += preview.char.get_strength()
            elif self.sort_type == 'Magic':
                value += preview.char.get_magic()
            elif self.sort_type == 'Endurance':
                value += preview.char.get_endurance()
            elif self.sort_type == 'Dexterity':
                value += preview.char.get_dexterity()
            elif self.sort_type == 'Agility':
                value += preview.char.get_agility()
            elif self.sort_type == 'Health':
                value += preview.char.get_health()
            elif self.sort_type == 'Mana':
                value += preview.char.get_mana()
            elif self.sort_type == 'Phy. Atk':
                value += preview.char.get_phyatk()
            elif self.sort_type == 'Mag. Atk':
                value += preview.char.get_magatk()
            elif self.sort_type == 'Defense':
                value += preview.char.get_defense()
            elif self.sort_type == 'Party':
                value += preview.char.get_index() #Placeholder
            elif self.sort_type == 'Rank':
                value += preview.char.get_current_rank()
            elif self.sort_type == 'Name':
                value = preview.char.get_name()
            elif self.sort_type == 'Score':
                value += preview.char.get_score()
            elif self.sort_type == 'Worth':
                value += preview.char.get_worth()
            self.values_sort[index] = value
            index += 1
        self.no_sort = False
        self.sort()

    def force_update_values(self):
        self.no_sort = True
        values = []
        for preview in self.previews_sort:
            if self.sort_type == 'Strength':
                value = preview.char.get_strength()
            elif self.sort_type == 'Magic':
                value = preview.char.get_magic()
            elif self.sort_type == 'Endurance':
                value = preview.char.get_endurance()
            elif self.sort_type == 'Dexterity':
                value = preview.char.get_dexterity()
            elif self.sort_type == 'Agility':
                value = preview.char.get_agility()
            elif self.sort_type == 'Health':
                value = preview.char.get_health()
            elif self.sort_type == 'Mana':
                value = preview.char.get_mana()
            elif self.sort_type == 'Phy. Atk':
                value = preview.char.get_phyatk()
            elif self.sort_type == 'Mag. Atk':
                value = preview.char.get_magatk()
            elif self.sort_type == 'Defense':
                value = preview.char.get_defense()
            elif self.sort_type == 'Party':
                value = preview.char.get_index()  # Placeholder
            elif self.sort_type == 'Rank':
                value = preview.char.get_current_rank()
            elif self.sort_type == 'Name':
                value = preview.char.get_name()
            elif self.sort_type == 'Score':
                value = preview.char.get_score()
            elif self.sort_type == 'Worth':
                value = preview.char.get_worth()
            else:
                value = None
            values.append(value)
        self.values_sort = values
        self.no_sort = False
        self.sort()

    def on_after_sort(self):
        pass


class SortWidget(Widget):
    initialized = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size = (0, 0)

        self.shadow = Image(source='../res/screens/backgrounds/shadow.png', allow_stretch=True)
        self.shadow.bind(on_touch_down=self.toss)
        self.background = Image(source="../res/screens/stats/sort_background.png", allow_stretch=True)

        self.title = Label(text="Sort", font_name="../res/fnt/Precious.ttf", color=(0, 0, 0, 1), size_hint=(None, None))

        self.overlay_bar1 = Image(source="../res/screens/stats/overlay_bar.png", size_hint=(None, None), allow_stretch=True)
        self.overlay_bar2 = Image(source="../res/screens/stats/overlay_bar.png", size_hint=(None, None), allow_stretch=True)

        self.layout = GridLayout(cols=3, rows=5)
        self.layout2 = GridLayout(cols=2, rows=1)

        self.ascending = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Ascending")
        self.descending = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Descending")
        self.strength = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Strength")
        self.magic = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Magic")
        self.endurance = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Endurance")
        self.dexterity = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Dexterity")
        self.agility = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Agility")
        self.health = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Health")
        self.mana = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Mana")
        self.phyatk = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Phy. Atk")
        self.magatk = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Mag. Atk")
        self.defense = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Defense")
        self.party = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Party")
        self.rank = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Rank")
        self.name = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Name")
        self.score = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Score")
        self.worth = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_stat", text="Worth")

        self.add_widget(self.shadow)
        self.add_widget(self.background)
        self.add_widget(self.title)
        self.add_widget(self.overlay_bar1)
        self.add_widget(self.layout2)
        self.layout2.add_widget(self.ascending)
        self.layout2.add_widget(self.descending)
        self.add_widget(self.overlay_bar2)
        self.add_widget(self.layout)
        self.layout.add_widget(self.strength)
        self.layout.add_widget(self.magic)
        self.layout.add_widget(self.endurance)
        self.layout.add_widget(self.dexterity)
        self.layout.add_widget(self.agility)
        self.layout.add_widget(self.health)
        self.layout.add_widget(self.mana)
        self.layout.add_widget(self.phyatk)
        self.layout.add_widget(self.magatk)
        self.layout.add_widget(self.defense)
        self.layout.add_widget(self.party)
        self.layout.add_widget(self.rank)
        self.layout.add_widget(self.name)
        self.layout.add_widget(self.score)
        self.layout.add_widget(self.worth)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        width, height = self.height * 0.9 * 750 / 600, self.height * 0.9
        x, y = (self.width - width) / 2, (self.height - height) / 2

        self.shadow.size = self.size
        self.background.size = width, height
        self.background.pos = x, y

        self.title.font_size = self.height * .125
        self.title.texture_update()
        self.title.size = self.title.texture_size
        self.title.pos = (x + (width - self.title.width) / 2, y + height - self.title.height * 1.125)

        button_size = height * 0.15 * 570 / 215, height * 0.15
        gap = (width * 0.9 - button_size[0] * 3) / 4, (height * 0.55 - button_size[1] * 5) / 6
        gap2 = (width * 0.9 - button_size[0] * 2) / 3, (height * 0.175 - button_size[1]) / 2

        self.overlay_bar1.size = width * 0.8, width * 0.8 * 20 / 620
        self.overlay_bar1.pos = x + width * 0.1, self.title.y - width * 0.8 * 20 / 620
        self.overlay_bar2.size = width * 0.8, width * 0.8 * 20 / 620
        self.overlay_bar2.pos = x + width * 0.1, y + height * 0.625

        self.layout.padding = gap
        self.layout.spacing = gap
        self.layout.size = width * 0.9, height * 0.55
        self.layout.pos = x + width * 0.05, y + height * 0.05

        self.layout2.padding = gap2
        self.layout2.spacing = gap2
        self.layout2.size = width * 0.9, self.overlay_bar1.y - self.overlay_bar2.y - self.overlay_bar2.height
        self.layout2.pos = x + width * 0.05, self.overlay_bar2.y + self.overlay_bar2.height * 2

        self.ascending.size = button_size
        self.ascending.font_size = button_size[1] * 0.5
        self.descending.size = button_size
        self.descending.font_size = button_size[1] * 0.5
        self.strength.size = button_size
        self.strength.font_size = button_size[1] * 0.5
        self.magic.size = button_size
        self.magic.font_size = button_size[1] * 0.5
        self.endurance.size = button_size
        self.endurance.font_size = button_size[1] * 0.5
        self.dexterity.size = button_size
        self.dexterity.font_size = button_size[1] * 0.5
        self.agility.size = button_size
        self.agility.font_size = button_size[1] * 0.5
        self.health.size = button_size
        self.health.font_size = button_size[1] * 0.5
        self.mana.size = button_size
        self.mana.font_size = button_size[1] * 0.5
        self.phyatk.size = button_size
        self.phyatk.font_size = button_size[1] * 0.5
        self.magatk.size = button_size
        self.magatk.font_size = button_size[1] * 0.5
        self.defense.size = button_size
        self.defense.font_size = button_size[1] * 0.5
        self.party.size = button_size
        self.party.font_size = button_size[1] * 0.5
        self.rank.size = button_size
        self.rank.font_size = button_size[1] * 0.5
        self.name.size = button_size
        self.name.font_size = button_size[1] * 0.5
        self.score.size = button_size
        self.score.font_size = button_size[1] * 0.5
        self.worth.size = button_size
        self.worth.font_size = button_size[1] * 0.5

    def toss(self, *args):
        return True