from kivy.properties import BooleanProperty, ListProperty, StringProperty

from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen
from uix.screens.profile.main import CharacterList

load_kv(__name__)


class SkillTreeMain(Screen):
    def __init__(self, perks, **kwargs):
        self._width = 0
        self._height = 0
        self.tree_lines = []
        self.tree_sizes = {}
        self.perks = perks

        self._perk_trees = {}
        self._perk_count = 0
        self._box_width = 0
        self._box_height = 0
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.ids.perk_points.text = f'You have {Refs.gc.get_perk_points()} perk points'

        for perk_id, perk in Refs.gc['perks'].items():
            tree_id, level_id = perk.get_tree(), perk.get_level()
            self.tree_sizes[tree_id] = 0

            if level_id not in self._perk_trees:
                self._perk_trees[level_id] = {}
            if tree_id not in self._perk_trees[level_id]:
                self._perk_trees[level_id][tree_id] = []

            self._perk_trees[level_id][tree_id].append(perk)
            self._perk_count += 1

        for level_id, trees in self._perk_trees.items():
            for tree_id, perks in trees.items():
                self.tree_sizes[tree_id] = max(self.tree_sizes[tree_id], len(perks))

        rows = 4
        cols = sum(self.tree_sizes.values())
        self._box_width = self.width * 0.904 / cols
        self._box_height = self.height * 0.5 / rows
        self._width = self.width
        self._height = self.height

        self.display_perk_boxes()

        self.tree_lines.clear()

        self.canvas.add(Color(rgba=(0, 0, 0, 1)))

        start = self.width * 0.048
        for index, (tree_id, tree_count) in enumerate(self.tree_sizes.items()):
            tree_width = tree_count * self._box_width

            tree_title = tree_id.title()
            label = Label(size_hint_x=None, width=tree_width, text=tree_title, font_name='Precious', font_size='36', color=(0, 0, 0, 1))
            self.ids.tree_titles.add_widget(label)

            if index == len(self.tree_sizes) - 1:
                continue
            x = start + tree_width
            line = Line(width=3, points=[x, self.height * 0.25, x, self.height * 0.75])
            self.tree_lines.append(line)
            self.canvas.add(line)
            start += tree_width

    def reload(self, perks, *args):
        self.perks = perks
        self.display_perk_boxes()

    def display_perk_boxes(self):
        self.ids.perk_grid.clear_widgets()
        for level_id, trees in reversed(self._perk_trees.items()):
            cost = {4: 105, 3: 21, 2: 3, 1: 1}[level_id]
            for tree_id, perks in trees.items():
                spacer_size = (self.tree_sizes[tree_id] - len(perks)) * self._box_width
                if spacer_size > 0:
                    self.ids.perk_grid.add_widget(Widget(size_hint=(None, None), width=spacer_size / 2, height=self._box_height))
                for perk in perks:
                    perk_box = PerkBox(size_hint=(None, None), size=(self._box_width, self._box_height))
                    if Refs.gc.has_perk(perk.get_id()):
                        perk_box.obtained = True
                        perk_box.char_list = self.perks[tree_id][perk.get_id()]
                    elif cost > Refs.gc.get_skill_level() and cost != 1:
                        perk_box.active = False
                    perk_box.text = perk.get_name()
                    perk_box.bind(on_release=lambda instance, perk_id=perk.get_id(): self.show_perk_info(perk_id))
                    self.ids.perk_grid.add_widget(perk_box)
                if spacer_size > 0:
                    self.ids.perk_grid.add_widget(Widget(size_hint=(None, None), width=spacer_size / 2, height=self._box_height))

    def update_perk_box(self, perk_id, char_id):
        perk = Refs.gc['perks'][perk_id]
        tree = perk.get_tree()
        if tree not in self.perks:
            self.perks[tree] = {}
        if perk_id not in self.perks[tree]:
            self.perks[tree][perk_id] = []
        character = Refs.gc.get_char_by_id(char_id)
        self.perks[tree][perk_id].append(character)

        for perk_box in self.ids.perk_grid.children:
            if not isinstance(perk_box, PerkBox):
                continue
            if perk_box.text == perk.get_name():
                perk_box.char_list = self.perks[tree][perk_id]
                perk_box.obtained = True

    def on_size(self, instance, new_size):
        if 'perk_grid' in self.ids:
            scale_width = self.width / self._width
            scale_height = self.height / self._height
            rows = 4
            cols = sum(self.tree_sizes.values())
            self._box_width = self.width * 0.904 / cols
            self._box_height = self.height * 0.5 / rows
            self._width = self.width
            self._height = self.height

            start = self.width * 0.048
            box_width = self.width * 0.904 / sum(self.tree_sizes.values())
            for index, (tree_id, tree_width) in enumerate(self.tree_sizes.items()):
                if index == len(self.tree_sizes) - 1:
                    continue
                x = start + tree_width * box_width
                points = [x, self.height * 0.25, x, self.height * 0.75]
                self.tree_lines[index].points = points
                start += tree_width * box_width

            for label in self.ids.tree_titles.children:
                label.width *= scale_width

            for child in self.ids.perk_grid.children:
                child.width *= scale_width
                child.height *= scale_height

    def show_perk_info(self, perk_id):
        Refs.gp.display_popup(self, 'perk_info', perk_id)


class PerkBox(RelativeLayout):
    color = ListProperty([0, 0, 0, 255])
    color_fade = ListProperty([0, 0, 0, 0])

    text = StringProperty('test')
    obtained = BooleanProperty(False)
    active = BooleanProperty(True)

    char_list = ListProperty([])

    def __init__(self, **kwargs):
        self.register_event_type('on_release')
        super().__init__(**kwargs)

    def on_obtained(self, instance, value):
        if self.obtained:
            self.color = [0, 255, 255, 255]
            self.color_fade = [0, 125, 125, 0]

    def on_active(self, instance, value):
        if not self.active:
            self.color = [75, 75, 75, 255]
            self.color_fade = [37, 37, 37, 0]
        else:
            self.color = [0, 0, 0, 255]
            self.color_fade = [125, 125, 125, 0]

    def on_perk_info(self):
        if not self.active:
            return
        self.dispatch('on_release')

    def on_char_list(self, instance, char_list):
        perk_display = CharacterList(char_list)
        perk_display.size_hint = (1, None)
        perk_display.height = self.height * 0.25
        perk_display.pos_hint = {'x': 0.075, 'y': 0.075}
        self.ids['perk_display'] = perk_display
        self.add_widget(perk_display)

    def on_height(self, instance, height):
        if 'perk_display' in self.ids:
            self.ids['perk_display'].height = self.height * 0.25

    def on_release(self):
        pass
