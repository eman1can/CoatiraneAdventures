from kivy.animation import Animation
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.app import App

from src.modules.HTButton import HTButton
from src.modules.KivyBase.Hoverable import ScreenBase as Screen, RelativeLayoutBase as RelativeLayout


class StatusBoardManager(Screen):
    char = ObjectProperty(None)

    overlay_background_source = StringProperty("../res/screens/attribute/stat_background.png")
    overlay_source = StringProperty("../res/screens/attribute/stat_background_overlay.png")

    skills_switch_text = StringProperty('Skills')
    current_board_name = StringProperty('Rank 1\nStatus Board')

    animation_left = ObjectProperty(None, allownone=True)
    animation_right = ObjectProperty(None, allownone=True)
    animate_distance = NumericProperty(100)
    animate_start_left = NumericProperty(5)
    animate_start_right = NumericProperty(95)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.root = DragSnapWidgetNew(main_screen=App.get_running_app())
        #
        sb = self.ids.status_board_screen
        ranks = self.char.get_grids()
        for rank in ranks:
            # drag = DragWidgetObject(drag_ratio=(1 / 4))
            # drag.root = GridWidget(self.character.get_current_rank(), grid=rank.grid)
            # drag.root._parent = self
            sb.add_widget(GridWidget(self.char.get_current_rank(), rank.grid, manager=self))
        sb.load_slide(sb.slides[self.char.get_current_rank() - 1])

    #     self.overlay_background = Image(source="../res/screens/attribute/stat_background.png", size_hint=(None, None), allow_stretch=True)
    #     self.overlay = Image(source="../res/screens/attribute/stat_background_overlay.png", size_hint=(None, None), allow_stretch=True)
    #
    #     self.total_abilities = Label(text="Total Abilities", size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')
    #     self.rank_abilities = Label(text="Rank Abilities", size_hint=(None, None), color=(0, 0, 0, 1), font_name='../res/fnt/Precious.ttf')
    #
    #     self.total_abilities_box = AbilityStatBox(color=(0, 0, 0, 1), font='../res/fnt/Gabriola.ttf',
    #                                               strength=self.character.get_strength(), strength_path=self.character.get_strength_rank(),
    #                                               magic=self.character.get_magic(), magic_path=self.character.get_magic_rank(),
    #                                               endurance=self.character.get_endurance(), endurance_path=self.character.get_endurance_rank(),
    #                                               dexterity=self.character.get_dexterity(), dexterity_path=self.character.get_dexterity_rank(),
    #                                               agility=self.character.get_agility(), agility_path=self.character.get_agility_rank())
    #
    #     self.current_abilities_box = AbilityStatBox(color=(0, 0, 0, 1), font='../res/fnt/Gabriola.ttf',
    #                                                 strength=self.character.get_strength(self.character.get_current_rank()), strength_path=self.character.get_strength_rank(self.character.get_current_rank()),
    #                                                 magic=self.character.get_magic(self.character.get_current_rank()), magic_path=self.character.get_magic_rank(self.character.get_current_rank()),
    #                                                 endurance=self.character.get_endurance(self.character.get_current_rank()), endurance_path=self.character.get_endurance_rank(self.character.get_current_rank()),
    #                                                 dexterity=self.character.get_dexterity(self.character.get_current_rank()), dexterity_path=self.character.get_dexterity_rank(self.character.get_current_rank()),
    #                                                 agility=self.character.get_agility(self.character.get_current_rank()), agility_path=self.character.get_agility_rank(self.character.get_current_rank()))
    #
    #     self.add_widget(self.background)
    #     # self.add_widget(self.root)
    #     self.add_widget(self.overlay_background)
    #     self.add_widget(self.overlay)
    #
    #     self.add_widget(self.total_abilities)
    #     self.add_widget(self.rank_abilities)
    #
    #     self.add_widget(self.total_abilities_box)
    #     self.add_widget(self.current_abilities_box)
    #
    #     self.add_widget(self.back_button)
    #     self.initialized = True
    #
    # def on_size(self, instance, size):
    #     if not self.initialized or self._size == size:
    #         return
    #     self._size = size.copy()
    #
    #     self.background.size = self.size
    #
    #     slot_size = self.height / 13
    #     spacer = (self.height - slot_size * 11) / 13
    #     msize = slot_size * 11 + spacer * 10
    #     overlay_size = self.width - msize - spacer * 3, (self.width - msize - spacer * 3) * 610 / 620
    #     overlay_pos = spacer, spacer
    #
    #     self.overlay_background.size = overlay_size
    #     self.overlay_background.pos = overlay_pos
    #
    #     self.overlay.size = overlay_size
    #     self.overlay.pos = overlay_pos
    #
    #     self.total_abilities.font_size = self.width * 0.0175
    #     self.total_abilities.texture_update()
    #     self.total_abilities.size = self.total_abilities.texture_size
    #     self.total_abilities.pos = overlay_pos[0] + (overlay_size[0] - self.total_abilities.width * 2) / 3, overlay_pos[1] + overlay_size[1] - self.total_abilities.height * 1.5
    #
    #     self.rank_abilities.font_size = self.width * 0.0175
    #     self.rank_abilities.texture_update()
    #     self.rank_abilities.size = self.rank_abilities.texture_size
    #     self.rank_abilities.pos = overlay_pos[0] + (overlay_size[0] - self.rank_abilities.width * 2) * 2 / 3 + self.total_abilities.width, overlay_pos[1] + overlay_size[1] - self.rank_abilities.height * 1.5
    #
    #     self.total_abilities_box.size = overlay_size[0] * 0.35, overlay_size[0] * 0.35 * 250 / 260
    #     spacer = (overlay_size[0] - self.total_abilities_box.width * 2) / 3
    #     self.total_abilities_box.pos = overlay_pos[0] + spacer, overlay_pos[1] + overlay_size[1] - self.total_abilities.height * 1.75 - self.total_abilities_box.height
    #
    #     self.current_abilities_box.size = overlay_size[0] * 0.35, overlay_size[0] * 0.35 * 250 / 260
    #     self.current_abilities_box.pos = overlay_pos[0] + spacer * 2 + self.total_abilities_box.width, overlay_pos[1] + overlay_size[1] - self.rank_abilities.height * 1.75 - self.current_abilities_box.height
    #
    #     self.back_button.size = self.width * .05, self.width * .05
    #     self.back_button.pos = 0, self.height - self.back_button.height

        # self.root.size = self.size

    def on_skills_switch(self):
        if self.skills_switch_text == 'Skills':
            self.skills_switch_text = 'Status'
        else:
            self.skills_switch_text = 'Skills'
        self.ids.normal_layout.opacity = int(not bool(int(self.ids.normal_layout.opacity)))
        self.ids.skill_layout.opacity = int(not bool(int(self.ids.skill_layout.opacity)))
        self.ids.skillslist.scroll_y = 1
        self.ids.skillslist.update_from_scroll()

    def on_board_move(self, index):
        self.current_board_name = f'Rank {index + 1}\nStatus Board'
        if index != 0 and index != 9:
            if not self.animation_left.repeat or not self.animation_right.repeat:
                self.animation_left.cancel(self.ids.left_arrow)
                self.animation_right.cancel(self.ids.right_arrow)
                self.animate_left_arrow()
                self.animate_right_arrow()
        elif index == 0:
            self.unanimate_left_arrow()
        else:
            self.unanimate_right_arrow()

    def on_arrow_touch(self, direction):
        if direction:
            self.ids.status_board_screen.load_previous()
        else:
            self.ids.status_board_screen.load_next()

    def animate_arrows(self, index=0):
        self.ensure_creation()
        if index > 0:
            self.animate_left_arrow()
        if index < 9:
            self.animate_right_arrow()

    def ensure_creation(self):
        if self.animation_left is None or self.animation_right is None:
            self.animation_left = Animation(x=self.animate_start_left - self.animate_distance, duration=1) + Animation(x=self.animate_start_left, duration=0.25)
            self.animation_right = Animation(x=self.animate_start_right + self.animate_distance, duration=1) + Animation(x=self.animate_start_right, duration=0.25)

    def unanimate_arrows(self):
        self.unanimate_left_arrow()
        self.unanimate_right_arrow()

    def unanimate_left_arrow(self):
        if self.animation_left is None:
            return
        self.animation_left.cancel(self.ids.left_arrow)
        self.animation_left.repeat = False

    def animate_left_arrow(self):
        if self.animation_left is None:
            return
        self.animation_left.repeat = True
        self.animation_left.start(self.ids.left_arrow)

    def unanimate_right_arrow(self):
        if self.animation_right is None:
            return
        self.animation_right.cancel(self.ids.right_arrow)
        self.animation_right.repeat = False

    def animate_right_arrow(self):
        if self.animation_right is None:
            return
        self.animation_right.repeat = True
        self.animation_right.start(self.ids.right_arrow)

    def on_enter(self, *args):
        self.animate_arrows(self.ids.status_board_screen._get_index())

    def on_leave(self, *args):
        self.unanimate_arrows()

    def on_release(self, type, slot_num):
        rank = self.char.get_rank(slot_num)

        if type == 'strength':
            rank.update_strength(rank.grid.amounts[0], True)
            self.total_abilities_box.strength = self.char.get_strength()
            self.current_abilities_box.strength = self.char.get_strength(self.char.get_current_rank())
        elif type == 'magic':
            rank.update_magic(rank.grid.amounts[1], True)
            self.total_abilities_box.magic = self.char.get_magic()
            self.current_abilities_box.magic = self.char.get_magic(self.char.get_current_rank())
        elif type == 'endurance':
            rank.update_endurance(rank.grid.amounts[2], True)
            self.total_abilities_box.endurance = self.char.get_endurance()
            self.current_abilities_box.endurance = self.char.get_endurance(self.char.get_current_rank())
        elif type == 'dexterity':
            rank.update_dexterity(rank.grid.amounts[3], True)
            self.total_abilities_box.dexterity = self.char.get_dexterity()
            self.current_abilities_box.dexterity = self.char.get_dexterity(self.char.get_current_rank())
        elif type == 'agility':
            rank.update_agility(rank.grid.amounts[4], True)
            self.total_abilities_box.agility = self.char.get_agility()
            self.current_abilities_box.agility = self.char.get_agility(self.char.get_current_rank())
        else:
            raise Exception("Unknown slot releasing")
        self.total_abilities_box.reload()
        self.current_abilities_box.reload()
        #Update item count when applicable


class GridWidget(RelativeLayout):
#     initialized = BooleanProperty(False)
    grid = ObjectProperty(None)
    manager = ObjectProperty(None)

    slots = ListProperty([])
    titles = ListProperty([])
    offsets = ListProperty([])
    toffsets = ListProperty([])

    overlay_background_source = StringProperty("../res/screens/attribute/stat_background.png")
    overlay_source = StringProperty("../res/screens/attribute/stat_background_overlay.png")
#
    def __init__(self, rank, grid, **kwargs):  # number, managerPass, rank, char, grid
        self.grid = grid
        super().__init__(**kwargs)

        index = 0
        y_i = len(self.grid.grid) - 1
        pos_hint_x, pos_hint_y = 0.5, 0.5 + y_i * 0.03125 + y_i * 0.00625
        for r, row in enumerate(self.grid.grid):
            list = []
            offsets = []
            for c, column in enumerate(row):
                slot_unlocked = self.grid.unlocked[r][c]
                #title = Label(text="Rank " + str(self.grid.index), size_hint=(None, None), color=(0, 0, 0, 1), font_name="../res/fnt/Precious.ttf")
                disabled = self.grid.index > rank
                if column == 'S':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.0625, 0.0625), path="../res/screens/status/slot_strength", collide_image="../res/screens/status/slot.collision.png", background_hover_down="../res/screens/status/slot_strength.down.png", toggle_state=slot_unlocked)
                    slot.bind(on_release=lambda instance: self.manager.on_release('strength', self.grid.index))
                elif column == 'M':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.0625, 0.0625), path="../res/screens/status/slot_magic", collide_image="../res/screens/status/slot.collision.png", background_hover_down="../res/screens/status/slot_magic.down.png", toggle_state=slot_unlocked)
                    slot.bind(on_release=lambda instance: self.manager.on_release('magic', self.grid.index))
                elif column == 'E':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.0625, 0.0625), path="../res/screens/status/slot_endurance", collide_image="../res/screens/status/slot.collision.png", background_hover_down="../res/screens/status/slot_endurance.down.png", toggle_state=slot_unlocked)
                    slot.bind(on_release=lambda instance: self.manager.on_release('endurance', self.grid.index))
                elif column == 'D':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.0625, 0.0625), path="../res/screens/status/slot_dexterity", collide_image="../res/screens/status/slot.collision.png", background_hover_down="../res/screens/status/slot_dexterity.down.png", toggle_state=slot_unlocked)
                    slot.bind(on_release=lambda instance: self.manager.on_release('dexterity', self.grid.index))
                else:
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.0625, 0.0625), path="../res/screens/status/slot_agility", collide_image="../res/screens/status/slot.collision.png", background_hover_down="../res/screens/status/slot_agility.down.png", toggle_state=slot_unlocked)
                    slot.bind(on_release=lambda instance: self.manager.on_release('agility', self.grid.index))
                # print(index, r, c, column, pos_hint_x, pos_hint_y)
                pos_hint_x += 0.00625 + 0.03125
                pos_hint_y -= 0.00625 + 0.03125

                slot.disabled = disabled
                list.append(slot)
                index += 1
                offsets.append((0, 0))
                #self.titles.append(title)
                self.toffsets.append((0, 0))
                self.add_widget(slot)
                #self.add_widget(title)
            pos_hint_x -= (0.00625 + 0.03125) * (len(row) + 1)
            pos_hint_y += (0.00625 + 0.03125) * (len(row) - 1)
            self.slots.append(list)
            self.offsets.append(offsets)




#         self.initialized = True
#
#     def on_size(self, instance, size):
#         if not self.initialized or self._size == size:
#             return
#         self._size = size.copy()
#
#
#
#         length = len(self.grid.grid[0])
#         slot_size = self.height / 13
#         spacer = (self.height - slot_size * 11) / 13
#         msize = slot_size * 11 + spacer * 10
#         tsize = slot_size * length + spacer * (length - 1)
#         x, y = self.width - spacer - msize/2 - slot_size / 2, self.height - (self.height - tsize) / 2 - slot_size - spacer
#
#         for i, title in enumerate(self.titles):
#             title.font_size = self.height * 0.1
#             title.texture_update()
#             title.size = title.texture_size
#             title.pos = self.x + self.width - msize - title.width, self.y + self.height - title.height * 1.25
#             self.toffsets[i] = (self.width - msize, self.height - title.height * 1.25)
#
#         for r, (row, offsets) in enumerate(zip(self.slots, self.offsets)):
#             for c, (column, offset) in enumerate(zip(row, offsets)):
#                 column.size = slot_size, slot_size
#                 column.pos = self.x + x, self.y + y
#                 self.offsets[r][c] = (x, y)
#
#                 x += slot_size / 2 + spacer / 2
#                 y -= (slot_size / 2 + spacer / 2)
#             x -= (slot_size * float(len(row) + 1) / 2 + float(spacer * (len(row) + 1)) / 2)
#             y += slot_size * float(len(row) - 1) / 2 + spacer * float(len(row) - 1) / 2
#
#     def on_pos(self, instance, pos):
#         if not self.initialized or self._pos == pos:
#             return
#         self._pos = pos.copy()
#
#         for title, offset in zip(self.titles, self.toffsets):
#             title.pos = self.x + offset[0], self.y + offset[1]
#
#         for row, offsets in zip(self.slots, self.offsets):
#             for column, offset in zip(row, offsets):
#                 column.pos = self.x + offset[0], self.y + offset[1]
#
#     def on_mouse_pos(self, hover):
#         if not self.collide_point(*hover.pos):
#             return False
#         for slots in self.slots:
#             for slot in slots:
#                 if slot.dispatch('on_mouse_pos', hover):
#                     return True
#         return False

    # def slotPressed(self, instance, touch):
    #     if instance.collide_point(*touch.pos):
    #         if self.currentSlot == None:
    #             # print(str(instance))
    #             if not instance.opened:
    #                 # print("slot pressed")
    #                 # print("True")
    #                 self.currentSlot = instance
    #                 self.confirm = Label(id='confirm_box', text='Are you sure?', size=(300, 150), font_size=50,
    #                                      pos=(0, 390), size_hint=(None, None), color=(1, 1, 1, 1))
    #                 with self.confirm.canvas.before:
    #                     Color(.1, .1, .1, .9)
    #                     Rectangle(size=(300, 150), pos=(self.confirm.x, self.confirm.y - 25))
    #                 yes = Button(text='unlock', color=(1, 1, 1, 1), size=(100, 45), font_size=30,
    #                              pos=(self.confirm.x + 300 - 75 - 75 / 2, self.confirm.y), on_touch_down=self.onConfirm)
    #                 no = Button(text='cancel', color=(1, 1, 1, 1), size=(100, 45), font_size=30,
    #                             pos=(self.confirm.x + 75 - 75 / 2, self.confirm.y), on_touch_down=self.onCancel)
    #                 self.confirm.add_widget(yes)
    #                 self.confirm.add_widget(no)
    #                 self.add_widget(self.confirm)
    #                 # print(str(self))
    #
    # def unlockAll(self, instance, touch):
    #     if instance.collide_point(*touch.pos):
    #         self.confirm = Label(id='confirm_box', text='Are you sure?', size=(300, 150), font_size=50,
    #                              center=(200, 400), size_hint=(None, None), color=(1, 1, 1, 1))
    #         with self.confirm.canvas.before:
    #             Color(.1, .1, .1, .9)
    #             Rectangle(size=(300, 150), pos=(self.confirm.x, self.confirm.y - 25))
    #         yes = Button(text='unlock', color=(1, 1, 1, 1), size=(100, 45), font_size=30,
    #                      pos=(self.confirm.x + 300 - 75 - 75 / 2, self.confirm.y), on_touch_down=self.onConfirmAll)
    #         no = Button(text='cancel', color=(1, 1, 1, 1), size=(100, 45), font_size=30,
    #                     pos=(self.confirm.x + 75 - 75 / 2, self.confirm.y), on_touch_down=self.onCancel)
    #         self.confirm.add_widget(yes)
    #         self.confirm.add_widget(no)
    #         self.add_widget(self.confirm)
    #
    # def unlockAllNum(self):
    #     for x in self.slots:
    #         if not x.opened:
    #             source = x.source[:-4]
    #             source += 'Unlocked.png'
    #             if x.slottype == 1:
    #                 self.rank.updateValues(0, 0, 0, self.rank.grid.SW, 0, 0, 0, 0)
    #             elif x.slottype == 2:
    #                 self.rank.updateValues(0, 0, 0, 0, self.rank.grid.MW, 0, 0, 0)
    #             elif x.slottype == 3:
    #                 self.rank.updateValues(0, 0, 0, 0, 0, self.rank.grid.AW, 0, 0)
    #             elif x.slottype == 4:
    #                 self.rank.updateValues(0, 0, 0, 0, 0, 0, self.rank.grid.DW, 0)
    #             elif x.slottype == 5:
    #                 self.rank.updateValues(0, 0, 0, 0, 0, 0, 0, self.rank.grid.EW)
    #             self.char.updateCharValues()
    #             self.managerObject.parent.parent.updateRankLabels()
    #             self.managerObject.parent.parent.updateRankPreviewLabels(self.rank.rankNum)
    #             x.source = source
    #             x.opened = True
    #
    # def onConfirmAll(self, instance, touch):
    #     if instance.collide_point(*touch.pos):
    #         for x in self.slots:
    #             if not x.opened:
    #                 source = x.source[:-4]
    #                 source += 'Unlocked.png'
    #                 if x.slottype == 1:
    #                     self.rank.updateValues(0, 0, 0, self.rank.grid.SW, 0, 0, 0, 0)
    #                 elif x.slottype == 2:
    #                     self.rank.updateValues(0, 0, 0, 0, self.rank.grid.MW, 0, 0, 0)
    #                 elif x.slottype == 3:
    #                     self.rank.updateValues(0, 0, 0, 0, 0, self.rank.grid.AW, 0, 0)
    #                 elif x.slottype == 4:
    #                     self.rank.updateValues(0, 0, 0, 0, 0, 0, self.rank.grid.DW, 0)
    #                 elif x.slottype == 5:
    #                     self.rank.updateValues(0, 0, 0, 0, 0, 0, 0, self.rank.grid.EW)
    #                 self.char.updateCharValues()
    #                 self.managerObject.parent.parent.updateRankLabels()
    #                 self.managerObject.parent.parent.updateRankPreviewLabels(self.rank.rankNum)
    #                 x.source = source
    #                 x.opened = True
    #         self.remove_widget(self.confirm)
    #         self.remove_widget(self.unlockAllButton)
    #
    # def onCancel(self, instance, touch):
    #     if instance.collide_point(*touch.pos):
    #         # print("Canceled")
    #         # print(str(self))
    #         self.currentSlot = None
    #         self.remove_widget(self.confirm)
    #
    # def onConfirm(self, instance, touch):
    #     if instance.collide_point(*touch.pos):
    #         if not self.currentSlot.opened:
    #             source = self.currentSlot.source[:-4]
    #             source += 'Unlocked.png'
    #             self.currentSlot.source = source
    #             # print("opened slot")
    #             if self.currentSlot.slottype == 1:
    #                 self.rank.updateValues(0, 0, 0, self.rank.grid.SW, 0, 0, 0, 0)
    #             elif self.currentSlot.slottype == 2:
    #                 self.rank.updateValues(0, 0, 0, 0, self.rank.grid.MW, 0, 0, 0)
    #             elif self.currentSlot.slottype == 3:
    #                 self.rank.updateValues(0, 0, 0, 0, 0, self.rank.grid.AW, 0, 0)
    #             elif self.currentSlot.slottype == 4:
    #                 self.rank.updateValues(0, 0, 0, 0, 0, 0, self.rank.grid.DW, 0)
    #             elif self.currentSlot.slottype == 5:
    #                 self.rank.updateValues(0, 0, 0, 0, 0, 0, 0, self.rank.grid.EW)
    #             self.char.updateCharValues()
    #             self.managerObject.parent.parent.updateRankLabels()
    #             self.managerObject.parent.parent.updateRankPreviewLabels(self.rank.rankNum)
    #             self.currentSlot.opened = True
    #             self.currentSlot = None
    #             self.remove_widget(self.confirm)


class CustomSlot(HTButton):

    def __init__(self, **kwargs):
        super().__init__(toggle_enabled=True, **kwargs)

    def _do_press(self):
        if self.toggle_enabled:
            self.toggle_state = True
            if not self.state.startswith('hover'):
                self.state = 'down' if self.toggle_state else 'normal'
            else:
                if self.do_hover:
                    self.state = 'hover_down' if self.toggle_state else 'hover_normal'
        else:
            self.state = 'down'
#
# class StatLabel(Label):
#
#     def __init__(self, **kwargs):
#         super(StatLabel, self).__init__(**kwargs)
#         if self.font_size != 60 and self.font_size != 50:
#             self.font_size = 40
#
#
# class StatPreview(Image):
#
#     def __init__(self, char, rank, attacktype, totalstats, physicalattack, magicalattack, magicalpoints, health,
#                  defense, strength, magic, agility, dexterity, endurance, **kwargs):
#         super(StatPreview, self).__init__(**kwargs)
#         self.source = "../res/screens/stats/TotalSingleAttackWindow.png"
#         self.size_hint = None, None
#         self.allow_stretch = True
#         self.keep_ratio = False
#         x = self.x + 10
#         y = self.y + self.height * .85
#         # size: app.size
#         # allow_stretch: True
#         # keep_ratio: False
#         # source: 'res/TotalSingleAttackWindow'
#
#         if totalstats:
#             y -= 25
#             x += 10
#             barwidth = 166
#             barheight = (self.height * .85) / 5
#             self.add_widget(Label(text="Total   Stats", color=(.1, .1, .1, 1), font_size=40, pos=(x + 55, y - 10)))
#             y -= (barheight / 2 - 10) + 25
#             self.add_widget(Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                                   allow_stretch=True))
#             self.add_widget(Image(source='../res/screens/stats/Health.png', size=(40, 40), pos=(x + 15, y + 5)))
#             self.healthlabel = StatLabel(text='HP')
#             self.healthlabel.x = x + 65
#             self.healthlabel.y = y
#             self.healthlabelnumber = StatLabel(text='%d' % health, color=(0, 0, 0, 1))
#             self.healthlabelnumber.x = x + 190
#             self.healthlabelnumber.y = y
#             self.healthlabeldiff = StatLabel(text='(+ 0)', color=(.3, .4, .6, 1))
#             self.healthlabeldiff.x = x + 310
#             self.healthlabeldiff.y = y
#             self.add_widget(self.healthlabelnumber)
#             self.add_widget(self.healthlabeldiff)
#             self.add_widget(self.healthlabel)
#
#             y -= (barheight + 5)
#             self.add_widget(Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                                   allow_stretch=True))
#             self.add_widget(Image(source='../res/screens/stats/Mana.png', size=(40, 40), pos=(x + 15, y + 5)))
#             self.magicalpointlabel = StatLabel(text='MP')
#             self.magicalpointlabel.x = x + 65
#             self.magicalpointlabel.y = y
#             self.magicalpointlabelnumber = StatLabel(text='%d' % magicalpoints, color=(0, 0, 0, 1))
#             self.magicalpointlabelnumber.x = x + 190
#             self.magicalpointlabelnumber.y = y
#             self.magicalpointlabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
#             self.magicalpointlabeldiff.x = x + 310
#             self.magicalpointlabeldiff.y = y
#             self.add_widget(self.magicalpointlabelnumber)
#             self.add_widget(self.magicalpointlabeldiff)
#             self.add_widget(self.magicalpointlabel)
#
#             y -= (barheight + 5)
#             if attacktype == 1:
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.add_widget(Image(source='../res/screens/stats/PhysicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
#                 self.attacklabel = StatLabel(text='P.Atk')
#                 self.attacklabel.x = x + 65
#                 self.attacklabel.y = y
#                 self.attacklabelnumber = StatLabel(text='%d' % physicalattack, color=(0, 0, 0, 1))
#                 self.attacklabelnumber.x = x + 190
#                 self.attacklabelnumber.y = y
#                 self.attacklabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
#                 self.attacklabeldiff.x = x + 310
#                 self.attacklabeldiff.y = y
#                 self.add_widget(self.attacklabelnumber)
#                 self.add_widget(self.attacklabeldiff)
#                 self.add_widget(self.attacklabel)
#             elif attacktype == 2:
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.add_widget(Image(source='../res/screens/stats/MagicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
#                 self.attacklabel2 = StatLabel(text='M.Atk')
#                 self.attacklabel2.x = x + 65
#                 self.attacklabel2.y = y
#                 self.attacklabel2number = StatLabel(text='%d' % magicalattack, color=(0, 0, 0, 1))
#                 self.attacklabel2number.x = x + 190
#                 self.attacklabel2number.y = y
#                 self.attacklabel2diff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
#                 self.attacklabel2diff.x = x + 310
#                 self.attacklabel2diff.y = y
#                 self.add_widget(self.attacklabel2number)
#                 self.add_widget(self.attacklabel2diff)
#                 self.add_widget(self.attacklabel2)
#             else:
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.add_widget(Image(source='../res/screens/stats/PhysicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
#                 self.attacklabel = StatLabel(text='P.Atk')
#                 self.attacklabel.x = x + 65
#                 self.attacklabel.y = y
#                 self.attacklabelnumber = StatLabel(text='%d' % physicalattack, color=(0, 0, 0, 1))
#                 self.attacklabelnumber.x = x + 190
#                 self.attacklabelnumber.y = y
#                 self.attacklabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
#                 self.attacklabeldiff.x = x + 310
#                 self.attacklabeldiff.y = y
#                 self.add_widget(self.attacklabelnumber)
#                 self.add_widget(self.attacklabeldiff)
#                 self.add_widget(self.attacklabel)
#                 y -= (barheight + 5)
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.add_widget(Image(source='../res/screens/stats/magicalAttack.png', size=(40, 40), pos=(x + 15, y + 5)))
#                 self.attacklabel2 = StatLabel(text='M.Atk')
#                 self.attacklabel2.x = x + 65
#                 self.attacklabel2.y = y
#                 self.attacklabel2number = StatLabel(text='%d' % magicalattack, color=(0, 0, 0, 1))
#                 self.attacklabel2number.x = x + 190
#                 self.attacklabel2number.y = y
#                 self.attacklabel2diff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
#                 self.attacklabel2diff.x = x + 310
#                 self.attacklabel2diff.y = y
#                 self.add_widget(self.attacklabel2number)
#                 self.add_widget(self.attacklabel2diff)
#                 self.add_widget(self.attacklabel2)
#             y -= (barheight + 5)
#             self.add_widget(Image(source='../res/screens/stats/StatBar.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                                   allow_stretch=True))
#             self.add_widget(Image(source='../res/screens/stats/Defense.png', size=(40, 40), pos=(x + 15, y + 5)))
#             self.defenselabel = StatLabel(text='Def')
#             self.defenselabel.x = x + 65
#             self.defenselabel.y = y
#             self.defenselabelnumber = StatLabel(text='%d' % defense, color=(0, 0, 0, 1))
#             self.defenselabelnumber.x = x + 190
#             self.defenselabelnumber.y = y
#
#             self.defenselabeldiff = StatLabel(text='(+0)', color=(.3, .4, .6, 1))
#             self.defenselabeldiff.x = x + 310
#             self.defenselabeldiff.y = y
#             self.add_widget(self.defenselabelnumber)
#             self.add_widget(self.defenselabeldiff)
#             self.add_widget(self.defenselabel)
#             y += 200
#             x += 470
#             barwidth = 330
#             barheight = 60
#             if attacktype == 1:
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.strengthlabel = StatLabel(text='Str.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#                 # print(str(strength))
#                 # print(str(char.ranks[9].strengthMax))
#                 self.strengthgrade = Image(source=Scale.getScaleAsImagePath(strength, char.totalCaps[0]),
#                                            pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
#                 self.strengthnumber = StatLabel(text='%d' % strength, font_size=50, color=(0, 0, 0, 1),
#                                                 pos=(x + 180, y))
#                 self.add_widget(self.strengthgrade)
#                 self.add_widget(self.strengthlabel)
#                 self.add_widget(self.strengthnumber)
#             elif attacktype == 2:
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.magiclabel = StatLabel(text='Mag.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#                 self.magicgrade = Image(source=Scale.getScaleAsImagePath(magic, char.totalCaps[1]),
#                                         pos=(x + 90, y + 10),
#                                         height=40, keep_ratio=True, allow_stretch=True)
#                 self.magicnumber = StatLabel(text='%d' % magic, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
#                 self.add_widget(self.magicgrade)
#                 self.add_widget(self.magiclabel)
#                 self.add_widget(self.magicnumber)
#             else:
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.strengthlabel = StatLabel(text='Str.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#                 self.strengthgrade = Image(source=Scale.getScaleAsImagePath(strength, char.totalCaps[0]),
#                                            pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
#                 self.strengthnumber = StatLabel(text='%d' % strength, font_size=50, color=(0, 0, 0, 1),
#                                                 pos=(x + 180, y))
#                 self.add_widget(self.strengthgrade)
#                 self.add_widget(self.strengthlabel)
#                 self.add_widget(self.strengthnumber)
#                 y -= 70
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.magiclabel = StatLabel(text='Mag.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#                 self.magicgrade = Image(source=Scale.getScaleAsImagePath(magic, char.totalCaps[1]),
#                                         pos=(x + 90, y + 10),
#                                         height=40, keep_ratio=True, allow_stretch=True)
#                 self.magicnumber = StatLabel(text='%d' % magic, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
#                 self.add_widget(self.magicgrade)
#                 self.add_widget(self.magiclabel)
#                 self.add_widget(self.magicnumber)
#             y -= 70
#             self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                                   allow_stretch=True))
#             self.agilitylabel = StatLabel(text='Agi.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#             self.agilitygrade = Image(source=Scale.getScaleAsImagePath(agility, char.totalCaps[2]),
#                                       pos=(x + 90, y + 10),
#                                       height=40, keep_ratio=True, allow_stretch=True)
#             self.agilitynumber = StatLabel(text='%d' % agility, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
#             self.add_widget(self.agilitygrade)
#             self.add_widget(self.agilitylabel)
#             self.add_widget(self.agilitynumber)
#             y -= 70
#             self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                                   allow_stretch=True))
#             self.dexteritylabel = StatLabel(text='Dex.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#             self.dexteritygrade = Image(source=Scale.getScaleAsImagePath(dexterity, char.totalCaps[3]),
#                                         pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
#             self.dexteritynumber = StatLabel(text='%d' % dexterity, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
#             self.add_widget(self.dexteritygrade)
#             self.add_widget(self.dexteritylabel)
#             self.add_widget(self.dexteritynumber)
#             y -= 70
#             self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                                   allow_stretch=True))
#             self.endurancelabel = StatLabel(text='End.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#             self.endurancegrade = Image(source=Scale.getScaleAsImagePath(endurance, char.totalCaps[4]),
#                                         pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
#             self.endurancenumber = StatLabel(text='%d' % endurance, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
#             self.add_widget(self.endurancegrade)
#             self.add_widget(self.endurancelabel)
#             self.add_widget(self.endurancenumber)
#             y += 200
#             x += 470
#             # self.healthLvlBar = ProgressBar(max = 120, value = 0, pos =(x, y), width = 200, height =25)
#             # self.mpLvlBar = ProgressBar(max = 120, value = 0, pos= (x,y), width = 200, height = 25)
#             # Health Exp Bar
#             self.healthLvlBar = ProgressBar(1, (275, 25))
#             self.healthLvlBar.max = char.ranks[char.currentRank - 1].expHpCap
#             self.healthLvlBar.value = char.ranks[char.currentRank - 1].exphealth
#             self.healthLvlBar.pos = 890, 190
#             self.healthLvlTitle = Label(text='HP', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 200))
#             self.healthLvlTitle.size = self.healthLvlTitle.texture_size
#             self.add_widget(self.healthLvlBar)
#             self.add_widget(self.healthLvlTitle)
#             # Mp Exp Bar
#             self.mpLvlBar = ProgressBar(2, (275, 25))
#             self.mpLvlBar.max = char.ranks[char.currentRank - 1].expMpCap
#             self.mpLvlBar.value = char.ranks[char.currentRank - 1].expmagicalpoints
#             self.mpLvlBar.pos = 890, 160
#             self.mpLvlTitle = Label(text='MP', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 170))
#             self.mpLvlTitle.size = self.mpLvlTitle.texture_size
#             self.add_widget(self.mpLvlBar)
#             self.add_widget(self.mpLvlTitle)
#             # Def Exp Bar
#             self.defLvlBar = ProgressBar(0, (275, 25))
#             self.defLvlBar.max = char.ranks[char.currentRank - 1].expDefCap
#             self.defLvlBar.value = char.ranks[char.currentRank - 1].expdefense
#             self.defLvlBar.pos = 890, 130
#             self.defLvlTitle = Label(text='Def', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 140))
#             self.defLvlTitle.size = self.defLvlTitle.texture_size
#             self.add_widget(self.defLvlBar)
#             self.add_widget(self.defLvlTitle)
#             # Str Exp Bar
#             self.strLvlBar = ProgressBar(1, (275, 25))
#             self.strLvlBar.max = char.ranks[char.currentRank - 1].expStrCap
#             self.strLvlBar.value = char.ranks[char.currentRank - 1].expstrength
#             self.strLvlBar.pos = 890, 100
#             self.strLvlTitle = Label(text='Str', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 110))
#             self.strLvlTitle.size = self.strLvlTitle.texture_size
#             self.add_widget(self.strLvlBar)
#             self.add_widget(self.strLvlTitle)
#             # Agi Exp Bar
#             self.agiLvlBar = ProgressBar(3, (275, 25))
#             self.agiLvlBar.max = char.ranks[char.currentRank - 1].expAgiCap
#             self.agiLvlBar.value = char.ranks[char.currentRank - 1].expagility
#             self.agiLvlBar.pos = 890, 70
#             self.agiLvlTitle = Label(text='Agi', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 80))
#             self.agiLvlTitle.size = self.agiLvlTitle.texture_size
#             self.add_widget(self.agiLvlBar)
#             self.add_widget(self.agiLvlTitle)
#             # Dex Exp Bar
#             self.dexLvlBar = ProgressBar(4, (275, 25))
#             self.dexLvlBar.max = char.ranks[char.currentRank - 1].expDexCap
#             self.dexLvlBar.value = char.ranks[char.currentRank - 1].expdexterity
#             self.dexLvlBar.pos = 890, 40
#             self.dexLvlTitle = Label(text='Dex', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 50))
#             self.dexLvlTitle.size = self.dexLvlTitle.texture_size
#             self.add_widget(self.dexLvlBar)
#             self.add_widget(self.dexLvlTitle)
#             # End Exp Bar
#             self.endLvlBar = ProgressBar(5, (275, 25))
#             self.endLvlBar.max = char.ranks[char.currentRank - 1].expEndCap
#             self.endLvlBar.value = char.ranks[char.currentRank - 1].expendurance
#             self.endLvlBar.pos = 890, 10
#             self.endLvlTitle = Label(text='End', font_size=30, color=(0, 0, 0, 1), size=(50, 20), pos=(860, 20))
#             self.endLvlTitle.size = self.endLvlTitle.texture_size
#             self.add_widget(self.endLvlBar)
#             self.add_widget(self.endLvlTitle)
#             # self.add_widget(self.mpLvlBar)
#         if not totalstats:
#             y -= 50
#             self.add_widget(Label(text="Rank Attributes", color=(.1, .1, .1, 1), font_size=40, pos=(x + 90, y + 20)))
#             barwidth = 330
#             barheight = 60
#             y -= 15
#             if attacktype == 1:
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.strengthlabel = StatLabel(text='Str.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#                 self.strengthgrade = Image(source=Scale.getScaleAsImagePath(strength, char.ranks[rank - 1].strengthMax),
#                                            pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
#                 self.strengthnumber = StatLabel(text='%d' % strength, font_size=50, color=(0, 0, 0, 1),
#                                                 pos=(x + 180, y))
#                 self.add_widget(self.strengthgrade)
#                 self.add_widget(self.strengthlabel)
#                 self.add_widget(self.strengthnumber)
#             elif attacktype == 2:
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.magiclabel = StatLabel(text='Mag.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#                 self.magicgrade = Image(source=Scale.getScaleAsImagePath(magic, char.ranks[rank - 1].magicMax),
#                                         pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
#                 self.magicnumber = StatLabel(text='%d' % magic, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
#                 self.add_widget(self.magicgrade)
#                 self.add_widget(self.magiclabel)
#                 self.add_widget(self.magicnumber)
#             else:
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.strengthlabel = StatLabel(text='Str.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#                 self.strengthgrade = Image(source=Scale.getScaleAsImagePath(strength, char.ranks[rank - 1].strengthMax),
#                                            pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
#                 self.strengthnumber = StatLabel(text='%d' % strength, font_size=50, color=(0, 0, 0, 1),
#                                                 pos=(x + 180, y))
#                 self.add_widget(self.strengthgrade)
#                 self.add_widget(self.strengthlabel)
#                 self.add_widget(self.strengthnumber)
#                 y -= 70
#                 self.add_widget(
#                     Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                           allow_stretch=True))
#                 self.magiclabel = StatLabel(text='Mag.', font_size=60, color=(0, 0, 0, 1), pos=(x + 20, y))
#                 self.magicgrade = Image(source=Scale.getScaleAsImagePath(magic, char.ranks[rank - 1].magicMax),
#                                         pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
#                 self.magicnumber = StatLabel(text='%d' % magic, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
#                 self.add_widget(self.magicgrade)
#                 self.add_widget(self.magiclabel)
#                 self.add_widget(self.magicnumber)
#             y -= 70
#             self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                                   allow_stretch=True))
#             self.agilitylabel = StatLabel(text='Agi.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#             self.agilitygrade = Image(source=Scale.getScaleAsImagePath(agility, char.ranks[rank - 1].agilityMax),
#                                       pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
#             self.agilitynumber = StatLabel(text='%d' % agility, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
#             self.add_widget(self.agilitygrade)
#             self.add_widget(self.agilitylabel)
#             self.add_widget(self.agilitynumber)
#             y -= 70
#             self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                                   allow_stretch=True))
#             self.dexteritylabel = StatLabel(text='Dex.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#             self.dexteritygrade = Image(source=Scale.getScaleAsImagePath(dexterity, char.ranks[rank - 1].dexterityMax),
#                                         pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
#             self.dexteritynumber = StatLabel(text='%d' % dexterity, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
#             self.add_widget(self.dexteritygrade)
#             self.add_widget(self.dexteritylabel)
#             self.add_widget(self.dexteritynumber)
#             y -= 70
#             self.add_widget(Image(source='../res/screens/stats/StatBar2.png', size=(barwidth, barheight), pos=(x, y), keep_ratio=False,
#                                   allow_stretch=True))
#             self.endurancelabel = StatLabel(text='End.', font_size=50, color=(0, 0, 0, 1), pos=(x + 20, y))
#             self.endurancegrade = Image(source=Scale.getScaleAsImagePath(endurance, char.ranks[rank - 1].enduranceMax),
#                                         pos=(x + 90, y + 10), height=40, keep_ratio=True, allow_stretch=True)
#             self.endurancenumber = StatLabel(text='%d' % endurance, font_size=50, color=(0, 0, 0, 1), pos=(x + 180, y))
#             self.add_widget(self.endurancegrade)
#             self.add_widget(self.endurancelabel)
#             self.add_widget(self.endurancenumber)