# UIX Imports
from uix.popups.general import GeneralConfirm
from uix.popups.inspection import Inspection
from uix.popups.inventory import Inventory
from uix.popups.map_options import MapOptions
from uix.popups.skill_tree import PerkInfo, PerkBestow
from uix.screens.almanac import Almanac
from uix.screens.crafting import CraftingMain
from uix.screens.dungeon.result import DungeonResult
from uix.screens.equipment.equipment_change import EquipmentChange, GearChange
from uix.screens.housing.main import HousingMain
from uix.screens.inventory import InventoryMain
from uix.popups.filterable import FilterPopup
from uix.popups.sortable import SortPopup
from uix.popups.tavern import Cancel as TMCancel, Confirm as TMConfirm, NoRecruit as TMNoRecruit, Roll as TMRoll
from uix.popups.dungeon import DungeonConfirm as DMConfirm
from uix.screens.character_display.attributes.attribute_main import CharacterAttributeScreen
from uix.screens.character_display.attributes.status_board import StatusBoardManager
from uix.screens.character_display.character_selector import CharacterSelector
from uix.screens.dungeon.battle import DungeonBattle
from uix.screens.dungeon.main import DungeonMain
from uix.screens.intro.intro_domain import IntroDomain
from uix.screens.intro.intro_news import IntroNews
from uix.screens.intro.intro_start import IntroStart
from uix.screens.intro.intro_select import IntroSelect
from uix.screens.character_display.image_preview import ImagePreview
from uix.screens.intro.start_game import StartGame
from uix.screens.intro.save_select import SaveSelect
from uix.screens.profile.main import ProfileMain
from uix.screens.profile.skill_tree import SkillTreeMain
from uix.screens.quests import QuestsMain
from uix.screens.shop import Shop
from uix.screens.tavern import TavernMain
from uix.screens.tavern.recruit_preview import RecruitPreview
from uix.screens.town import TownMain

SCREEN_LIST = {
    'start_game':       StartGame,
    'save_select':      SaveSelect,
    'intro_start':      IntroStart,
    'intro_domain':     IntroDomain,
    'intro_select':     IntroSelect,
    'intro_news':       IntroNews,
    'town_main':        TownMain,
    'dungeon_main':     DungeonMain,
    'select_char':      CharacterSelector,
    'tavern_main':      TavernMain,
    'inventory_main':   InventoryMain,
    'char_attr_':       CharacterAttributeScreen,
    'recruit_':         RecruitPreview,
    'image_preview_':   ImagePreview,
    'status_board_':    StatusBoardManager,
    'dungeon_battle':   DungeonBattle,
    'dungeon_result':   DungeonResult,
    'gear_change':      GearChange,
    'equipment_change': EquipmentChange,
    'profile_main':     ProfileMain,
    'skill_tree_main':  SkillTreeMain,
    'housing_main':     HousingMain,
    'shop_main':        Shop,
    'crafting_main':    CraftingMain,
    'almanac_main':     Almanac,
    'quests_main':      QuestsMain
}

SCREEN_NON_WHITELIST = ["char_attr_", "status_board_", "image_preview_", "equipment_change_"]

SCREEN_BLACKLIST = ['dungeon_battle', 'dungeon_result']

POPUP_LIST = {
    'confirm':       GeneralConfirm,
    'tm_confirm':    TMConfirm,
    'tm_cancel':     TMCancel,
    'tm_roll':       TMRoll,
    'tm_no_recruit': TMNoRecruit,
    'dm_confirm':    DMConfirm,
    'sort':          SortPopup,
    'filter':        FilterPopup,
    'inventory':     Inventory,
    'map_options':   MapOptions,
    'inspection':    Inspection,
    'perk_info':     PerkInfo,
    'perk_bestow':   PerkBestow
}

POPUP_WHITELIST = [
    'map_options',
    'inventory'
]
