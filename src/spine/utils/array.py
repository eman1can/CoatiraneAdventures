class Array:

    def __init__(self, *args):

        self.items = None
        self.size = 0
        self.ordered = False

        if len(args) == 0:
            ordered, capacity = True, 16
        elif len(args) == 1:
            ordered, capacity = True, args[0]
        else:
            ordered, capacity = args[0], args[1]
        self.ordered = ordered
        self.items = [None for _ in range(capacity)]

    def __len__(self):
        return self.size

    def __str__(self):
        return f'<{self.items}>'

    def add(self, value):
        if self.size + 1 >= len(self.items):
            self.resize(max(8, int(self.size * 1.75)))
        self.items[self.size] = value
        self.size += 1

    def addAll(self, array):
        for item in array:
            self.add(item)

    def get(self, index):
        if index >= self.size:
            raise Exception(f"index can't be >= size: {index} >= {self.size}")
        return self.items[index]

    def set(self, index, value):
        if index >= self.size:
            raise Exception(f"index can't be >= size: {index} >= {self.size}")
        self.items[index] = value

    def insert(self, index, value):
        if index >= self.size:
            raise Exception(f"index can't be >= size: {index} >= {self.size}")
        if self.size == len(self.items):
            self.resize(max(8, self.size * 1.75))
        if self.ordered:
            self.items[index+1:self.size+1] = self.items[index:self.size]
        else:
            self.items[self.size] = self.items[index]
        self.size += 1
        self.items[index] = value

    def __contains__(self, item):
        return item in self.items

    def index(self, item, start, stop):
        return self.items.index(item, start, stop)

    def removeValue(self, value):
        self.removeIndex(self.index(value))

    def removeIndex(self, index):
        if index >= self.size:
            raise Exception(f"index cannot be >= size: {index} >= {self.size}")
        value = self.items[index]
        self.size -= 1
        if self.ordered:
            self.items[index:self.size - 1] = self.items[index+1:self.size]
        else:
            self.items[index] = self.items[self.size]
        self.items[self.size] = None
        return value

    def pop(self):
        if self.size == 0:
            raise Exception("Array is Empty")
        self.size -= 1
        item = self.items[self.size]
        self.items[self.size] = None
        return item

    def peek(self):
        if self.size == 0:
            raise Exception("Array is Empty")
        return self.items[self.size - 1]

    def first(self):
        if self.size == 0:
            raise Exception("Array is Empty")
        return self.items[0]

    def isEmpty(self):
        return self.size == 0

    def clear(self):
        for x in range(self.size):
            self.items[x] = None
        self.size = 0

    def sort(self):
        post = self.items[self.size:]
        pre = self.items[:self.size].sort()
        self.items = pre + post

    def ensureCapacity(self, additionalCapacity):
        if additionalCapacity < 0:
            raise Exception("additionalCapacity must be > 0")
        sizeNeeded = self.size + additionalCapacity
        if sizeNeeded > len(self.items):
            self.resize(max(8, sizeNeeded))
        return self.items

    def resize(self, newSize):
        newItems = self.items + [0 for x in range(newSize - self.size)]
        self.items = newItems
        return newItems
