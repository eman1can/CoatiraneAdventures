from random import choices, randint
from time import time

from pandas import DataFrame, ExcelWriter
import numpy as np

compass = 'S, compass, Compass, general, single, 375\nnone\nHave trouble getting lost? Buy a compass and never get lost again!'
pocket_watch = 'S, pocket_watch, Pocket Watch, general, single, 375\nnone\nKeep losing track of time? Buy a watch and always know the time!'

tool_types = ['harvesting_knife', 'pickaxe', 'shovel', 'axe']
soft_materials = ['Cloth 0.5', 'Padded 0.75', 'Leather 1', 'Hardened Leather 1.5']
hard_materials = [
    'Tin 1.5',
    'Copper 3.0',
    'Iron 4.5',
    'Platinum 4.0-4.5',
    'Titanium 6.0',
    'Tungsten 7.5',
    'Meteoric Iron 10.5-11.0',
    'Golanthium 13.0-15.0']

alloy_hard_materials = [
    'Bronze 3.0',
    'Steel 4.0-4.5',
    'Hardened Steel 7.0-8.0',
    'Tungsten Carbide 8.5-9.0',
    'Dark Steel 9.0-9.5',
    'Mithril 9.5-10.5',
    'Adamantite 11.0-13.0',
    'Trinium 15.0-16.0']

gems = [
    'Spinel 7.5-8.0',
    'Opal 5.5-6.0',
    'Onyx 6.5-7.0',
    'Agate 6.5-7.0',
    'Emerald 7.5-8.0',
    'Garnet 6.5-7.5',
    'Danburite 7.0-7.5',
    'Diopside 5.5-6.5',
    'Chrysoberyl 8.5',
    'Chrysocolla 2.5-3.5',
    'Sapphire 9.0',
    'Topaz 8.0',
    'Zircon 7.5',
    'Ruby 9.0',
    'Citrine 7.0',
    'Fluorite 4.0',
    'Garnet 6.5-7.5',
    'Amethyst 7.0',
    'Ametrine 7.0',
    'Ammolite 3.5-4.5',
    'Andesine 6.0-6.5',
    'Apatite 5.0',
    'Aquamarine 7.5-8.0',
    'Beryl 7.5-8.0',
    'Aventurine 6.5',
    'Azurite 3.5-4.0',
    'Zoisite 6.0-7.0',
    'Bixbite 7.5-8.0',
    'Blizzard Stone 6.0-7.0',
    'Bloodstone 7.0',
    'Goshenite 7.5-8.0',
    'Kyanite 4.5-7.0',
    'Heliodor 7.5-8.0',
    'Hessonite 6.5-7.5',
    'Indraneelam 6.0',
    'Iolite 7.0-7.5',
    'Jade 6.0-7.0',
    'Jasper 6.5-7.0',
    'Neelam 9.0',
    'Kunzite 6.5-7.0',
    'Labradorite 6.0-6.5',
    'Lapis Lazuli 5.0-5.5',
    'Quartz 7.0',
    'Malachite 3.5-4.0',
    'Moonstone 6.0-6.5',
    'Morganite 7.5-8.0',
    'Obsidian 5.0-6.0',
    'Padparadscha 9.0',
    'Peridot 6.5-7.0',
    'Turquoise 5.0-6.0',
    'Petalite 6.5',
    'Prehnite 6.0-6.5',
    'Rhodochrosite 3.5-4.0',
    'Rhodonite 5.5-6.0',
    'Rutilated Quartz 7.0',
    'Sang-E-Maryam 8.6',
    'Serpentine 3.0-6.0',
    'Sodalite 5.5-6.0',
    'Spectrolite 6.5',
    'Spessartite 7.0',
    'Sunstone 6.0-6.5',
    'Taaffeite 8.5',
    'Tanzanite 6-6.5',
    'Tiger eye 7.0',
    'Titanite 5.0-5.5',
    'Tsavorite 7.0-7.5',
    'Zoisite 6.0-6.5']

magic_stone_types = ['tiny', 'small', 'medium', 'regular', 'large', 'huge']

# Unit conversion is for crafting only, but should be reflected in prices too.

# Generate Magic Stone Types
magic_stone_text = {'tiny': 'sliver', 'small': 'fragment', 'medium': 'chunk', 'regular': '', 'large': 'crystal', 'huge': 'cluster'}
magic_stone_sub_text = {'tiny': 'A {0} sliver of a magic stone',
                        'small': 'A {0} fragment of a magic stone',
                        'medium': 'A {0} chunk of a magic stone',
                        'regular': 'A {0} magic stone',
                        'large': 'A {0} magic stone crystal',
                        'huge': 'A {0} cluster of magic stones'}

magic_stones = []
for large_type in magic_stone_types:
    for small_type in magic_stone_types:
        definition = f'D, {large_type}_{small_type}_magic_stone, {small_type.title()} Magic Stone {magic_stone_text[large_type]}, multi, {100}, {200}\n{magic_stone_sub_text[large_type].format(small_type)}.\n'
        magic_stones.append(definition)
print(f'{len(magic_stones)} Magic Stones.')

# All enemy shit
ENCOUNTER_CHANCE = 0.15

floor_ids = [f'floor_{x + 1}' for x in range(60)]
floor_sizes = [13, 14, 17, 18, 18, 19, 19, 20, 21,  21,
               22, 22, 23, 24, 24, 25, 26, 26, 27,  27,
               28, 29, 29, 30, 31, 31, 32, 32, 33,  34,
               34, 35, 36, 36, 37, 37, 38, 39, 39,  40,
               41, 43, 45, 47, 49, 51, 53, 55, 57,  57,
               59, 61, 64, 66, 68, 71, 73, 75, 78,  80,
               82, 85, 87, 89, 92, 94, 96, 99, 101, 103]
map_types = ['path_map', 'full_map', 'safe_zone_map']

enemies = ['goblin', 'kobold', 'jack_bird', 'dungeon_lizard', 'frog_shooter', 'war_shadow', 'killer_ant', 'purple_moth', 'needle_rabbit', 'blue_papilio',
           'orc', 'imp', 'bad_bat', 'hard_armored', 'infant_dragon', 'silverback', 'black_wyvern', 'wyvern', 'crystal_mantis', 'lamia mormos', 'hellhound',
           'almiraj', 'dungeon_worm', 'minotaur', 'lygerfang', 'bugbear', 'battle_boar', 'lizardman', 'firebird', 'vouivre',
           'mad_beetle', 'mammoth_fool', 'dark_fungus', 'gun_libellula', 'sword_stag', 'troll', 'deadly_hornet', 'bloody_hive', 'green_dragon',
           'hobgoblin', 'viscum', 'moss huge', 'metal_rabbit', 'poison_vermis', 'raider_fish', 'harpy', 'siren', 'blue_crab', 'aqua_serpent',
           'crystal_turtle', 'devil_mosquito', 'light_quartz', 'crystaroth_urchin', 'iguazu', 'mermaid', 'merman', 'kelpie', 'afanc', 'dodora',
           'lamia', 'voltimeria', 'bloodsaurus', 'power_bull', 'grand_treant', 'worm_well', 'spartoi', 'barbarian', 'lizardman_elite',
           'obsidian_soldier', 'skull_sheep', 'loup_garou', 'peluda', 'flame_rock', 'fomoire', 'black_rhino', 'deformis_spider', 'cadmus',
           'venom_scorpion', 'thunder_snake', 'silver_worm', 'ill_wyvern', 'valgang_dragon', 'titan_alm', 'unicorn', 'dungeon_fly', 'ogre',
           'gargoyle', 'gryphon', 'arachne', 'hippogriff', 'armarosaurus', 'old_bison', 'ape', 'vulture']

floor_spawns = {'floor_1': {'goblin': 1, 'kobold': 2, 'jack_bird': 5},
                'floor_2': {'goblin': 1, 'kobold': 1, 'jack_bird': 5},
                'floor_3': {'goblin': 1, 'kobold': 1, 'jack_bird': 5},
                'floor_4': {'goblin': 2, 'kobold': 1, 'dungeon_lizard': 2},
                'floor_5': {'goblin': 2, 'kobold': 1, 'dungeon_lizard': 2},
                'floor_6': {'kobold': 1, 'dungeon_lizard': 1, 'frog_shooter': 2},
                'floor_7': {'kobold': 1, 'dungeon_lizard': 2, 'war_shadow': 3, 'killer_ant': 2, 'orc': 3},
                'floor_8': {'war_shadow': 4, 'killer_ant': 2, 'purple_moth': 3, 'orc': 1, 'imp': 1},
                'floor_9': {'war_shadow': 4, 'killer_ant': 2, 'purple_moth': 3, 'blue_papilio': 5, 'orc': 1, 'imp': 1},
                'floor_10': {'killer_ant': 1, 'purple_moth': 4, 'blue_papilio': 5, 'bad_bat': 3, 'hard_armored': 2},
                'floor_11': {'purple_moth': 4, 'blue_papilio': 5, 'imp': 2, 'bad_bat': 3, 'hard_armored': 1},
                'floor_12': {'blue_papilio': 5, 'imp': 2, 'hard_armored': 1, 'silverback': 3, 'infant_dragon': 5},
                'floor_13': {'hard_armored': 1, 'infant_dragon': 5, 'silverback': 2, 'black_wyvern': 4},
                'floor_14': {'hard_armored': 1, 'silverback': 1, 'black_wyvern': 4, 'wyvern': 4, 'metal_rabbit': 1},
                'floor_15': {'black_wyvern': 4, 'wyvern': 4, 'crystal_mantis': 3, 'hellhound': 1, 'metal_rabbit': 1},
                'floor_16': {'black_wyvern': 4, 'wyvern': 4, 'crystal_mantis': 3, 'hellhound': 1, 'imp': 2, 'needle_rabbit': 1},
                'floor_17': {'crystal_mantis': 3, 'wyvern': 4, 'lamia mormos': 3, 'hellhound': 1, 'almiraj': 1, 'imp': 2, 'needle_rabbit': 1},
                'floor_18': {'crystal_mantis': 3, 'wyvern': 4, 'lamia mormos': 3, 'hellhound': 2, 'imp': 2, 'armarosaurus': 4},
                'floor_19': {'wyvern': 4, 'lamia mormos': 2, 'hellhound': 1, 'almiraj': 1, 'imp': 2, 'poison_vermis': 4},
                'floor_20': {'lamia mormos': 2, 'hellhound': 1, 'almiraj': 1, 'imp': 2, 'minotaur': 3, 'poison_vermis': 4},

                # The "Middle" Levels
                'floor_21': {'dungeon_worm': 4, 'minotaur': 2, 'lygerfang': 1, 'bugbear': 1, 'hobgoblin': 1, 'flame_rock': 2, 'old_bison': 3, 'needle_rabbit': 2},
                'floor_22': {'dungeon_worm': 4, 'minotaur': 2, 'lygerfang': 1, 'bugbear': 1, 'hobgoblin': 1, 'flame_rock': 2, 'old_bison': 3, 'needle_rabbit': 2},
                'floor_23': {'dungeon_worm': 4, 'minotaur': 2, 'lygerfang': 1, 'lizardman': 1, 'hobgoblin': 2, 'flame_rock': 2, 'needle_rabbit': 2},
                'floor_24': {'dungeon_worm': 3, 'minotaur': 2, 'lygerfang': 2, 'battle_boar': 1, 'metal_rabbit': 2, 'dungeon_fly': 2, 'armarosaurus': 3},
                'floor_25': {'dungeon_worm': 3, 'minotaur': 2, 'lygerfang': 2, 'battle_boar': 1, 'metal_rabbit': 2, 'dungeon_fly': 2, 'armarosaurus': 3},
                'floor_26': {'lygerfang': 1, 'bugbear': 2, 'battle_boar': 2, 'lizardman': 1, 'firebird': 3, 'poison_vermis': 4, 'needle_rabbit': 1},
                'floor_27': {'lizardman': 1, 'firebird': 3, 'mad_beetle': 1, 'deadly_hornet': 2, 'bloody_hive': 2, 'dungeon_fly': 1, 'arachne': 1},
                'floor_28': {'lizardman': 1, 'firebird': 3, 'vouivre': 5, 'mad_beetle': 1, 'mammoth_fool': 3, 'metal_rabbit': 2, 'arachne': 2},
                'floor_29': {'lizardman': 1, 'firebird': 3, 'vouivre': 5, 'mad_beetle': 1, 'mammoth_fool': 3, 'metal_rabbit': 2, 'arachne': 2},
                'floor_30': {'vouivre':  5, 'mad_beetle': 1, 'mammoth_fool': 1, 'dark_fungus': 1, 'green_dragon': 3, 'dungeon_fly': 2, 'arachne': 2},
                'floor_31': {'mad_beetle': 1, 'mammoth_fool': 1, 'dark_fungus': 2, 'deadly_hornet': 2, 'bloody_hive': 2, 'dungeon_fly': 2, 'arachne': 3},
                'floor_32': {'mad_beetle': 2, 'mammoth_fool': 1, 'dark_fungus': 1, 'deadly_hornet': 2, 'bloody_hive': 2, 'unicorn': 5, 'gryphon': 4},
                'floor_33': {'mammoth_fool': 1, 'dark_fungus': 1, 'gun_libellula': 2, 'deadly_hornet': 3, 'bloody_hive': 3, 'unicorn': 5, 'gryphon': 4},
                'floor_34': {'mammoth_fool': 1, 'dark_fungus': 1, 'gun_libellula': 1, 'deadly_hornet': 3, 'bloody_hive': 3, 'unicorn': 5, 'gryphon': 3},
                'floor_35': {'dark_fungus': 2, 'gun_libellula': 1, 'sword_stag': 2, 'green_dragon': 3, 'hobgoblin': 2, 'unicorn': 5, 'ogre': 3},
                'floor_36': {'dark_fungus': 2, 'gun_libellula': 1, 'sword_stag': 2, 'green_dragon': 4, 'hobgoblin': 2, 'dungeon_fly': 2, 'ogre': 3},
                'floor_37': {'gun_libellula': 2, 'sword_stag': 1, 'green_dragon': 3, 'viscum': 3, 'moss huge': 2, 'metal_rabbit': 1, 'unicorn': 5},
                'floor_38': {'gun_libellula': 1, 'sword_stag': 1, 'green_dragon': 3, 'hobgoblin': 1, 'viscum': 3, 'moss huge': 2, 'ogre': 2},
                'floor_39': {'green_dragon': 2, 'hobgoblin': 1, 'viscum': 3, 'moss huge': 2, 'metal_rabbit': 1, 'poison_vermis': 3, 'unicorn': 4},

                # The "Water" Levels
                'floor_40': {'raider_fish': 1, 'blue_crab': 1, 'devil_mosquito': 2, 'crystaroth_urchin': 3, 'afanc': 3, 'lamia': 2, 'vulture': 3, 'troll': 2},
                'floor_41': {'raider_fish': 1, 'blue_crab': 1, 'aqua_serpent': 2, 'crystal_turtle': 3, 'crystaroth_urchin': 2, 'afanc': 3, 'lamia': 2, 'vulture': 3, 'troll': 3},
                'floor_42': {'raider_fish': 1, 'harpy': 4, 'blue_crab': 2, 'aqua_serpent': 2, 'crystaroth_urchin': 3, 'afanc': 3, 'lamia': 2, 'vulture': 3, 'troll': 2},
                'floor_43': {'raider_fish': 1, 'harpy': 3, 'blue_crab': 1, 'aqua_serpent': 1, 'crystaroth_urchin': 3, 'kelpie': 3, 'afanc': 2, 'lamia': 1, 'voltimeria': 3, 'vulture': 3},
                'floor_44': {'raider_fish': 1, 'harpy': 2, 'siren': 4, 'blue_crab': 1, 'devil_mosquito': 2, 'iguazu': 3, 'mermaid': 5, 'kelpie': 3, 'dodora': 4, 'voltimeria': 3},
                'floor_45': {'raider_fish': 1, 'harpy': 2, 'siren': 3, 'blue_crab': 1, 'devil_mosquito': 2, 'iguazu': 3, 'mermaid': 5, 'merman': 4, 'kelpie': 3, 'dodora': 4, 'voltimeria':3},
                'floor_46': {'raider_fish': 1, 'siren': 3, 'blue_crab': 1, 'crystal_turtle': 4, 'devil_mosquito': 3, 'iguazu':2, 'mermaid': 4, 'merman': 4, 'kelpie': 3, 'dodora': 4, 'voltimeria': 2},
                'floor_47': {'siren': 2, 'blue_crab': 1, 'aqua_serpent': 1, 'light_quartz': 3, 'iguazu': 2, 'mermaid': 4, 'merman': 4, 'dodora': 3, 'voltimeria': 2},
                'floor_48': {'siren': 2, 'aqua_serpent': 1, 'crystal_turtle': 4, 'light_quartz': 3, 'iguazu': 2, 'mermaid': 3, 'merman': 3, 'dodora': 3, 'voltimeria': 2},

                # The "Deep" Levels
                'floor_49': {'bloodsaurus': 1, 'grand_treant': 2, 'worm_well': 5, 'spartoi': 1, 'loup_garou': 1, 'black_rhino': 1, 'venom_scorpion': 3, 'titan_alm': 3, 'gargoyle': 4, 'armarosaurus': 4, 'ape':  2},
                'floor_50': {'bloodsaurus': 1, 'grand_treant': 2, 'worm_well': 5, 'spartoi': 1, 'loup_garou': 1, 'black_rhino': 1, 'venom_scorpion': 3, 'titan_alm': 3, 'gargoyle': 4, 'armarosaurus': 4, 'ape':  2},
                'floor_51': {'bloodsaurus': 1, 'worm_well': 5, 'spartoi': 1, 'skull_sheep': 2, 'loup_garou': 1, 'flame_rock': 3, 'black_rhino': 2, 'ill_wyvern': 3, 'titan_alm': 3, 'gargoyle': 3, 'ape':  1},
                'floor_52': {'power_bull': 1, 'worm_well': 4, 'spartoi': 1, 'barbarian': 1, 'skull_sheep': 2, 'flame_rock': 3, 'black_rhino': 2, 'ill_wyvern': 3, 'titan_alm': 3, 'armarosaurus': 4, 'ape':  1},
                'floor_53': {'power_bull': 1, 'worm_well': 4, 'spartoi': 2, 'barbarian': 1, 'skull_sheep': 2, 'flame_rock': 3, 'venom_scorpion': 2, 'ill_wyvern': 3, 'gargoyle': 3, 'old_bison': 1, 'ape':  1},
                'floor_54': {'power_bull': 1, 'worm_well': 4, 'barbarian': 1, 'lizardman_elite': 1, 'peluda': 3, 'fomoire': 2, 'venom_scorpion': 2, 'valgang_dragon': 5, 'old_bison': 1, 'ape':  2},
                'floor_55': {'grand_treant': 1, 'worm_well': 4, 'barbarian': 1, 'lizardman_elite': 1, 'peluda': 2, 'fomoire': 2, 'deformis_spider': 1, 'valgang_dragon': 4, 'gryphon': 3, 'old_bison': 2, 'ape':  2},
                'floor_56': {'grand_treant': 1, 'worm_well': 3, 'barbarian': 2, 'lizardman_elite': 1, 'peluda': 2, 'fomoire': 2, 'deformis_spider': 1, 'valgang_dragon': 4, 'gryphon': 3, 'old_bison': 2, 'ape':  2},
                'floor_57': {'worm_well': 4, 'barbarian': 2, 'lizardman_elite': 1, 'obsidian_soldier': 2, 'fomoire': 1, 'deformis_spider': 1, 'cadmus': 3, 'silver_worm': 3, 'hippogriff': 3, 'ape':  3},
                'floor_58': {'worm_well': 4, 'lizardman_elite': 1, 'obsidian_soldier': 2, 'fomoire': 1, 'cadmus': 3, 'thunder_snake': 3, 'silver_worm': 3, 'valgang_dragon': 3, 'hippogriff': 3, 'ape':  3},
                'floor_59': {'worm_well': 4, 'lizardman_elite': 1, 'obsidian_soldier': 2, 'fomoire': 1, 'cadmus': 3, 'thunder_snake': 2, 'silver_worm': 3, 'valgang_dragon': 3, 'hippogriff': 3, 'ape':  3},
                'floor_60': {'worm_well': 4, 'lizardman_elite': 1, 'obsidian_soldier': 1, 'cadmus': 3, 'thunder_snake': 2, 'silver_worm': 2, 'hippogriff': 3, 'ape':  2, 'valgang_dragon': 2}}

drop_types = {
    'claw': {
        'goblin': 1,
        'kobold': 1,
        'dungeon_lizard': 1,
        'war_shadow': 1,
        'imp': 1,
        'hard_armored': 1,
        'infant_dragon': 1,
        'wyvern': 1,
        'lamia mormos': 1,
        'minotaur': 1,
        'bugbear': 1,
        'battle_boar': 1,
        'lizardman': 1,
        'vouivre': 1,
        'green_dragon': 1,
        'hobgoblin': 1,
        'moss huge': 1,
        'harpy': 1,
        'siren': 1,
        'blue_crab': 1,
        'afanc': 1,
        'dodora': 1,
        'lamia': 1,
        'spartoi': 1,
        'lizardman_elite': 1,
        'deformis_spider': 1
    }, 'fang': {
        'goblin': 1,
        'kobold': 1,
        'dungeon_lizard': 1,
        'imp': 1,
        'infant_dragon': 1,
        'black_wyvern': 1,
        'wyvern': 1,
        'hellhound': 1,
        'almiraj': 1,
        'dungeon_worm': 1,
        'minotaur': 1,
        'lygerfang': 1,
        'vouivre': 1,
        'battle_boar': 1,
        'mammoth_fool': 1,
        'green_dragon': 1,
        'hobgoblin': 1,
        'raider_fish': 2,
        'siren': 2,
        'devil_mosquito': 1,
        'crystaroth_urchin': 1,
        'afanc': 1,
        'bloodsaurus': 1,
        'worm_well': 1,
        'loup_garou': 1,
        'thunder_snake': 1,
        'silver_worm': 1,
        'valgang_dragon': 1,
        'vulture': 1
    }, 'egg': {
        'jack_bird': 0,
        'vouivre': 0,
        'flame_rock': 1
    }, 'hide': {
        'kobold': 2,
        'jack_bird': 2,
        'needle_rabbit': 2,
        'orc': 2,
        'imp': 2,
        'silverback': 2,
        'hellhound': 2,
        'almiraj': 2,
        'minotaur': 2,
        'lygerfang': 2,
        'bugbear': 2,
        'battle boar': 2,
        'mammoth_fool': 2,
        'sword_stag': 2,
        'troll': 2,
        'moss huge': 2,
        'metal_rabbit': 2,
        'kelpie': 2,
        'power_bull': 2,
        'grand_treant': 2,
        'barbarian': 2,
        'skull_sheep': 2,
        'loup_garou': 2,
        'fomoire': 2,
        'black_rhino': 2,
        'deformis_spider': 2,
        'titan_alm': 2,
        'unicorn': 3,
        'ogre': 2,
        'gryphon': 2,
        'arachne': 2,
        'hippogriff': 2,
        'old_bison': 2,
        'ape': 2,
        'battle_boar': 2
    }, 'scale': {
        'dungeon_lizard': 2,
        'frog_shooter': 2,
        'killer_ant': 2,
        'hard_armored': 2,
        'infant_dragon': 2,
        'black_wyvern': 2,
        'wyvern': 2,
        'lamia mormos': 2,
        'lizardman': 2,
        'vouivre': 2,
        'mad_beetle': 2,
        'deadly_hornet': 2,
        'green_dragon': 2,
        'raider_fish': 2,
        'blue_crab': 2,
        'aqua_serpent': 2,
        'crystal_turtle': 2,
        'mermaid': 2,
        'merman': 2,
        'dodora': 2,
        'lamia': 2,
        'voltimeria': 2,
        'bloodsaurus': 2,
        'worm_well': 2,
        'lizardman_elite': 2,
        'obsidian_soldier': 2,
        'peluda': 2,
        'cadmus': 2,
        'venom_scorpion': 2,
        'thunder_snake': 2,
        'silver_worm': 2,
        'ill_wyvern': 2,
        'valgang_dragon': 2,
        'gargoyle': 2,
        'armarosaurus': 2
    }, 'wing': {
        'purple_moth': 2,
        'blue_papilio': 3,
        'bad_bat': 2,
        'crystal_mantis': 2,
        'firebird': 3,
        'mad_beetle': 2,
        'gun_libellula': 2,
        'deadly_hornet': 2,
        'harpy': 3,
        'siren': 3,
        'aqua_serpent': 2,
        'devil_mosquito': 2,
        'iguazu': 2,
        'kelpie': 2,
        'ill_wyvern': 2,
        'dungeon_fly': 2
    }, 'tongue': {
        'dungeon_lizard': 1,
        'frog_shooter': 1,
        'vulture': 1
    }, 'meat': {
        'jack_bird': 1,
        'needle_rabbit': 1,
        'infant_dragon': 1,
        'blue_crab': 1,
        'light_quartz': 1,
        'afanc': 1,
        'bloodsaurus': 1,
        'barbarian': 1,
        'titan_alm': 1,
        'ogre': 1
    }, 'blood': {
        'killer_ant': 3,
        'infant_dragon': 3,
        'bloody_hive': 3,
        'mermaid': 5,
        'deformis_spider': 3,
        'unicorn': 4
    }, 'horn': {
        'needle_rabbit': 1,
        'sword_stag': 1,
        'crystaroth_urchin': 2,
        'iguazu': 1,
        'power_bull': 2,
        'skull_sheep': 2,
        'peluda': 2,
        'fomoire': 2,
        'black_rhino': 2,
        'unicorn': 5
    }, 'venom': {
        'purple_moth': 2,
        'blue_papilio': 3,
        'black_wyvern': 2,
        'dungeon_worm': 2,
        'dark_fungus': 2,
        'deadly_hornet': 2,
        'bloody_hive': 2,
        'viscum': 2,
        'poison_vermis': 2,
        'crystaroth_urchin': 2,
        'dodora': 2,
        'worm_well': 2,
        'peluda': 2,
        'venom_scorpion': 2,
        'arachne': 2
    }
}

non_natural_hard_materials = []
non_natural_soft_materials = []
monster_types = {}

file = open('monster_list.txt', 'r', encoding='utf-8')
monster_list = file.read().split('\n\n')
file.close()

file = open('natural_materials.txt', 'r', encoding='utf-8')
material_list = file.read().split('\n\n')
file.close()
natural_materials_found = {}
gems_found = {}
floor_hardnesses = {}
for floor in material_list:
    name, material_string, gem_string = floor.split('\n')
    floor_id, hardness = name.split(' → Hardness ')
    floor_hardnesses[floor_id[len('Floor '):]] = float(hardness)
    material_list = material_string[len('   - '):].split(', ')
    gem_list = gem_string[len('   - '):].split(', ')
    for material in material_list:
        if material not in natural_materials_found:
            natural_materials_found[material] = []
        natural_materials_found[material].append(int(floor_id[len('Floor '):]))
    for gem in gem_list:
        if gem not in gems_found:
            gems_found[gem] = []
        gems_found[gem].append(int(floor_id[len('Floor '):]))

element_counts = {
    'None': 0,
    'Earth': 0,
    'Water': 0,
    'Fire': 0,
    'Thunder': 0,
    'Wind': 0,
    'Light': 0,
    'Dark': 0
}
total_elements = 0

materials_found = {}

for monster in monster_list:
    lines = monster.split('\n')
    name = lines[0]
    found = lines[1]
    found_list = found[len('Found on Floor '):].strip().split(', ')
    if name == 'Frog Shooter':
        print(found_list, found)
    for index in range(len(found_list)):
        if 'and' in found_list[index]:
            found_list[index] = found_list[index][4:]
    description = lines[2]
    elements_string = lines[3][len('Type: '):]
    if ',' in elements_string:
        elements = elements_string.split(', ')
    else:
        elements = [elements_string]
    monster_types[name] = elements
    for element in elements:
        element_counts[element] += 1
        total_elements += 1
    hardnesses = lines[4][len('Hardness: '):]
    hard, soft = hardnesses.split(', ')
    hard = hard[:-len('(hard)')]
    soft = soft[:-len('(soft)')]
    for material_type, monster_list in drop_types.items():
        if name.lower().replace(' ', '_') in monster_list:
            if material_type in ['hide']:
                if floor_hardnesses[found_list[0]] == floor_hardnesses[found_list[-1]]:
                    soft = f'{floor_hardnesses[found_list[0]] * 2 / 3}'
                else:
                    soft = f'{floor_hardnesses[found_list[0]] * 2 / 3}-{floor_hardnesses[found_list[-1]] * 2 / 3}'
                # if soft != 'None' and soft != '':
                materials_found[f'{name} {material_type.title()}'] = found_list
                non_natural_soft_materials.append(f'{name} {material_type.title()} {soft}')
                # else:
                #     print('Error', name, 'soft')
            elif material_type in ['fang', 'claw', 'scale', 'horn']:
                # if hard != 'None' and hard != '':
                materials_found[f'{name} {material_type.title()}'] = found_list
                if floor_hardnesses[found_list[0]] == floor_hardnesses[found_list[-1]]:
                    hard = f'{floor_hardnesses[found_list[0]]}'
                else:
                    hard = f'{floor_hardnesses[found_list[0]]}-{floor_hardnesses[found_list[-1]]}'
                non_natural_hard_materials.append(f'{name} {material_type.title()} {hard}')
                # else:
                #     print('Error', name, 'hard')
print('Total Elements:', total_elements)
for element, element_count in element_counts.items():
    print(element, element_count, '-', str(round(element_count / total_elements * 100, 2)) + '%')


class Material:
    def __init__(self, string):
        space_index = string.rindex(' ')
        self.full_string = string[:space_index]
        self.string = string[space_index + 1:]

    def get_numbers(self):
        if '-' in self.string:
            mi, ma = self.string.split('-')
            return float(mi), float(ma)
        else:
            return float(self.string), float(self.string)

    def __gt__(self, other):
        min_self, max_self = self.get_numbers()
        min_other, max_other = other.get_numbers()
        return min_other < min_self

    def __eq__(self, other):
        return self.string == other.string

    def __lt__(self, other):
        min_self, max_self = self.get_numbers()
        min_other, max_other = other.get_numbers()
        return min_other > min_self

    def __str__(self):
        return self.string + ' ' + self.full_string

    def __hash__(self):
        return self.string.__hash__()
materials_found.update(natural_materials_found)
materials_found.update(gems_found)


natural_hard_materials_by_hardness = []
for material in hard_materials:
    natural_hard_materials_by_hardness.append(Material(material))

alloy_hard_materials_by_hardness = []
for material in alloy_hard_materials:
    alloy_hard_materials_by_hardness.append(Material(material))

monster_hard_materials_by_hardness = []
for material in non_natural_hard_materials:
    monster_hard_materials_by_hardness.append(Material(material))

hard_materials_by_hardness = natural_hard_materials_by_hardness + alloy_hard_materials_by_hardness + monster_hard_materials_by_hardness

natural_soft_materials_by_hardness = []
for material in soft_materials:
    natural_soft_materials_by_hardness.append(Material(material))

monster_soft_materials_by_hardness = []
for material in non_natural_soft_materials:
    monster_soft_materials_by_hardness.append(Material(material))

soft_materials_by_hardness = natural_soft_materials_by_hardness + monster_soft_materials_by_hardness

gems_by_hardness = []
for material in gems:
    gems_by_hardness.append(Material(material))

all_materials_by_hardness = hard_materials_by_hardness + soft_materials_by_hardness + gems_by_hardness

natural_hard_materials_by_hardness.sort()
alloy_hard_materials_by_hardness.sort()
monster_hard_materials_by_hardness.sort()
hard_materials_by_hardness.sort()
natural_soft_materials_by_hardness.sort()
monster_soft_materials_by_hardness.sort()
soft_materials_by_hardness.sort()
gems_by_hardness.sort()
all_materials_by_hardness.sort()

# Generate Common items
common_items = []
common_items.append(compass)
common_items.append(pocket_watch)

# Generate mob drops
drops = []
for drop, enemy_list in drop_types.items():
    for enemy in enemy_list:
        drops.append(f'{drop}_{enemy}')
# Generate ore types
for material in hard_materials:
    pass

# Generate gems
for gem in gems:
    pass

# Generate tools
tools = []

for tool in tool_types:
    for material in hard_materials:
        pass
        'S, {tool}_{material}, {names[material]} {names[tool]}, tools, single, cost\nfloor, floor_start\ntext\nWarning: floor_end'

# Generate floor maps
for floor in floor_ids:
    for map_type in map_types:
        pass

# Generate Resource maps
for floor in floor_ids:
    for ore in hard_materials:
        pass
    for gem in gems:
        pass
    for enemy in enemies:
        pass

# Generate plants

# Generate woods

# Generate Ingredients
#- Vials

# Generate Potions

# Generate Equipment

# Generate unique items (undine cloth, etc.)

# Generate other

# Higher rarity = less spawn
rarities = [1, 2, 3, 4, 5]
rarities_weights = [1 / (2 ** rarities[x]) for x in range(5)]

enemy_drops = {}
for drop_type, drop_list in drop_types.items():
    for enemy_name, drop_rarity in drop_list.items():
        if enemy_name not in enemy_drops:
            enemy_drops[enemy_name] = {}
        enemy_drops[enemy_name][drop_type] = drop_rarity


def get_drop_item(drop_rarities):
    drop_list = drop_rarities[choices(rarities, rarities_weights, k=1)[0]]
    if len(drop_list) > 0:
        item = drop_list[randint(0, len(drop_list) - 1)]
        if item is None:
            return [None]
        # item_count = int(item[:item.index(' ')])
        # if item_count > 4:
        #     enemy_name, item_name = item[item.index(' ') + 1:item.rindex(' ')], item[item.rindex(' ') + 1:]
        #     enemy_id = enemy_name.replace(' ', '_').lower()
        #     replace_count = randint(0, item_count - 4)
        #     if replace_count > 0 and len(enemy_drops[enemy_id]) > 1:
        #         first_item = f'{item_count - replace_count} {enemy_name} {item_name}'
        #         new_item = None
        #         while new_item is None:
        #             print(enemy_drops[enemy_id])
        #             new_item = list(enemy_drops[enemy_id].keys())[randint(0, len(enemy_drops[enemy_id].keys()))]
        #             if new_item == item_name.lower():
        #                 new_item = None
        #         second_item = f'{replace_count} {enemy_name} {new_item.title()}'
        #         return [first_item, second_item]
        return [item]
    return [None]


def simulate_ecounters(floor_spawn_rarities, drop_rarities, guarrenteed):
    spawn_count_total, spawn_counts, spawn_count_totals, drop_counts, drop_count_totals, first_encounters = 0, {}, {}, {}, {}, {}
    # Set all counters to 0
    for enemy, boost_list in drop_rarities.items():
        spawn_count_totals[enemy] = 0
        drop_count_totals[enemy] = {}
        first_encounters[enemy] = None
        if enemy in guarrenteed:
            for drop_item in guarrenteed[enemy]:
                drop_count_totals[drop_item[2:]] = 0
        for boost, rarity_list in boost_list.items():
            spawn_counts[f'{enemy} Level {boost + 1}'] = 0
            drop_counts[f'{enemy} Level {boost + 1}'] = {}
            for drop_list in rarity_list.values():
                for drop_name in drop_list:
                    if drop_name is None:
                        continue
                    drop_count_totals[enemy][drop_name[drop_name.index(' ') + 1:]] = 0
                    drop_counts[f'{enemy} Level {boost + 1}'][drop_name] = 0
    # Do 1 million encounters
    for x in range(1000):
        # Choose a random number of enemies to spawn
        count = choices([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], k=1)[0]
        spawn_count_total += count

        # Choose rarities to spawn
        spawn = choices(rarities, rarities_weights, k=count)
        for rarity in spawn:
            # From the spawn rarity list, choose a random enemy to spawn
            if len(floor_spawn_rarities[rarity]) > 0:
                name = floor_spawn_rarities[rarity][randint(0, len(floor_spawn_rarities[rarity]) - 1)]

                # Individual counts
                spawn_counts[name] += 1

                # Total counts
                total_name = name[:-8]
                spawn_count_totals[total_name] += 1

                if not first_encounters[total_name]:
                    first_encounters[total_name] = x

                # Drop Item
                boost = int(name[name.rindex(' ') + 1:]) - 1
                dropped_item_list = get_drop_item(drop_rarities[total_name][boost])
                for dropped_item in dropped_item_list:
                    if dropped_item is not None:
                        drop_counts[name][str(dropped_item)] += 1
                        drop_count_totals[total_name][str(dropped_item)[str(dropped_item).index(' ') + 1:]] += 1
                if total_name in guarrenteed:
                    for drop_item in guarrenteed[total_name]:
                        drop_count_totals[drop_item[2:]] += 1
    return spawn_count_total, spawn_counts, spawn_count_totals, drop_counts, drop_count_totals, first_encounters


floors = {}
# Make the dictionary of the spawn rarities
for floor_id in list(floor_spawns.keys()):
    floors[floor_id] = {1: [], 2: [], 3: [], 4: [], 5: []}
    for enemy, rarity in floor_spawns[floor_id].items():
        name = enemy.replace("_", " ").title()
        for new_rarity in range(rarity, 6):
            level_name = f'{name} Level {new_rarity + 1 - rarity}'
            floors[floor_id][new_rarity].append(level_name)

floor_data = {}
start_time = time()
last_time = start_time
for floor_id, spawn_rarities in floors.items():
    drop_rarities = {}
    guarrenteed = {}
    for spawn_list in spawn_rarities.values():
        for enemy in spawn_list:
            name, boost = enemy[:-8], int(enemy[-1]) - 1
            if name not in drop_rarities:
                drop_rarities[name] = {}
            if boost not in drop_rarities[name]:
                drop_rarities[name][boost] = {1: [None], 2: [], 3: [], 4: [], 5: []}
            for drop_type, drop_list in drop_types.items():
                if name.lower().replace(" ", "_") in drop_list.keys():
                    rarity = drop_list[name.lower().replace(" ", "_")]
                    if rarity == 0:
                        if name not in guarrenteed:
                            guarrenteed[name] = []
                        guarrenteed[name].append(f'1 {name} {drop_type.title()}')
                        continue
                    for new_rarity in range(rarity, 6):
                        drop_rarities[name][boost][new_rarity].append(f'{1 + new_rarity - 1 + boost} {name} {drop_type.title()}')
    spawn_count_total, spawn_counts, spawn_count_totals, drop_counts, drop_count_totals, first_encounters = simulate_ecounters(spawn_rarities, drop_rarities, guarrenteed)
    # floor_num = int(floor_id.split('_')[1])
    floor_data[floor_id.title().replace('_', ' ')] = {}
    floor_data[floor_id.title().replace('_', ' ')]['spawn_count_total'] = spawn_count_total
    floor_data[floor_id.title().replace('_', ' ')]['spawn_counts'] = spawn_counts
    floor_data[floor_id.title().replace('_', ' ')]['spawn_count_totals'] = spawn_count_totals
    floor_data[floor_id.title().replace('_', ' ')]['drop_counts'] = drop_counts
    floor_data[floor_id.title().replace('_', ' ')]['drop_count_totals'] = drop_count_totals
    floor_data[floor_id.title().replace('_', ' ')]['first_encounters'] = first_encounters

    # print(floor_id.title().replace('_', ' ') + ':')
    current_time = time()
    print(floor_id.title().replace('_', ' '), f'took {round(current_time - last_time, 2)} - currently {round(current_time - start_time, 2)}')
    last_time = current_time
    # for name, count in spawn_count_totals.items():
    #     print('\t' + name, str(round(count / spawn_count_total * 100, 2)) + '%', '-', first_encounters[name])
    #     if name in guarrenteed:
    #         for drop_item in guarrenteed[name]:
    #             print('\t\t' + drop_item[2:], str(round(drop_count_totals[drop_item[2:]] / count * 100, 2)) + '%', '/', str(round(drop_count_totals[drop_item[2:]] / spawn_count_total * 100, 2)) + '%')
    #     for drop_item, drop_count in sorted(drop_count_totals[name].items()):
    #         print('\t\t' + drop_item, str(round(drop_count / count * 100, 2)) + '%', '/', str(round(drop_count / spawn_count_total * 100, 2)) + '%')
    # print()
    # for name, count in spawn_counts.items():
    #     print('\t' + name, str(round(count / spawn_count_total * 100, 2)) + '%')
    #     if name[:-8] in guarrenteed:
    #         for drop_item in guarrenteed[name[:-8]]:
    #             print('\t\t' + drop_item, str(round(drop_count_totals[drop_item[2:]] / count * 100, 2)) + '%', '/', str(round(drop_count_totals[drop_item[2:]] / spawn_count_total * 100, 2)) + '%')
    #     for drop_item, drop_count in sorted(drop_counts[name].items()):
    #         print('\t\t' + drop_item, str(round(drop_count / count * 100, 2)) + '%', '/', str(round(drop_count / spawn_count_total * 100, 2)) + '%')
    # print('\n')

def char_string_to_index(string):
    if len(string) > 1:
        return (char_string_to_index(string[:-1]) + 1) * 26 + (ord(string[-1]) - 65)
    return ord(string[-1]) - 65

def index_to_char_string(index):
    if index > 25:
        return index_to_char_string(int(index / 26) - 1) + chr((index % 26) + 65)
    return chr(index + 65)

def get_next(string):
    if string[-1] != 'Z':
        return string[:-1] + chr(ord(string[-1]) + 1)
    elif len(string) > 1:
        # String has another to increment
        return get_next(string[:-1]) + 'A'
    else:
        return 'AA'


def char_range(start, end):
    start_index = char_string_to_index(start.upper())
    end_index = char_string_to_index(end.upper())

    current = start.upper()
    for x in range(start_index, end_index):
        yield current
        current = get_next(current)

# Make Spawn Rate vs Floor data frame
floor_spawn_rates_data = {}
for monster in enemies:
    name = monster.replace('_', ' ').title()
    floor_spawn_rates_data[name] = []
    for floor in floor_data.values():
        if name in floor['spawn_count_totals']:
            floor_spawn_rates_data[name].append(floor['spawn_count_totals'][name] / floor['spawn_count_total'])
        else:
            floor_spawn_rates_data[name].append(np.nan)

floor_spawn_rates_data['Totals'] = []
for floor in floor_data.values():
    floor_spawn_rates_data['Totals'].append(floor['spawn_count_total'])


# Material Hardness Data
def create_hardness_data(hardness_array):
    hardness_data = {}
    for index, material in enumerate(hardness_array):
        array = []
        min_hardness, max_hardness = material.get_numbers()
        for x in range(0, 16 * 4 + 1):
            if x / 4 >= min_hardness and x / 4 <= max_hardness:
                array.append(index + 1)
            else:
                array.append(np.nan)
        hardness_data[material.full_string] = array
    return hardness_data


def create_hardness_data_frame(hardness_data):
    return DataFrame(data=hardness_data, index=[x / 4 for x in range(0, 16 * 4 + 1)], columns=hardness_data.keys())


hardness_types = {
    'Hard Materials (Natural)': natural_hard_materials_by_hardness,
    'Hard Materials (Alloys)': alloy_hard_materials_by_hardness,
    'Hard Materials (Monster)': monster_hard_materials_by_hardness,
    'All Hard Materials': hard_materials_by_hardness,
    'Soft Materials (Natural)': natural_soft_materials_by_hardness,
    'Soft Materials (Monster)': monster_soft_materials_by_hardness,
    'All Soft Materials' : soft_materials_by_hardness,
    'Gems': gems_by_hardness,
    'All Materials': all_materials_by_hardness
}

hardness_datas = {}
for hardness_type, hardness_array in hardness_types.items():
    hardness_datas[hardness_type] = create_hardness_data(hardness_array)

floor_spawn_rates = DataFrame(data=floor_spawn_rates_data, index=list(floor_data.keys()), columns=floor_spawn_rates_data.keys())

hardness_dataframes = {}
for hardness_type, hardness_data in hardness_datas.items():
    hardness_dataframes[hardness_type] = create_hardness_data_frame(hardness_data)


with ExcelWriter('output.xlsx') as writer:
    floor_spawn_rates.to_excel(writer, sheet_name='Spawn Rates')
    for hardness_type, hardness_dataframe in hardness_dataframes.items():
        hardness_dataframe.to_excel(writer, sheet_name=hardness_type)
    floor_spawn_rates_sheet = writer.sheets['Spawn Rates']
    hardness_sheets = {}
    for hardness_type in hardness_dataframes.keys():
        hardness_sheets[hardness_type] = writer.sheets[hardness_type]

    # Create Monster Spawn Rate Charts
    chart = writer.book.add_chart({'type': 'scatter', 'subtype': 'straight'})
    log_chart = writer.book.add_chart({'type': 'scatter', 'subtype': 'straight'})
    for char_index in char_range('B', index_to_char_string(len(enemies) + 2)):
        if char_string_to_index(char_index) != len(enemies) + 1:
            name = (enemies)[char_string_to_index(char_index) - 1].replace('_', ' ').title()
            chart.add_series({
                'name': ['Spawn Rates', 0, char_string_to_index(char_index)],
                'categories': ['Spawn Rates', 1, 0, len(floor_data) + 1, 0],
                'values': ['Spawn Rates', 1, char_string_to_index(char_index), len(floor_data), char_string_to_index(char_index)],
                'marker': {'type': 'circle'}
            })
            log_chart.add_series({
                'name':       ['Spawn Rates', 0, char_string_to_index(char_index)],
                'categories': ['Spawn Rates', 1, 0, len(floor_data) + 1, 0],
                'values':     ['Spawn Rates', 1, char_string_to_index(char_index), len(floor_data), char_string_to_index(char_index)],
                'marker':     {'type': 'circle'}
            })
    chart.set_title({'name': 'Monster Spawn Rates by Floor'})
    log_chart.set_title({'name': 'Monster Spawn Rates by Floor'})
    chart.show_blanks_as('span')
    log_chart.show_blanks_as('span')
    chart.set_legend({'position': 'top'})
    log_chart.set_legend({'position': 'bottom'})
    chart.set_x_axis({'name': 'Floors'})
    log_chart.set_x_axis({'name': 'Floors'})
    chart.set_y_axis({'name': 'Spawn Percent', 'major_gridlines': {'visible': False}, 'max': 1, 'log_base': 2})
    log_chart.set_y_axis({'name': 'Spawn Percent', 'major_gridlines': {'visible': False}, 'max': 1})
    chart.set_size({'width': 2560, 'height': 1440})
    log_chart.set_size({'width': 2560, 'height': 1440})
    floor_spawn_rates_sheet.insert_chart(f'A{len(floor_data) + 2}', chart)
    floor_spawn_rates_sheet.insert_chart(f'A134', log_chart)

    # Create Material Hardness Charts
    def create_material_hardness_chart(hardness_sheet, sheet_name, hardness_data):
        chart = writer.book.add_chart({'type': 'line'})
        for char_index in char_range('B', index_to_char_string(len(hardness_data.keys()) + 1)):
            chart.add_series({
                'name':       [sheet_name, 0, char_string_to_index(char_index)],
                'categories': [sheet_name, 1, 0, 16 * 4 + 1, 0],
                'values':     [sheet_name, 1, char_string_to_index(char_index), 16 * 4 + 1, char_string_to_index(char_index)],
                'marker':     {'type': 'circle'},
                'line':       {'width': 5}
            })
        chart.set_title({'name': f'{sheet_name} Hardnesses'})
        chart.set_legend({'position': 'bottom'})
        chart.set_drop_lines()
        chart.set_x_axis({'name': 'Hardness', 'min': 0, 'max': 16, 'interval': 0.25})
        chart.set_y_axis({'name': 'Materials'})
        chart.set_size({'width': 1920, 'height': 1080})
        hardness_sheet.insert_chart(f'A67', chart)
    for hardness_type, hardness_sheet in hardness_sheets.items():
        create_material_hardness_chart(hardness_sheet, hardness_type, hardness_datas[hardness_type])
print('Done')
