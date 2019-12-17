# Internal Imports
from ..utils.Type import Dictionary

from ..objects.Object import Object

from ..Format import Format


class Texts(Dictionary):
    pass


class TextDictionaryItem:
    text = None
    renderer = None

    def __init__(self, *args):
        self.text = args[0]
        self.renderer = args[1] if len(args) is 2 else None


class TextDictionary(Dictionary):
    pass


class Text(Object):
    m_name = None

    def __init__(self, lwf, p, objId, instId=-1):
        super().__init__(lwf, p, Format.Object.Type.TEXT, objId)
        text = lwf.data.texts[objId]
        self.m_dataMatrixId = text.matrixId

        if text.nameStringId is not -1:
            self.m_name = lwf.data.strings[text.nameStringId]
        else:
            if 0 <= instId < len(lwf.data.instanceNames):
                stringId = lwf.GetInstanceNameStringId(instId)
                if stringId is not -1:
                    self.m_name = lwf.data.strings[stringId]

        textRenderer = lwf.rendererFactory.ConstructText(lwf, objId, self)
        t = None
        if text.stringId is not -1:
            t = lwf.data.strings[text.stringId]

        if text.nameStringId is -1 and (self.name is None or self.name is ""):
            if text.stringId is not -1:
                textRenderer.SetText(t)
        else:
            lwf.SetTextRenderer(p.GetFullName(), self.name, t, textRenderer)

        self.m_renderer = textRenderer

    @property
    def name(self):
        return self.m_name
