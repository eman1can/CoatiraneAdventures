from src.modules.KivyBase.Hoverable import RelativeLayoutBase as RelativeLayout
from kivy.properties import NumericProperty, BooleanProperty, OptionProperty
from kivy.app import App


class HeartIndicator(RelativeLayout):
    is_visible = BooleanProperty(False)
    familiarity = NumericProperty(0.0)
    familiarity_gold = NumericProperty(0.0)

    how_opened = OptionProperty('Closed', options=['Closed', 'Hover', 'Button'])

    def __init__(self, **kwargs):
        self.register_event_type('on_hint_open')
        self.register_event_type('on_hint_close')
        super().__init__(**kwargs)

    def on_mouse_pos(self, hover):
        return self.ids.button.dispatch('on_mouse_pos', hover)

    def on_touch_down(self, touch):
        if self.disabled:
            return False
        if not self.collide_point(*touch.pos):
            return False
        touch.push()
        touch.apply_transform_2d(self.to_local)

        for child in self.children[:]:
            if child.on_touch_down(touch):
                touch.pop()
                return True
        touch.pop()
        return False

    def toggle_hint(self):
        if self.opacity > 0:
            if self.how_opened == 'Hover':
                self.how_opened = 'Button'
                return
            if self.how_opened == 'Closed':
                self.dispatch('on_hint_open')
                self.how_opened = 'Button'
            else:
                self.dispatch('on_hint_close')
                self.how_opened = 'Closed'

    def show_hint(self):
        if self.opacity > 0:
            print(self.how_opened)
            if self.how_opened == 'Closed':
                self.dispatch('on_hint_open')
                self.how_opened = 'Hover'

    def hide_hint(self):
        if self.opacity > 0:
            if self.how_opened == 'Hover':
                self.dispatch('on_hint_close')
                self.how_opened = 'Closed'

    def reset_open(self):
        self.how_opened = 'Closed'

    def on_hint_open(self):
        pass

    def on_hint_close(self):
        pass

    @staticmethod
    def calculate_familiarity_bonus(char_checking, char_exclude=None):
        """
        Familiarity Bonus Mechanics
        Each Character can have a 0.00-100.00 point bonus with another char
        For each 100% they have, they get a 2% bonus w/ and additional 1% at 100
        ex: 50% → 1%, 25% → 0.5%, 99% → 1.98%, 100 -> 3%

        """
        if char_checking is None:
            return -1

        parties = App.get_running_app().main.parties
        current_party = parties[parties[0] + 1]

        value_gold = 0.00
        value_total = 0.00
        bonus = 0.00

        count = 0
        fam = {}
        for char in current_party:
            if char == char_checking or char == char_exclude:
                continue
            if char is not None:
                percentage = char_checking.get_familiarity(char.get_id())
                fam[char.get_display_name().capitalize() + ' ' + char.get_name().capitalize()] = percentage
                if percentage == 100.00: #gold
                    value_gold += 1
                    bonus += 1
                value_total += percentage / 100
                bonus += 2 * (percentage / 100)
                count += 1
        if count < 1:
            return -1, -1, -1, {}
        return value_total / count, value_gold / count, bonus, fam
