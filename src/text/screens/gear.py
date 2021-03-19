def gear_main(console):
    display_text, _options = '', {}

    name = 'Sohpie Nicholson'
    equipment = ['Weapon', 'Off-Hand Weapon', 'Necklace', 'Ring', 'Helmet', 'Chest', 'Boots', 'Gloves', 'Grieves', 'Vambraces']

    character = '│' + name.center(16) + '│\n'
    for item in equipment:
        character += '│' + item.center(16) + '│\n'
        string = '│ ['
        for index in range(16-4):
            string += '='
        string += '] │\n'
        character += string

    gear_rows = character.split('\n')
    for x in range(len(gear_rows)):
        display_text += '\t' + gear_rows[x][:-1] + gear_rows[x][:-1] + gear_rows[x][:-1] + gear_rows[x][:-1] + gear_rows[x][:-1] + gear_rows[x][:-1] + gear_rows[x][:-1] + gear_rows[x][:-1] + gear_rows[x][:-1] + gear_rows[x] + '\n'
    display_text += '\n'
    return display_text, _options
