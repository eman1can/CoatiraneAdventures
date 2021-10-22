# UIX Imports
# Kivy Imports
from kivy.properties import BooleanProperty, StringProperty

# KV Import
from loading.kv_loader import load_kv
from uix.popups.view import View

load_kv(__name__)


class Confirm(View):
    title_text = StringProperty('')
    description_text = StringProperty('')
    cancel_text = StringProperty('')
    confirm_text = StringProperty('')

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
