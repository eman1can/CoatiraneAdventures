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
        if eventName is "load":
            self.m_handler.Add(eventId, load=handler)
            return eventId
        elif eventName is "unload":
            self.m_handler.Add(eventId, u=handler)
            return eventId
        elif eventName is "enterFrame":
            self.m_handler.Add(eventId, e=handler)
            return eventId
        elif eventName is "update":
            self.m_handler.Add(eventId, up=handler)
            return eventId
        elif eventName is "render":
            self.m_handler.Add(eventId, r=handler)
            return eventId
        elif eventName is "press":
            self.m_handler.Add(eventId, p=handler)
            return eventId
        elif eventName is "release":
            self.m_handler.Add(eventId, rl=handler)
            return eventId
        elif eventName is "rollOver":
            self.m_handler.Add(eventId, rOver=handler)
            return eventId
        elif eventName is "rollOut":
            self.m_handler.Add(eventId, rOut=handler)
            return eventId
        else:
            return -1

    def AddButtonKeyPressHandler(self, eventName, handler):
        eventId = -1
        if eventName is "keyPress":
            eventId = self.m_lwf.GetEventOffset()
            self.m_handler.Add(eventId, k=handler)
        return eventId

    def RemoveEventHandler(self, eventName, eventId):
        if eventName is "load" \
                or eventName is "unload" \
                or eventName is "enterFrame" \
                or eventName is "update" \
                or eventName is "render" \
                or eventName is "press" \
                or eventName is "release" \
                or eventName is "rollOver" \
                or eventName is "rollOut" \
                or eventName is "keyPress":
            self.m_handler.Remove(eventId)

    def ClearEventHandler(self, eventName):
        if eventName is "load":
            self.m_handler.Clear(ButtonEventHandlers.Type.LOAD)
        elif eventName is "unload":
            self.m_handler.Clear(ButtonEventHandlers.Type.UNLOAD)
        elif eventName is "enterFrame":
            self.m_handler.Clear(ButtonEventHandlers.Type.ENTERFRAME)
        elif eventName is "update":
            self.m_handler.Clear(ButtonEventHandlers.Type.UPDATE)
        elif eventName is "render":
            self.m_handler.Clear(ButtonEventHandlers.Type.RENDER)
        elif eventName is "press":
            self.m_handler.Clear(ButtonEventHandlers.Type.PRESS)
        elif eventName is "release":
            self.m_handler.Clear(ButtonEventHandlers.Type.RELEASE)
        elif eventName is "rollOver":
            self.m_handler.Clear(ButtonEventHandlers.Type.ROLLOVER)
        elif eventName is "rollOut":
            self.m_handler.Clear(ButtonEventHandlers.Type.ROLLOUT)
        elif eventName is "keyPress":
            self.m_handler.Clear(ButtonEventHandlers.Type.KEYPRESS)
