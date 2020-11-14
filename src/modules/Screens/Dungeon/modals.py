from src.modules.KivyBase.Hoverable import ModalViewBase as ModalView
from kivy.properties import BooleanProperty, NumericProperty, StringProperty


class DMConfirmWidget(ModalView):
    descending = BooleanProperty(False)
    current_floor = StringProperty('')
    next_floor = StringProperty('')
    recc_score = NumericProperty(0)
    act_score = NumericProperty(0)

    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        super().__init__(**kwargs)

    def confirm(self):
        self.dismiss()
        self.dispatch('on_confirm')

    def on_confirm(self):
        pass
