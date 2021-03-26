"""
Crafting Perk Tree
Level 1 - Cost 1 Perk Point
- Daedalus' Protégé
  - Craft basic items
- Basic Tailor
  - Process Soft Materials 2.0 and below
- Apprentice Blacksmith
  - Process Hard Materials and craft alloys with hardness 3.0 or below

Level 2 - Cost 3 Perk Points
- The beginning of Enigma
  - Requires Daedalus' Protégé
  - Craft advanced items
- Reputable Tailor
  - Requires Basic Tailor
  - Process Soft Materials 5.5 and below
  - Craft Soft Material based equipment using soft materials 5.5 and below
- Skilled Blacksmith
  - Requires Basic Blacksmith
  - Process Hard Materials and craft alloys with hardness 8.0 and below
  - Craft Hard Material based equipment with access to hard materials 8.0 and below

Level 3 - Cost 7 Perk Points
- The Truth to Enigma
  - Requires The beginning of Enigma
  - Craft any items
- Famous Tailor
  - Requires Reputable Tailor
  - Process Soft Materials 8.75 and below
  - Craft Soft Material based equipment using soft materials 8.75 and below
  - Sold Soft Material based equipment and processed soft materials sell for 20% more
- Famous Blacksmith
  - Requires Skilled Blacksmith
  - Process Hard Materials and craft alloys with hardness 10.5 and below
  - Craft Hard Material based equipment with access to hard materials 10.5 and below
  - Sold Hard Material based equipment and processed hard materials sell for 20% more

Level 4 - Cost 15 Perk Points
- Master Tailor
  - Requires Famous Tailor
  - Process Any Soft Materials
  - Craft Soft Material based equipment using any soft materials
  - Sold Soft Material based equipment and processed soft materials sell for 50% more (Overwrites Famous Tailor)
- Master Blacksmith
  - Requires Famous Tailor
  - Process Hard Materials and craft alloys with any hardness
  - Craft Hard Material based equipment using any hard materials
  - Sold Hard Material based equipment and processed hard materials sell for 50% more (Overwrites Famous Blacksmith)
- Insider Information
  - Requires Famous Tailor, Famous Blacksmith
  - Decrease Price of materials by 30%

Information Perk Tree
Level 1 - Cost 1 Perk Point
- Mapping
  - Create basic maps in the dungeon

Level 2 - Cost 3 Perk Points
- Trial Argo
  - Increase Recruitment amount by 30%
  - Increase chance of successful information by 30%
- A Miners bearings
  - Requries Mapping
  - Recognize resource nodes twice as fast - Implemented
- Hunter
  - Requires Mapping
  -Recognize monster nodes twice as fast - Implemented
- Extended Awareness
  - Requires Mapping
  - Increase mapping radius by 1

Level 3 - Cost 7 Perk Points
- Argo
  - Requires Trial Argo
  - Increase chance of successful perk point by 30%
  - Decrease Recruitment Party cost by 30%
- Increased Extended Awareness
  - Requires Extended Awareness
  - Increase mapping radius by 3 (Overwrites Extended Awareness)

Level 4 - Cost 15 Perk Points
- Sixth Sense
  - Requires A Miners Bearings, Hunter, Increased Extended Awareness
  - Increase mapping radius by 5 (Overwrites Increased Extended Awareness)
  - Mapping Radius affects all surrounding area
- The Rat
  - Requires Argo
  - Decrease Adventurer Recruitment Cost by 50%
  - Increase chance of rare adventurer by a single bracket

Alchemist Perk Tree
Level 1 - Cost 1 Perk Point
- Fledgling Alchemist
  - Unlock basic potions
  - Experiment with materials Grade G and below

Level 2 - Cost 3 Perk Points
- Reputable Alchemist
  - Requires Fledgling Alchemist
  - Unlock advanced potions
  - Experiment with materials Grade D and below
- Researcher
  - Requires Fledgling Alchemist
  - Increase chance to unlocking ingredient attributes by 30%

Level 3 - Cost 7 Perk Points
- True Efficiency
  - Requires Reputable Alchemist
  - Decrease material requirements by 30%
  - Increase yield by 30%
- Stanford Grad
  - Requires Researcher
  - Increase chance to unlocking ingredient attributes to one use

Level 4 - Cost 15 Perk Points
- The Chemist
  - Requires Reputable Alchemist
  - Craft all potions
- Harvard Grad
  - Requires Stanford Grad
  - Increase sale price of your potions by 40%
  - Decrease potion and ingredient prices by 40%
"""

from refs import END_OPT_C, FADED_C, OPT_C, Refs, SEA_FOAM_C
from text.screens.dungeon_battle import get_plain_size
from text.screens.town import get_town_header


def wrap_in_box(string, option_index, color):
    if color is None:
        new_string = '┌'
    else:
        new_string = f'{color}┌'
    for _ in range(13):
        new_string += '─'
    if color is None:
        new_string += f'┐\n'
    else:
        new_string += f'┐{END_OPT_C}\n'

    string_rows = []
    while len(string) > 0:
        if len(string) > 11:
            index = string.rindex(' ', 0, 12)
            string_rows.append(string[:index].center(11))
            string = string[index + 1:]
        else:
            string_rows.append(string.center(11))
            string = ''

    if len(string_rows) == 2:
        string_rows.append(''.center(11))
    if len(string_rows) == 1:
        string_rows.insert(0, ''.center(11))
        string_rows.append(''.center(11))

    for row in string_rows:
        if color is None:
            new_string += f'│ {row} │\n'
        else:
            new_string += f'{color}│ {row} │{END_OPT_C}\n'
    if color is None:
        new_string += f'│ {OPT_C}{str(option_index).center(11)}{END_OPT_C} │\n└'
    else:
        new_string += f'{color}│{END_OPT_C} {OPT_C}{str(option_index).center(11)}{END_OPT_C} {color}│{END_OPT_C}\n{color}└'
    for _ in range(13):
        new_string += '─'
    if color is None:
        return new_string + '┘'
    else:
        return new_string + f'┘{END_OPT_C}'


def add_box(row, box, seperate=False, tree_index=0):
    rows = row.split('\n')
    box_rows = box.split('\n')
    string = ''
    for x in range(len(rows)):
        if seperate:
            if tree_index == 0:
                string += rows[x] + box_rows[x] + '\n'
            elif rows[x] == '':
                string += box_rows[x] + '\n'
            else:
                string += rows[x] + '│' + box_rows[x] + '\n'
        else:
            if rows[x] == '':
                string += box_rows[x] + '\n'
            else:
                string += rows[x] + ' ' + box_rows[x] + '\n'
    return string[:-1]


def center_row(row, length):
    rows = row.split('\n')
    string = ''
    for row in rows:
        row_length = get_plain_size(row)
        string += row.center(len(row) + (length - row_length)) + '\n'
    return string[:-1]


def add_row(rows, row, tree_widths, level):
    if level == 4:
        rows += '\n'
        for x in range(len(tree_widths)):
            if x == 0:
                rows += '        '
            if x == 0 or x == len(tree_widths) - 1:
                tree_width = tree_widths[x] * 16
            else:
                tree_width = tree_widths[x] * 16 + 1
            rows += ['Crafting', 'Information', 'Alchemy'][x].center(tree_width) + ' '
        return rows + '\n' + row
    rows += '\n'
    for x in range(len(tree_widths)):
        if x == 0:
            rows += '        '
        if x == 0 or x == len(tree_widths) - 1:
            tree_width = tree_widths[x] * 16
        else:
            tree_width = tree_widths[x] * 16 + 1
        for _ in range(tree_width):
            rows += '─'
        rows += '┼'
    return rows[:-1] + '\n' + row


def skill_tree_main(console):
    perk_trees = {}
    perk_count = 0
    for perk_id, perk in Refs.gc['perks'].items():
        tree, level = perk.get_tree(), perk.get_level()
        if tree not in perk_trees:
            perk_trees[tree] = {}
        if level not in perk_trees[tree]:
            perk_trees[tree][level] = []
        perk_trees[tree][level].append(perk)
        perk_count += 1
    display_text, _options = '', {}

    console.header_callback = get_town_header
    display_text += f'\n\n\tYou have {Refs.gc.get_perk_points()} Perk Points\n'

    tree_widths = {}
    for tree_name, tree in perk_trees.items():
        width = 0
        for level_id, perks in tree.items():
            width = max(width, len(perks))
        tree_widths[tree_name] = width

    # Display all the trees
    for level_id in [4, 3, 2, 1]:
        cost = {4: 105, 3: 21, 2: 3, 1: 1}[level_id]
        level_row = f'       \n       \n    {str(cost).rjust(3)}\n       \n       \n       '
        for index, (tree_name, tree) in enumerate(perk_trees.items()):
            tree_row = '\n\n\n\n\n'
            tree_width = tree_widths[tree_name]
            # TODO Add tree names to top of trees
            for perk in tree[level_id]:
                # TODO Wrap Perk box in color based on whether or not it is unlocked
                color = None
                if Refs.gc.has_perk(perk.get_id()):
                    color = SEA_FOAM_C
                else:
                    if cost > Refs.gc.get_skill_level() and cost != 1:
                        color = FADED_C
                perk_box = wrap_in_box(perk.get_name(), perk_count, color)
                _options[str(perk_count)] = f'perk_info_{perk.get_id()}'
                tree_row = add_box(tree_row, perk_box)
                perk_count -= 1
            tree_row = center_row(tree_row, tree_width * 16 + 1)
            level_row = add_box(level_row, tree_row, True, index)
            # TODO Add perk cost to beginning and end of each row
        level_row = add_box(level_row, f'\n\n{str(cost).rjust(2)}\n\n\n')
        display_text = add_row(display_text, level_row, list(tree_widths.values()), level_id)

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = 'back'
    return display_text, _options


def perk_info(console):
    perk_id = console.get_current_screen()[len('perk_info_'):]
    perk = Refs.gc['perks'][perk_id]

    perk_cost = perk.get_cost()

    console.header_callback = get_town_header
    _options = {}

    display_text = f'\n\n\t{perk.get_name()} - {perk.get_tree().title()}'
    display_text += f'\n\t\t' + perk.get_description().replace('\n', '\n\t\t')
    display_text += f'\n\n\t\tCosts {perk_cost} Perk Points to unlock\n'

    perk_points = Refs.gc.get_perk_points()
    meets_requirements = True
    for requirement in perk.get_requirements():
        if requirement == 'none':
            continue
        meets_requirements &= Refs.gc.has_perk(requirement)

    if perk_points >= perk_cost and (Refs.gc.get_skill_level() > perk_cost or perk_cost == 1) and meets_requirements:
        display_text += f'\n\t{OPT_C}1:{END_OPT_C} Bestow Perk Upon Adventurer'
        _options['1'] = f'perk_bestow_{perk_id}'
    else:
        display_text += f'\n\t[s]{OPT_C}2:{END_OPT_C} Bestow Perk Upon Adventurer[/s]'

    display_text += f'\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = 'back'
    return display_text, _options


def perk_bestow(console):
    perk_id = console.get_current_screen()[len('perk_bestow_'):]
    perk = Refs.gc['perks'][perk_id]

    # A perk can only be bestowed on an adventurer who has the required perks
    console.header_callback = get_town_header
    _options = {}
    display_text = f'\n\n\t{perk.get_name()} - {perk.get_tree().title()} - Level {perk.get_level()}'

    display_text += '\n\n\tEligible Adventurers:'
    characters = list(Refs.gc.get_obtained_characters(False))

    valid_characters = []
    for character in characters:
        meets_requirements = not character.has_perk(perk_id)

        for requirement in perk.get_requirements():
            if requirement == 'none':
                continue
            meets_requirements &= character.has_perk(requirement)

        for char_perk_id in character.get_perks():
            print(Refs.gc['perks'][char_perk_id].get_tree(), perk.get_tree())
            meets_requirements &= Refs.gc['perks'][char_perk_id].get_tree() == perk.get_tree()

        if meets_requirements:
            valid_characters.append(character)

    if len(valid_characters) == 0:
        display_text += f'\n\tNo Eligible Adventurers.'

    for index, character in enumerate(valid_characters):
        display_text += f'\n\t{OPT_C}{index + 1}:{END_OPT_C} {character.get_display_name()} {character.get_name()}'
        _options[str(index + 1)] = f'perk_bestow_{perk_id}#{character.get_id()}'

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = 'back'
    return display_text, _options
