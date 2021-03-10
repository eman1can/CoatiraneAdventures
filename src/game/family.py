class Family:
    def __init__(self):
        self.name = ""
        self.symbol = None
        self.domain = None
        self.score = 0

    def get_rank(self):
        if self.score < 99:
            return 'I'
        elif self.score < 199:
            return 'H'
        elif self.score < 299:
            return 'G'
        elif self.score < 399:
            return 'F'
        elif self.score < 499:
            return 'E'
        elif self.score < 599:
            return 'D'
        elif self.score < 699:
            return 'C'
        elif self.score < 799:
            return 'B'
        elif self.score < 899:
            return 'A'
        else:
            return 'S'

    def get_rank_as_image_path(self):
        return "screens/stats/" + self.get_rank() + ".png"

    def get_name(self):
        return self.name

    def get_display_name(self):
        return self.name + " Family"
