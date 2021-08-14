import json
from os import listdir
from os.path import exists

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

root = '''
<Window>:
    Image:
        id: image
        size_hint: 1, 0.8
        pos_hint: {'y': 0.2}
    Button:
        id: button
        size_hint: 0.9, 0.1
        text: 'Set Name and Version Name'
        on_release: root.save_key()
    Button:
        id: close
        size_hint: 0.1, 0.1
        pos_hint: {'x': 0.9}
        text: 'Exit'
        on_release: root.close()
    TextInput:
        id: name_input
        multiline: False
        write_tab: False
        size_hint: 0.5, 0.1
        pos_hint: {'y': 0.1}
        hint_text: 'Name'
    TextInput:
        id: version_input
        multiline: False
        size_hint: 0.5, 0.1
        pos_hint: {'y': 0.1, 'x': 0.5}
        hint_text: 'Version Name'
'''


Builder.load_string(root)


class Window(RelativeLayout):
    def __init__(self):
        super().__init__()

        self.ids.version_input.bind(on_text_validate=self.save_key)

        game_extract_location = 'C:/Users/Zoe/Code Projects/PycharmProjects/CoatiraneAdventures Development/Game Extracts/'

        latest = None
        latest_extract = None
        for game_extract in listdir(game_extract_location):
            month, day, year = game_extract[len('Extract '):].split('-')
            date = f'{year}{month}{day}'
            if latest is None or date > latest:
                latest = date
                latest_extract = game_extract

        self.latest_asset_location = f'{game_extract_location}{latest_extract}/'

        # self.ids = {}
        # self.char_id_to_name = {}
        # self.type_id_to_name = {}
        self.images = []

        for x in range(1, 9):
            path = f'{self.latest_asset_location}{x}/files/character/lottery'
            if exists(path):
                for char_key in listdir(path):
                    self.images.append(f'{path}/{char_key}/all_rectangle.png')

        self.images.sort()

        self.chars = {}
        self.char_versions = {}
        if exists('output.json'):
            with open('output.json', 'r') as file:
                input = json.load(file)
                if 'chars' in input:
                    self.chars = input['chars']
                if 'versions' in input:
                    self.char_versions = input['versions']

        self.goto_next_key()

    def close(self):
        with open('output.json', 'w') as file:
            output = {
                'chars': self.chars,
                'versions': self.char_versions
            }
            json.dump(output, file)
        quit(0)

    def save_key(self, *args):
        name = self.ids.name_input.text.strip()
        version_name = self.ids.version_input.text.strip()
        if name is None or name == '':
            return
        if version_name is None or version_name == '':
            return
        basename = self.filename.split('/')[-2]
        char_key, version_key = basename[8:11], basename[7] + basename[11:]
        if char_key not in self.chars:
            self.chars[char_key] = name
        if char_key not in self.char_versions:
            self.char_versions[char_key] = {}
        if version_key not in self.char_versions[char_key]:
            self.char_versions[char_key][version_key] = version_name
        self.goto_next_key()

    def goto_next_key(self):
        while True:
            self.filename = self.images[0]
            basename = self.filename.split('/')[-2]
            char_key, version_key = basename[8:11], basename[7] + basename[11:]
            if char_key in self.chars and version_key in self.char_versions[char_key]:
                self.images.pop(0)
            else:
                break
        self.filename = self.images.pop(0)
        basename = self.filename.split('/')[-2]
        char_key, version_key = basename[8:11], basename[7] + basename[11:]
        print(char_key, version_key)
        if char_key in self.chars:
            self.ids.name_input.text = self.chars[char_key]
        else:
            self.ids.name_input.text = ''
        self.ids.version_input.text = ''
        self.ids.image.source = self.filename

        # char_keys = list(chars.keys())
        # char_keys.sort()
        # for char in char_keys:
        #     types = chars[char]
        #     if char in self.char_id_to_name:
        #         name = self.char_id_to_name[char]
        #     else:
        #         name = ''

            # print(f'{char} - {name}')
            # types.sort()
            # for type in types:
            #     if char in self.type_id_to_name and type in self.type_id_to_name[char]:
            #         type_name = self.type_id_to_name[char][type]
            #     else:
            #         type_name = ''
            #     print(f'\t{type} - {type_name}')


class Main(App):
    def build(self):
        return Window()


if __name__ == "__main__":
    Main().run()
