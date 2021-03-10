# UIX Imports
from uix.popups.view import View

# Kivy Imports
from kivy.properties import BooleanProperty

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class Confirm(View):

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


class Cancel(View):

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


class Roll(View):
    show_warning = BooleanProperty(True)

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


class NoRecruit(View):
    pass
