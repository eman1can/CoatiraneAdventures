__all__ = ('ControlMoveM',)


class ControlMoveM:
    def __init__(self):
        self.place_id = 0
        self.matrix_id = 0

    def __str__(self):
        return f"Control Move M <Place Id: {self.place_id}, Matrix Id: {self.matrix_id}>"
