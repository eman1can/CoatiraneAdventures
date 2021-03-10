# Project Imports
from refs import Refs
from lists import POPUP_LIST, POPUP_WHITELIST

# UIX Imports
from uix.popups.managed_popup import ManagedPopup


class PopupManager:
    def __init__(self):
        self.list = []

    def display_popup(self, previous, popup_name, *args, **kwargs):
        Refs.log(f'Display popup {popup_name}')
        popup = None
        for saved_popup in self.list:
            if saved_popup.name.startswith(popup_name):
                if popup_name + str(args[0]) == saved_popup.name:
                    Refs.log(popup_name + str(args[0]), saved_popup.name)
                    popup = saved_popup
                    popup.previous = previous
                    popup.refresh(*args)
                    Refs.log('Found saved popup')
        if popup is None:
            Refs.log('Create popup')
            popup = self._create_popup(previous, popup_name, *args, **kwargs)
        popup.open()
        Refs.log('Open popup')

    def _create_popup(self, previous, popup_name, *args, **kwargs):
        popup = ManagedPopup(manager=self)
        try:
            view = POPUP_LIST[popup_name](manager=popup, *args, **kwargs)
        except ValueError:
            raise Exception('Unsupported View!')
        popup.previous = previous
        popup.size_hint = view.size_override()
        popup.next = view.get_next()
        popup.content = view
        popup.name = popup_name + view.get_name()
        if popup_name in POPUP_WHITELIST:
            self.list.append(popup)
        return popup

    def clear_memory(self):
        self.list.clear()
