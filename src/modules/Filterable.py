from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty, ListProperty
from kivy.graphics import Color, Rectangle
from src.modules.HCButton import HCButton
from src.modules.HTButton import HTButton

class Filterable(object):
    previews_filter = ListProperty(None)
    output = ListProperty(None)
    filter_types = ListProperty(['type_light', 'type_dark', 'type_earth', 'type_wind', 'type_thunder', 'type_fire', 'type_water',
                    'type_physical', 'type_magical', 'type_balanced', 'type_defensive', 'type_healing',
                    'rank_1', 'rank_2', 'rank_3', 'rank_4', 'rank_5', 'rank_6', 'rank_7', 'rank_8', 'rank_9', 'rank_10'])
    filters_applied = ListProperty(['type_light', 'type_dark', 'type_earth', 'type_wind', 'type_thunder', 'type_fire', 'type_water',
                    'type_physical', 'type_magical', 'type_balanced', 'type_defensive', 'type_healing',
                    'rank_1', 'rank_2', 'rank_3', 'rank_4', 'rank_5', 'rank_6', 'rank_7', 'rank_8', 'rank_9', 'rank_10'])
    no_filter = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_after_filter')
        super().__init__(**kwargs)
        self._filters_applied = self.filters_applied

    def filter(self):
        self.no_filter = True
        self.apply_filter()
        self.no_filter = False
        self.dispatch('on_after_filter')

    def apply_filter(self):
        stage1 = []
        for preview in self.previews_filter:
            if 'type_light' in self.filters_applied and preview.char.get_element() == 'light':
                stage1.append(preview)
            elif 'type_dark' in self.filters_applied and preview.char.get_element() == 'dark':
                stage1.append(preview)
            elif 'type_earth' in self.filters_applied and preview.char.get_element() == 'earth':
                stage1.append(preview)
            elif 'type_wind' in self.filters_applied and preview.char.get_element() == 'wind':
                stage1.append(preview)
            elif 'type_thunder' in self.filters_applied and preview.char.get_element() == 'thunder':
                stage1.append(preview)
            elif 'type_fire' in self.filters_applied and preview.char.get_element() == 'fire':
                stage1.append(preview)
            elif 'type_water' in self.filters_applied and preview.char.get_element() == 'water':
                stage1.append(preview)
        stage2 = []
        for preview in stage1:
            if 'type_magical' in self.filters_applied and preview.char.get_type() == 'Magical':
                stage2.append(preview)
            elif 'type_physical' in self.filters_applied and preview.char.get_type() == 'Physical':
                stage2.append(preview)
            elif 'type_balanced' in self.filters_applied and preview.char.get_type() == 'Balanced':
                stage2.append(preview)
            elif 'type_defensive' in self.filters_applied and preview.char.get_type() == 'Defensive':
                stage2.append(preview)
            elif 'type_healing' in self.filters_applied and preview.char.get_type() == 'Healing':
                stage2.append(preview)
        output = []
        for preview in stage2:
            if 'rank_1' in self.filters_applied and preview.char.get_current_rank() == 1:
                output.append(preview)
            elif 'rank_2' in self.filters_applied and preview.char.get_current_rank() == 2:
                output.append(preview)
            elif 'rank_3' in self.filters_applied and preview.char.get_current_rank() == 3:
                output.append(preview)
            elif 'rank_4' in self.filters_applied and preview.char.get_current_rank() == 4:
                output.append(preview)
            elif 'rank_5' in self.filters_applied and preview.char.get_current_rank() == 5:
                output.append(preview)
            elif 'rank_6' in self.filters_applied and preview.char.get_current_rank() == 6:
                output.append(preview)
            elif 'rank_7' in self.filters_applied and preview.char.get_current_rank() == 7:
                output.append(preview)
            elif 'rank_8' in self.filters_applied and preview.char.get_current_rank() == 8:
                output.append(preview)
            elif 'rank_9' in self.filters_applied and preview.char.get_current_rank() == 9:
                output.append(preview)
            elif 'rank_10' in self.filters_applied and preview.char.get_current_rank() == 10:
                output.append(preview)
        self.output = output



    def on_previews(self, instance, preview):
        if self.no_filter:
            return
        self.filter()

    def on_filters_applied(self, instance, filters_applied):
        if filters_applied == self._filters_applied:
            return
        self._filters_applied = filters_applied
        self.filter()

    def on_after_filter(self):
        pass


class FilterWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(.2, .2, .2, .4)
            Rectangle(size=self.size, pos=self.pos)
        width, height = self.height * 0.9 * 750 / 600, self.height * 0.9
        x, y = (self.width - width) / 2, (self.height - height) / 2

        self.shadow = Image(source='../res/screens/backgrounds/shadow.png', size=self.size, pos=self.pos, keep_ratio=True, allow_stretch=True)
        self.shadow.bind(on_touch_down=self.toss, on_touch_up=self.toss)
        self.background = Image(source="../res/screens/stats/sort_background.png", size=(width, height), pos=(x, y), keep_ratio=True, allow_stretch=True)
        self.title = Label(text="Filter", font_size=self.height * .125, font_name="../res/fnt/Precious.ttf", color=(0, 0, 0, 1), size_hint=(None, None))
        self.title._label.refresh()
        self.title.size = self.title._label.texture.size
        self.title.pos = (x + (width - self.title.width) / 2, y + height - self.title.height * 1.125)

        button_size = height * 0.0725 * 570 / 215, height * 0.0725
        side = (width - button_size[0] * 5 - width * 0.0125 * 4) / 2

        self.filter_button = HTButton(size=(button_size[0] * 1.25, button_size[1] * 1.25), pos=(x + (width - button_size[0] * 1.25) / 2, y + height * 0.74), size_hint=(None, None), color=(0, 0, 0, 1), border=[0, 0, 0, 0], text="Apply Filter", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", path="../res/screens/buttons/long_stat")

        self.layout_main = GridLayout(cols=1, rows=9, padding=(side, 0, side, 0), spacing=(0, height * 0.0125), size=(width, height * 0.75), pos=(x, y))
        self.overlay_bar_type = Image(source="../res/screens/stats/overlay_bar.png", size=(width - side * 2, width * 0.8 * 20 / 620), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.overlay_bar_element = Image(source="../res/screens/stats/overlay_bar.png", size=(width - side * 2, width * 0.8 * 20 / 620), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.overlay_bar_rank = Image(source="../res/screens/stats/overlay_bar.png", size=(width - side * 2, width * 0.8 * 20 / 620), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.label_type = Label(text="By Type", font_size=self.height * .03125, font_name="../res/fnt/Precious.ttf", color=(0, 0, 0, 1), size_hint=(None, None))
        self.label_type._label.refresh()
        self.label_type.size = self.label_type._label.texture.size
        self.label_element = Label(text="By Element", font_size=self.height * .03125, font_name="../res/fnt/Precious.ttf", color=(0, 0, 0, 1), size_hint=(None, None))
        self.label_element._label.refresh()
        self.label_element.size = self.label_type._label.texture.size[0] * 1.5, self.label_type._label.texture.size[1]
        self.label_rank = Label(text="By Rank", font_size=self.height * .03125, font_name="../res/fnt/Precious.ttf", color=(0, 0, 0, 1), size_hint=(None, None))
        self.label_rank._label.refresh()
        self.label_rank.size = self.label_type._label.texture.size
        self.layout_type = GridLayout(cols=5, rows=1, spacing=(width * 0.0125, height * 0.0125), size=(width - side * 2, height * 0.075), size_hint=(None, None))
        self.layout_element = GridLayout(cols=5, rows=2, spacing=(width * 0.0125, height * 0.0125), size=(width - side * 2, height * 0.15), size_hint=(None, None))
        self.layout_rank = GridLayout(cols=5, rows=2, spacing=(width * 0.0125, height * 0.0125), size=(width - side * 2, height * 0.15), size_hint=(None, None))

        self.magical = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", padding_x=button_size[0] * 0.2, text="=Magical", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.physical = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", padding_x=button_size[0] * 0.2, text="Physical", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.balanced = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", padding_x=button_size[0] * 0.2, text="Balanced", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.defensive = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", padding_x=button_size[0] * 0.2, text="Defensive", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.healing = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", padding_x=button_size[0] * 0.2, text="Healing", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)

        self.light = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Light", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.dark = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Dark", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.earth = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Earth", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.wind = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Wind", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.thunder = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="      Thunder", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.fire = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Fire", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.water = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Water", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)

        self.rank_1 = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Rank 1", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.rank_2 = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Rank 2", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.rank_3 = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Rank 3", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.rank_4 = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Rank 4", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.rank_5 = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Rank 5", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.rank_6 = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Rank 6", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.rank_7 = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Rank 7", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.rank_8 = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Rank 8", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.rank_9 = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Rank 9", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)
        self.rank_10 = HCButton(size=button_size, size_hint=(None, None), border=[0, 0, 0, 0], path="../res/screens/buttons/long_toggle", text="  Rank 10", font_size=button_size[1] * 0.45, font_name="../res/fnt/Gabriola.ttf", color=(0, 0, 0, 1), toggle_state=True)

        self.add_widget(self.shadow)
        self.add_widget(self.background)
        self.add_widget(self.title)
        self.add_widget(self.filter_button)
        self.add_widget(self.layout_main)

        self.layout_main.add_widget(self.overlay_bar_type)
        self.layout_main.add_widget(self.label_type)
        self.layout_main.add_widget(self.layout_type)

        self.layout_type.add_widget(self.magical)
        self.layout_type.add_widget(self.physical)
        self.layout_type.add_widget(self.balanced)
        self.layout_type.add_widget(self.defensive)
        self.layout_type.add_widget(self.healing)

        self.layout_main.add_widget(self.overlay_bar_element)
        self.layout_main.add_widget(self.label_element)
        self.layout_main.add_widget(self.layout_element)

        self.layout_element.add_widget(self.light)
        self.layout_element.add_widget(self.dark)
        self.layout_element.add_widget(self.earth)
        self.layout_element.add_widget(self.wind)
        self.layout_element.add_widget(self.thunder)
        self.layout_element.add_widget(self.fire)
        self.layout_element.add_widget(self.water)

        self.layout_main.add_widget(self.overlay_bar_rank)
        self.layout_main.add_widget(self.label_rank)
        self.layout_main.add_widget(self.layout_rank)

        self.layout_rank.add_widget(self.rank_1)
        self.layout_rank.add_widget(self.rank_2)
        self.layout_rank.add_widget(self.rank_3)
        self.layout_rank.add_widget(self.rank_4)
        self.layout_rank.add_widget(self.rank_5)
        self.layout_rank.add_widget(self.rank_6)
        self.layout_rank.add_widget(self.rank_7)
        self.layout_rank.add_widget(self.rank_8)
        self.layout_rank.add_widget(self.rank_9)
        self.layout_rank.add_widget(self.rank_10)

    def toss(self, *args):
        return True
