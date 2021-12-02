from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv
from refs import Refs
from uix.screens.header_screen import HeaderScreen

load_kv(__name__)


class QuestsMain(HeaderScreen):
    def __init__(self, **kwargs):
        self._display_type = None
        super().__init__(**kwargs)
        self._quest_manager = Refs.gc.get_quest_manager()
        self.display_quests()

    def on_enter(self):
        frame_rate = 30
        Clock.schedule_interval(self.ids.spine_display.update, 1 / frame_rate)

    def on_leave(self):
        Clock.unschedule(self.ids.spine_display.update)

    def display_quests(self, display_type='all'):
        if self._display_type == display_type:
            return
        self.ids.view.clear_widgets()
        if display_type in ('all', 'daily'):
            self.display_quest_stacks(self._quest_manager.get_daily_quest_stacks())
        if display_type in ('all', 'weekly'):
            self.display_quest_stacks(self._quest_manager.get_weekly_quest_stacks())
        if display_type in ('all', 'monthly'):
            self.display_quest_stacks(self._quest_manager.get_monthly_quest_stacks())
        if display_type in ('all', 'campaign'):
            self.display_quest_stacks(self._quest_manager.get_campaign_quest_stacks())

    def display_quest_stacks(self, quest_stacks):
        for quest_stack in quest_stacks:
            for quest in quest_stack.all_completed():
                if quest.claimed():
                    continue
                self.display_quest(quest)
            if len(quest_stack.all_uncompleted()) > 1:
                self.display_quest(quest_stack.first_uncompleted(), True)
            else:
                self.display_quest(quest_stack.first_uncompleted())

    def display_quest(self, quest, stack=False):
        if quest is None:
            return
        quest_display = QuestDisplay()
        quest_display.hash = quest.get_hash()
        quest_display.size_hint = 1, None
        quest_display.stack = stack
        quest_display.height = self.height * 0.104
        if stack:
            quest_display.height *= 1.25
        quest_display.title = quest.get_title()
        quest_display.description = quest.get_description()
        quest_display.progress = quest.get_progress()
        quest_display.goal = quest.get_goal()
        self.ids.view.add_widget(quest_display)

    def on_height(self, *args):
        for child in self.ids.view.children:
            child.height = self.height * 0.104
            if child.stack:
                child.height *= 1.25

    def reload(self, *args):
        self._display_type = None
        self.display_quests()


class QuestDisplay(RelativeLayout):
    title = StringProperty('')
    description = StringProperty('')
    image_source = StringProperty('')
    progress = NumericProperty(0)
    goal = NumericProperty(1)
    finished = BooleanProperty(False)
    stack = BooleanProperty(False)

    def on_size(self, *args):
        print(self.size)