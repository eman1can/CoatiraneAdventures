# Project Imports
from lists import POPUP_LIST, POPUP_WHITELIST
from refs import Refs
# UIX Imports
from uix.popups.managed_popup import ManagedPopup


class PopupManager:
    def __init__(self):
        self.list = []
        self.open_popups = []

    def is_popup_open(self, popup_name):
        for saved_popup in self.open_popups:
            print(saved_popup.name)
            if saved_popup.name.startswith(popup_name):
                print('Found popup', popup_name)
                print('Open', saved_popup.is_open())
                return saved_popup.is_open()
        return False

    def display_popup(self, previous, popup_name, *args, **kwargs):
        Refs.log(f'Display popup {popup_name}')
        popup = None
        for saved_popup in self.list:
            if saved_popup.name.startswith(popup_name):
                # if popup_name + str(args[0]) == saved_popup.name:
                #     Refs.log(popup_name + str(args[0]), saved_popup.name)
                popup = saved_popup
                popup.previous = previous
                popup.refresh(*args)
                Refs.log('Found saved popup')
        if popup is None:
            Refs.log('Create popup')
            popup = self._create_popup(previous, popup_name, *args, **kwargs)
        popup.open()
        self.open_popups.append(popup)
        Refs.log('Open popup')
        return popup

    def close_popup(self, popup_name):
        for saved_popup in self.open_popups:
            if saved_popup.name.startswith(popup_name):
                saved_popup.dismiss()
                return True
        return False

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
        popup.bind(on_dismiss=self._on_popup_closed)
        return popup

    def _on_popup_closed(self, popup):
        if popup in self.open_popups:
            self.open_popups.remove(popup)

    def clear_memory(self):
        self.list.clear()
