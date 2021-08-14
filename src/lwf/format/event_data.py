__all__ = ('Event',)

from lwf.format.string_base import StringBase


class Event(StringBase):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Event <{self.string}>"
