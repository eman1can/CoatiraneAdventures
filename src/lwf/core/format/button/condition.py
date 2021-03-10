__all__ = ('ButtonCondition',)


class ButtonCondition:
    class Condition:
        ROLL_OVER = (1 << 0)
        ROLL_OUT = (1 << 1)
        PRESS = (1 << 2)
        RELEASE = (1 << 3)
        DRAG_OUT = (1 << 4)
        DRAG_OVER = (1 << 5)
        RELEASE_OUTSIDE = (1 << 6)
        KEY_PRESS = (1 << 7)

    def __init__(self):
        self.condition = 0
        self.key_code = 0
        self.animation_id = 0

    def __str__(self):
        if self.condition == ButtonCondition.Condition.ROLL_OVER:
            condition = 'RollOver'
        elif self.condition == ButtonCondition.Condition.ROLL_OUT:
            condition = 'RollOut'
        elif self.condition == ButtonCondition.Condition.PRESS:
            condition = 'Press'
        elif self.condition == ButtonCondition.Condition.RELEASE:
            condition = 'Release'
        elif self.condition == ButtonCondition.Condition.DRAG_OUT:
            condition = 'DragOut'
        elif self.condition == ButtonCondition.Condition.DRAG_OVER:
            condition = 'DragOver'
        elif self.condition == ButtonCondition.Condition.RELEASE_OUTSIDE:
            condition = 'Release Outside'
        else:
            condition = 'Key Press'
        return f"Button Condition <Condition: {condition}, Key Code: {self.key_code}, Animation Id:{self.animation_id}>"
