MIN_VALUE = -2147483648
MAX_VALUE = 2147483647

from src.spine.utils.array import Array


class Poolable:
    def reset(self):
        pass


class Pool:

    def newObject(self):
        pass

    def __init__(self, *args):

        self.max = 0
        self.peak = 0

        self.freeObjects = None

        if len(args) == 0:
            initialCapacity, maximum = 16, MAX_VALUE
        elif len(args) == 1:
            initialCapacity, maximum = args[0], MAX_VALUE
        elif len(args) == 2:
            initialCapacity, maximum = args[1], args[2]
        else:
            initialCapacity, maximum = args[0], args[1]

        self.freeObjects = Array(False, initialCapacity)
        self.max = maximum

    def obtain(self):
        return self.newObject() if len(self.freeObjects) == 0 else self.freeObjects.pop()

    def free(self, object):
        if object is None:
            raise Exception("object cannot be None")
        if len(self.freeObjects) < self.max:
            self.freeObjects.add(object)
            self.peak = max(self.peak, len(self.freeObjects))
        self.reset(object)

    def reset(self, object):
        if isinstance(object, Poolable):
            object.reset()

    def freeAll(self, objects):
        if objects is None:
            raise Exception("Objects cannot be None")
        for i in range(len(objects)):
            object = objects[i]
            if object is None:
                continue
            if len(self.freeObjects) < self.max:
                self.freeObjects.add(object)
            self.reset(object)
        self.peak = max(self.peak, len(self.freeObjects))

    def clear(self):
        self.freeObjects.clear()

    def getFree(self):
        return len(self.freeObjects)
