__all__ = ('ParticleData',)


class ParticleData:
    def __init__(self):
        self.string_id = 0

    def __str__(self):
        return f"ParticleData <String Id: {self.string_id}>"
