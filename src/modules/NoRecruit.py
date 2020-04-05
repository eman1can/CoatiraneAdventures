from kivy.properties import ObjectProperty

from src.modules.KivyBase.Hoverable import ModalViewH as ModalView


class NoRecruitWidget(ModalView):
    main_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
