# UIX Imports
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty, StringProperty

# Kivy Imports
from kivy.clock import Clock
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview import RecycleView
# KV Import
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.filterable import Filterable
from uix.modules.sortable import Sortable

load_kv(__name__)


class RecyclePreview(RecycleView, Filterable, Sortable):
    is_support = BooleanProperty(False)

    mode = StringProperty('')
    scroll = ObjectProperty(None)
    grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        self._characters = []
        super().__init__(**kwargs)

        self.scroll = ScrollPreview()
        self.grid = GridPreview()

        self.set_scroll()

    def hover_subscribe(self, widget=None, layer=0, adjust=None, blocking=False):
        if adjust is None:
            super().hover_subscribe(widget, layer, adjust=self.to_local, blocking=blocking)
        else:
            super().hover_subscribe(widget, layer, adjust=lambda x, y: self.to_local(*adjust(x, y)), blocking=blocking)

    def on_touch_hover(self, touch):
        if self.disabled:
            return False
        if not self.collide_point(*touch.pos):
            return False
        return self.dispatch_to_relative_children(touch)

    def set_characters(self, characters):
        self._characters = characters

    def update(self, preview, char, is_support):
        self.is_support = is_support

        self.data.clear()
        party = Refs.gc.get_current_party()
        for char_index in Refs.gc.get_obtained_character_indexes(is_support):
            if char_index == char:
                continue
            self.data.append({'character': char_index, 'support': -1, 'is_select': True, 'has_tag': char_index in party, 'has_stat': True, 'stat_type': self.sort_type, 'on_return': lambda character: self.update_preview(character, preview)})
        self.previews_filter = self.data
        self.refresh_from_data()
        self.filter()

    def update_preview(self, character, preview):
        if self.is_support:
            preview.set_char_screen(preview.get_character(), character, True)
        else:
            preview.set_char_screen(character, preview.get_support(), True)
        Refs.gs.display_screen(None, False, False)

    def change_hover(self, new_hover):
        self.child.change_hover(new_hover)

    def set_scroll(self):
        if self.mode == 'scroll':
            return
        self.remove_widget(self.grid)
        self.add_widget(self.scroll)
        self.viewclass = 'FilledCharacterPreview'
        self.mode = 'scroll'
        self.child = self.scroll
        self.refresh_from_layout()

    def set_grid(self):
        if self.mode == 'grid':
            return
        self.remove_widget(self.scroll)
        self.add_widget(self.grid)
        self.viewclass = 'SquareCharacterPreview'
        self.mode = 'grid'
        self.child = self.grid
        self.refresh_from_layout()

    def on_after_sort(self, *args):
        # self.previews_filter = self.previews_sort
        for preview in self.previews_sort:
            preview['stat_type'] = self.sort_type
        self.data = self.previews_sort
        # print(self.previews_sort)
        self.refresh_from_data()
        # self.filter()
        #self.selector.update_number()

    def on_after_filter(self):
        # print(self.output)
        self.previews_sort = self.output
        self.force_update_values()
        self.sort()


        # self.data = self.output
        # self.refresh_from_data()
        # self.selector.update_number()

    def on_scroll_start(self, touch, check_children=True):
        if check_children:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if self.dispatch_children('on_scroll_start', touch):
                touch.pop()
                return True
            touch.pop()

        if not self.collide_point(*touch.pos):
            touch.ud[self._get_uid('svavoid')] = True
            return
        if self.disabled:
            return True
        if self._touch or (not (self.do_scroll_x or self.do_scroll_y)):
            return self.simulate_touch_down(touch)

        # handle mouse scrolling, only if the viewport size is bigger than the
        # scrollview size, and if the user allowed to do it
        vp = self._viewport
        if not vp:
            return True
        scroll_type = self.scroll_type
        ud = touch.ud
        scroll_bar = 'bars' in scroll_type

        # check if touch is in bar_x(horizontal) or bar_y(vertical)
        width_scrollable = vp.width > self.width
        height_scrollable = vp.height > self.height

        d = {'bottom': touch.y - self.y - self.bar_margin,
             'top': self.top - touch.y - self.bar_margin,
             'left': touch.x - self.x - self.bar_margin,
             'right': self.right - touch.x - self.bar_margin}

        ud['in_bar_x'] = (scroll_bar and width_scrollable and
                          (0 <= d[self.bar_pos_x] <= self.bar_width))
        ud['in_bar_y'] = (scroll_bar and height_scrollable and
                          (0 <= d[self.bar_pos_y] <= self.bar_width))

        if vp and 'button' in touch.profile and \
                touch.button.startswith('scroll'):
            btn = touch.button
            m = self.scroll_wheel_distance
            e = None

            if width_scrollable and ((btn == 'scrolldown' and self.scroll_x >= 1) or (btn == 'scrollup' and self.scroll_x <= 0) or (btn == 'scrollleft' and self.scroll_x >= 1) or (btn == 'scrollright' and self.scroll_x <= 0)):
                return False

            if height_scrollable and ((btn == 'scrolldown' and self.scroll_y >= 1) or (btn == 'scrollup' and self.scroll_y <= 0) or (btn == 'scrollleft' and self.scroll_y >= 1) or (btn == 'scrollright' and self.scroll_y <= 0)):
                return False

            if (self.effect_x and self.do_scroll_y and height_scrollable and
                    btn in ('scrolldown', 'scrollup', 'scrollleft', 'scrollright')):
                e = self.effect_x if ud['in_bar_x'] else self.effect_y

            elif (self.effect_y and self.do_scroll_x and width_scrollable and
                  btn in ('scrollleft', 'scrollright', 'scrollup', 'scrolldown')):
                e = self.effect_y if ud['in_bar_y'] else self.effect_x

            if e:
                if btn in ('scrolldown', 'scrollleft'):
                    if self.smooth_scroll_end:
                        e.velocity -= m * self.smooth_scroll_end
                    else:
                        e.value = max(e.value - m, e.min)
                        e.velocity = 0
                elif btn in ('scrollup', 'scrollright'):
                    if self.smooth_scroll_end:
                        e.velocity += m * self.smooth_scroll_end
                    else:
                        e.value = min(e.value + m, e.max)
                        e.velocity = 0
                touch.ud[self._get_uid('svavoid')] = True
                e.trigger_velocity_update()
            return True

        in_bar = ud['in_bar_x'] or ud['in_bar_y']
        if scroll_type == ['bars'] and not in_bar:
            return self.simulate_touch_down(touch)

        if in_bar:
            if (ud['in_bar_y'] and not
            self._touch_in_handle(
                self._handle_y_pos, self._handle_y_size, touch)):
                self.scroll_y = (touch.y - self.y) / self.height
            elif (ud['in_bar_x'] and not
            self._touch_in_handle(
                self._handle_x_pos, self._handle_x_size, touch)):
                self.scroll_x = (touch.x - self.x) / self.width

        # no mouse scrolling, so the user is going to drag the scrollview with
        # this touch.
        self._touch = touch
        uid = self._get_uid()

        ud[uid] = {
            'mode': 'unknown',
            'dx': 0,
            'dy': 0,
            'user_stopped': in_bar,
            'frames': Clock.frames,
            'time': touch.time_start}

        if self.do_scroll_x and self.effect_x and not ud['in_bar_x']:
            self._effect_x_start_width = self.width
            self.effect_x.start(touch.x)
            self._scroll_x_mouse = self.scroll_x
        if self.do_scroll_y and self.effect_y and not ud['in_bar_y']:
            self._effect_y_start_height = self.height
            self.effect_y.start(touch.y)
            self._scroll_y_mouse = self.scroll_y

        if not in_bar:
            Clock.schedule_once(self._change_touch_mode,
                                self.scroll_timeout / 1000.)
        return True


class Preview(RecycleGridLayout):
    def change_hover(self, new_hover):
        for preview in self.children:
            preview.do_hover = new_hover

    def on_touch_hover(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        return self.dispatch_to_children(touch)


class ScrollPreview(Preview):
    pass


class GridPreview(Preview):
    pass
