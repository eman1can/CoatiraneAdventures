from kivy.animation import Animation
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty, BooleanProperty, OptionProperty
from kivy.app import App

from src.modules.KivyBase.Hoverable import ScreenBase as Screen, RelativeLayoutBase as RelativeLayout, ModalViewBase as ModalView, WidgetBase as Widget

from kivy.graphics import Line
from kivy.gesture import Gesture, GestureDatabase
from src.modules.ca_gestures import left, right
import math


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

    minimum_x_distance = NumericProperty(0.0)
    minimum_y_distance = NumericProperty(0.0)

    def __init__(self, **kwargs):
        self.gdb = GestureDatabase()
        self.gdb.add_gesture(left)
        self.gdb.add_gesture(right)
        self.rank_loaded_max = 0
        self.rank_loaded_min = 0
        self.finished_loading = False
        self.rank_current = -1
        self.slot_confirm = SlotConfirm()
        super().__init__(**kwargs)

        sb = self.ids.status_board_screen
        ranks = self.char.get_grids()
        self.rank_loaded_min = self.rank_current = self.rank_loaded_max = self.char.get_current_rank() - 1

        if self.rank_current != 0:
            for index in range(0, self.rank_current - 1):
                sb.add_widget(Widget())
            self.rank_loaded_min = self.rank_current - 1
            sb.add_widget(GridWidget(self.char.get_current_rank(), ranks[self.rank_current - 1].grid, manager=self))
        sb.add_widget(GridWidget(self.char.get_current_rank(), ranks[self.rank_current].grid, manager=self))
        if self.rank_current != 9:
            self.rank_loaded_max = self.rank_current + 1
            sb.add_widget(GridWidget(self.char.get_current_rank(), ranks[self.rank_current + 1].grid, manager=self))
            for index in range(self.rank_current + 2, 10):
                sb.add_widget(Widget())
        self.current_board_name = f'Rank {self.rank_current + 1}\nStatus Board'
        sb.bind(on_load_next=self.goto_next_board)
        sb.bind(on_load_previous=self.goto_previous_board)
        sb.anim_move_duration = 0.0
        sb.load_slide(sb.slides[self.rank_current])
        sb.anim_move_duration = 0.5
        self.finished_loading = True

    def goto_next_board(self, *args):
        self.rank_current += 1
        if self.rank_loaded_max == 9:
            return
        if self.rank_loaded_max > self.rank_current:
            return
        ranks = self.char.get_grids()
        self.ids.status_board_screen.replace_widget(self.rank_loaded_max + 1, GridWidget(self.char.get_current_rank(), ranks[self.rank_loaded_max + 1].grid, manager=self))
        self.rank_loaded_max += 1

    def goto_previous_board(self, *args):
        self.rank_current -= 1
        if self.rank_loaded_min == 0:
            return
        if self.rank_loaded_min < self.rank_current:
            return
        ranks = self.char.get_grids()
        self.ids.status_board_screen.replace_widget(self.rank_loaded_min - 1, GridWidget(self.char.get_current_rank(), ranks[self.rank_loaded_min - 1].grid, manager=self))
        self.rank_loaded_min -= 1

    def on_board_move(self, index):
        if self.finished_loading:
            print("in ", index, self.rank_current)
            if index < self.rank_current:
                self.goto_previous_board()
            elif index > self.rank_current:
                self.goto_next_board()

        self.current_board_name = f'Rank {self.rank_current + 1}\nStatus Board'
        if index != 0 and index != 9:

            if self.animation_left is not None and not self.animation_left.repeat or self.animation_right is not None and not self.animation_right.repeat:
                self.animation_left.cancel(self.ids.left_arrow)
                self.animation_right.cancel(self.ids.right_arrow)
                self.animate_left_arrow()
                self.animate_right_arrow()
        elif index == 0:
            self.unanimate_left_arrow()
        else:
            self.unanimate_right_arrow()

    def on_skills_switch(self):
        if self.skills_switch_text == 'Skills':
            self.skills_switch_text = 'Status'
        else:
            self.skills_switch_text = 'Skills'
        self.ids.normal_layout.opacity = int(not bool(int(self.ids.normal_layout.opacity)))
        self.ids.skill_layout.opacity = int(not bool(int(self.ids.skill_layout.opacity)))
        self.ids.skillslist.scroll_y = 1
        self.ids.skillslist.update_from_scroll()

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
            self.ids.left_arrow.disabled = True
            self.ids.right_arrow.disabled = True
            self.animation_left = Animation(x=self.animate_start_left - self.animate_distance, duration=1) + Animation(x=self.animate_start_left, duration=0.25)
            self.animation_right = Animation(x=self.animate_start_right + self.animate_distance, duration=1) + Animation(x=self.animate_start_right, duration=0.25)

    def unanimate_arrows(self):
        self.unanimate_left_arrow()
        self.unanimate_right_arrow()

    def unanimate_left_arrow(self):
        if self.animation_left is None:
            return
        self.animation_left.cancel(self.ids.left_arrow)
        self.ids.left_arrow.disabled = True
        self.animation_left.repeat = False

    def animate_left_arrow(self):
        if self.animation_left is None:
            return
        self.animation_left.repeat = True
        self.ids.left_arrow.disabled = False
        self.animation_left.start(self.ids.left_arrow)

    def unanimate_right_arrow(self):
        if self.animation_right is None:
            return
        self.animation_right.cancel(self.ids.right_arrow)
        self.ids.right_arrow.disabled = True
        self.animation_right.repeat = False

    def animate_right_arrow(self):
        if self.animation_right is None:
            return
        self.animation_right.repeat = True
        self.ids.right_arrow.disabled = False
        self.animation_right.start(self.ids.right_arrow)

    def on_enter(self, *args):
        self.animate_arrows(self.ids.status_board_screen.index)

    def on_leave(self, *args):
        self.unanimate_arrows()

    def on_release(self, slot_obj, type, slot_num):
        rank = self.char.get_rank(slot_num)
        self.slot_confirm.text_main = type[:3].capitalize() + '. +' + str(slot_obj.value)
        stat = 0
        if type == 'strength':
            stat = self.char.get_strength(slot_num)
        elif type == 'magic':
            stat = self.char.get_magic(slot_num)
        elif type == 'endurance':
            stat = self.char.get_endurance(slot_num)
        elif type == 'dexterity':
            stat = self.char.get_dexterity(slot_num)
        elif type == 'agility':
            stat = self.char.get_agility(slot_num)
        self.slot_confirm.text_update = str(stat) + ' -> ' + str(stat + slot_obj.value)
        self.slot_confirm.callback = lambda: self.unlock_slot(slot_obj, type, rank)
        self.slot_confirm.open()

    def unlock_slot(self, slot_obj, type, rank):
        print("unlock slot!!")
        if type == 'strength':
            rank.update_strength(rank.grid.amounts[0], True)
        elif type == 'magic':
            rank.update_magic(rank.grid.amounts[1], True)
        elif type == 'endurance':
            rank.update_endurance(rank.grid.amounts[2], True)
        elif type == 'dexterity':
            rank.update_dexterity(rank.grid.amounts[3], True)
        elif type == 'agility':
            rank.update_agility(rank.grid.amounts[4], True)
        slot_obj.unlock_slot()
        self.ids.total_stats_box.reload()
        self.ids.total_abilities_box.reload()

    def simplegesture(self, name, point_list):
        g = Gesture()
        g.add_stroke(point_list)
        g.normalize()
        g.name = name
        return g

    def on_touch_down(self, touch):
        touch.ud['start'] = (touch.x, touch.y)
        touch.ud['line'] = Line(points=(touch.x, touch.y))
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        try:
            touch.ud['line'].points += [touch.x, touch.y]
        except (KeyError) as e:
            pass
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if 'start' in touch.ud:
            if math.fabs(touch.x - touch.ud['start'][0]) <= self.minimum_x_distance:
                return super().on_touch_up(touch)
            if math.fabs(touch.y - touch.ud['start'][1]) <= self.minimum_y_distance:
                return super().on_touch_up(touch)
        else:
            return super().on_touch_up(touch)

        g = self.simplegesture('', list(zip(touch.ud['line'].points[::2],
                                            touch.ud['line'].points[1::2])))
        # print("gesture representation:", self.gdb.gesture_to_str(g))
        # print("left:", g.get_score(left))
        # print("right:", g.get_score(right))
        g2 = self.gdb.find(g, minscore=0.70)
        if g2:
            if g2[1] == left:
                self.goto_left()
            if g2[1] == right:
                self.goto_right()
        return super().on_touch_up(touch)

    def goto_left(self):
        root = App.get_running_app().main
        party = root.parties[root.parties[0] + 1]
        if self.char in party:
            index = party.index(self.char)
            next = None
            for x in range(index - 1, -1, -1):
                if party[x] is not None:
                    next = party[x]
                    break
            if next is None:
                for x in range(len(party) - 1, index, -1):
                    if party[x] is not None:
                        next = party[x]
                        break
            if next is not None:
                screen, made = root.create_screen('status_board_' + next.get_id(), next)
                root.display_screen(screen, True, False)
        else:
            for screen in root.screens:
                if screen.name == 'select_char':
                    index = 0
                    for char in screen.multi.data:
                        if char['id'] == self.char.get_id():
                            if index == 0:
                                next = screen.multi.data[len(screen.multi.data) - 1]
                            else:
                                next = screen.multi.data[index - 1]
                            screen, made = root.create_screen('status_board_' + next['id'], next['character'])
                            root.display_screen(screen, True, False)
                            break
                        index += 1
                    break

    def goto_right(self):
        root = App.get_running_app().main
        party = root.parties[root.parties[0] + 1]
        if self.char in party:
            index = party.index(self.char)
            next = None
            for x in range(index + 1, len(party)):
                if party[x] is not None:
                    next = party[x]
                    break
            if next is None:
                for x in range(0, index):
                    if party[x] is not None:
                        next = party[x]
                        break
            if next is not None:
                screen, made = root.create_screen('status_board_' + next.get_id(), next)
                root.display_screen(screen, True, False)
        else:
            for screen in root.screens:
                if screen.name == 'select_char':
                    index = 0
                    for char in screen.multi.data:
                        if char['id'] == self.char.get_id():
                            if index == len(screen.multi.data) - 1:
                                next = screen.multi.data[0]
                            else:
                                next = screen.multi.data[index + 1]
                            screen, made = root.create_screen('status_board_' + next['id'], next['character'])
                            root.display_screen(screen, True, False)
                            break
                        index += 1
                    break


class SlotConfirm(ModalView):
    text_main = StringProperty('')
    text_update = StringProperty('')
    callback = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        super().__init__(**kwargs)

    def on_confirm(self):
        if self.callback is not None:
            self.dismiss()
            self.callback()


class GridWidget(RelativeLayout):
    grid = ObjectProperty(None)
    manager = ObjectProperty(None)

    slots = ListProperty([])
    titles = ListProperty([])
    offsets = ListProperty([])
    toffsets = ListProperty([])

    overlay_background_source = StringProperty("../res/screens/attribute/stat_background.png")
    overlay_source = StringProperty("../res/screens/attribute/stat_background_overlay.png")

    def __init__(self, rank, grid, **kwargs):
        self.grid = grid
        super().__init__(**kwargs)

        index = 0
        y_i = len(self.grid.grid) - 1
        pos_hint_x, pos_hint_y = 0.5, 0.5 + y_i * 0.03125 + y_i * 0.00625
        for r, row in enumerate(self.grid.grid):
            list = []
            # offsets = []
            for c, column in enumerate(row):
                slot_unlocked = self.grid.unlocked[r][c]
                # print(self.grid.amounts)
                # print("gi-r ", self.grid.index, rank)
                disabled = self.grid.index > rank
                if column == 'S':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.07076, 0.0625), type='strength', locked=(not slot_unlocked), disabled=disabled, value=self.grid.amounts[0])
                    slot.bind(on_unlock=lambda instance: self.manager.on_release(instance, 'strength', self.grid.index))
                elif column == 'M':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.07076, 0.0625),type='magic', locked=(not slot_unlocked), disabled=disabled, value=self.grid.amounts[1])
                    slot.bind(on_unlock=lambda instance: self.manager.on_release(instance, 'magic', self.grid.index))
                elif column == 'E':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.07076, 0.0625), type='endurance', locked=(not slot_unlocked), disabled=disabled, value=self.grid.amounts[2])
                    slot.bind(on_unlock=lambda instance: self.manager.on_release(instance, 'endurance', self.grid.index))
                elif column == 'D':
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.07076, 0.0625),  type='dexterity', locked=(not slot_unlocked), disabled=disabled, value=self.grid.amounts[3])
                    slot.bind(on_unlock=lambda instance: self.manager.on_release(instance, 'dexterity', self.grid.index))
                else:
                    slot = CustomSlot(pos_hint={'center_x': pos_hint_x, 'center_y': pos_hint_y}, size_hint=(0.07076, 0.0625),  type='agility', locked=(not slot_unlocked), disabled=disabled, value=self.grid.amounts[4])
                    slot.bind(on_unlock=lambda instance: self.manager.on_release(instance, 'agility', self.grid.index))
                pos_hint_x += 0.007076 + 0.03538
                pos_hint_y -= 0.00625 + 0.03125
                list.append(slot)
                index += 1
                # offsets.append((0, 0))
                # self.toffsets.append((0, 0))
                self.add_widget(slot)
            pos_hint_x -= (0.007076 + 0.03538) * (len(row) + 1)
            pos_hint_y += (0.00625 + 0.03125) * (len(row) - 1)
            self.slots.append(list)
            # self.offsets.append(offsets)

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


class CustomSlot(RelativeLayout):

    type = OptionProperty('strength', options=['strength', 'magic', 'endurance', 'dexterity', 'agility'])
    locked = BooleanProperty(False)
    value = NumericProperty(0.0)

    def __init__(self, **kwargs):
        self.register_event_type('on_unlock')
        super().__init__(**kwargs)

    def _do_press(self):
        if not self.toggle_enabled:
            self.state = 'down'
        else:
            if self.locked:
                self.dispatch('on_unlock')

    def on_unlock(self, *args):
        pass

    def unlock_slot(self):
        if not self.locked:
            return
        self.locked = False