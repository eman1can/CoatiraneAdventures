from src.modules.KivyBase.Hoverable import ModalViewBase as ModalView
from kivy.properties import BooleanProperty, NumericProperty, StringProperty


class TMConfirmWidget(ModalView):

    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        super().__init__(**kwargs)

    def confirm(self):
        self.dismiss()
        self.dispatch('on_confirm')

    def on_confirm(self):
        pass


class TMCancelWidget(ModalView):

    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        super().__init__(**kwargs)

    def confirm(self):
        self.dismiss()
        self.dispatch('on_confirm')

    def on_confirm(self):
        pass


class TMRollWidget(ModalView):
    show_warning = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        super().__init__(**kwargs)

    def confirm(self):
        self.dismiss()
        self.dispatch('on_confirm')

    def on_confirm(self):
        pass
