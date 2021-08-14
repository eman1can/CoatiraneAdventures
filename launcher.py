from os import environ

base_path = environ['CA_PATH']
environ['KIVY_HOME'] = base_path + '/data/'

print('LAUNCHING from', base_path)

from kivy.config import Config
from kivy.utils import platform

monitor_positions = []
if platform == 'win':
    # Use ctypes to get resolution
    import ctypes
    user32 = ctypes.windll.user32
    width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    monitors = user32.GetSystemMetrics(80)

    import win32api
    monitor_list = win32api.EnumDisplayMonitors()
    for monitor in monitor_list:
        info = win32api.GetMonitorInfo(monitor[0])
        (x, t, r, y) = info['Work']
        monitor_positions.insert(0, (x, t, r, y))
else:
    raise Exception("Running on unsupported Platform!")

(x, y, r, t) = monitor_positions[0]
sw, sh = r - x, t - y
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', int(x + sw / 2 - sw * 0.09))
Config.set('graphics', 'top', int(y + sh / 2 - sh * 0.14))
Config.set('graphics', 'borderless', 0)

from configparser import NoOptionError
try:
    if width != int(Config.get('graphics', 'screen_width')) or height != int(Config.get('graphics', 'screen_height')):
        Config.set('graphics', 'screen_width', width)
        Config.set('graphics', 'screen_height', height)
except NoOptionError:
    Config.set('graphics', 'screen_width', width)
    Config.set('graphics', 'screen_height', height)

Config.set('graphics', 'width', int(width * 0.18))
Config.set('graphics', 'minimum_width', int(width * 0.18))
Config.set('graphics', 'height', int(height * 0.28))
Config.set('graphics', 'minimum_height', int(height * 0.28))
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'borderless', 0)
play_game = False

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.hoverbutton import HoverButton
from kivy.properties import ListProperty, BooleanProperty


class TabPanel(RelativeLayout):
    pass

root = """
<TabPanel>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.width, self.height * 0.878
        Rectangle:
            size: self.width * 0.128, self.height * 0.122
            pos: 0, self.height * 0.878
        Color:
            rgba: 217 / 255, 217 / 255, 217 / 255, 1
        Rectangle:
            size: 1, self.height
        Rectangle:
            size: self.width * 0.128, 1
            pos: 0, self.height - 1
        Rectangle:
            size: 1, self.height * 0.122
            pos: self.width * 0.128 - 1, self.height * 0.878
        Rectangle:
            size: self.width * 0.872, 1
            pos: self.width * 0.128, self.height * 0.878
        Rectangle:
            size: 1, self.height
            pos: self.width - 1, 0
        Rectangle:
            size: self.width, 1
    RelativeLayout: # 441, 171
        id: tab1
        Button:
            opacity: 0
            size_hint: 0.128, 0.122
            pos_hint: {'top': 1}
        Label:
            size_hint: 0.128, 0.122
            pos_hint: {'top': 1}
            font_name: 'Calibri'
            font_size: root.height * 0.1
            text: 'Graphics'
            color: 0, 0, 0, 1
            background_color: 1, 1, 1, 1
        RelativeLayout:
            size_hint: 0.77, 0.467
            pos_hint: {'x': 0.099, 'y': 0.194}
            # 340, 80s
            RelativeLayout:
                size_hint: 0.338, 1
                Label:
                    size_hint: 1, 0.333
                    font_name: 'Calibri'
                    font_size: root.height * 0.1
                    text: 'Select monitor'
                    color: 0, 0, 0, 1
                Label:
                    size_hint: 1, 0.333
                    pos_hint: {'y': 0.333}
                    font_name: 'Calibri'
                    font_size: root.height * 0.1
                    text: 'Graphics quality'
                    color: 0, 0, 0, 1
                Label:
                    size_hint: 1, 0.333
                    pos_hint: {'y': 0.666}
                    font_name: 'Calibri'
                    font_size: root.height * 0.1
                    text: 'Screen resolution'
                    color: 0, 0, 0, 1
            RelativeLayout:
                size_hint: 0.373, 1
                pos_hint: {'x': 0.338}
                HoverButton:
                    id: resolution_button
                    size_hint: 1, 0.2625
                    pos_hint: {'top': 1}
                    background_normal: 'res/uix/launcher/drop_down.png'
                    on_release:
                        screen_resolution.open(self)
                        monitor.close()
                        graphics_quality.close()
                    color: 0, 0, 0, 1
                    font_name: 'Calibri'
                    font_size: root.height * 0.1
                HoverButton:
                    id: graphics_quality_button
                    size_hint: 1, 0.2625
                    pos_hint: {'center_y': 0.5}
                    background_normal: 'res/uix/launcher/drop_down.png'
                    on_release:
                        graphics_quality.open(self)
                        monitor.close()
                        screen_resolution.close()
                    color: 0, 0, 0, 1
                    font_name: 'Calibri'
                    font_size: root.height * 0.1
                HoverButton:
                    id: monitor_button
                    size_hint: 1, 0.2625
                    background_normal: 'res/uix/launcher/drop_down.png'
                    on_release:
                        monitor.open(self)
                        graphics_quality.close()
                        screen_resolution.close()
                    color: 0, 0, 0, 1
                    font_name: 'Calibri'
                    font_size: root.height * 0.1
            RelativeLayout:
                size_hint: 0.373, 1
                pos_hint: {'x': 0.676}
                ToggleButton:
                    size_hint: 0.246, 0.26
                    pos_hint: {'top': 1}
                    id: windowed
                    background_normal: 'res/uix/launcher/box_not_checked.png'
                    background_down: 'res/uix/launcher/box_checked.png'
                    state: 'down'
                Label:
                    size_hint: 0.754, 0.26
                    pos_hint: {'top': 1, 'x': 0.246}
                    font_name: 'Calibri'
                    font_size: root.height * 0.1
                    text: 'Windowed'
                    color: 0, 0, 0, 1
        DropDownList: # 126, 92
            id: screen_resolution
            disabled: True
            opacity: 0
            size_hint: 0.285, 0.538
            pos_hint: {'x': 0.360}
        DropDownList: # 126, 62
            id: graphics_quality
            disabled: True
            opacity: 0
            size_hint: 0.285, 0.362
            pos_hint: {'x': 0.360}
        DropDownList: # 126, 33
            id: monitor
            disabled: True
            opacity: 0
            size_hint: 0.285, 0.192
            pos_hint: {'x': 0.360}
                    
RootWidget:
    canvas:
        Color:
            rgba: 240 / 255, 240 / 255, 240 / 255, 1
        Rectangle:
            size: self.size
    Image:
        id: banner
        source: 'res/uix/launcher/launcher_banner.png'
        size_hint: 0.95, 0.39
        pos_hint: {'x': 0.025, 'top': 0.975}
    TabPanel:
        id: graphics_panel
        size_hint: 0.95, 0.39
        pos_hint: {'x': 0.025, 'y': 0.111}
    HoverButton:
        background_normal: 'res/uix/launcher/button_background.png'
        size_hint: 0.156, 0.048
        pos_hint: {'x': 0.627, 'y': 0.0278}
        color: 0, 0, 0, 1
        font_name: 'Calibri'
        font_size: root.height * 0.1 * 0.39
        text: 'Play!'
        on_release: root.write_config_and_run()
    HoverButton:
        background_normal: 'res/uix/launcher/button_background.png'
        size_hint: 0.156, 0.048
        pos_hint: {'x': 0.817, 'y': 0.0278}
        color: 0, 0, 0, 1
        font_name: 'Calibri'
        font_size: root.height * 0.1 * 0.39
        text: 'Quit!'
        on_release: root.close_launcher()

<StyledButton>:
    background_normal: ''
    canvas.before:
        Color:
            rgba: 217 / 255, 217 / 255, 217 / 255, 1
        Rectangle:
            size: self.size
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.width - 2, self.height - 2
            pos: 1, 1
    color: 0, 0, 0, 1
    font_name: 'Calibri'
    
<DropDownList>:
    RecycleView:
        id: list
        viewclass: 'StyledButton'
        RecycleBoxLayout:
            default_size: None, 20
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
"""


class DropDownList(RelativeLayout):
    is_open = BooleanProperty(False)
    data = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button = None

    def on_data(self, instance, value):
        self.ids.list.data = self.data

    def open(self, button):
        if self.is_open:
            self.close()
            return
        self.button = button
        self.is_open = True
        self.disabled = False
        self.opacity = 1

    def close(self):
        self.is_open = False
        self.disabled = True
        self.opacity = 0
        self.button = None

    def set_resolution(self, width):
        height = width / 16 * 9
        if self.button is not None:
            self.button.text = f'{width} x {int(height)}'
        self.close()

    def set_quality(self, quality):
        if self.button is not None:
            self.button.text = quality
        self.close()

    def set_monitor(self, monitor):
        if self.button is not None:
            self.button.text = monitor
        self.close()

    def on_touch_down(self, touch):
        if self.disabled:
            return False
        return super().on_touch_down(touch)


class StyledButton(HoverButton):
    pass


class RootWidget(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def close_launcher(self):
        App.get_running_app().stop()

    def write_config_and_run(self):
        global play_game
        play_game = True
        windowed = self.ids.graphics_panel.ids.windowed.state == 'down'
        monitor_name = self.ids.graphics_panel.ids.monitor_button.text
        monitor_index = self.monitor_names.index(monitor_name)
        resolution_text = self.ids.graphics_panel.ids.resolution_button.text
        width, height = resolution_text.split(' x ')
        w, h = int(width), int(height)

        (x, t, r, y) = monitor_positions[monitor_index]
        sw, sh = r - x, y - t
        if sw == w and sh == h:
            windowed = False
        Config.set('graphics', 'position', 'custom')
        Config.set('graphics', 'left', int(x + sw / 2 - w * 0.5))
        Config.set('graphics', 'top', int(t + sh / 2 - h * 0.5))
        Config.set('graphics', 'width', w)
        Config.set('graphics', 'height', h)
        Config.set('graphics', 'borderless', (not windowed))
        Config.set('graphics', 'fullscreen', (not windowed))
        Config.write()

        print('Play on monitor', monitor_index)
        print('Play at resolution', w, h)
        print('Play windowed', windowed)
        self.close_launcher()


class Launcher(App):
    def build(self):
        self.title = 'Coatirane Adventures Launcher'
        self.rootw = Builder.load_string(root)

        sizes = [(5120, 2880), (3200, 1800), (3840, 2160), (2560, 1440),
                 (2048, 1152), (1920, 1080), (1600, 900), (1366, 768),
                 (1280, 720), (1152, 648), (1024, 576), (960, 540), (640, 360)]
        self.resolution = None
        resolution_buttons = []
        screen_resolution = self.rootw.ids.graphics_panel.ids.screen_resolution
        for (swidth, sheight) in sizes:
            if swidth > width or sheight > height:
                continue
            if self.resolution is None:
                self.resolution = swidth
                self.rootw.ids.graphics_panel.ids.resolution_button.text = f'{swidth} x {sheight}'
            resolution_buttons.append({'size_hint_y': None, 'height': height*0.28*0.0487, 'text': f'{swidth} x {sheight}', 'on_release': lambda w=swidth: screen_resolution.set_resolution(w)})

        screen_resolution.data = resolution_buttons
        self.rootw.ids.graphics_panel.ids.graphics_quality_button.text = 'Standard'
        graphics_quality = self.rootw.ids.graphics_panel.ids.graphics_quality
        graphics_quality.data = [{'size_hint_y': None, 'height': height*0.28*0.0487, 'text': f'Standard', 'on_release': lambda: graphics_quality.set_quality('Standard')}]

        monitor = self.rootw.ids.graphics_panel.ids.monitor
        monitor_list = []
        monitor_names = []
        for monitor_name in [f'Display {x + 1}' for x in range(monitors)]:
            if monitor_name == 'Display 1':
                monitor_name += ' (Main)'
            monitor_names.append(monitor_name)
            monitor_list.append({'size_hint_y': None, 'height': height*0.28*0.0487, 'text': monitor_name, 'on_release': lambda name=monitor_name: monitor.set_monitor(name)})
        self.rootw.ids.graphics_panel.ids.monitor_button.text = f'Display 1 (Main)'
        monitor.data = monitor_list
        self.rootw.monitor_names = monitor_names
        return self.rootw


if __name__ == "__main__":
    # Open Launcher

    launcher = Launcher()
    root_widget = launcher.build()
    launcher.run()
    if play_game:
        quit(0)
    quit(1)
