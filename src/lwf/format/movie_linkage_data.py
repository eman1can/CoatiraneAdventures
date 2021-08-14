__all__ = ('MovieLinkage',)

from lwf.format.string_base import StringBase


class MovieLinkage(StringBase):
    def __init__(self):
        super().__init__()
        self.movie_id = 0

    def __str__(self):
        return f"Movie Linkage <Movie Id: {self.movie_id}, StringId: {self.string}>"
