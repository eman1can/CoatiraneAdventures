__all__ = ('StringBase',)


class StringBase:
    def __init__(self):
        self.string_id = 0

    def __str__(self):
        return f"String Base <String Id: {self.string_id}>"
