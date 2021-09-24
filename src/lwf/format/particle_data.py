__all__ = ('Particle')


class Particle:
    def __init__(self):
        self.matrix_id = 0
        self.color_transform_id = 0
        self.particle_data_id = 0

    def __str__(self):
        return f"Particle <Matrix Id: {self.matrix_id}, CT Id: {self.color_transform_id}, PD Id: {self.particle_data_id}>"
