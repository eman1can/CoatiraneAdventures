__all__ = ('ManagedPopup',)

# Kivy Imports
from kivy.properties import ObjectProperty, StringProperty

from kivy.uix.modalview import ModalView
# KV Import
from loading.kv_loader import load_kv
# UIX Imports
from uix.modules.screen import Screen

load_kv(__name__)


class ManagedPopup(ModalView):
    name = StringProperty('None')
    manager = ObjectProperty(None)
    next = ObjectProperty(None, allownone=True)
    previous = ObjectProperty(None, allownone=True)
    content = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self._content = None
        super().__init__(background='background/background.jpg', **kwargs)

    def refresh(self, *args):
        self.content.refresh(*args)

    def on_content(self, instance, new_content):
        if self._content is not None:
            self.remove_widget(self._content)
        if self.content is not None:
            self.add_widget(self.content)
        self._content = new_content

    def on_pre_open(self, *args):
        self.content.dispatch('on_pre_open')

    def on_pre_dismiss(self):
        self.content.dispatch('on_pre_dismiss')

    def get_root(self):
        previous = self.previous
        while previous.get_previous() is not None:
            previous = previous.get_previous()
        return previous

    def get_previous(self):
        return self.previous

    def get_next(self):
        if self.next is None:
            return self.previous
        return self.next

    def goto_next(self, *args):
        next_popup = self.get_next()
        if isinstance(next_popup, str):
            # Popups can have their next be a string
            # Resolve the string to a popup
            try:
                next_popup = self.manager.display_popup(self, next_popup, *args)
            except Exception as e:
                next_popup = self.get_root().manager.get_screen(next_popup)

        if isinstance(next_popup, ManagedPopup):
            # Go to next popup in chain
            pass
        elif isinstance(next_popup, Screen):
            # Go back to start
            next_popup.next_callback(*args)
            next_popup = None

        self.dismiss()
        if next_popup is not None:
            next_popup.open()

    def goto_previous(self):
        self.dismiss()
        if isinstance(self.previous, ManagedPopup):
            self.previous.open()

    def __str__(self):
        return f'<Popup: {self.name}>'
