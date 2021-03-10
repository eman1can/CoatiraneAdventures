__all__ = ('Animation',)


class Animation:
    END = 0
    PLAY = 1
    STOP = 2
    NEXT_FRAME = 3
    PREV_FRAME = 4
    GOTO_FRAME = 5
    GOTO_LABEL = 6
    SET_TARGET = 7
    EVENT = 8
    CALL = 9
    INSTANCE_TARGET_ROOT = -1
    INSTANCE_TARGET_PARENT = -2
