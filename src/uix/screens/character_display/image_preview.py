# UIX Imports
# Kivy Imports
from kivy.properties import ObjectProperty

# KV Import
from loading.kv_loader import load_kv
from uix.modules.screen import Screen

load_kv(__name__)


class ImagePreview(Screen):
    char = ObjectProperty(None)
