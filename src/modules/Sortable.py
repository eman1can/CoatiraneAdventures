from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.graphics import Color, Rectangle
from src.modules.HTButton import HTButton

class Sortable(object):
    previews = ListProperty(None)
    values = ListProperty(None)
    ascending = BooleanProperty(False) # Highest to smallest on False aka descending
    sort_type = StringProperty('Strength')
    no_sort = BooleanProperty(False)

    # sORTING tYPES:
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
        self.quick_sort(0, len(self.values) - 1)
        self.no_sort = False
        self.dispatch('on_after_sort')

    def quick_sort(self, start, end):
        if start < end:
            index = self.partition(start, end)

            self.quick_sort(start, index - 1)
            self.quick_sort(index + 1, end)

    def partition(self, start, end):
        i = start - 1  # index of element to move
        pivot = self.values[end]  # pivot

        for j in range(start, end):  # Check against elements

            # If current element obeys order change
            if self.values[j] <= pivot and not self.ascending or self.values[j] >= pivot and self.ascending:
                # increment index of element
                i = i + 1
                self.values[i], self.values[j] = self.values[j], self.values[i]
                self.previews[i], self.previews[j] = self.previews[j], self.previews[i]
        self.values[i + 1], self.values[end] = self.values[end], self.values[i + 1]
        self.previews[i + 1], self.previews[end] = self.previews[end], self.previews[i + 1]
        return i + 1

    def on_ascending(self, instance, ascending):
        if self.ascending == self._ascending:
            return
        self._ascending = ascending
        self.sort()

    def on_previews(self, instance, preview):
        if self.no_sort or len(self.previews) != len(self.values):
            return
        self.sort()

    def on_values(self, instance, values):
        if self.no_sort or len(self.previews) != len(self.values):
            return
        self.sort()

    def on_sort_type(self, instance, sort_type):
        if sort_type == self._sort_type:
            return
        self._sort_type = sort_type

        # Change Value Array
        self.no_sort = True
        index = 0
        for preview in self.previews:
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
            self.values[index] = value
            index += 1
        self.no_sort = False
        self.sort()

    def on_after_sort(self):
        pass


class SortWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(.2, .2, .2, .4)
            Rectangle(size=self.size, pos=self.pos)
        width, height = self.height * 0.9 * 750 / 600, self.height * 0.9
        x, y = (self.width - width) / 2, (self.height - height) / 2
        self.background = Image(source="../res/screens/stats/sort_background.png", size=(width, height), pos=(x, y), keep_ratio=True, allow_stretch=True)
        self.background.bind(on_touch_down=self.toss, on_touch_up=self.toss)
        self.title = Label(text="Sort", font_size=self.height * .125, font_name="../res/fnt/Precious.ttf", color=(0, 0, 0, 1), size_hint=(None, None))
        self.title._label.refresh()
        self.title.size = self.title._label.texture.size
        self.title.pos = (x + (width - self.title.width) / 2, y + height - self.title.height * 1.125)

        button_size = width * 0.1125 * 570 / 215, height * 0.15
        gap = (width * 0.9 - button_size[0] * 3) / 4, (height * 0.6 - button_size[1] * 5) / 6
        gap2 = (width * 0.9 - button_size[0] * 2) / 3, (height * 0.175 - button_size[1]) / 2
        self.layout = GridLayout(cols=3, rows=5, padding=gap, spacing=gap, size=(width * 0.9, height * 0.6), pos=(x + width * 0.05, y + height * 0.05))
        self.ascending = HTButton(size=button_size, pos=(x + gap2[0], y + height * 0.65 + gap2[1]), size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                  text="Ascending", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.descending = HTButton(size=button_size, pos=(x + gap2[0] * 2 + button_size[0], y + height * 0.65 + gap2[1]), size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                  text="Descending", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.strength = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                  text="Strength", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.magic = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                  text="Magic", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.endurance = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                  text="Endurance", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.dexterity = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                  text="Dexterity", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.agility = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                  text="Agility", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.health = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                text="Health", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.mana = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                text="Mana", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.phyatk = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                text="Phy. Atk", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.magatk = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                text="Mag. Atk", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.defense = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                text="Defense", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.party = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                text="Party", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.rank = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                text="Rank", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.name = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                text="Name", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.score = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                text="Score", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
        self.worth = HTButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_stat",
                                text="Worth", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1))
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

        self.add_widget(self.background)
        self.add_widget(self.ascending)
        self.add_widget(self.descending)
        self.add_widget(self.layout)
        self.add_widget(self.title)

    def toss(self, *args):
        return True