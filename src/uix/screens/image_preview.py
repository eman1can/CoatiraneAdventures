# UIX Imports
from uix.modules.screen import Screen

# Kivy Imports
from kivy.properties import ObjectProperty

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class ImagePreview(Screen):
    char = ObjectProperty(None)
