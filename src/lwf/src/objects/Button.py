# Internal Imports
from ..utils.Type import Matrix, Action, Dictionary
from ..utils.Utility import Utility
from ..utils.Constants import INT32_MINVALUE
from ..Format import Format
from .Object import IObject


class ButtonEventHandler(Action):
    pass


class ButtonKeyPressHandler(Action):
    pass


class ButtonEventHandlerDictionary(Dictionary):
    pass


class ButtonKeyPressHandlerDictionary(Dictionary):
    pass


class ButtonEventHandlersDictionary(Dictionary):
    pass


class ButtonEventHandlers:
    class Type:
        LOAD = 0
        UNLOAD = 1
        ENTERFRAME = 2
        UPDATE = 3
        RENDER = 4
        PRESS = 5
        RELEASE = 6
        ROLLOVER = 7
        ROLLOUT = 8
        KEYPRESS = 9

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
            if args[0] == ButtonEventHandlers.Type.LOAD:
                self.load.clear()
            elif args[0] == ButtonEventHandlers.Type.UNLOAD:
                self.unload.clear()
            elif args[0] == ButtonEventHandlers.Type.RENDER:
                self.render.clear()
            elif args[0] == ButtonEventHandlers.Type.PRESS:
                self.press.clear()
            elif args[0] == ButtonEventHandlers.Type.RELEASE:
                self.release.clear()
            elif args[0] == ButtonEventHandlers.Type.ROLLOVER:
                self.rollOver.clear()
            elif args[0] == ButtonEventHandlers.Type.ROLLOUT:
                self.rollOut.clear()
            elif args[0] == ButtonEventHandlers.Type.KEYPRESS:
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
        if buttonType == ButtonEventHandlers.Type.LOAD:
            dictionary = self.load
        elif buttonType == ButtonEventHandlers.Type.UNLOAD:
            dictionary = self.unload
        elif buttonType == ButtonEventHandlers.Type.RENDER:
            dictionary = self.render
        elif buttonType == ButtonEventHandlers.Type.PRESS:
            dictionary = self.press
        elif buttonType == ButtonEventHandlers.Type.RELEASE:
            dictionary = self.release
        elif buttonType == ButtonEventHandlers.Type.ROLLOVER:
            dictionary = self.rollOver
        elif buttonType == ButtonEventHandlers.Type.ROLLOUT:
            dictionary = self.rollOut
        if dictionary is not None:
            dictionary = ButtonEventHandlerDictionary(dictionary)
            for k, v in dictionary.items():
                v(target)

    def CallKEYPRESS(self, target, code):
        dictionary = ButtonKeyPressHandlerDictionary(self.keyPress)
        for k, v in dictionary.items():
            v(target, code)


class Button(IObject):
    m_data = None
    m_buttonLink = None
    m_handler = None
    m_invert = None
    m_hitX = 0.0
    m_hitY = 0.0

    def __init__(self, *args):
        if len(args) > 0:
            lwf, parent, objId, instId = args[0], args[1], args[2], args[3]
            matrixId = args[4] if args[4] else -1
            colorTransformId = args[5] if args[5] else -1
            super().__init__(lwf, parent, Format.Object.Type.BUTTON, objId, instId)
            self.m_matrixId = matrixId
            self.m_colorTransformId = colorTransformId

            self.m_invert = Matrix()
            self.m_hitX = INT32_MINVALUE
            self.m_hitY = INT32_MINVALUE

            if objId >= 0:
                self.m_data = lwf.data.buttons[objId]
                self.m_dataMatrixId = self.m_data.matrixId

            handler = lwf.GetButtonEventHandlers(self)
            if handler is not None:
                self.m_handler = ButtonEventHandlers()
                self.m_handler.Add(handler)
                self.m_handler.Call(ButtonEventHandlers.Type.LOAD, self)

    # Getters and setters
    @property
    def data(self):
        return self.m_data

    @property
    def width(self):
        return self.m_data.width if self.m_data is not None else 0

    @property
    def height(self):
        return self.m_data.height if self.m_data is not None else 0

    @property
    def hitX(self):
        return self.m_hitX

    @property
    def hitY(self):
        return self.m_hitY

    @property
    def buttonLink(self):
        return self.m_buttonLink

    @buttonLink.setter
    def buttonLink(self, value):
        self.m_buttonLink = value

    # main methods
    def SetHandlers(self, handler):
        if self.m_handler is None:
            self.m_handler = ButtonEventHandlers()
        else:
            self.m_handler.Clear()
        self.m_handler.Add(handler)

    def Exec(self, matrixId=0, colorTransformId=0):
        super().Exec(matrixId, colorTransformId)
        self.EnterFrame()

    def Update(self, m, c):
        super().Update(m, c)

        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.UPDATE, self)

    def Render(self, v, rOffset):
        if v and self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.RENDER, self)

    def Destroy(self):
        self.m_lwf.ClearFocus(self)
        self.m_lwf.ClearPressed(self)

        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.UNLOAD, self)

        super().Destroy()

    def LinkButton(self):
        if self.m_lwf.focus == self:
            self.m_lwf.focusOnLink = True
        self.m_buttonLink = self.m_lwf.buttonHead
        self.m_lwf.buttonHead = self

    def CheckHit(self, px, py):
        Utility.InvertMatrix(self.m_invert, self.m_matrix)
        x, y = Utility.CalcMatrixToPoint(px, py, self.m_invert)
        if 0 <= x < self.m_data.width and 0 <= y < self.m_data.height:
            self.m_hitX = x
            self.m_hitY = y
            return True
        self.m_hitX = INT32_MINVALUE
        self.m_hitY = INT32_MINVALUE
        return False

    def EnterFrame(self):
        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.ENTERFRAME, self)

    def RollOver(self):
        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.ROLLOVER, self)

        self.PlayAnimation(Format.ButtonCondition.Condition.ROLLOVER)

    def RollOut(self):
        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.ROLLOUT, self)

        self.PlayAnimation(Format.ButtonCondition.Condition.ROLLOUT)

    def Press(self):
        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.PRESS, self)

        self.PlayAnimation(Format.ButtonCondition.Condition.PRESS)

    def Release(self):
        if self.m_handler is not None:
            self.m_handler.Call(ButtonEventHandlers.Type.RELEASE, self)

        self.PlayAnimation(Format.ButtonCondition.Condition.RELEASE)

    def KeyPress(self, code):
        if self.m_handler is not None:
            self.m_handler.CallKEYPRESS(self, code)

        self.PlayAnimation(Format.ButtonCondition.Condition.KEYPRESS, code)

    def PlayAnimation(self, condition, code=0):
        conditions = self.m_lwf.data.buttonConditions
        i = 0
        while i < self.m_data.conditions:
            c = conditions[self.m_data.conditionId + i]
            if (c.condition & condition) != 0 and (
                    condition != Format.ButtonCondition.Condition.KEYPRESS or c.keyCode == code):
                self.m_lwf.PlayAnimation(c.animationId, self.m_parent, self)
            i += 1

    def AddButtonEventHandler(self, eventName, handler):
        eventId = self.m_lwf.GetEventOffset()
        if eventName == "load":
            self.m_handler.Add(eventId, load=handler)
            return eventId
        elif eventName == "unload":
            self.m_handler.Add(eventId, u=handler)
            return eventId
        elif eventName == "enterFrame":
            self.m_handler.Add(eventId, e=handler)
            return eventId
        elif eventName == "update":
            self.m_handler.Add(eventId, up=handler)
            return eventId
        elif eventName == "render":
            self.m_handler.Add(eventId, r=handler)
            return eventId
        elif eventName == "press":
            self.m_handler.Add(eventId, p=handler)
            return eventId
        elif eventName == "release":
            self.m_handler.Add(eventId, rl=handler)
            return eventId
        elif eventName == "rollOver":
            self.m_handler.Add(eventId, rOver=handler)
            return eventId
        elif eventName == "rollOut":
            self.m_handler.Add(eventId, rOut=handler)
            return eventId
        else:
            return -1

    def AddButtonKeyPressHandler(self, eventName, handler):
        eventId = -1
        if eventName == "keyPress":
            eventId = self.m_lwf.GetEventOffset()
            self.m_handler.Add(eventId, k=handler)
        return eventId

    def RemoveEventHandler(self, eventName, eventId):
        if eventName == "load" \
                or eventName == "unload" \
                or eventName == "enterFrame" \
                or eventName == "update" \
                or eventName == "render" \
                or eventName == "press" \
                or eventName == "release" \
                or eventName == "rollOver" \
                or eventName == "rollOut" \
                or eventName == "keyPress":
            self.m_handler.Remove(eventId)

    def ClearEventHandler(self, eventName):
        if eventName == "load":
            self.m_handler.Clear(ButtonEventHandlers.Type.LOAD)
        elif eventName == "unload":
            self.m_handler.Clear(ButtonEventHandlers.Type.UNLOAD)
        elif eventName == "enterFrame":
            self.m_handler.Clear(ButtonEventHandlers.Type.ENTERFRAME)
        elif eventName == "update":
            self.m_handler.Clear(ButtonEventHandlers.Type.UPDATE)
        elif eventName == "render":
            self.m_handler.Clear(ButtonEventHandlers.Type.RENDER)
        elif eventName == "press":
            self.m_handler.Clear(ButtonEventHandlers.Type.PRESS)
        elif eventName == "release":
            self.m_handler.Clear(ButtonEventHandlers.Type.RELEASE)
        elif eventName == "rollOver":
            self.m_handler.Clear(ButtonEventHandlers.Type.ROLLOVER)
        elif eventName == "rollOut":
            self.m_handler.Clear(ButtonEventHandlers.Type.ROLLOUT)
        elif eventName == "keyPress":
            self.m_handler.Clear(ButtonEventHandlers.Type.KEYPRESS)
