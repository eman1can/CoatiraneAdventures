# UIX Imports
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty, StringProperty

# Kivy Imports
from kivy.uix.widget import Widget
# KV Import
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.screen import Screen
from uix.popups.status_board import SBUnlockAll, SlotConfirm
from uix.screens.character_display.attributes.status_board.page import GridWidget

load_kv(__name__)


class StatusBoardManager(Screen):
    char = ObjectProperty(None)

    overlay_background_source = StringProperty('screens/attributes/stat_background.png')
    overlay_source = StringProperty('screens/attributes/stat_background_overlay.png')

    skills_switch_text = StringProperty('Skills')
    current_board_name = StringProperty('Rank 1\nStatus Board')

    modal_open = BooleanProperty(False)

    slot_nums = ListProperty([])

    def __init__(self, **kwargs):
        self.rank_loaded_max = 0
        self.rank_loaded_min = 0
        self.finished_loading = False
        self.rank_current = -1
        self.slot_confirm = SlotConfirm()
        self.unlock_all = SBUnlockAll()
        super().__init__(**kwargs)
        self.unlock_all.bind(on_dismiss=self.modal_dismiss)
        self.slot_confirm.bind(on_dismiss=self.modal_dismiss)
        self.unlock_all.bind(on_confirm=self.unlock_all_slots)

        sb = self.ids.status_board_screen
        ranks = self.char.get_grids()
        self.rank_loaded_min = self.rank_current = self.rank_loaded_max = self.char.get_current_rank() - 1

        if self.rank_current != 0:
            for index in range(0, self.rank_current - 1):
                sb.add_widget(Widget())
            self.rank_loaded_min = self.rank_current - 1
            sb.add_widget(GridWidget(self.char.get_current_rank(), self.rank_current - 1, ranks[self.rank_current - 1].grid, manager=self))
        sb.add_widget(GridWidget(self.char.get_current_rank(), self.rank_current, ranks[self.rank_current].grid, manager=self))
        if self.rank_current != 9:
            self.rank_loaded_max = self.rank_current + 1
            sb.add_widget(GridWidget(self.char.get_current_rank(), self.rank_current + 1, ranks[self.rank_current + 1].grid, manager=self))
            for index in range(self.rank_current + 2, 10):
                sb.add_widget(Widget())
        self.current_board_name = f'Rank {self.rank_current + 1}\nStatus Board'
        sb.bind(on_load_next=self.goto_next_board)
        sb.bind(on_load_previous=self.goto_previous_board)
        sb.anim_move_duration = 0.0
        sb.load_slide(sb.slides[self.rank_current])
        sb.anim_move_duration = 0.5
        self.finished_loading = True

    # def on_touch_hover(self, touch):
    #     if self.modal_open:
    #         return False
    #     return self.dispatch_to_relative_children(touch)

    def goto_next_board(self, *args):
        self.rank_current += 1
        if self.rank_loaded_max == 9:
            return
        if self.rank_loaded_max > self.rank_current:
            return
        ranks = self.char.get_grids()
        self.rank_loaded_max += 1
        self.ids.status_board_screen.replace_widget(self.rank_loaded_max, GridWidget(self.char.get_current_rank(), self.rank_loaded_max, ranks[self.rank_loaded_max].grid, manager=self))

    def goto_previous_board(self, *args):
        self.rank_current -= 1
        if self.rank_loaded_min == 0:
            return
        if self.rank_loaded_min < self.rank_current:
            return
        ranks = self.char.get_grids()
        self.rank_loaded_min -= 1
        self.ids.status_board_screen.replace_widget(self.rank_loaded_min, GridWidget(self.char.get_current_rank(), self.rank_loaded_min, ranks[self.rank_loaded_min].grid, manager=self))

    def on_board_move(self, index):
        if self.finished_loading:
            print("in ", index, self.rank_current)
            if index < self.rank_current:
                self.goto_previous_board()
            elif index > self.rank_current:
                self.goto_next_board()

        self.current_board_name = f'Rank {self.rank_current + 1}\nStatus Board'

        self.ids.arrows.unanimate_arrows()
        self.ids.arrows.animate_arrows(index)

    def on_skills_switch(self):
        if self.skills_switch_text == 'Skills':
            self.skills_switch_text = 'Status'
        else:
            self.skills_switch_text = 'Skills'
        self.ids.normal_layout.opacity = int(not bool(int(self.ids.normal_layout.opacity)))
        self.ids.skill_layout.opacity = int(not bool(int(self.ids.skill_layout.opacity)))
        self.ids.skillslist.scroll_y = 1
        self.ids.skillslist.update_from_scroll()

    def on_enter(self, *args):
        self.ids.arrows.animate_arrows(self.ids.status_board_screen.index)

    def on_leave(self, *args):
        self.ids.arrows.unanimate_arrows()
        if self.modal_open:
            self.slot_confirm.dismiss()
            self.unlock_all.dismiss()

    def modal_dismiss(self, instance):
        self.modal_open = False

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
        self.modal_open = False
        if type == 'strength':
            rank.update_strength(slot_obj.value, True)
        elif type == 'magic':
            rank.update_magic(slot_obj.value, True)
        elif type == 'endurance':
            rank.update_endurance(slot_obj.value, True)
        elif type == 'dexterity':
            rank.update_dexterity(slot_obj.value, True)
        elif type == 'agility':
            rank.update_agility(slot_obj.value, True)
        slot_obj.unlock_slot()
        self.ids.total_stats_box.reload()
        self.ids.total_abilities_box.reload()

    def on_unlock_all_touch(self):
        rank = self.ids.status_board_screen.current_slide.rank
        str = 0
        str_gain = 0
        mag = 0
        mag_gain = 0
        end = 0
        end_gain = 0
        dex = 0
        dex_gain = 0
        agi = 0
        agi_gain = 0
        for list in self.ids.status_board_screen.current_slide.slots:
            for slot in list:
                if slot.type == 'strength':
                    str += 1
                    str_gain += slot.value
                elif slot.type == 'magic':
                    mag += 1
                    mag_gain += slot.value
                elif slot.type == 'endurance':
                    end += 1
                    end_gain += slot.value
                elif slot.type == 'dexterity':
                    dex += 1
                    dex_gain += slot.value
                elif slot.type == 'agility':
                    agi += 1
                    agi_gain += slot.value
        str_cost = str * rank
        mag_cost = mag * rank
        end_cost = end * rank
        dex_cost = dex * rank
        agi_cost = agi * rank
        str_current = self.char.get_strength()
        mag_current = self.char.get_magic()
        end_current = self.char.get_endurance()
        dex_current = self.char.get_dexterity()
        agi_current = self.char.get_agility()
        str_falna = 200
        mag_falna = 180
        end_falna = 120
        dex_falna = 140
        agi_falna = 150

        self.slot_nums = [0, 0, 0, 0, 0]
        # Need to add image overlays to dim - do once items are added
        # str
        self.unlock_all.ids.str_change.text = f"Str. +{str_gain}"
        if str_falna > str_cost:
            self.unlock_all.ids.str_falna_change.text = f"{str_falna} -> {str_falna - str_cost}"
            self.slot_nums[0] = str_cost
            self.unlock_all.ids.str_falna_change.color = 0, 0, 0, 1
            self.unlock_all.ids.str_missing.text = f"{0}"
            self.unlock_all.ids.str_missing.color = 1, 0, 0, 1
        else:
            self.slot_nums[0] = str_falna
            self.unlock_all.ids.str_falna_change.text = f"{str_falna} -> 0"
            self.unlock_all.ids.str_missing.text = f"{str_cost - str_falna}"
            self.unlock_all.ids.str_missing.color = 0, 0, 0, 1
        self.unlock_all.ids.str_increase.text = f"{str_current} -> {str_current + str_gain}"
        if str == 0 or str_falna == 0:
            self.unlock_all.ids.str_change.color = 1, 0, 0, 1
            self.unlock_all.ids.str_increase.color = 1, 0, 0, 1
            self.unlock_all.ids.str_falna_change.color = 1, 0, 0, 1
        else:
            self.unlock_all.ids.str_change.color = 0, 0, 0, 1
            self.unlock_all.ids.str_increase.color = 0, 0, 0, 1
            self.unlock_all.ids.str_falna_change.color = 0, 0, 0, 1

        # mag
        self.unlock_all.ids.mag_change.text = f"Mag. +{mag_gain}"
        if mag_falna > mag_cost:
            self.unlock_all.ids.mag_falna_change.text = f"{mag_falna} -> {mag_falna - mag_cost}"
            self.slot_nums[1] = mag_cost
            self.unlock_all.ids.mag_falna_change.color = 0, 0, 0, 1
            self.unlock_all.ids.mag_missing.text = f"{0}"
            self.unlock_all.ids.mag_missing.color = 1, 0, 0, 1
        else:
            self.slot_nums[1] = mag_falna
            self.unlock_all.ids.mag_falna_change.text = f"{mag_falna} -> 0"
            self.unlock_all.ids.mag_missing.text = f"{mag_cost - mag_falna}"
            self.unlock_all.ids.mag_missing.color = 0, 0, 0, 1
        self.unlock_all.ids.mag_increase.text = f"{mag_current} -> {mag_current + mag_gain}"
        if mag == 0 or mag_falna == 0:
            self.unlock_all.ids.mag_change.color = 1, 0, 0, 1
            self.unlock_all.ids.mag_increase.color = 1, 0, 0, 1
            self.unlock_all.ids.mag_falna_change.color = 1, 0, 0, 1
        else:
            self.unlock_all.ids.mag_change.color = 0, 0, 0, 1
            self.unlock_all.ids.mag_increase.color = 0, 0, 0, 1
            self.unlock_all.ids.mag_falna_change.color = 0, 0, 0, 1

        # end
        self.unlock_all.ids.end_change.text = f"End. +{end_gain}"
        if end_falna > end_cost:
            self.unlock_all.ids.end_falna_change.text = f"{end_falna} -> {end_falna - end_cost}"
            self.slot_nums[2] = end_cost
            self.unlock_all.ids.end_falna_change.color = 0, 0, 0, 1
            self.unlock_all.ids.end_missing.text = f"{0}"
            self.unlock_all.ids.end_missing.color = 1, 0, 0, 1
        else:
            self.slot_nums[2] = end_falna
            self.unlock_all.ids.end_falna_change.text = f"{end_falna} -> 0"
            self.unlock_all.ids.end_missing.text = f"{end_cost - end_falna}"
            self.unlock_all.ids.end_missing.color = 0, 0, 0, 1
        self.unlock_all.ids.end_increase.text = f"{end_current} -> {end_current + end_gain}"
        if end == 0 or end_falna == 0:
            self.unlock_all.ids.end_change.color = 1, 0, 0, 1
            self.unlock_all.ids.end_increase.color = 1, 0, 0, 1
            self.unlock_all.ids.end_falna_change.color = 1, 0, 0, 1
        else:
            self.unlock_all.ids.end_change.color = 0, 0, 0, 1
            self.unlock_all.ids.end_increase.color = 0, 0, 0, 1
            self.unlock_all.ids.end_falna_change.color = 0, 0, 0, 1

        # dex
        self.unlock_all.ids.dex_change.text = f"Dex. +{dex_gain}"
        if dex_falna > dex_cost:
            self.unlock_all.ids.dex_falna_change.text = f"{dex_falna} -> {dex_falna - dex_cost}"
            self.slot_nums[3] = dex_cost
            self.unlock_all.ids.dex_falna_change.color = 0, 0, 0, 1
            self.unlock_all.ids.dex_missing.text = f"{0}"
            self.unlock_all.ids.dex_missing.color = 1, 0, 0, 1
        else:
            self.slot_nums[2] = dex_falna
            self.unlock_all.ids.dex_falna_change.text = f"{dex_falna} -> 0"
            self.unlock_all.ids.dex_missing.text = f"{dex_cost - dex_falna}"
            self.unlock_all.ids.dex_missing.color = 0, 0, 0, 1
        self.unlock_all.ids.dex_increase.text = f"{dex_current} -> {dex_current + dex_gain}"
        if dex == 0 or dex_falna == 0:
            self.unlock_all.ids.dex_change.color = 1, 0, 0, 1
            self.unlock_all.ids.dex_increase.color = 1, 0, 0, 1
            self.unlock_all.ids.dex_falna_change.color = 1, 0, 0, 1
        else:
            self.unlock_all.ids.dex_change.color = 0, 0, 0, 1
            self.unlock_all.ids.dex_increase.color = 0, 0, 0, 1
            self.unlock_all.ids.dex_falna_change.color = 0, 0, 0, 1

        # agi
        self.unlock_all.ids.agi_change.text = f"Agi. +{agi_gain}"
        if agi_falna > agi_cost:
            self.unlock_all.ids.agi_falna_change.text = f"{agi_falna} -> {agi_falna - agi_cost}"
            self.slot_nums[4] = agi_cost
            self.unlock_all.ids.agi_falna_change.color = 0, 0, 0, 1
            self.unlock_all.ids.agi_missing.text = f"{0}"
            self.unlock_all.ids.agi_missing.color = 1, 0, 0, 1
        else:
            self.slot_nums[4] = agi_falna
            self.unlock_all.ids.agi_falna_change.text = f"{agi_falna} -> 0"
            self.unlock_all.ids.agi_missing.text = f"{agi_cost - agi_falna}"
            self.unlock_all.ids.agi_missing.color = 0, 0, 0, 1
        self.unlock_all.ids.agi_increase.text = f"{agi_current} -> {agi_current + agi_gain}"
        if agi == 0 or agi_falna == 0:
            self.unlock_all.ids.agi_change.color = 1, 0, 0, 1
            self.unlock_all.ids.agi_increase.color = 1, 0, 0, 1
            self.unlock_all.ids.agi_falna_change.color = 1, 0, 0, 1
        else:
            self.unlock_all.ids.agi_change.color = 0, 0, 0, 1
            self.unlock_all.ids.agi_increase.color = 0, 0, 0, 1
            self.unlock_all.ids.agi_falna_change.color = 0, 0, 0, 1
        self.unlock_all.open()

    def unlock_all_slots(self, instance):
        self.modal_open = False
        rank_num = self.ids.status_board_screen.current_slide.rank
        rank = self.char.get_rank(rank_num)
        for list in self.ids.status_board_screen.current_slide.slots:
            for slot in list:
                if slot.type == 'strength':
                    if self.slot_nums[0] > 0:
                        self.slot_nums[0] -= 1
                        rank.update_strength(slot.value, True)
                        slot.unlock_slot()
                elif slot.type == 'magic':
                    if self.slot_nums[1] > 0:
                        self.slot_nums[1] -= 1
                        rank.update_magic(slot.value, True)
                        slot.unlock_slot()
                elif slot.type == 'endurance':
                    if self.slot_nums[2] > 0:
                        self.slot_nums[2] -= 1
                        rank.update_endurance(slot.value, True)
                        slot.unlock_slot()
                elif slot.type == 'dexterity':
                    if self.slot_nums[3] > 0:
                        self.slot_nums[3] -= 1
                        rank.update_dexterity(slot.value, True)
                        slot.unlock_slot()
                else:
                    if self.slot_nums[4] > 0:
                        self.slot_nums[4] -= 1
                        rank.update_agility(slot.value, True)
                        slot.unlock_slot()
        self.ids.total_stats_box.reload()
        self.ids.total_abilities_box.reload()

    def goto_status_board(self, direction):
        next_char = Refs.gc.get_next_char(self.char, direction)
        Refs.gs.display_screen('status_board_' + next_char.get_id(), True, False, next_char)
