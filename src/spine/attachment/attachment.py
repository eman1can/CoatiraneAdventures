class Attachment:

    def __init__(self, name):

        self.name = None

        if name is None:
            raise Exception("Name cannot be none")
        self.name = name

    def getName(self):
        return self.name

    def __str__(self):
        return self.name
