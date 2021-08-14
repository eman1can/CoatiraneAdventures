__all__ = ('MovieEventHandlers',)


class MovieEventHandlers:
    LOAD = 0
    POST_LOAD = 1
    UNLOAD = 2
    ENTER_FRAME = 3
    UPDATE = 4
    RENDER = 5
    EVENTS = 6

    def __init__(self):
        self.table = {'load': MovieEventHandlers.LOAD,
                      'postLoad': MovieEventHandlers.POST_LOAD,
                      'unload': MovieEventHandlers.UNLOAD,
                      'enterFrame': MovieEventHandlers.ENTER_FRAME,
                      'update': MovieEventHandlers.UPDATE,
                      'render': MovieEventHandlers.RENDER}
        self._empty = True
        self._handlers = [[] for _ in range(MovieEventHandlers.EVENTS)]

    def clear(self, handler_type=None):
        if handler_type is None:
            for i in range(0, MovieEventHandlers.EVENTS):
                self._handlers[i].clear()
            self._empty = True
        else:
            self._handlers[self.table[handler_type]].clear()
            self._update_empty()

    def add(self, *args):
        if len(args) == 1:
            h = args[0]
            if not h:
                return

            for i in range(0, MovieEventHandlers.EVENTS):
                self._handlers[i] = self._handlers[i] + h._handlers[i]

            if self._empty:
                self._empty = h.empty()
            return None
        else:
            if isinstance(args[1], str):
                event_id, handler_type, h = args
                self.add(self.table[handler_type], {handler_type: h}, None)
                return True
            else:
                event_id, h = args
                for handler_id, handler in h:
                    for handler_type, handler_index in self.table:
                        if handler_id == handler_index:
                            self._handlers[handler_id].append((event_id, handler))

                if self._empty:
                    self._update_empty()
                return None

    def remove(self, handler_id):
        if handler_id < 0:
            return

        for i in range(0, MovieEventHandlers.EVENTS):
            handler_list = self._handlers[i]
            for event_id, handler in handler_list:
                if event_id == handler_id:
                    self._handlers[i].remove((event_id, handler))
        self._update_empty()

    def call(self, handler_type, target):
        for event_id, handler in self._handlers[handler_type]:
            handler(target)

    def _update_empty(self):
        self._empty = True
        for i in range(0, MovieEventHandlers.EVENTS):
            if len(self._handlers[i]) != 0:
                self._empty = False
                break

    def empty(self):
        return self._empty
