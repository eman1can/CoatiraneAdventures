__all__ = ('InstanceName',)

from src.lwf.core.format.string.base import StringBase


class InstanceName(StringBase):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Instance Name <{super().__str__()}>"
