from kivy.app import App
from kivy.uix.widget import Widget
from src.lwf.src.LWF import LWF
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout


class WindowObject(Widget):
    def __init__(self):
        super().__init__()
        layout = FloatLayout()
        button = Button(size_hint=(None, None), x=self.width/2, y=self.height-50, size=(100, 200), text="Push me!", on_release=lambda instance: self.stop_start())
        layout.add_widget(button)
        self.add_widget(layout)
        self.lwf = None
        self.play_lwf()

    def play_lwf(self):
        stage = Widget()
        stage.width = 0
        stage.height = 0
        self.add_widget(stage)

        # lwf.useCanvasRenderer()

        cache = LWF.ResourceCache.get()

        win = self
        def load(settings, lwf):
            # lwf.rendererFactory = cache.newFactory(settings, cache, lwf.data)
            # lwf = lwf(lwf.data, cache.newFactory(settings, cache, lwf.data))
            win.lwf = lwf
            win.lwf.SetFrameRate(60)
        settings = {}
        settings['lwf'] = "animated_building.lwf"
        settings['prefix'] = "animated_building.lwfdata/"
        settings['stage'] = stage
        settings['onload'] = load
        cache.LoadLWF(settings)
        # self.lwf.rootMovie.Play()
        # self.lwf.rootMovie.SetVisible(True)
        self.update(0)
        # Clock.schedule_interval(self.update, 1/30)

    def update(self, dt):
        if self.lwf != None:
            self.lwf.Exec(dt)
            # self.lwf.Exec(self.calc_tick())
            self.lwf.Render()
        else:
            pass
            # print("The lwf is none!")
    #
    # def calc_tick(self):
    #     self.current_time = time.time()
    #     tick = self.current_time - self.from_time
    #     self.from_time = self.current_time
    #     return tick

    def stop_start(self):
        if self.lwf.rootMovie.playing:
            self.lwf.rootMovie.Stop()
        else:
            self.lwf.rootMovie.Play()


class BuildApp(App):
    def build(self):
        return WindowObject()

if __name__ == "__main__":
    window = BuildApp().run()
    # window.stop_start()