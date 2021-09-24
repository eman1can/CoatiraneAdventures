__all__ = ('ParticleData',)

from lwf.format.string_base import StringBase


class ParticleData(StringBase):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"ParticleData <String Id: {self.string}>"
