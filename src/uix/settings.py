__all__ = ('Settings',)

from kivy.app import App
from kivy.config import Config, ConfigParser
from kivy.core.window import Window
from kivy.metrics import dp, platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingSpacer, SettingsWithSidebar


class Settings(SettingsWithSidebar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        settings_config = ConfigParser()
        settings_config.read('../save/settings.ini')
        if platform == 'win':
            self.add_json_panel('General', settings_config, '../save/settings/general.json')
        elif platform == 'android':
            self.add_json_panel('General', settings_config, '../save/settings/general_android.json')

    def on_config_change(self, config, section, key, value):
        app = App.get_running_app()
        if section == 'graphics':
            if key == 'window':
                if value == 'FullScreen':
                    Config.set('graphics', 'fullscreen', 1)

                    app.log('Restart is needed to apply changes')
                    width = min(0.95 * Window.width, dp(500))
                    popup = RestartPopup(app, title='Restart Needed', size_hint=(None, None), size=(width, '400dp'))
                    popup.open()

                elif value == 'Windowed':
                    Config.set('graphics', 'fullscreen', 0)
                    Config.set('graphics', 'borderless', 0)
                    app.make_windowed()
                elif value == 'Fake FullScreen':
                    Config.set('graphics', 'fullscreen', 0)
                    Config.set('graphics', 'borderless', 1)
                    app.make_fake_fullscreen()
        Config.write()


class RestartPopup(Popup):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.content = BoxLayout(orientation='vertical', spacing='5dp')
        self.content.add_widget(Label(text='Please restart the game to apply these changes', size_hint_y=None, height=dp(100)))
        self.content.add_widget(SettingSpacer())
        btn = Button(text='Ok', size_hint_y=None, height=dp(50))
        btn.bind(on_release=self.dismiss)
        self.content.add_widget(btn)
        self.app = app
