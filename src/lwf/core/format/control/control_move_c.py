__all__ = ('ControlMoveC',)


class ControlMoveC:
    def __init__(self):
        self.place_id = 0
        self.color_transform_id = 0

    def __str__(self):
        return f"Control Move C <Place Id: {self.place_id}, Color Transform Id: {self.color_transform_id}>"
