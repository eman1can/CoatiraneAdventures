__all__ = ('ControlMoveMCB',)


class ControlMoveMCB:
    def __init__(self):
        self.place_id = 0
        self.matrix_id = 0
        self.color_transform_id = 0
        self.blend_mode = 0

    def __str__(self):
        return f"Control Move MCB <Place Id: {self.place_id}, Matrix Id: {self.matrix_id}, Color Transform Id: {self.color_transform_id}, Blend Mode: {self.blend_mode}>"
