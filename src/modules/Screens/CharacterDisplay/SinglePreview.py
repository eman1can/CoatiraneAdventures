from kivy.properties import ObjectProperty, BooleanProperty

from src.modules.KivyBase.Hoverable import RelativeLayoutBase as RelativeLayout


class SinglePreview(RelativeLayout):
    preview = ObjectProperty(None)
    character = ObjectProperty(None)
    is_support = BooleanProperty(False)

    def reload(self):
        self.root.reload()
