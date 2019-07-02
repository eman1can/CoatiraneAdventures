class AnimationStateData:
    self.skeletonData = None


class ObjectFloatMap:
    def __init__(self):
        self.PRIME1 = 0xbe1f14b1
        self.PRIME2 = 0xb4b82e39
        self.PRIME3 = 0xced1c241

        self.size = 0

        self.keyTable = []

        self.loadFactor = 0.0
        self.hashShift, self.mask, self.threshold = 0, 0, 0
        self.stashCapacity = 0
        self.pushIterations = 0

        self.entries1, self.entries2 = None, None

class Entries(MapIterator):


    def __init__(self, map):
        self.entry = Entry()
        super(MapIterator, self).__init__(map)

    def next(self):
        if not self.hasNext:
            raise Exception("No such element!")
        if not self.valid:
            raise Exception("Iterator() cannot be used nested")
        keyTable = self.map.keyTable
        self.entry.key = keyTable[self.nextIndex]
        self.entry.value = map.valueTable[self.nextIndex]
        self.currentIndex = self.nextIndex
        self.findNextIndex()
        return self.entry

    def hasNext(self):
        if not self.valid:
            raise Exception("Iterator() cannot be used nested")
        return self.hasNext

    def iterator(self):
        return self

    def remove(self):
        super.remove()

class Values(MapIterator):
    def __init__(self, map):
        super(Values, self).__init__(map)

    def hasNext(self):
        if not self.valid:
            raise Exception("Iterator cannot be used nested")
        return self.hasNext

    def next(self):
        if not self.hasNext:
            raise Exception("No such element exception")
        if not self.valid:
            raise Exception("Iterator cannot be used nested")
        value = self.map.valueTable[self.nextIndex]
        self.currentIndex = self.nextIndex
        self.findNextIndex()
        return value

    def toArray(self):
        array = []
        while self.hasNext():
            array.append(self.next())
        return array

class Keys(MapIterator):
    def __init__(self, map):
        super(Keys, self).__init__(map)

    def hasNext(self):
        if not valid:
            raise Exception("Iterator cannot be used nested")
        return self.hasNext

    def next(self):
        if not self.hasNext:
            raise Exception("No such element exception")
        if not self.valid:
            raise Exception("Iterator cannot be used nested")
        key = self.map.keyTable[self.nextIndex]
        self.currentIndex = self.nextIndex
        self.findNextIndex()
        return key

    def iterator(self):
        return self

    def toArray(self):
        array = []
        while self.hasNext():
            array.append(self.next())
        return array

    def addToArray(self, array):
        while self.hasNext():
            array.append(self.next())
        return array

    def remove(self):
        super.remove()

class MapIterator():

    def __init__(self, map):
        self.hasNext = False
        self.nextIndex, self.currentIndex = 0, 0
        self.valid = True
        self.map = map
        self.reset()

    def reset(self):
        self.currentIndex = -1
        self.nextIndex = -1
        self.findNextIndex()

    def findNextIndex(self):
        self.hasNext = False
        keytable = self.map.keyTable
        n = self.map.capacity + self.map.stashSize
        while self.nextIndex < n:
            if keyTable[self.nextIndex] is not None:
                self.hasNext = True
                break
            self.nextIndex += 1

    def remove(self):
        if self.currentIndex < 0:
            raise Exception("Next must be called before remove")
        if self.currentIndex >= self.map.capacity:
            self.map.removeStashIndex(self.currentIndex)
            self.nextIndex = self.currentIndex - 1
            self.findNextIndex()
        else:
            self.map.keyTable[self.currentindex] = None

        self.currentIndex = -1
        self.map.size -= 1

class Entry():
    def __init__(self):
        self.key = None
        self.value = 0.0

    def toString(self):
        return str(self.key) + "=" + str(self.value)

