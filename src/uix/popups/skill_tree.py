from kivy.properties import NumericProperty, StringProperty

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

    def size_override(self):
        return 0.75, 0.5
