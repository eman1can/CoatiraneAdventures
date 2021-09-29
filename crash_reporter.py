from datetime import datetime
from os import environ, getcwd
import sys, platform

# Add src to python path
base_path = getcwd()
sys.path.insert(0, f'{base_path}\\src')
sys.path.insert(0, f'{base_path}\\res')
environ['KIVY_HOME'] = f'{base_path}\\data'

from kivy.config import Config
from kivy.utils import platform as operating_system

if operating_system == 'win':
    # Use ctypes to get resolution
    import ctypes

    user32 = ctypes.windll.user32
    width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
else:
    raise Exception("Running on unsupported Platform!")


Config.set('graphics', 'position', 'auto')
Config.set('graphics', 'width', int(width * 0.36))
Config.set('graphics', 'minimum_width', int(width * 0.36))
Config.set('graphics', 'height', int(height * 0.28))
Config.set('graphics', 'minimum_height', int(height * 0.28))
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'borderless', 0)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.hoverbutton import HoverButton

root = """
RootWindow:
    canvas:
        Color:
            rgba: 240 / 255, 240 / 255, 240 / 255, 1
        Rectangle:
            size: self.size
    ScrollView:
        size_hint: 1, 0.9
        pos_hint: {'top': 1}
        do_scroll_x: False
        do_scroll_y: True
        canvas.before:
            Color:
                rgba: 225 / 255, 225 / 255, 225 / 255, 1
            Rectangle:
                size: self.size
                pos: self.pos
        Label:
            id: label
            text_size: self.width, None
            text: 'blank'
            size_hint_y: None
            height: self.texture_size[1]
            color: 1, 0.2, 0.2, 1
            font_name: 'Calibri'
            font_size: root.height * 0.1 * 0.39
    Label:
        size_hint: 0.6, 0.048
        pos_hint: {'x': 0, 'y': 0.0278}
        color: 0, 0, 0, 1
        font_name: 'Calibri'
        font_size: root.height * 0.125 * 0.39
        text: 'You crashed! Would you like to send a crash report to the developers?'
    HoverButton:
        background_normal: '../res/uix/button_background.png'
        size_hint: 0.156, 0.048
        pos_hint: {'x': 0.627, 'y': 0.0278}
        color: 0, 0, 0, 1
        font_name: 'Calibri'
        font_size: root.height * 0.1 * 0.39
        text: 'Yes!'
        on_release: root.send_crash_report()
    HoverButton:
        background_normal: '../res/uix/button_background.png'
        size_hint: 0.156, 0.048
        pos_hint: {'x': 0.817, 'y': 0.0278}
        color: 0, 0, 0, 1
        font_name: 'Calibri'
        font_size: root.height * 0.1 * 0.39
        text: 'no'
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

"""


class RootWindow(RelativeLayout):
    def send_crash_report(self):
        self.send_email(self.stacktrace)
        self.close_launcher()

    def close_launcher(self):
        App.get_running_app().stop()

    def send_email(self, stacktrace):
        import smtplib, ssl

        crash_report = f'''
            Crash At: {datetime.now()}

            Game Type: {Config.get('coatiraneadventures', 'type')}
            Game Version: {Config.get('coatiraneadventures', 'version')}

            Processor Type: {platform.machine()}
            Processor: {platform.processor()}
            Operating System: {platform.platform()}

            Stacktrace:
            {stacktrace}
            '''
        email = f'''
                    Subject: Coatirane Adventures Crash Report
                    Message:
                    {crash_report}
                    '''

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login("eman.blitz@gmail.com", 'Alpha1112')

            server.sendmail('eman.blitz@gmail.com', 'ethan.wolfe212@gmail.com', email)


class StyledButton(HoverButton):
    pass


class Reporter(App):
    def __init__(self, logfile):
        self.logfile = logfile
        super().__init__()

    def build(self):
        self.title = 'Coatirane Adventures Crash Reporter'

        self.rootw = Builder.load_string(root)

        with open(self.logfile, 'r') as file:
            stacktrace = file.read()

        self.rootw.stacktrace = stacktrace
        self.rootw.ids.label.text = stacktrace

        return self.rootw


logfile = sys.argv[1]
launcher = Reporter(logfile).run()
sys.exit(0)
