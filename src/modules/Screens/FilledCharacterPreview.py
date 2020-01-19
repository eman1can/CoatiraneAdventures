from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.input.providers.wm_touch import WM_MotionEvent

from src.modules.HTButton import HTButton


class FilledCharacterPreviewScreen(Screen):
    initialized = BooleanProperty(False)

    def __init__(self, main_screen, preview, is_support, character, support, **kwargs):
        print("Filled Screen: ", self.pos)
        pos = (0, 0)  # Posistion gets reset
        super().__init__(size_hint=(None, None), **kwargs)
        self.name = character.get_id()
        if support is not None:
            self.name += "_" + support.get_id()

        self._size = (0, 0)

        self.preview = FilledCharacterPreview(main_screen=main_screen, preview=preview, is_support=is_support, is_select=False, has_screen=True, character=character, support=support)

        self.add_widget(self.preview)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.preview.size = self.size

    def reload(self):
        self.preview.reload()


class FilledCharacterPreview(Widget):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None, allownone=True)
    preview = ObjectProperty(None, allownone=True)

    new_image_instance = BooleanProperty(False)
    has_screen = BooleanProperty(False)
    emptied = BooleanProperty(False)
    event = ObjectProperty(None, allownone=True)
    has_tag = BooleanProperty(False)
    tag = ObjectProperty(None, allownone=True)

    preview_wgap = NumericProperty(0)
    preview_hgap = NumericProperty(0)
    image_width = NumericProperty(0)

    is_select = BooleanProperty(False)
    is_support = BooleanProperty(False)
    character = ObjectProperty(None, allownone=True)
    support = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(size_hint=(None, None), **kwargs)

        self._size = (0, 0)
        self._pos = (0, 0)

        self.background = Image(source="../res/screens/stats/preview_background.png", allow_stretch=True)
        self.char_image = self.character.get_slide_image(self.new_image_instance)
        self.slide_image_loaded = True

        if self.support is None:
            # Load non-support Overlay
            self.support_image = None
            if self.is_select:
                # Load Empty Overlay
                self.char_button = HTButton(path='../res/screens/buttons/char_button', collide_image='../res/screens/buttons/char_button_select.collision.png')
                self.overlay = Image(source="../res/screens/stats/preview_overlay_empty.png", allow_stretch=True)
            else:
                # Load Empty Add Overlay
                self.char_button = HTButton(path='../res/screens/buttons/char_button')
                self.overlay = Image(source="../res/screens/stats/preview_overlay_empty_add.png", allow_stretch=True)
        else:
            self.support_image = self.support.get_slide_support_image(self.new_image_instance)
            self.slide_support_image_loaded = True

            if self.is_select:
                # Cannot have a selection preview that has a support character
                raise Exception("Selection preview cannot have a support character")
            else:
                self.char_button = HTButton(path='../res/screens/buttons/char_button_full')
                self.overlay = Image(source="../res/screens/stats/preview_overlay_full.png", allow_stretch=True)
        self.char_button.bind(on_touch_down=self.on_char_touch_down, on_touch_up=self.on_char_touch_up)

        if not self.is_select:
            if self.support is None:
                self.support_button = HTButton(path='../res/screens/buttons/support_button')
            else:
                self.support_button = HTButton(path='../res/screens/buttons/support_button_full')
            self.support_button.bind(on_touch_down=self.on_support_touch_down, on_touch_up=self.on_support_touch_up)
        else:
            self.support_button = None

        self.add_widget(self.background)
        self.add_widget(self.char_image)
        if self.support_image is not None:
            self.add_widget(self.support_image)
        self.add_widget(self.overlay)

        self.add_widget(self.char_button)
        if not self.is_select:
            self.add_widget(self.support_button)

        self.stars = []

        for level in self.character.ranks:
            if level.unlocked:
                if not level.broken:
                    star = Image(source="../res/screens/stats/star.png", size_hint=(None, None), opacity=1)
                else:
                    star = Image(source="../res/screens/stats/rankbrk.png", size_hint=(None, None), opacity=1)
            else:
                star = Image(source='../res/screens/stats/star.png', size_hint=(None, None), opacity=0)
            star.type = True
            self.stars.append(star)
            self.add_widget(star)

        if self.support is not None:
            for level in self.support.ranks:
                if level.unlocked:
                    if not level.broken:
                        star = Image(source="../res/screens/stats/star.png", size_hint=(None, None), opacity=1)
                    else:
                        star = Image(source="../res/screens/stats/rankbrk.png", size_hint=(None, None), opacity=1)
                else:
                    star = Image(source='../res/screens/stats/star.png', size_hint=(None, None), opacity=0)
                star.type = False
                self.stars.append(star)
                self.add_widget(star)

        text_color = (.796, .773, .678, 1)

        self.phyatk_image = Image(source='../res/screens/stats/PhysicalAttack.png')
        self.magatk_image = Image(source='../res/screens/stats/MagicalAttack.png')
        self.hp_image = Image(source='../res/screens/stats/Health.png')
        self.mp_image = Image(source='../res/screens/stats/Mana.png')
        self.def_image = Image(source='../res/screens/stats/Defense.png')

        self.str_image = Image(source='../res/screens/stats/Str.png')
        self.mag_image = Image(source='../res/screens/stats/Mag.png')
        self.end_image = Image(source='../res/screens/stats/End.png')
        self.dex_image = Image(source='../res/screens/stats/Dex.png')
        self.agi_image = Image(source='../res/screens/stats/Agi.png')

        self.label_words = Label(text='Strength\nMagic\nHealth\nMana\nDefense', halign="left", color=text_color)
        self.label_words2 = Label(text='trength\nagic\nndurance\nexterity\ngility', halign="left", color=text_color)

        if self.support is None:
            text = str(self.character.get_phyatk())    + "\n" + \
                   str(self.character.get_magatk())    + "\n" + \
                   str(self.character.get_health())    + "\n" + \
                   str(self.character.get_mana())      + "\n" + \
                   str(self.character.get_defense())   + "\n" + \
                   str(self.character.get_strength())  + "\n" + \
                   str(self.character.get_magic())     + "\n" + \
                   str(self.character.get_endurance()) + "\n" + \
                   str(self.character.get_dexterity()) + "\n" + \
                   str(self.character.get_agility())
        else:
            text = str(self.character.get_phyatk()    + self.support.get_phyatk())    + "\n" + \
                   str(self.character.get_magatk()    + self.support.get_magatk())    + "\n" + \
                   str(self.character.get_health()    + self.support.get_health())    + "\n" + \
                   str(self.character.get_mana()      + self.support.get_mana())      + "\n" + \
                   str(self.character.get_defense()   + self.support.get_defense())   + "\n" + \
                   str(self.character.get_strength()  + self.support.get_strength())  + "\n" + \
                   str(self.character.get_magic()     + self.support.get_magic())     + "\n" + \
                   str(self.character.get_endurance() + self.support.get_endurance()) + "\n" + \
                   str(self.character.get_dexterity() + self.support.get_dexterity()) + "\n" + \
                   str(self.character.get_agility()   + self.support.get_agility())

        self.label_numbers = Label(text=text, halign="right", color=text_color)

        self.add_widget(self.phyatk_image)
        self.add_widget(self.magatk_image)
        self.add_widget(self.hp_image)
        self.add_widget(self.mp_image)
        self.add_widget(self.def_image)

        self.add_widget(self.str_image)
        self.add_widget(self.mag_image)
        self.add_widget(self.end_image)
        self.add_widget(self.agi_image)
        self.add_widget(self.dex_image)

        self.add_widget(self.label_words)
        self.add_widget(self.label_words2)
        self.add_widget(self.label_numbers)
        self.initialized = True

    def reload(self):
        if not self.initialized:
            return
        if not self.slide_image_loaded:
            self.char_image = self.character.get_slide_image(False)
            index = 0
            for child in self.children:
                if child.id == 'image_standin_slide':
                    self.children[index] = self.char_image
                    self.char_image.parent = self
                index += 1
            self.slide_image_loaded = True
            self.char_image.size = self.size
            self.char_image.pos = self.pos
        if self.support is not None:
            if not self.slide_support_image_loaded:
                self.support_image = self.support.get_slide_support_image(False)
                index = 0
                for child in self.children:
                    if child.id == 'image_standin_slide_support':
                        self.children[index] = self.support_image
                        self.support_image.parent = self
                    index += 1
                self.slide_support_image_loaded = True
                self.support_image.size = self.size
                self.support_image.pos = self.pos

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return False
        self._size = size.copy()

        self.background.size = self.size
        self.char_image.size = self.size
        if self.support is not None:
            self.support_image.size = self.size
        self.overlay.size = self.size
        self.char_button.size = size
        if not self.is_select:
            self.support_button.size = self.size

        self.preview_wgap = 5 * self.width / 250
        self.preview_hgap = 5 * self.height / 935

        star_size_large = (size[1] * 62 / 935) / 1.5, (size[1] * 62 / 935) / 1.5
        star_size_small = (size[1] * 120 / 935) / 4, (size[1] * 120 / 935) / 4
        for star in self.stars:
            if star.type:
                star.size = star_size_large
            else:
                star.size = star_size_small

        label_height = (size[1] * 120 / 935) / 4
        image_width = label_height
        image_height = image_width
        label_width = (size[0] - self.preview_wgap * 2 - image_width * 1.75) / 2

        self.phyatk_image.size = \
            self.magatk_image.size = \
            self.hp_image.size = \
            self.mp_image.size = \
            self.def_image.size = \
            self.str_image.size = \
            self.mag_image.size = \
            self.end_image.size = \
            self.dex_image.size = \
            self.agi_image.size = (image_width, image_height)

        self.label_words.font_size = label_height * 0.85
        self.label_words.size = (label_width, label_height * 5)
        self.label_words2.font_size = label_height * 0.85
        self.label_words2.size = (label_width, label_height * 5)
        self.label_numbers.font_size = label_height * 0.85
        self.label_numbers.size = (label_width, label_height * 10)

    def on_pos(self, instance, pos):
        if not self.initialized or self._pos == pos:
            return False
        self._pos = pos.copy()

        self.background.pos = self.pos
        self.char_image.pos = self.pos
        self.overlay.pos = self.pos
        self.char_button.pos = pos
        if not self.is_select:
            self.support_button.pos = pos
        if self.support is not None:
            self.support_image.pos = pos

        star_size = (self.size[1] * 62 / 935) / 1.5, (self.size[1] * 62 / 935) / 1.5
        star_columns = 5
        star_width_overlap = .75
        star_height_overlap = .5
        stars_width = star_size[0] * star_columns * star_width_overlap
        star_start = self.size[0] / 2 - stars_width / 2, self.size[1] - self.preview_hgap - star_size[1]

        if self.support is not None:
            diamond_top = 545 * self.size[1] / 935
            diamond_center = 426.5 * self.size[1] / 935
            diamond_bottom = 309 * self.size[1] / 935

            diamond_left = 7 * self.size[0] / 250
            diamond_middle = self.size[0] / 2
            space = (diamond_middle - diamond_left) / 5, (diamond_center - diamond_bottom) / 5

        count = 0
        for star in self.stars:
            if star.type:
                star_row = int(count / star_columns)
                star_column = count % star_columns

                star_x = star_column * star_size[0] * star_width_overlap
                star_y = star_row * star_size[1] * star_height_overlap
                star_offset = (-15 * (star_row + 1)) + (30 * star_row)
                self.stars[count].pos = pos[0] + star_x + star_start[0] + star_offset, pos[1] + self.size[1] - star_size[ 1] - star_y - self.preview_wgap
            else:
                scount = (count - 10)
                if scount < 3:
                    column = row = (count - 10) % 5 + 1
                    star_pos = self.size[0] / 2 - star_size[0] * 1.1 - space[0] * column, diamond_bottom - star_size[1] * 1.1 + space[1] * (row + 1)
                elif scount < 6:
                    column = row = (count - 13) % 5 + 1
                    star_pos = self.size[0] / 2 + star_size[0] * .1 + space[0] * column, diamond_bottom - star_size[1] * 1.1 + space[1] * (row + 1)
                elif scount < 8:
                    column = row = (count - 15) % 5
                    star_pos = self.size[0] / 2 - star_size[0] * 1.4 - space[0] * column, diamond_top - star_size[1] * .1 - space[1] * (row + 1)
                else:
                    column = row = (count - 17) % 5
                    star_pos = self.size[0] / 2 + star_size[0] * .4 + space[0] * column, diamond_top - star_size[1] * .1 - space[1] * (row + 1)
                self.stars[count].pos = star_pos
            count += 1

        label_height = (self.size[1] * 120 / 935) / 4
        image_width = label_height
        label_width = (self.size[0] - self.preview_wgap * 2 - image_width * 1.75) / 2
        # image_height = image_width
        # text_color = (.796, .773, .678, 1)

        image_wstart = pos[0] + self.preview_wgap + image_width / 2
        image_hstart = pos[1] + (self.size[1] * 310 / 935)

        label_wstart = image_wstart + image_width
        label_hstart = pos[1] + (self.size[1] * 310 / 935)

        self.phyatk_image.pos = image_wstart, image_hstart - image_width
        self.magatk_image.pos = image_wstart, image_hstart - image_width * 2
        self.hp_image.pos = image_wstart, image_hstart - image_width * 3
        self.mp_image.pos = image_wstart, image_hstart - image_width * 4
        self.def_image.pos = image_wstart, image_hstart - image_width * 5
        self.str_image.pos = image_wstart, image_hstart - image_width * 6
        self.mag_image.pos = image_wstart, image_hstart - image_width * 7
        self.end_image.pos = image_wstart, image_hstart - image_width * 8
        self.dex_image.pos = image_wstart, image_hstart - image_width * 9
        self.agi_image.pos = image_wstart, image_hstart - image_width * 10

        self.label_words.pos = (label_wstart + image_width * .25, label_hstart - label_height * 5)
        self.label_words2.pos = (label_wstart + self.preview_wgap, label_hstart - label_height * 10)
        self.label_numbers.pos = (label_wstart + label_width, label_hstart - label_height * 10)

        if self.has_tag:
            self.tag.pos = pos[0], pos[1] + self.size[1] - (60 * self.size[1] / 935) - self.tag.height

    def updateStars(self, character, support):
        count = 0
        for level in character.ranks:
            if level.unlocked:
                if not level.broken:
                    self.stars[count].opacity = 1
                else:
                    if self.stars[count].source != '../res/screens/stats/rankbrk.png':
                        self.stars[count].source = '../res/screens/stats/rankbrk.png'
                    self.stars[count].opacity = 1
            count += 1
        if support is not None:
            for level in support.ranks:
                if level.unlocked:
                    if not level.broken:
                        self.stars[count].opacity = 1
                    else:
                        if self.stars[count].source != '../res/screens/stats/rankbrk.png':
                            self.stars[count].source = '../res/screens/stats/rankbrk.png'
                        self.stars[count].opacity = 1
                count += 1

    def is_valid_touch(self, instance, touch):
        if not self.has_screen:
            return True
        else:
            current = self.preview.parent.parent._parent.slots[self.preview.parent.parent._parent.index]
            if current == self.preview.parent.parent:
                return True
        return False

    def on_char_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.is_valid_touch(instance, touch):
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
            if self.is_valid_touch(instance, touch):
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
            if touch.grab_current == self and not self.emptied:
                touch.ungrab(self)
                if isinstance(touch, WM_MotionEvent):
                    touch.button = 'left'
                if touch.button == 'left':
                    if self.event is not None:
                        self.event.cancel()
                    self.preview.show_select_screen(self, True)
                    return True
                elif touch.button == 'right':
                    screen = self.support.get_attr_screen()
                    screen.main_screen = self.main_screen
                    screen.preview = self.preview
                    screen.reload()
                    self.main_screen.display_screen(screen, True, True)
                    return True
            return False

    def on_char_touch_up(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if touch.grab_current == self and not self.emptied:
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
                        self.main_screen.display_screen(None, False, False)
                        for screen in self.main_screen.screens:
                            if screen.name == 'dungeon_main':
                                screen.update_party_score()
                                break
                    else:
                        self.preview.show_select_screen(self, False)
                    return True
                elif touch.button == 'right':
                    screen = self.character.get_attr_screen()
                    screen.main_screen = self.main_screen
                    screen.preview = self.preview
                    screen.reload()
                    self.main_screen.display_screen(screen, True, True)
                    return True
            return False
