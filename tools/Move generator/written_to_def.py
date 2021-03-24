from game.effect import COUNTER, COUNTER_TYPES, STAT, STAT_TYPES, TYPES
from game.skill import AILMENT_CURE, ALLIES, ALLY, ATTACK, ATTACK_POWERS, ATTACK_SPEEDS, ATTACK_TYPES, BOOST_TYPES, CAUSE_EFFECT, ELEMENTS, FOE, FOES, HEAL, SELF, SKILL_TYPES, TARGETS
from game.status_effect import LEVELS, NORMAL, STATUS_EFFECTS


def error(msg):
    print(msg)
    quit(1)


def get_list(section):
    items = []
    if ',' in section:
        items = section.split(', ')
        if ' and ' in items[-1]:
            items[-1] = items[5:]
    elif ' and ' in section:
        items = section.split(' and ')
    else:
        items = [section]
    return items


class Skill:
    def __init__(self):
        self.move_id = -1
        self.type = None
        self.target = None
        self.attack_speed = None
        self.attack_power = None
        self.attack_type = None
        self.element = 0
        self.boost = []
        self.status_effect = None
        self.effect_list = []

    def __str__(self):
        string = f'{SKILL_TYPES[self.type]} [{TARGETS[self.target]}]'
        if self.attack_speed is not None:
            string += ' ' + ATTACK_SPEEDS[self.attack_speed]
        if self.attack_power is not None:
            string += ' ' + ATTACK_POWERS[self.attack_power]
        if self.attack_type is not None:
            string += ' ' + ATTACK_TYPES[self.attack_type] + ' Atk.'
        if self.element is not None:
            string += ' ' + ELEMENTS[self.element]
        string += '\n'
        for boost in self.boost:
            string += str(boost) + '\n'
        if self.status_effect is not None:
            string += f'{self.status_effect}\n'
        for effect in self.effect_list:
            string += str(effect) + '\n'
        return string


class Boost:
    def __init__(self):
        self.type = None
        self.stat_type = None

    def __str__(self):
        return f'<{BOOST_TYPES[self.type]} {STAT_TYPES[self.stat_type]}>'


class StatusEffect:
    def __init__(self):
        self.amount = None
        self.level = None
        self.type = None

    def __str__(self):
        return f'<StatusEffect {self.amount}% {LEVELS[self.level if self.level else 1]} {STATUS_EFFECTS[self.type]}>'


class Effect:
    def __init__(self):
        self.target = None
        self.type = None
        self.sub_type = None
        self.amount = None
        self.duration = None

    def __str__(self):
        return f'<Effect [{TARGETS[self.target]}] {TYPES[self.type][self.sub_type]} {self.amount if self.amount else ""} {self.duration}>'


class MoveReader:
    def __init__(self, moves):
        self._section = None
        self._definition = None

        for move in moves:
            skill = self._process_move(move)
            print(skill)

    def next_section(self, delimiter=' ', overwrite=True):
        if delimiter not in self._definition:
            self._section = self._definition
            if overwrite:
                self._definition = ''
            return
        index = self._definition.index(delimiter)
        self._section = self._definition[:index].strip()
        if overwrite:
            self._definition = self._definition[index + len(delimiter):].strip()

    def swallow(self, string, optional=False):
        if optional:
            if self._definition.startswith(string):
                self._definition = self._definition[len(string):].strip()
                return True
            return False
        self._definition = self._definition[len(string):].strip()
        return True

    def has_more(self):
        return self._definition != ''

    def get_list(self):
        list = []
        has_next = True
        while has_next:
            index = self._definition.index(' ')
            section = self._definition[:index].strip()
            list.append(section)
            self._definition = self._definition[index:].strip()
            has_next = section[-1] == ','
            if not has_next:
                if self._definition.startswith('and'):
                    has_next = True
                    self._definition = self._definition[len('and'):].strip()
        return list

    def get_target(self, optional=False):
        self.next_section(overwrite=not optional)
        if optional and self._section[1:-1] not in TARGETS.values():
            return None
        target = list(TARGETS.values()).index(self._section[1:-1])
        if optional:
            self.next_section()
        return target

    def get_attack_speed(self, optional=False):
        self.next_section(overwrite=not optional)
        if optional and self._section not in ATTACK_SPEEDS.values():
            return None
        attack_speed = list(ATTACK_SPEEDS.values()).index(self._section)
        if optional:
            self.next_section()
        return attack_speed

    def get_attack_power(self, optional=False):
        self.next_section(overwrite=not optional)
        if optional and self._section not in ATTACK_POWERS.values():
            return None
        attack_power = list(ATTACK_POWERS.values()).index(self._section)
        if optional:
            self.next_section()
        return attack_power

    def get_element(self, optional=False):
        self.next_section(overwrite=not optional)
        if optional and self._section not in ELEMENTS.values():
            return 0
        element = list(ELEMENTS.values()).index(self._section)
        if optional:
            self.next_section()
        return element

    def get_attack_type(self, optional=False):
        self.next_section(overwrite=not optional)
        if optional and self._section not in ATTACK_TYPES.values():
            return None
        attack_type = list(ATTACK_TYPES.values()).index(self._section)
        if optional:
            self.next_section()
        return attack_type

    def get_boost(self, optional=False):
        self.next_section(overwrite=not optional)
        if optional and self._section not in BOOST_TYPES.values():
            return None
        boost_type = list(BOOST_TYPES.values()).index(self._section)
        if optional:
            self.next_section()
        return boost_type

    def get_amount(self, optional=False):
        self.next_section(overwrite=not optional)
        amount = int(self._section[:-1])
        if optional:
            self.next_section()
        return amount

    def get_duration(self, optional=False):
        self.next_section(overwrite=not optional)
        duration = int(self._section)
        if optional:
            self.next_section()
        return duration

    def get_level(self, optional=False):
        self.next_section(overwrite=not optional)
        if optional and self._section not in LEVELS.values():
            return None
        level = list(LEVELS.values()).index(self._section)
        if optional:
            self.next_section()
        return level

    def get_status_effect_type(self, optional=False):
        self.next_section(overwrite=not optional)
        if optional and self._section not in STATUS_EFFECTS.values():
            return None
        status_effect_type = list(STATUS_EFFECTS.values()).index(self._section)
        if optional:
            self.next_section()
        return status_effect_type

    def resolve_type(self):
        if self._section in list(STAT_TYPES.values()):
            return STAT, list(STAT_TYPES.values()).index(self._section)
        elif self._section in list(COUNTER_TYPES.values()):
            return COUNTER, list(COUNTER_TYPES.values()).index(self._section)
        else:
            section = self._section
            self.next_section()
            self._section = f'{section} {self._section}'
            return self.resolve_type()

    def get_effect(self, target):
        if not self.has_more():
            return

        effects = []
        types = []
        amount = -1

        has_next = True
        while has_next:
            self.next_section(overwrite=False)
            if '%' in self._section:
                amount = self.get_amount()
            self.next_section()
            if self._section.endswith(','):
                self._section = self._section[:-1]
            self.swallow('and', True)
            types.append(self.resolve_type())
            if self._definition.startswith('-') or self._definition.startswith('+'):
                amount = self.get_amount()
            if self._definition.startswith('for'):
                self.swallow('for')
                duration = self.get_duration()
                for type, sub_type in types:
                    effect = Effect()
                    effect.target = target
                    effect.type = type
                    effect.sub_type = sub_type
                    effect.amount = amount
                    effect.duration = duration
                    effects.append(effect)
                self.swallow('turns')
                return effects
            if self._definition.startswith('x'):
                self.swallow('x')
                count = self.get_duration()
                for type, sub_type in types:
                    effect = Effect()
                    effect.target = target
                    effect.type = type
                    effect.sub_type = sub_type
                    effect.amount = amount
                    effect.duration = count
                    effects.append(effect)
                return effects

    def _process_move(self, move_string):
        move_id, self._definition = move_string.split(' - ')
        skill = Skill()

        skill.move_id = int(move_id.strip())

        skill.target = self.get_target()

        skill.attack_speed = self.get_attack_speed(True)
        skill.attack_power = self.get_attack_power(True)
        if self.swallow('Heal', True):
            skill.type = HEAL
        elif self.swallow('Ailment Cure', True):
            skill.type = AILMENT_CURE
        else:
            skill.element = self.get_element(True)
            skill.attack_type = self.get_attack_type(True)
            if self.swallow('Atk.', True):
                skill.type = ATTACK
            else:
                skill.type = CAUSE_EFFECT
                skill.effect_list = self.get_effect(skill.target)

        if self.swallow('with', True):
            if self.swallow('temp.', True):
                boost_list = []
                type_list = self.get_list()
                boost_type = self.get_boost()
                for type in type_list:
                    boost = Boost()
                    boost.stat_type = list(STAT_TYPES.values()).index(type)
                    boost.type = boost_type
                    boost_list.append(boost)
                skill.boost = boost_list
            else:
                status_effect = StatusEffect()
                status_effect.amount = self.get_amount()
                status_effect.level = self.get_level(True)
                status_effect.type = self.get_status_effect_type()
                skill.status_effect = status_effect
        if self.swallow('and', True):
            effect_target = self.get_target(True)
            if effect_target is None:
                effect_target = skill.target
            skill.effect_list = self.get_effect(effect_target)

        if self.has_more():
            print(self._definition, 'Left Over')
            quit(1)
        return skill


file = open('moves_written.txt', 'r', encoding='utf-8')
data = file.read()
file.close()

moves = data.split('\n')
MoveReader(moves)