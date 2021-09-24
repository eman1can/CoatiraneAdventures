from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty

from game.effect import CONDITION, COUNTER, COUNTER_TYPES, DURATION, DURATION_TYPES, EFFECT_TYPES, SPECIFIC_TARGET, STAT, STATUS_EFFECT, STAT_TYPES
from game.enemy import NICKNAMES
from game.skill import ELEMENTS
from game.status_effect import STATUS_EFFECTS
from kivy.uix.relativelayout import RelativeLayout
from loading.kv_loader import load_kv
from uix.popups.view import View

load_kv(__name__)


class InspectionItem(RelativeLayout):
    text = StringProperty('')
    icon_source = StringProperty('')
    indent = BooleanProperty(False)


class Inspection(View):
    name = StringProperty('')

    background_source = StringProperty('')
    portrait_source = StringProperty('')

    element_source = StringProperty('')
    sub_element_source = StringProperty('')

    health = NumericProperty(0)
    max_health = NumericProperty(0)

    # affect_list = ListProperty([])

    def __init__(self, entity, **kwargs):
        super().__init__(**kwargs)
        self.set_info(entity)

    def set_info(self, entity):
        self.name = entity.get_name()
        self.health = entity.get_battle_health()
        self.max_health = entity.get_health()

        if entity.is_enemy():
            self.background_source = f'items/frame_1.png'
            self.portrait_source = f'items/Goblin 1.png'
            for index, nickname in enumerate(NICKNAMES[1:]):
                if self.name.startswith(nickname):
                    self.background_source = f'res/uix/items/frame_{int((index + 1) / 3) + 1}.png'
                    monster_name = self.name[len(nickname):]
                    if index < 5:
                        self.portrait_source = f'res/uix/items/{monster_name} {index + 2}.png'
                    else:
                        self.portrait_source = f'res/uix/items/{monster_name} {index - 1}.png'
                    break
        else:
            self.background_source = f'items/frame_1.png'
            self.portrait_source = entity.get_image('preview')

        self.element_source = ELEMENTS[entity.get_element()]
        if entity.is_enemy():
            self.sub_element_source = ELEMENTS[entity.get_sub_element()]
        else:
            self.sub_element_source = ''

        effect_list = self._get_effect_list(entity.get_effects())

        self.ids.effect_list.data = effect_list
        self.ids.effect_list.refresh_from_data()

    def _get_effect_list(self, effect_list, status_effects_only=False):
        affect_list = []
        for effect_type, effects in effect_list.items():
            if effect_type == CONDITION:
                continue
            for effect_id, effect in effects.items():
                if effect_id.split(' ')[-1] in STATUS_EFFECTS.values():
                    if status_effects_only:
                        affect_list.append(self._get_status_effect_source(effect_type, effect, effect.get_applied_name()))
                    continue
                elif status_effects_only:
                    continue

                affect_list.append(self._get_effect_source(effect_type, effect, effect.get_parent_name(), effect.get_applied_name()))
                if effect_type in EFFECT_TYPES:
                    affect_list += self._get_effect_list(effect_list, True)
        return affect_list

    def _get_effect_source(self, effect_type, effect, entity_name, name):
        if effect_type in STAT_TYPES:
            suffix = '+' if effect.get_amount() > 0 else '-'
            if effect.get_duration() == 0:
                text = f'{int(effect.get_amount() * 100)}% {STAT_TYPES[effect_type]} - Assist Skill - {name} - {entity_name}'
            else:
                text = f'{int(effect.get_amount() * 100)}% {STAT_TYPES[effect_type]} - {int(effect.get_duration())} turns - {name} - {entity_name}'
            return {'icon_source': f'icons/{effect_type}{suffix}.png', 'text': text, 'indent': False}
        elif effect_type in DURATION_TYPES:
            text = f'{DURATION_TYPES[effect_type]} x{int(effect.get_amount())} - {name} - {entity_name}'
            return {'icon_source': f'icons/{effect_type}.png', 'text': text, 'indent': False}
        elif effect_type in COUNTER_TYPES:
            text = f'{COUNTER_TYPES[effect_type]} x{int(effect.get_amount())} - {name} - {entity_name}'
            return {'icon_source': f'icons/{effect_type}.png', 'text': text, 'indent': False}
        elif effect_type in EFFECT_TYPES:
            text = f'{EFFECT_TYPES[effect_type][effect.get_amount()]} - {name} - {entity_name}'
            return {'icon_source': f'icons/{effect_type}.png', 'text': text, 'indent': False}
        else:
            text = f'Unknown - {name} - {entity_name}'
            return {'icon_source': f'icons/{effect_type}.png', 'text': text, 'indent': False}

    def _get_status_effect_source(self, effect_type, effect, name):
        if effect_type in STAT_TYPES:
            suffix = '+' if effect.get_amount() > 0 else '-'
            text = f'{int(effect.get_amount() * 100)}% {STAT_TYPES[effect_type]} - {name}'
            return {'icon_source': f'icons/{effect_type}{suffix}.png', 'text': text, 'indent': True}
        else:
            text = f'Unknown - {name}'
            return {'icon_source': f'icons/{effect_type}.png', 'text': text, 'indent': True}
