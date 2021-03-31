BACK = 'back'

GAME_LOADING = 'game_loading'

NEW_GAME            = 'new_game'
SAVE_SELECT         = 'new_game.save_select'
INTRO_DOMAIN        = 'new_game.intro_domain'
INTRO_DOMAIN_NAME   = 'new_game.intro_domain_name'
INTRO_DOMAIN_GENDER = 'new_game.intro_domain_gender'
INTRO_SELECT        = 'new_game.intro_select'
INTRO_NEWS          = 'new_game.intro_news'

TOWN_MAIN                  = 'town'
PROFILE_MAIN               = 'town.profile'
SKILL_TREE_MAIN            = 'town.skill_tree'
PERK_INFO                  = 'town.skill_tree.perk_info'
PERK_BESTOW                = 'town.skill_tree.perk_bestow'
QUESTS_MAIN                = 'town.quests'
TAVERN_MAIN                = 'town.tavern'
TAVERN_RELAX               = 'town.tavern.relax'
TAVERN_CHAT                = 'town.tavern.chat'
TAVERN_RECRUIT             = 'town.tavern.recruit'
TAVERN_RECRUIT_SHOW        = 'town.tavern.recruit_show'
SHOP_MAIN                  = 'town.shop'
HOUSING_MAIN               = 'town.housing'
HOUSING_BROWSE             = 'town.housing.browse'
HOUSING_BUY                = 'town.housing.buy'
HOUSING_RENT               = 'town.housing.rent'
CRAFTING_MAIN              = 'town.crafting'
CRAFTING_PROCESS_MATERIALS = 'town.crafting.process_materials'
CRAFTING_ALLOYS            = 'town.crafting.alloys'
CRAFTING_ITEMS             = 'town.crafting.items'
CRAFTING_EQUIPMENT         = 'town.crafting.equipment'
CRAFTING_POTIONS           = 'town.crafting.potions'
CRAFT_ITEM_MULTIPLE        = 'town.crafting.craft_item_multiple'
CRAFT_EQUIPMENT            = 'town.crafting.craft_equipment'
ALMANAC_MAIN               = 'town.almanac'

CHARACTER_ATTRIBUTE     = 'character_attributes'
CHARACTER_SELECTION     = 'character_attributes.select_character'
STATUS_BOARD            = 'character_attributes.status_board'
STATUS_BOARD_UNLOCK     = 'character_attributes.status_board_unlock'
STATUS_BOARD_VIEW_FALNA = 'character_attributes.status_board_view_falna'
CHANGE_EQUIP            = 'character_attributes.change_equip'
CHANGE_EQUIP_ITEM       = 'character_attributes.change_equip_item'

INVENTORY               = 'inventory'
INVENTORY_BATTLE        = 'inventory.battle'
INVENTORY_BATTLE_SELECT = 'inventory.battle_select'

DUNGEON_MAIN              = 'dungeon'
DUNGEON_MAIN_LOCKED       = 'dungeon.locked'
DUNGEON_CONFIRM           = 'dungeon.confirm'
DUNGEON_BATTLE            = 'dungeon.battle'
MAP_OPTIONS               = 'dungeon.map_options'
DUNGEON_RESULT            = 'dungeon.result'
DUNGEON_RESOURCE_RESULT   = 'dungeon.resource_result'
DUNGEON_HARVEST_RESULT    = 'dungeon.result_harvest'
DUNGEON_EXPERIENCE_RESULT = 'dungeon.result_experience'


# Screen Template
'''
from refs import END_OPT_C, OPT_C
from text.screens.screen_names import BACK


def get_screen(console, screen_data):
    display_text, _options = '', {'0': BACK}
    console.header_callback = None
    
    display_text = '\n\tThis screen is not implemented!\n'
    
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options


def handle_action(console, action):
    console.set_screen(action)

'''