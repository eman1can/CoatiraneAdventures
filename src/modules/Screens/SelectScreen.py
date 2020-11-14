from kivy.app import App

from src.modules.KivyBase.Hoverable import ScreenBase as Screen


class SelectScreen(Screen):
    def choose_character(self, choice):
        # print('Chosen Character: %s, adding to char Array.' % choice)
        root = App.get_running_app().main
        testing = False
        if testing:
            for x in root.characters:
                root.obtained_characters.append(x.get_index())
                if x.is_support():
                    root.obtained_characters_s.append(x.get_index())
                else:
                    root.obtained_characters_a.append(x.get_index())
            root.display_screen('town_screen', True, False)
        else:
            char = support = False
            for x in root.characters:
                id = x.get_id()
                if id == choice:
                    x.first = True
                    root.obtained_characters.append(x.get_index())
                    root.obtained_characters_a.append(x.get_index())
                    char = True
                if id == 'enticing_misha':
                    root.obtained_characters.append(x.get_index())
                    root.obtained_characters_s.append(x.get_index())
                    support = True
                if char and support:
                    root.display_screen('town_screen', True, False)
                    return