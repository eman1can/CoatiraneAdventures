__all__ = ('ControlMoveMC',)


class ControlMoveMC:
    def __init__(self):
        self.place_id = 0
        self.matrix_id = 0
        self.color_transform_id = 0

    def __str__(self):
        return f"Control Move MC <Place Id: {self.place_id}, Matrix Id: {self.matrix_id}, Color Transform Id: {self.color_transform_id}>"
