from kivy.properties import ObjectProperty, BooleanProperty

from src.modules.KivyBase.Hoverable import RelativeLayoutH as RelativeLayout


class SinglePreview(RelativeLayout):
    preview = ObjectProperty(None)
    character = ObjectProperty(None)
    is_support = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def reload(self):
        self.root.reload()
