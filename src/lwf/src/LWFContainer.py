
class LWFContainer(Button):
    m_child = None

    def __init__(self, parent, child):
        self.m_lwf = parent.lwf
        self.m_parent = parent
        self.m_child = child

    @property
    def child(self):
        return self.m_child

    def CheckHit(self, px, py):
        button = self.m_child.InputPoint(int(px), int(py))
        return True if button is not None else False

    def RollOver(self):
        pass

    def RollOut(self):
        if self.m_child.focus is not None:
            self.m_child.RollOut()
            self.m_child.ClearFocus(self.m_child.focus)

    def Press(self):
        self.m_child.InputPress()

    def Release(self):
        self.m_child.InputRelease()

    def KeyPress(self, code):
        self.m_child.InputKeyPress(code)
