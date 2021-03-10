__all__ = ('Font',)


class Font:
    def __init__(self):
        self.string_id = 0
        self.letter_spacing = 0.0

    def __str__(self):
        return f"Font <String Id: {self.string_id}, Letter Spacing: {self.letter_spacing}>"
