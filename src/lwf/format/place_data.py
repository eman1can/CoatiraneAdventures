__all__ = ('Place',)


class Place:
    def __init__(self):
        self.depth = 0
        self.object_id = 0
        self.instance_id = 0
        self.matrix_id = 0
        self.blend_mode = 0

    def __str__(self):
        return f"Place <Depth: {self.depth}, Object Id: {self.object_id}, Instance Id: {self.instance_id}, Matrix Id: {self.matrix_id}, Blend Mode: {self.blend_mode}"
