# UIX Imports
from refs import Refs
from uix.modules.screen import Screen

# Kivy Imports
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class CharacterSelector(Screen):
    #initialized = BooleanProperty(False)
    #preview = ObjectProperty(None)

    has_left = BooleanProperty(False)
    toggle = BooleanProperty(False)  # When False, Is Slots

    #overlay_texture = ObjectProperty(None)
    #number_icon_texture = ObjectProperty(None)
    character_num = NumericProperty(0.0)

    def __init__(self, preview, is_support, **kwargs):
        self.is_support = is_support
        #self.overlay_texture = Image('backgrounds/select_char_overlay.png').texture
        #self.number_icon_texture = Image('screens/stats/icon.png').texture
        self._size = 0, 0
        super().__init__(**kwargs)

        # self.sort = SortWidget()#id='sort')
        # self.ids.sort.text = self.ids.multi.sort_type
        # self.sort.ids.back.bind(on_release=lambda instance: self.close_sort())
        # self.sort.ids.ascending.bind(on_release=lambda instance: self.do_sort(instance, 'Ascending'))
        # self.sort.ids.descending.bind(on_release=lambda instance: self.do_sort(instance, 'Descending'))
        # self.sort.ids.strength.bind(on_release=lambda instance: self.do_sort(instance, 'Strength'))
        # self.sort.ids.magic.bind(on_release=lambda instance: self.do_sort(instance, 'Magic'))
        # self.sort.ids.endurance.bind(on_release=lambda instance: self.do_sort(instance, 'Endurance'))
        # self.sort.ids.dexterity.bind(on_release=lambda instance: self.do_sort(instance, 'Dexterity'))
        # self.sort.ids.agility.bind(on_release=lambda instance: self.do_sort(instance, 'Agility'))
        # self.sort.ids.health.bind(on_release=lambda instance: self.do_sort(instance, 'Health'))
        # self.sort.ids.mana.bind(on_release=lambda instance: self.do_sort(instance, 'Mana'))
        # self.sort.ids.phyatk.bind(on_release=lambda instance: self.do_sort(instance, 'Phy. Atk'))
        # self.sort.ids.magatk.bind(on_release=lambda instance: self.do_sort(instance, 'Mag. Atk'))
        # self.sort.ids.defense.bind(on_release=lambda instance: self.do_sort(instance, 'Defense'))
        # self.sort.ids.party.bind(on_release=lambda instance: self.do_sort(instance, 'Party'))
        # self.sort.ids.rank.bind(on_release=lambda instance: self.do_sort(instance, 'Rank'))
        # self.sort.ids.name.bind(on_release=lambda instance: self.do_sort(instance, 'Name'))
        # self.sort.ids.score.bind(on_release=lambda instance: self.do_sort(instance, 'Score'))
        # self.sort.ids.worth.bind(on_release=lambda instance: self.do_sort(instance, 'Worth'))

        # self.filter = FilterWidget()#id='filter')
        # self.filter.ids.apply_filter.bind(on_release=lambda instance: self.do_filter())
        # self.filter.ids.back.bind(on_release=lambda instance: self.close_filter())
        # self.filter.ids.magical.bind(on_release=lambda instance: self.modify_filter(instance, 'type_magical'))
        # self.filter.ids.physical.bind(on_release=lambda instance: self.modify_filter(instance, 'type_physical'))
        # self.filter.ids.balanced.bind(on_release=lambda instance: self.modify_filter(instance, 'type_balanced'))
        # self.filter.ids.defensive.bind(on_release=lambda instance: self.modify_filter(instance, 'type_defensive'))
        # self.filter.ids.healing.bind(on_release=lambda instance: self.modify_filter(instance, 'type_healing'))
        # self.filter.ids.light.bind(on_release=lambda instance: self.modify_filter(instance, 'type_light'))
        # self.filter.ids.dark.bind(on_release=lambda instance: self.modify_filter(instance, 'type_dark'))
        # self.filter.ids.earth.bind(on_release=lambda instance: self.modify_filter(instance, 'type_earth'))
        # self.filter.ids.wind.bind(on_release=lambda instance: self.modify_filter(instance, 'type_wind'))
        # self.filter.ids.thunder.bind(on_release=lambda instance: self.modify_filter(instance, 'type_thunder'))
        # self.filter.ids.fire.bind(on_release=lambda instance: self.modify_filter(instance, 'type_fire'))
        # self.filter.ids.water.bind(on_release=lambda instance: self.modify_filter(instance, 'type_water'))
        # self.filter.ids.rank_1.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_1'))
        # self.filter.ids.rank_2.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_2'))
        # self.filter.ids.rank_3.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_3'))
        # self.filter.ids.rank_4.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_4'))
        # self.filter.ids.rank_5.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_5'))
        # self.filter.ids.rank_6.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_6'))
        # self.filter.ids.rank_7.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_7'))
        # self.filter.ids.rank_8.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_8'))
        # self.filter.ids.rank_9.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_9'))
        # self.filter.ids.rank_10.bind(on_release=lambda instance: self.modify_filter(instance, 'rank_10'))

        #char = preview.char
        #if is_support:
        #    char = preview.support

        #self.has_left = preview is not None and char is not None

        #if self.has_left:
        #    self.ids.single.update(preview, char)

        Clock.schedule_once(lambda dt: self.update_screen(preview, is_support), 0)
        #self.single = None
        #if self.has_left:
        #    self.single = SinglePreview(preview=preview, character=char, is_support=is_support, size_hint=(None, None))

        # self.multi = RecyclePreview(self, preview, is_support=is_support, size_hint=(None, None))

        #if self.has_left:
        #    self.single.reload()
        #    self.add_widget(self.single)

        #self.add_widget(self.multi)

    def reload(self, preview, is_support, **kwargs):
        self.update_screen(preview, is_support)

    def update_screen(self, preview, is_support):
        self.is_support = is_support

        char = preview.char
        if is_support:
            char = preview.support

        self.has_left = preview is not None and char is not None

        if self.has_left:
            self.ids.single.update(preview, char)

        self.ids.multi.update(preview, char, self.content.get_obtained_characters(is_support), self.content.get_current_party())

    def on_pre_enter(self, *args):
        pass
        #self.update_number()

    # def on_size(self, instance, size):
    #     if self._size == size:
    #         return
    #     self._size = size.copy()
    #
    #     self.sort.size = self.size
    #     self.filter.size = self.size

    def on_scroll(self):
        self.ids.multi.do_scroll()

    def on_grid(self):
        self.ids.multi.do_grid()

    def on_sort(self):
        # self.ids.switch_display.state = 'normal'
        # self.ids.switch_display.do_hover = False
        # self.ids.switch_display.disabled = True
        # self.ids.multi.change_hover(False)
        # self.sort.open()
        Refs.gp.display_popup(self, 'sort', self.ids.multi.sort_type, self.do_sort)

    def do_sort(self, sort_type):
        self.reset_scroll()
        if sort_type == 'Ascending':
            self.ids.multi.ascending = False
        elif sort_type == 'Descending':
            self.ids.multi.ascending = True
        else:
            if sort_type in ['Party', 'Name']:
                self.ids.multi.ascending = False
            else:
                self.ids.multi.ascending = True
            # self.ids.sort.text = type
            self.ids.multi.sort_type = sort_type
        # self.close_sort()

    def on_filter(self):
        Refs.gp.display_popup(self, 'filter', self.do_filter, self.modify_filter)
        # self.ids.switch_display.state = 'normal'
    #     self.ids.switch_display.do_hover = False
    #     self.ids.switch_display.disabled = True
    #     self.ids.multi.change_hover(False)
    #     self.filter.open()

    def modify_filter(self, filter_type):
        self.ids.multi.no_filter = True
        if filter_type in self.ids.multi.filters_applied:
            self.ids.multi.filters_applied.remove(filter_type)
        else:
            self.ids.multi.filters_applied.append(filter_type)
        self.ids.multi.no_filter = False

    def do_filter(self):
        self.reset_scroll()
        self.ids.multi.filter()
        self.close_filter()
        self.update_number()

    def update_number(self):
        if self.ids.multi is None:
            self.character_num = 0
        else:
            self.character_num = len(self.ids.multi.output)

    def reset_scroll(self):
        self.ids.multi.scroll_x = 0
        self.ids.multi.scroll_y = 1

    # def close_sort(self):
    #     self.ids.switch_display.disabled = False
    #     self.ids.switch_display.do_hover = True
    #     self.ids.multi.change_hover(True)
    #     self.sort.dismiss()

    # def close_filter(self):
    #     self.ids.switch_display.disabled = False
    #     self.ids.switch_display.do_hover = True
    #     self.ids.multi.change_hover(True)
    #     self.filter.dismiss()