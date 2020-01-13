# Internal Imports
from .utils.Type import Action, Dictionary

# External Imports
from typing import List


class DetachHandler(Action):
    pass


class Inspector(Action):
    pass


class AllowButtonList(Dictionary):
    pass


class DenyButtonList(Dictionary):
    pass


class ExecHandler(Action):
    pass


class ExecHandlerList(List):
    pass


class BlendModes(List):
    pass


class MaskModes(List):
    pass
