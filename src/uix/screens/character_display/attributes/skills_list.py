# Kivy Imports
from kivy.properties import NumericProperty
from kivy.uix.scrollview import ScrollView

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class SkillsList(ScrollView):
    height_unit = NumericProperty(0)
