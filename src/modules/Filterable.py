from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty, ListProperty
from kivy.graphics import Color, Rectangle
from src.modules.HTButton import HTButton

class Filterable(object):
    previews_filter = ListProperty(None)
    output = ListProperty(None)
    filter_types = ListProperty(['type_light', 'type_dark', 'type_earth', 'type_wind', 'type_thunder', 'type_fire', 'type_water',
                    'type_physical', 'type_magical', 'type_balanced', 'type_defensive', 'type_healing',
                    'rank_1', 'rank_2', 'rank_3', 'rank_4', 'rank_5', 'rank_6', 'rank_7', 'rank_8', 'rank_9', 'rank_10'])
    filters_applied = ListProperty(['type_light', 'type_dark', 'type_earth', 'type_wind', 'type_thunder', 'type_fire', 'type_water',
                    'type_physical', 'type_magical', 'type_balance', 'type_defensive', 'type_healer',
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
            elif 'type_balance' in self.filters_applied and preview.char.get_type() == 'Balance':
                stage2.append(preview)
            elif 'type_defensive' in self.filters_applied and preview.char.get_type() == 'Defensive':
                stage2.append(preview)
            elif 'type_healer' in self.filters_applied and preview.char.get_type() == 'Healer':
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
    initialized = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size = (0, 0)

        self.shadow = Image(source='../res/screens/backgrounds/shadow.png', allow_stretch=True)
        self.shadow.bind(on_touch_down=self.toss)

        self.background = Image(source="../res/screens/stats/sort_background.png", allow_stretch=True)

        self.title = Label(text="Filter", font_name="../res/fnt/Precious.ttf", color=(0, 0, 0, 1), size_hint=(None, None))

        self.filter_button = HTButton(size_hint=(None, None), text="Apply Filter", path="../res/screens/buttons/long_stat")
        self.filter_button = HTButton(size_hint=(None, None), text="Apply Filter", path="../res/screens/buttons/long_stat")

        self.layout_main = GridLayout(cols=1, rows=9)

        self.overlay_bar_type = Image(source="../res/screens/stats/overlay_bar.png", size_hint=(None, None), allow_stretch=True)
        self.overlay_bar_element = Image(source="../res/screens/stats/overlay_bar.png", size_hint=(None, None), allow_stretch=True)
        self.overlay_bar_rank = Image(source="../res/screens/stats/overlay_bar.png", size_hint=(None, None), allow_stretch=True)

        self.label_type = Label(text="By Type", font_name="../res/fnt/Precious.ttf", color=(0, 0, 0, 1), size_hint=(None, None))
        self.label_element = Label(text="By Element", font_name="../res/fnt/Precious.ttf", color=(0, 0, 0, 1), size_hint=(None, None))
        # self.label_element.size = self.label_type._label.texture.size[0] * 1.5, self.label_type._label.texture.size[1]
        self.label_rank = Label(text="By Rank", font_name="../res/fnt/Precious.ttf", color=(0, 0, 0, 1), size_hint=(None, None))

        self.layout_type = GridLayout(cols=5, rows=1, size_hint=(None, None))
        self.layout_element = GridLayout(cols=5, rows=2, size_hint=(None, None))
        self.layout_rank = GridLayout(cols=5, rows=2, size_hint=(None, None))

        self.magical = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="Magical", toggle_enabled=True, toggle_state=True)
        self.physical = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="Physical", toggle_enabled=True, toggle_state=True)
        self.balanced = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="Balanced", toggle_enabled=True, toggle_state=True)
        self.defensive = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="Defensive", toggle_enabled=True, toggle_state=True)
        self.healing = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="Healing", toggle_enabled=True, toggle_state=True)

        self.light = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="Light", toggle_enabled=True, toggle_state=True)
        self.dark = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="Dark", toggle_enabled=True, toggle_state=True)
        self.earth = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="Earth", toggle_enabled=True, toggle_state=True)
        self.wind = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="Wind", toggle_enabled=True, toggle_state=True)
        self.thunder = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="Thunder", toggle_enabled=True, toggle_state=True)
        self.fire = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Fire", toggle_enabled=True, toggle_state=True)
        self.water = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Water", toggle_enabled=True, toggle_state=True)

        self.rank_1 = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Rank 1", toggle_enabled=True, toggle_state=True)
        self.rank_2 = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Rank 2", toggle_enabled=True, toggle_state=True)
        self.rank_3 = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Rank 3", toggle_enabled=True, toggle_state=True)
        self.rank_4 = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Rank 4", toggle_enabled=True, toggle_state=True)
        self.rank_5 = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Rank 5", toggle_enabled=True, toggle_state=True)
        self.rank_6 = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Rank 6", toggle_enabled=True, toggle_state=True)
        self.rank_7 = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Rank 7", toggle_enabled=True, toggle_state=True)
        self.rank_8 = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Rank 8", toggle_enabled=True, toggle_state=True)
        self.rank_9 = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Rank 9", toggle_enabled=True, toggle_state=True)
        self.rank_10 = HTButton(size_hint=(None, None), path="../res/screens/buttons/long_toggle", text="  Rank 10", toggle_enabled=True, toggle_state=True)

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
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.shadow.size = self.size

        width, height = self.height * 0.9 * 750 / 600, self.height * 0.9
        x, y = (self.width - width) / 2, (self.height - height) / 2

        self.background.size = width, height
        self.background.pos = x, y

        self.title.font_size = self.height * .125
        self.title.texture_update()
        self.title.size = self.title.texture_size
        self.title.pos = (x + (width - self.title.width) / 2, y + height - self.title.height * 1.125)

        button_size = height * 0.0725 * 570 / 215, height * 0.0725
        side = (width - button_size[0] * 5 - width * 0.0125 * 4) / 2

        self.filter_button.size = (button_size[0] * 1.25, button_size[1] * 1.25)
        self.filter_button.pos = (x + (width - button_size[0] * 1.25) / 2, y + height * 0.74)
        self.filter_button.font_size = button_size[1] * 0.5

        self.layout_main.padding = side, 0, side, 0
        self.layout_main.spacing = 0, height * 0.0125
        self.layout_main.size = width, height * 0.75
        self.layout_main.pos = x, y

        self.overlay_bar_type.size = width - side * 2, width * 0.8 * 20 / 620
        self.overlay_bar_element.size = width - side * 2, width * 0.8 * 20 / 620
        self.overlay_bar_rank.size = width - side * 2, width * 0.8 * 20 / 620

        self.label_type.font_size = self.height * .03125
        self.label_type.texture_update()
        self.label_type.size = self.label_type.texture_size

        self.label_element.font_size = self.height * .03125
        self.label_element.texture_update()
        self.label_element.size = self.label_element.texture_size

        self.label_rank.font_size = self.height * .03125
        self.label_rank.texture_update()
        self.label_rank.size = self.label_rank.texture_size

        self.layout_type.spacing = width * 0.0125, height * 0.0125
        self.layout_type.size = width - side * 2, height * 0.075

        self.layout_element.spacing = width * 0.0125, height * 0.0125
        self.layout_element.size = width - side * 2, height * 0.15

        self.layout_rank.spacing = width * 0.0125, height * 0.0125
        self.layout_rank.size = width - side * 2, height * 0.15

        self.magical.size = button_size
        self.magical.label_padding = [button_size[0] * .2, 0, 0, 0]
        self.magical.font_size = button_size[1] * 0.45
        self.physical.size = button_size
        self.physical.label_padding = [button_size[0] * .2, 0, 0, 0]
        self.physical.font_size = button_size[1] * 0.45
        self.balanced.size = button_size
        self.balanced.label_padding = [button_size[0] * .2, 0, 0, 0]
        self.balanced.font_size = button_size[1] * 0.45
        self.defensive.size = button_size
        self.defensive.label_padding = [button_size[0] * .2, 0, 0, 0]
        self.defensive.font_size = button_size[1] * 0.45
        self.healing.size = button_size
        self.healing.label_padding = [button_size[0] * .2, 0, 0, 0]
        self.healing.font_size = button_size[1] * 0.45

        self.light.size = button_size
        self.light.font_size = button_size[1] * 0.45
        self.light.label_padding = [button_size[0] * .2, 0, 0, 0]
        self.dark.size = button_size
        self.dark.font_size = button_size[1] * 0.45
        self.dark.label_padding = [button_size[0] * .2, 0, 0, 0]
        self.earth.size = button_size
        self.earth.font_size = button_size[1] * 0.45
        self.earth.label_padding = [button_size[0] * .2, 0, 0, 0]
        self.wind.size = button_size
        self.wind.font_size = button_size[1] * 0.45
        self.wind.label_padding = [button_size[0] * .2, 0, 0, 0]
        self.thunder.size = button_size
        self.thunder.font_size = button_size[1] * 0.45
        self.thunder.label_padding = [button_size[0] * .2, 0, 0, 0]
        self.fire.size = button_size
        self.fire.font_size = button_size[1] * 0.45
        self.fire.label_padding = [button_size[0] * .2, 0, 0, 0]
        self.water.size = button_size
        self.water.font_size = button_size[1] * 0.45
        self.water.label_padding = [button_size[0] * .2, 0, 0, 0]

        self.rank_1.size = button_size
        self.rank_1.font_size = button_size[1] * 0.45
        self.rank_2.size = button_size
        self.rank_2.font_size = button_size[1] * 0.45
        self.rank_3.size = button_size
        self.rank_3.font_size = button_size[1] * 0.45
        self.rank_4.size = button_size
        self.rank_4.font_size = button_size[1] * 0.45
        self.rank_5.size = button_size
        self.rank_5.font_size = button_size[1] * 0.45
        self.rank_6.size = button_size
        self.rank_6.font_size = button_size[1] * 0.45
        self.rank_7.size = button_size
        self.rank_7.font_size = button_size[1] * 0.45
        self.rank_8.size = button_size
        self.rank_8.font_size = button_size[1] * 0.45
        self.rank_9.size = button_size
        self.rank_9.font_size = button_size[1] * 0.45
        self.rank_10.size = button_size
        self.rank_10.font_size = button_size[1] * 0.45

    def toss(self, *args):
        return True
