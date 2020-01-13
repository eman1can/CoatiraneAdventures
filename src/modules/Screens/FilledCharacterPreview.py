from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from kivy.uix.label import Label
from kivy.input.providers.wm_touch import WM_MotionEvent
from kivy.clock import Clock

from datetime import datetime

from src.modules.CustomHoverableButton import CustomHoverableButton

class FilledCharacterPreviewScreen(Screen):
    def __init__(self, main_screen, preview, size, pos, isSelect, character, support, isSupport):
        pos = (0, 0) # Posistion gets reset
        super().__init__(size=size, pos=pos)
        self.main_screen = main_screen
        self.preview = FilledCharacterPreview(main_screen, preview, size, pos, isSelect, True, character, support, isSupport, False)
        self.add_widget(self.preview)
        if support is not None:
            self.name = character.get_id() + "_" + support.get_id()
        else:
            self.name = character.get_id()

    def reload(self):
        self.preview.reload()

class FilledCharacterPreview(Widget):
    def __init__(self, main_screen, preview, size, pos, isSelect, has_screen, character, support, isSupport, new_image_instance, **kwargs):
        self.initalized = False
        if pos == (-1, -1):
            super().__init__(size=size, **kwargs)
        else:
            super().__init__(size=size, pos=pos)

        self.main_screen = main_screen
        self.has_screen = has_screen
        self.preview = preview
        self.character = character
        self.support = support
        self.isSelect = isSelect
        self.isSupport = isSupport
        self.event = None

        self.preview_width = 250
        self.preview_height = 935

        self.preview_wgap = 5 * size[0] / self.preview_width
        self.preview_hgap = 5 * size[1] / self.preview_height
        self.image_width = size[0] - self.preview_wgap * 2
        self.image_height = 635 * size[1] / self.preview_height - self.preview_hgap * 2

        self.background = Image(source="../res/screens/stats/preview_background.png", size=size, pos=pos, allow_stretch=True)
        self.char_image = character.get_slide_image(new_image_instance)
        self.slide_image_loaded = True
        self.char_image.width = self.image_width
        self.char_image.height = self.image_width * self.char_image.texture_size[1] / self.char_image.texture_size[0]
        self.char_image.pos = pos[0] + self.preview_wgap, pos[1] + size[1] - self.char_image.height - self.preview_hgap - (60 * size[1] / self.preview_height)

        self.char_button = Button(background_color=(0, 0, 0, 0), size=size, pos=pos, on_touch_down=self.on_char_touch_down, on_touch_up=self.on_char_touch_up)

        self.support_image = None
        if support is None:
            # Load non-support Overlay
            if isSelect:
                # Load Empty Overlay
                self.overlay = Image(source="../res/screens/stats/preview_overlay_empty.png", size=size, pos=pos, allow_stretch=True)
            else:
                # Load Empty Add Overlay
                self.overlay = Image(source="../res/screens/stats/preview_overlay_empty_add.png", size=size, pos=pos, allow_stretch=True)
        else:
            self.support_image = support.get_preview_image(new_image_instance)
            self.preview_image_loaded = True
            self.support_image.size = self.image_width, self.image_width
            self.support_image.pos = self.preview_wgap, size[1] - self.image_height - self.preview_hgap

            if isSelect:
                # Cannot have a selection preview that has a support character
                raise Exception("Selection preview cannot have a support character")
            else:
                self.overlay = Image(source="../res/screens/stats/preview_overlay_full.png", size=size, pos=pos, allow_stretch=True)

        if not self.isSelect:
            if support is None:
                self.support_button = CustomHoverableButton(
                    background_normal='../res/screens/stats/support_button.normal.png', background_down='',
                    collide_image='../res/screens/stats/support_button.collide.png', size=size, pos=pos)
            else:
                self.support_button = CustomHoverableButton(
                    background_normal='../res/screens/stats/support_button.normal.png', background_down='',
                    collide_image='../res/screens/stats/support_button_full.collide.png', size=size, pos=pos)
            self.support_button.bind(on_touch_down=self.on_support_touch_down, on_touch_up=self.on_support_touch_up)

        self.add_widget(self.background)
        self.add_widget(self.char_image)
        if self.support_image is not None:
            self.add_widget(self.support_image)
        self.add_widget(self.overlay)

        self.stars = []
        count = 0
        star_width = (size[1] * 62 / self.preview_height) / 1.5
        star_size = star_width, star_width
        star_columns = 5
        star_width_overlap = .75
        star_height_overlap = .5
        stars_width = star_size[0] * star_columns * star_width_overlap
        star_start = size[0] / 2 - stars_width / 2, size[1] - self.preview_hgap - star_size[1]

        for level in character.ranks:
            star_row = int(count / star_columns)
            star_column = count % star_columns

            star_x = star_column * star_size[0] * star_width_overlap
            star_y = star_row * star_size[1] * star_height_overlap
            star_offset = (-15 * (star_row + 1)) + (30 * star_row)
            star_pos = pos[0] + star_x + star_start[0] + star_offset, pos[1] + size[1] - star_size[1] - star_y - self.preview_wgap

            if level.unlocked:
                if not level.broken:
                    self.stars.append(
                        Image(source="../res/screens/stats/star.png", pos=star_pos, size=star_size, size_hint=(None, None), opacity=1))
                else:
                    self.stars.append(
                        Image(source="../res/screens/stats/rankbrk.png", pos=star_pos, size=star_size, size_hint=(None, None), opacity=1))
                self.add_widget(self.stars[count])
            else:
                self.stars.append(
                    Image(source='../res/screens/stats/star.png', pos=star_pos, size=star_size, size_hint=(None, None), opacity=0))
                self.add_widget(self.stars[count])
            count += 1
        if support is not None:
            diamond_top = 545 * size[1] / self.preview_height
            diamond_center = 426.5 * size[1] / self.preview_height
            diamond_bottom = 309 * size[1] / self.preview_height

            diamond_left = 7 * size[0] / self.preview_width
            diamond_middle = size[0] / 2

            space = (diamond_middle - diamond_left) / 5, (diamond_center - diamond_bottom) / 5

            for level in support.ranks:
                scount = (count - 10)
                if scount < 3:
                    column = row = (count - 10) % 5 + 1
                    star_pos = size[0] / 2 - star_size[0] * 1.1 - space[0] * column, diamond_bottom - star_size[1] * 1.1 + space[1] * (row + 1)
                elif scount < 6:
                    column = row = (count - 13) % 5 + 1
                    star_pos = size[0] / 2 + star_size[0] * .1 + space[0] * column, diamond_bottom - star_size[1] * 1.1 + space[1] * (row + 1)
                elif scount < 8:
                    column = row = (count - 15) % 5
                    star_pos = size[0] / 2 - star_size[0] * 1.4 - space[0] * column, diamond_top - star_size[1] * .1 - space[1] * (row + 1)
                else:
                    column = row = (count - 17) % 5
                    star_pos = size[0] / 2 + star_size[0] * .4 + space[0] * column, diamond_top - star_size[1] * .1 - space[1] * (row + 1)

                if level.unlocked:
                    if not level.broken:
                        self.stars.append(
                            Image(source="../res/screens/stats/star.png", pos=star_pos, size=star_size,
                                  size_hint=(None, None), opacity=1))
                    else:
                        self.stars.append(
                            Image(source="../res/screens/stats/rankbrk.png", pos=star_pos,
                                  size=star_size,
                                  size_hint=(None, None), opacity=1))
                    self.add_widget(self.stars[count])
                else:
                    self.stars.append(
                        Image(source='../res/screens/stats/star.png', pos=star_pos, size=star_size,
                              size_hint=(None, None), opacity=0))
                    self.add_widget(self.stars[count])
                count += 1

        self.add_widget(self.char_button)
        if not self.isSelect:
            self.add_widget(self.support_button)

        label_height = (size[1] * 120 / self.preview_height) / 4
        image_width = label_height
        image_height = image_width
        label_width = (size[0] - self.preview_wgap * 2 - image_width * 1.75) / 2
        text_color = (.796, .773, .678, 1)

        image_wstart = pos[0] + self.preview_wgap + image_width/2
        image_hstart = pos[1] + (size[1] * 310 / self.preview_height)

        label_wstart = image_wstart + image_width
        label_hstart = pos[1] + (size[1] * 310 / self.preview_height)

        self.phyatk_image = Image(source='../res/screens/stats/PhysicalAttack.png', size=(image_width, image_height), pos=(image_wstart, image_hstart - image_height))
        self.magatk_image = Image(source='../res/screens/stats/MagicalAttack.png', size=(image_width, image_height), pos=(image_wstart, image_hstart - image_height*2))
        self.hp_image = Image(source='../res/screens/stats/Health.png', size=(image_width, image_height), pos=(image_wstart, image_hstart - image_height * 3))
        self.mp_image = Image(source='../res/screens/stats/Mana.png', size=(image_width, image_height), pos=(image_wstart, image_hstart - image_height * 4))
        self.def_image = Image(source='../res/screens/stats/Defense.png', size=(image_width, image_height), pos=(image_wstart, image_hstart - image_height * 5))

        self.str_image = Image(source='../res/screens/stats/Str.png', size=(image_width, image_height), pos=(image_wstart, image_hstart - image_height * 6))
        self.mag_image = Image(source='../res/screens/stats/Mag.png', size=(image_width, image_height), pos=(image_wstart, image_hstart - image_height * 7))
        self.end_image = Image(source='../res/screens/stats/End.png', size=(image_width, image_height), pos=(image_wstart, image_hstart - image_height * 8))
        self.dex_image = Image(source='../res/screens/stats/Dex.png', size=(image_width, image_height), pos=(image_wstart, image_hstart - image_height * 9))
        self.agi_image = Image(source='../res/screens/stats/Agi.png', size=(image_width, image_height), pos=(image_wstart, image_hstart - image_height * 10))

        self.label_words = Label(text='Strength\nMagic\nHealth\nMana\nDefense', halign="left", font_size=label_height * 0.85, color=text_color)
        self.label_words.bind(text_size=self.label_words.setter('size'))
        self.label_words.pos = (label_wstart + image_width * .25, label_hstart - label_height*5)
        self.label_words.size = (label_width, label_height*5)

        self.label_words2 = Label(text='trength\nagic\nndurance\nexterity\ngility', halign="left",
                                       font_size=label_height * 0.85, color=text_color)
        self.label_words2.bind(text_size=self.label_words.setter('size'))
        self.label_words2.pos = (label_wstart + self.preview_wgap, label_hstart - label_height * 10)
        self.label_words2.size = (label_width, label_height * 5)

        if support is None:
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

        self.label_numbers = Label(text=text, halign="right", font_size=label_height * 0.85, color=text_color)
        self.label_numbers.bind(text_size=self.label_numbers.setter('size'))
        self.label_numbers.pos = (label_wstart + label_width, label_hstart - label_height*10)
        self.label_numbers.size = (label_width, label_height*10)

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

        self.initalized = True
        self.size = size
        self.pos = pos

    def reload(self):
        if not self.slide_image_loaded:
            self.char_image = self.character.get_slide_image(False)
            index = 0
            for child in self.children:
                if child.id == 'image_standin_slide':
                    self.children[index] = self.char_image
                    self.char_image.parent = self
                index += 1
            self.slide_image_loaded = True
            self.char_image.width = self.image_width
            self.char_image.height = self.image_width * self.char_image.texture_size[1] / self.char_image.texture_size[0]
            self.char_image.pos = self.pos[0] + self.preview_wgap, self.pos[1] + self.size[1] - self.char_image.height - self.preview_hgap - (60 * self.size[1] / self.preview_height)
        if self.support is not None:
            if not self.preview_image_loaded:
                self.support_image = self.support.get_preview_image(False)
                index = 0
                for child in self.children:
                    if child.id == 'image_standin_preview':
                        self.children[index] = self.support_image
                        self.support_image.parent = self
                    index += 1
                self.preview_image_loaded = True
                self.support_image.size = self.image_width, self.image_width
                self.support_image.pos = self.preview_wgap, self.size[1] - self.image_height - self.preview_hgap

    def on_size(self, instance, size):
        if not self.initalized:
            return False
        self.background.size = size

        self.preview_wgap = 5 * size[0] / self.preview_width
        self.preview_hgap = 5 * size[1] / self.preview_height
        self.image_width = size[0] - self.preview_wgap * 2
        self.image_height = 635 * size[1] / self.preview_height - self.preview_hgap * 2

        self.char_image.width = self.image_width
        self.char_image.height = self.image_width * self.char_image.texture_size[1] / self.char_image.texture_size[0]
        if self.support is not None:
            self.support_image.size = self.image_width, self.image_width

        self.overlay.size = size

        count = 0
        star_width = (size[1] * 62 / self.preview_height) / 1.5
        star_size = star_width, star_width
        for level in self.character.ranks:
            self.stars[count].size = star_size
            count += 1

        if self.support is not None:
            for level in self.character.ranks:
                self.stars[count].size = star_size
                count += 1

        label_height = (size[1] * 120 / self.preview_height) / 4
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

        self.label_words.size = (label_width, label_height * 5)
        self.label_words.font_size = label_height * 0.85
        self.label_words2.size = (label_width, label_height * 5)
        self.label_words2.font_size = label_height * 0.85
        self.label_numbers.size = (label_width, label_height * 10)
        self.label_numbers.font_size = label_height * 0.85

        self.char_button.size = size
        if not self.isSelect:
            self.support_button.size = size

    def on_pos(self, instance, pos):
        if not self.initalized:
            return False
        self.background.pos = pos
        self.char_image.pos = pos[0] + self.preview_wgap, pos[1] + self.size[1] - self.char_image.height - self.preview_hgap - (60 * self.size[1] / self.preview_height)
        if self.support is not None:
            self.support_image.pos = self.preview_wgap, self.size[1] - self.image_height - self.preview_hgap
        self.overlay.pos = pos

        count = 0
        star_width = (self.size[1] * 62 / self.preview_height) / 1.5
        star_size = star_width, star_width
        star_columns = 5
        star_width_overlap = .75
        star_height_overlap = .5
        stars_width = star_size[0] * star_columns * star_width_overlap
        star_start = self.size[0] / 2 - stars_width / 2, self.size[1] - self.preview_hgap - star_size[1]
        for level in self.character.ranks:
            star_row = int(count / star_columns)
            star_column = count % star_columns

            star_x = star_column * star_size[0] * star_width_overlap
            star_y = star_row * star_size[1] * star_height_overlap
            star_offset = (-15 * (star_row + 1)) + (30 * star_row)
            star_pos = pos[0] + star_x + star_start[0] + star_offset, pos[1] + self.size[1] - star_size[
                1] - star_y - self.preview_wgap
            self.stars[count].pos = star_pos
            count += 1
        if self.support is not None:
            diamond_top = 545 * self.size[1] / self.preview_height
            diamond_center = 426.5 * self.size[1] / self.preview_height
            diamond_bottom = 309 * self.size[1] / self.preview_height

            diamond_left = 7 * self.size[0] / self.preview_width
            diamond_middle = self.size[0] / 2

            space = (diamond_middle - diamond_left) / 5, (diamond_center - diamond_bottom) / 5

            for level in self.support.ranks:
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

        label_height = (self.size[1] * 120 / self.preview_height) / 4
        image_width = label_height
        image_height = image_width
        label_width = (self.size[0] - self.preview_wgap * 2 - image_width * 1.75) / 2
        text_color = (.796, .773, .678, 1)

        image_wstart = pos[0] + self.preview_wgap + image_width / 2
        image_hstart = pos[1] + (self.size[1] * 310 / self.preview_height)

        label_wstart = image_wstart + image_width
        label_hstart = pos[1] + (self.size[1] * 310 / self.preview_height)

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
        self.label_numbers.pos = (label_wstart + label_width, label_hstart - label_height*10)

        self.char_button.pos = pos
        if not self.isSelect:
            self.support_button.pos = pos

    def updateStars(self, character, support):
        # print("updating preview stars")
        count = 0
        for level in character.ranks:
            # print(str(self.stars[count].opacity))
            if level.unlocked:
                if not level.broken:
                    if self.stars[count].source != '../res/screens/stats/star.png':
                        self.stars[count].source = '../res/screens/stats/star.png'
                    self.stars[count].opacity = 1
                else:
                    if self.stars[count].source != '../res/screens/stats/rankbrk.png':
                        self.stars[count].source = '../res/screens/stats/rankbrk.png'
                    self.stars[count].opacity = 1
            count += 1
        if support is not None:
            for level in support.ranks:
                # print(str(self.stars[count].opacity))
                if level.unlocked:
                    if not level.broken:
                        if self.stars[count].source != '../res/screens/stats/star.png':
                            self.stars[count].source = '../res/screens/stats/star.png'
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
                    if touch.is_double_tap:
                        self.main_screen.display_screen(self.character.get_attr_screen(), True, True)
                        return True
                    if not self.isSelect:
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
                    if touch.is_double_tap:
                        self.main_screen.display_screen(self.support.get_attr_screen(), True, True)
                        return True
                    if not self.isSelect:
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
                    self.main_screen.display_screen(self.support.get_attr_screen(), True, True)
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
                    if self.isSelect:
                        if self.isSupport:
                            self.preview.set_char_screen(True, self.preview.char, self.character)
                        else:
                            self.preview.set_char_screen(True, self.character, None)
                        self.main_screen.display_screen(None, False, False)
                    else:
                        self.preview.show_select_screen(self, False)
                    return True
                elif touch.button == 'right':
                    self.main_screen.display_screen(self.character.get_attr_screen(), True, True)
                    return True
            return False







