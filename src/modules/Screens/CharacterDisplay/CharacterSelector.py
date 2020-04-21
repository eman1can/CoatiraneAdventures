from kivy.app import App
from kivy.core.image import Image
from kivy.properties import BooleanProperty, ObjectProperty

from src.modules.Filterable import FilterWidget
from src.modules.KivyBase.Hoverable import ScreenH as Screen
from src.modules.Screens.CharacterDisplay.ScrollPreview import RecyclePreview
from src.modules.Screens.CharacterDisplay.SinglePreview import SinglePreview
from src.modules.Sortable import SortWidget


class CharacterSelector(Screen):
    initialized = BooleanProperty(False)
    preview = ObjectProperty(None)

    is_support = BooleanProperty(False)
    toggle = BooleanProperty(False)  # When False, Is Slots

    background_texture = ObjectProperty(None)
    overlay_texture = ObjectProperty(None)
    number_icon_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.background_texture = Image('../res/screens/backgrounds/background.png').texture
        self.overlay_texture = Image('../res/screens/backgrounds/select_char_overlay.png').texture
        self.number_icon_texture = Image('../res/screens/stats/icon.png').texture
        self.root = App.get_running_app().main
        self._size = 0, 0
        super().__init__(**kwargs)

        if not self.is_support:
            characters = self.root.obtained_characters_a.copy()
        else:
            characters = self.root.obtained_characters_s.copy()

        for x in range(len(characters)):
            characters[x] = self.root.characters[characters[x]]

        if self.preview is None:
            self.has_left = False
        else:
            self.has_left = self.preview.char is not None and not self.is_support or self.is_support and self.preview.support is not None
        if self.has_left:
            if self.is_support:
                char = self.preview.support
            else:
                char = self.preview.char
            self.single = SinglePreview(preview=self.preview, character=char, is_support=self.is_support, size_hint=(None, None))
        else:
            self.single = None

        self.multi = RecyclePreview(preview=self.preview, characters=characters, is_support=self.is_support, selector=self, size_hint=(None, None))

        self.sort = SortWidget(id='sort')
        self.ids.sort.text = self.multi.sort_type
        self.sort.ids.back.bind(on_release=lambda instance : self.close_sort())
        self.sort.ids.ascending.bind(on_release=lambda instance: self.do_sort(instance, 'Ascending'))
        self.sort.ids.descending.bind(on_release=lambda instance: self.do_sort(instance, 'Descending'))
        self.sort.ids.strength.bind(on_release=lambda instance: self.do_sort(instance, 'Strength'))
        self.sort.ids.magic.bind(on_release=lambda instance: self.do_sort(instance, 'Magic'))
        self.sort.ids.endurance.bind(on_release=lambda instance: self.do_sort(instance, 'Endurance'))
        self.sort.ids.dexterity.bind(on_release=lambda instance: self.do_sort(instance, 'Dexterity'))
        self.sort.ids.agility.bind(on_release=lambda instance: self.do_sort(instance, 'Agility'))
        self.sort.ids.health.bind(on_release=lambda instance: self.do_sort(instance, 'Health'))
        self.sort.ids.mana.bind(on_release=lambda instance: self.do_sort(instance, 'Mana'))
        self.sort.ids.phyatk.bind(on_release=lambda instance: self.do_sort(instance, 'Phy. Atk'))
        self.sort.ids.magatk.bind(on_release=lambda instance: self.do_sort(instance, 'Mag. Atk'))
        self.sort.ids.defense.bind(on_release=lambda instance: self.do_sort(instance, 'Defense'))
        self.sort.ids.party.bind(on_release=lambda instance: self.do_sort(instance, 'Party'))
        self.sort.ids.rank.bind(on_release=lambda instance: self.do_sort(instance, 'Rank'))
        self.sort.ids.name.bind(on_release=lambda instance: self.do_sort(instance, 'Name'))
        self.sort.ids.score.bind(on_release=lambda instance: self.do_sort(instance, 'Score'))
        self.sort.ids.worth.bind(on_release=lambda instance: self.do_sort(instance, 'Worth'))

        self.filter = FilterWidget(id='filter')
        self.filter.ids.apply_filter.bind(on_release=lambda instance : self.do_filter())
        self.filter.ids.back.bind(on_release=lambda instance : self.close_filter())
        self.filter.ids.magical.bind(on_release=lambda instance: self.modify_filter(instance, 'type_magical'))
        self.filter.ids.physical.bind(on_release=lambda instance: self.modify_filter(instance, 'type_physical'))
        self.filter.ids.balanced.bind(on_release=lambda instance: self.modify_filter(instance, 'type_balanced'))
        self.filter.ids.defensive.bind(on_release=lambda instance: self.modify_filter(instance, 'type_defensive'))
        self.filter.ids.healing.bind(on_release=lambda instance: self.modify_filter(instance, 'type_healing'))
        self.filter.ids.light.bind(on_release=lambda instance: self.modify_filter(instance, 'type_light'))
        self.filter.ids.dark.bind(on_release=lambda instance: self.modify_filter(instance, 'type_dark'))
        self.filter.ids.earth.bind(on_release=lambda instance: self.modify_filter(instance, 'type_earth'))
        self.filter.ids.wind.bind(on_release=lambda instance: self.modify_filter(instance, 'type_wind'))
        self.filter.ids.thunder.bind(on_release=lambda instance: self.modify_filter(instance, 'type_thunder'))
        self.filter.ids.fire.bind(on_release=lambda instance: self.modify_filter(instance, 'type_fire'))
        self.filter.ids.water.bind(on_release=lambda instance: self.modify_filter(instance, 'type_water'))
        self.filter.ids.rank_1.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_1'))
        self.filter.ids.rank_2.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_2'))
        self.filter.ids.rank_3.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_3'))
        self.filter.ids.rank_4.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_4'))
        self.filter.ids.rank_5.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_5'))
        self.filter.ids.rank_6.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_6'))
        self.filter.ids.rank_7.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_7'))
        self.filter.ids.rank_8.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_8'))
        self.filter.ids.rank_9.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_9'))
        self.filter.ids.rank_10.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_10'))

        if self.has_left:
            self.single.reload()
            self.add_widget(self.single)

        self.add_widget(self.multi)

        self.initialized = True

    def update_screen(self, preview, is_support):
        if self.has_left:
            self.remove_widget(self.single)
            self.single = None

        self.preview, self.is_support = preview, is_support

        if not self.is_support:
            characters = self.root.obtained_characters_a.copy()
        else:
            characters = self.root.obtained_characters_s.copy()

        for x in range(len(characters)):
            characters[x] = self.root.characters[characters[x]]

        self.has_left = self.preview.char is not None and not self.is_support or self.is_support and self.preview.support is not None
        if self.has_left:
            if self.is_support:
                char = self.preview.support
            else:
                char = self.preview.char
            self.single = SinglePreview(preview=self.preview, character=char, is_support=self.is_support, size_hint=(None, None))
            self.add_widget(self.single)
        else:
            self.single = None
        single_x = 0
        if self.has_left:
            single_x = self.width * 0.15
            self.single.size = single_x, self.height * 0.85
        self.multi.size = self.width - single_x, self.height * 0.85
        self.multi.pos = single_x, 0
        self.multi.update(None if self.single is None else self.single.character, self.preview, self.is_support, characters, self.root.parties[self.root.parties[0] + 1])

    def on_pre_enter(self, *args):
        self.update_number(len(self.multi.output))

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        single_x = 0
        if self.has_left:
            single_x = self.width * 0.15
            self.single.size = single_x, self.height * 0.85
        self.multi.size = self.width - single_x, self.height * 0.85
        self.multi.pos = single_x, 0

        self.sort.size = self.size
        self.filter.size = self.size

    def reload(self):
        pass

    def on_scroll(self):
        self.multi.do_scroll()

    def on_grid(self):
        self.multi.do_grid()

    def on_sort(self):
        self.ids.switch_display.state = 'normal'
        self.ids.switch_display.do_hover = False
        self.ids.switch_display.disabled = True
        self.multi.change_hover(False)
        self.sort.open()

    def do_sort(self, instance, type):
        self.reset_scroll()
        if type == 'Ascending':
            self.multi.ascending = False
        elif type == 'Descending':
            self.multi.ascending = True
        else:
            if type in ['Party', 'Name']:
                self.multi.ascending = False
            else:
                self.multi.ascending = True
            self.ids.sort.text = type
            self.multi.sort_type = type
        self.close_sort()

    def on_filter(self):
        self.ids.switch_display.state = 'normal'
        self.ids.switch_display.do_hover = False
        self.ids.switch_display.disabled = True
        self.multi.change_hover(False)
        self.filter.open()

    def modify_filter(self, instance, filter):
        if filter in self.multi.filters_applied:
            self.multi.filters_applied.remove(filter)
        else:
            self.multi.filters_applied.append(filter)

    def do_filter(self):
        self.reset_scroll()
        self.multi.filter()
        self.close_filter()
        self.update_number(len(self.multi.previews_sort))

    def update_number(self, number):
        self.ids.number.text = str(number)

    def reset_scroll(self):
        self.multi.scroll_x = 0
        self.multi.scroll_y = 1

    def on_back_press(self):
        if not self.ids.back.disabled:
            self.root.display_screen(None, False, False)

    def close_sort(self):
        self.ids.switch_display.disabled = False
        self.ids.switch_display.do_hover = True
        self.multi.change_hover(True)
        self.sort.dismiss()

    def close_filter(self):
        self.ids.switch_display.disabled = False
        self.ids.switch_display.do_hover = True
        self.multi.change_hover(True)
        self.filter.dismiss()