# Internal Imports
# External Imports
from typing import List

from .utils.Type import Action, Dictionary


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
