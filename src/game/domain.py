class Domain:
    def __init__(self, title, description, small_description):
        self.title = title
        self.description = description
        self.small_description = small_description
        self.effects = []

    def get_title(self):
        return self.title

    def get_small_description(self):
        return self.small_description

    def get_large_description(self):
        return self.description
