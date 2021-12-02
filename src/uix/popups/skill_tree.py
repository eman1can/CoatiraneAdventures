from kivy.properties import NumericProperty, ObjectProperty, StringProperty

from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv
from refs import Refs
from uix.popups.view import View

load_kv(__name__)


class PerkInfo(View):
    perk_id = StringProperty('')
    perk_cost = NumericProperty(0)

    name = StringProperty('')
    description = StringProperty('')
    cost = StringProperty('')

    def __init__(self, perk_id, **kwargs):
        self.perk_id = perk_id
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        perk = Refs.gc['perks'][self.perk_id]

        self.name = f'{perk.get_name()} - {perk.get_tree().title()}'
        self.description = perk.get_description()
        self.perk_cost = perk.get_cost()
        self.cost = f'Costs {self.perk_cost} perk points to bestow on an adventurer'

        perk_points = Refs.gc.get_perk_points()
        meets_requirements = True
        for requirement in perk.get_requirements():
            if requirement == 'none':
                continue
            meets_requirements &= Refs.gc.has_perk(requirement)

        self.ids.bestow.enabled = perk_points >= self.perk_cost and (Refs.gc.get_skill_level() > self.perk_cost or self.perk_cost == 1) and meets_requirements

    def on_bestow(self):
        self.manager.manager.display_popup(self.manager.previous, 'perk_bestow', self.perk_id)
        self.manager.dismiss()

    def size_override(self):
        return 0.75, 0.5


class PerkBestow(View):
    perk_info = StringProperty('')

    def __init__(self, perk_id, **kwargs):
        super().__init__(**kwargs)
        self._perk_id = perk_id
        perk = Refs.gc['perks'][perk_id]
        self.perk_info = f'{perk.get_name()} - {perk.get_tree().title()} - Level {perk.get_level()}'

        characters = list(Refs.gc.get_obtained_characters(False))

        data = []
        for character in characters:
            meets_requirements = not character.has_perk(perk_id)

            for requirement in perk.get_requirements():
                if requirement == 'none':
                    continue
                meets_requirements &= character.has_perk(requirement)

            for char_perk_id in character.get_all_perks():
                meets_requirements &= Refs.gc['perks'][char_perk_id].get_tree() == perk.get_tree()

            if meets_requirements:
                data.append({'character': character.get_index(), 'callback': lambda char_id=character.get_id(): self.on_bestow(char_id)})
        self.ids.characters.data = data

    def size_override(self):
        return 0.75, 0.5

    def on_bestow(self, char_id):
        perk = Refs.gc['perks'][self._perk_id]
        cost = perk.get_cost()
        self.manager.manager.display_popup(self, 'confirm', title_text='Are you sure?', description_text=f'This will cost {cost} points.', on_confirm=lambda instance, char=char_id: self.do_bestow(char))

    def do_bestow(self, char_id):
        self.manager.dismiss()

        perk = Refs.gc['perks'][self._perk_id]
        character = Refs.gc.get_char_by_id(char_id)

        character.bestow_perk(perk.get_id())
        Refs.gc.unlock_perk(perk)

        self.manager.previous.update_perk_box(self._perk_id, char_id)


class SquarePerkCharacterPreview(RelativeLayout):
    callback = ObjectProperty(None)

    character = NumericProperty(-1)

    char_button_source = StringProperty('buttons/char_button_square')
    char_button_collide_image = StringProperty('')

    background_source = StringProperty('preview_square_background.png')
    char_image_source = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_character(self, *args):
        character = Refs.gc.get_char_by_index(self.character)
        self.char_image_source = character.get_image('preview')

    def handle_preview_click(self):
        self.callback()
