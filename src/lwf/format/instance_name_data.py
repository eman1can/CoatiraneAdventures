__all__ = ('InstanceName',)

from lwf.format.string_base import StringBase


class InstanceName(StringBase):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Instance Name <{self.string}>"
