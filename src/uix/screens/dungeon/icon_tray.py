from game.effect import CONDITION, STAT_TYPES
from game.status_effect import STATUS_EFFECTS
from kivy.uix.recycleview import RecycleView
from loading.kv_loader import load_kv

load_kv(__name__)


class IconTray(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._applied_icons = []

    def on_touch_down(self, touch):
        return False

    def on_touch_move(self, touch):
        return False

    def on_touch_up(self, touch):
        return False

    def update_icons(self, entity):
        self._applied_icons = []
        for effect_type, effects in entity.get_effects().items():  # For updating icons at end of every turn
            if effect_type == CONDITION:
                continue
            for effect_id, effect in effects.items():
                if effect_id.split(' ')[-1] in STATUS_EFFECTS.values():
                    continue
                if effect_type in STAT_TYPES:
                    icon = f"{effect_type}{'+' if effect.get_amount() > 0 else '-'}"
                else:
                    icon = f"{effect_type}"
                if icon in self._applied_icons:
                    continue
                self._applied_icons.append(icon)

        self.refresh_from_appplied()

    def refresh_from_appplied(self):
        applied_icons = []
        for icon in self._applied_icons:
            applied_icons.append({'source': f'icons/{icon}.png'})
        self.data = applied_icons
        self.refresh_from_data()

    def apply_icons(self, icons):
        for icon in icons:
            if icon in self._applied_icons:
                continue
            self._applied_icons.append(icon)
        self.refresh_from_appplied()

    def remove_icons(self, icons):
        for icon in icons:
            if icon not in self._applied_icons:
                continue
            self._applied_icons.remove(icon)
        self.refresh_from_appplied()

    def clear_icons(self):
        self.data = []
        self._applied_icons = []
