from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang.builder import Builder
from kivy.uix.button import Button


Builder.load_string('''
<Root>:
    Main:
        id: main_screen
        canvas:
            Color:
                rgba: 0, 0, 0.4, 0.2
            Rectangle:
                size: self.size
                pos: self.pos
            Rectangle:
                size: 300, 300
                pos: 100, 150
        MyLayout:
            size_hint: None, None
            size: 300, 300
            pos: 100, 150
            Manager:
                size_hint: None, None
                size: 100, 250
                pos: 50, 50
                canvas:
                    Color:
                        rgba: 0.4, 0, 0, 0.2
                    Rectangle:
                        size: self.size
                        pos: self.pos
                Main:
                    MyButton:
                        size_hint: None, None
                        size: 25, 25
                        pos: 20, 20
            
            


''')


class Root(ScreenManager):
    def __init__(self, **kwargs):
        self.register_event_type('on_touch_hover')
        super().__init__(**kwargs)

    def on_touch_hover(self, hover):
        return False

    def on_touch_down(self, touch):
        print("\n\n\nRoot")
        print("\tclick at ", touch.pos)
        print("\tMy pos is ", self.pos)
        print("\tMy size is ", self.size)
        print(self.x, '<=', touch.x, '<=', self.right, ' | ', self.y, '<=', touch.y, '<=', self.top)
        print("\tCollide_point: ", self.collide_point(*touch.pos))

        if not self.collide_point(*touch.pos):
            return False

        for child in self.children:
            if child.dispatch('on_touch_down', touch):
                return True


class Manager(ScreenManager):
    def on_touch_down(self, touch):
        print("Manager")
        print("\tclick at ", touch.pos)
        print("\tMy pos is ", self.pos)
        print("\tMy size is ", self.size)
        print(self.x, '<=', touch.x, '<=', self.right, ' | ', self.y, '<=', touch.y, '<=', self.top)
        print("\tCollide_point: ", self.collide_point(*touch.pos))

        if not self.collide_point(*touch.pos):
            return False

        for child in self.children:
            if child.dispatch('on_touch_down', touch):
                return True


class Main(Screen):
    def on_touch_down(self, touch):
        print("Main")
        print("\tclick at ", touch.pos)
        print("\tMy pos is ", self.pos)
        print("\tMy size is ", self.size)
        print(self.x, '<=', touch.x, '<=', self.right, ' | ', self.y, '<=', touch.y, '<=', self.top)
        print("\tCollide_point: ", self.collide_point(*touch.pos))

        if not self.collide_point(*touch.pos):
            return False

        touch.push()
        touch.apply_transform_2d(self.to_local)
        for child in self.children:
            if child.dispatch('on_touch_down', touch):
                touch.pop()
                return True
        touch.pop()
        return False


class MyLayout(RelativeLayout):
    def on_touch_down(self, touch):
        print("MyLayout")
        print("\tclick at ", touch.pos)
        print("\tMy pos is ", self.pos)
        print("\tMy size is ", self.size)
        print(self.x, '<=', touch.x, '<=', self.right, ' | ', self.y, '<=', touch.y, '<=', self.top)
        print("\tCollide_point: ", self.collide_point(*touch.pos))

        if not self.collide_point(*touch.pos):
            return False

        touch.push()
        touch.apply_transform_2d(self.to_local)
        for child in self.children:
            if child.dispatch('on_touch_down', touch):
                touch.pop()
                return True
        touch.pop()
        return False


class MyButton(Button):
    def on_touch_down(self, touch):
        print("MyButton")
        print("\tclick at ", touch.pos)
        print("\tMy pos is ", self.pos)
        print("\tMy size is ", self.size)
        print(self.x, '<=', touch.x, '<=', self.right, ' | ', self.y, '<=', touch.y, '<=', self.top)
        print("\tCollide_point: ", self.collide_point(*touch.pos))
        return self.collide_point(*touch.pos)


class TestApp(App):
    def build(self):
        return Root()


if __name__ == '__main__':
    TestApp().run()