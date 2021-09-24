__all__ = ('Control', 'ControlMoveM', 'ControlMoveC', 'ControlMoveMC', 'ControlMoveMCB')


MOVE = 0
MOVE_M = 1
MOVE_C = 2
MOVE_MC = 3
ANIMATION = 4
MOVE_MCB = 5
CONTROL_MAX = 6


TO_STRING = {
    MOVE: 'Move',
    MOVE_M: 'Move Matrix',
    MOVE_C: 'Move Color',
    MOVE_MC: 'Move Matrix, Color',
    ANIMATION: 'Animation',
    MOVE_MCB: 'Move Matrix, Color, Blend'
}


class Control:
    def __init__(self):
        self.control_type = 0
        self.control_id = 1

    def __str__(self):
        control_type = TO_STRING[self.control_type]
        return f"Control <Type: {control_type}, Id: {self.control_id}>"


class ControlMoveM:
    def __init__(self):
        self.place_id = 0
        self.matrix_id = 0

    def __str__(self):
        return f"Control Move M <Place Id: {self.place_id}, Matrix Id: {self.matrix_id}>"


class ControlMoveC:
    def __init__(self):
        self.place_id = 0
        self.color_transform_id = 0

    def __str__(self):
        return f"Control Move C <Place Id: {self.place_id}, Color Transform Id: {self.color_transform_id}>"


class ControlMoveMC:
    def __init__(self):
        self.place_id = 0
        self.matrix_id = 0
        self.color_transform_id = 0

    def __str__(self):
        return f"Control Move MC <Place Id: {self.place_id}, Matrix Id: {self.matrix_id}, Color Transform Id: {self.color_transform_id}>"


class ControlMoveMCB:
    def __init__(self):
        self.place_id = 0
        self.matrix_id = 0
        self.color_transform_id = 0
        self.blend_mode = 0

    def __str__(self):
        return f"Control Move MCB <Place Id: {self.place_id}, Matrix Id: {self.matrix_id}, Color Transform Id: {self.color_transform_id}, Blend Mode: {self.blend_mode}>"
