from refs import END_OPT_C, FADED_C, OPT_C, Refs, SEA_FOAM_C
from text.screens.common_functions import get_plain_size
from text.screens.screen_names import BACK, PERK_INFO
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


def add_box(row, box, separate=False, tree_index=0):
    rows = row.split('\n')
    box_rows = box.split('\n')
    string = ''
    for x in range(len(rows)):
        if separate:
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


def add_row(rows, row, trees, level):
    tree_widths = list(trees.values())
    tree_names = list(trees.keys())
    if level == 4:
        rows += '\n'
        for x in range(len(tree_widths)):
            if x == 0:
                rows += '        '
            if x == 0 or x == len(tree_widths) - 1:
                tree_width = tree_widths[x] * 16
            else:
                tree_width = tree_widths[x] * 16 + 1
            rows += tree_names[x].center(tree_width) + ' '
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


def get_screen(console, screen_data):
    console.header_callback = get_town_header
    perk_trees, perk_count = {}, 0
    display_text, _options = '', {}

    display_text += f'\n\n\tYou have {Refs.gc.get_perk_points()} Perk Points\n'

    for perk_id, perk in Refs.gc['perks'].items():
        tree, level = perk.get_tree(), perk.get_level()
        if tree not in perk_trees:
            perk_trees[tree] = {}
        if level not in perk_trees[tree]:
            perk_trees[tree][level] = []
        perk_trees[tree][level].append(perk)
        perk_count += 1

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
            for perk in tree[level_id]:
                color = None
                if Refs.gc.has_perk(perk.get_id()):
                    color = SEA_FOAM_C
                else:
                    if cost > Refs.gc.get_skill_level() and cost != 1:
                        color = FADED_C
                perk_box = wrap_in_box(perk.get_name(), perk_count, color)
                _options[str(perk_count)] = f'{PERK_INFO}:{perk.get_id()}'
                tree_row = add_box(tree_row, perk_box)
                perk_count -= 1
            tree_row = center_row(tree_row, tree_width * 16 + 1)
            level_row = add_box(level_row, tree_row, True, index)
        level_row = add_box(level_row, f'\n\n{str(cost).rjust(2)}\n\n\n')
        display_text = add_row(display_text, level_row, tree_widths, level_id)

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options['0'] = BACK
    return display_text, _options


def handle_action(console, action):
    console.set_screen(action)
