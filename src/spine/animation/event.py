class Event:
    def __init__(self, name):
        assert(name is not None, "Name cannot be None")
        self.name = name
        self.intValue = 0
        self.floatValue = 0.0
        self.stringValue = None

    def getInt(self):
        return self.intValue

    def setInt(self, intValue):
        self.intValue = intValue

    def getFloat(self):
        return self.floatValue

    def setFloat(self, floatValue):
        self.floatValue = floatValue

    def getString(self):
        return self.stringValue

    def setString(self, stringValue):
        self.stringValue = stringValue

    def getName(self):
        return self.name

    def __str__(self):
        return self.name
