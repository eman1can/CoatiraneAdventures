class Event:

    def __init__(self, data):

        self.data = None
        self.intValue = 0
        self.floatValue = 0.0
        self.stringValue = None

        self.data = data

    def getInt(self):
        return self.intValue

    def setInt(self, intValue):
        self.intValue = intValue

    def getFloat(self):
        return self.floatValue

    def setFloat(self, floatValue):
        self.floatValue = floatValue

    def getString(self, stringValue):
        return self.stringValue

    def setString(self, stringValue):
        self.stringValue = stringValue

    def getData(self):
        return self.data

    def __str__(self):
        return self.data.name
