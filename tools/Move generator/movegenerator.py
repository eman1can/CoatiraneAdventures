from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout

from game.effect import Effect

Config.set('kivy', 'keyboard_mode', 'system')
from kivy.app import App
from kivy.lang.builder import Builder

from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

kv = """

<BaseWindow>:
    Label:
        size_hint: 0.7, 0.1
        pos_hint: {'x': 0, 'top': 1}
        font_size: root.height * 0.1
        font_name: 'Gabriola'
        text: 'Move Generator'
        color: 1, 1, 1, 1
    Button:
        size_hint: 0.3, 0.1
        pos_hint: {'x': 0.7, 'top': 1}
        text: 'Output'
        on_release: root.on_output()
    ToggleButton:
        id: toggle_ability
        size_hint: 0.5, 0.1
        pos_hint: {'x': 0, 'top': 0.9}
        text: 'Ability'
        group: 'main_type'
        state: 'down'
    ToggleButton:
        id: toggle_skill
        pos_hint: {'x': 0.5, 'top': 0.9}
        size_hint: 0.5, 0.1
        text: 'Skill'
        group: 'main_type'
    RelativeLayout:
        id: skill
        size_hint: 1, 0.8
        pos_hint: {'x': 0, 'top': 0.8}
        disabled: False if toggle_skill.state == 'down' else True
        opacity: 1 if toggle_skill.state == 'down' else 0
        Label:
            size_hint: 0.3, 0.1
            pos_hint: {'x': 0, 'top': 1}
            font_size: ability.height * 0.1
            font_name: 'Gabriola'
            text: 'Name: '
            color: 1, 1, 1, 1
        TextInput:
            id: skill_name
            hint_text: 'Agitation'
            multiline: False
            size_hint: 0.7, 0.1
            pos_hint: {'x': 0.3, 'top': 1}
        Label:
            size_hint: 0.3, 0.1
            pos_hint: {'x': 0, 'top': 0.9}
            font_size: ability.height * 0.1
            font_name: 'Gabriola'
            text: 'Type: '
            color: 1, 1, 1, 1
        GridLayout:
            cols: 5
            rows: 1
            id: skill_type
            size_hint: 0.7, 0.1
            pos_hint: {'x': 0.3, 'top': 0.9}
            ToggleButton:
                text: 'Normal'
                group: 'type'
                state: 'down'
            ToggleButton:
                text: 'Special'
                group: 'type'
            ToggleButton:
                text: 'Counter'
                group: 'type'
            ToggleButton:
                text: 'Block'
                group: 'type'
            ToggleButton:
                text: 'Combo'
                group: 'type'
        Label:
            size_hint: 0.3, 0.1
            pos_hint: {'x': 0, 'top': 0.8}
            font_size: ability.height * 0.1
            font_name: 'Gabriola'
            text: 'Mana Cost: '
            color: 1, 1, 1, 1
        TextInput:
            id: skill_mana_cost
            hint_text: '30'
            multiline: False
            size_hint: 0.7, 0.1
            pos_hint: {'x': 0.3, 'top': 0.8}
        Label:
            size_hint: 0.3, 0.1
            pos_hint: {'x': 0, 'top': 0.7}
            font_size: ability.height * 0.1
            font_name: 'Gabriola'
            text: 'Power: '
            color: 1, 1, 1, 1
        GridLayout:
            rows: 1
            cols: 5
            size_hint: 0.7, 0.1
            pos_hint: {'x': 0.3, 'top': 0.7}
            id: skill_power
            ToggleButton:
                text: 'Low'
                group: 'power'
                state: 'down'
            ToggleButton:
                text: 'Mid'
                group: 'power'
            ToggleButton:
                text: 'High'
                group: 'power'
            ToggleButton:
                text: 'Ultra'
                group: 'power'
            ToggleButton:
                text: 'Super'
                group: 'power'
        Label:
            size_hint: 0.3, 0.1
            pos_hint: {'x': 0, 'top': 0.6}
            font_size: ability.height * 0.1
            font_name: 'Gabriola'
            text: 'Element: '
            color: 1, 1, 1, 1
        GridLayout:
            rows: 1
            cols: 6
            size_hint: 0.7, 0.1
            pos_hint: {'x': 0.3, 'top': 0.6}
            id: skill_element
            ToggleButton:
                text: 'Water'
                group: 'element'
                state: 'down'
            ToggleButton:
                text: 'Fire'
                group: 'element'
            ToggleButton:
                text: 'Light'
                group: 'element'
            ToggleButton:
                text: 'Dark'
                group: 'element'
            ToggleButton:
                text: 'Thunder'
                group: 'element'
            ToggleButton:
                text: 'Earth'
                group: 'element'
        Label:
            size_hint: 0.3, 0.1
            pos_hint: {'x': 0, 'top': 0.5}
            font_size: ability.height * 0.1
            font_name: 'Gabriola'
            text: 'Has Effect: '
            color: 1, 1, 1, 1
        GridLayout:
            cols: 2
            rows: 1
            size_hint: 0.7, 0.1
            pos_hint: {'x': 0.3, 'top': 0.5}
            id: skill_has_effect
            ToggleButton:
                text: 'True'
                group: 'has_effect'
                state: 'down'
            ToggleButton:
                text: 'False'
                group: 'has_effect'
        Button:
            id: add_effect
            text: 'Add Effect'
            size_hint: 1, 0.1
            pos_hint: {'x': 0, 'top': 0.4}
            on_release: root.add_effect()
    
    RelativeLayout:
        id: ability
        size_hint: 1, 0.8
        pos_hint: {'x': 0, 'top': 0.8}
        disabled: False if toggle_ability.state == 'down' else True
        opacity: 1 if toggle_ability.state == 'down' else 0
        Label:
            size_hint: 0.3, 0.1
            pos_hint: {'x': 0, 'top': 1}
            font_size: ability.height * 0.1
            font_name: 'Gabriola'
            text: 'Name: '
            color: 1, 1, 1, 1
        TextInput:
            id: ability_name
            hint_text: 'Agitation'
            multiline: False
            size_hint: 0.7, 0.1
            pos_hint: {'x': 0.3, 'top': 1}
        Label:
            size_hint: 0.3, 0.2
            pos_hint: {'x': 0, 'top': 0.9}
            font_size: ability.height * 0.1
            font_name: 'Gabriola'
            text: 'Description: '
            color: 1, 1, 1, 1
        TextInput:
            id: ability_description
            hint_text: 'Become luckier!'
            multiline: True
            size_hint: 0.7, 0.2
            pos_hint: {'x': 0.3, 'top': 0.9}
        Label:
            size_hint: 0.3, 0.1
            pos_hint: {'x': 0, 'top': 0.7}
            font_size: ability.height * 0.1
            font_name: 'Gabriola'
            text: 'Has Effect: '
            color: 1, 1, 1, 1
        GridLayout:
            id: ability_has_effect
            cols: 2
            size_hint: 0.7, 0.1
            pos_hint: {'x': 0.3, 'top': 0.7}
            ToggleButton:
                text: 'True'
                group: 'has_effect'
                state: 'down'
            ToggleButton:
                text: 'False'
                group: 'has_effect'
        Button:
            id: add_effect
            text: 'Add Effect'
            size_hint: 1, 0.1
            pos_hint: {'x': 0, 'top': 0.6}
            on_release: root.add_effect()
    ScrollView:
        id: scroll
        size_hint: 1, 0.2
        pos_hint: {'x': 0, 'top': 0.2}
        do_scroll_y: True
        GridLayout:
            id: effect_list
            size_hint_y: None
            height: self.minimum_height
            row_default_height: '45dp'
            row_force_default: True
            cols: 1
<EffectNamePopup>:
    auto_dismiss: False
    RelativeLayout:
        id: layout
        Button:
            size_hint: 0.5, 0.1
            text: 'Cancel'
            on_release: root.dismiss()
        Button:
            size_hint: 0.5, 0.1
            pos_hint: {'x': 0.5}
            text: 'Goto customization'
            on_release: root.on_add()
        TextInput:
            id: name
            font_size: layout.height *0.2
            hint_font_size: layout.height *0.2
            hint_text: 'What is the name of the effect?'
            multiline: True
            size_hint: 1, 0.9
            pos_hint: {'x': 0, 'top': 1}
            
<DeletePopup>:
    auto_dismiss: False
    RelativeLayout:
        id: layout
        Button:
            size_hint: 0.5, 0.1
            text: 'Cancel'
            on_release: root.dismiss()
        Button:
            size_hint: 0.5, 0.1
            pos_hint: {'x': 0.5}
            text: 'Delete Effect'
            on_release: root.on_delete()

<EffectPopup>:
    auto_dismiss: False
    RelativeLayout:
        id: layout
        Label:
            size_hint: 0.4, 0.1
            pos_hint: {'x': 0, 'top': 1}
            font_size: layout.height * 0.1
            font_name: 'Gabriola'
            text: 'Targeting Type: '
            color: 1, 1, 1, 1
        GridLayout:
            id: target_type
            cols: 4
            size_hint: 0.6, 0.1
            pos_hint: {'x': 0.4, 'top': 1}
            
            ToggleButton:
                text: 'All Foes'
                group: 'target_type'
                state: 'down'
            ToggleButton:
                text: 'One Foe'
                group: 'target_type'
            ToggleButton:
                text: 'All Allies'
                group: 'target_type'
            ToggleButton:
                text: 'Self'
                group: 'target_type'
        Label:
            size_hint: 0.4, 0.1
            pos_hint: {'x': 0, 'top': 0.9}
            font_size: layout.height * 0.1
            font_name: 'Gabriola'
            text: 'Duration: '
            color: 1, 1, 1, 1
        TextInput:
            id: duration
            hint_text: '10'
            multiline: False
            size_hint: 0.6, 0.1
            pos_hint: {'x': 0.4, 'top': 0.9}
        Label:
            size_hint: 0.2, 0.4
            pos_hint: {'x': 0, 'top': 0.8}
            font_size: layout.height * 0.1
            font_name: 'Gabriola'
            text: 'Type: '
            color: 1, 1, 1, 1
        GridLayout:
            id: effect_type
            cols: 6
            size_hint: 0.8, 0.4
            pos_hint: {'x': 0.2, 'top': 0.8}
            ToggleButton:
                text: 'Health'
                group: 'effect_type'
                on_release: root.show_sub(0)
                state: 'down'
            ToggleButton:
                text: 'Mana'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Strength'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Magic'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Endurance'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Dexterity'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Agility'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'PhysicalAttack'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'MagicalAttack'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Defense'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Damage'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Physical Resist'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Magical Resist'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Physical Null'
                group: 'effect_type'
                on_release: root.show_sub(1)
            ToggleButton:
                text: 'Magical Null'
                group: 'effect_type'
                on_release: root.show_sub(1)
            ToggleButton:
                text: 'Action Time'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Guard Chance'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Counter Chance'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Usage Block'
                group: 'effect_type'
                on_release: root.show_sub(-1)
            ToggleButton:
                text: 'Special Block'
                group: 'effect_type'
                on_release: root.show_sub(-1)
            ToggleButton:
                text: 'Target Focus'
                group: 'effect_type'
                on_release: root.show_sub(-1)
            ToggleButton:
                text: 'Cause Effect'
                group: 'effect_type'
                on_release: root.show_sub(2)
            ToggleButton:
                text: 'Heal Block'
                group: 'effect_type'
                on_release: root.show_sub(-1)
            ToggleButton:
                text: 'Potion Block'
                group: 'effect_type'
                on_release: root.show_sub(-1)
            ToggleButton:
                text: 'Focus Lock'
                group: 'effect_type'
                on_release: root.show_sub(-1)
            ToggleButton:
                text: 'Treason'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Drop Rate'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Drop Chance'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Spawn Rate'
                group: 'effect_type'
                on_release: root.show_sub(0)
            ToggleButton:
                text: 'Avoid'
                group: 'effect_type'
                on_release: root.show_sub(1)
            ToggleButton:
                text: 'Penetration'
                group: 'effect_type'
                on_release: root.show_sub(0)
        RelativeLayout:
            id: st_cause_effect
            opacity: 0
            disabled: True
            size_hint: 1, 0.4
            pos_hint: {'x': 0, 'top': 0.4}
            Label:
                size_hint: 0.4, 0.25
                pos_hint: {'x': 0, 'top': 1}
                font_size: layout.height * 0.1
                font_name: 'Gabriola'
                text: 'Efect Type: '
                color: 1, 1, 1, 1
            GridLayout:
                id: st_cause_effect_type
                cols: 7
                size_hint: 0.6, 0.25
                pos_hint: {'x': 0.4, 'top': 1}
                ToggleButton:
                    text: 'Poison'
                    group: 'chance_effect_type'
                    state: 'down'
                ToggleButton:
                    text: 'Stun'
                    group: 'chance_effect_type'
                ToggleButton:
                    text: 'Sleep'
                    group: 'chance_effect_type'
                ToggleButton:
                    text: 'Slow'
                    group: 'chance_effect_type'
                ToggleButton:
                    text: 'Taunt'
                    group: 'chance_effect_type'
                ToggleButton:
                    text: 'Seal'
                    group: 'chance_effect_type'
                ToggleButton:
                    text: 'Charm'
                    group: 'chance_effect_type'
            Label:
                size_hint: 0.4, 0.25
                pos_hint: {'x': 0, 'top': 0.75}
                font_size: layout.height * 0.1
                font_name: 'Gabriola'
                text: 'Effect Level: '
                color: 1, 1, 1, 1
            GridLayout:
                id: st_cause_effect_level
                cols: 4
                size_hint: 0.6, 0.25
                pos_hint: {'x': 0.4, 'top': 0.75}
                ToggleButton:
                    text: '1'
                    group: 'chance_effect_level'
                    state: 'down'
                ToggleButton:
                    text: '2'
                    group: 'chance_effect_level'
                ToggleButton:
                    text: '3'
                    group: 'chance_effect_level'
                ToggleButton:
                    text: '4'
                    group: 'chance_effect_level'
            Label:
                size_hint: 0.4, 0.25
                pos_hint: {'x': 0, 'top': 0.5}
                font_size: layout.height * 0.1
                font_name: 'Gabriola'
                text: 'Chance: '
                color: 1, 1, 1, 1
            TextInput:
                id: st_cause_effect_value
                hint_text: '0.25'
                multiline: False
                size_hint: 0.6, 0.25
                pos_hint: {'x': 0.4, 'top': 0.5}
        RelativeLayout:
            id: st_chance
            opacity: 0
            disabled: True
            size_hint: 1, 0.4
            pos_hint: {'x': 0, 'top': 0.4}
            Label:
                size_hint: 0.4, 0.25
                pos_hint: {'x': 0, 'top': 1}
                font_size: layout.height * 0.1
                font_name: 'Gabriola'
                text: 'Chance: '
                color: 1, 1, 1, 1
            TextInput:
                id: st_chance_value
                hint_text: '0.25'
                multiline: False
                size_hint: 0.6, 0.25
                pos_hint: {'x': 0.4, 'top': 1}
        RelativeLayout:
            id: st_amount
            opacity: 1
            size_hint: 1, 0.4
            pos_hint: {'x': 0, 'top': 0.4}
            Label:
                size_hint: 0.4, 0.25
                pos_hint: {'x': 0, 'top': 1}
                font_size: layout.height * 0.1
                font_name: 'Gabriola'
                text: 'Amount: '
                color: 1, 1, 1, 1
            TextInput:
                id: st_amount_value
                hint_text: '0.75'
                multiline: False
                size_hint: 0.6, 0.25
                pos_hint: {'x': 0.4, 'top': 1}
        Button:
            size_hint: 0.5, 0.1
            text: 'Cancel'
            on_release: root.dismiss()
        Button:
            size_hint: 0.5, 0.1
            pos_hint: {'x': 0.5}
            text: 'Add Effect to List'
            on_release: root.on_add()
"""


class DeletePopup(Popup):
    window = ObjectProperty(None, allownone=True)

    def on_delete(self):
        self.window.delete()
        self.dismiss()


class EffectButton(Button):
    effect = ListProperty([])
    list = ObjectProperty(None, allownone=True)

    def on_release(self):
        popup = DeletePopup(window=self, title=self.text)
        popup.open()

    def delete(self):
        self.list.remove_widget(self)


class EffectNamePopup(Popup):
    window = ObjectProperty(None, allownone=True)
    ranks = ListProperty([])

    def on_add(self):
        self.window.name_effect(self)


class EffectPopup(Popup):
    window = ObjectProperty(None, allownone=True)
    ranks = ListProperty([])

    def on_add(self):
        self.window.do_add_effect(self)

    def show_sub(self, sub_index):
        self.ids.st_amount.disabled = True
        self.ids.st_chance.disabled = True
        self.ids.st_cause_effect.disabled = True
        self.ids.st_amount.opacity = 0
        self.ids.st_chance.opacity = 0
        self.ids.st_cause_effect.opacity = 0
        if sub_index == -1:
            return
        elif sub_index == 0:
            self.ids.st_amount.opacity = 1
            self.ids.st_amount.disabled = False
            return
        elif sub_index == 1:
            self.ids.st_chance.opacity = 1
            self.ids.st_chance.disabled = False
            return
        elif sub_index == 2:
            self.ids.st_cause_effect.opacity = 1
            self.ids.st_cause_effect.disabled = False
            return


class BaseWindow(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_effect(self):
        popup = EffectNamePopup(window=self, title='Add Effect - Naming')
        popup.open()

    def name_effect(self, popup):
        popup.dismiss()
        self.new_effect = []
        self.new_effect.append(popup.ids.name.text)
        ranks = ['I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A', 'S', 'SS', 'SSS']
        rank = ranks.pop(0)
        popup = EffectPopup(window=self, title='Add Effect - ' + rank, ranks=ranks)
        popup.open()

    def do_add_effect(self, popup):
        popup.dismiss()
        new_effect = Effect()
        target_type = 0
        target_type_obj = popup.ids.target_type
        for child in reversed(target_type_obj.children):
            if child.state == 'down':
                break
            target_type += 1
        duration = int(popup.ids.duration.text)
        type = 0
        type_obj = popup.ids.effect_type
        for child in reversed(type_obj.children):
            if child.state == 'down':
                break
            type += 1
        new_effect.target_type = target_type
        new_effect.duration = duration
        new_effect.type = type
        if popup.ids.st_amount.opacity == 1:
            new_effect.st.append(float(popup.ids.st_amount_value.text))
        if popup.ids.st_chance.opacity == 1:
            new_effect.st.append(float(popup.ids.st_chance_value.text))
        if popup.ids.st_cause_effect.opacity == 1:
            ce_type = 0
            ce_type_obj = popup.ids.st_cause_effect_type
            for child in reversed(ce_type_obj.children):
                if child.state == 'down':
                    break
                ce_type += 1
            new_effect.st.append(ce_type)
            ce_level = 0
            ce_level_obj = popup.ids.st_cause_effect_level
            for child in reversed(ce_level_obj.children):
                if child.state == 'down':
                    break
                ce_level += 1
            new_effect.st.append(ce_level)
            new_effect.st.append(float(popup.ids.st_cause_effect_value.text))
        self.new_effect.append(new_effect)
        if len(popup.ranks) > 0:
            rank = popup.ranks.pop(0)
            new_popup = EffectPopup(window=self, title='Add Effect - ' + rank, ranks=popup.ranks)
            old_children, new_children = popup.children.copy(), new_popup.children.copy()
            for old_child, new_child in zip(old_children, new_children):
                new_child.opacity = old_child.opacity
                if isinstance(old_child, ToggleButton):
                    new_child.state = old_child.state
                elif isinstance(old_child, TextInput):
                    new_child.text = old_child.text
                else:
                    for old, new in zip(old_child.children, new_child.children):
                        old_children.append(old)
                        new_children.append(new)
            new_popup.open()
        else:
            self.ids.effect_list.add_widget(EffectButton(text=self.new_effect.pop(0), effect=self.new_effect, list=self.ids.effect_list))

    def on_output(self):
        with open("output/SAGenerated.txt", "a") as file:
            file.write("\n")
            if self.ids.skill.opacity == 0:
                file.write('1, -')
                file.write(", " + str(self.ids.ability_name.text))
                file.write(", " + str(self.ids.ability_description.text))
                has_effect = 0
                has_effect_obj = self.ids.ability_has_effect
                for child in has_effect_obj.children:
                    if child.state == 'down':
                        break
                    has_effect += 1
                file.write(", " + str(has_effect))
                if bool(has_effect):
                    file.write(", " + str(len(self.ids.effect_list.children)))
                    effects = []
                    for effect_button in self.ids.effect_list.children:
                        effects.append(effect_button.effect)
                    for effects_list in zip(*effects):
                        for effect_obj in effects_list:
                            file.write(", " + self.effect_to_string(effect_obj))
                else:
                    file.write(", -")
            else:
                file.write('0, -')
                file.write(", " + str(self.ids.skill_name.text))
                type = 0
                for child in self.ids.skill_type.children:
                    if child.state == 'down':
                        break
                    type += 1
                file.write(", " + str(type))
                file.write(", " + str(self.ids.skill_mana_cost.text))
                power = 0
                for child in self.ids.skill_power.children:
                    if child.state == 'down':
                        break
                    power += 1
                file.write(", " + str(power))
                element = 0
                for child in self.ids.skill_element.children:
                    if child.state == 'down':
                        break
                    element += 1
                file.write(", " + str(element))
                has_effect = 0
                has_effect_obj = self.ids.skill_has_effect
                for child in has_effect_obj.children:
                    if child.state == 'down':
                        break
                    has_effect += 1
                file.write(", " + str(has_effect))
                if bool(has_effect):
                    file.write(", " + str(len(self.ids.effect_list.children)))
                    effects = []
                    for effect_button in self.ids.effect_list.children:
                        effects.append(effect_button.effect)
                    for effects_list in zip(*effects):
                        for effect_obj in effects_list:
                            file.write(", " + self.effect_to_string(effect_obj))
                else:
                    file.write(", -")

    def effect_to_string(self, effect_obj):
        effect_str = " "
        effect_str += str(effect_obj.target_type)
        effect_str += ", " + str(effect_obj.type)
        if effect_obj.duration == -1:
            effect_str += ", -"
        else:
            effect_str += ", " + str(effect_obj.duration)
        effect_str += ", " + str(len(effect_obj.st))
        for st in effect_obj.st:
            effect_str += ", " + str(st)
        return effect_str


class Generator(App):
    def build(self):
        Builder.load_string(kv)
        return BaseWindow()


if __name__ == '__main__':
    Generator().run()