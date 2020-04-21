from src.modules.KivyBase.Hoverable import ScrollViewH as ScrollView
from kivy.properties import NumericProperty


class SkillsList(ScrollView):
    height_unit = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)