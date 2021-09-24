__all__ = ('Event',)

from .string.base import StringBase


class Event(StringBase):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Event <{super().__str__()}>"
