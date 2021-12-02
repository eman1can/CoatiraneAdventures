from kivy.properties import StringProperty

from loading.kv_loader import load_kv
from uix.popups.view import View

load_kv(__name__)


class GeneralConfirm(View):
    title_text = StringProperty('Title')
    description_text = StringProperty('Description')
    cancel_text = StringProperty('Cancel')
    confirm_text = StringProperty('Confirm')

    def __init__(self, **kwargs):
        self._override = 0.5, 0.5
        self.register_event_type('on_confirm')
        confirm_callback = None
        if 'on_confirm' in kwargs:
            confirm_callback = kwargs.pop('on_confirm')
        if 'size_override' in kwargs:
            self._override = kwargs.pop('size_override')
        super().__init__(**kwargs)
        if confirm_callback is not None:
            self.bind(on_confirm=confirm_callback)

    def confirm(self):
        self.manager.goto_previous()
        self.dispatch('on_confirm')

    def on_confirm(self):
        pass

    def size_override(self):
        return self._override