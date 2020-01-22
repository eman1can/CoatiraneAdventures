from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.graphics import BorderImage
from kivy.uix.label import Label
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.uix.progressbar import ProgressBar

from src.entitites.Character.Scale import Scale
from src.modules.HTButton import HTButton


class CharacterAttributeScreen(Screen):
    initialized = BooleanProperty(False)
    main_screen = ObjectProperty(None, allownone=True)
    preview = ObjectProperty(None, allownone=True)

    char = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = self.char.get_name()

        self._size = (0, 0)

        self.back_button = HTButton(size_hint=(None, None), path='../res/screens/buttons/back', on_release=self.on_back_press)

        # Overlays & Backgrounds
        self.background = Image(source="../res/screens/backgrounds/background.png", keep_ratio=False, allow_stretch=True)

        self.char_image = self.char.get_full_image(False)
        self.full_image_loaded = True

        self.overlay_background = Image(source="../res/screens/attribute/stat_background.png", size_hint=(None, None), allow_stretch=True)
        self.overlay = Image(source="../res/screens/attribute/stat_background_overlay.png", size_hint=(None, None), allow_stretch=True)


        self.flag = Image(source="../res/screens/attribute/char_type_flag.png", size_hint=(None, None), allow_stretch=True)
        if self.char.is_support():
            text = "Supporter"
        else:
            text = "Adventurer"
        self.flag_label = Label(text=text, size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')

        self.type = Image(source="../res/screens/recruit/" + str(self.char.get_type()).lower() + "_flag.png", size_hint=(None, None), allow_stretch=True)
        self.type_label = Label(text=str(self.char.get_type()) + " Type", size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')

        self.element_flag_background = Image(source="../res/screens/attribute/" + self.char.get_element().lower() + "_flag.png", allow_stretch=True, size_hint=(None, None))
        self.element_flag_label = Label(text=self.char.get_element().capitalize(), color=(0, 0, 0, 1), font_name="../res/fnt/Gabriola.ttf", size_hint=(None, None))
        self.element_flag_image = Image(source="../res/screens/attribute/" + self.char.get_element().lower() + ".png", allow_stretch=True, size_hint=(None, None))

        # Stars
        self.stars = []
        for level in self.char.ranks:
            star = Image(source="../res/screens/stats/star.png", size_hint=(None, None), opacity=1)
            if level.unlocked:
                if level.broken:
                    star.source = "../res/screens/stats/rankbrk.png"
            else:
                star.opacity = 0
            self.stars.append(star)

        # Title Names & Bar
        self.display_name_label = Label(text=str(self.char.get_display_name()), size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')
        self.name_label = Label(text=str(self.char.get_name()), size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')

        self.overlay_bar = Image(source="../res/screens/stats/overlay_bar.png", size_hint=(None, None), allow_stretch=True)

        self.total_label = Label(text="Total Stats", size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')
        self.total_abilities = Label(text="Total Abilities", size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')
        self.rank_abilities = Label(text="Rank Abilities", size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')

        # Health
        self.stat_bar_health = Image(source="../res/screens/attribute/stat_bar.png", size_hint=(None, None), allow_stretch=True)
        self.stat_image_health = Image(source="../res/screens/stats/Health.png", size_hint=(None, None), allow_stretch=True)
        self.stat_label_health = Label(text="Health", size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_health_number = Label(text=str(self.char.get_health()), size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Gabriola.ttf')

        # Mana
        self.stat_bar_mana = Image(source="../res/screens/attribute/stat_bar.png", size_hint=(None, None), allow_stretch=True)
        self.stat_image_mana = Image(source="../res/screens/stats/Mana.png", size_hint=(None, None), allow_stretch=True)
        self.stat_label_mana = Label(text="Mana", size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_mana_number = Label(text=str(self.char.get_mana()), size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Gabriola.ttf')

        # Phy Attack
        self.stat_bar_phyattack = Image(source="../res/screens/attribute/stat_bar.png", size_hint=(None, None), allow_stretch=True)
        self.stat_image_phyattack = Image(source="../res/screens/stats/PhysicalAttack.png", size_hint=(None, None), allow_stretch=True)
        self.stat_label_phyattack = Label(text="P. Attack", size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_phyattack_number = Label(text=str(self.char.get_phyatk()), size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Gabriola.ttf')

        # Mag Attack
        self.stat_bar_magattack = Image(source="../res/screens/attribute/stat_bar.png",size_hint=(None, None), allow_stretch=True)
        self.stat_image_magattack = Image(source="../res/screens/stats/MagicalAttack.png", size_hint=(None, None), allow_stretch=True)
        self.stat_label_magattack = Label(text="M. Attack", size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_magattack_number = Label(text=str(self.char.get_magatk()), size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Gabriola.ttf')

        # Defense
        self.stat_bar_defense = Image(source="../res/screens/attribute/stat_bar.png", size_hint=(None, None), allow_stretch=True)
        self.stat_image_defense = Image(source="../res/screens/stats/Defense.png", size_hint=(None, None), allow_stretch=True)
        self.stat_label_defense = Label(text="Defense", size_hint=(None, None), color=(1, 1, 1, 1), font_name='../res/fnt/Gabriola.ttf')
        self.stat_label_defense_number = Label(text=str(self.char.get_defense()), size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Gabriola.ttf')

        # Rank Total Stats
        self.rank_total_overlay = Image(source="../res/screens/attribute/ability_overlay.png", size_hint=(None, None), allow_stretch=True)
        rank_stat_color = 0, 0, 0, 1

        # Strength
        self.rank_total_strength_label = Label(text="Strength", size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_strength_image = Image(source=self.char.get_strength_rank(), size_hint=(None, None), allow_stretch=True)
        self.rank_total_strength_label_number = Label(text=str(self.char.get_strength()), size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')

        # Magic
        self.rank_total_magic_label = Label(text="Magic", size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_magic_image = Image(source=self.char.get_magic_rank(), size_hint=(None, None), allow_stretch=True)
        self.rank_total_magic_label_number = Label(text=str(self.char.get_magic()), size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')

        # Endurance
        self.rank_total_endurance_label = Label(text="Endurance", size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_endurance_image = Image(source=self.char.get_endurance_rank(), size_hint=(None, None),allow_stretch=True)
        self.rank_total_endurance_label_number = Label(text=str(self.char.get_endurance()), size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')

        # Dexterity
        self.rank_total_dexterity_label = Label(text="Dexterity", size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_dexterity_image = Image(source=self.char.get_dexterity_rank(), size_hint=(None, None), allow_stretch=True)
        self.rank_total_dexterity_label_number = Label(text=str(self.char.get_dexterity()), size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')

        # Agility
        self.rank_total_agility_label = Label(text="Agility", size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_total_agility_image = Image(source=self.char.get_agility_rank(), size_hint=(None, None), allow_stretch=True)
        self.rank_total_agility_label_number = Label(text=str(self.char.get_agility()), size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')

        # Current Rank Stats
        self.rank_current_overlay = Image(source="../res/screens/attribute/ability_overlay.png", size_hint=(None, None), allow_stretch=True)

        # Strength
        self.rank_current_strength_label = Label(text="Strength", size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_strength_image = Image(source=self.char.get_strength_rank(self.char.get_current_rank()), size_hint=(None, None), allow_stretch=True)
        self.rank_current_strength_label_number = Label(text=str(self.char.get_strength(self.char.get_current_rank())), size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')

        # Magic
        self.rank_current_magic_label = Label(text="Magic", size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_magic_image = Image(source=self.char.get_magic_rank(self.char.get_current_rank()), size_hint=(None, None), allow_stretch=True)
        self.rank_current_magic_label_number = Label(text=str(self.char.get_magic(self.char.get_current_rank())), size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')

        # Endurance
        self.rank_current_endurance_label = Label(text="Endurance", size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_endurance_image = Image(source=self.char.get_endurance_rank(self.char.get_current_rank()), size_hint=(None, None), allow_stretch=True)
        self.rank_current_endurance_label_number = Label(text=str(self.char.get_endurance(self.char.get_current_rank())), size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')

        # Dexterity
        self.rank_current_dexterity_label = Label(text="Dexterity", size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_dexterity_image = Image(source=self.char.get_dexterity_rank(self.char.get_current_rank()), size_hint=(None, None), allow_stretch=True)
        self.rank_current_dexterity_label_number = Label(text=str(self.char.get_dexterity(self.char.get_current_rank())), size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')

        # Agility
        self.rank_current_agility_label = Label(text="Agility", size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.rank_current_agility_image = Image(source=self.char.get_agility_rank(self.char.get_current_rank()), size_hint=(None, None), allow_stretch=True)
        self.rank_current_agility_label_number = Label(text=str(self.char.get_agility(self.char.get_current_rank())), size_hint=(None, None), color=rank_stat_color, font_name='../res/fnt/Gabriola.ttf')

        # Equipment
        equipment_color = 0, 0, 0, 1
        equipment_font = '../res/fnt/Gabriola.ttf'

        self.equipment_layout = GridLayout(rows=4, cols=3, size_hint=(None, None))

        self.weapon = EquipmentSlot(item=self.char.get_equipment().weapon, slot_name='weapon', color=equipment_color, font=equipment_font)
        self.necklace = EquipmentSlot(item=self.char.get_equipment().necklace, slot_name='necklace', color=equipment_color, font=equipment_font)
        self.ring = EquipmentSlot(item=self.char.get_equipment().ring, slot_name='ring', color=equipment_color, font=equipment_font)
        self.helmet = EquipmentSlot(item=self.char.get_equipment().helmet, slot_name='helmet', color=equipment_color, font=equipment_font)
        self.vambraces = EquipmentSlot(item=self.char.get_equipment().vambraces, slot_name='vambraces', color=equipment_color, font=equipment_font)
        self.gloves = EquipmentSlot(item=self.char.get_equipment().gloves, slot_name='gloves', color=equipment_color, font=equipment_font)
        self.chest = EquipmentSlot(item=self.char.get_equipment().chest, slot_name='chest', color=equipment_color, font=equipment_font)
        self.leggings = EquipmentSlot(item=self.char.get_equipment().leggings, slot_name='leggings', color=equipment_color, font=equipment_font)
        self.boots = EquipmentSlot(item=self.char.get_equipment().boots, slot_name='boots', color=equipment_color, font=equipment_font)

        # Neat Stats
        neat_stat_color = 0, 0, 0, 1
        self.neat_stat_overlay = Image(source="../res/screens/attribute/stat_overlay.png", size_hint=(None, None), allow_stretch=True)

        self.neat_stat_layout = GridLayout(cols=3, rows=3, size_hint=(None, None))

        self.familia_label = Label(text=str(self.char.get_familia().get_name()) + " Familia", size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.gender_label = Label(text="Gender: " + str(self.char.get_gender()), size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.race_label = Label(text="Race: " + str(self.char.get_race()), size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.score_label = Label(text="Score: " + str(self.char.get_score()), size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.high_dmg_label = Label(text="High Dmg.: " + str(self.char.get_high_dmg()), size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.worth_label = Label(text="Worth: " + str(self.char.get_worth()), size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.floor_depth_label = Label(text="Floor Depth: " + str(self.char.get_floor_depth()), size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.people_slain_label = Label(text="People Slain: " + str(self.char.get_people_killed()), size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')
        self.monsters_slain_label = Label(text="Monsters Slain: " + str(self.char.get_monsters_killed()), size_hint=(None, None), color=neat_stat_color, font_name='../res/fnt/Gabriola.ttf')

        self.status_board = HTButton(path='../res/screens/buttons/long_stat', size_hint=(None, None), label_color=(0, 0, 0, 1), text="Status Board", font_name='../res/fnt/Gabriola.ttf', on_release=self.on_status_board)
        self.change_equip = HTButton(path='../res/screens/buttons/long_stat', size_hint=(None, None), label_color=(0, 0, 0, 1), text="Change Equip", font_name='../res/fnt/Gabriola.ttf', on_release=self.on_change_equip)
        self.image_preview = HTButton(path='../res/screens/buttons/preview', size_hint=(None, None), on_release=self.on_image_preview)

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
        self.add_widget(self.element_flag_background)
        self.add_widget(self.element_flag_label)
        self.add_widget(self.element_flag_image)

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

        self.neat_stat_layout.add_widget(self.familia_label)
        self.neat_stat_layout.add_widget(self.race_label)
        self.neat_stat_layout.add_widget(self.gender_label)

        self.neat_stat_layout.add_widget(self.score_label)
        self.neat_stat_layout.add_widget(self.worth_label)
        self.neat_stat_layout.add_widget(self.high_dmg_label)

        self.neat_stat_layout.add_widget(self.floor_depth_label)
        self.neat_stat_layout.add_widget(self.monsters_slain_label)
        self.neat_stat_layout.add_widget(self.people_slain_label)
        self.add_widget(self.neat_stat_layout)

        self.equipment_layout.add_widget(self.weapon)
        self.equipment_layout.add_widget(self.necklace)
        self.equipment_layout.add_widget(self.ring)
        self.equipment_layout.add_widget(self.helmet)
        self.equipment_layout.add_widget(self.vambraces)
        self.equipment_layout.add_widget(self.gloves)
        self.equipment_layout.add_widget(self.chest)
        self.equipment_layout.add_widget(self.leggings)
        self.equipment_layout.add_widget(self.boots)
        self.add_widget(self.equipment_layout)

        self.add_widget(self.back_button)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.background.size = self.size

        self.back_button.size = self.width * .05, self.width * .05
        self.back_button.pos = 0, self.height - self.back_button.height

        self.char_image.size = (self.char_image.image_ratio * self.height, self.height)
        # self.char_image.size = self.size
        # self.char_image.pos = (-(self.width - self.char_image.image_ratio * self.height) / 2, 0)

        overlay_size = self.height * .9 * 620 / 610, self.height * .9
        overlay_pos = self.width - self.height * .05 - overlay_size[0], self.height * .05

        self.overlay_background.size = overlay_size
        self.overlay_background.pos = overlay_pos

        self.overlay.size = overlay_size
        self.overlay.pos = overlay_pos

        gap = 10 * overlay_size[1] / 610
        flag_size = overlay_size[0] * 0.25, overlay_size[0] * 0.25 * 150 / 619
        flag_pos = overlay_pos[0] + gap, overlay_pos[1] + overlay_size[1] - flag_size[1] - gap

        self.flag.size = flag_size
        self.flag.pos = flag_pos

        self.flag_label.font_size = flag_size[1] * 0.7
        self.flag_label.size = flag_size[0] * 0.83, flag_size[1] * 0.85
        self.flag_label.pos = flag_pos[0], flag_pos[1] + flag_size[1] * 0.15

        type_size = overlay_size[0] * 0.25, overlay_size[0] * 0.25 * 150 / 575
        type_pos = overlay_pos[0] + overlay_size[0] - type_size[0] - gap, overlay_pos[1] + overlay_size[1] - type_size[1] - gap
        self.type.size = type_size
        self.type.pos = type_pos

        self.type_label.font_size = type_size[1] * 0.65
        self.type_label.size = flag_size[0] * 0.83, flag_size[1] * 0.85
        self.type_label.pos = type_pos[0] + type_size[0] * 0.17, type_pos[1] + type_size[1] * 0.15

        element_flag_size = (self.height - self.type.y) * 150 / 400 * 1.25, (self.height - self.type.y) * 1.25
        element_flag_pos = overlay_pos[0] + overlay_size[0] - element_flag_size[0] - gap, self.type_label.pos[1] - element_flag_size[1]
        self.element_flag_background.size = element_flag_size
        self.element_flag_background.pos = element_flag_pos
        self.element_flag_label.font_size = element_flag_size[1] * 0.1
        self.element_flag_label.size = element_flag_size[0], element_flag_size[1] * 0.6
        self.element_flag_label.pos = element_flag_pos[0], element_flag_pos[1] + element_flag_size[1] * 0.4
        self.element_flag_image.size = element_flag_size[0] * 0.3, element_flag_size[0] * 0.3
        self.element_flag_image.pos = element_flag_pos[0] + element_flag_size[0] * 0.35, element_flag_pos[1] + element_flag_size[0] * 0.65

        add_x = False
        count = 0
        for star in self.stars:
            x_pos = self.height * 0.05
            if add_x:
                x_pos += self.height * 0.025
            star.size = self.height * 0.125, self.height * 0.125
            star.pos = x_pos, self.height * 0.05 + (count * self.height * 0.075)
            count += 1
            if add_x:
                x_pos -= self.height * 0.025
            add_x = not add_x

        self.display_name_label.font_size = self.width * .025
        self.display_name_label.texture_update()
        self.display_name_label.size = self.display_name_label.texture_size
        self.display_name_label.pos = overlay_pos[0] + (overlay_size[0] - self.display_name_label.width) / 2, overlay_pos[1] + overlay_size[1] * .975 - self.display_name_label.height

        self.name_label.font_size = self.width * 0.05
        self.name_label.texture_update()
        self.name_label.size = self.name_label.texture_size
        self.name_label.pos = overlay_pos[0] + (overlay_size[0] - self.name_label.width) / 2, overlay_pos[1] + overlay_size[1] * .95 - self.display_name_label.height - self.name_label.height

        self.overlay_bar.size = overlay_size[0] * .6, overlay_size[1] * 20 / 620
        self.overlay_bar.pos = overlay_pos[0] + overlay_size[0] * .2, overlay_pos[1] + overlay_size[1] * .93 - self.display_name_label.height - self.name_label.height

        self.total_label.font_size = self.width * 0.0175
        self.total_label.texture_update()
        self.total_label.size = self.total_label.texture_size
        self.total_label.pos = overlay_pos[0] + overlay_size[0] * 0.0625 + (overlay_size[0] * .25 - self.total_label.width) / 2, overlay_pos[1] + overlay_size[1] * .92 - self.display_name_label.height - self.name_label.height - self.total_label.height

        self.total_abilities.font_size = self.width * 0.0175
        self.total_abilities.texture_update()
        self.total_abilities.size = self.total_abilities.texture_size
        self.total_abilities.pos = overlay_pos[0] + (overlay_size[0] - self.total_abilities.width) / 2, overlay_pos[1] + overlay_size[1] * .92 - self.display_name_label.height - self.name_label.height - self.total_abilities.height

        self.rank_abilities.font_size = self.width * 0.0175
        self.rank_abilities.texture_update()
        self.rank_abilities.size = self.rank_abilities.texture_size
        self.rank_abilities.pos = overlay_pos[0] + overlay_size[0] * 0.6875 + (overlay_size[0] * .25 - self.rank_abilities.width) / 2, overlay_pos[1] + overlay_size[1] * .92 - self.display_name_label.height - self.name_label.height - self.rank_abilities.height

        stat_bar_size = overlay_size[0] * 0.1875, overlay_size[0] * 0.1875 * 25 / 135
        stat_image_size = stat_bar_size[1] * .9, stat_bar_size[1] * .9
        stat_bar_start = overlay_pos[0] + overlay_size[0] * 0.0625
        start = overlay_pos[1] + overlay_size[1] * .9125 - self.display_name_label.height - self.name_label.height - self.total_label.height
        spacer = stat_bar_size[1] / 2

        # Health
        self.stat_bar_health.size = stat_bar_size
        self.stat_bar_health.pos = stat_bar_start, start - stat_bar_size[1]

        self.stat_image_health.size = stat_image_size
        self.stat_image_health.pos = self.stat_bar_health.x + stat_bar_size[0] * 0.05, self.stat_bar_health.y + stat_bar_size[1] * 0.05

        self.stat_label_health.font_size = stat_image_size[1]
        self.stat_label_health.texture_update()
        self.stat_label_health.size = self.stat_label_health.texture_size
        self.stat_label_health.pos = self.stat_image_health.x + stat_image_size[0] + (stat_bar_size[0] * 0.95 - stat_image_size[0] - self.stat_label_health.width) / 2, self.stat_bar_health.y + (stat_bar_size[1] - self.stat_label_health.height) / 2

        self.stat_label_health_number.font_size = stat_image_size[1]
        self.stat_label_health_number.texture_update()
        self.stat_label_health_number.size = self.stat_label_health_number.texture_size
        self.stat_label_health_number.pos = self.stat_bar_health.x + overlay_size[0] * 0.25 - self.stat_label_health_number.width, self.stat_bar_health.y + (stat_bar_size[1] - self.stat_label_health_number.height) / 2

        # Mana
        self.stat_bar_mana.size = stat_bar_size
        self.stat_bar_mana.pos = stat_bar_start, start - stat_bar_size[1] * 2 - spacer

        self.stat_image_mana.size = stat_image_size
        self.stat_image_mana.pos = self.stat_bar_mana.x + stat_bar_size[0] * 0.05, self.stat_bar_mana.y + stat_bar_size[1] * 0.05

        self.stat_label_mana.font_size = stat_image_size[1]
        self.stat_label_mana.texture_update()
        self.stat_label_mana.size = self.stat_label_mana.texture_size
        self.stat_label_mana.pos = self.stat_image_mana.x + stat_image_size[0] + (stat_bar_size[0] * 0.95 - stat_image_size[0] - self.stat_label_mana.width) / 2, self.stat_bar_mana.y + (stat_bar_size[1] - self.stat_label_mana.height) / 2

        self.stat_label_mana_number.font_size = stat_image_size[1]
        self.stat_label_mana_number.texture_update()
        self.stat_label_mana_number.size = self.stat_label_mana_number.texture_size
        self.stat_label_mana_number.pos = self.stat_bar_mana.x + overlay_size[0] * 0.25 - self.stat_label_mana_number.width, self.stat_bar_mana.y + (stat_bar_size[1] - self.stat_label_mana_number.height) / 2

        # Phy Attack
        self.stat_bar_phyattack.size = stat_bar_size
        self.stat_bar_phyattack.pos = stat_bar_start, start - stat_bar_size[1] * 3 - spacer * 2

        self.stat_image_phyattack.size = stat_image_size
        self.stat_image_phyattack.pos = self.stat_bar_phyattack.x + stat_bar_size[0] * 0.05, self.stat_bar_phyattack.y + stat_bar_size[1] * 0.05

        self.stat_label_phyattack.font_size = stat_image_size[1]
        self.stat_label_phyattack.texture_update()
        self.stat_label_phyattack.size = self.stat_label_phyattack.texture_size
        self.stat_label_phyattack.pos = self.stat_image_phyattack.x + stat_image_size[0] + (stat_bar_size[0] * 0.95 - stat_image_size[0] - self.stat_label_phyattack.width) / 2, self.stat_bar_phyattack.y + (stat_bar_size[1] - self.stat_label_phyattack.height) / 2

        self.stat_label_phyattack_number.font_size = stat_image_size[1]
        self.stat_label_phyattack_number.texture_update()
        self.stat_label_phyattack_number.size = self.stat_label_phyattack_number.texture_size
        self.stat_label_phyattack_number.pos = self.stat_bar_phyattack.x + overlay_size[0] * 0.25 - self.stat_label_phyattack_number.width, self.stat_bar_phyattack.y + (stat_bar_size[1] - self.stat_label_phyattack_number.height) / 2

        # Mag Attack
        self.stat_bar_magattack.size = stat_bar_size
        self.stat_bar_magattack.pos = stat_bar_start, start - stat_bar_size[1] * 4 - spacer * 3

        self.stat_image_magattack.size = stat_image_size
        self.stat_image_magattack.pos = self.stat_bar_magattack.x + stat_bar_size[0] * 0.05, self.stat_bar_magattack.y + stat_bar_size[1] * 0.05

        self.stat_label_magattack.font_size = stat_image_size[1]
        self.stat_label_magattack.texture_update()
        self.stat_label_magattack.size = self.stat_label_magattack.texture_size
        self.stat_label_magattack.pos = self.stat_image_magattack.x + stat_image_size[0] + (stat_bar_size[0] * 0.95 - stat_image_size[0] - self.stat_label_magattack.width) / 2, self.stat_bar_magattack.y + (stat_bar_size[1] - self.stat_label_magattack.height) / 2

        self.stat_label_magattack_number.font_size = stat_image_size[1]
        self.stat_label_magattack_number.texture_update()
        self.stat_label_magattack_number.size = self.stat_label_magattack_number.texture_size
        self.stat_label_magattack_number.pos = self.stat_bar_magattack.x + overlay_size[0] * 0.25 - self.stat_label_magattack_number.width, self.stat_bar_magattack.y + (stat_bar_size[1] - self.stat_label_magattack_number.height) / 2

        # Defense
        self.stat_bar_defense.size = stat_bar_size
        self.stat_bar_defense.pos = stat_bar_start, start - stat_bar_size[1] * 5 - spacer * 4

        self.stat_image_defense.size = stat_image_size
        self.stat_image_defense.pos = self.stat_bar_defense.x + stat_bar_size[0] * 0.05, self.stat_bar_defense.y + stat_bar_size[1] * 0.05

        self.stat_label_defense.font_size = stat_image_size[1]
        self.stat_label_defense.texture_update()
        self.stat_label_defense.size = self.stat_label_defense.texture_size
        self.stat_label_defense.pos = self.stat_image_defense.x + stat_image_size[0] + (stat_bar_size[0] * 0.95 - stat_image_size[0] - self.stat_label_defense.width) / 2, self.stat_bar_defense.y + (stat_bar_size[1] - self.stat_label_defense.height) / 2

        self.stat_label_defense_number.font_size = stat_image_size[1]
        self.stat_label_defense_number.texture_update()
        self.stat_label_defense_number.size = self.stat_label_defense_number.texture_size
        self.stat_label_defense_number.pos = self.stat_bar_defense.x + overlay_size[0] * 0.25 - self.stat_label_defense_number.width, self.stat_bar_defense.y + (stat_bar_size[1] - self.stat_label_defense_number.height) / 2

        # Rank Total Stats
        rank_overlay_size = overlay_size[0] * 0.25, start - self.stat_bar_defense.y
        rank_overlay_pos = overlay_pos[0] + overlay_size[0] * 0.375, start - rank_overlay_size[1]
        height = rank_overlay_size[1] / 6
        rank_image_size = rank_overlay_size[0] / 3, height * .85

        rank_stat_font_size = stat_image_size[1] * 1.1

        self.rank_total_overlay.size = rank_overlay_size
        self.rank_total_overlay.pos = rank_overlay_pos

        # Strength
        self.rank_total_strength_label.font_size = rank_stat_font_size
        self.rank_total_strength_label.texture_update()
        self.rank_total_strength_label.size = self.rank_total_strength_label.texture_size
        self.rank_total_strength_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 4.5

        self.rank_total_strength_image.size = rank_image_size
        self.rank_total_strength_image.pos = rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 4.5

        self.rank_total_strength_label_number.font_size = rank_stat_font_size
        self.rank_total_strength_label_number.texture_update()
        self.rank_total_strength_label_number.size = self.rank_total_strength_label_number.texture_size
        self.rank_total_strength_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_total_strength_label_number.width, rank_overlay_pos[1] + height * 4.5

        # Magic
        self.rank_total_magic_label.font_size = rank_stat_font_size
        self.rank_total_magic_label.texture_update()
        self.rank_total_magic_label.size = self.rank_total_magic_label.texture_size
        self.rank_total_magic_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 3.5

        self.rank_total_magic_image.size = rank_image_size
        self.rank_total_magic_image.pos = rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 3.5

        self.rank_total_magic_label_number.font_size = rank_stat_font_size
        self.rank_total_magic_label_number.texture_update()
        self.rank_total_magic_label_number.size = self.rank_total_magic_label_number.texture_size
        self.rank_total_magic_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_total_magic_label_number.width, rank_overlay_pos[1] + height * 3.5

        # Endurance
        self.rank_total_endurance_label.font_size = rank_stat_font_size
        self.rank_total_endurance_label.texture_update()
        self.rank_total_endurance_label.size = self.rank_total_endurance_label.texture_size
        self.rank_total_endurance_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 2.5

        self.rank_total_endurance_image.size = rank_image_size
        self.rank_total_endurance_image.pos = rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 2.5

        self.rank_total_endurance_label_number.font_size = rank_stat_font_size
        self.rank_total_endurance_label_number.texture_update()
        self.rank_total_endurance_label_number.size = self.rank_total_endurance_label_number.texture_size
        self.rank_total_endurance_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_total_endurance_label_number.width, rank_overlay_pos[1] + height * 2.5

        # Dexterity
        self.rank_total_dexterity_label.font_size = rank_stat_font_size
        self.rank_total_dexterity_label.texture_update()
        self.rank_total_dexterity_label.size = self.rank_total_dexterity_label.texture_size
        self.rank_total_dexterity_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 1.5

        self.rank_total_dexterity_image.size = rank_image_size
        self.rank_total_dexterity_image.pos = rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 1.5

        self.rank_total_dexterity_label_number.font_size = rank_stat_font_size
        self.rank_total_dexterity_label_number.texture_update()
        self.rank_total_dexterity_label_number.size = self.rank_total_dexterity_label_number.texture_size
        self.rank_total_dexterity_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_total_dexterity_label_number.width, rank_overlay_pos[1] + height * 1.5

        # Agility
        self.rank_total_agility_label.font_size = rank_stat_font_size
        self.rank_total_agility_label.texture_update()
        self.rank_total_agility_label.size = self.rank_total_agility_label.texture_size
        self.rank_total_agility_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 0.5

        self.rank_total_agility_image.size = rank_image_size
        self.rank_total_agility_image.pos = rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 0.5

        self.rank_total_agility_label_number.font_size = rank_stat_font_size
        self.rank_total_agility_label_number.texture_update()
        self.rank_total_agility_label_number.size = self.rank_total_agility_label_number.texture_size
        self.rank_total_agility_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_total_agility_label_number.width, rank_overlay_pos[1] + height * 0.5

        # Current Rank Overlay
        rank_overlay_pos = overlay_pos[0] + overlay_size[0] * 0.6875, start - rank_overlay_size[1]

        self.rank_current_overlay.size = rank_overlay_size
        self.rank_current_overlay.pos = rank_overlay_pos

        # Strength
        self.rank_current_strength_label.font_size = rank_stat_font_size
        self.rank_current_strength_label.texture_update()
        self.rank_current_strength_label.size = self.rank_current_strength_label.texture_size
        self.rank_current_strength_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 4.5

        self.rank_current_strength_image.size = rank_image_size
        self.rank_current_strength_image.pos = rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 4.5

        self.rank_current_strength_label_number.font_size = rank_stat_font_size
        self.rank_current_strength_label_number.texture_update()
        self.rank_current_strength_label_number.size = self.rank_current_strength_label_number.texture_size
        self.rank_current_strength_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_current_strength_label_number.width, rank_overlay_pos[1] + height * 4.5

        # Magic
        self.rank_current_magic_label.font_size = rank_stat_font_size
        self.rank_current_magic_label.texture_update()
        self.rank_current_magic_label.size = self.rank_current_magic_label.texture_size
        self.rank_current_magic_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 3.5

        self.rank_current_magic_image.size = rank_image_size
        self.rank_current_magic_image.pos = rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 3.5

        self.rank_current_magic_label_number.font_size = rank_stat_font_size
        self.rank_current_magic_label_number.texture_update()
        self.rank_current_magic_label_number.size = self.rank_current_magic_label_number.texture_size
        self.rank_current_magic_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_current_magic_label_number.width, rank_overlay_pos[1] + height * 3.5

        # Endurance
        self.rank_current_endurance_label.font_size = rank_stat_font_size
        self.rank_current_endurance_label.texture_update()
        self.rank_current_endurance_label.size = self.rank_current_endurance_label.texture_size
        self.rank_current_endurance_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 2.5

        self.rank_current_endurance_image.size = rank_image_size
        self.rank_current_endurance_image.pos = rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 2.5

        self.rank_current_endurance_label_number.font_size = rank_stat_font_size
        self.rank_current_endurance_label_number.texture_update()
        self.rank_current_endurance_label_number.size = self.rank_current_endurance_label_number.texture_size
        self.rank_current_endurance_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_current_endurance_label_number.width, rank_overlay_pos[1] + height * 2.5

        # Dexterity
        self.rank_current_dexterity_label.font_size = rank_stat_font_size
        self.rank_current_dexterity_label.texture_update()
        self.rank_current_dexterity_label.size = self.rank_current_dexterity_label.texture_size
        self.rank_current_dexterity_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 1.5

        self.rank_current_dexterity_image.size = rank_image_size
        self.rank_current_dexterity_image.pos = rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 1.5

        self.rank_current_dexterity_label_number.font_size = rank_stat_font_size
        self.rank_current_dexterity_label_number.texture_update()
        self.rank_current_dexterity_label_number.size = self.rank_current_dexterity_label_number.texture_size
        self.rank_current_dexterity_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_current_dexterity_label_number.width, rank_overlay_pos[1] + height * 1.5

        # Agility
        self.rank_current_agility_label.font_size = rank_stat_font_size
        self.rank_current_agility_label.texture_update()
        self.rank_current_agility_label.size = self.rank_current_agility_label.texture_size
        self.rank_current_agility_label.pos = rank_overlay_pos[0] + rank_overlay_size[0] * 0.0625, rank_overlay_pos[1] + height * 0.5

        self.rank_current_agility_image.size = rank_image_size
        self.rank_current_agility_image.pos = rank_overlay_pos[0] + (rank_overlay_size[0] - rank_image_size[0]) * 2 / 3, rank_overlay_pos[1] + height * 0.5

        self.rank_current_agility_label_number.font_size = rank_stat_font_size
        self.rank_current_agility_label_number.texture_update()
        self.rank_current_agility_label_number.size = self.rank_current_agility_label_number.texture_size
        self.rank_current_agility_label_number.pos = rank_overlay_pos[0] + rank_overlay_size[0] - rank_overlay_size[0] * 0.0625 - self.rank_current_agility_label_number.width, rank_overlay_pos[1] + height * 0.5

        # Equipment

        equipment_size = overlay_size[0] * 0.275, overlay_size[0] * 0.275 * 50 / 200

        self.weapon.size = equipment_size
        self.necklace.size = equipment_size
        self.ring.size = equipment_size
        self.helmet.size = equipment_size
        self.vambraces.size = equipment_size
        self.gloves.size = equipment_size
        self.chest.size = equipment_size
        self.leggings.size = equipment_size
        self.boots.size = equipment_size

        hgap = (overlay_size[0] - overlay_size[0] * 0.125 - equipment_size[0] * 3) / 2
        vgap = (overlay_size[1] * 0.2 - equipment_size[1] * 3) / 5
        self.equipment_layout.spacing = hgap, vgap
        self.equipment_layout.padding = [overlay_size[0] * 0.0625, vgap, overlay_size[0] * 0.0625, vgap]
        self.equipment_layout.size = overlay_size[0], equipment_size[1] * 4 + vgap * 5
        self.equipment_layout.pos = overlay_pos

        # Neat Stats
        gap = self.rank_total_overlay.y - self.equipment_layout.y - self.equipment_layout.height
        neat_stat_size = overlay_size[0] - overlay_size[0] * 0.125, gap * 0.9
        neat_stat_pos = overlay_pos[0] + overlay_size[0] * 0.0625, self.equipment_layout.y + self.equipment_layout.height + gap * 0.01

        neat_stat_font_size = neat_stat_size[1] * 0.3

        self.neat_stat_overlay.size = neat_stat_size
        self.neat_stat_overlay.pos = neat_stat_pos

        self.neat_stat_layout.size = neat_stat_size
        self.neat_stat_layout.pos = neat_stat_pos

        self.familia_label.font_size = neat_stat_font_size
        self.familia_label.size = neat_stat_size[0] / 3, neat_stat_size[1] / 3

        self.gender_label.font_size = neat_stat_font_size
        self.gender_label.size = neat_stat_size[0] / 3, neat_stat_size[1] / 3

        self.race_label.font_size = neat_stat_font_size
        self.race_label.size = neat_stat_size[0] / 3, neat_stat_size[1] / 3

        self.score_label.font_size = neat_stat_font_size
        self.score_label.size = neat_stat_size[0] / 3, neat_stat_size[1] / 3

        self.high_dmg_label.font_size = neat_stat_font_size
        self.high_dmg_label.size = neat_stat_size[0] / 3, neat_stat_size[1] / 3

        self.worth_label.font_size = neat_stat_font_size
        self.worth_label.size = neat_stat_size[0] / 3, neat_stat_size[1] / 3

        self.floor_depth_label.font_size = neat_stat_font_size
        self.floor_depth_label.size = neat_stat_size[0] / 3, neat_stat_size[1] / 3

        self.people_slain_label.font_size = neat_stat_font_size
        self.people_slain_label.size = neat_stat_size[0] / 3, neat_stat_size[1] / 3

        self.monsters_slain_label.font_size = neat_stat_font_size
        self.monsters_slain_label.size = neat_stat_size[0] / 3, neat_stat_size[1] / 3

        height = self.size[1] * 0.075
        spacer = self.size[0] * 0.025

        self.status_board.font_size = height * 0.4
        self.status_board.size = height * 570 / 215, height
        self.status_board.pos = overlay_pos[0] - spacer - height * 570 / 215, overlay_pos[1]

        self.change_equip.font_size = height * 0.4
        self.change_equip.size = height * 570 / 215, height
        self.change_equip.pos = overlay_pos[0] - spacer * 2 - self.status_board.width - height * 570 / 215, overlay_pos[1]

        self.image_preview.size = height * 300 / 188, height
        self.image_preview.pos = overlay_pos[0] - spacer * 3 - self.status_board.width - self.change_equip.width - height * 200 / 125, overlay_pos[1]

    def reload(self):
        if not self.initialized:
            return
        if not self.full_image_loaded:
            self.char_image = self.character.get_full_image(False)
            index = 0
            for child in self.children:
                if child.id == 'image_standin_slide':
                    self.children[index] = self.char_image
                    self.char_image.parent = self
                index += 1
            self.full_image_loaded = True
            self.char_image.size = self.size
            self.char_image.pos = self.pos

    def on_image_preview(self, instance):
        pass

    def on_status_board(self, instance):
        pass

    def on_change_equip(self, instance):
        pass

    def update_stars(self):
        count = 0
        for level in self.char.ranks:
            if level.unlocked:
                if not level.broken:
                    self.stars[count].opacity = 1
                else:
                    self.stars[count].source = '../res/screens/stats/rankbrk.png'
                    self.stars[count].opacity = 1
            count += 1
        self.preview.update_stars(self.char)

    def on_back_press(self, instance):
        if self.main_screen is not None:
            self.main_screen.display_screen(None, False, False)


class EquipmentSlot(Widget):
    initialized = BooleanProperty(False)
    item = ObjectProperty(None, allownone=True)

    color = ListProperty([0, 0, 0, 0])
    font = StringProperty(None)
    slot_name = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size = (0, 0)
        self._pos = (-1, -1)

        self.background = Image(source="../res/screens/attribute/equipment.png", size_hint=(None, None), allow_stretch=True)
        self.label = Label(text=self.slot_name.capitalize(), size_hint=(None, None), color=self.color, font_name=self.font)

        if self.item is not None:
            self.label_equip = Label(text=self.item.get_name(), size_hint=(None, None), color=self.color, font_name=self.font)
            self.image_equip = Image(source="../res/items/equipment/" + self.item.get_id() + ".png", size_hint=(None, None), allow_stretch=True)
            self.durability = DurabilityBar(max=self.item.get_durability(), value=self.item.get_current_durability())
        else:
            self.label_equip = Label(text="Not Equipped", size_hint=(None, None), color=self.color, font_name=self.font)
            self.image_equip = Image(source="../res/items/equipment/empty.png", size_hint=(None, None), allow_stretch=True, opacity=0)
            self.durability = DurabilityBar(value=700, max=1000, opacity=0)

        self.add_widget(self.background)
        self.add_widget(self.label)
        self.add_widget(self.label_equip)
        self.add_widget(self.image_equip)
        self.add_widget(self.durability)
        self.initialized = True

    def on_item(self, instance, item):
        if not self.initialized:
            return
        self.label_equip.opacity = 1
        self.image_equip.opacity = 1
        self.durability.opacity = 1

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size = size.copy()

        self.background.size = self.size

        self.label.font_size = self.height * 0.30
        self.label.texture_update()
        self.label.size = self.label.texture_size
        self.label.pos = self.x + 4 * self.width / 200, self.y + self.height - self.label.height - 12 * self.width / 200

        if self.item is not None:
            self.label_equip.size = self.width * 0.75, self.height * 0.85
        else:
            self.label_equip.size = self.width, self.height * 0.85
        self.label_equip.font_size = self.height * 0.30 * 1.25
        self.label_equip.pos = self.pos
        self.image_equip.size = self.width * 0.8, self.width * 0.8
        self.image_equip.pos = self.x + self.width - 4 * self.width / 200, self.y + self.height - 4 * self.width / 200
        self.durability.size = self.width - 8 * self.width / 200, self.height * 0.05
        self.durability.pos = self.x + 4 * self.width / 200, self.y + self.height * 0.175

    def on_pos(self, instance, pos):
        if not self.initialized or self._pos == pos:
            return
        self._pos = pos.copy()

        self.background.pos = self.pos
        self.label_equip.pos = self.pos
        self.label.pos = self.x + 4 * self.width / 200, self.y + self.height - self.label.height - 12 * self.width / 200

        self.image_equip.pos = self.x + self.width - 4 * self.width / 200, self.y + self.height - 4 * self.width / 200
        self.durability.pos = self.x + 4 * self.width / 200, self.y + self.height * 0.175

class DurabilityBar(Widget):
    max = NumericProperty(0.0)
    value = NumericProperty(0.0)
    opacity = NumericProperty(1)

    initialized = BooleanProperty(False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size = (0, 0)
        self._pos = (-1, -1)

        self.background = Image(source='../res/screens/stats/progress_background.png', allow_stretch=True, keep_ratio=False, opacity=self.opacity)
        self.clip = StencilView(size_hint=(None, None))
        self.foreground = Image(source='../res/screens/stats/progress_foreground.png', allow_stretch=True, keep_ratio=False, opacity=self.opacity)
        self.add_widget(self.background)
        self.add_widget(self.clip)
        self.clip.add_widget(self.foreground)
        self.initialized = True

    def on_size(self, instance, size):
        if not self.initialized or self._size == size:
            return
        self._size == size.copy()

        self.background.size = self.size
        self.foreground.size = self.size
        self.clip.size = self.width * (self.value / float(self.max)), self.height

    def on_pos(self, instance, pos):
        if not self.initialized or self._pos == pos:
            return
        self._pos == pos.copy()

        self.background.pos = self.pos
        self.foreground.pos = self.pos
        self.clip.pos = self.pos

    def on_opacity(self, instance, value):
        if not self.initialized:
            return

        self.background.opacity = 1
        self.foreground.opacity = 1