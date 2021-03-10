from game.skill import ATTACK_TYPES, ATTACK_TYPE_INDEX_TO_STRING, ELEMENTS, ELEMENT_INDEX_TO_STRING, MODIFIERS, MOD_INDEX_TO_STRING, SPEEDS, SPEED_INDEX_TO_STRING, TARGET_INDEX_TO_STRING

moves = []
move = ['', '', '', '']
index = 0

# DEF_TYPE, skill_id, skill_name, animation_id, attack_type, target_type, modifier, speed, element, effect_array_length, effect_array

for attack_type in ATTACK_TYPES:
    move[0] = ATTACK_TYPE_INDEX_TO_STRING[attack_type]
    for target_type in [0, 2]:
        move[1] = TARGET_INDEX_TO_STRING[target_type]
        for modifier in MODIFIERS:
            move[2] = MOD_INDEX_TO_STRING[modifier]
            for speed in SPEEDS:
                move[3] = SPEED_INDEX_TO_STRING[speed]
                for element in ELEMENTS:
                    if speed != 1:
                        if element == 0:
                            name = f'[{move[1]}] {move[3]} {move[2]} {move[0]}'
                        else:
                            name = f'[{move[1]}] {move[3]} {move[2]} {ELEMENT_INDEX_TO_STRING[element]} {move[0]}'
                    else:
                        if element == 0:
                            name = f'[{move[1]}] {move[2]} {move[0]}'
                        else:
                            name = f'[{move[1]}] {move[2]} {ELEMENT_INDEX_TO_STRING[element]} {move[0]}'
                    moves.append(['0', f'{index}', name, 'attack', f'{attack_type}', f'{target_type}', f'{modifier}', f'{speed}', f'{element}', f'{0}', '0', '-'])
                    index += 1

paddings = [0 for _ in range(12)]
for x in range(12):
    for move in moves:
        if len(move[x]) > paddings[x]:
            paddings[x] = len(move[x])

string = ''
for move in moves:
    for x in range(12):
        string += move[x].ljust(paddings[x])
        if x != 11:
            string += ', '
    string += '\n'
print(string)
