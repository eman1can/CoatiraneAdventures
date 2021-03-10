# UIX Imports
from uix.popups.filterable import FilterPopup
from uix.popups.sortable import SortPopup
from uix.popups.tavern import Cancel as TMCancel, Confirm as TMConfirm, NoRecruit as TMNoRecruit, Roll as TMRoll
from uix.popups.dungeon import Confirm as DMConfirm
from uix.screens.character_display.attributes.attribute_main import CharacterAttributeScreen
from uix.screens.character_display.attributes.status_board import StatusBoardManager
from uix.screens.character_display.character_selector import CharacterSelector
from uix.screens.dungeon.battle import DungeonBattle
from uix.screens.dungeon.main import DungeonMain
from uix.screens.family.domain import FamilyDomain
from uix.screens.family.intro import FamilyIntro
from uix.screens.family.select import SelectScreen
from uix.screens.image_preview import ImagePreview
from uix.screens.pre_game.new_game import NewGameScreen
from uix.screens.pre_game.select_save import SelectSaveScreen
from uix.screens.tavern import TavernMain
from uix.screens.tavern.recruit_preview import RecruitPreview
from uix.screens.town import TownScreen


SCREEN_LIST = {'new_game': NewGameScreen,
               'select_save': SelectSaveScreen,
               'intro_start': FamilyIntro,
               'intro_domain': FamilyDomain,
               'select_start': SelectScreen,
               'town_main': TownScreen,
               'dungeon_main': DungeonMain,
               'select_char': CharacterSelector,
               'tavern_main': TavernMain,
               'char_attr_': CharacterAttributeScreen,
               'recruit_': RecruitPreview,
               'image_preview_': ImagePreview,
               'status_board_': StatusBoardManager,
               'dungeon_battle': DungeonBattle}

SCREEN_NON_WHITELIST = ["char_attr_", "status_board_", "image_preview_", "equipment_change_"]

SCREEN_WHITELIST = ['select_char', 'dungeon_main', 'town_main', 'tavern_main']

POPUP_LIST = {'tm_confirm': TMConfirm,
              'tm_cancel': TMCancel,
              'tm_roll': TMRoll,
              'tm_no_recruit': TMNoRecruit,
              'dm_confirm': DMConfirm,
              'sort': SortPopup,
              'filter': FilterPopup}

POPUP_WHITELIST = []
