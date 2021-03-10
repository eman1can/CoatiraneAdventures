# coding=utf-8

from kivy.garden.spine import SpineAsset
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

kv = """
BoxLayout:
    orientation: "vertical"
    BoxLayout:
        size_hint_y: None
        height: "48dp"
        CheckBox:
            id: pause
        CheckBox:
            id: debug
        Spinner:
            id: assets
            size_hint_y: None
            height: "48dp"
            # text: "data/1040142001"
            text: "data/dragon"
            values: ("data/dragon", "data/spineboy", "data/goblins", "data/alien/alien", "data/spinosaurus", "data/powerup", "data/1041042001")
            on_text: dragon.filename = self.text
        Spinner:
            id: valign
            size_hint_y: None
            height: "96dp"
            text: "middle"
            values: ("middle", "bottom")
            on_text: dragon.valign = self.text
    Spinner:
        size_hint_y: None
        height: "96dp"
        text: (dragon.animations or ["-"])[0]
        values: dragon.animations
        on_text: dragon.animate(self.text)
    SpineAsset:
        id: dragon
        # filename: "data/1041042001"
        filename: "data/dragon"
        debug: debug.active
        pause: pause.active
"""

class SpineApp(App):
    def build(self):
        from kivy.lang import Builder
        return Builder.load_string(kv)


if __name__ == "__main__":
    SpineApp().run()
