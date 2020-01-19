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

    res_path = "C:/Users/ethan/Downloads/Make Into Chars/Final/"
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
    dir_list_s = [o for o in listdir(res_path + "/supporters") if isdir(join(res_path + "/supporters", o))]
    dir_list_a = [o for o in listdir(res_path + "/adventurers") if isdir(join(res_path + "/adventurers", o))]

    # Find Names
    names = []
    file = open(names_path, "r")
    for name in file:
        names.append(name[:-1])
    file.close()

    # STart to write to output
    file = open(output_path, "w+")
    # Type, Type, health, mana, strength, magic, endurance, dexterity, agility, Full Name, Display Name, ID, Moves
    for name in dir_list_a:
        print("Adding ", name, "To the File as an Adventurer")
        file.write('A, ')

        t_type = random.randint(0, 4) # 0:Magical, 1:Physical 2:Balanced, 3:Defensive, 4:Healing
        print("Is of type: ", t_type)
        file.write(str(t_type) + ', ')

        health_base = random.randint(80, 150)
        print("Has health: ", health_base)
        file.write(str(health_base) + ', ')

        mana_base = random.randint(20, 60)
        print("Has mana: ", mana_base)
        file.write(str(mana_base) + ', ')

        strength_base = random.randint(2, 20)
        print("Has strength: ", strength_base)
        file.write(str(strength_base) + ', ')

        magic_base = random.randint(2, 20)
        print("Has magic: ", magic_base)
        file.write(str(magic_base) + ', ')

        endurance_base = random.randint(1, 15)
        print("Has endurance: ", endurance_base)
        file.write(str(endurance_base) + ', ')

        dexterity_base = random.randint(1, 15)
        print("Has dexterity: ", dexterity_base)
        file.write(str(dexterity_base) + ', ')

        agility_base = random.randint(1, 15)
        print("Has agility: ", agility_base)
        file.write(str(agility_base))

        id_name, full_name = get_name(name)

        print("Full Name: ", full_name)
        file.write('\t, ' + full_name + '')
        print("Id: ", id_name)
        file.write('\t\t\t, ' + id_name)
        print("File Id: ", name)
        file.write('\t\t\t, ' + name)
        print('Basic Moves: Mid P.Attack,Fiendfyre,Rapture,Drill,Lil Rafaga')
        file.write('\t\t\t\t,Mid P.Attack,Fiendfyre,Rapture,Drill,Lil Rafaga\n')

    for name in dir_list_s:
        print("Adding ", name, "To the File as an Supporter")
        file.write('S, ')

        t_type = random.randint(0, 4) # 0:Magical, 1:Physical 2:Balanced, 3:Defensive, 4:Healing
        print("Is of type: ", t_type)
        file.write(str(t_type) + ', ')

        health_base = random.randint(80, 150)
        print("Has health: ", health_base)
        file.write(str(health_base) + ', ')

        mana_base = random.randint(20, 60)
        print("Has mana: ", mana_base)
        file.write(str(mana_base) + ', ')

        strength_base = random.randint(2, 20)
        print("Has strength: ", strength_base)
        file.write(str(strength_base) + ', ')

        magic_base = random.randint(2, 20)
        print("Has magic: ", magic_base)
        file.write(str(magic_base) + ', ')

        endurance_base = random.randint(1, 15)
        print("Has endurance: ", endurance_base)
        file.write(str(endurance_base) + ', ')

        dexterity_base = random.randint(1, 15)
        print("Has dexterity: ", dexterity_base)
        file.write(str(dexterity_base) + ', ')

        agility_base = random.randint(1, 15)
        print("Has agility: ", agility_base)
        file.write(str(agility_base))

        id_name, full_name = get_name(name)

        print("Full Name: ", full_name)
        file.write('\t, ' + full_name + '')
        print("Id: ", id_name)
        file.write('\t\t\t, ' + id_name)
        print("File Id: ", name)
        file.write('\t\t\t, ' + name + '\n')
    file.close()
    print("Finished Writing config file!")