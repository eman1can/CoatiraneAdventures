from kivy.properties import BooleanProperty, ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

from src.modules.Screens.SinglePreview import SinglePreview
from src.modules.Screens.ScrollPreview import ScrollPreview
from src.modules.Screens.GridPreview import GridPreview
from src.modules.HTButton import HTButton
from src.modules.Sortable import SortWidget
from src.modules.Filterable import FilterWidget

class CharacterSelector(Screen):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None)
    preview = ObjectProperty(None)

    is_support = BooleanProperty(False)
    toggle = BooleanProperty(False)  # When False, Is Slots

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'select_char'

        self._size = (0, 0)

        self.background = Image(source="../res/screens/backgrounds/background.png", allow_stretch=True)
        self.overlay = Image(source='../res/screens/backgrounds/select_char_overlay.png', allow_stretch=True)

        if not self.is_support:
            characters = self.main_screen.obtained_characters_a.copy()
        else:
            characters = self.main_screen.obtained_characters_s.copy()

        for x in range(len(characters)):
            characters[x] = self.main_screen.characters[characters[x]]

        self.has_left = self.preview.char is not None and not self.is_support or self.is_support and self.preview.support is not None
        if self.has_left:
            if self.is_support:
                char = self.preview.support
            else:
                char = self.preview.char
            self.single = SinglePreview(main_screen=self.main_screen, preview=self.preview, character=char, is_support=self.is_support, size_hint=(None, None))
        else:
            self.single = None

        self.scroll = ScrollPreview(main_screen=self.main_screen, preview=self.preview, characters=characters, is_support=self.is_support, size_hint=(None, None))
        self.grid = GridPreview(main_screen=self.main_screen, preview=self.preview, characters=characters, is_support=self.is_support, size_hint=(None, None))

        self.sort = SortWidget()
        self.sort.ascending.bind(on_release=lambda instance: self.do_sort(instance, 'Ascending'))
        self.sort.descending.bind(on_release=lambda instance: self.do_sort(instance, 'Descending'))
        self.sort.strength.bind(on_release=lambda instance: self.do_sort(instance, 'Strength'))
        self.sort.magic.bind(on_release=lambda instance: self.do_sort(instance, 'Magic'))
        self.sort.endurance.bind(on_release=lambda instance: self.do_sort(instance, 'Endurance'))
        self.sort.dexterity.bind(on_release=lambda instance: self.do_sort(instance, 'Dexterity'))
        self.sort.agility.bind(on_release=lambda instance: self.do_sort(instance, 'Agility'))
        self.sort.health.bind(on_release=lambda instance: self.do_sort(instance, 'Health'))
        self.sort.mana.bind(on_release=lambda instance: self.do_sort(instance, 'Mana'))
        self.sort.phyatk.bind(on_release=lambda instance: self.do_sort(instance, 'Phy. Atk'))
        self.sort.magatk.bind(on_release=lambda instance: self.do_sort(instance, 'Mag. Atk'))
        self.sort.defense.bind(on_release=lambda instance: self.do_sort(instance, 'Defense'))
        self.sort.party.bind(on_release=lambda instance: self.do_sort(instance, 'Party'))
        self.sort.rank.bind(on_release=lambda instance: self.do_sort(instance, 'Rank'))
        self.sort.name.bind(on_release=lambda instance: self.do_sort(instance, 'Name'))
        self.sort.score.bind(on_release=lambda instance: self.do_sort(instance, 'Score'))
        self.sort.worth.bind(on_release=lambda instance: self.do_sort(instance, 'Worth'))

        self.filter = FilterWidget()
        self.filter.filter_button.bind(on_release=self.do_filter)
        self.filter.magical.bind(on_release=lambda instance: self.modify_filter(instance, 'type_magical'))
        self.filter.physical.bind(on_release=lambda instance: self.modify_filter(instance, 'type_physical'))
        self.filter.balanced.bind(on_release=lambda instance: self.modify_filter(instance, 'type_balanced'))
        self.filter.defensive.bind(on_release=lambda instance: self.modify_filter(instance, 'type_defensive'))
        self.filter.healing.bind(on_release=lambda instance: self.modify_filter(instance, 'type_healing'))
        self.filter.light.bind(on_release=lambda instance: self.modify_filter(instance, 'type_light'))
        self.filter.dark.bind(on_release=lambda instance: self.modify_filter(instance, 'type_dark'))
        self.filter.earth.bind(on_release=lambda instance: self.modify_filter(instance, 'type_earth'))
        self.filter.wind.bind(on_release=lambda instance: self.modify_filter(instance, 'type_wind'))
        self.filter.thunder.bind(on_release=lambda instance: self.modify_filter(instance, 'type_thunder'))
        self.filter.fire.bind(on_release=lambda instance: self.modify_filter(instance, 'type_fire'))
        self.filter.water.bind(on_release=lambda instance: self.modify_filter(instance, 'type_water'))
        self.filter.rank_1.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_1'))
        self.filter.rank_2.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_2'))
        self.filter.rank_3.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_3'))
        self.filter.rank_4.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_4'))
        self.filter.rank_5.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_5'))
        self.filter.rank_6.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_6'))
        self.filter.rank_7.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_7'))
        self.filter.rank_8.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_8'))
        self.filter.rank_9.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_9'))
        self.filter.rank_10.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_10'))

        self.sort_button = HTButton(size_hint=(None, None), text=self.grid.sort_type, path='../res/screens/buttons/long_stat', on_release=self.on_sort)
        self.filter_button = HTButton(size_hint=(None, None), text="Filter", path="../res/screens/buttons/long_stat", on_release=self.on_filter)
        self.toggle_button = HTButton(size_hint=(None, None), text="Switch Display", path='../res/screens/buttons/long_stat', toggle_enabled=True, on_toggle_up=self.on_scroll, on_toggle_down=self.on_grid)

        self.add_widget(self.background)
        self.add_widget(self.overlay)
        if self.has_left:
            self.single.reload()
            self.add_widget(self.single)

        if self.toggle:
            self.add_widget(self.grid)
        else:
            self.add_widget(self.scroll)

        self.add_widget(self.sort_button)
        self.add_widget(self.filter_button)
        self.add_widget(self.toggle_button)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        single_x = 0
        if self.has_left:
            single_x = self.width * 0.15
            self.single.size = single_x, self.height * 0.85
        self.grid.size = self.width - single_x, self.height * 0.85
        self.grid.pos = single_x, 0
        self.scroll.size = self.width - single_x, self.height * 0.85
        self.scroll.pos = single_x, 0

        button_size = self.width * 0.075 * 570 / 215, self.width * 0.075
        self.sort_button.size = button_size
        self.filter_button.size = button_size
        self.toggle_button.size = button_size

        self.sort.size = self.size
        self.filter.size = self.size

        self.sort_button.font_size = button_size[1] * 0.45
        self.sort_button.pos = (self.width - button_size[0] * 3) * 1 / 4, self.height * 0.85 + self.height * 0.075 - button_size[1] / 2
        self.filter_button.font_size = button_size[1] * 0.45
        self.filter_button.pos = (self.width - button_size[0] * 3) * 2 / 4 + button_size[0], self.height * 0.85 + self.height * 0.075 - button_size[1] / 2
        self.toggle_button.font_size = button_size[1] * 0.45
        self.toggle_button.pos = (self.width - button_size[0] * 3) * 3 / 4 + button_size[0] * 2, self.height * 0.85 + self.height * 0.075 - button_size[1] / 2

    def reload(self):
        pass

    def on_scroll(self, instance):
        self.remove_widget(self.grid)
        self.add_widget(self.scroll)

    def on_grid(self, instance):
        self.remove_widget(self.scroll)
        self.add_widget(self.grid)

    def on_sort(self, instance):
        self.toggle_button.state = 'normal'
        self.toggle_button.do_hover = False
        self.toggle_button.disabled = True
        for preview in self.grid.previews_sort:
            preview.char_button.do_hover = False
        for preview in self.scroll.previews_sort:
            preview.char_button.do_hover = False
        self.add_widget(self.sort)

    def do_sort(self, instance, type):
        if type == 'Ascending':
            self.grid.ascending = False
            self.scroll.ascending = False
        elif type == 'Descending':
            self.grid.ascending = True
            self.scroll.ascending = True
        else:
            self.sort_button.text = type
            self.grid.sort_type = type
            self.scroll.sort_type = type
        self.toggle_button.disabled = False
        self.toggle_button.do_hover = True
        for preview in self.grid.previews_sort:
            preview.char_button.do_hover = True
        for preview in self.scroll.previews_sort:
            preview.char_button.do_hover = True
        self.remove_widget(self.sort)

    def on_filter(self, instance):
        self.toggle_button.state = 'normal'
        self.toggle_button.do_hover = False
        self.toggle_button.disabled = True
        for preview in self.grid.previews_sort:
            preview.char_button.do_hover = False
        for preview in self.scroll.previews_sort:
            preview.char_button.do_hover = False
        self.add_widget(self.filter)

    def modify_filter(self, instance, filter):
        if filter in self.grid.filters_applied:
            self.grid.filters_applied.remove(filter)
            self.scroll.filters_applied.remove(filter)
        else:
            self.grid.filters_applied.append(filter)
            self.scroll.filters_applied.append(filter)

    def do_filter(self, instance):
        self.grid.filter()
        self.scroll.filter()
        self.toggle_button.disabled = False
        self.toggle_button.do_hover = True
        for preview in self.grid.previews_sort:
            preview.char_button.do_hover = True
        for preview in self.scroll.previews_sort:
            preview.char_button.do_hover = True
        self.remove_widget(self.filter)