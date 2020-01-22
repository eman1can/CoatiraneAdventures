from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.input.providers.wm_touch import WM_MotionEvent

from src.modules.HTButton import HTButton


class FilledCharacterPreviewScreen(Screen):
    initialized = BooleanProperty(False)

    def __init__(self, main_screen, preview, is_support, character, support, **kwargs):
        pos = (0, 0)  # Posistion gets reset
        super().__init__(size_hint=(None, None), **kwargs)
        self.name = character.get_id()
        if support is not None:
            self.name += "_" + support.get_id()

        self._size = (0, 0)

        self.preview = FilledCharacterPreview(main_screen=main_screen, preview=preview, is_support=is_support, is_select=False, has_screen=True, character=character, support=support)

        self.add_widget(self.preview)
        self.initialized = True

    def update_lock(self, locked):
        self.preview.update_lock(locked)

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

    locked = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(size_hint=(None, None), **kwargs)

        self._size = (0, 0)
        self._pos = (0, 0)

        self.background = Image(source="../res/screens/stats/preview_background.png", allow_stretch=True)
        self.char_image = self.character.get_slide_image(self.new_image_instance)
        self.slide_image_loaded = True

        self.type_flag = Image(source="../res/screens/stats/" + str(self.character.get_type()).lower() + "_flag.png", size_hint=(None, None), allow_stretch=True)
        self.type_flag_label = Label(text=str(self.character.get_type()) + " Type", size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')

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
        if self.is_select:
            self.add_widget(self.type_flag)
            self.add_widget(self.type_flag_label)
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

        self.phyatk_image = Image(source='../res/screens/stats/PhysicalAttack.png', allow_stretch=True, size_hint=(None, None))
        self.magatk_image = Image(source='../res/screens/stats/MagicalAttack.png', allow_stretch=True, size_hint=(None, None))
        self.health_image = Image(source='../res/screens/stats/Health.png', allow_stretch=True, size_hint=(None, None))
        self.mana_image = Image(source='../res/screens/stats/Mana.png', allow_stretch=True, size_hint=(None, None))
        self.defense_image = Image(source='../res/screens/stats/Defense.png', allow_stretch=True, size_hint=(None, None))

        self.strength_image = Image(source='../res/screens/stats/Str.png', allow_stretch=True, size_hint=(None, None))
        self.magic_image = Image(source='../res/screens/stats/Mag.png', allow_stretch=True, size_hint=(None, None))
        self.endurance_image = Image(source='../res/screens/stats/End.png', allow_stretch=True, size_hint=(None, None))
        self.dexterity_image = Image(source='../res/screens/stats/Dex.png', allow_stretch=True, size_hint=(None, None))
        self.agility_image = Image(source='../res/screens/stats/Agi.png', allow_stretch=True, size_hint=(None, None))

        number_phyatk = self.character.get_phyatk()
        number_magatk = self.character.get_magatk()
        number_health = self.character.get_health()
        number_mana = self.character.get_mana()
        number_defense = self.character.get_defense()
        number_strength = self.character.get_strength()
        number_magic = self.character.get_magic()
        number_endurance = self.character.get_endurance()
        number_dexterity = self.character.get_dexterity()
        number_agility = self.character.get_agility()
        if self.support is not None:
            number_phyatk += self.support.get_phyatk()
            number_magatk += self.support.get_magatk()
            number_health += self.support.get_health()
            number_mana += self.support.get_mana()
            number_defense += self.support.get_defense()
            number_strength += self.support.get_strength()
            number_magic += self.support.get_magic()
            number_endurance += self.support.get_endurance()
            number_dexterity += self.support.get_dexterity()
            number_agility += self.support.get_agility()

        self.phyatk_label_word = Label(text='Phy. Atk', color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.phyatk_label_number = Label(text=str(number_phyatk), color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.magatk_label_word = Label(text='Mag. Atk', color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.magatk_label_number = Label(text=str(number_magatk), color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.health_label_word = Label(text='Health', color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.health_label_number = Label(text=str(number_health), color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.mana_label_word = Label(text='Mana', color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.mana_label_number = Label(text=str(number_mana), color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.defense_label_word = Label(text='Defense', color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.defense_label_number = Label(text=str(number_defense), color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))

        self.strength_label_word = Label(text='trength', color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.strength_label_number = Label(text=str(number_strength), color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.magic_label_word = Label(text='agic', color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.magic_label_number = Label(text=str(number_magic), color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.endurance_label_word = Label(text='ndurance', color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.endurance_label_number = Label(text=str(number_endurance), color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.dexterity_label_word = Label(text='exterity', color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.dexterity_label_number = Label(text=str(number_dexterity), color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.agility_label_word = Label(text='gility', color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.agility_label_number = Label(text=str(number_agility), color=text_color, font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))

        self.lock = Image(source="../res/screens/stats/lock.png", allow_stretch=True, size_hint=(None, None), opacity=0)

        self.add_widget(self.phyatk_image)
        self.add_widget(self.magatk_image)
        self.add_widget(self.health_image)
        self.add_widget(self.mana_image)
        self.add_widget(self.defense_image)

        self.add_widget(self.strength_image)
        self.add_widget(self.magic_image)
        self.add_widget(self.endurance_image)
        self.add_widget(self.agility_image)
        self.add_widget(self.dexterity_image)

        self.add_widget(self.phyatk_label_word)
        self.add_widget(self.phyatk_label_number)
        self.add_widget(self.magatk_label_word)
        self.add_widget(self.magatk_label_number)
        self.add_widget(self.health_label_word)
        self.add_widget(self.health_label_number)
        self.add_widget(self.mana_label_word)
        self.add_widget(self.mana_label_number)
        self.add_widget(self.defense_label_word)
        self.add_widget(self.defense_label_number)

        self.add_widget(self.strength_label_word)
        self.add_widget(self.strength_label_number)
        self.add_widget(self.magic_label_word)
        self.add_widget(self.magic_label_number)
        self.add_widget(self.endurance_label_word)
        self.add_widget(self.endurance_label_number)
        self.add_widget(self.dexterity_label_word)
        self.add_widget(self.dexterity_label_number)
        self.add_widget(self.agility_label_word)
        self.add_widget(self.agility_label_number)

        self.add_widget(self.lock)
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

        self.type_flag.size = self.width * 0.75, self.width * 0.75 * 150 / 619
        self.type_flag_label.size = self.type_flag.width * 0.83, self.type_flag.height * 0.85
        self.type_flag_label.font_size = self.type_flag.size[1] * 0.75

        star_size_large = (size[1] * 62 / 935) / 1.5, (size[1] * 62 / 935) / 1.5
        star_size_small = (size[1] * 120 / 935) / 4, (size[1] * 120 / 935) / 4
        for star in self.stars:
            if star.type:
                star.size = star_size_large
            else:
                star.size = star_size_small

        box_height = self.height * 303 / 935
        row_height = box_height / 10
        image_size = row_height, row_height

        self.phyatk_image.size    = image_size
        self.magatk_image.size    = image_size
        self.health_image.size    = image_size
        self.mana_image.size      = image_size
        self.defense_image.size   = image_size
        self.strength_image.size  = image_size
        self.magic_image.size     = image_size
        self.endurance_image.size = image_size
        self.dexterity_image.size = image_size
        self.agility_image.size   = image_size

        self.phyatk_label_word.font_size  = row_height
        self.magatk_label_word.font_size  = row_height
        self.health_label_word.font_size  = row_height
        self.mana_label_word.font_size    = row_height
        self.defense_label_word.font_size = row_height
        self.phyatk_label_word.texture_update()
        self.magatk_label_word.texture_update()
        self.health_label_word.texture_update()
        self.mana_label_word.texture_update()
        self.defense_label_word.texture_update()
        self.phyatk_label_word.size  = self.phyatk_label_word.texture_size[0], row_height
        self.magatk_label_word.size  = self.magatk_label_word.texture_size[0], row_height
        self.health_label_word.size  = self.health_label_word.texture_size[0], row_height
        self.mana_label_word.size    = self.mana_label_word.texture_size[0], row_height
        self.defense_label_word.size = self.defense_label_word.texture_size[0], row_height

        self.phyatk_label_number.font_size  = row_height
        self.magatk_label_number.font_size  = row_height
        self.health_label_number.font_size  = row_height
        self.mana_label_number.font_size    = row_height
        self.defense_label_number.font_size = row_height
        self.phyatk_label_number.texture_update()
        self.magatk_label_number.texture_update()
        self.health_label_number.texture_update()
        self.mana_label_number.texture_update()
        self.defense_label_number.texture_update()
        self.phyatk_label_number.size  = self.phyatk_label_number.texture_size[0], row_height
        self.magatk_label_number.size  = self.magatk_label_number.texture_size[0], row_height
        self.health_label_number.size  = self.health_label_number.texture_size[0], row_height
        self.mana_label_number.size    = self.mana_label_number.texture_size[0], row_height
        self.defense_label_number.size = self.defense_label_number.texture_size[0], row_height

        self.strength_label_word.font_size  = row_height
        self.magic_label_word.font_size     = row_height
        self.endurance_label_word.font_size = row_height
        self.dexterity_label_word.font_size = row_height
        self.agility_label_word.font_size   = row_height
        self.strength_label_word.texture_update()
        self.magic_label_word.texture_update()
        self.endurance_label_word.texture_update()
        self.dexterity_label_word.texture_update()
        self.agility_label_word.texture_update()
        self.strength_label_word.size  = self.strength_label_word.texture_size[0], row_height
        self.magic_label_word.size     = self.magic_label_word.texture_size[0], row_height
        self.endurance_label_word.size = self.endurance_label_word.texture_size[0], row_height
        self.dexterity_label_word.size = self.dexterity_label_word.texture_size[0], row_height
        self.agility_label_word.size   = self.agility_label_word.texture_size[0], row_height

        self.strength_label_number.font_size  = row_height
        self.magic_label_number.font_size     = row_height
        self.endurance_label_number.font_size = row_height
        self.dexterity_label_number.font_size = row_height
        self.agility_label_number.font_size   = row_height
        self.strength_label_number.texture_update()
        self.magic_label_number.texture_update()
        self.endurance_label_number.texture_update()
        self.dexterity_label_number.texture_update()
        self.agility_label_number.texture_update()
        self.strength_label_number.size  = self.strength_label_number.texture_size[0], row_height
        self.magic_label_number.size     = self.magic_label_number.texture_size[0], row_height
        self.endurance_label_number.size = self.endurance_label_number.texture_size[0], row_height
        self.dexterity_label_number.size = self.dexterity_label_number.texture_size[0], row_height
        self.agility_label_number.size   = self.agility_label_number.texture_size[0], row_height

        self.lock.size = self.width * 0.3, self.width * 0.3
        self.lock.pos = self.x + self.width - self.width * 0.3, self.y + self.height - self.width * 0.3

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

        self.type_flag.pos = self.x + self.preview_wgap * 0.6, self.y + self.height - self.preview_hgap - (600 * self.height / 935)
        self.type_flag_label.pos = self.x + self.preview_wgap * 0.6, self.y + self.height - self.preview_hgap - (600 * self.height / 935) + self.type_flag.height * 0.15

        star_size = (self.height * 62 / 935) / 1.5, (self.height * 62 / 935) / 1.5
        star_columns = 5
        star_width_overlap = .75
        star_height_overlap = .5
        stars_width = star_size[0] * star_columns * star_width_overlap
        star_start = self.width / 2 - stars_width / 2, self.height - self.preview_hgap - star_size[1]

        if self.support is not None:
            diamond_top = 545 * self.height / 935
            diamond_center = 426.5 * self.height / 935
            diamond_bottom = 309 * self.height / 935

            diamond_left = 7 * self.width / 250
            diamond_middle = self.width / 2
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
                    star_pos = self.width / 2 - star_size[0] * 1.1 - space[0] * column, diamond_bottom - star_size[1] * 1.1 + space[1] * (row + 1)
                elif scount < 6:
                    column = row = (count - 13) % 5 + 1
                    star_pos = self.width / 2 + star_size[0] * .1 + space[0] * column, diamond_bottom - star_size[1] * 1.1 + space[1] * (row + 1)
                elif scount < 8:
                    column = row = (count - 15) % 5
                    star_pos = self.width / 2 - star_size[0] * 1.4 - space[0] * column, diamond_top - star_size[1] * .1 - space[1] * (row + 1)
                else:
                    column = row = (count - 17) % 5
                    star_pos = self.size[0] / 2 + star_size[0] * .4 + space[0] * column, diamond_top - star_size[1] * .1 - space[1] * (row + 1)
                self.stars[count].pos = star_pos
            count += 1

        box_height = self.height * 303 / 935
        box_width = self.width - self.preview_wgap * 2
        row_height = box_height / 10
        image_size = row_height, row_height
        image_x = self.x + image_size[0] * 0.5 + self.preview_wgap
        image_y = self.y + self.preview_hgap
        label_xs = image_x + image_size[0] * 1.5
        label_xl = image_x + image_size[0]
        label_xr = self.x + box_width - self.preview_wgap
        label_y = image_y

        self.phyatk_image.pos    = image_x, image_y + row_height * 9
        self.magatk_image.pos    = image_x, image_y + row_height * 8
        self.health_image.pos    = image_x, image_y + row_height * 7
        self.mana_image.pos      = image_x, image_y + row_height * 6
        self.defense_image.pos   = image_x, image_y + row_height * 5
        self.strength_image.pos  = image_x, image_y + row_height * 4
        self.magic_image.pos     = image_x, image_y + row_height * 3
        self.endurance_image.pos = image_x, image_y + row_height * 2
        self.dexterity_image.pos = image_x, image_y + row_height
        self.agility_image.pos   = image_x, image_y

        self.phyatk_label_word.pos    = label_xs, label_y + row_height * 9
        self.magatk_label_word.pos    = label_xs, label_y + row_height * 8
        self.health_label_word.pos    = label_xs, label_y + row_height * 7
        self.mana_label_word.pos      = label_xs, label_y + row_height * 6
        self.defense_label_word.pos   = label_xs, label_y + row_height * 5
        self.strength_label_word.pos  = label_xl, label_y + row_height * 4
        self.magic_label_word.pos     = label_xl, label_y + row_height * 3
        self.endurance_label_word.pos = label_xl, label_y + row_height * 2
        self.dexterity_label_word.pos = label_xl, label_y + row_height
        self.agility_label_word.pos   = label_xl, label_y

        self.phyatk_label_number.pos    = label_xr - self.phyatk_label_number.width, label_y + row_height * 9
        self.magatk_label_number.pos    = label_xr - self.magatk_label_number.width, label_y + row_height * 8
        self.health_label_number.pos    = label_xr - self.health_label_number.width, label_y + row_height * 7
        self.mana_label_number.pos      = label_xr - self.mana_label_number.width, label_y + row_height * 6
        self.defense_label_number.pos   = label_xr - self.defense_label_number.width, label_y + row_height * 5
        self.strength_label_number.pos  = label_xr - self.strength_label_number.width, label_y + row_height * 4
        self.magic_label_number.pos     = label_xr - self.magic_label_number.width, label_y + row_height * 3
        self.endurance_label_number.pos = label_xr - self.endurance_label_number.width, label_y + row_height * 2
        self.dexterity_label_number.pos = label_xr - self.dexterity_label_number.width, label_y + row_height
        self.agility_label_number.pos   = label_xr - self.agility_label_number.width, label_y

        self.lock.pos = self.x + self.width - self.width * 0.3, self.y + self.height - self.width * 0.3

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

    def update_lock(self, locked):
        self.locked = locked
        if self.locked:
            self.lock.opacity = 1
        else:
            self.lock.opacity = 0

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
                    screen = self.support.get_attr_screen()
                    screen.main_screen = self.main_screen
                    screen.preview = self.preview
                    screen.reload()
                    self.main_screen.display_screen(screen, True, True)
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
