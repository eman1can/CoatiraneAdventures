# UIX Imports
from uix.popups.view import View
from uix.screens.character_display.attributes.abilities import AbilityChoice

# Kivy Imports
from kivy.properties import StringProperty, ListProperty, ObjectProperty

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class SBSkillUnlock(View):
    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        confirm_callback = None
        if 'on_confirm' in kwargs:
            confirm_callback = kwargs.pop('on_confirm')
        super().__init__(**kwargs)
        if confirm_callback is not None:
            self.bind(on_confirm=confirm_callback)

    def confirm(self):
        self.manager.goto_previous()
        self.dispatch('on_confirm')

    def on_confirm(self):
        pass


class SBAbilityUnlock(View):
    choices = ListProperty([])

    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        confirm_callback = None
        if 'on_confirm' in kwargs:
            confirm_callback = kwargs.pop('on_confirm')
        super().__init__(**kwargs)
        if confirm_callback is not None:
            self.bind(on_confirm=confirm_callback)

    def on_choices(self, *args):
        self.ids.content.clear_widgets()
        for x, choice in enumerate(self.choices):
            ab_c = AbilityChoice(choice, choice_id=x)
            ab_c.bind(on_choice=self.confirm)
            self.ids.content.add_widget(ab_c)

    def confirm(self, instance, choice):
        self.manager.goto_previous()
        self.dispatch('on_confirm', choice)

    def on_confirm(self, choice):
        pass


class SBUnlockAll(View):
    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        confirm_callback = None
        if 'on_confirm' in kwargs:
            confirm_callback = kwargs.pop('on_confirm')
        super().__init__(**kwargs)
        if confirm_callback is not None:
            self.bind(on_confirm=confirm_callback)

    def confirm(self):
        self.manager.goto_previous()
        self.dispatch('on_confirm')

    def on_confirm(self):
        pass


class SlotConfirm(View):
    text_main = StringProperty('')
    text_update = StringProperty('')
    callback = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        confirm_callback = None
        if 'on_confirm' in kwargs:
            confirm_callback = kwargs.pop('on_confirm')
        super().__init__(**kwargs)
        if confirm_callback is not None:
            self.bind(on_confirm=confirm_callback)

    def on_confirm(self):
        if self.callback is not None:
            self.manager.goto_previous()
            self.callback()
