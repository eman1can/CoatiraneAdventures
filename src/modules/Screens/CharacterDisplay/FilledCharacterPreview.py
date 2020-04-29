from kivy.app import App
from kivy.clock import Clock
from kivy.input.providers.wm_touch import WM_MotionEvent
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, StringProperty, ListProperty

from src.modules.KivyBase.Hoverable import ScreenBase as Screen, RelativeLayoutBase as RelativeLayout
from src.modules.Screens.CharacterDisplay.HeartIndicator import HeartIndicator


class FilledCharacterPreviewScreen(Screen):
    preview = ObjectProperty(None)
    character = ObjectProperty(None)
    support = ObjectProperty(None)

    is_support = BooleanProperty(False)

    def on_character(self, *args):
        self.name = self.character.get_id()

    def on_support(self, *args):
        if self.support is not None:
            self.name += "_" + self.support.get_id()

    def update_lock(self, locked):
        self.ids.filledPreview.update_lock(locked)

    def close_hints(self):
        self.ids.filledPreview.close_hints()

    def reload(self):
        self.ids.filledPreview.reload()


class FilledCharacterPreview(RelativeLayout):

    text_color = ListProperty([0.796, 0.773, 0.678, 1])
    font_name = StringProperty('../res/fnt/Gabriola.ttf')

    preview = ObjectProperty(None, allownone=True)

    new_image_instance = BooleanProperty(False)
    has_screen = BooleanProperty(False)
    emptied = BooleanProperty(False)
    event = ObjectProperty(None, allownone=True)
    has_tag = BooleanProperty(False)

    preview_wgap = NumericProperty(0)
    preview_hgap = NumericProperty(0)
    image_width = NumericProperty(0)

    is_select = BooleanProperty(False)
    is_support = BooleanProperty(False)
    character = ObjectProperty(None, allownone=True)
    support = ObjectProperty(None, allownone=True)

    locked = BooleanProperty(False)
    do_hover = BooleanProperty(True)

    char_hint_showing = BooleanProperty(False)
    support_hint_showing = BooleanProperty(False)
    hint_text_words = StringProperty('')
    hint_text_numbers = StringProperty('')
    char_hint_words = StringProperty('')
    char_hint_numbers = StringProperty('')
    support_hint_words = StringProperty('')
    support_hint_numbers = StringProperty('')

    char_button_source = StringProperty('')
    support_button_source = StringProperty('')
    char_button_collide_image = StringProperty('')
    support_button_collide_image = StringProperty('')

    background_source = StringProperty('../res/screens/stats/preview_background.png')
    char_image_source = StringProperty('')
    support_image_source = StringProperty('')
    overlay_source = StringProperty('')

    phy_atk_text = StringProperty('0.0')
    mag_atk_text = StringProperty('0.0')
    health_text = StringProperty('0.0')
    mana_text = StringProperty('0.0')
    defense_text = StringProperty('0.0')
    strength_text = StringProperty('0.0')
    magic_text = StringProperty('0.0')
    endurance_text = StringProperty('0.0')
    dexterity_text = StringProperty('0.0')
    agility_text = StringProperty('0.0')

    def __init__(self, **kwargs):
        self.update_overlay()
        self.update_buttons()
        self.update_labels()
        super().__init__(**kwargs)

    def on_is_select(self, *args):
        self.update_overlay()
        self.update_buttons()
        self.update_labels()

    def on_character(self, *args):
        self.char_image_source = self.character.slide_image_source
        self.update_overlay()
        self.update_buttons()
        self.reload()

    def on_support(self, *args):
        self.support_image_source = self.support.slide_support_image_source
        self.update_overlay()
        self.update_buttons()
        self.reload()

    def update_overlay(self):
        if self.support is not None:
            self.overlay_source = "../res/screens/stats/preview_overlay_full.png"
        elif not self.is_select and not self.locked:
            self.overlay_source = "../res/screens/stats/preview_overlay_empty_add.png"
        else:
            self.overlay_source = "../res/screens/stats/preview_overlay_empty.png"

    def get_hint(self, array):
        words = ''
        numbers = ''
        if len(array) > 0:
            for k, v in array.items():
                words += k + '\n'
                numbers += str(round(v, 2)) + '\n'
            words = words[:-1]
            numbers = numbers[:-1]
        else:
            return 'Invalid', '0%'
        return words, numbers

    def close_hints(self):
        self.on_char_hint_close()
        self.on_support_hint_close()
        self.ids.character_heart.how_closed = 'Closed'
        self.ids.support_heart.how_closed = 'Closed'

    def update_labels(self):
        self.phy_atk_text = str(0.0) if self.character is None else str(round(self.character.get_phyatk(), 2)) if self.support is None else str(round(self.character.get_phyatk() + self.support.get_phyatk(), 2))
        self.mag_atk_text = str(0.0) if self.character is None else str(round(self.character.get_magatk(), 2)) if self.support is None else str(round(self.character.get_magatk() + self.support.get_magatk(), 2))
        self.health_text = str(0.0) if self.character is None else str(round(self.character.get_health(), 2)) if self.support is None else str(round(self.character.get_health() + self.support.get_health(), 2))
        self.mana_text = str(0.0) if self.character is None else str(round(self.character.get_mana(), 2)) if self.support is None else str(round(self.character.get_mana() + self.support.get_mana(), 2))
        self.defense_text = str(0.0) if self.character is None else str(round(self.character.get_defense(), 2)) if self.support is None else str(round(self.character.get_defense() + self.support.get_defense(), 2))
        self.strength_text = str(0.0) if self.character is None else str(round(self.character.get_strength(), 2)) if self.support is None else str(round(self.character.get_strength() + self.support.get_strength(), 2))
        self.magic_text = str(0.0) if self.character is None else str(round(self.character.get_magic(), 2)) if self.support is None else str(round(self.character.get_magic() + self.support.get_magic(), 2))
        self.endurance_text = str(0.0) if self.character is None else str(round(self.character.get_endurance(), 2)) if self.support is None else str(round(self.character.get_endurance() + self.support.get_endurance(), 2))
        self.dexterity_text = str(0.0) if self.character is None else str(round(self.character.get_dexterity(), 2)) if self.support is None else str(round(self.character.get_dexterity() + self.support.get_dexterity(), 2))
        self.agility_text = str(0.0) if self.character is None else str(round(self.character.get_agility(), 2)) if self.support is None else str(round(self.character.get_agility() + self.support.get_agility(), 2))

    def update_buttons(self):
        if self.support is not None:
            self.char_button_source = '../res/screens/buttons/char_button_full'
            self.support_button_source = '../res/screens/buttons/support_button_full'
            self.char_button_collide_image = '../res/screens/buttons/char_button_full.collision.png'
        else:
            self.char_button_source = '../res/screens/buttons/char_button'
            self.support_button_source = '../res/screens/buttons/support_button'
            if self.is_select or self.locked:
                self.support_button_collide_image = '../res/screens/buttons/support_button.normal.png'
                self.char_button_collide_image = '../res/screens/buttons/char_button_select.collision.png'
            else:
                self.support_button_collide_image = '../res/screens/buttons/support_button.collision.png'
                self.char_button_collide_image = '../res/screens/buttons/char_button.collision.png'

    def reload(self):
        total, gold, bonus, array = HeartIndicator.calculate_familiarity_bonus(self.character)
        self.ids.character_heart.is_visible = total != -1
        if total != -1:
            self.ids.character_heart.familiarity = total
            self.ids.character_heart.familiarity_gold = gold
            self.char_hint_words, self.char_hint_numbers = self.get_hint(array)
            if self.char_hint_showing:
                self.hint_text_words = self.char_hint_words
                self.hint_text_numbers = self.char_hint_numbers
            self.character.familiarity_bonus = 1 + bonus / 100
        else:
            self.character.familiarity_bonus = 1
        if self.support is not None:
            total, gold, bonus, array = HeartIndicator.calculate_familiarity_bonus(self.support)
            # support calculation will never return false. Base char will always be there
            self.ids.support_heart.familiarity = total
            self.ids.support_heart.familiarity_gold = gold
            self.support_hint_words, self.support_hint_numbers = self.get_hint(array)
            if self.support_hint_showing:
                self.hint_text_words = self.support_hint_words
                self.hint_text_numbers = self.support_hint_numbers
            self.support.familiarity_bonus = 1 + bonus / 100
        self.update_labels()

    def on_locked(self, *args):
        self.update_overlay()
        self.update_buttons()

    def on_char_hint_open(self, *args):
        if self.char_hint_showing or self.support_hint_showing:
            return
        self.hint_text_words = self.char_hint_words
        self.hint_text_numbers = self.char_hint_numbers
        self.ids.hint.opacity = 1
        self.ids.hint.disabled = False
        self.char_hint_showing = True

    def on_char_hint_close(self, *args):
        if not self.char_hint_showing:
            return
        self.ids.hint.opacity = 0
        self.ids.hint.disabled = True
        self.char_hint_showing = False

    def on_support_hint_open(self, *args):
        if self.support_hint_showing or self.char_hint_showing:
            return
        self.hint_text_words = self.support_hint_words
        self.hint_text_numbers = self.support_hint_numbers
        self.ids.hint.opacity = 1
        self.ids.hint.disabled = False
        self.support_hint_showing = True

    def on_support_hint_close(self, *args):
        if not self.support_hint_showing:
            return
        self.ids.hint.opacity = 0
        self.ids.hint.disabled = True
        self.support_hint_showing = False

    def update_lock(self, locked):
        self.locked = locked

    def is_valid_touch(self, *args):
        if not self.has_screen:
            return True
        else:
            current = self.preview.portfolio.parent.parent.current_slide
            if current == self.preview.portfolio:
                return True
        return False

    def on_char_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.is_valid_touch(instance, touch) and not self.locked:
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                touch.grab(self)
                self.emptied = False
                if touch.button == 'left':
                    if not self.is_select:
                        self.event = Clock.schedule_once(lambda dt: self.on_char_empty(instance, touch), .25)
                        return True

    def on_char_empty(self, instance, touch):
        touch.ungrab(self)
        self.emptied = True
        self.preview.set_empty()

    def on_support_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.is_valid_touch(instance, touch) and not self.locked:
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                touch.grab(self)
                self.emptied = False
                if touch.button == 'left':
                    if not self.is_select:
                        self.event = Clock.schedule_once(lambda dt: self.on_support_empty(instance, touch), .25)
                        return True

    def on_support_empty(self, instance, touch):
        touch.ungrab(self)
        self.emptied = True
        self.preview.set_char_screen(False, self.character, None)

    def on_support_touch_up(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if touch.grab_current == self and not self.emptied and not self.locked:
                touch.ungrab(self)
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                if touch.button == 'left':
                    if self.event is not None:
                        self.event.cancel()
                    self.preview.show_select_screen(self, True)
                    return True
                elif touch.button == 'right':
                    if self.support is not None:
                        screen = self.support.get_attr_screen()
                        screen.preview = self.preview
                        screen.reload()
                        App.get_running_app().main.display_screen(screen, True, True)
                        return True
            return False

    def on_char_touch_up(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if touch.grab_current == self and not self.emptied and not self.locked:
                touch.ungrab(self)
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                if touch.button == 'left':
                    if self.event is not None:
                        self.event.cancel()
                    if self.is_select:
                        if self.is_support:
                            self.preview.set_char_screen(True, self.preview.char, self.character)
                        else:
                            self.preview.set_char_screen(True, self.character, None)
                        App.get_running_app().main.display_screen(None, False, False)
                        for screen in App.get_running_app().main.screens:
                            if screen.name == 'dungeon_main':
                                screen.update_party_score()
                                break
                    else:
                        self.preview.show_select_screen(self, False)
                    return True
                elif touch.button == 'right':
                    screen = self.character.get_attr_screen()
                    screen.preview = self.preview
                    screen.reload()
                    App.get_running_app().main.display_screen(screen, True, True)
                    return True
            return False
