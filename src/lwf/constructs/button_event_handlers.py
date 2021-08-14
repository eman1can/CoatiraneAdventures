__all__ = ('ButtonEventHandlers',)


class ButtonEventHandlers:
    LOAD = 0
    UNLOAD = 1
    ENTER_FRAME = 2
    UPDATE = 3
    RENDER = 4
    PRESS = 5
    RELEASE = 6
    ROLL_OVER = 7
    ROLL_OUT = 8
    KEY_PRESS = 9
    EVENTS = KEY_PRESS

    def __init__(self):
        self.table = {ButtonEventHandlers.LOAD: 0,
                      ButtonEventHandlers.UNLOAD: 1,
                      ButtonEventHandlers.ENTER_FRAME: 2,
                      ButtonEventHandlers.UPDATE: 3,
                      ButtonEventHandlers.RENDER: 4,
                      ButtonEventHandlers.PRESS: 5,
                      ButtonEventHandlers.RELEASE: 6,
                      ButtonEventHandlers.ROLL_OVER: 7,
                      ButtonEventHandlers.ROLL_OUT: 8}
        self._empty = True
        self._handlers = [[] for _ in range(ButtonEventHandlers.EVENTS)]
        self._key_press_handler = []

    def clear(self, handler_type=None):
        if handler_type is None:
            for i in range(0, ButtonEventHandlers.EVENTS):
                self._handlers[i].clear()
            self._key_press_handler.clear()
            self._empty = True
        else:
            if handler_type == ButtonEventHandlers.KEY_PRESS:
                self._key_press_handler.clear()
            else:
                self._handlers[self.table[handler_type]].clear()
            self._update_empty()

    def add(self, *args):
        if len(args) == 1:
            h = args[0]
            if not h:
                return

            for i in range(0, ButtonEventHandlers.EVENTS):
                self._handlers[i] = self._handlers[i] + h._handlers[i]
            self._key_press_handler = self._key_press_handler + h._key_press_handler

            if self._empty:
                self._empty = h.empty()
            return None
        else:
            if isinstance(args[1], str):
                event_id, handler_type, h = args
                self.add(self.table[handler_type], {handler_type: h}, None)
                return True
            else:
                event_id, h, kh = args
                for handler_id, handler in h:
                    for handler_type, handler_index in self.table:
                        if handler_id == handler_index:
                            self._handlers[handler_id].append((event_id, handler))
                if kh:
                    self._key_press_handler.append((event_id, kh))

                if self._empty:
                    self._update_empty()
                return None

    def remove(self, handler_id):
        if handler_id < 0:
            return

        for i in range(0, ButtonEventHandlers.EVENTS):
            handler_list = self._handlers[i]
            for event_id, handler in handler_list:
                if event_id == handler_id:
                    self._handlers[i].remove((event_id, handler))
        for event_id, handler in self._key_press_handler:
            if event_id == handler_id:
                self._key_press_handler.remove((event_id, handler))
        self._update_empty()

    def call(self, handler_type, target):
        for event_id, handler in self._handlers[handler_type]:
            handler(target)

    def call_key_press(self, target, code):
        for event_id, handler in self._key_press_handler:
            handler(target, code)

    def _update_empty(self):
        self._empty = True
        for i in range(0, ButtonEventHandlers.EVENTS):
            if len(self._handlers[i]) != 0:
                self._empty = False
                break
        if self._empty:
            self._empty = len(self._key_press_handler) == 0

    def empty(self):
        return self._empty
