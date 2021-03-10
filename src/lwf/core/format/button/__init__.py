__all__ = ('Button', 'ButtonCondition',)

from .condition import ButtonCondition


class Button:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.matrix_id = 0
        self.color_transform_id = 0
        self.condition_id = 0
        self.conditions = 0

    def __str__(self):
        return f"Button <Width: {self.width}, Height: {self.height}, Matrix Id: {self.matrix_id}, CT Id: {self.color_transform_id}, Condition Id: {self.condition_id}, Conditions: {self.conditions}>"
