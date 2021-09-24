__all__ = ('ButtonCondition',)

ROLL_OVER = 1
ROLL_OUT = 2
PRESS = 4
RELEASE = 8
DRAG_OUT = 16
DRAG_OVER = 32
RELEASE_OUTSIDE = 64
KEY_PRESS = 128

TO_STRING = {
    ROLL_OVER: 'Roll Over',
    ROLL_OUT: 'Roll Out',
    PRESS: 'Press',
    RELEASE: 'Release',
    DRAG_OUT: 'Drag Out',
    DRAG_OVER: 'Drag Over',
    RELEASE_OUTSIDE: 'Release Outside',
    KEY_PRESS: 'Key Press',
}


class ButtonCondition:
    def __init__(self):
        self.condition = 0
        self.key_code = 0
        self.animation_id = 0

    def __str__(self):
        return f"Button Condition <Condition: {TO_STRING[self.condition]}, Key Code: {self.key_code}, Animation Id:{self.animation_id}>"
