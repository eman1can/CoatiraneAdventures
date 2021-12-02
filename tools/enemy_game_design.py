enemies = []
with open('Item Config Generator/implemented_monster_list.txt', 'r') as file:
    enemies = file.read().split('\n\n')

for enemy_chunk in enemies:
    enemy = {}
    info_lines = enemy_chunk.split('\n')
    enemy['name'] = info_lines[0]
    enemy['id'] = info_lines[0].lower().replace(' ', '_')
    enemy['skel_id'] = info_lines[1][len('Skeleton Number: '):]
    enemy['floors'] = [int(x.strip()) for x in info_lines[2][len('Found on Floors: '):].split(', ')]
    enemy['description'] = info_lines[3]
    elements = info_lines[4][len('Type: '):].split(', ')
    enemy['element'] = elements[0]
    if len(elements) == 1:
        enemy['sub_element'] = None
    else:
        enemy['sub_element'] = elements[1]
