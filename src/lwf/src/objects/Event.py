class EventHandler(Action):
    pass


class EventHandlers(Dictionary):
    pass


class EventHandlerDictionary(Dictionary):
    pass




class CalculateBoundsCallbacks(SortedList):
    pass


class ButtonEventHandler(Action):
    pass


class ButtonKeyPressHandler(Action):
    pass


class ButtonEventHandlerDictionary(Dictionary):
    pass


class ButtonKeyPressHandlerDictionary(Dictionary):
    pass


class GenericEventHandlerDictionary(Dictionary):
    pass





class ButtonEventHandlersDictionary(Dictionary):
    pass

class ButtonEventHandlers:
    class Type(Enum):
        LOAD = 0
        UNLOAD = 1
        ENTERFRAME = 2
        UPDATE = 3
        RENDER = 4
        PRESS = 5
        RELEASE = 6
        ROLLOVER = 7
        KEYPRESS = 8

    load = None
    unload = None
    enterFrame = None
    update = None
    render = None
    press = None
    release = None
    rollOver = None
    rollOut = None
    keyPress = None

    def __init__(self):
        self.load = ButtonEventHandlerDictionary()
        self.unload = ButtonEventHandlerDictionary()
        self.enterFrame = ButtonEventHandlerDictionary()
        self.update = ButtonEventHandlerDictionary()
        self.render = ButtonEventHandlerDictionary()
        self.press = ButtonEventHandlerDictionary()
        self.release = ButtonEventHandlerDictionary()
        self.rollOver = ButtonEventHandlerDictionary()
        self.rollOut = ButtonEventHandlerDictionary()
        self.keyPress = ButtonKeyPressHandlerDictionary()

    def Clear(self, *args):
        if len(args) is 0:
            self.load.clear()
            self.unload.clear()
            self.enterFrame.clear()
            self.update.clear()
            self.render.clear()
            self.press.clear()
            self.release.clear()
            self.rollOver.clear()
            self.rollOut.clear()
            self.keyPress.clear()
        else:
            if args[0] == ButtonEventHandlers.Type.LOAD.value:
                self.load.clear()
            elif args[0] == ButtonEventHandlers.Type.UNLOAD.value:
                self.unload.clear()
            elif args[0] == ButtonEventHandlers.Type.RENDER.value:
                self.render.clear()
            elif args[0] == ButtonEventHandlers.Type.PRESS.value:
                self.press.clear()
            elif args[0] == ButtonEventHandlers.Type.RELEASE.value:
                self.release.clear()
            elif args[0] == ButtonEventHandlers.Type.ROLLOVER.value:
                self.rollOver.clear()
            elif args[0] == ButtonEventHandlers.Type.ROLLOUT.value:
                self.rollOut.clear()
            elif args[0] == ButtonEventHandlers.Type.KEYPRESS.value:
                self.keyPress.clear()

    def Add(self, arg, load=None, u=None, e=None, up=None, r=None, p=None, rl=None, rOver=None, rOut=None, k=None):
        if not isinstance(arg, int):
            handlers = arg
            if handlers is None:
                return

            for hk, hv in handlers.load:
                self.load.set(hk, hv)
            for hk, hv in handlers.unload:
                self.unload.set(hk, hv)
            for hk, hv in handlers.enterFrame:
                self.enterFrame.set(hk, hv)
            for hk, hv in handlers.update:
                self.update.set(hk, hv)
            for hk, hv in handlers.render:
                self.render.set(hk, hv)
            for hk, hv in handlers.press:
                self.press.set(hk, hv)
            for hk, hv in handlers.release:
                self.release.set(hk, hv)
            for hk, hv in handlers.rollOver:
                self.rollOver.set(hk, hv)
            for hk, hv in handlers.rollOut:
                self.rollOut.set(hk, hv)
            for hk, hv in handlers.keyPress:
                self.keyPress.set(hk, hv)
        else:
            key = arg
            if load is not None:
                self.load.set(key, load)
            if u is not None:
                self.unload.set(key, u)
            if e is not None:
                self.enterFrame.set(key, e)
            if up is not None:
                self.update.set(key, up)
            if r is not None:
                self.render.set(key, r)
            if p is not None:
                self.press.set(key, p)
            if rl is not None:
                self.release.set(key, rl)
            if rOver is not None:
                self.rollOver.set(key, rOver)
            if rOut is not None:
                self.rollOut.set(key, rOut)
            if k is not None:
                self.keyPress.set(key, k)

    def Remove(self, key):
        self.load.remove(key)
        self.unload.remove(key)
        self.enterFrame.remove(key)
        self.update.remove(key)
        self.render.remove(key)
        self.press.remove(key)
        self.release.remove(key)
        self.rollOver.remove(key)
        self.rollOut.remove(key)
        self.keyPress.remove(key)

    def Call(self, buttonType, target):
        dictionary = None
        if buttonType == ButtonEventHandlers.Type.LOAD.value:
            dictionary = self.load
        elif buttonType == ButtonEventHandlers.Type.UNLOAD.value:
            dictionary = self.unload
        elif buttonType == ButtonEventHandlers.Type.RENDER.value:
            dictionary = self.render
        elif buttonType == ButtonEventHandlers.Type.PRESS.value:
            dictionary = self.press
        elif buttonType == ButtonEventHandlers.Type.RELEASE.value:
            dictionary = self.release
        elif buttonType == ButtonEventHandlers.Type.ROLLOVER.value:
            dictionary = self.rollOver
        elif buttonType == ButtonEventHandlers.Type.ROLLOUT.value:
            dictionary = self.rollOut
        if dictionary is not None:
            dictionary = ButtonEventHandlerDictionary(dictionary)
            for k, v in dictionary.items():
                v(target)

    def CallKEYPRESS(self, target, code):
        dictionary = ButtonKeyPressHandlerDictionary(self.keyPress)
        for k, v in dictionary.items():
            v(target, code)

