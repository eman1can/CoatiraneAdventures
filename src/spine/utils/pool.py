MIN_VALUE = -2147483648
MAX_VALUE = 2147483647

from src.spine.utils.array import Array


class Poolable:
    def reset(self):
        pass


class Pool:

    def new_object(self):
        pass

    def __init__(self, *args):
        self.max = MAX_VALUE
        self.peak = 0
        self.free_objects = Array(False, 16)

    def obtain(self):
        return self.new_object() if len(self.free_objects) == 0 else self.free_objects.pop()

    def free(self, obj):
        assert(obj is not None, "Object to free cannot be None")
        if len(self.free_objects) < self.max:
            self.free_objects.add(obj)
            self.peak = max(self.peak, len(self.free_objects))
        self.reset(obj)

    def reset(self, obj):
        if isinstance(obj, Poolable):
            obj.reset()

    def free_all(self, objects):
        assert(objects is not None, 'Objects to free cannot be None')
        for obj in objects:
            if len(self.free_objects) < self.max:
                self.free_objects.add(obj)
            self.reset(obj)
        self.peak = max(self.peak, len(self.free_objects))

    def clear(self):
        self.free_objects.clear()

    def get_free(self):
        return len(self.free_objects)
