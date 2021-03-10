__all__ = ('Control', 'ControlMoveM', 'ControlMoveC', 'ControlMoveMC', 'ControlMoveMCB',)

from .control_move_m import ControlMoveM
from .control_move_c import ControlMoveC
from .control_move_mc import ControlMoveMC
from .control_move_mcb import ControlMoveMCB


class Control:
    MOVE = 0
    MOVE_M = 1
    MOVE_C = 2
    MOVE_MC = 3
    ANIMATION = 4
    MOVE_MCB = 5
    CONTROL_MAX = 6

    def __init__(self):
        self.control_type = 0
        self.control_id = 1

    def __str__(self):
        if self.control_type == Control.MOVE:
            control_type = 'Move'
        elif self.control_type == Control.MOVE_M:
            control_type = 'Move m'
        elif self.control_type == Control.MOVE_C:
            control_type = 'Move c'
        elif self.control_type == Control.MOVE_MC:
            control_type = 'Move mc'
        elif self.control_type == Control.ANIMATION:
            control_type = 'Animation'
        else:
            control_type = 'Move mcb'
        return f"Control <Type: {control_type}, Id: {self.control_id}>"
