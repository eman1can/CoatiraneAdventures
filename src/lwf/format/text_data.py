__all__ = ('Text',)


class Text:
    def __init__(self):
        self.matrix_id = 0
        self.name_string_id = 0
        self.text_property_id = 0
        self.string_id = 0
        self.color_id = 0
        self.width = 0
        self.height = 0

    def __str__(self):
        return f"Text <Matrix Id: {self.matrix_id}, Name String Id: {self.name_string_id}, Text Property Id: {self.text_property_id}, String Id: {self.string_id}, Color Id: {self.color_id}, Width: {self.width}, Height: {self.height}>"
