__all__ = ('PlaceCompat',)


class PlaceCompat:
    def __init__(self):
        self.depth = 0
        self.object_id = 0
        self.instance_id = 0
        self.matrix_id = 0

    def __str__(self):
        return f"PlaceCompat <Depth={self.depth}, Object Id={self.object_id}, Instance Id={self.instance_id}, Matrix Id={self.matrix_id}>"
