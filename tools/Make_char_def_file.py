from os import listdir
from os.path import isfile, join, isdir
import random

"""
Character Definition File generator. Will update later to include "classes"
Currently finds all res folders in the given paths and assigns random values in the def file.
Uses a names file to assign full Display Names
Must set config strings to work properly
"""

if __name__ == '__main__':
    # Configuration Settings

    res_path = "C:/Users/ethan/PycharmProjects/CoatiraneAdventures/tools/"
    names_path = "C:/Users/ethan/PycharmProjects/CoatiraneAdventures/tools/names.txt"
    output_path = "C:/Users/ethan/PycharmProjects/CoatiraneAdventures/tools/char_def.txt"

    # End Configuration Settings

    # Methods
    def get_name(id_string):
        tokens = id_string.split('_')
        display = ""
        full = ""
        if tokens[-2] == 'and':
            full = tokens[-3].capitalize() + " & " + tokens[-1].capitalize()
            for token in tokens[:-3]:
                if display != "":
                    display += ' '
                display += token.capitalize()
        else:
            for token in tokens[:-1]:
                if display != "":
                    display += ' '
                display += token.capitalize()
            for name_guess in names:
                if name_guess.startswith(tokens[-1].capitalize()):
                    full = name_guess
                    break
        return display, full

    #

    # Find ID values
    adventurers = []
    file = open(res_path + "/adventurers.txt", "r")
    for id in file:
        adventurers.append(id[:-1])
    file.close()
    supporters = []
    file = open(res_path + "/supporters.txt", "r")
    for id in file:
        supporters.append(id[:-1])
    file.close()
    # dir_list_s = [o for o in listdir(res_path + "/supporters") if isdir(join(res_path + "/supporters", o))]
    # dir_list_a = [o for o in listdir(res_path + "/adventurers") if isdir(join(res_path + "/adventurers", o))]

    # Find Names
    names = []
    file = open(names_path, "r")
    for name in file:
        names.append(name[:-1])
    file.close()

    max_lengths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    file_array = []
    # Type, Type, health, mana, strength, magic, endurance, dexterity, agility, Full Name, Display Name, ID, Moves
    for name in adventurers:
        line = []
        print("Adding ", name, "To the File as an Adventurer")
        line.append('A')
        index = 0
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        t_type = random.randint(0, 4) # 0:Magical, 1:Physical 2:Balanced, 3:Defensive, 4:Healing
        print("Is of type: ", t_type)
        line.append(str(t_type))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        element = random.randint(0, 6)
        print("Is of element: ", element)
        line.append(str(element))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        health_base = random.randint(80, 150)
        print("Has health: ", health_base)
        line.append(str(health_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        mana_base = random.randint(20, 60)
        print("Has mana: ", mana_base)
        line.append(str(mana_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        strength_base = random.randint(2, 20)
        print("Has strength: ", strength_base)
        line.append(str(strength_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        magic_base = random.randint(2, 20)
        print("Has magic: ", magic_base)
        line.append(str(magic_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        endurance_base = random.randint(1, 15)
        print("Has endurance: ", endurance_base)
        line.append(str(endurance_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        dexterity_base = random.randint(1, 15)
        print("Has dexterity: ", dexterity_base)
        line.append(str(dexterity_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        agility_base = random.randint(1, 15)
        print("Has agility: ", agility_base)
        line.append(str(agility_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        id_name, full_name = get_name(name)

        print("Full Name: ", full_name)
        line.append(full_name)
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        print("Id: ", id_name)
        line.append(id_name)
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        print("File Id: ", name)
        line.append(name)
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        print('Basic Moves: Mid P.Attack,Fiendfyre,Rapture,Drill,Lil Rafaga')
        line.append('Mid P.Attack,Fiendfyre,Rapture,Drill,Lil Rafaga')
        file_array.append(line)
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

    for name in supporters:
        line = []
        print("Adding ", name, "To the File as an Supporter")
        line.append('S')
        index = 0
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        t_type = random.randint(0, 4) # 0:Magical, 1:Physical 2:Balanced, 3:Defensive, 4:Healing
        print("Is of type: ", t_type)
        line.append(str(t_type))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        element = random.randint(0, 6)
        print("Is of element: ", element)
        line.append(str(element))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        health_base = random.randint(80, 150)
        print("Has health: ", health_base)
        line.append(str(health_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        mana_base = random.randint(20, 60)
        print("Has mana: ", mana_base)
        line.append(str(mana_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        strength_base = random.randint(2, 20)
        print("Has strength: ", strength_base)
        line.append(str(strength_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        magic_base = random.randint(2, 20)
        print("Has magic: ", magic_base)
        line.append(str(magic_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        endurance_base = random.randint(1, 15)
        print("Has endurance: ", endurance_base)
        line.append(str(endurance_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        dexterity_base = random.randint(1, 15)
        print("Has dexterity: ", dexterity_base)
        line.append(str(dexterity_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        agility_base = random.randint(1, 15)
        print("Has agility: ", agility_base)
        line.append(str(agility_base))
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        id_name, full_name = get_name(name)

        print("Full Name: ", full_name)
        line.append(full_name)
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        print("Id: ", id_name)
        line.append(id_name)
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        print("File Id: ", name)
        line.append(name)
        index += 1
        if len(line[index]) > max_lengths[index]:
            max_lengths[index] = len(line[index])

        file_array.append(line)

    file = open(output_path, "w+")

    for line in file_array:
        index = 0
        for item in line:
            max_length = max_lengths[index]
            spaces = max_length - len(item)

            file.write(item)
            for space in range(0, spaces):
                file.write(' ')
            if item is not line[-1]:
                file.write(', ')
            else:
                file.write('\n')
            index += 1
    file.close()
    print("Finished Writing config file!")