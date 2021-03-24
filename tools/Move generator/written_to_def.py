from game.character import ADVENTURER, CHARACTER_ATTACK_TYPES, GENDERS, RACES, SUPPORTER
from game.effect import COUNTER, COUNTER_TYPES, DURATION, SPECIFIC_TARGET, STAT, STATUS_EFFECT, STAT_TYPES, TYPES
from game.equipment import WEAPON_TYPES
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
        if self.element is not None and self.element != 0:
            string += ' ' + ELEMENTS[self.element]
        # string += '\n'
        for boost in self.boost:
            string += ' - ' + str(boost)
        if self.status_effect is not None:
            string += ' - ' + f'{self.status_effect}'
        if self.effect_list is not None:
            for effect in self.effect_list:
                string += ' - ' + str(effect)
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
    def __init__(self):
        self._section = None
        self._definition = None

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
        # Make sure that we have some kind of an end of a list
        # section end in a ',', next section is and/for/per
        print('Resolve', self._section)
        full_type = False
        while not full_type:
            if self._section.endswith(','):
                full_type = True
                self._section = self._section[:-1]
            if not full_type:
                section = self._section
                self.next_section(overwrite=False)
                if self._section in ['and', 'per', 'for'] or self._section[0] in ['x', '+', '-']:
                    full_type = True
                    self._section = section
                else:
                    self.next_section()
                    self._section = f'{section} {self._section}'
        if self._section in list(STAT_TYPES.values()):
            return STAT, list(STAT_TYPES.values()).index(self._section)
        elif self._section in list(COUNTER_TYPES.values()):
            return COUNTER, list(COUNTER_TYPES.values()).index(self._section)
        else:
            section = self._section
            self.next_section()
            self._section = f'{section} {self._section}'
            return self.resolve_type()

    def get_effect(self, target, supporter=False):
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
            types.append(self.resolve_type())
            self.swallow('and', True)
            if self._definition.startswith('-') or self._definition.startswith('+'):
                amount = self.get_amount()
                if supporter:
                    for type, sub_type in types:
                        effect = Effect()
                        effect.target = target
                        effect.type = type
                        effect.sub_type = sub_type
                        effect.amount = amount
                        effects.append(effect)
                    has_next = self.has_more()
                    if has_next:
                        self.swallow('and', True)
            if self._definition.startswith('for'):
                self.swallow('for')
                duration = self.get_duration()
                self.swallow('turns')
                for type, sub_type in types:
                    effect = Effect()
                    effect.target = target
                    effect.type = type
                    effect.sub_type = sub_type
                    effect.amount = amount
                    effect.duration = duration
                    effects.append(effect)
                has_next = self.has_more()
                if has_next:
                    self.swallow('and', True)
            if self._definition.startswith('per'):
                self.swallow('per turn')
                for type, sub_type in types:
                    effect = Effect()
                    effect.target = target
                    effect.type = type
                    effect.sub_type = sub_type
                    effect.amount = amount
                    effects.append(effect)
                has_next = self.has_more()
                if has_next:
                    self.swallow('and', True)
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
                has_next = self.has_more()
                if has_next:
                    self.swallow('and', True)
        return effects

    def process_move(self, move_string, support_skill=False):
        self._definition = move_string.strip()
        print('Process', self._definition)
        # move_id, self._definition = move_string.split(' - ')
        skill = Skill()

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
                skill.effect_list = self.get_effect(skill.target, supporter=support_skill)

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


move_reader = MoveReader()

file = open('implementations.txt')
data = file.read()
file.close()

enemies_data, character_data = data.split('\n#\n')

enemies = []
skills = {}
enemy_skills = {}
for enemy in enemies_data.split('\n\n'):
    name_and_element, hsmead, attack_type, moves = enemy.split('\n', 3)
    name, element_list = name_and_element.split(' - ')
    element_list = element_list.split(', ')
    if len(element_list) == 1:
        element_list.append(None)
    enemy_id = name.lower().replace(' ', '_')
    attack_type = ['Physical Attack Type', 'Magical Attack Type', 'Hybrid Attack Type'].index(attack_type[2:])
    moves = moves.split('\n')
    string = f'{enemy_id}, {name}, -, {element_list[0]}, {element_list[1]}, {attack_type}'
    enemy_skills[name] = {}
    for stat in hsmead[len('HSMEAD - '):].split(', '):
        min_stat, max_stat = stat.split('-')
        string += f', {min_stat}, {max_stat}'
    string += f', {len(moves) - 3}'
    for move in moves:
        info, move_definition = move[2:].split(' - ')
        if info.strip() == 'Counter':
            if move_definition[0] != '[':
                move_name = move_definition
                move_definition = enemy_skills[name][move_name]
                move_id = list(skills.keys()).index(f'{move_name} - {move_definition}')
            else:
                if f'Counter - {move_definition}' in skills.keys():
                    move_id = list(skills.keys()).index(f'Counter - {move_definition}')
                    enemy_skills[name]['Counter'] = move_definition
                else:
                    move_id = len(skills)
                    skills[f'Counter - {move_definition}'] = move_reader.process_move(move_definition)
                    enemy_skills[name]['Counter'] = move_definition
            string += f', {move_id}'
        elif info.strip() == 'Block':
            if move_definition == 'None':
                string += f', -'
                enemy_skills[name]['Block'] = 'None'
                continue
            else:
                if move_definition[0] != '[':
                    move_name = move_definition
                    move_definition = enemy_skills[name][move_name]
                    move_id = list(skills.keys()).index(f'{move_name} - {move_definition}')
                else:
                    if f'Block - {move_definition}' in skills.keys():
                        move_id = list(skills.keys()).index(f'Block - {move_definition}')
                        enemy_skills[name]['Block'] = move_definition
                    else:
                        move_id = len(skills)
                        skills[f'Block - {move_definition}'] = move_reader.process_move(move_definition)
                        enemy_skills[name]['Block'] = move_definition
                string += f', {move_id}'
        else:
            chance, skill_name = info.strip().split(' ', 1)
            if f'{skill_name} - {move_definition}' in skills.keys():
                move_id = list(skills.keys()).index(f'{skill_name} - {move_definition}')
                enemy_skills[name][skill_name] = move_definition
            else:
                move_id = len(skills)
                skills[f'{skill_name} - {move_definition}'] = move_reader.process_move(move_definition)
                enemy_skills[name][skill_name] = move_definition
            string += f', {move_id}, {chance}'
    enemies.append(string)

adventurers = []
adventurer_lengths = []
supporters = []
supporter_lengths = []
character_skills = {}
for character in character_data.split('\n\n'):
    info, character_type, character = character.split('\n', 2)
    if character_type == 'Adventurer':
        character_type = ADVENTURER
        string = 'A, '
        race_string, gender_string, age_string, description_string, favorite_weapons, attack_info, hmsmead, basic_move, move1, move2, move3, move_special, move_counter, move_block, recruitment_cost = character.split('\n')
    else:
        character_type = SUPPORTER
        string = 'S, '
        race_string, gender_string, age_string, description_string, hmsmead, effect_level_1, effect_level_2, effect_level_3, effect_level_4, effect_level_5, recruitment_cost = character.split('\n')

    name, display_name = info.split(' - ')
    character_id = (display_name.lower() + ' ' + name.lower().split(' ')[0]).replace(' ', '_')
    string += f'{character_id}, {name}, {display_name}, -'  # TODO Add Skels
    race = list(RACES.values()).index(race_string[len('Race: '):])
    gender = list(GENDERS.values()).index(gender_string[len('Gender: '):])
    age = int(age_string[len('Age: '):])
    string += f', {race}, {gender}, {age}'
    description = description_string[len('Description: '):]

    string += f', {hmsmead[len("HMSMEAD - "):]}'

    recruitment_item_list = recruitment_cost[len('Recruitment Cost: '):].split(', ')
    recruitment_items = {}
    for item in recruitment_item_list:
        count, item_name = item.split(' ', 1)
        recruitment_items[item_name.lower().replace(' ', '_')] = int(count)
    character_skills[name] = {}
    if character_type == ADVENTURER:
        attack_type, element = attack_info.split(' - ')
        attack_type = list(CHARACTER_ATTACK_TYPES.values()).index(attack_type)
        element = list(ELEMENTS.values()).index(element)
        string += f', {attack_type}, {element}'

        weapon_count = 0
        for weapon in favorite_weapons[len('Favorite Weapon: '):].split(', '):
            weapon_id = list(WEAPON_TYPES.values()).index(weapon)
            string += f', {weapon_id}'
            weapon_count += 1
        if weapon_count != 2:
            string += ', -'

        basic_move_def = basic_move.split(' - ')[1]
        skill_1_name, skill_1_cost, skill_1_def = move1.split(' - ')[1:]
        skill_1_mana_cost = int(skill_1_cost[:-len(' Mana')].strip())
        skill_2_name, skill_2_cost, skill_2_def = move2.split(' - ')[1:]
        skill_2_mana_cost = int(skill_2_cost[:-len(' Mana')].strip())
        skill_3_name, skill_3_cost, skill_3_def = move3.split(' - ')[1:]
        skill_3_mana_cost = int(skill_3_cost[:-len(' Mana')].strip())
        skill_1_name, skill_2_name, skill_3_name = skill_1_name.strip(), skill_2_name.strip(), skill_3_name.strip()

        special_name, special_def = move_special[len('Special Skill - '):].split(' - ')
        special_name = special_name.strip()

        counter_def = move_counter.split(' - ')[1]
        block_def = move_block.split(' - ')[1]

        skill_names = ['Basic Attack', skill_1_name, skill_2_name, skill_3_name, special_name]
        skill_defs = [basic_move_def, skill_1_def, skill_2_def, skill_3_def, special_def]
        mana_costs = [0, skill_1_mana_cost, skill_2_mana_cost, skill_3_mana_cost, 0]

        for index, skill_name in enumerate(skill_names):
            skill_def = skill_defs[index]
            if f'{skill_name} - {skill_def}' in skills.keys():
                skill_id = list(skills.keys()).index(f'{skill_name} - {skill_def}')
            else:
                skill_id = len(skills.keys())
                skills[f'{skill_name} - {skill_def}'] = move_reader.process_move(skill_def, True)
                character_skills[name][skill_name] = skill_def
            if mana_costs[index] != 0:
                string += f', {skill_id}, {mana_costs[index]}'
            else:
                string += f', {skill_id}'

        if counter_def[0] != '[':
            move_name = counter_def
            counter_def = character_skills[name][move_name]
            counter_id = list(skills.keys()).index(f'{move_name} - {counter_def}')
        else:
            if f'Counter - {counter_def}' in skills.keys():
                counter_id = list(skills.keys()).index(f'Counter - {counter_def}')
                character_skills[name]['Counter'] = counter_def
            else:
                counter_id = len(skills)
                skills[f'Counter - {counter_def}'] = move_reader.process_move(counter_def)
                character_skills[name]['Counter'] = counter_def

        if block_def == 'None':
            block_id = None
            character_skills[name]['Block'] = 'None'
        else:
            if block_def[0] != '[':
                move_name = block_def
                block_def = character_skills[name][move_name]
                block_id = list(skills.keys()).index(f'{move_name} - {block_def}')
            else:
                if f'Block - {block_def}' in skills.keys():
                    block_id = list(skills.keys()).index(f'Block - {block_def}')
                    character_skills[name]['Block'] = block_def
                else:
                    block_id = len(skills)
                    skills[f'Block - {block_def}'] = move_reader.process_move(block_def)
                    character_skills[name]['Block'] = block_def

        # TODO Add Combo skills
        if block_id is None:
            block_id = '-'
        string += f', {counter_id}, {block_id}, 0'
    else:
        effect_name, effect_level_1_def = effect_level_1[len('Effect Level 1 - '):].split(' - ')
        effect_level_2_def = effect_level_2.split(' - ')[1]
        effect_level_3_def = effect_level_3.split(' - ')[1]
        effect_level_4_def = effect_level_4.split(' - ')[1]
        effect_level_5_def = effect_level_5.split(' - ')[1]

        effect_names = [f'{effect_name} Level {x + 1}' for x in range(5)]
        effect_defs = [effect_level_1_def, effect_level_2_def, effect_level_3_def, effect_level_4_def, effect_level_5_def]

        for index, effect_name in enumerate(effect_names):
            effect_def = effect_defs[index]
            if f'{effect_name} - {effect_def}' in skills.keys():
                effect_id = list(skills.keys()).index(f'{effect_name} - {effect_def}')
            else:
                effect_id = len(skills.keys())
                skills[f'{effect_name} - {effect_def}'] = move_reader.process_move(effect_def, True)
                character_skills[name][effect_name] = effect_def
            string += f', {effect_id}'

    for recruitment_item, count in recruitment_items.items():
        string += f', {recruitment_item}#{count}'
    string += f', {len(recruitment_items.keys())}'
    string += f', {description}'
    if character_type == ADVENTURER:
        adventurers.append(string)
        adventurer_lengths.append(32 + 0 + len(recruitment_items.keys()))
    else:
        supporters.append(string)
        supporter_lengths.append(22 + 0 + len(recruitment_items.keys()))

skills_lines = []
skill_lengths = []
for index, (skill_name, skill) in enumerate(skills.items()):
    skill_name, skill_def = skill_name.split(' - ', 1)
    if skill_name in ['Basic Attack', 'Counter', 'Block']:
        skill_name = skill_def
    string = f'{index}, {skill_name}, -, '
    string += f'{skill.type}, {skill.target}'
    if skill.type == ATTACK:
        string += f', {skill.attack_speed}'
        string += f', {skill.attack_power}'
        string += f', {skill.attack_type}'
        string += f', {skill.element}'
    elif skill.type == HEAL:
        string += f', {skill.attack_speed}'
        string += f', {skill.attack_power}'
    elif skill.type == AILMENT_CURE:
        string += f', {skill.attack_speed}'
    if skill.boost is not None:
        string += f', {len(skill.boost)}'
        for boost in skill.boost:
            string += f', {boost.type}'
            string += f', {boost.stat_type}'
    else:
        string += f', 0'
    if skill.effect_list is not None:
        string += f', {len(skill.effect_list)}'
        for effect in skill.effect_list:
            string += f', {skill.type}'
            if effect.type == STAT:
                string += f', {effect.sub_type}'
                string += f', {effect.target}'
                string += f', {effect.amount}'
                string += f', {effect.duration}'
            elif effect.type == COUNTER:
                string += f', {effect.sub_type}'
                string += f', {effect.target}'
                string += f', {effect.duration}'
            elif effect.type == DURATION:
                string += f', {effect.sub_type}'
                string += f', {effect.target}'
                string += f', {effect.duration}'
            elif effect.type == SPECIFIC_TARGET:
                error('AAAAAH')
            elif effect.type == STATUS_EFFECT:
                string += f', {effect.type}'
                string += f', {effect.level}'
    else:
        string += ', 0'
    skills_lines.append(string)
    skill_lengths.append(string.count(',') + 1)

skill_cols = [[] for x in range(max(skill_lengths))]
for skill in skills_lines:
    for index, col in enumerate(skill.split(', ')):
        skill_cols[index].append(len(col))

for skill_index, skill_line in enumerate(skills_lines):
    for index, col in enumerate(skill_line.split(', ')):
        print(col.ljust(max(skill_cols[index])), end='')
        if index != skill_lengths[skill_index]:
            print(', ', end='')
    print()

enemy_cols = [[] for x in range(enemies[0].count(',') + 1)]
for enemy in enemies:
    for index, col in enumerate(enemy.split(', ')):
        enemy_cols[index].append(len(col))

for enemy in enemies:
    for index, col in enumerate(enemy.split(', ')):
        print(col.ljust(max(enemy_cols[index])), end='')
        if index != 26:
            print(', ', end='')
    print()

adventurer_cols = [[] for x in range(max(adventurer_lengths))]
supporter_cols = [[] for x in range(max(adventurer_lengths))]

for char_index, character in enumerate(adventurers):
    for index, col in enumerate(character.split(', ', adventurer_lengths[char_index] - 1)):
        adventurer_cols[index].append(len(col))

for char_index, character in enumerate(supporters):
    for index, col in enumerate(character.split(', ', supporter_lengths[char_index] - 1)):
        supporter_cols[index].append(len(col))

for char_index, character in enumerate(adventurers):
    for index, col in enumerate(character.split(', ', adventurer_lengths[char_index] - 1)[:-2]):
        print(col.ljust(max(adventurer_cols[index])), end='')
        if index != adventurer_lengths[char_index] - 1:
            print(', ', end='')
    for col in range(adventurer_lengths[char_index], max(adventurer_lengths)):
        print(''.ljust(max(adventurer_cols[index]) + 1), end='')
    for index, col in enumerate(character.split(', ', adventurer_lengths[char_index] - 1)[-2:]):
        print(col, end='')
        if index != 1:
            print(', ', end='')
    print()

for char_index, character in enumerate(supporters):
    for index, col in enumerate(character.split(', ', supporter_lengths[char_index] - 1)[:-2]):
        print(col.ljust(max(supporter_cols[index])), end='')
        if index != supporter_lengths[char_index] - 1:
            print(', ', end='')
    for col in range(supporter_lengths[char_index], max(supporter_lengths)):
        print(''.ljust(max(supporter_cols[index]) + 1), end='')
    for index, col in enumerate(character.split(', ', supporter_lengths[char_index] - 1)[-2:]):
        print(col, end='')
        if index != 1:
            print(', ', end='')
    print()

file = open('moves_written.txt', 'r', encoding='utf-8')
data = file.read()
file.close()
