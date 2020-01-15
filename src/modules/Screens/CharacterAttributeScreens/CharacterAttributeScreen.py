from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.app import App
import random

from src.entitites.Character.Scale import Scale
from src.modules.CustomHoverableButton import CustomHoverableButton


class CharacterAttributeScreen(Screen):
    def __init__(self, main_screen, preview, size, pos, char, name):
        self.main_screen = main_screen
        self.preview = preview
        self.initalized = False
        super(CharacterAttributeScreen, self).__init__(name=name, size=size, pos=pos)

        back_button_size = (size[0] * .05, size[0] * .05)
        back_button_pos = 0, size[1] - back_button_size[1]
        self.back_button = CustomHoverableButton(size=back_button_size, pos=back_button_pos, path='../res/screens/buttons/back', on_touch_down=self.on_back_press, background_disabled_normal=True)

        # Overlays & Backgrounds
        self.background = Image(source="../res/screens/backgrounds/charattributebg.png", size=size, pos=(0, 0), keep_ratio=False, allow_stretch=True)

        self.char_image = char.get_full_image(False)
        self.char_image.size = (self.char_image.image_ratio * size[1], size[1])
        self.char_image.pos = (-(size[0] - self.char_image.image_ratio * size[1]) / 2, 0)

        overlay_size = size[1] * .9 * 620 / 610, size[1] * .9
        overlay_pos = size[0] - size[1] * .05 - overlay_size[0], size[1] * .05
        self.overlay_background = Image(source="../res/screens/stats/stat_background.png", size=overlay_size, pos=overlay_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.overlay = Image(source="../res/screens/stats/stat_background_overlay.png", size=overlay_size, pos=overlay_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        flag_size = overlay_size[0] * 110 / 620, overlay_size[1] * 35 / 610
        flag_pos = overlay_pos[0] - 2, overlay_pos[1] + overlay_size[1] - flag_size[1] + 2
        self.flag = Image(source="../res/screens/stats/flag.png", size=flag_size, pos=flag_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        if char.is_support():
            text = "Supporter"
        else:
            text = "Adventurer"
        self.flag_label = Label(text=text, font_size=flag_size[1] * 0.7, size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.flag_label._label.refresh()
        self.flag_label.size = self.flag_label._label.texture.size
        self.flag_label.pos = flag_pos[0] + flag_size[0] - (flag_size[0] * 0.9 - self.flag_label.width) / 2 - self.flag_label.width, flag_pos[1]

        type_size = overlay_size[0] * 160 / 620, overlay_size[1] * 35 / 610
        type_pos = overlay_pos[0] + overlay_size[0] + 2 - type_size[0], overlay_pos[1] + overlay_size[1] - type_size[1] + 2
        self.type = Image(source="../res/screens/stats/type_" + str(char.get_type())[0].lower() + ".png", size=type_size, pos=type_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.type_label = Label(text=str(char.get_type()) + " Type", font_size=type_size[1] * 0.7, size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.type_label._label.refresh()
        self.type_label.size = self.type_label._label.texture.size
        self.type_label.pos = type_pos[0] + (type_size[0] * 0.9375 - self.type_label.width) / 2, type_pos[1]

        # Stars
        count = 0
        self.stars = []
        addx = False
        for x in char.ranks:
            # print("Rank: " + str(x))
            xpos = 50
            if addx:
                xpos += 25
            if x.unlocked:
                if not x.broken:
                    self.stars.append(Image(source="../res/screens/stats/star.png", pos=(xpos, 50 + (count * 75)), size=(140, 140),
                                            size_hint=(None, None), opacity=1))
                else:
                    self.stars.append(Image(source="../res/screens/stats/rankbrk.png", pos=(xpos, 50 + (count * 75)), size=(140, 140),
                                            size_hint=(None, None), opacity=1))
            else:
                self.stars.append(Image(source="../res/screens/stats/star.png", pos=(xpos, 50 + (count * 75)), size=(140, 140), size_hint=(None, None), opacity=0))
            count += 1
            if addx:
                xpos -= 25
            addx = not addx

        # Title Names & Bar
        self.display_name_label = Label(text=str(char.get_display_name()), font_size=size[0] * .025, size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')
        self.display_name_label._label.refresh()
        self.display_name_label.size = self.display_name_label._label.texture.size
        self.display_name_label.pos = (overlay_pos[0] + (overlay_size[0] - self.display_name_label.width) / 2), overlay_pos[1] + overlay_size[1] * .975 - self.display_name_label.height

        self.name_label = Label(text=str(char.get_name()), font_size=size[0] * .05, size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')
        self.name_label._label.refresh()
        self.name_label.size = self.name_label._label.texture.size
        self.name_label.pos = (overlay_pos[0] + (overlay_size[0] - self.name_label.width) / 2), overlay_pos[1] + overlay_size[1] * .95 - self.display_name_label.height - self.name_label.height

        self.overlay_bar = Image(source="../res/screens/stats/overlay_bar.png", size=(overlay_size[0] * .6, overlay_size[1] * 10 / 610 + 5), pos=(overlay_pos[0] + overlay_size[0] * .2, overlay_pos[1] + overlay_size[1] * .93 - self.display_name_label.height - self.name_label.height), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.total_label = Label(text="Total Stats", font_size=size[0] * .01625, size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')
        self.total_label._label.refresh()
        self.total_label.size = self.total_label._label.texture.size
        self.total_label.pos = (overlay_pos[0] + overlay_size[0] * 0.0625 + (overlay_size[0] * .25 - self.total_label.width) / 2), overlay_pos[1] + overlay_size[1] * .92 - self.display_name_label.height - self.name_label.height - self.total_label.height

        self.total_abilities = Label(text="Total Abilities", font_size=size[0] * .01625, size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')
        self.total_abilities._label.refresh()
        self.total_abilities.size = self.total_abilities._label.texture.size
        self.total_abilities.pos = (overlay_pos[0] + (overlay_size[0] - self.total_abilities.width) / 2), overlay_pos[1] + overlay_size[1] * .92 - self.display_name_label.height - self.name_label.height - self.total_abilities.height

        self.rank_abilities = Label(text="Rank Abilities", font_size=size[0] * .01625, size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')
        self.rank_abilities._label.refresh()
        self.rank_abilities.size = self.rank_abilities._label.texture.size
        self.rank_abilities.pos = (overlay_pos[0] + overlay_size[0] * 0.6875 + (overlay_size[0] * .25 - self.rank_abilities.width) / 2), overlay_pos[1] + overlay_size[1] * .92 - self.display_name_label.height - self.name_label.height - self.rank_abilities.height

        # Main Label Variables
        stat_bar_size = overlay_size[0] * 0.1875, overlay_size[0] * 0.1875 * 25 / 135
        stat_image_size = stat_bar_size[1] * .9, stat_bar_size[1] * .9
        stat_bar_start = overlay_pos[0] + overlay_size[0] * 0.0625
        start = overlay_pos[1] + overlay_size[1] * .9125 - self.display_name_label.height - self.name_label.height - self.total_label.height
        spacer = stat_bar_size[1] / 2

        # Health
        self.stat_bar_health = Image(source="../res/screens/stats/stat_bar.png", size=stat_bar_size, pos=(stat_bar_start, start - stat_bar_size[1]), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.stat_image_health = Image(source="../res/screens/stats/Health.png", size=stat_image_size, pos=(self.stat_bar_health.x + stat_bar_size[0] * 0.05, self.stat_bar_health.y + stat_bar_size[1] * 0.05), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.stat_label_health = Label(text="Health", font_size=stat_image_size[1], size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_health._label.refresh()
        self.stat_label_health.size = self.stat_label_health._label.texture.size
        self.stat_label_health.pos = self.stat_image_health.x + stat_image_size[0] + (stat_bar_size[0] * 0.95 - stat_image_size[0] - self.stat_label_health.width) / 2, self.stat_bar_health.y + (stat_bar_size[1] - self.stat_label_health.height) / 2

        self.stat_label_health_number = Label(text=str(char.get_health()), font_size=stat_image_size[1], size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_health_number._label.refresh()
        self.stat_label_health_number.size = self.stat_label_health_number._label.texture.size
        self.stat_label_health_number.pos = self.stat_bar_health.x + overlay_size[0] * 0.25 - self.stat_label_health_number.width, self.stat_bar_health.y + (stat_bar_size[1] - self.stat_label_health_number.height) / 2

        # Mana
        self.stat_bar_mana = Image(source="../res/screens/stats/stat_bar.png", size=stat_bar_size, pos=(stat_bar_start, start - stat_bar_size[1] * 2 - spacer), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.stat_image_mana = Image(source="../res/screens/stats/Mana.png", size=stat_image_size, pos=(self.stat_bar_mana.x + stat_bar_size[0] * 0.05, self.stat_bar_mana.y + stat_bar_size[1] * 0.05), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.stat_label_mana = Label(text="Mana", font_size=stat_image_size[1], size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_mana._label.refresh()
        self.stat_label_mana.size = self.stat_label_mana._label.texture.size
        self.stat_label_mana.pos = self.stat_image_mana.x + stat_image_size[0] + (stat_bar_size[0] * 0.95 - stat_image_size[0] - self.stat_label_mana.width) / 2, self.stat_bar_mana.y + (stat_bar_size[1] - self.stat_label_mana.height) / 2

        self.stat_label_mana_number = Label(text=str(char.get_mana()), font_size=stat_image_size[1], size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_mana_number._label.refresh()
        self.stat_label_mana_number.size = self.stat_label_mana_number._label.texture.size
        self.stat_label_mana_number.pos = self.stat_bar_mana.x + overlay_size[0] * 0.25 - self.stat_label_mana_number.width, self.stat_bar_mana.y + (stat_bar_size[1] - self.stat_label_mana_number.height) / 2

        # Phy Attack
        self.stat_bar_phyattack = Image(source="../res/screens/stats/stat_bar.png", size=stat_bar_size, pos=(stat_bar_start, start - stat_bar_size[1] * 3 - spacer * 2), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.stat_image_phyattack = Image(source="../res/screens/stats/PhysicalAttack.png", size=stat_image_size, pos=(self.stat_bar_phyattack.x + stat_bar_size[0] * 0.05, self.stat_bar_phyattack.y + stat_bar_size[1] * 0.05), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.stat_label_phyattack = Label(text="P. Attack", font_size=stat_image_size[1], size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_phyattack._label.refresh()
        self.stat_label_phyattack.size = self.stat_label_phyattack._label.texture.size
        self.stat_label_phyattack.pos = self.stat_image_phyattack.x + stat_image_size[0] + (stat_bar_size[0] * 0.95 - stat_image_size[0] - self.stat_label_phyattack.width) / 2, self.stat_bar_phyattack.y + (stat_bar_size[1] - self.stat_label_phyattack.height) / 2

        self.stat_label_phyattack_number = Label(text=str(char.get_phyatk()), font_size=stat_image_size[1], size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_phyattack_number._label.refresh()
        self.stat_label_phyattack_number.size = self.stat_label_phyattack_number._label.texture.size
        self.stat_label_phyattack_number.pos = self.stat_bar_phyattack.x + overlay_size[0] * 0.25 - self.stat_label_phyattack_number.width, self.stat_bar_phyattack.y + (stat_bar_size[1] - self.stat_label_phyattack_number.height) / 2

        # Mag Attack
        self.stat_bar_magattack = Image(source="../res/screens/stats/stat_bar.png", size=stat_bar_size, pos=(stat_bar_start, start - stat_bar_size[1] * 4 - spacer * 3), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.stat_image_magattack = Image(source="../res/screens/stats/MagicalAttack.png", size=stat_image_size, pos=(self.stat_bar_magattack.x + stat_bar_size[0] * 0.05, self.stat_bar_magattack.y + stat_bar_size[1] * 0.05), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.stat_label_magattack = Label(text="M. Attack", font_size=stat_image_size[1], size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_magattack._label.refresh()
        self.stat_label_magattack.size = self.stat_label_magattack._label.texture.size
        self.stat_label_magattack.pos = self.stat_image_magattack.x + stat_image_size[0] + (stat_bar_size[0] * 0.95 - stat_image_size[0] - self.stat_label_magattack.width) / 2, self.stat_bar_magattack.y + (stat_bar_size[1] - self.stat_label_magattack.height) / 2

        self.stat_label_magattack_number = Label(text=str(char.get_magatk()), font_size=stat_image_size[1], size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_magattack_number._label.refresh()
        self.stat_label_magattack_number.size = self.stat_label_magattack_number._label.texture.size
        self.stat_label_magattack_number.pos = self.stat_bar_magattack.x + overlay_size[0] * 0.25 - self.stat_label_magattack_number.width, self.stat_bar_magattack.y + (stat_bar_size[1] - self.stat_label_magattack_number.height) / 2

        # Defense
        self.stat_bar_defense = Image(source="../res/screens/stats/stat_bar.png", size=stat_bar_size, pos=(stat_bar_start, start - stat_bar_size[1] * 5 - spacer * 4), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.stat_image_defense = Image(source="../res/screens/stats/Defense.png", size=stat_image_size, pos=(self.stat_bar_defense.x + stat_bar_size[0] * 0.05, self.stat_bar_defense.y + stat_bar_size[1] * 0.05), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.stat_label_defense = Label(text="Defense", font_size=stat_image_size[1], size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_defense._label.refresh()
        self.stat_label_defense.size = self.stat_label_defense._label.texture.size
        self.stat_label_defense.pos = self.stat_image_defense.x + stat_image_size[0] + (stat_bar_size[0] * 0.95 - stat_image_size[0] - self.stat_label_defense.width) / 2, self.stat_bar_defense.y + (stat_bar_size[1] - self.stat_label_defense.height) / 2

        self.stat_label_defense_number = Label(text=str(char.get_defense()), font_size=stat_image_size[1], size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_defense_number._label.refresh()
        self.stat_label_defense_number.size = self.stat_label_defense_number._label.texture.size
        self.stat_label_defense_number.pos = self.stat_bar_defense.x + overlay_size[0] * 0.25 - self.stat_label_defense_number.width, self.stat_bar_defense.y + (stat_bar_size[1] - self.stat_label_defense_number.height) / 2

        # Rank Total Stats
        rank_overlay_size = overlay_size[0] * 0.25, start - self.stat_bar_defense.y
        rank_overlay_pos = overlay_pos[0] + overlay_size[0] * 0.375, start - rank_overlay_size[1]
        height = rank_overlay_size[1] / 6
        rank_image_size = rank_overlay_size[0] / 3, height * .85
        self.rank_total_overlay = Image(source="../res/screens/stats/ability_overlay.png", size=rank_overlay_size, pos=rank_overlay_pos, size_hint=(None, None), keep_ratio=False, allow_stretch=True)
        rank_stat_color = 0, 0, 0, 1
        rank_stat_font_size = stat_image_size[1] * 1.1

        # Strength
        self.rank_total_strength_label = Label(text="Strength", font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_strength_label._label.refresh()
        self.rank_total_strength_label.size = self.rank_total_strength_label._label.texture.size
        self.rank_total_strength_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 4.5

        self.rank_total_strength_image = Image(source=char.get_strength_rank(), size=rank_image_size, pos=(rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 4.5), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.rank_total_strength_label_number = Label(text=str(char.get_strength()), font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_strength_label_number._label.refresh()
        self.rank_total_strength_label_number.size = self.rank_total_strength_label_number._label.texture.size
        self.rank_total_strength_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_total_strength_label_number.width, rank_overlay_pos[1] + height * 4.5

        # Magic
        self.rank_total_magic_label = Label(text="Magic", font_size=stat_image_size[1] * 1.1, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_magic_label._label.refresh()
        self.rank_total_magic_label.size = self.rank_total_magic_label._label.texture.size
        self.rank_total_magic_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 3.5

        self.rank_total_magic_image = Image(source=char.get_magic_rank(), size=rank_image_size, pos=(rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 3.5), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.rank_total_magic_label_number = Label(text=str(char.get_magic()), font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_magic_label_number._label.refresh()
        self.rank_total_magic_label_number.size = self.rank_total_magic_label_number._label.texture.size
        self.rank_total_magic_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_total_magic_label_number.width, rank_overlay_pos[1] + height * 3.5

        # Endurance
        self.rank_total_endurance_label = Label(text="Endurance", font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_endurance_label._label.refresh()
        self.rank_total_endurance_label.size = self.rank_total_endurance_label._label.texture.size
        self.rank_total_endurance_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 2.5

        self.rank_total_endurance_image = Image(source=char.get_endurance_rank(), size=rank_image_size, pos=(rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 2.5), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.rank_total_endurance_label_number = Label(text=str(char.get_endurance()), font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_endurance_label_number._label.refresh()
        self.rank_total_endurance_label_number.size = self.rank_total_endurance_label_number._label.texture.size
        self.rank_total_endurance_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_total_endurance_label_number.width, rank_overlay_pos[1] + height * 2.5

        # Dexterity
        self.rank_total_dexterity_label = Label(text="Dexterity", font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_dexterity_label._label.refresh()
        self.rank_total_dexterity_label.size = self.rank_total_dexterity_label._label.texture.size
        self.rank_total_dexterity_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 1.5

        self.rank_total_dexterity_image = Image(source=char.get_dexterity_rank(), size=rank_image_size, pos=(rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 1.5), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.rank_total_dexterity_label_number = Label(text=str(char.get_dexterity()), font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_dexterity_label_number._label.refresh()
        self.rank_total_dexterity_label_number.size = self.rank_total_dexterity_label_number._label.texture.size
        self.rank_total_dexterity_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_total_dexterity_label_number.width, rank_overlay_pos[1] + height * 1.5

        # Agility
        self.rank_total_agility_label = Label(text="Agility", font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_agility_label._label.refresh()
        self.rank_total_agility_label.size = self.rank_total_agility_label._label.texture.size
        self.rank_total_agility_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 0.5

        self.rank_total_agility_image = Image(source=char.get_agility_rank(), size=rank_image_size, pos=(rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 0.5), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.rank_total_agility_label_number = Label(text=str(char.get_agility()), font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_agility_label_number._label.refresh()
        self.rank_total_agility_label_number.size = self.rank_total_agility_label_number._label.texture.size
        self.rank_total_agility_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_total_agility_label_number.width, rank_overlay_pos[1] + height * 0.5

        # Current Rank Stats
        rank_overlay_pos = overlay_pos[0] + overlay_size[0] * 0.6875, start - rank_overlay_size[1]
        self.rank_current_overlay = Image(source="../res/screens/stats/ability_overlay.png", size=rank_overlay_size, pos=rank_overlay_pos, size_hint=(None, None), keep_ratio=False, allow_stretch=True)

        # Strength
        self.rank_current_strength_label = Label(text="Strength", font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_strength_label._label.refresh()
        self.rank_current_strength_label.size = self.rank_current_strength_label._label.texture.size
        self.rank_current_strength_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 4.5

        self.rank_current_strength_image = Image(source=char.get_strength_rank(char.get_current_rank()), size=rank_image_size, pos=(rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 4.5), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.rank_current_strength_label_number = Label(text=str(char.get_strength(char.get_current_rank())), font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_strength_label_number._label.refresh()
        self.rank_current_strength_label_number.size = self.rank_current_strength_label_number._label.texture.size
        self.rank_current_strength_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_current_strength_label_number.width, rank_overlay_pos[1] + height * 4.5

        # Magic
        self.rank_current_magic_label = Label(text="Magic", font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_magic_label._label.refresh()
        self.rank_current_magic_label.size = self.rank_current_magic_label._label.texture.size
        self.rank_current_magic_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 3.5

        self.rank_current_magic_image = Image(source=char.get_magic_rank(char.get_current_rank()), size=rank_image_size, pos=(rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 3.5), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.rank_current_magic_label_number = Label(text=str(char.get_magic(char.get_current_rank())), font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_magic_label_number._label.refresh()
        self.rank_current_magic_label_number.size = self.rank_current_magic_label_number._label.texture.size
        self.rank_current_magic_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_current_magic_label_number.width, rank_overlay_pos[1] + height * 3.5

        # Endurance
        self.rank_current_endurance_label = Label(text="Endurance", font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_endurance_label._label.refresh()
        self.rank_current_endurance_label.size = self.rank_current_endurance_label._label.texture.size
        self.rank_current_endurance_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 2.5

        self.rank_current_endurance_image = Image(source=char.get_endurance_rank(char.get_current_rank()), size=rank_image_size, pos=(rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 2.5), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.rank_current_endurance_label_number = Label(text=str(char.get_endurance(char.get_current_rank())), font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_endurance_label_number._label.refresh()
        self.rank_current_endurance_label_number.size = self.rank_current_endurance_label_number._label.texture.size
        self.rank_current_endurance_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_current_endurance_label_number.width, rank_overlay_pos[1] + height * 2.5

        # Dexterity
        self.rank_current_dexterity_label = Label(text="Dexterity", font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_dexterity_label._label.refresh()
        self.rank_current_dexterity_label.size = self.rank_current_dexterity_label._label.texture.size
        self.rank_current_dexterity_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 1.5

        self.rank_current_dexterity_image = Image(source=char.get_dexterity_rank(char.get_current_rank()), size=rank_image_size, pos=(rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 1.5), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.rank_current_dexterity_label_number = Label(text=str(char.get_dexterity(char.get_current_rank())), font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_dexterity_label_number._label.refresh()
        self.rank_current_dexterity_label_number.size = self.rank_current_dexterity_label_number._label.texture.size
        self.rank_current_dexterity_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_current_dexterity_label_number.width, rank_overlay_pos[1] + height * 1.5

        # Agility
        self.rank_current_agility_label = Label(text="Agility", font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_agility_label._label.refresh()
        self.rank_current_agility_label.size = self.rank_current_agility_label._label.texture.size
        self.rank_current_agility_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 0.5

        self.rank_current_agility_image = Image(source=char.get_agility_rank(char.get_current_rank()), size=rank_image_size, pos=(rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 0.5), size_hint=(None, None), keep_ratio=True, allow_stretch=True)

        self.rank_current_agility_label_number = Label(text=str(char.get_agility(char.get_current_rank())), font_size=rank_stat_font_size, size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_agility_label_number._label.refresh()
        self.rank_current_agility_label_number.size = self.rank_current_agility_label_number._label.texture.size
        self.rank_current_agility_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_current_agility_label_number.width, rank_overlay_pos[1] + height * 0.5

        # Equipment
        equipment_size = overlay_size[0] * 0.25, overlay_size[0] * 0.25 * 75 / 200
        spacer = (overlay_size[0] - equipment_size[0] * 3) / 4
        equipment_color = 0, 0, 0, 1
        equipment_font = '../res/fnt/Gabriola.ttf'
        equipment_font_size = equipment_size[1] * .30

        label_pos = overlay_pos[0] + spacer, overlay_pos[1] + overlay_size[1] * 0.025 + equipment_size[1]
        image_size = equipment_size[1] * 0.6, equipment_size[1] * 0.6
        image_pos = (overlay_pos[0] + spacer + equipment_size[0] - (equipment_size[1] * 0.6) - 4 *  equipment_size[1] / 75,  overlay_pos[1] + overlay_size[1] * 0.025 + equipment_size[1] * 2 - 4 * equipment_size[1] / 75 - equipment_size[1] * 0.6)

        # Helmet
        self.helmet = Image(source="../res/screens/stats/equipment.png", size=equipment_size, pos=(overlay_pos[0] + spacer, overlay_pos[1] + overlay_size[1] * 0.025 + equipment_size[1]), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.helmet_label = Label(text="Helmet", font_size=equipment_font_size, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
        self.helmet_label._label.refresh()
        self.helmet_label.size = self.helmet_label._label.texture.size
        self.helmet_label.pos = overlay_pos[0] + spacer + 4 * equipment_size[0] / 200, overlay_pos[1] + overlay_size[1] * 0.025 + equipment_size[1] * 2 - self.helmet_label.height - 4 * equipment_size[1] / 75
        if char.get_equipment().helmet is not None:
            self.helmet_label_equip = Label(text=char.get_equipment().helmet.get_name(), font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.helmet_label_equip.size = equipment_size[0] * 0.75, equipment_size[1] * 0.75
            self.helmet_label_equip.pos = label_pos
            self.helmet_image_equip = Image(source="../res/items/equipment/" + char.get_equipment().helmet.get_id() + ".png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True)
            self.helmet_equipped = char.get_equipment().helmet
        else:
            self.helmet_equipped = None
            self.helmet_image_equip = Image(source="../res/items/equipment/empty.png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True, opacity=0)
            self.helmet_label_equip = Label(text="Not Equipped", font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.helmet_label_equip.size = equipment_size[0], equipment_size[1] * 0.75
            self.helmet_label_equip.pos = label_pos

        # Vambraces
        label_pos = label_pos[0] + spacer + equipment_size[0], label_pos[1]
        image_pos = image_pos[0] + spacer + equipment_size[0], image_pos[1]
        self.vambraces = Image(source="../res/screens/stats/equipment.png", size=equipment_size, pos=(overlay_pos[0] + spacer * 2 + equipment_size[0], overlay_pos[1] + overlay_size[1] * 0.025 + equipment_size[1]), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.vambraces_label = Label(text="Vambraces", font_size=equipment_font_size, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
        self.vambraces_label._label.refresh()
        self.vambraces_label.size = self.vambraces_label._label.texture.size
        self.vambraces_label.pos = overlay_pos[0] + spacer * 2 + equipment_size[0] + 4 * equipment_size[0] / 200, overlay_pos[1] + overlay_size[1] * 0.025 + equipment_size[1] * 2 - self.vambraces_label.height - 4 * equipment_size[1] / 75
        if char.get_equipment().vambraces is not None:
            self.vambraces_label_equip = Label(text=char.get_equipment().vambraces.get_name(), font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.vambraces_label_equip.size = equipment_size[0] * 0.75, equipment_size[1] * 0.75
            self.vambraces_label_equip.pos = label_pos
            self.vambraces_image_equip = Image(source="../res/items/equipment/" + char.get_equipment().vambraces.get_id() + ".png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True)
            self.vambraces_equipped = char.get_equipment().vambraces
        else:
            self.vambraces_equipped = None
            self.vambraces_image_equip = Image(source="../res/items/equipment/empty.png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True, opacity=0)
            self.vambraces_label_equip = Label(text="Not Equipped", font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.vambraces_label_equip.size = equipment_size[0], equipment_size[1] * 0.75
            self.vambraces_label_equip.pos = label_pos

        # Gloves
        label_pos = label_pos[0] + spacer + equipment_size[0], label_pos[1]
        image_pos = image_pos[0] + spacer + equipment_size[0], image_pos[1]
        self.gloves = Image(source="../res/screens/stats/equipment.png", size=equipment_size, pos=(overlay_pos[0] + spacer * 3 + equipment_size[0] * 2, overlay_pos[1] + overlay_size[1] * 0.025 + equipment_size[1]), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.gloves_label = Label(text="Gloves", font_size=equipment_font_size, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
        self.gloves_label._label.refresh()
        self.gloves_label.size = self.gloves_label._label.texture.size
        self.gloves_label.pos = overlay_pos[0] + spacer * 3 + equipment_size[0] * 2 + 4 * equipment_size[0] / 200, overlay_pos[1] + overlay_size[1] * 0.025 + equipment_size[1] * 2 - self.gloves_label.height - 4 * equipment_size[1] / 75
        if char.get_equipment().gloves is not None:
            self.gloves_label_equip = Label(text=char.get_equipment().gloves.get_name(), font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.gloves_label_equip.size = equipment_size[0] * 0.75, equipment_size[1] * 0.75
            self.gloves_label_equip.pos = label_pos
            self.gloves_image_equip = Image(source="../res/items/equipment/" + char.get_equipment().gloves.get_id() + ".png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True)
            self.gloves_equipped = char.get_equipment().gloves
        else:
            self.gloves_equipped = None
            self.gloves_image_equip = Image(source="../res/items/equipment/empty.png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True, opacity=0)
            self.gloves_label_equip = Label(text="Not Equipped", font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.gloves_label_equip.size = equipment_size[0], equipment_size[1] * 0.75
            self.gloves_label_equip.pos = label_pos

        # Chest
        label_pos = label_pos[0] - spacer * 2 - equipment_size[0] * 2, label_pos[1] - overlay_size[1] * 0.0125 - equipment_size[1]
        image_pos = image_pos[0] - spacer * 2 - equipment_size[0] * 2, image_pos[1] - overlay_size[1] * 0.0125 - equipment_size[1]
        self.chest = Image(source="../res/screens/stats/equipment.png", size=equipment_size, pos=(overlay_pos[0] + spacer, overlay_pos[1] + overlay_size[1] * 0.0125), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.chest_label = Label(text="Chest", font_size=equipment_font_size, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
        self.chest_label._label.refresh()
        self.chest_label.size = self.chest_label._label.texture.size
        self.chest_label.pos = overlay_pos[0] + spacer + 4 * equipment_size[0] / 200, overlay_pos[1] + overlay_size[1] * 0.0125 + equipment_size[1] - self.chest_label.height - 4 * equipment_size[1] / 75
        if char.get_equipment().chest is not None:
            self.chest_label_equip = Label(text=char.get_equipment().chest.get_name(), font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.chest_label_equip.size = equipment_size[0] * 0.75, equipment_size[1] * 0.75
            self.chest_label_equip.pos = label_pos
            self.chest_image_equip = Image(source="../res/items/equipment/" + char.get_equipment().chest.get_id() + ".png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True)
            self.chest_equipped = char.get_equipment().chest
        else:
            self.chest_equipped = None
            self.chest_image_equip = Image(source="../res/items/equipment/empty.png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True, opacity=0)
            self.chest_label_equip = Label(text="Not Equipped", font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.chest_label_equip.size = equipment_size[0], equipment_size[1] * 0.75
            self.chest_label_equip.pos = label_pos

        # Leggings
        label_pos = label_pos[0] + spacer + equipment_size[0], label_pos[1]
        image_pos = image_pos[0] + spacer + equipment_size[0], image_pos[1]
        self.leggings = Image(source="../res/screens/stats/equipment.png", size=equipment_size, pos=(overlay_pos[0] + spacer * 2 + equipment_size[0], overlay_pos[1] + overlay_size[1] * 0.0125), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.leggings_label = Label(text="Leggings", font_size=equipment_font_size, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
        self.leggings_label._label.refresh()
        self.leggings_label.size = self.leggings_label._label.texture.size
        self.leggings_label.pos = overlay_pos[0] + spacer * 2 + equipment_size[0] + 4 * equipment_size[0] / 200, overlay_pos[1] + overlay_size[1] * 0.0125 + equipment_size[1] - self.leggings_label.height - 4 * equipment_size[1] / 75
        if char.get_equipment().leggings is not None:
            self.leggings_label_equip = Label(text=char.get_equipment().leggings.get_name(), font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.leggings_label_equip.size = equipment_size[0] * 0.75, equipment_size[1] * 0.75
            self.leggings_label_equip.pos = label_pos
            self.leggings_image_equip = Image(source="../res/items/equipment/" + char.get_equipment().leggings.get_id() + ".png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True)
            self.leggings_equipped = char.get_equipment().leggings
        else:
            self.leggings_equipped = None
            self.leggings_image_equip = Image(source="../res/items/equipment/empty.png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True, opacity=0)
            self.leggings_label_equip = Label(text="Not Equipped", font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.leggings_label_equip.size = equipment_size[0], equipment_size[1] * 0.75
            self.leggings_label_equip.pos = label_pos

        # Boots
        label_pos = label_pos[0] + spacer + equipment_size[0], label_pos[1]
        image_pos = image_pos[0] + spacer + equipment_size[0], image_pos[1]
        self.boots = Image(source="../res/screens/stats/equipment.png", size=equipment_size, pos=(overlay_pos[0] + spacer * 3 + equipment_size[0] * 2, overlay_pos[1] + overlay_size[1] * 0.0125), size_hint=(None, None), keep_ratio=True, allow_stretch=True)
        self.boots_label = Label(text="Boots", font_size=equipment_font_size, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
        self.boots_label._label.refresh()
        self.boots_label.size = self.boots_label._label.texture.size
        self.boots_label.pos = overlay_pos[0] + spacer * 3 + equipment_size[0] * 2 + 4 * equipment_size[0] / 200, overlay_pos[1] + overlay_size[1] * 0.0125 + equipment_size[1] - self.boots_label.height - 4 * equipment_size[1] / 75
        if char.get_equipment().boots is not None:
            self.boots_label_equip = Label(text=char.get_equipment().boots.get_name(), font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.boots_label_equip.size = equipment_size[0] * 0.75, equipment_size[1] * 0.75
            self.boots_label_equip.pos = label_pos
            self.boots_image_equip = Image(source="../res/items/equipment/" + char.get_equipment().boots.get_id() + ".png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True)
            self.boots_equipped = char.get_equipment().boots
        else:
            self.boots_equipped = None
            self.boots_image_equip = Image(source="../res/items/equipment/empty.png", size=image_size, pos=image_pos, size_hint=(None, None), keep_ratio=True, allow_stretch=True, opacity=0)
            self.boots_label_equip = Label(text="Not Equipped", font_size=equipment_font_size * 1.25, size_hint=(None, None), color=equipment_color, font_name=equipment_font)
            self.boots_label_equip.size = equipment_size[0], equipment_size[1] * 0.75
            self.boots_label_equip.pos = label_pos

        # Neat Stats
        gap = self.rank_total_overlay.y - self.helmet.y - self.helmet.height
        neat_stat_size = overlay_size[0] * 0.875, gap * 0.875
        neat_stat_pos = overlay_pos[0] + overlay_size[0] * .0625, self.helmet.y + self.helmet.height + gap * 0.0625
        print(165 * neat_stat_size[0] / neat_stat_size[1])
        self.neat_stat_overlay = Image(source="../res/screens/stats/stat_overlay.png", size=neat_stat_size, pos=neat_stat_pos, size_hint=(None, None), keep_ratio=False, allow_stretch=True)

        size = neat_stat_size[0] * 0.95 / 3, neat_stat_size[1] * 0.95 / 3
        spacer = neat_stat_size[0] * 0.0375, neat_stat_size[1] * 0.0375
        neat_stat_color = 0, 0, 0, 1
        neat_stat_font_size = size[1] * 0.9

        # Familia
        self.familia_label = Label(text=str(char.get_familia().get_name()) + " Familia", font_size=neat_stat_font_size, size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.familia_label._label.refresh()
        self.familia_label.size = self.familia_label._label.texture.size
        self.familia_label.pos = neat_stat_pos[0] + spacer[0], neat_stat_pos[1] + neat_stat_size[1] - spacer[1] - size[1]

        # Gender
        self.gender_label = Label(text="Gender: " + str(char.get_gender()), font_size=neat_stat_font_size, size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.gender_label._label.refresh()
        self.gender_label.size = self.gender_label._label.texture.size
        self.gender_label.pos = neat_stat_pos[0] + spacer[0], neat_stat_pos[1] + spacer[1]

        # Race
        self.race_label = Label(text="Race: " + str(char.get_race()), font_size=neat_stat_font_size, size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.race_label._label.refresh()
        self.race_label.size = self.race_label._label.texture.size
        self.race_label.pos = neat_stat_pos[0] + spacer[0], self.gender_label.y + self.gender_label.height + (self.familia_label.y - self.gender_label.y - self.gender_label.height - self.race_label.height) / 2

        # Score
        self.score_label = Label(text="Score: " + str(char.get_score()), font_size=neat_stat_font_size, size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.score_label._label.refresh()
        self.score_label.size = self.score_label._label.texture.size
        self.score_label.pos = neat_stat_pos[0] + spacer[0] * 2 + size[0], neat_stat_pos[1] + neat_stat_size[1] - spacer[1] - size[1]

        # High Dmg
        self.high_dmg_label = Label(text="High Dmg.: " + str(char.get_high_dmg()), font_size=neat_stat_font_size, size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.high_dmg_label._label.refresh()
        self.high_dmg_label.size = self.high_dmg_label._label.texture.size
        self.high_dmg_label.pos = neat_stat_pos[0] + spacer[0] * 2 + size[0], neat_stat_pos[1] + spacer[1]

        # Current Worth
        self.worth_label = Label(text="Worth: " + str(char.get_worth()), font_size=neat_stat_font_size, size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.worth_label._label.refresh()
        self.worth_label.size = self.worth_label._label.texture.size
        self.worth_label.pos = neat_stat_pos[0] + spacer[0] * 2 + size[0], self.high_dmg_label.y + self.high_dmg_label.height + (self.score_label.y - self.high_dmg_label.y - self.high_dmg_label.height - self.worth_label.height) / 2

        # Floor Depth
        self.floor_depth_label = Label(text="Floor Depth: " + str(char.get_floor_depth()), font_size=neat_stat_font_size, size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.floor_depth_label._label.refresh()
        self.floor_depth_label.size = self.floor_depth_label._label.texture.size
        self.floor_depth_label.pos = neat_stat_pos[0] + neat_stat_size[0] - spacer[0] - self.floor_depth_label.width, neat_stat_pos[1] + neat_stat_size[1] - spacer[1] - size[1]

        # People Slain
        self.people_slain_label = Label(text="People Slain: " + str(char.get_people_killed()), font_size=neat_stat_font_size, size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.people_slain_label._label.refresh()
        self.people_slain_label.size = self.people_slain_label._label.texture.size
        self.people_slain_label.pos = neat_stat_pos[0] + neat_stat_size[0] - spacer[0] - self.people_slain_label.width, neat_stat_pos[1] + spacer[1]

        # Monsters Slain
        self.monsters_slain_label = Label(text="Monsters Slain: " + str(char.get_monsters_killed()), font_size=neat_stat_font_size, size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.monsters_slain_label._label.refresh()
        self.monsters_slain_label.size = self.monsters_slain_label._label.texture.size
        self.monsters_slain_label.pos = neat_stat_pos[0] + neat_stat_size[0] - spacer[0] - self.monsters_slain_label.width, self.people_slain_label.y + self.people_slain_label.height + (self.floor_depth_label.y - self.people_slain_label.y - self.people_slain_label.height - self.monsters_slain_label.height) / 2

        height = self.size[1] * 0.05
        spacer = self.size[0] * 0.025
        self.status_board = CustomHoverableButton(size=(height * 475 / 125, height), border=[0, 0, 0, 0], pos=(overlay_pos[0] - spacer - height * 475 / 125, overlay_pos[1]), path='../res/screens/buttons/long_stat', size_hint=(None, None), color=(0, 0, 0, 1), text="Status Board", font_size=height * 0.8, font_name='../res/fnt/Gabriola.ttf', on_touch_down=self.on_status_board)
        self.change_equip = CustomHoverableButton(size=(height * 475 / 125, height), border=[0, 0, 0, 0], pos=(overlay_pos[0] - spacer * 2 - self.status_board.width - height * 475 / 125, overlay_pos[1]), path='../res/screens/buttons/long_stat', size_hint=(None, None), color=(0, 0, 0, 1), text="Change Equip", font_size=height * 0.8, font_name='../res/fnt/Gabriola.ttf', on_touch_down=self.on_change_equip)
        self.image_preview = CustomHoverableButton(size=(height * 200 / 125, height), border=[0, 0, 0, 0], pos=(overlay_pos[0] - spacer * 3 - self.status_board.width - self.change_equip.width - height * 200 / 125, overlay_pos[1]), path='../res/screens/buttons/preview', size_hint=(None, None), on_touch_down=self.on_preview)

        # ###### DEV BUTTONS ######
        # self.maxStats = Button(text="Max Stats", font_size=40, pos=(500, 1000), size=(200, 200),
        #                        on_touch_down=self.maxOut, size_hint=(None, None))
        # self.rankupButton = Button(text="Rank Up", font_size=40, pos=(900, 500), size=(200, 200),
        #                            on_touch_down=self.onRankUp, size_hint=(None, None))
        # self.rankbreakButton = Button(text="Rank Break", font_size=40, pos=(900, 300), size=(200, 200),
        #                               on_touch_down=self.onRankBreak, size_hint=(None, None))
        #
        # self.hpexpincreaseButton = Button(text="Increase Hp Exp", font_size=40, pos=(1200, 1000), size=(300, 50),
        #                                   on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.mpexpincreaseButton = Button(text="Increase Mp Exp", font_size=40, pos=(1200, 925), size=(300, 50),
        #                                   on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.defexpincreaseButton = Button(text="Increase Def Exp", font_size=40, pos=(1200, 850), size=(300, 50),
        #                                    on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.strexpincreaseButton = Button(text="Increase Str Exp", font_size=40, pos=(1200, 775), size=(300, 50),
        #                                    on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.agiexpincreaseButton = Button(text="Increase Agi Exp", font_size=40, pos=(1200, 700), size=(300, 50),
        #                                    on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.dexexpincreaseButton = Button(text="Increase Dex Exp", font_size=40, pos=(1200, 625), size=(300, 50),
        #                                    on_touch_down=self.increaseExpStat, size_hint=(None, None))
        # self.endexpincreaseButton = Button(text="Increase End Exp", font_size=40, pos=(1200, 550), size=(300, 50),
        #                                    on_touch_down=self.increaseExpStat, size_hint=(None, None))
        #
        # # self.add_widget(self.maxStats)
        # # self.add_widget(self.rankupButton)
        # # self.add_widget(self.rankbreakButton)
        # # self.add_widget(self.hpexpincreaseButton)
        # # self.add_widget(self.mpexpincreaseButton)
        # # self.add_widget(self.defexpincreaseButton)
        # # self.add_widget(self.strexpincreaseButton)
        # # self.add_widget(self.agiexpincreaseButton)
        # # self.add_widget(self.dexexpincreaseButton)
        # # self.add_widget(self.endexpincreaseButton)
        #
        # ###### DEV BUTTONS END ######
        #

        self.add_widget(self.background)
        self.add_widget(self.char_image)

        for star in self.stars:
            self.add_widget(star)

        self.add_widget(self.image_preview)
        self.add_widget(self.change_equip)
        self.add_widget(self.status_board)

        self.add_widget(self.overlay_background)
        self.add_widget(self.overlay)

        self.add_widget(self.flag)
        self.add_widget(self.flag_label)
        self.add_widget(self.type)
        self.add_widget(self.type_label)

        self.add_widget(self.display_name_label)
        self.add_widget(self.name_label)
        self.add_widget(self.overlay_bar)
        self.add_widget(self.total_label)
        self.add_widget(self.total_abilities)
        self.add_widget(self.rank_abilities)

        self.add_widget(self.stat_bar_health)
        self.add_widget(self.stat_image_health)
        self.add_widget(self.stat_label_health)
        self.add_widget(self.stat_label_health_number)

        self.add_widget(self.stat_bar_mana)
        self.add_widget(self.stat_image_mana)
        self.add_widget(self.stat_label_mana)
        self.add_widget(self.stat_label_mana_number)

        self.add_widget(self.stat_bar_phyattack)
        self.add_widget(self.stat_image_phyattack)
        self.add_widget(self.stat_label_phyattack)
        self.add_widget(self.stat_label_phyattack_number)

        self.add_widget(self.stat_bar_magattack)
        self.add_widget(self.stat_image_magattack)
        self.add_widget(self.stat_label_magattack)
        self.add_widget(self.stat_label_magattack_number)

        self.add_widget(self.stat_bar_defense)
        self.add_widget(self.stat_image_defense)
        self.add_widget(self.stat_label_defense)
        self.add_widget(self.stat_label_defense_number)

        self.add_widget(self.rank_total_overlay)

        self.add_widget(self.rank_total_strength_label)
        self.add_widget(self.rank_total_strength_image)
        self.add_widget(self.rank_total_strength_label_number)

        self.add_widget(self.rank_total_magic_label)
        self.add_widget(self.rank_total_magic_image)
        self.add_widget(self.rank_total_magic_label_number)

        self.add_widget(self.rank_total_endurance_label)
        self.add_widget(self.rank_total_endurance_image)
        self.add_widget(self.rank_total_endurance_label_number)

        self.add_widget(self.rank_total_dexterity_label)
        self.add_widget(self.rank_total_dexterity_image)
        self.add_widget(self.rank_total_dexterity_label_number)

        self.add_widget(self.rank_total_agility_label)
        self.add_widget(self.rank_total_agility_image)
        self.add_widget(self.rank_total_agility_label_number)

        self.add_widget(self.rank_current_overlay)

        self.add_widget(self.rank_current_strength_label)
        self.add_widget(self.rank_current_strength_image)
        self.add_widget(self.rank_current_strength_label_number)

        self.add_widget(self.rank_current_magic_label)
        self.add_widget(self.rank_current_magic_image)
        self.add_widget(self.rank_current_magic_label_number)

        self.add_widget(self.rank_current_endurance_label)
        self.add_widget(self.rank_current_endurance_image)
        self.add_widget(self.rank_current_endurance_label_number)

        self.add_widget(self.rank_current_dexterity_label)
        self.add_widget(self.rank_current_dexterity_image)
        self.add_widget(self.rank_current_dexterity_label_number)

        self.add_widget(self.rank_current_agility_label)
        self.add_widget(self.rank_current_agility_image)
        self.add_widget(self.rank_current_agility_label_number)

        self.add_widget(self.neat_stat_overlay)

        self.add_widget(self.familia_label)
        self.add_widget(self.race_label)
        self.add_widget(self.gender_label)

        self.add_widget(self.score_label)
        self.add_widget(self.worth_label)
        self.add_widget(self.high_dmg_label)

        self.add_widget(self.floor_depth_label)
        self.add_widget(self.monsters_slain_label)
        self.add_widget(self.people_slain_label)

        self.add_widget(self.helmet)
        self.add_widget(self.helmet_label)
        self.add_widget(self.helmet_label_equip)
        self.add_widget(self.helmet_image_equip)

        self.add_widget(self.vambraces)
        self.add_widget(self.vambraces_label)
        self.add_widget(self.vambraces_label_equip)
        self.add_widget(self.vambraces_image_equip)

        self.add_widget(self.gloves)
        self.add_widget(self.gloves_label)
        self.add_widget(self.gloves_label_equip)
        self.add_widget(self.gloves_image_equip)

        self.add_widget(self.chest)
        self.add_widget(self.chest_label)
        self.add_widget(self.chest_label_equip)
        self.add_widget(self.chest_image_equip)

        self.add_widget(self.leggings)
        self.add_widget(self.leggings_label)
        self.add_widget(self.leggings_label_equip)
        self.add_widget(self.leggings_image_equip)

        self.add_widget(self.boots)
        self.add_widget(self.boots_label)
        self.add_widget(self.boots_label_equip)
        self.add_widget(self.boots_image_equip)

        self.add_widget(self.back_button)
        self.initalized = True

    def on_size(self, instance, size):
        pass

    def reload(self):
        pass

    def on_preview(self, instance, touch):
        pass

    def on_status_board(self, instance, touch):
        pass

    def on_change_equip(self, instance, touch):
        pass

    def maxOut(self, instance, touch):
        if instance.collide_point(*touch.pos) and instance == self.maxStats:
            for x in range(10):
                self.status_board_manager.screens[x].unlockAllNum()
                self.increaseExpStatNum(0)
                self.increaseExpStatNum(1)
                self.increaseExpStatNum(2)
                self.increaseExpStatNum(3)
                self.increaseExpStatNum(4)
                self.increaseExpStatNum(5)
                self.increaseExpStatNum(6)
                self.char.printstats()
                self.char.rankbreak()
                self.updateStars()
                self.char.ranks[self.char.currentRank - 1].calcvalues()
                self.char.ranks[self.char.currentRank - 1].calcexpvalues()
                self.char.updateCharValues()
                self.updateRankLabels()
                self.updateRankPreviewLabels(self.char.currentRank)
                self.updateexpbars()
                self.char.printstats()
                if not x == 9:
                    if not self.char.first == None:
                        # print("character is first")
                        if self.char.currentRank > 2:
                            # print("unlocking the tavern")
                            App.tavern_unlocked = False
                    self.char.rankup()
                    self.updateStars()
                    self.updateexpbarsmaxs()

    def increaseExpStatNum(self, statType):
        if statType == 0:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expHpCap - self.char.ranks[
                    self.char.currentRank - 1].exphealthraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expHpCap - self.char.ranks[
                    self.char.currentRank - 2].expHpCap) - self.char.ranks[
                                 self.char.currentRank - 1].exphealthraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].exphealthraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.healthLvlBar.value = self.char.exphealthtotal
            self.updateRankLabels()
        elif statType == 1:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expMpCap - self.char.ranks[
                    self.char.currentRank - 1].expmagicalpointsraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expMpCap - self.char.ranks[
                    self.char.currentRank - 2].expMpCap) - self.char.ranks[
                                 self.char.currentRank - 1].expmagicalpointsraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expmagicalpointsraw += random.uniform(bottomrange,
                                                                                             toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.mpLvlBar.value = self.char.expmptotal
            self.updateRankLabels()
        elif statType == 2:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expDefCap - self.char.ranks[
                    self.char.currentRank - 1].expdefenseraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expDefCap - self.char.ranks[
                    self.char.currentRank - 2].expDefCap) - self.char.ranks[
                                 self.char.currentRank - 1].expdefenseraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expdefenseraw += random.uniform(bottomrange,
                                                                                       toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.defLvlBar.value = self.char.expdeftotal
            self.updateRankLabels()
        elif statType == 3:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expStrCap - self.char.ranks[
                    self.char.currentRank - 1].expstrengthraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expStrCap - self.char.ranks[
                    self.char.currentRank - 2].expStrCap) - self.char.ranks[
                                 self.char.currentRank - 1].expstrengthraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expstrengthraw += random.uniform(bottomrange,
                                                                                        toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.strLvlBar.value = self.char.expstrtotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif statType == 4:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expAgiCap - self.char.ranks[
                    self.char.currentRank - 1].expagilityraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expAgiCap - self.char.ranks[
                    self.char.currentRank - 2].expAgiCap) - self.char.ranks[
                                 self.char.currentRank - 1].expagilityraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expagilityraw += random.uniform(bottomrange,
                                                                                       toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.agiLvlBar.value = self.char.expagitotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif statType == 5:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expDexCap - self.char.ranks[
                    self.char.currentRank - 1].expdexterityraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expDexCap - self.char.ranks[
                    self.char.currentRank - 2].expDexCap) - self.char.ranks[
                                 self.char.currentRank - 1].expdexterityraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expdexterityraw += random.uniform(bottomrange,
                                                                                         toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.dexLvlBar.value = self.char.expdextotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif statType == 6:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expEndCap - self.char.ranks[
                    self.char.currentRank - 1].expenduranceraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expEndCap - self.char.ranks[
                    self.char.currentRank - 2].expEndCap) - self.char.ranks[
                                 self.char.currentRank - 1].expenduranceraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expenduranceraw += random.uniform(bottomrange,
                                                                                         toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.endLvlBar.value = self.char.expendtotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)

    def increaseExpStat(self, instance, touch):
        if self.hpexpincreaseButton.collide_point(*touch.pos) and instance == self.hpexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expHpCap - self.char.ranks[
                    self.char.currentRank - 1].exphealthraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expHpCap - self.char.ranks[
                    self.char.currentRank - 2].expHpCap) - self.char.ranks[self.char.currentRank - 1].exphealthraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].exphealthraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.healthLvlBar.value = self.char.exphealthtotal
            self.updateRankLabels()
        elif self.mpexpincreaseButton.collide_point(*touch.pos) and instance == self.mpexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expMpCap - self.char.ranks[
                    self.char.currentRank - 1].expmagicalpointsraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expMpCap - self.char.ranks[
                    self.char.currentRank - 2].expMpCap) - self.char.ranks[
                                 self.char.currentRank - 1].expmagicalpointsraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expmagicalpointsraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.mpLvlBar.value = self.char.expmptotal
            self.updateRankLabels()
        elif self.defexpincreaseButton.collide_point(*touch.pos) and instance == self.defexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expDefCap - self.char.ranks[
                    self.char.currentRank - 1].expdefenseraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expDefCap - self.char.ranks[
                    self.char.currentRank - 2].expDefCap) - self.char.ranks[self.char.currentRank - 1].expdefenseraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expdefenseraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.defLvlBar.value = self.char.expdeftotal
            self.updateRankLabels()
        elif self.strexpincreaseButton.collide_point(*touch.pos) and instance == self.strexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expStrCap - self.char.ranks[
                    self.char.currentRank - 1].expstrengthraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expStrCap - self.char.ranks[
                    self.char.currentRank - 2].expStrCap) - self.char.ranks[self.char.currentRank - 1].expstrengthraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expstrengthraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.strLvlBar.value = self.char.expstrtotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif self.agiexpincreaseButton.collide_point(*touch.pos) and instance == self.agiexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expAgiCap - self.char.ranks[
                    self.char.currentRank - 1].expagilityraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expAgiCap - self.char.ranks[
                    self.char.currentRank - 2].expAgiCap) - self.char.ranks[self.char.currentRank - 1].expagilityraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expagilityraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.agiLvlBar.value = self.char.expagitotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif self.dexexpincreaseButton.collide_point(*touch.pos) and instance == self.dexexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expDexCap - self.char.ranks[
                    self.char.currentRank - 1].expdexterityraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expDexCap - self.char.ranks[
                    self.char.currentRank - 2].expDexCap) - self.char.ranks[self.char.currentRank - 1].expdexterityraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expdexterityraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.dexLvlBar.value = self.char.expdextotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)
        elif self.endexpincreaseButton.collide_point(*touch.pos) and instance == self.endexpincreaseButton:
            if self.char.currentRank == 1:
                valuerange = self.char.ranks[self.char.currentRank - 1].expEndCap - self.char.ranks[
                    self.char.currentRank - 1].expenduranceraw
            else:
                valuerange = (self.char.ranks[self.char.currentRank - 1].expEndCap - self.char.ranks[
                    self.char.currentRank - 2].expEndCap) - self.char.ranks[self.char.currentRank - 1].expenduranceraw
            toprange = float(valuerange) * 1
            bottomrange = float(valuerange) * 1
            self.char.ranks[self.char.currentRank - 1].expenduranceraw += random.uniform(bottomrange, toprange)
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.totalstatpreview.endLvlBar.value = self.char.expendtotal
            self.updateRankLabels()
            if self.status_board_manager.currentGrid + 1 == self.char.currentRank:
                self.updateRankPreviewLabels(self.char.currentRank)

    def updateStars(self):
        count = 0
        for x in self.char.ranks:
            if x.unlocked:
                if not x.broken:
                    self.stars[count].source = '../res/screens/stats/star.png'
                    self.stars[count].opacity = 1
                else:
                    self.stars[count].source = '../res/screens/stats/rankbrk.png'
                    self.stars[count].opacity = 1
            count += 1
        self.preview.updateStars(self.char)

    def onRankUp(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if not self.char.first == None:
                # print("character is first")
                if self.char.currentRank > 2:
                    # print("unlocking the tavern")
                    App.tavern_unlocked = False
            self.char.rankup()
            self.updateStars()
            self.updateexpbarsmaxs()
            # self.preview.updateStars()

    def onRankBreak(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.char.printstats()
            self.char.rankbreak()
            self.updateStars()
            self.char.ranks[self.char.currentRank - 1].calcvalues()
            self.char.ranks[self.char.currentRank - 1].calcexpvalues()
            self.char.updateCharValues()
            self.updateRankLabels()
            self.updateRankPreviewLabels(self.char.currentRank)
            self.updateexpbars()
            self.char.printstats()

    def updateexpbars(self, *args):
        self.totalstatpreview.healthLvlBar.value = self.char.exphealthtotal
        self.totalstatpreview.mpLvlBar.value = self.char.expmptotal
        self.totalstatpreview.defLvlBar.value = self.char.expdeftotal
        self.totalstatpreview.strLvlBar.value = self.char.expstrtotal
        self.totalstatpreview.agiLvlBar.value = self.char.expagitotal
        self.totalstatpreview.dexLvlBar.value = self.char.expdextotal
        self.totalstatpreview.endLvlBar.value = self.char.expendtotal

    def updateexpbarsmaxs(self):
        self.totalstatpreview.healthLvlBar.max = self.char.ranks[self.char.currentRank - 1].expHpCap
        self.totalstatpreview.mpLvlBar.max = self.char.ranks[self.char.currentRank - 1].expMpCap
        self.totalstatpreview.defLvlBar.max = self.char.ranks[self.char.currentRank - 1].expDefCap
        self.totalstatpreview.strLvlBar.max = self.char.ranks[self.char.currentRank - 1].expStrCap
        self.totalstatpreview.agiLvlBar.max = self.char.ranks[self.char.currentRank - 1].expAgiCap
        self.totalstatpreview.dexLvlBar.max = self.char.ranks[self.char.currentRank - 1].expDexCap
        self.totalstatpreview.endLvlBar.max = self.char.ranks[self.char.currentRank - 1].expEndCap

    def updateRankLabels(self, *args):
        self.totalstatpreview.healthlabelnumber.text = '%d' % self.char.totalHealth
        self.totalstatpreview.magicalpointlabelnumber.text = '%d' % self.char.totalMP
        self.totalstatpreview.attacklabelnumber.text = '%d' % self.char.totalPhysicalAttack
        self.totalstatpreview.defenselabelnumber.text = '%d' % self.char.totalDefense
        self.totalstatpreview.strengthnumber.text = '%d' % self.char.totalStrength
        self.totalstatpreview.agilitynumber.text = '%d' % self.char.totalAgility
        self.totalstatpreview.dexteritynumber.text = '%d' % self.char.totalDexterity
        self.totalstatpreview.endurancenumber.text = '%d' % self.char.totalEndurance
        self.totalstatpreview.strengthgrade.source = Scale.getScaleAsImagePath(self.char.totalStrength,
                                                                               self.char.ranks[9].strengthMax)
        self.totalstatpreview.agilitygrade.source = Scale.getScaleAsImagePath(self.char.totalAgility,
                                                                              self.char.ranks[9].agilityMax)
        self.totalstatpreview.dexteritygrade.source = Scale.getScaleAsImagePath(self.char.totalDexterity,
                                                                                self.char.ranks[9].dexterityMax)
        self.totalstatpreview.endurancegrade.source = Scale.getScaleAsImagePath(self.char.totalEndurance,
                                                                                self.char.ranks[9].enduranceMax)

    def updateRankPreviewLabels(self, rank):
        self.rankstatpreview.strengthnumber.text = '%d' % self.char.ranks[rank - 1].rankstrengthtotal
        self.rankstatpreview.strengthgrade.source = Scale.getScaleAsImagePath(
            self.char.ranks[rank - 1].rankstrengthtotal,
            self.char.ranks[rank - 1].strengthMax)
        self.rankstatpreview.agilitynumber.text = '%d' % self.char.ranks[rank - 1].rankagilitytotal
        self.rankstatpreview.agilitygrade.source = Scale.getScaleAsImagePath(self.char.ranks[rank - 1].rankagilitytotal,
                                                                             self.char.ranks[rank - 1].agilityMax)
        self.rankstatpreview.dexteritynumber.text = '%d' % self.char.ranks[rank - 1].rankdexteritytotal
        self.rankstatpreview.dexteritygrade.source = Scale.getScaleAsImagePath(
            self.char.ranks[rank - 1].rankdexteritytotal,
            self.char.ranks[rank - 1].dexterityMax)
        self.rankstatpreview.endurancenumber.text = '%d' % self.char.ranks[rank - 1].rankendurancetotal
        self.rankstatpreview.endurancegrade.source = Scale.getScaleAsImagePath(
            self.char.ranks[rank - 1].rankendurancetotal,
            self.char.ranks[rank - 1].enduranceMax)

    def updatelabels(self, *args):
        # print(self.nameLabel.texture_size)
        # print(self.displaynameLabel.texture_size)
        self.nameLabel.pos = App.height - 100 - self.nameLabel.texture_size[0] / 2, App.height - 140
        # self.displaynameLabel.pos = self.nameLabel.texture_size[0] + 200 + 100 + self.displaynameLabel.texture_size[0]/2, App.height - 159
        # self.layout.add_widget(self.displaynameLabel)

    def on_back_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.main_screen is not None:
                self.main_screen.display_screen(None, False, False)
            return True