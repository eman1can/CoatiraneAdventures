# Internal Imports
from .utils.Constants import SINGLE_MINVALUE, INT32_MINVALUE
from .utils.Type import Matrix, ColorTransform, HandlerWrapper
from .utils.Utility import Utility
from .utils.Animation import *

from .objects.Event import EventHandlerDictionary, GenericEventHandlerDictionary
from .objects.Property import Property
from .objects.Object import IObject
from .objects.Button import Button, ButtonEventHandlers, ButtonEventHandlersDictionary
from .objects.Movie import MovieCommands, Movie, MovieEventHandlers, MovieEventHandlersDictionary
from .objects.ProgramObject import ProgramObjectConstructor
from .objects.Text import TextDictionary, TextDictionaryItem

from .RenderFactory import NullRendererFactory
from .Format import Format
from .Core import MaskModes, BlendModes, AllowButtonList, DenyButtonList, ExecHandlerList

# External Imports
from typing import List
from datetime import datetime
import math


class LWF:
    class TweenMode:
        Movie = 0
        LWF = 1

    m_instanceOffset = 0
    m_iObjectOffset = 0
    ROUND_OFF_TICK_RATE = 0.05
    m_textureLoadHandler = None

    m_data = None
    m_rendererFactory = None
    m_rootMovieStringId = 0
    m_property = None
    m_rootMovie = None
    m__root = None
    m_instances = None
    m_focus = None
    m_pressed = None
    m_buttonHead = None
    m_movieCommands = None
    m_programObjectConstructors = None
    m_detachHandler = None
    m_allowButtonList = None
    m_denyButtonList = None
    m_execHandlers = None
    m_textDictionary = None
    m_blendModes = None
    m_maskModes = None
    m_frameRate = 0
    m_fastForwardTimeout = 0
    m_fastForward = False
    m_fastForwardCurrent = False
    m_frameSkip = False
    m_execLimit = 0
    m_renderingIndex = 0
    m_renderingIndexOffsetted = 0
    m_renderingCount = 0
    m_depth = 0
    m_execCount = 0
    m_updateCount = 0
    m_instanceId = 0
    m_time = 0.0
    m_progress = 0.0
    m_tick = 0.0
    m_roundOffTick = 0.0
    m_parent = None
    m_attachName = None
    m_attachVisible = False
    m_execDisabled = False
    m_executedForExecDisabled = False
    m_interceptByNotAllowOrDenyButtons = False
    m_intercepted = False
    m_propertyDirty = False
    m_focusOnLink = False
    m_needsUpdate = False
    m_needsUpdateForAttachLWF = False
    m_pointX = 0.0
    m_pointY = 0.0
    m_pressing = False
    m_matrix = None
    m_matrixIdentity = None
    m_execMatrix = None
    m_colorTransform = None
    m_colorTransformIdentity = None
    m_execColorTransform = None
    m_alive = False
    m_eventOffset = 0
    # lwf_event -----------------------------------------------------------------------------------------
    m_eventHandlers: List[(EventHandlerDictionary or None)] = None
    m_genericEventHandlerDictionary = None
    m_movieEventHandlers = None
    m_buttonEventHandlers = None
    m_movieEventHandlersByFullName = None
    m_buttonEventHandlersByFullName = None

    # lwf_core ------------------------------------------------------------------------------------------

    interactive = False
    scaleByStage = 0.0
    isLWFAttached = False
    lwfLoader = None
    lwfUnloader = None
    privateData = None
    tweenMode = None
    tweens = None
    tweenEventId = None

    def __init__(self, lwfData, r):
        print("Create a lwf!")
        self.m_data = lwfData
        self.interactive = len(self.m_data.buttonConditions) > 0
        self.m_frameRate = self.m_data.header.frameRate
        self.m_execLimit = 3
        self.m_frameSkip = False
        self.m_tick = 1.0 / self.m_frameRate
        self.m_roundOffTick = self.m_tick * self.ROUND_OFF_TICK_RATE
        self.m_attachVisible = True
        self.m_interceptByNotAllowOrDenyButtons = True
        self.m_intercepted = False
        self.scaleByStage = 1
        self.m_needsUpdate = False
        self.m_needsUpdateForAttachLWF = False
        self.m_pointX = SINGLE_MINVALUE
        self.m_pointY = SINGLE_MINVALUE
        self.m_pressing = False
        self.m_instanceOffset += 1
        self.m_instanceId = self.m_instanceOffset
        self.m_alive = True

        if not self.interactive and len(self.m_data.frames) == 1:
            self.DisableExec()
        self.m_property = Property(self)
        self.m_instances = [IObject() for _ in range(0, len(self.m_data.instanceNames))]
        print(self.m_instances)
        self.InitEvent()
        self.m_movieCommands = MovieCommands()
        self.m_programObjectConstructors = [ProgramObjectConstructor() for _ in
                                            range(0, len(self.m_data.programObjects))]
        self.m_textDictionary = TextDictionary()

        self.m_matrix = Matrix()
        self.m_matrixIdentity = Matrix()
        self.m_execMatrix = Matrix()
        self.m_colorTransform = ColorTransform()
        self.m_ColorTransFormIdentity = ColorTransform()
        self.m_execColorTransform = ColorTransform()
        self.m_blendModes = BlendModes()
        self.m_maskModes = MaskModes()

        self.Init()

        self.SetRendererFactory(r)

    # getters and setters
    @property
    def data(self):
        return self.m_data

    # @property
    # def interactive(self):
    #     return self.m_interactive
    #
    # @interactive.setter
    # def interactive(self, value):
    #     self.m_interactive = value

    # @property
    # def scaleByStage(self):
    #     return self.m_scaleByStage
    #
    # @scaleByStage.setter
    # def scaleByStage(self, value):
    #     self.m_scaleByStage = value
    @property
    def isExecDisabled(self):
        return self.m_execDisabled

    @property
    def attachVisible(self):
        return self.m_attachVisible

    @property
    def isPropertyDirty(self):
        return self.m_propertyDirty

    # @property
    # def isLWFAttached(self):
    #     return self.b_isLWFAttached
    #
    # @isLWFAttached.setter
    # def isLWFAttached(self, value):
    #     self.b_isLWFAttached = value

    # @property
    # def lwfLoader(self):
    #     return self.b_lwfLoader
    #
    # @lwfLoader.setter
    # def lwfLoader(self, value):
    #     self.b_lwfLoader = value

    # @property
    # def lwfUnloader(self):
    #     return self.b_lwfUnloader
    #
    # @lwfUnloader.setter
    # def lwfUnloader(self, value):
    #     self.b_lwfUnloader = value

    # @property
    # def privateData(self):
    #     return self.b_privateData
    #
    # @privateData.setter
    # def privateData(self, value):
    #     self.b_privateData = value

    # @property
    # def tweenMode(self):
    #     return self.b_tweenMode
    #
    # @tweenMode.setter
    # def tweenMode(self, value):
    #     self.b_tweenMode = value

    # @property
    # def tweens(self):
    #     return self.b_tweens
    #
    # @tweens.setter
    # def tweens(self, value):
    #     self.b_tweens = value

    # @property
    # def tweenEventId(self):
    #     return self.b_tweenEventId
    #
    # @tweenEventId.setter
    # def tweenEventId(self, value):
    #     self.b_tweenEventId = value

    @property
    def rendererFactory(self):
        return self.m_rendererFactory

    @property
    def lwfproperty(self):
        return self.m_property

    @property
    def rootMovie(self):
        return self.m_rootMovie

    @property
    def __root(self):
        return self.m__root

    @property
    def focus(self):
        return self.m_focus

    @property
    def pressed(self):
        return self.m_pressed

    @property
    def buttonHead(self):
        return self.m_buttonHead

    @buttonHead.setter
    def buttonHead(self, value):
        self.m_buttonHead = value

    @property
    def needsUpdate(self):
        return self.m_needsUpdate

    @property
    def needsUpdateForAttachLWF(self):
        return self.m_needsUpdateForAttachLWF

    @property
    def pointX(self):
        return self.m_pointX

    @property
    def pointY(self):
        return self.m_pointY

    @property
    def pressing(self):
        return self.m_pressing

    @property
    def frameRate(self):
        return self.m_frameRate

    @property
    def renderingIndex(self):
        return self.m_renderingIndex

    @property
    def renderingIndexOffsetted(self):
        return self.m_renderingIndexOffsetted

    @property
    def renderingCount(self):
        return self.m_renderingCount

    @property
    def execCount(self):
        return self.m_execCount

    @property
    def updateCount(self):
        return self.m_updateCount

    @property
    def instanceId(self):
        return self.m_instanceId

    @property
    def width(self):
        return self.m_data.header.width

    @property
    def height(self):
        return self.m_data.header.height

    @property
    def time(self):
        return self.m_time

    @property
    def progress(self):
        return self.m_progress

    @progress.setter
    def progress(self, value):
        self.m_progress = value

    @property
    def tick(self):
        return self.m_tick

    @property
    def alive(self):
        return self.m_alive

    @property
    def focusOnLink(self):
        return self.m_focusOnLink

    @focusOnLink.setter
    def focusOnLink(self, value):
        self.m_focusOnLink = value

    @property
    def parent(self):
        return self.m_parent

    @parent.setter
    def parent(self, value):
        self.m_parent = value

    @property
    def name(self):
        return self.m_data.strings[self.m_data.header.nameStringId]

    @property
    def attachName(self):
        return self.m_attachName

    @attachName.setter
    def attachName(self, value):
        self.m_attachName = value

    @property
    def depth(self):
        return self.m_depth

    @depth.setter
    def depth(self, value):
        self.m_depth = value

    @property
    def detachHandler(self):
        return self.m_detachHandler

    @detachHandler.setter
    def detachHandler(self, value):
        self.m_detachHandler = value

    @property
    def interceptByNotAllowOrDenyButtons(self):
        return self.m_interceptByNotAllowOrDenyButtons

    @interceptByNotAllowOrDenyButtons.setter
    def interceptByNotAllowOrDenyButtons(self, value):
        self.m_interceptByNotAllowOrDenyButtons = value

    @property
    def intercepted(self):
        return self.interactive and self.m_intercepted

    # main methods

    def SetRendererFactory(self, rendererFactory=None):
        if rendererFactory is None:
            rendererFactory = NullRendererFactory()
        self.m_rendererFactory = rendererFactory
        self.m_rendererFactory.init(self)

    def SetFrameRate(self, f):
        if f == 0:
            return
        self.m_frameRate = f
        self.m_tick = 1 / self.m_frameRate

    def SetPreferredFrameRate(self, f, execLimit=2):
        if f == 0:
            return
        self.m_execLimit = math.ceil(self.m_frameRate / f) + execLimit

    def FitForHeight(self, stageHeight):
        Utility.FitForHeight(self, stageHeight)

    def FitForWidth(self, stageWidth):
        Utility.FitForWidth(self, stageWidth)

    def ScaleFroheight(self, stageHeight):
        Utility.ScaleForHeight(self, stageHeight)

    def ScaleForWidth(self, stageWidth):
        Utility.ScaleForWidth(self, stageWidth)

    def RenderOffset(self):
        self.m_renderingIndexOffsetted = 0

    def ClearRenderOffset(self):
        self.m_renderingIndexOffsetted = self.m_renderingIndex

    def RenderObject(self, count=1):
        self.m_renderingIndex += count
        self.m_renderingIndexOffsetted += count
        return self.m_renderingIndex

    def BeginBlendMode(self, blendMode):
        self.m_blendModes.append(blendMode)
        self.m_rendererFactory.SetBlendMode(blendMode)

    def EndBlendMode(self):
        self.m_blendModes.remove(len(self.m_blendModes) - 1)
        self.m_rendererFactory.SetBlendMode(self.m_blendModes[len(self.m_blendModes) - 1] if len(self.m_blendModes) > 0
                                            else Format.Constant.BLEND_MODE_NORMAL)

    def BeginMaskMode(self, maskMode):
        self.m_maskModes.append(maskMode)
        self.m_rendererFactory.SetMaskMode(maskMode)

    def EndMaskMode(self):
        self.m_maskModes.remove(len(self.m_maskModes) - 1)
        self.m_rendererFactory.SetMaskMode(self.m_maskModes[len(self.m_maskModes) - 1] if len(self.m_maskModes) > 0
                                           else Format.Constant.BLEND_MODE_NORMAL)

    def SetAttachVisible(self, visible):
        self.m_attachVisible = visible

    def ClearFocus(self, button):
        if self.m_focus == button:
            self.m_focus = None

    def ClearPressed(self, button):
        if self.m_pressed == button:
            self.m_pressed = None

    def ClearIntercepted(self):
        self.m_intercepted = False

    def Init(self):
        self.m_time = 0
        self.m_progress = 0

        Utility.Clear_Array(self.m_instances, 0, len(self.m_instances))
        self.m_focus = None

        self.m_movieCommands.clear()

        self.m_rootMovieStringId = self.GetStringId("_root")
        if self.m_rootMovie is not None:
            self.m_rootMovie.Destroy()
        self.m_rootMovie = Movie(self, None, self.m_data.header.rootMovieId,
                                 self.SearchInstanceId(self.m_rootMovieStringId))
        self.m__root = self.m_rootMovie

    def SetRoot(self, root):
        self.m__root = root

    def CalcMatrix(self, matrix):
        p = self.m_property
        if p.hasMatrix:
            if matrix is not None:
                m = Utility.CalcMatrix(self.m_matrix, matrix, p.matrix)
            else:
                m = p.matrix
        else:
            m = self.m_matrixIdentity if matrix is None else matrix
        return m

    def CalcColorTransform(self, colorTransform):
        p = self.m_property
        if p.hasColorTransform:
            if colorTransform is not None:
                c = Utility.CalcColorTransform(self.m_colorTransform, colorTransform, p.colorTransform)
            else:
                c = p.colorTransform
        else:
            c = self.m_colorTransformIdentity if colorTransform is None else colorTransform
        return c

    def LinkButton(self):
        self.m_buttonHead = None
        if self.interactive and self.m_rootMovie.hasButton:
            self.m_focusOnLink = False
            self.m_rootMovie.LinkButton()
            if self.m_focus is not None and not self.m_focusOnLink:
                self.m_focus.RollOut()
                self.m_focus = None

    def ExecInternal(self, tick):
        print("Exec Internal lwf")
        if self.m_rootMovie is None:
            return 0
        execed = False
        currentProgress = self.m_progress

        if self.m_execDisabled and self.tweens is None:
            if not self.m_executedForExecDisabled:
                self.m_execCount += 1
                self.m_rootMovie.Exec()
                self.m_rootMovie.PostExec(True)
                self.m_executedForExecDisabled = True
                execed = True
        else:
            progressing = True
            if tick == 0:
                self.m_progress = self.m_tick
            elif tick < 0:
                self.m_progress = self.m_tick
                progressing = False
            else:
                if self.m_time == 0:
                    self.m_time += self.m_tick
                    self.m_progress += self.m_tick
                else:
                    self.m_time += tick
                    self.m_progress += tick

            if self.m_execHandlers is not None:
                for h in self.m_execHandlers:
                    h(self)

            execLimit = self.m_execLimit
            while self.m_progress >= self.m_tick - self.m_roundOffTick:
                execLimit -= 1
                if execLimit < 0:
                    self.m_progress = 0
                    break
                self.m_progress -= self.m_tick
                self.m_execCount += 1
                self.m_rootMovie.Exec()
                self.m_rootMovie.PostExec(progressing)
                execed = True
                if not self.m_frameSkip:
                    break
            if self.m_progress < self.m_roundOffTick:
                self.m_progress = 0

            self.LinkButton()

        if self.isLWFAttached:
            hasButton = self.m_rootMovie.ExecAttachedLWF(tick, currentProgress)
            if hasButton:
                self.LinkButton()

        self.m_needsUpdate = False
        if not self.m_fastForward:
            if execed or self.m_propertyDirty or self.m_needsUpdateForAttachLWF:
                self.m_needsUpdate = True

        if not self.m_execDisabled:
            if tick < 0:
                self.m_progress = currentProgress

        return self.m_renderingCount

    def Exec(self, tick=0, matrix=None, colorTransform=None):
        print("Exec lwf")
        needsToUpdate = False
        if matrix is not None:
            needsToUpdate |= self.m_execMatrix.SetWithComparing(matrix)
        if colorTransform is not None:
            needsToUpdate |= self.m_execColorTransform.SetWithComparing(colorTransform)
        startTime = datetime.now()
        if self.m_parent is None:
            self.m_fastForwardCurrent = self.m_fastForward
            if self.m_fastForwardCurrent:
                tick = self.m_tick
                startTime = datetime.now()

        while True:
            renderingCount = self.ExecInternal(tick)
            needsToUpdate |= self.m_needsUpdate
            if needsToUpdate:
                self.Update(matrix, colorTransform)
            if self.isLWFAttached:
                self.m_rootMovie.UpdateAttachedLWF()
            if needsToUpdate:
                self.m_rootMovie.PostUpdate()
            if self.m_fastForwardCurrent and self.m_fastForward and self.m_parent is None:
                diff = datetime.now() - startTime
                if diff >= self.m_fastForwardTimeout:
                    break
            else:
                break

        return renderingCount

    def ForceExec(self, matrix=None, colorTransform=None):
        return self.Exec(0, matrix, colorTransform)

    def ForceExecWithoutProgress(self, matrix=None, colorTransform=None):
        return self.Exec(-1, matrix, colorTransform)

    def Update(self, matrix=None, colorTransform=None):
        self.m_updateCount += 1
        m = self.CalcMatrix(matrix)
        c = self.CalcColorTransform(colorTransform)
        self.m_renderingIndex = 0
        self.m_renderingIndexOffsetted = 0
        self.m_rootMovie.Update(m, c)
        self.m_renderingCount = self.m_renderingIndex
        self.m_propertyDirty = False
        self.m_needsUpdateForAttachLWF = False

    def Render(self, rIndex=0, rCount=0, rOffset=INT32_MINVALUE):
        if self.m_rootMovie is None or self.m_fastForwardCurrent:
            return 0
        if rCount > 0:
            self.m_renderingCount = rCount
        self.m_renderingIndex = rIndex
        self.m_renderingIndexOffsetted = rIndex
        if self.m_property.hasRenderingOffset:
            self.RenderOffset()
            rOffset = self.m_property.renderingOffset
        self.m_rendererFactory.beginRender(self)
        self.m_rootMovie.Render(self.m_attachVisible, rOffset)
        self.m_rendererFactory.endRender(self)
        return self.m_renderingIndex - rIndex

    def Inspect(self, inspector, hierarchy=0, inspectDepth=0, rIndex=0, rCount=0, rOffset=-2147483648):
        if rCount > 0:
            self.m_renderingCount = rCount
        self.m_renderingIndex = rIndex
        self.m_renderingIndexOffsetted = rIndex
        if self.m_property.hasRenderingOffset:
            self.RenderOffset()
            rOffset = self.m_property.renderingOffset
        self.m_rootMovie.Inspect(inspector, hierarchy, inspectDepth, rOffset)
        return self.m_renderingIndex - rIndex

    def Destroy(self):
        self.m_rootMovie.Destroy()
        if self.m_rendererFactory is not None:
            self.m_rendererFactory.Destruct()
            self.m_rendererFactory = None
        self.m_alive = False
        if self.lwfUnloader is not None:
            self.lwfUnloader()

    def GetIObjectOffset(self):
        self.m_iObjectOffset += 1
        return self.m_iObjectOffset

    def SearchMovieInstance(self, *args):
        assert len(args) is 1
        if isinstance(args[0], int):
            stringId = args[0]
            return self.SearchMovieInstanceByInstanceId(self.SearchInstanceId(stringId))
        else:
            instanceName = args[0]
            if "." in instanceName:
                names = instanceName.split('.')
                if names[0] != self.m_data.strings[self.m_rootMovieStringId]:
                    return None

                m = self.m_rootMovie
                i = 1
                while i < len(names):
                    m = m.SearchMovieInstance(names[i], False)
                    if m is None:
                        return None
                    i += 1

                return m

            stringId = self.GetStringId(instanceName)
            if stringId == -1:
                return self.rootMovie.SearchMovieInstance(instanceName, True)
            return self.SearchMovieInstance(stringId)

    def __getitem__(self, instanceName):
        return self.SearchMovieInstance(instanceName)

    def SearchMovieInstanceByInstanceId(self, instId):
        if instId < 0 or instId >= len(self.m_instances):
            return None
        obj = self.m_instances[instId]
        while obj is not None:
            if obj.IsMovie():
                return obj
            obj = obj.nextInstance
        return None

    def SearchButtonInstance(self, *args) -> (Button or None):
        assert len(args) is 1
        if isinstance(args[0], int):
            stringId = args[0]
            return self.SearchButtonInstanceByInstanceId(self.SearchInstanceId(stringId))
        else:
            instanceName = args[0]
            if "." in instanceName:
                names = instanceName.split('.')
                if names[0] is not self.m_data.strings[self.m_rootMovieStringId]:
                    return None

                m = self.m_rootMovie
                i = 1
                while i < len(names):
                    if i is len(names) - 1:
                        return m.SearchButtonInstance(names[i], False)
                    else:
                        m = m.SearchMovieInstance(names[i], False)
                        if m is None:
                            return None
                    i += 1
                return None

            stringId = self.GetStringId(instanceName)
            if stringId is -1:
                return self.rootMovie.SearchButtonInstance(instanceName, True)

            return self.SearchButtonInstance(stringId)

    def SearchButtonInstanceByInstanceId(self, instId):
        if instId < 0 or instId >= len(self.m_instances):
            return None
        obj = self.m_instances[instId]
        while obj is not None:
            if obj.IsButton():
                return obj
            obj = obj.nextInstance
        return None

    def GetInstance(self, instId):
        print(self.m_instances)
        print(self)
        return self.m_instances[instId]

    def SetInstance(self, instId, instance):
        self.m_instances[instId] = instance

    def GetProgramObjectConstructor(self, arg):
        if isinstance(arg, int):
            programObjectId = arg
            if programObjectId < 0 or programObjectId >= len(self.m_data.programObjects):
                return None
            return self.m_programObjectConstructors[programObjectId]
        else:
            programObjectName = arg
            return self.GetProgramObjectConstructor(self.SearchProgramObjectId(programObjectName))

    def SetProgramObjectConstructor(self, arg, programObjectConstructor):
        if isinstance(arg, int):
            programObjectId = arg
            if programObjectId < 0 or programObjectId >= len(self.m_data.programObjects):
                return
            self.m_programObjectConstructors[programObjectId] = programObjectConstructor
        else:
            programObjectName = arg
            self.SetProgramObjectConstructor(self.SearchProgramObjectId(programObjectName),
                                             programObjectConstructor)

    def ExecMovieCommand(self):
        if len(self.m_movieCommands) is 0:
            return
        deletes = []
        for key, value in self.m_movieCommands.items():
            avaliable = True
            movie = self.m_rootMovie
            for name in key:
                movie = movie.SearchMovieInstance(name)
                if movie is None:
                    avaliable = False
                    break
            if avaliable:
                value(movie)
                deletes.append(key)

        for key in deletes:
            self.m_movieCommands.remove(key)

    def SetMovieCommand(self, instanceNames, cmd):
        names = []
        for name in instanceNames:
            names.append(name)
        self.m_movieCommands.set(names, cmd)
        self.ExecMovieCommand()

    def SearchAttachedMovie(self, attachName):
        return self.m_rootMovie.SearchAttachedMovie(attachName)

    def SearchAttachedLWF(self, attachName):
        return self.m_rootMovie.SearchAttachedLWF(attachName)

    def AddAllowButton(self, buttonName):
        instId = self.SearchInstanceId(self.GetStringId(buttonName))
        if instId < 0:
            return False

        if self.m_allowButtonList is None:
            self.m_allowButtonList = AllowButtonList()
        self.m_allowButtonList[instId] = True
        return True

    def RemoveAllowButton(self, buttonName):
        if self.m_allowButtonList is None:
            return False

        instId = self.SearchInstanceId(self.GetStringId(buttonName))
        if instId < 0:
            return False
        return self.m_allowButtonList.Remove(instId)

    def ClearAllowButton(self):
        self.m_allowButtonList = None

    def AddDenyButton(self, buttonName):
        instId = self.SearchInstanceId(self.GetStringId(buttonName))
        if instId < 0:
            return False
        if self.m_denyButtonList is None:
            self.m_denyButtonList = DenyButtonList()
        self.m_denyButtonList[instId] = True
        return True

    def DenyAllButtons(self):
        if self.m_denyButtonList is None:
            self.m_denyButtonList = DenyButtonList()
        instId = 0
        while instId < len(self.m_instances):
            self.m_denyButtonList[instId] = True
            instId += 1

    def RemoveDenyButton(self, buttonName):
        if self.m_denyButtonList is None:
            return False
        instId = self.SearchInstanceId(self.GetStringId(buttonName))
        if instId < 0:
            return False
        return self.m_denyButtonList.Remove(instId)

    def ClearDenyButton(self):
        self.m_denyButtonList = None

    def DisableExec(self):
        self.m_execDisabled = True
        self.m_executedForExecDisabled = False

    def EnableExec(self):
        self.m_execDisabled = False

    def SetPropertyDirty(self):
        self.m_propertyDirty = True
        if self.m_parent is not None:
            self.m_parent.lwf.SetPropertyDirty()

    def GetParent(self):
        if self.m_parent is None:
            return None

        lwfParent = self.m_parent.lwf
        while True:
            if lwfParent is None or lwfParent.m_parent is None:
                return lwfParent
            lwfParent = lwfParent.m_parent.lwf

    def SetInteractive(self):
        self.interactive = True
        if self.m_parent is not None:
            self.m_parent.lwf.SetInteractive()

    def SetFrameSkip(self, frameSkip):
        self.m_frameSkip = frameSkip
        self.m_progress = 0
        if self.m_parent is not None:
            self.m_parent.lwf.SetFrameSkip(frameSkip)

    def SetLWFAttached(self):
        self.isLWFAttached = True
        self.m_needsUpdateForAttachLWF = True
        if self.m_parent is not None:
            self.m_parent.lwf.SetLWFAttached()

    def SetFastForwardTimeout(self, fastForwardTimeout):
        self.m_fastForwardTimeout = fastForwardTimeout

    def SetFastForward(self, fastForward):
        self.m_fastForward = fastForward
        if self.m_parent is not None:
            self.m_parent.lwf.SetFastForward(fastForward)

    def AddExecHandler(self, execHandler):
        if self.m_execHandlers is None:
            self.m_execHandlers = ExecHandlerList()
        self.m_execHandlers.append(execHandler)

    def RemoveExecHandler(self, execHandler):
        if self.m_execHandlers is None:
            return
        self.m_execHandlers.RemoveAll(lambda h: h == execHandler)

    def ClearExecHandler(self):
        self.m_execHandlers = None

    def SetExecHandler(self, execHandler):
        self.ClearExecHandler()
        self.AddExecHandler(execHandler)

    def SetText(self, textName, text):
        boolean, item = self.m_textDictionary.TryGetValue(textName)
        if not boolean:
            self.m_textDictionary[textName] = TextDictionaryItem(text)
        else:
            if item.renderer is not None:
                item.renderer.SetText(text)
            item.text = text

    def GetText(self, textName):
        boolean, item = self.m_textDictionary.TryGetValue(textName)
        if boolean:
            return item.text
        return None

    def SetTextRenderer(self, fullPath, textName, text, textRenderer):
        setText = False
        fullName = fullPath + "." + textName
        boolean, item = self.m_textDictionary.TryGetValue(fullName)
        if boolean:
            item.renderer = textRenderer
            if not (item.text is None or item.text == ""):
                textRenderer.SetText(item.text)
                setText = True
        else:
            self.m_textDictionary[fullName] = TextDictionaryItem(text, textRenderer)

        boolean, item = self.m_textDictionary.TryGetValue(textName)
        if boolean:
            item.renderer = textRenderer
            if not setText and not (item.text is None or item.text == ""):
                textRenderer.SetText(item.text)
                setText = True
        else:
            self.m_textDictionary[textName] = TextDictionaryItem(text, textRenderer)

        if not setText:
            textRenderer.SetText(text)

    def ClearTextRenderer(self, textName):
        boolean, item = self.m_textDictionary.TryGetValue(textName)
        if not boolean:
            item.renderer = None

    @staticmethod
    def SetTextureLoadHandler(h):
        LWF.m_textureLoadHandler = h

    @staticmethod
    def GetTextureLoadHandler():
        return LWF.m_textureLoadHandler

    # -----------------------   lwf_animation -------------------------------

    def PlayAnimation(self, animationId, movie, button=None):
        i = 0
        animations = self.m_data.animations[animationId]
        target = movie
        while True:
            case = animations[i]
            i += 1
            if case == END:
                return
            elif case == PLAY:
                target.Play()
            elif case == STOP:
                target.Stop()
            elif case == NEXTFRAME:
                target.NextFrame()
            elif case == PREVFRAME:
                target.PrevFrame()
            elif case == GOTOFRAME:
                target.GotoFrameInternal(animations[i])
                i += 1
            elif case == GOTOLABEL:
                target.GotoFrame(self.SearchFrame(target, animations[i]))
                i += 1
            elif case == SETTARGET:
                target = movie
                count = animations[i]
                i += 1
                if count is 0:
                    break

                j = 0
                while j < count:
                    instId = animations[i]
                    i += 1
                    if instId == INSTANCE_TARGET_ROOT:
                        target = self.m_rootMovie
                    elif instId == INSTANCE_TARGET_PARENT:
                        target = target.parent
                        if target is None:
                            target = self.m_rootMovie
                    else:
                        target = target.SearchMovieInstanceByInstanceId(instId, False)
                        if target is None:
                            target = movie
                    j += 1
            elif case == EVENT:
                eventId = animations[i]
                i += 1
                if self.m_eventHandlers[eventId] is not None:
                    handlers = EventHandlerDictionary(self.m_eventHandlers[eventId])
                    for hk, hv in handlers:
                        hv(movie, button)
            elif case == CALL:
                i += 1

    # ----------------------------- lwf_coredata -----------------------------------------------

    def GetInstanceNameStringId(self, instId):
        if instId < 0 or instId >= len(self.m_data.instanceNames):
            return -1
        return self.m_data.instanceNames[instId].stringId

    def GetStringId(self, string):
        boolean, i = self.m_data.stringMap.TryGetValue(string)
        if boolean:
            return i
        else:
            return -1

    def SearchInstanceId(self, stringId):
        if stringId < 0 or stringId >= len(self.m_data.strings):
            return -1
        boolean, i = self.m_data.instanceNameMap.TryGetValue(stringId)
        if boolean:
            return i
        else:
            return -1

    def SearchFrame(self, movie, *args):
        if not isinstance(args[0], int):
            return self.SearchFrame(movie, self.GetStringId(args[0]))
        else:
            if args[0] < 0 or args[0] >= len(self.m_data.strings):
                return -1
            labelMap = self.m_data.labelMap[movie.objectId]
            boolean, frameNo = labelMap.tryGetValue(args[0])
            if boolean:
                return frameNo + 1
            else:
                return -1

    def GetMovieLabels(self, movie):
        if movie is None:
            return None
        else:
            return self.m_data.labelMap[movie.objectId]

    def SearchMovieLinkage(self, stringId):
        if stringId < 0 or stringId >= len(self.m_data.strings):
            return -1
        boolean, i = self.m_data.movieLinkageMap.TryGetValue(stringId)
        if boolean:
            return self.m_data.movieLinkages[i].movieId
        else:
            return -1

    def GetMovieLinkageName(self, movieId):
        boolean, i = self.m_data.movieLinkageNameMap.TryGetValue(movieId)
        if boolean:
            return self.m_data.strings[i]
        else:
            return None

    def SearchEventId(self, *args):
        assert len(args) is 1
        if not isinstance(args[0], int):
            return self.SearchEventId(self.GetStringId(args[0]))
        else:
            if args[0] < 0 or args[0] >= len(self.m_data.strings):
                return -1
            boolean, i = self.m_data.eventMap.TryGetValue(args[0])
            if boolean:
                return i
            else:
                return -1

    def SearchProgramObjectId(self, *args):
        assert len(args) is 1
        if not isinstance(args[0], int):
            return self.SearchProgramObjectId(self.GetStringId(args[0]))
        else:
            if args[0] < 0 or args[0] >= len(self.m_data.strings):
                return -1
            boolean, i = self.m_data.programObjectMap.TryGetValue(args[0])
            if boolean:
                return i
            else:
                return -1

    # ---------------------------- lwf_coreop --------------------------------------------

    def SetMovieLoadCommand(self, instanceName, handler):
        movie = self.SearchMovieInstance(instanceName)
        if movie is not None:
            handler(movie)
        else:
            w = HandlerWrapper()

            def handle(m):
                self.RemoveMovieEventHandler(instanceName, w.id)
                handler(m)

            h = handle
            w.id = self.AddMovieEventHandler(instanceName, load=h)

    def SetMoviePostLoadCommand(self, instanceName, handler):
        movie = self.SearchMovieInstance(instanceName)
        if movie is not None:
            handler(movie)
        else:
            w = HandlerWrapper()

            def handle(m):
                self.RemoveMovieEventHandler(instanceName, w.id)
                handler(m)

            h = handle
            w.id = self.AddMovieEventHandler(instanceName, postLoad=h)

    def PlayMovie(self, instanceName):
        self.SetMovieLoadCommand(instanceName, lambda m: m.Play())

    def StopMovie(self, instanceName):
        self.SetMovieLoadCommand(instanceName, lambda m: m.Stop())

    def NextFrameMovie(self, instanceName):
        self.SetMovieLoadCommand(instanceName, lambda m: m.NextFrame())

    def PrevFrameMovie(self, instanceName):
        self.SetMovieLoadCommand(instanceName, lambda m: m.PrevFrame())

    def SetVisibleMovie(self, instanceName, visible):
        self.SetMovieLoadCommand(instanceName, lambda m: m.SetVisible(visible))

    def GotoAndStopMovie(self, instanceName, arg):
        if not isinstance(arg, int):
            label = arg
            self.SetMovieLoadCommand(instanceName, lambda m: m.GotoAndStop(label))
        else:
            frameNo = arg
            self.SetMovieLoadCommand(instanceName, lambda m: m.GotoAndStop(frameNo))

    def GotoAndPlayMovie(self, instanceName, arg):
        if not isinstance(arg, int):
            label = arg
            self.SetMovieLoadCommand(instanceName, lambda m: m.GotoAndPlay(label))
        else:
            frameNo = arg
            self.SetMovieLoadCommand(instanceName, lambda m: m.GotoAndPlay(frameNo))

    def MoveMovie(self, instanceName, vx, vy):
        self.SetMovieLoadCommand(instanceName, lambda m: m.Move(vx, vy))

    def MoveToMovie(self, instanceName, vx, vy):
        self.SetMovieLoadCommand(instanceName, lambda m: m.MoveTo(vx, vy))

    def RotateMovie(self, instanceName, degree):
        self.SetMovieLoadCommand(instanceName, lambda m: m.Rotate(degree))

    def RotateToMovie(self, instanceName, degree):
        self.SetMovieLoadCommand(instanceName, lambda m: m.RetateTo(degree))

    def ScaleMovie(self, instanceName, vx, vy):
        self.SetMovieLoadCommand(instanceName, lambda m: m.Scale(vx, vy))

    def ScaleToMovie(self, instanceName, vx, vy):
        self.SetMovieLoadCommand(instanceName, lambda m: m.ScaleTo(vx, vy))

    def SetAlphaMovie(self, instanceName, v):
        self.SetMovieLoadCommand(instanceName, lambda m: m.SetAlpha(v))

    def SetColorTransformMovie(self, instanceName, vr, vg, vb, va, ar, ag, ab, aa):
        self.SetMovieLoadCommand(instanceName,
                                 lambda m: m.SetColorTransform(ColorTransform(vr, vg, vb, va, ar, ag, ab, aa)))

    # lwf_input --------------------------------------------------------------------
    def InputPoint(self, px, py):
        self.m_intercepted = False
        if not self.interactive:
            return None

        x, y = px, py

        self.m_pointX, self.m_pointY = x, y

        found = False
        button = self.m_buttonHead
        while button is not None:
            if button.CheckHit(x, y):
                if self.m_allowButtonList is not None:
                    boolean, v = self.m_allowButtonList.TryGetValue(button.instanceId)
                    if not boolean:
                        if self.m_interceptByNotAllowOrDenyButtons:
                            self.m_intercepted = True
                            break
                        else:
                            continue
                elif self.m_denyButtonList is not None:
                    boolean, v = self.m_denyButtonList.TryGetValue(button.instanceId)
                    if boolean:
                        if self.m_interceptByNotAllowOrDenyButtons:
                            self.m_intercepted = True
                            break
                        else:
                            continue
                found = True
                if self.m_focus is not button:
                    if self.m_focus is not None:
                        self.m_focus.RollOut()
                    self.m_focus = button
                    self.m_focus.RollOver()
                break
            button = button.buttonLink
        if not found and self.m_focus is not None:
            self.m_focus.RollOut()
            self.m_focus = None
        return self.m_focus

    def InputPress(self):
        if not self.interactive:
            return
        self.m_pressing = True
        if self.m_focus is not None:
            self.m_pressed = self.m_focus
            self.m_focus.Press()

    def InputRelease(self):
        if not self.interactive:
            return
        if self.m_focus is not None and self.m_pressed == self.m_focus:
            self.m_focus.Release()
            self.m_pressed = None

    def InputKeyPress(self, code):
        if not self.interactive:
            return

        button = self.m_buttonHead
        while button is not None:
            button.keyPress(code)
            button = button.buttonLink

    # lwf_event -------------------------------------------------------------------------

    def InitEvent(self):
        self.m_eventHandlers = [EventHandlerDictionary() for _ in range(len(self.m_data.events))]
        self.m_genericEventHandlerDictionary = GenericEventHandlerDictionary()
        self.m_movieEventHandlers = [MovieEventHandlers() for _ in range(len(self.m_instances))]
        self.m_buttonEventHandlers = [ButtonEventHandlers() for _ in range(len(self.m_instances))]

    def GetEventOffset(self):
        self.m_eventOffset += 1
        return self.m_eventOffset

    def AddEventHandler(self, arg, eventHandler):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_data.events):
                return -1
            dictionary = self.m_eventHandlers[arg]
            if dictionary is None:
                dictionary = EventHandlerDictionary()
                self.m_eventHandlers[arg] = dictionary
            handlerId = self.GetEventOffset()
            dictionary.set(handlerId, eventHandler)
            return handlerId
        else:
            eventId = self.SearchEventId(arg)
            if 0 <= eventId < len(self.m_data.events):
                handlerId = self.AddEventHandler(eventId, eventHandler)
            else:
                boolean, dictionary = self.m_genericEventHandlerDictionary.TryGetValue(arg)
                if not boolean:
                    dictionary = EventHandlerDictionary()
                    self.m_genericEventHandlerDictionary[arg] = dictionary
                handlerId = self.GetEventOffset()
                dictionary.set(handlerId, eventHandler)
            return handlerId

    def RemoveEventHandler(self, arg, handlerId):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_data.events):
                return
            dictionary = self.m_eventHandlers[arg]
            if dictionary is None:
                return
            dictionary.remove(handlerId)
        else:
            eventId = self.SearchEventId(arg)
            if 0 <= eventId < len(self.m_data.events):
                self.RemoveEventHandler(eventId, handlerId)
            else:
                dictionary = self.m_genericEventHandlerDictionary[arg]
                if dictionary is None:
                    return
                dictionary.remove(handlerId)

    def ClearEventHandler(self, arg):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_data.events):
                return
            self.m_eventHandlers[arg] = None
        else:
            eventId = self.SearchEventId(arg)
            if 0 <= eventId < len(self.m_data.events):
                self.ClearEventHandler(eventId)
            else:
                self.m_genericEventHandlerDictionary.remove(arg)

    def SetEventHandler(self, arg, eventHandler):
        if isinstance(arg, int):
            self.ClearEventHandler(arg)
            return self.AddEventHandler(arg, eventHandler)
        else:
            return self.SetEventHandler(self.SearchEventId(arg), eventHandler)

    def DispatchEvent(self, eventName, m=None, b=None):
        if m is None:
            m = self.m_rootMovie
        eventId = self.SearchEventId(eventName)
        if 0 <= eventId < len(self.m_data.events):
            dictionary = EventHandlerDictionary(self.m_eventHandlers[eventId])
            for hk, hv in dictionary:
                hv(m, b)

    def GetMovieEventHandlers(self, m):
        if self.m_movieEventHandlersByFullName is not None:
            fullName = m.GetFullName()
            if fullName is not None:
                boolean, handlers = self.m_movieEventHandlersByFullName.TryGetValue(fullName)
                return handlers

        instId = m.instanceId
        if instId < 0 or instId >= len(self.m_instances):
            return None
        return self.m_movieEventHandlers[instId]

    def AddMovieEventHandler(self, arg, load=None, postLoad=None, unload=None, enterFrame=None, update=None,
                             render=None):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_instances):
                return -1

            handlers = self.m_movieEventHandlers[arg]
            if handlers is None:
                handlers = MovieEventHandlers()
                self.m_movieEventHandlers[arg] = handlers

            handlerId = self.GetEventOffset()
            handlers.Add(handlerId, load, postLoad, unload, enterFrame, update, render)
            movie = self.SearchMovieInstanceByInstanceId(arg)
            if movie is not None:
                movie: Movie
                movie.SetHandlers(handlers)
            return handlerId
        else:
            instId = self.SearchInstanceId(self.GetStringId(arg))
            if instId >= 0:
                return self.AddMovieEventHandler(instId, load, postLoad, unload, enterFrame, update, render)

            if "." not in arg:
                return -1

            if self.m_movieEventHandlersByFullName is None:
                self.m_movieEventHandlersByFullName = MovieEventHandlersDictionary()

            boolean, handlers = self.m_movieEventHandlersByFullName.TryGetValue(arg)
            if not boolean:
                handlers = MovieEventHandlers()
                self.m_movieEventHandlersByFullName[arg] = handlers

            handlerId = self.GetEventOffset()
            handlers.Add(handlerId, load, postLoad, unload, enterFrame, update, render)

            movie = self.SearchMovieInstance(arg)
            if movie is not None:
                movie.SetHandlers(handlers)
            return handlerId

    def RemoveMovieEventHandler(self, arg, handlerId):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_instances):
                return

            handlers = self.m_movieEventHandlers[arg]
            if handlers is None:
                return

            handlers.Remove(handlerId)
            movie = self.SearchMovieInstanceByInstanceId(arg)
            if movie is not None:
                movie: Movie
                movie.SetHandlers(handlers)
        else:
            instId = self.SearchInstanceId(self.GetStringId(arg))
            if instId >= 0:
                self.RemoveMovieEventHandler(instId, handlerId)
                return

            if self.m_movieEventHandlersByFullName is None:
                return

            boolean, handlers = self.m_movieEventHandlersByFullName.TryGetValue(arg)
            if not boolean:
                return

            handlers.remove(handlerId)
            movie = self.SearchMovieInstance(arg)
            if movie is not None:
                movie.SetHandlers(handlers)

    def ClearMovieEventHandler(self, arg, *args):
        if len(arg) is 0:
            if isinstance(arg, int):
                if arg < 0 or arg >= len(self.m_instances):
                    return

                handlers = self.m_movieEventHandlers[arg]
                if handlers is None:
                    return

                handlers.Clear()
                movie = self.SearchMovieInstanceByInstanceId(arg)
                if movie is not None:
                    movie: Movie
                    movie.SetHandlers(handlers)
            else:
                instId = self.SearchInstanceId(self.GetStringId(arg))

                if instId >= 0:
                    self.ClearMovieEventHandler(instId)
                    return

                if self.m_movieEventHandlersByFullName is None:
                    return

                boolean, handlers = self.m_movieEventHandlersByFullName.TryGetValue(arg)
                if not boolean:
                    return

                handlers.Clear()
                movie = self.SearchMovieInstance(arg)
                if movie is not None:
                    movie.SetHandlers(handlers)
        else:
            if isinstance(arg, int):
                if arg < 0 or arg >= len(self.m_instances):
                    return

                handlers = self.m_movieEventHandlers[arg]
                if handlers is None:
                    return

                handlers.Clear(args[0])
                movie = self.SearchMovieInstanceByInstanceId(arg)
                if movie is not None:
                    movie: Movie
                    movie.SetHandlers(handlers)
            else:
                instId = self.SearchInstanceId(self.GetStringId(arg))

                if instId >= 0:
                    self.ClearMovieEventHandler(instId, args[0])
                    return

                if self.m_movieEventHandlersByFullName is None:
                    return

                boolean, handlers = self.m_movieEventHandlersByFullName.TryGetValue(arg)
                if not boolean:
                    return

                handlers.Clear(args[0])
                movie = self.SearchMovieInstance(arg)
                if movie is not None:
                    movie.SetHandlers(handlers)

    def SetMovieEventHandler(self, arg, load=None, postLoad=None, unload=None, enterFrame=None, update=None,
                             render=None):
        self.ClearMovieEventHandler(arg)
        return self.AddMovieEventHandler(arg, load, postLoad, unload, enterFrame, update, render)

    def GetButtonEventHandlers(self, b):
        if self.m_buttonEventHandlersByFullName is not None:
            fullName = b.GetFullName()
            if fullName is not None:
                boolean, handlers = self.m_buttonEventHandlersByFullName.TryGetValue(fullName)
                if boolean:
                    return handlers

        instId = b.instanceId
        if instId < 0 or instId >= len(self.m_instances):
            return None
        return self.m_buttonEventHandlers[instId]

    def AddButtonEventHandler(self, arg, load=None, unload=None, enterFrame=None, update=None, render=None, press=None,
                              release=None, rollOver=None, rollOut=None, keyPress=None):
        self.interactive = True
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_instances):
                return -1
            handlers = self.m_buttonEventHandlers[arg]
            if handlers is None:
                handlers = ButtonEventHandlers()
                self.m_buttonEventHandlers[arg] = handlers

            handlerId = self.GetEventOffset()
            handlers.Add(handlerId, load, unload, enterFrame, update, render, press, release, rollOver, rollOut,
                         keyPress)

            button = self.SearchButtonInstanceByInstanceId(arg)
            if button is not None:
                button: Button
                button.SetHandlers(handlers)
            return handlerId
        else:
            instId = self.SearchInstanceId(self.GetStringId(arg))
            if instId >= 0:
                return self.AddButtonEventHandler(instId, load, unload, enterFrame, update, render, press, release,
                                                  rollOver, rollOut, keyPress)

            if "." not in arg:
                return -1

            if self.m_buttonEventHandlersByFullName is None:
                self.m_buttonEventHandlersByFullName = ButtonEventHandlersDictionary()

            boolean, handlers = self.m_buttonEventHandlersByFullName.TryGetValue(arg)
            if not boolean:
                handlers = ButtonEventHandlers()
                self.m_buttonEventHandlersByFullName[arg] = handlers

            handlerId = self.GetEventOffset()
            handlers.Add(handlerId, load, unload, enterFrame, update, render, press, release, rollOver, rollOut,
                         keyPress)

            button = self.SearchButtonInstance(arg)
            if button is not None:
                button: Button
                button.SetHandlers(handlers)
            return handlerId

    def RemoveButtonEventHandler(self, arg, handlerId):
        if isinstance(arg, int):
            if arg < 0 or arg >= len(self.m_instances):
                return

            handlers = self.m_buttonEventHandlers[arg]
            if handlers is None:
                return

            handlers.Remove(handlerId)
            button = self.SearchButtonInstanceByInstanceId(arg)
            if button is not None:
                button: Button
                button.SetHandlers(handlers)
        else:
            instId = self.SearchInstanceId(self.GetStringId(arg))
            if instId >= 0:
                self.RemoveButtonEventHandler(instId, handlerId)
                return

            if self.m_buttonEventHandlersByFullName is None:
                return

            boolean, handlers = self.m_buttonEventHandlersByFullName.TryGetValue(arg)
            if not boolean:
                return

            handlers.remove(handlerId)
            button = self.SearchButtonInstance(arg)
            if button is not None:
                button: Button
                button.SetHandlers(handlers)

    def ClearButtonEventHandler(self, arg, *args):
        if len(arg) is 0:
            if isinstance(arg, int):
                if arg < 0 or arg >= len(self.m_instances):
                    return

                handlers = self.m_buttonEventHandlers[arg]
                if handlers is None:
                    return

                handlers.Clear()
                button = self.SearchButtonInstanceByInstanceId(arg)
                if button is not None:
                    button: Button
                    button.SetHandlers(handlers)
            else:
                instId = self.SearchInstanceId(self.GetStringId(arg))

                if instId >= 0:
                    self.ClearButtonEventHandler(instId)
                    return

                if self.m_buttonEventHandlersByFullName is None:
                    return

                boolean, handlers = self.m_buttonEventHandlersByFullName.TryGetValue(arg)
                if not boolean:
                    return

                handlers.Clear()
                button = self.SearchButtonInstance(arg)
                if button is not None:
                    button.SetHandlers(handlers)
        else:
            if isinstance(arg, int):
                if arg < 0 or arg >= len(self.m_instances):
                    return

                handlers = self.m_buttonEventHandlers[arg]
                if handlers is None:
                    return

                handlers.Clear(args[0])
                button = self.SearchButtonInstanceByInstanceId(arg)
                if button is not None:
                    button: Button
                    button.SetHandlers(handlers)
            else:
                instId = self.SearchInstanceId(self.GetStringId(arg))

                if instId >= 0:
                    self.ClearButtonEventHandler(instId, args[0])
                    return

                if self.m_buttonEventHandlersByFullName is None:
                    return

                boolean, handlers = self.m_buttonEventHandlersByFullName.TryGetValue(arg)
                if not boolean:
                    return

                handlers.Clear(args[0])
                button = self.SearchButtonInstance(arg)
                if button is not None:
                    button: Button
                    button.SetHandlers(handlers)

    def SetButtonEventHandler(self, arg, load=None, unload=None, enterFrame=None, update=None,
                              render=None, press=None, release=None, rollOver=None, rollOut=None, keyPress=None):
        self.ClearButtonEventHandler(arg)
        return self.AddButtonEventHandler(arg, load, unload, enterFrame, update, render, press, release, rollOver,
                                          rollOut, keyPress)

    # class RendererFactory(IRendererFactory):
    #     def __init__(self, data, resourceCache, cache, stage, textInSubpixel, needsClear, quirkyClearRect):
    #         self.blendMode = "normal"
    #         self.maskMode = "normal"
    #         self.stage = stage
    #
    #         if stage.width == 0 and stage.height == 0:
    #             stage.width = data.header.width
    #             stage.height = data.header.height
    #
    #     def BeginRender(self, ctx):
    #         print("Pre-Render func")
    #
    #     def Render(self, ctx, cmd):
    #         print("Render me!")
    #
    #     def EndRender(self, ctx):
    #         print("Post render!")
    #
    # class ResourceCache:
    #     @staticmethod
    #     def get():
    #         return lwf.ResourceCache()
    #
    #     def __init__(self):
    #         self.cache = {}
    #         self.lwfInstanceIndex = 0
    #         self.canvasIndex = 0
    #
    #     def getRendererName(self):
    #         return "Canvas"
    #
    #     def newFactory(self, settings, cache, data):
    #         return lwf.RendererFactory(data, self, cache, settings['stage'],
    #                                settings['textInSubpixel'] if 'textInSubpixel'in settings else False,
    #                                settings['needsClear'] if 'needsClear'in settings else True,
    #                                settings['quirkyClearRect'] if 'quirkyClearRect' in settings else False)
    #
    #     def generateImages(self, settings, imageCache, texture, image):
    #         imageCache[texture.filename] = texture
    #         # super().generateImages(settings, imageCache, texture, image)
    #
    #     def LoadLWF(self, settings):
    #         lwfUrl = settings['prefix'] + settings['lwf']
    #         settings['error'] = []
    #         if lwfUrl in self.cache:
    #             return self.cache[lwfUrl]
    #         file = open(lwfUrl, 'rb').read()
    #         data = Data(file)
    #         self.cache[lwfUrl] = data
    #         settings['data'] = data
    #         onload = settings['onload']
    #         onload(settings)
    #         return

    # class CustomImage:
    #
    #     def __init__(self):
    #         self.source = ""
    #         self.data = None
    #
    #     @staticmethod
    #     def load_image(cache, RCache, image, texture, url, settings, data):
    #         image.data = Image(source=url)
    #
    #         cache[texture.filename] = image.data
    #         if texture.filename in settings['_alphaMap']:
    #             d = settings['_alphaMap'][texture.filename]
    #             jpg = d[0]
    #             alpha = d[1]
    #             jpgImg = cache[jpg.filename]
    #             alphaImg = cache[alpha.filename]
    #             if jpgImg and alphaImg:
    #                 (canvas, ctx) = RCache.createCanvas(jpgImg.width, jpgImg.height)
    #                 ctx.drawImage(jpgImg, 0, 0, jpgImg.width, jpgImg.height, 0, 0, jpgImg.width,
    #                               jpgImg.height)
    #                 ctx.globalCompositeOperation = "destination-in"
    #                 ctx.drawImage(alphaImg, 0, 0, alphaImg.width, alphaImg.height, 0, 0, jpgImg.width,
    #                               jpgImg.height)
    #                 ctx.globalCompositeOperation = "source-over"
    #                 del cache[jpg.filename]
    #                 del cache[alpha.filename]
    #                 cache[jpg.filename] = canvas
    #                 RCache.generateImages(settings, cache, jpg, canvas)
    #             else:
    #                 RCache.generateImages(settings, cache, texture, image.data)
    #             RCache.loadImagesCallback(settings, cache, data)
    #
    # class CustomCanvas(Widget):
    #     # Every Custom Canvas will store every instruction in a InstructionGroup
    #     # This will allow us to pass a variety of arguments into draw Image
    #     def __init__(self):
    #         super().__init__()
    #         self.hasTransform = False
    #         self.group = InstructionGroup()
    #         self._group = InstructionGroup()
    #         self.globalCompositeOperation = "source-over"
    #         self.globalAlpha = 1
    #         self.style = {}
    #         self.backgroundColor = Color(0, 0, 0, 1)
    #         self.fillStyle = "#000000"  # can be a color #000000 or "gradient" or "pattern"
    #
    #     def getContext(self):
    #         return self
    #
    #     def setTransform(self, scaleX, skew1, skew0, scaleY, translateX, translateY):
    #         if skew1 != 0 or skew0 != 0:
    #             raise Exception("Skewing is not implemented!")
    #         if self.hasTransform:
    #             self.group.add(PopMatrix())
    #             self.hasTransform = False
    #         self.group.add(PushMatrix())
    #         self.hasTransform = True
    #         if scaleX != 1 or scaleY != 1:
    #             self.group.add(Scale(scaleX, scaleY, 0))
    #         if translateX != 0 or translateY != 0:
    #             self.group.add(Translate(translateX, translateY))
    #
    #     def translate(self, x, y):
    #         if self.hasTransform:
    #             self.group.add(Translate(x, y))
    #         else:
    #             self.group.add(PushMatrix())
    #             self.hasTransform = True
    #             self.group.add(Translate(x, y))
    #
    #     def fillRect(self, x, y, w, h):
    #         self.rect(x, y, w, h)
    #
    #     def rect(self, x, y, w, h):  # should be the same as a fillRect
    #         if self.fillStyle == "pattern":
    #             # is an image pattern
    #             self.group.add(Rectangle(pos=(x, y), size=(w, h), source=self.pattern, tex_coords=self.tex_coords))
    #         elif self.fillStyle == "gradient":
    #             self.group.add(Rectangle(pos=(x, y), size=(w, h), texture=self.gradient, tex_coords=self.tex_coords))
    #         else:
    #             # is a color
    #             self.parseColor(self.fillStyle)
    #             self.group.add(Rectangle(pox=(x, y), size=(w, h)))
    #         self.draw()
    #
    #     def clearRect(self, x, y, w, h):
    #         # use background color to write over
    #         print(self.style)
    #
    #         if x <= 0 and y <= 0 and w >= self.width and h >= self.height:
    #             # Is a full Screen Clear, clean-up resources
    #             self.group = InstructionGroup()
    #             self._group = InstructionGroup()
    #             self.canvas.clear()
    #         self.group.add(self.backgroundColor)
    #         self.group.add(Rectangle(pos=(x, y), size=(w, h)))
    #         self.draw()
    #
    #     # Removes the instructions from the buffer and adds them to the canvas
    #     def draw(self):
    #         for instruction in self.group.children:
    #             # We may have an extra bind texture for every InstructionGroup()
    #             # If it causes problems, then filter them out.
    #             print("Adding ", instruction, " to the canvas!")
    #             self.group.remove(instruction)
    #             self._group.add(instruction)
    #             self.canvas.add(instruction)
    #
    #     def drawImage(self, *args):
    #         # img is either a canvas with instructions or a image
    #         if len(args) == 3:
    #             # img, x, y
    #             img = args[0]
    #             sx = 0
    #             sy = 0
    #             swidth = 1
    #             sheight = 1
    #             dx = args[1]
    #             dy = args[2]
    #             dwidth = img.width
    #             dheight = img.height
    #         elif len(args) == 5:
    #             # img, x, y, width, height
    #             img = args[0]
    #             sx = 0
    #             sy = 0
    #             swidth = 0
    #             sheight = 0
    #             dx = args[1]
    #             dy = args[2]
    #             dwidth = args[3]
    #             dheight = args[4]
    #         elif len(args) == 9:
    #             # img, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight
    #             img = args[0]
    #             sx = self.normalize(args[1], img.width)
    #             sy = self.normalize(args[2], img.height)
    #             swidth = self.normalize(args[3], img.width)
    #             sheight = self.normalize(args[4], img.height)
    #             dx = args[5]
    #             dy = args[6]
    #             dwidth = args[7]
    #             dheight = args[8]
    #         else:
    #             raise Exception("Incorrect method call for draw image!")
    #         # now that we have our vars, we need to sort our composite and image types
    #         if isinstance(img, LWF.CustomCanvas):
    #             # I am not sure how to sscale these down. ???
    #             if sx >= 0 or sy >= 0 or swidth <= 1 or sheight <= 1:
    #                 raise Exception("Unsupported Canvas operation. Cannot Scale already drawn canvas instructions!")
    #             for instruction in LWF.CustomCanvas._group.children:
    #                 self.group.add(instruction)
    #         else:
    #             tex_coords = [sx, sy, sx + swidth, sy, sx + swidth, sy + sheight, sx, sy + sheight]
    #             # top-left, top-right, right, left
    #             self.group.add(
    #                 Rectangle(pos=(dx, dy), size=(dwidth, dheight), texture=img.texture, tex_coords=tex_coords))
    #
    #         print(self.globalCompositeOperation + " was ignored!")
    #         # Do not currently do anything with self.globalCompositeOperation
    #         self.draw()
    #
    #     def parseColor(self, color):
    #         # Once I have a base working with this method, change to use Color by default
    #         if re.match('#[0-9]{6}', color):
    #             # make a hex color to rgba
    #             self.group.add(KivyColor(int(color[1:3]), int(color[3:5]), int(color[5:7]), 1 * self.globalAlpha))
    #         elif re.match('rgb\([0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?\)', color):
    #             r = re.match('[0-9](\.[0-9])?', color)
    #             g = re.match('[0-9](\.[0-9])?', color[len(r.string) + 1 + 4:])
    #             b = re.match('[0-9](\.[0-9])?', color[len(r.string) + len(g.string) + 2 + 4:])
    #             self.group.add(KivyColor(float(r.string), float(g.string), float(b.string), 1 * self.globalAlpha))
    #         elif re.match('rgba\([0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?\)', color):
    #             r = re.match('[0-9](\.[0-9])?', color)
    #             g = re.match('[0-9](\.[0-9])?', color[len(r.string) + 1 + 5:])
    #             b = re.match('[0-9](\.[0-9])?', color[len(r.string) + len(g.string) + 2 + 5:])
    #             a = re.match('[0-9](\.[0-9])?', color[len(r.string) + len(g.string) + len(b.string) + 3 + 5])
    #             self.group.add(
    #                 KivyColor(float(r.string), float(g.string), float(b.string), float(a.string) * self.globalAlpha))
    #         else:
    #             raise Exception("The color/filltype is not supported/implemented!!! ", color)
    #
    #     def createGradient(self, direction, *args):
    #         if direction == "horizontal":
    #             texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
    #         elif direction == "vertical":
    #             texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
    #         else:
    #             raise Exception("Unsupported gradient direction")
    #         buf = bytes([int(v * 255) for v in chain(*args)])  # flattens
    #         texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    #         self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]
    #         self.gradient = texture
    #
    #     def createPattern(self, image, wrap):
    #         self.fillStyle = "pattern"
    #         image.wrap = wrap
    #         self.pattern = image
    #         self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]
    #
    #     def normalize(self, value, max):
    #         return value / max
    #
    # class RenderCommand:
    #     def __init__(self):
    #         self.renderCount = 0
    #         self.renderingIndex = 0
    #         self.alpha = 0
    #         self.blendMode = 0
    #         self.maskMode = 0
    #         self.matrix = None
    #         self.image = None
    #         self.pattern = None
    #         self.u = 0
    #         self.v = 0
    #         self.w = 0
    #         self.h = 0
    #
    # class BaseRenderCommand:
    #     def __init__(self):
    #         self.renderCount = 0
    #         self.renderingIndex = 0
    #         self.isBitmap = False
    #         self.renderer = None
    #         self.matrix = None
    #         self.maskMode = 0
    #
    # class BitmapContext:
    #     def __init__(self, factory, data, bitmapEx):
    #         self.factory = factory
    #         self.data = data
    #         self.fragment = self.data.textureFragments[bitmapEx.textureFragmentId]
    #         texture = self.data.textures[self.fragment.textureId]
    #         if isinstance(self.factory.cache, dict):
    #             self.image = self.factory.cache[texture.filename]
    #         else:
    #             self.image = self.factory.cache.cache[texture.filename]
    #
    #         imageWidth = self.image.width
    #         withPadding = True if re.match('_withpadding', texture.filename) else False
    #         if withPadding:
    #             imageWidth -= 2
    #         imageScale = imageWidth / texture.width
    #         self.scale = 1 / (texture.scale * imageScale)
    #
    #         repeat = None
    #         if (bitmapEx.attribute & Format.BitmapEx.Attribute.REPEAT_S) != 0:
    #             repeat = 'repeat-x'
    #         if (bitmapEx.attribute & Format.BitmapEx.Attribute.REPEAT_T) != 0:
    #             if repeat != None:
    #                 repeat = "repeat"
    #             else:
    #                 repeat = "repeat-y"
    #         if repeat is not None:
    #             # look up this function and what it does in javascript make a port
    #             self.pattern = self.factory.stageContext.createPattern(self.image, repeat)
    #         else:
    #             self.pattern = None
    #
    #         x = self.fragment.x
    #         y = self.fragment.y
    #         u = self.fragment.u
    #         v = self.fragment.v
    #         w = self.fragment.w
    #         h = self.fragment.h
    #
    #         if withPadding:
    #             x -= 1
    #             y -= 1
    #             w += 2
    #             h += 2
    #
    #         bu = bitmapEx.u * w
    #         bv = bitmapEx.v * h
    #         bw = bitmapEx.w
    #         bh = bitmapEx.h
    #
    #         x += bu
    #         y += bv
    #         u += bu
    #         v += bv
    #         w *= bw
    #         h *= bh
    #
    #         self.x = round(x * imageScale)
    #         self.y = round(y * imageScale)
    #         self.u = round(u * imageScale)
    #         self.v = round(v * imageScale)
    #         if self.fragment.rotated:
    #             self.w = round(h * imageScale)
    #             self.h = round(w * imageScale)
    #         else:
    #             self.w = round(w * imageScale)
    #             self.h = round(h * imageScale)
    #         if self.u + self.w > self.image.width:
    #             self.w = self.image.width - self.u
    #         if self.v * self.h > self.image.height:
    #             self.h = self.image.height - self.v
    #         self.imageHeight = h * imageScale
    #
    # class BitmapRenderer:
    #     def __init__(self, context):
    #         self.context = context
    #         fragment = self.context.fragment
    #         self.matrix = Matrix(0, 0, 0, 0, 0, 0)
    #         if fragment.rotated or self.context.x != 0 or self.context.y != 0 or self.context.scale != 1:
    #             self.matrixForAtlas = Matrix()
    #         self.cmd = LWF.RenderCommand()
    #
    #     def destruct(self):
    #         pass
    #
    #     def render(self, m, c, renderingIndex, renderingCount, visible):
    #         if not visible or c.multi.alpha == 0:
    #             return
    #
    #         if self.matrix.SetWithComparing(m):
    #             m = self.matrix
    #             fragment = self.context.fragment
    #             x = self.context.x
    #             y = self.context.y
    #             scale = self.context.scale
    #             if fragment.rotated:
    #                 m = Utility.RotateMatrix(self.matrixForAtlas, m, scale, x, y + self.context.imageHeight)
    #             elif scale != 1 or x != 0 or y != 0:
    #                 m = Utility.ScaleMatrix(self.matrixForAtlas, m, scale, x, y)
    #         else:
    #             if self.matrixForAtlas is not None:
    #                 m = self.matrixForAtlas
    #         self.alpha = c.multi.alpha
    #
    #         f = self.context.factory.lwf.getRendererFactory()
    #         fragment = self.context.fragment
    #         cmd = self.cmd
    #         cmd.alpha = self.alpha
    #         cmd.blendMode = f.blendMode
    #         cmd.maskMode = f.maskMode
    #         cmd.matrix = m
    #         cmd.image = self.context.imageHeight
    #         cmd.pattern = self.context.pattern
    #         cmd.u = self.context.u
    #         cmd.v = self.context.v
    #         cmd.w = self.context.w
    #         cmd.h = self.context.h
    #         self.context.factory.addCommand(renderingIndex, cmd)
    #         return
    #
    # class TextContext:
    #     def __init__(self, factory, data, text):
    #         # not implemented. Do later.
    #         pass
    #
    # class TextRenderer:
    #     def __init__(self, lwf, context, text):
    #         pass  # implement later
    #
    # class DomElementRenderer:
    #     def __init__(self, factory, node):
    #         self.factory = factory
    #         self.node = node
    #         self.appended = False
    #         self.node.style.visibility = "hidden"
    #         self.matrix = Matrix(0, 0, 0, 0, 0, 0)
    #         self.matrixForDom = Matrix(0, 0, 0, 0, 0, 0)
    #         self.matrixForRender = Matrix(0, 0, 0, 0, 0, 0)
    #         self.alpha = -1
    #         self.zIndex = -1
    #         self.visible = False
    #
    #     def destructor(self):
    #         if self.appended:
    #             self.factory.stage.parent.remove_widget(self.node)
    #
    #     def destruct(self):
    #         if self.factory.resourceCache.constructor is LWF.BaseResourceCache:
    #             self.factory.destructRender(self)
    #         else:
    #             self.destructor()
    #         return
    #
    #     def update(self, m, c):
    #         pass
    #
    #     def render(self, m, c, renderingIndex, renderingCount, visible):
    #         if self.visible is visible:
    #             if visible is False:
    #                 return visible
    #         else:
    #             self.visible = visible
    #             if visible is False:
    #                 self.node.style.visibility = "hidden"
    #                 return
    #             else:
    #                 self.node.style.visibility = "visible"
    #
    #         matrixChanged = self.matrix.SetWithComparing(m)
    #         if not matrixChanged and self.appended and self.alpha == c.multi.alpha and self.zIndex is renderingIndex + renderingCount:
    #             return
    #
    #         if not self.appended:
    #             self.appended = True
    #             self.node.style.position = "absolute"
    #             self.node.style.webkitTransformOrigin = "0px 0px"
    #             self.node.style.display = "block"
    #
    #         raise Exception("NOT IMPLEMENTED")
    #
    # class CanvasLoader:
    #     @staticmethod
    #     def load(d):
    #         if not d or not isinstance(d, bytes):
    #             return None
    #         option = d[Format.Constant.OPTION_OFFSET] & 0xff
    #         if option & Format.Constant.OPTION_COMPRESSED == 0:
    #             print("uncompressed")
    #             return Loader.load(d)
    #         # if compressed
    #         a = [0 for _ in range(len(d))]
    #         for i in range(0, len(d)):
    #             a[i] = d[i] & 0xff
    #         print("compressed")
    #         return Loader.loadArray(a)
    #
    #     def loadArray(self, d):
    #         if not d:
    #             return None
    #         option = d[Format.Constant.OPTION_OFFSET]
    #         if (option & Format.Constant.OPTION_COMPRESSED) == 0:
    #             return Loader.loadArray(d)
    #
    #         header = d[0:Format.Constant.HEADER_SIZE]
    #         compressed = d[Format.Constant.HEADER_SIZE:]
    #         # if compressed
    #         try:  # implement
    #             decompressed = LZMADecompressor.decompress(compressed)
    #         except Exception:
    #             return None
    #         d.header.append(decompressed)
    #         return Loader.loadArray(d)
    #
    # class BaseRendererFactory:
    #     def __init__(self, data, resourceCache, cache, stage, textInSubpixel, use3D, recycleTextCanvas,
    #                  quirkyClearRect):
    #         self.resourceCache = resourceCache
    #         self.cache = cache
    #         self.stage = stage
    #         self.texInSubpixel = textInSubpixel
    #         self.use3D = use3D
    #         self.recycleTextCanvas = recycleTextCanvas
    #         self.quirkyClearRect = quirkyClearRect
    #         self.needsRenderForInactive = True
    #         self.maskMode = "normal"
    #         self.commands = None
    #
    #         self.bitmapContexts = []
    #         for bitmap in data.bitmaps:
    #             if bitmap.textureFragmentId == -1:
    #                 continue
    #             bitmapEx = Format.BitmapEx()
    #             bitmapEx.matrixId = bitmap.matrixId
    #             bitmapEx.textureFragmentId = bitmap.textureFragmentId
    #             bitmapEx.u = 0
    #             bitmapEx.v = 0
    #             bitmapEx.w = 1
    #             bitmapEx.h = 1
    #             bitmapEx.attribute = 0
    #             self.bitmapContexts.append(LWF.BitmapContext(self, data, bitmapEx))
    #
    #         self.bitmapExContexts = []
    #         for bitmapEx in data.bitmapExs:
    #             if bitmapEx.textureFragmentId == -1:
    #                 continue
    #             self.bitmapExContexts.append(LWF.BitmapContext(self, data, bitmapEx))
    #
    #         self.textContexts = []
    #         for text in data.texts:
    #             self.textContexts.append(LWF.TextContext(self, data, text))
    #
    #         # style = self.stage.style
    #         (w, h) = self.getStageSize()
    #         if w == 0 and h == 0:
    #             self.stage.width = str(data.header.width)
    #             self.stage.height = str(data.header.height)
    #
    #         self.initCommands()
    #         self.destructedRenderers = []
    #
    #     def initCommands(self):
    #         if not self.commands or self.commandsCount < len(self.commands) * 0.75:
    #             self.commands = []
    #         self.commandsCount = 0
    #         self.subCommands = None
    #         return
    #
    #     def isMask(self, cmd):
    #         if cmd.maskMode == "erase" or cmd.maskMode == "mask" or cmd.maskMode == "alpha":
    #             return True
    #         return False
    #
    #     def isLayer(self, cmd):
    #         return cmd.maskMode == "layer"
    #
    #     def addCommand(self, rIndex, cmd):
    #         cmd.renderCount = self.lwf.renderCount
    #         cmd.renderingIndex = rIndex
    #         if self.isMask(cmd):
    #             if self.subCommands:
    #                 self.subCommands[rIndex] = cmd
    #         else:
    #             if self.isLayer(cmd) and self.commandMaskMode != cmd.maskMode:
    #                 cmd.subCommands = []
    #                 self.subCommands = cmd.subCommands
    #             self.commands[rIndex] = cmd
    #             self.commandsCount += 1
    #         self.commandMaskMode = cmd.maskMode
    #         return
    #
    #     def addCommandToParent(self, lwf):
    #         f = lwf.getRendererFactory()
    #         renderCount = lwf.renderCount
    #         for rIndex in range(0, len(self.commands)):
    #             cmd = self.commands[rIndex]
    #             if not cmd or cmd.renderingIndex != rIndex or cmd.renderCount != renderCount:
    #                 continue
    #             subCommands = cmd.subCommands
    #             cmd.subCommands = None
    #             f.addCommand(rIndex, cmd)
    #             if subCommands:
    #                 for srIndex in range(0, len(subCommands)):
    #                     scmd = subCommands[srIndex]
    #                     if not scmd or scmd.renderingIndex != srIndex or scmd.renderCount != renderCount:
    #                         continue
    #                     f.addCommand(srIndex, scmd)
    #         self.initCommands()
    #         return
    #
    #     def destruct(self):
    #         if self.destructedRenderers:
    #             self.callRendererDestructor()
    #         for context in self.bitmapContexts:
    #             del context
    #         for context in self.bitmapExContexts:
    #             del context
    #         for context in self.textContexts:
    #             del context
    #
    #     def init(self, lwf):
    #         self.lwf = lwf
    #         lwf.stage = self.stage
    #         lwf.resourceCache = self.resourceCache
    #         # if self.setupedDomElementConstructor:
    #         #     return
    #         # self.setupedDomElementConstructor = True
    #         for progObj in lwf.data.programObjects:
    #             name = lwf.data.strings[progObj.stringId]
    #             m = re.match('^DOM_(.*)', name)
    #             if m:
    #                 domName = m[1]
    #
    #                 def do(domName):
    #                     def dom(lwf_, objId, w, h):
    #                         ctor = self.resourceCache.dolElementCOnstructor
    #                         if not ctor:
    #                             return None
    #                         domElement = ctor(lwf_, domName, w, h)
    #                         if not domElement:
    #                             return None
    #                         return LWF.DomElementRenderer(self, domElement)
    #
    #                     lwf.setProgramObjectConstructor(name, dom)
    #
    #                 do(domName)
    #
    #     def destructRenderer(self, renderer):
    #         self.destructedRenderers.append(renderer)
    #         return
    #
    #     def callRendererDestructor(self):
    #         for renderer in self.destructedRenderers:
    #             renderer.destructor()
    #         self.destructedRenderers = []
    #         return
    #
    #     def beginRender(self, lwf):
    #         if self.destructedRenderers:
    #             self.callRendererDestructor()
    #         return
    #
    #     def render(self, cmd):
    #         renderer = cmd.renderer
    #         node = renderer.node
    #         style = node.style
    #         style.zIndex = renderer.zIndex
    #         m = cmd.matrix
    #
    #         if cmd.maskMode == "mask" or cmd.maskMode == "alpha":
    #             self.renderMasked = True
    #             style.opacity = 0
    #             if self.renderMaskMode != "mask" and self.renderMaskMode != "alpha":
    #                 if node.mask:
    #                     self.mask = node.mask
    #                     style = self.mask.style
    #                 else:
    #                     self.mask = node.mask = LWF.CustomCanvas()
    #                     style = self.mask.style
    #                     style.display = "block"
    #                     style.position = "absolute"
    #                     style.overflow = "hidden"
    #                     style.webkitUserSelect = "none"
    #                     style.webkitTransformOrigin = "0px 0px"
    #                     self.stage.append_widget(self.mask)
    #                 style.width = node.style.width
    #                 style.height = node.style.height
    #                 if not self.maskMatrix:
    #                     self.maskMatrix = Matrix()
    #                     self.maskedMatrix = Matrix()
    #                 Utility.InvertMatrix(self.maskMatrix, m)
    #             else:
    #                 return
    #         elif cmd.maskMode == "layer":
    #             if self.renderMasked:
    #                 if self.renderMaskMode != cmd.maskMode:
    #                     self.mask.style.zIndex = renderer.zIndex
    #                 if node.parent != self.mask:
    #                     node.parent.remove_widget(node)
    #                     self.mask.add_widget(node)
    #                 m = Utility.CalcMatrix(self.maskedMatrix, self.maskMatrix, m)
    #             else:
    #                 if node.parent != self.stage:
    #                     node.parent.remove_widget(node)
    #                     self.stage.add_widget(node)
    #         else:
    #             if node.parent != self.stage:
    #                 node.parent.remove_widget(node)
    #                 self.stage.add_widget(node)
    #         self.renderMaskMode = cmd.maskMode
    #         style.opacity = renderer.alpha
    #         scaleX = round(m.scaleX, 12)
    #         scaleY = round(m.scaleY, 12)
    #         skew1 = round(m.skew1, 12)
    #         skew0 = round(m.skew0, 12)
    #         translateX = round(m.translateX, 12)
    #         translateY = round(m.translateY, 12)
    #         if self.use3D:
    #             style.webkitTransform = "matrix3d(" + str(scaleX) + "," + str(skew1) + ",0,0," + str(skew0) + "," + str(
    #                 scaleY) + ",0,0,0,0,1,0," + str(translateX) + "," + str(translateY) + ",0,1)"
    #         else:
    #             style.webkitTransform = "matrix(" + str(scaleX) + "," + str(skew1) + "," + str(skew0) + "," + str(
    #                 scaleY) + "," + str(translateX) + "," + str(translateY)
    #         return
    #
    #     def endRender(self, lwf):
    #         if lwf.parent:
    #             self.addCommandToParent(lwf)
    #             if self.destructedRenderers:
    #                 self.callRendererDestructor()
    #             return
    #
    #         self.renderMaskMode = "normal"
    #         self.renderMasked = False
    #         renderCount = lwf.renderingCount
    #         for rIndex in range(0, len(self.commands)):
    #             cmd = self.commands[rIndex]
    #             if not cmd or cmd.renderingIndex != rIndex or cmd.renderCount != renderCount:
    #                 continue
    #             if cmd.subCommands:
    #                 for srIndex in range(0, len(cmd.subCommands)):
    #                     scmd = cmd.subCommands[srIndex]
    #                     if not scmd or scmd.renderingIndex != srIndex or scmd.renderCount != renderCount:
    #                         continue
    #                     self.render(scmd)
    #                 self.render(cmd)
    #
    #             self.initCommands()
    #
    #             if self.destructedRenderers:
    #                 self.callRendererDestructor()
    #             return
    #
    #     def setBlendMode(self, blendMode):
    #         self.blendMode = blendMode
    #
    #     def setMaskMode(self, maskMode):
    #         self.maskMode = maskMode
    #
    #     def constructBitmap(self, lwf, objectId, bitmap):
    #         context = self.bitmapContexts[objectId]
    #         if context:
    #             return LWF.BitmapRenderer(context)
    #         return None
    #
    #     def constructBitmapEx(self, lwf, objectId, bitmapEx):
    #         context = self.bitmapExContexts[objectId]
    #         if context:
    #             return LWF.BitmapRenderer(context)
    #         return None
    #
    #     def constructText(self, lwf, objectId, text):
    #         context = self.textContexts[objectId]
    #         if context:
    #             return LWF.TextRenderer(lwf, context, text)
    #
    #     def constructParticle(self, lwf, objectId, particle):
    #         ctor = self.resourceCache.particleConstructor
    #         particleData = lwf.data.particleDatas[particle.particleDataId]
    #         if ctor:
    #             return ctor(lwf, lwf.data.strings[particleData.stringId])
    #         return None
    #
    #     def convertColor(self, lwf, d, c, t):
    #         Utility.CalcColor(d, c, t)
    #         d.red = round(d.red * 255)
    #         d.green = round(d.green * 255)
    #         d.blue = round(d.blue * 255)
    #         return
    #
    #     def convertRGB(self, c):
    #         r = round(c.red * 255)
    #         g = round(c.green * 255)
    #         b = round(c.blue * 255)
    #         return "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"
    #
    #     def getStageSize(self):
    #         r = self.getBoundingRect(self.stage)
    #         return (r.width, r.height)
    #
    #
    #     def getBoundingRect(self, widget):
    #         box = BoundingRect()
    #         box.width = widget.width
    #         box.height = widget.height
    #         box.x, box.y = widget.pos
    #         box.left = box.x
    #         box.top = box.y
    #         box.right = box.left + box.width
    #         box.bottom = box.top + box.height
    #         return box
    #
    #
    #     def fitForHeight(self, lwf):
    #         (w, h) = self.getStageSize()
    #         if h != 0 and h != lwf.data.header.height:
    #             lwf.fitForHeight(w, h)
    #         return
    #
    #     def fitForWidth(self, lwf):
    #         (w, h) = self.getStageSize()
    #         if w != 0 and w != lwf.data.header.width:
    #             lwf.fitForWidth(w, h)
    #         return
    #
    #     def scaleForHeight(self, lwf):
    #         (w, h) = self.getStageSize()
    #         if h != 0 and h != lwf.data.header.height:
    #             lwf.scaleForHeight(w, h)
    #         return
    #
    #     def scaleForWidth(self, lwf):
    #         (w, h) = self.getStageSize()
    #         if w != 0 and w != lwf.data.header.width:
    #             lwf.scaleForWidth(w, h)
    #         return
    #
    #     def parseBackgroundColor(self, v):
    #         if isinstance(v, float) or isinstance(v, int):
    #             bgColor = v
    #         elif isinstance(v, str):
    #             bgColor = int(v, 16)
    #         elif isinstance(v, LWF):
    #             lwf = v
    #             bgColor = lwf.data.header.backgroundColor
    #             bgColor |= 0xff << 24
    #         else:
    #             return 255, 255, 255, 255
    #         a = ((bgColor >> 24) & 0xff)
    #         r = ((bgColor >> 16) & 0xff)
    #         g = ((bgColor >> 8) & 0xff)
    #         b = ((bgColor >> 0) & 0xff)
    #         return r, g, b, a
    #
    #     def setBackgroundColor(self, v):
    #         (r, g, b, a) = self.parseBackgroundColor(v)
    #         self.stage.style.backgroundColor = "rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(a / 255) + ")"
    #         return
    #
    #     def clearCanvasRect(self, canvas, ctx):
    #         ctx.clearRect(0, 0, canvas.width + 1, canvas.height + 1)
    #         if self.quirkyClearRect:
    #             canvas.width = canvas.width
    #         return
    #
    #     def setFont(self, oldFontName, newFontName):
    #         oldFontName += ",sans-serif"
    #         newFontName += ",sans-serif"
    #         for context in self.textContexts:
    #             if context.fontName == oldFontName:
    #                 context.fontName = newFontName
    #                 context.fontChanged = True
    #         return
    #
    # class BaseResourceCache:
    #     _instance = None
    #
    #     @staticmethod
    #     def get():
    #         if LWF.BaseResourceCache._instance is None:
    #             LWF.BaseResourceCache._instance = LWF.BaseResourceCache()
    #         return LWF.BaseResourceCache._instance
    #
    #     def __init__(self):
    #         self.cache = {}
    #         self.lwfInstanceIndex = 0
    #         self.canvasIndex = 0
    #
    #     def getRendererName(self):
    #         return "webkitCSS"
    #
    #     def clear(self):
    #         for k, cache in self.cache:
    #             for kk, lwfInstance in cache.instances:
    #                 lwfInstance.destroy()
    #         self.cache = {}
    #
    #     def getTextureURL(self, settings, data, texture):
    #         if 'imagePrefix' in settings:
    #             prefix = settings['imagePrefix']
    #         elif 'prefix' in settings:
    #             prefix = settings['prefix'];
    #         else:
    #             prefix = ""
    #
    #         if 'imageSuffix' in settings:
    #             sufix = settings['imageSuffix']
    #         else:
    #             suffix = ""
    #
    #         if 'imageQueryString' in settings:
    #             queryString = settings['imageQueryString']
    #         else:
    #             queryString = ""
    #
    #         if len(queryString) > 0:
    #             queryString = "?" + queryString
    #
    #         # imageMap = settings['imageMap']
    #         url = texture.filename
    #         # if callable(imageMap):
    #         #     newUrl = imageMap(settings, url)
    #         # if newUrl:
    #         #     url = newUrl
    #         # elif isinstance(imageMap, dict):
    #         #     newUrl = imageMap[url]
    #         #     if newUrl:
    #         #         url = newUrl
    #         if not (re.match('^/', url) or re.match('^https?://', url)):
    #             url = prefix + url
    #         url = url.replace('(\.gif|\.png|\.jpg)', suffix + "$1" + queryString)
    #         print("returning! ", url)
    #         return url
    #
    #     def checkTextures(self, settings, data):
    #         settings['_alphaMap'] = {}
    #         settings['_colorMap'] = {}
    #         settings['_textures'] = []
    #
    #         re_o = '_atlas(.*)_info_' + '([0-9])_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)'
    #         re_rgb = '(.*)_rgb_([0-9a-f]{6})(.*)$'
    #         re_rgb10 = '(.*)_rgb_([0-9]*),([0-9]*),([0-9]*)(.*)$'
    #         re_rgba = '(.*)_rgba_([0-9a-f]{8})(.*)$'
    #         re_rgba10 = '(.*)_rgba_([0-9]*),([0-9]*),([0-9]*),([0-9]*)(.*)$'
    #         re_add = '(.*)_add_([0-9a-f]{6})(.*)$'
    #         re_add10 = '(.*)_add_([0-9]*),([0-9]*),([0-9]*)(.*)$'
    #
    #         for texture in data.textures:
    #             orig = None
    #             if re.match(re_rgb, texture.filename):
    #                 m = re.match(re_rgb, texture.filename)
    #                 orig = m[1] + m[3]
    #                 colorOp = "rgb"
    #                 colorValue = m[2]
    #             elif re.match(re_rgb10, texture.filename):
    #                 m = re.match(re_rgb10, texture.filename)
    #                 orig = m[1] + m[5]
    #                 colorOp = "rgb"
    #                 r = hex(int(m[2], 10))[2:]
    #                 g = hex(int(m[3], 10))[2:]
    #                 b = hex(int(m[4], 10))[2:]
    #                 colorValue = ("0" if len(r) == 1 else "") + r + \
    #                              ("0" if len(g) == 1 else "") + g + \
    #                              ("0" if len(b) == 1 else "") + b
    #             elif re.match(re_rgba, texture.filename):
    #                 m = re.match(re_rgba, texture.filename)
    #                 orig = m[1] + m[3]
    #                 colorOp = "rgba"
    #                 colorValue = m[2]
    #             elif re.match(re_rgba10, texture.filename):
    #                 m = re.match(re_rgba10, texture.filename)
    #                 orig = m[1] + m[6]
    #                 colorOp = "rgba"
    #                 r = hex(int(m[2], 10))[2:]
    #                 g = hex(int(m[3], 10))[2:]
    #                 b = hex(int(m[4], 10))[2:]
    #                 a = hex(int(m[5], 10))[2:]
    #                 colorValue = ("0" if len(r) == 1 else "") + r + \
    #                              ("0" if len(g) == 1 else "") + g + \
    #                              ("0" if len(b) == 1 else "") + b + \
    #                              ("0" if len(a) == 1 else "") + a
    #             elif re.match(re_add, texture.filename):
    #                 m = re.match(re_add, texture.filename)
    #                 orig = m[1] + m[3]
    #                 colorOp = "add"
    #                 colorValue = m[2]
    #             elif re.match(re_add10, texture.filename):
    #                 m = re.match(re_add10, texture.filename)
    #                 orig = m[1] + m[5]
    #                 colorOp = "add"
    #                 r = hex(int(m[2], 10))[2:]
    #                 g = hex(int(m[3], 10))[2:]
    #                 b = hex(int(m[4], 10))[2:]
    #                 colorValue = ("0" if len(r) == 1 else "") + r + \
    #                              ("0" if len(g) == 1 else "") + g + \
    #                              ("0" if len(b) == 1 else "") + b
    #
    #             if orig:
    #                 ma = re.match(re_o, texture.filename)
    #                 if ma:
    #                     orig = ma[1]
    #                     rotated = ma[2] == "1"
    #                     u = int(ma[3], 10)
    #                     v = int(ma[4], 10)
    #                     w = int(ma[5], 10)
    #                     h = int(ma[6], 10)
    #                     x = int(ma[7], 10)
    #                     y = int(ma[8], 10)
    #                 else:
    #                     rotated = False
    #                     u = 0
    #                     v = 0
    #                     w = None
    #                     h = None
    #                     x = 0
    #                     y = 0
    #                 if orig not in settings['_colorMap']:
    #                     settings['_colorMap'][orig] = []
    #                     settings['_colorMap'][orig].append({
    #                         'filename': texture.filename,
    #                         'colorOp': colorOp,
    #                         'colorValue': colorValue,
    #                         'rotated': rotated,
    #                         'u': u,
    #                         'v': v,
    #                         'w': w,
    #                         'h': h,
    #                         'x': x,
    #                         'y': y
    #                     })
    #                     continue
    #             settings['_textures'].append(texture)
    #             m = re.match('^(.*)_withalpha(.*\.)jpg(.*)$', texture.filename)
    #             if m:
    #                 pngFilename = m[1] + "_alpha" + m[2] + "png" + m[3]
    #                 t = Format.TextureReplacement(pngFilename)
    #                 settings['_textures'].append(t)
    #                 settings['_alphaMap'][texture.filename] = [texture, t]
    #                 settings['_alphaMap'][t.filename] = [texture, t]
    #         return
    #
    #     def onloaddata(self, settings, data, url):
    #         if not data or not data.Check():
    #             settings['error'].append({'url': url, 'reason': 'dataError'})
    #             settings['onload'](settings, None)
    #             return
    #
    #         settings['name'] = data.name
    #
    #         self.checkTextures(settings, data)
    #
    #         # Assume we have no scripts
    #         needsToLoadScript = data.useScript #and !global['lwf]?['Script']?[data.name()]?
    #
    #         self.cache[settings['lwfUrl']]['data'] = data
    #         settings['total'] = len(settings['_textures']) + 1
    #         # if needsToLoadScript:
    #         #   settings.total += 1
    #         settings['loadedCount'] = 1
    #         if 'onprogress' in settings:
    #             on_progress = settings['onprogress']
    #             on_progress(settings, settings['loadedCount'], settings['total'])
    #
    #         # Assume that out lwfs require no scripts
    #         if needsToLoadScript:
    #             pass
    #         #   self.loadJs(settings, data)
    #         else:
    #             self.loadImages(settings, data)
    #         return
    #
    #     def LoadLWF(self, settings):
    #         lwfUrl = settings['lwf']
    #         if not re.match('^/', lwfUrl):
    #             if 'prefix' in settings:
    #                 lwfUrl = settings['prefix'] + lwfUrl
    #         settings['lwfUrl'] = lwfUrl
    #         settings['error'] = []
    #
    #         if lwfUrl in self.cache:
    #             data = self.cache[lwfUrl].data
    #             if data:
    #                 settings['name'] = data.name()
    #                 self.checkTextures(settings, data)
    #                 settings.total = len(settings._textures) + 1
    #                 settings.loadedCount = 1
    #                 if 'onprogress' in settings:
    #                     on_progress = settings['onprogress']
    #                     on_progress(settings, settings.loadedCount, settings.total)
    #                 self.loadImages(settings, data)
    #                 return
    #         self.cache[lwfUrl] = {}
    #         self.loadLWFData(settings, lwfUrl)
    #
    #         # file = open(lwfUrl, "rb")
    #         # data = Data(file.read())
    #         # self.cache[lwfUrl] = data
    #         # settings['data'] = data
    #         # onload = settings['onload']
    #         # onload(settings)
    #         # return
    #
    #     def dispatchOnloaddata(self, settings, url, data):
    #         data = LWF.CanvasLoader.load(data)
    #         print(data)
    #
    #         self.onloaddata(settings, data, url)
    #
    #     def loadLWFData(self, settings, url):
    #         self.dispatchOnloaddata(settings, url, open(url, 'rb').read())
    #
    #     def loadImagesCallback(self, settings, imageCache, data):
    #         print("Images loaded callback!")
    #         settings['loadedCount'] += 1
    #         if settings['loadedCount'] is settings['total']:
    #             print("All images loaded!")
    #             del settings['_alphaMap']
    #             del settings['_colorMap']
    #             del settings['_textures']
    #             if len(settings['error']) > 0:
    #                 del self.cache[settings['lwf']]
    #                 on_load = settings['onload']
    #                 on_load(settings, None)
    #             else:
    #                 self.newLWF(settings, imageCache, data)
    #         else:
    #             print("\nNot all loaded!")
    #         return
    #
    #     def drawImage(self, ctx, image, o, u, v, w, h):
    #         if o.rotates:
    #             m = Matrix()
    #             Utility.RotateMatrix(m, Matrix(), 1, 0, w)
    #             ctx.setTransform(m.scaleX, m.skew1, m.skew0, m.scaleY, m.translateX, m.translateY)
    #         else:
    #             ctx.setTransform(1, 0, 0, 1, 0, 0)
    #         ctx.drawImage(image, u, v, w, h, 0, 0, w, h)
    #         ctx.setTransform(1, 0, 0, 1, 0, 0)
    #         return
    #
    #     def getCanvasName(self):
    #         self.canvasIndex += 1
    #         return "__canvas__" + str(self.canvasIndex)
    #
    #     def createCanvas(self, w, h):
    #         name = self.getCanvasName()
    #         canvas = LWF.CustomCanvas()
    #         canvas.width = w
    #         canvas.height = h
    #         ctx = canvas.getContext()
    #         canvas.name = name
    #         return (canvas, ctx)
    #
    #     def generateImages(self, settings, imageCache, texture, image):
    #         d = settings._colorMap[texture.filename]
    #         if d:
    #             scaleX = image.width / texture.width
    #             scaleY = image.height / texture.height
    #             for o in d:
    #                 u = round(o.u * scaleX)
    #                 v = round(o.v * scaleY)
    #                 w = round((o.w if o.w else texture.width) * scaleX)
    #                 h = round((o.h if o.h else texture.height) * scaleY)
    #                 if o.rotated:
    #                     iw = h
    #                     ih = w
    #                 else:
    #                     iw = w
    #                     ih = h
    #                 (canvas, ctx) = self.createCanvas(w, h)
    #
    #                 if o.colorOp == "rgb":
    #                     ctx.fillStyle = "#" + str(o.colorValue)
    #                     ctx.fillRect(0, 0, w, h)
    #                     ctx.globalCompositeOperation = "destination-in"
    #                     self.drawImage(ctx, image, o, u, v, iw, ih)
    #                 elif o.colorOp == "rgba":
    #                     self.drawImage(ctx, image, o, u, v, iw, ih)
    #                     ctx.globalCompositeOperation = "source-atop"
    #                     val = o.colorValue
    #                     r = int(val[0:2], 16)
    #                     g = int(val[2:2], 16)
    #                     b = int(val[4:2], 16)
    #                     a = int(val[6:2], 16) / 255
    #                     ctx.fillStyle = "rgba(" + str(r) + ", " + str(g) + ", " + str(b) + ", " + str(a) + ")"
    #                     ctx.fillRect(0, 0, w, h)
    #                 elif o.colorOp == "add":
    #                     canvasAdd = LWF.CustomCanvas()
    #                     canvasAdd.width = w
    #                     canvasAdd.height = h
    #                     ctxAdd = canvasAdd.getContext()
    #                     ctxAdd.fillStyle = "#" + str(o.colorValue)
    #                     ctxAdd.fillRect(0, 0, w, h)
    #                     ctxAdd.globalCompositeOperation = "destination-in"
    #                     self.drawImage(ctxAdd, image, o, u, v, iw, ih)
    #                     self.drawImage(ctx, image, o, u, v, iw, ih)
    #                     ctx.globalCompositeOperation = "lighter"
    #                     ctx.drawImage(canvasAdd, 0, 0, canvasAdd.width, canvasAdd.height, 0, 0, canvasAdd.width,
    #                                   canvasAdd.height)
    #                 ctx.globalCompositeOperation = "source-over"
    #                 imageCache[o.filename] = canvas
    #         return
    #
    #     def loadImages(self, settings, data):
    #         imageCache = {}
    #
    #         if len(data.textures) == 0:
    #             self.newLWF(settings, imageCache, data)
    #             return
    #
    #         for texture in settings['_textures']:
    #             url = self.getTextureURL(settings, data, texture)
    #
    #             image = LWF.CustomImage()
    #             try:
    #                 LWF.CustomImage.load_image(imageCache, self, image, texture, url, settings, data)
    #             except Exception:
    #                 settings['error'].append({'url': url, 'reason': "error"})
    #             self.loadImagesCallback(settings, imageCache, data)
    #         print("Finished Loading images!")
    #         return
    #
    #     def newFactory(self, settings, cache, data):
    #
    #         return LWF.BaseRendererFactory(data, self, cache, settings['stage'],
    #                                    settings['textInSubpixel'] if 'textInSubPixel' in settings else False,
    #                                    settings['use3D'] if 'use3D' in settings else False,
    #                                    settings['recycleTextCanvas'] if 'recycleTextCanvas' in settings else False,
    #                                    settings['quirkyClearRect'] if 'quirkyClearRect' in settings else False)
    #
    #     def onloadLWF(self, settings, lwf):
    #         factory = lwf.rendererFactory
    #         print("On Load!")
    #         if 'setBackgroundColor' in settings:
    #             factory.setBackgroundColor(settings['setBackgroundColor'])
    #         elif 'useBackgroundColor' in settings:
    #             factory.setBackgroundColor(lwf)
    #         if 'fitForHeight' in settings:
    #             factory.fitForHeight(lwf)
    #         elif 'fitForWidth' in settings:
    #             factory.fitForWidth(lwf)
    #         on_load = settings['onload']
    #         on_load(settings, lwf)
    #         return
    #
    #     def newLWF(self, settings, imageCache, data):
    #         lwfUrl = settings['lwfUrl']
    #         cache = self.cache[lwfUrl]
    #         factory = self.newFactory(settings, imageCache, data)
    #         # ignoring scripts
    #         # embeddedScript = global["lwf"]?["Script"]?[data.name()] if data.useScript
    #         lwf = LWF(data, factory)
    #         if 'active' in settings:
    #             lwf.active = settings['active']
    #         lwf.url = settings['lwfUrl']
    #         self.lwfInstanceIndex += 1
    #         lwf.lwfInstanceId = self.lwfInstanceIndex
    #         if 'instances' not in cache:
    #             cache['instances'] = {}
    #         cache['instances'][lwf.lwfInstanceId] = lwf
    #         if 'parentLWF' in settings:
    #             parentLWF = settings['parentLWF']
    #             parentLWF.loadedLWFs[lwf.lwfInstanceId] = lwf
    #         if 'preferredFrameRate' in settings:
    #             if 'execLimit' in settings:
    #                 lwf.SetPreferredFrameRate(settings['preferredFrameRate'], settings['execLimit'])
    #             else:
    #                 lwf.SetPreferredFrameRate(settings['preferredFrameRate'])
    #         self.onloadLWF(settings, lwf)
    #         return
    #
    #     def unloadLWF(self, lwf):
    #         cache = self.cache[lwf.url]
    #         if cache:
    #             if lwf.lwfInstanceId:
    #                 del cache.instances[lwf.lwfInstanceId]
    #                 empty = True
    #                 for k, v in cache.instances:
    #                     empty = False
    #                     break
    #                 if empty:
    #                     # we ignore scripts
    #                     #     try:
    #                     #         if cache.scripts:
    #                     #             head = document.getElementsByTagName('head')[0]
    #                     #             for script in cache.scripts
    #                     #                 head.removeChild(script)
    #                     #     catch e
    #                     del self.cache[lwf.url]
    #         return
    #
    #     def loadLWFs(self, settingsArray, onloadall):
    #         loadTotal = len(settingsArray)
    #         loadedCount = 0
    #         errors = None
    #         for settings in settingsArray:
    #             onload = settings['onload']
    #
    #             def do(onload):
    #                 def on_load(lwf):
    #                     if onload:
    #                         onload(lwf)
    #                     if len(settings.error) > 0:
    #                         if errors is not None:
    #                             errors = []
    #                         errors = errors.append(settings.error)
    #                     loadedCount += 1
    #                     if loadTotal == loadedCount:
    #                         onloadall(errors)
    #
    #                 settings['onload'] = on_load
    #
    #             do(onload)
    #             self.LoadLWF(settings)
    #
    #     def getCache(self):
    #         return self.cache
    #
    #     def setParticleConstructor(self, ctor):
    #         self.particleConstructor = ctor
    #         return
    #
    #     # We do not use DOM elements. No need for this
    #     # def setDOMElementCOnstructor(self, ctor):
    #     #     self.domElementConstructor = ctor
    #     #     return
    #
    # class RendererFactory(BaseRendererFactory):
    #     def __init__(self, data, resourceCache, cache, stage, textInSubpixel, needsClear, quirkyClearRect):
    #         self.resourceCache = resourceCache
    #         self.cache = cache
    #         self.stage = stage
    #         self.textInSubPixel = textInSubpixel
    #         self.needsClear = needsClear
    #         self.quirkyClearRect = quirkyClearRect
    #         self.blendMode = "normal"
    #         self.maskMode = "normal"
    #
    #         self.stageContext = self.stage.getContext()
    #         if self.stage.width == 0 and self.stage.height == 0:
    #             self.stage.width = data.header.width
    #             self.stage.height = data.header.height
    #
    #         self.bitmapContexts = []
    #         for bitmap in data.bitmaps:
    #             if bitmap.textureFragmentId == -1:
    #                 continue
    #             bitmapEx = Format.BitmapEx()
    #             bitmapEx.matrixId = bitmap.matrixId
    #             bitmapEx.textureFragmentId = bitmap.textureFragmentId
    #             bitmapEx.u = 0
    #             bitmapEx.v = 0
    #             bitmapEx.w = 1
    #             bitmapEx.h = 1
    #             bitmapEx.attribute = 0
    #             self.bitmapContexts.append(LWF.BitmapContext(self, data, bitmapEx))
    #
    #         self.bitmapExContexts = []
    #         for bitmapEx in data.bitmapExs:
    #             if bitmapEx.textureFragmentId == -1:
    #                 continue
    #             self.bitmapExContexts.append(LWF.BitmapContext(self, data, bitmapEx))
    #
    #         self.textContexts = []
    #         for text in data.texts:
    #             self.textContexts.append(LWF.TextContext(self, data, text))
    #
    #         self.initCommands()
    #
    #     def destruct(self):
    #         for context in self.bitmapContexts:
    #             del context
    #         for context in self.bitmapExContexts:
    #             del context
    #         for context in self.textContexts:
    #             del context
    #         return
    #
    #     def setBlendMode(self, blendMode):
    #         self.blendMode = blendMode
    #
    #     def setMaskMode(self, maskMode):
    #         self.maskMode = maskMode
    #
    #     def constructBitmap(self, lwf, objectId, bitmap):
    #         context = self.bitmapContexts[objectId]
    #         if context:
    #             return LWF.BitmapRenderer(context)
    #         return None
    #
    #     def constructBitmapEx(self, lwf, objectId, bitmapEx):
    #         context = self.bitmapExContexts[objectId]
    #         if context:
    #             return LWF.BitmapRenderer(context)
    #         return None
    #
    #     def constructText(self, lwf, objectId, text):
    #         context = self.textContexts[objectId]
    #         if context:
    #             return TextRenderer(lwf, context, text)
    #         return None
    #
    #     def constructParticle(self, lwf, objectId, particle):
    #         ctor = self.resourceCache.particleConstructor
    #         particleData = lwf.data.particleDatas[particle.particleDataId]
    #         if ctor:
    #             return ctor(lwf, lwf.data.strings[particleData.stringId])
    #
    #     def getStageSize(self):
    #         return (self.stage.width, self.stage.height)
    #
    #     def setBackgroundColor(self, v):
    #         r, g, b, a = self.parseBackgroundColor(v)
    #         self.clearColor = "rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(a / 255) + ")"
    #         return
    #
    #     def resetGlobalCompositeOperation(self, ctx):
    #         ctx.globalCompositeOperation = "source-over"
    #         self.renderBlendMode = "normal"
    #         return
    #
    #     def setGlobalCompositeOperation(self, ctx, blendMode):
    #         if self.renderBlendMode != blendMode:
    #             self.renderBlendMode = blendMode
    #             if self.renderBlendMode == "add":
    #                 ctx.globalCompositeOperation = "lighter"
    #             elif self.renderBlendMode == "normal":
    #                 ctx.globalCompositeOperation = "source-over"
    #         return
    #
    #     def renderMask(self, blendMode):
    #         print("Boss! I'm rendering a mask!")
    #         ctx = self.maskCanvas.getContext()
    #         ctx.globalCompositeOperation = self.maskComposition
    #         self.renderBlendMode = None
    #         ctx.setTransform(1, 0, 0, 1, 0, 0)
    #         ctx.drawImage(self.layerCanvas, 0, 0, self.layerCanvas.width, self.layerCanvas.height, 0, 0,
    #                       self.layerCanvas.width, self.layerCanvas.height)
    #
    #         ctx = self.stageContext
    #         self.setGlobalCompositeOperation(ctx, blendMode)
    #         ctx.setTransform(1, 0, 0, 1, 0, 0)
    #         ctx.drawImage(self.maskCanvas, 0, 0, self.maskCanvas.width, self.maskCanvas.height, 0, 0,
    #                       self.maskCanvas.width, self.maskCanvas.height)
    #         return
    #
    #     def render(self, ctx, cmd):
    #         print("Boss! I'm rendering!")
    #         if self.renderMaskMode != cmd.maskMode:
    #             if cmd.maskMode == "erase" or cmd.maskMode == "mask" or cmd.maskMode == "alpha":
    #                 if self.renderMaskMode == "layer" and self.renderMasked:
    #                     self.renderMask(cmd.blendMode)
    #                 self.renderMasked = True
    #                 if cmd.maskMode == "erase":
    #                     self.maskComposition = "source-out"
    #                 else:
    #                     self.maskComposition = "source-in"
    #                 if not self.maskCanvas:
    #                     self.maskCanvas = LWF.CustomCanvas()
    #                     self.maskCanvas.width = self.stage.width
    #                     self.maskCanvas.height = self.stage.height
    #                     cleared = True
    #                 else:
    #                     cleared = False
    #                 ctx = self.maskCanvas.getContext()
    #                 self.resetGlobalCompositeOperation(ctx)
    #                 if not cleared:
    #                     ctx.setTransform(1, 0, 0, 1, 0, 0)
    #                     self.clearCanvasRect(self.stage, ctx)
    #             elif cmd.maskMode == "layer":
    #                 if self.renderMasked:
    #                     if not self.layerCanvas:
    #                         self.layerCanvas = LWF.CustomCanvas()
    #                         self.layerCanvas.width = self.stage.width
    #                         self.layerCanvas.height = self.stage.height
    #                         cleared = True
    #                     else:
    #                         cleared = False
    #                     ctx = self.layerCanvas.getContext()
    #                     self.resetGlobalCompositeOperation(ctx)
    #                     if not cleared:
    #                         ctx.setTransform(1, 0, 0, 1, 0, 0)
    #                         self.clearCanvasRect(self.stage, ctx)
    #                 else:
    #                     ctx = self.stageContext
    #                     self.resetGlobalCompositeOperation(ctx)
    #             elif cmd.maskMode == "normal":
    #                 ctx = self.stageContext
    #                 self.resetGlobalCompositeOperation(ctx)
    #                 if self.renderMaskMode == "layer" and self.renderMasked:
    #                     self.renderMask(self.renderBlendMode)
    #             self.renderMaskMode = cmd.maskMode
    #         self.setGlobalCompositeOperation(ctx, cmd.blendMode)
    #         if cmd.alpha != 1:
    #             ctx.globalAlpha = cmd.alpha
    #         m = cmd.matrix
    #         ctx.setTransform(m.scaleX, m.skew1, m.skew0, m.scaleY, m.translateX, m.translateY)
    #         u = cmd.u
    #         v = cmd.v
    #         w = cmd.w
    #         h = cmd.h
    #         if cmd.pattern and (w > cmd.image.width or h > cmd.image.height):
    #             ctx.fillStyle = cmd.pattern
    #             ctx.translate(-u, -v)
    #             ctx.rect(u, v, w, h)
    #         else:
    #             ctx.drawImage(cmd.image, u, v, w, h, 0, 0, w, h)
    #         if cmd.alpha != 1:
    #             ctx.globalAlpha = 1
    #         return ctx
    #
    #     def endRender(self, lwf):
    #         print("Ending my render boss!")
    #         ctx = self.stageContext
    #         if lwf.parent:
    #             self.addCommandToParent(lwf)
    #             return
    #
    #         if self.needsClear:
    #             ctx.setTransform(1, 0, 0, 1, 0, 0)
    #             if self.clearColor:
    #                 if self.clearColor[3] == 'a':
    #                     self.clearCanvasRect(self.stage, ctx)
    #                 ctx.fillStyle = self.clearColor
    #                 ctx.fillRect(0, 0, self.stage.width, self.stage.height)
    #             else:
    #                 self.clearCanvasRect(self.stage, ctx)
    #
    #         ctx.globalAlpha = 1
    #         self.resetGlobalCompositeOperation(ctx)
    #         self.renderMaskMode = "normal"
    #         self.renderMasked = False
    #         renderCount = lwf.renderCount
    #         for rIndex in range(0, len(self.commands)):
    #             cmd = self.commands[rIndex]
    #             if not cmd or cmd.renderingIndex != rIndex or cmd.renderCount != renderCount:
    #                 continue
    #             if cmd.subCommands:
    #                 for srIndex in range(0, len(cmd.subCommands)):
    #                     scmd = cmd.subCommands[srIndex]
    #                     if not scmd or scmd.renderingIndex != srIndex or scmd.renderCount != renderCount:
    #                         continue
    #                     ctx = self.render(ctx, scmd)
    #             ctx = self.render(ctx, cmd)
    #         if self.renderMaskMode == "layer" and self.renderMasked:
    #             self.renderMask(self.renderBlendMode)
    #         self.initCommands()
    #         return
    #
    # class ResourceCache(BaseResourceCache):
    #
    #     def getRendererName(self):
    #         return "Canvas"
    #
    #     def newFactory(self, settings, cache, data):
    #         return LWF.RendererFactory(data, self, cache, settings['stage'],
    #                                    settings['textInSubpixel'] if 'textInSubpixel' in settings else False,
    #                                    settings['needsClear'] if 'needsClear' in settings else True,
    #                                    settings['quirkyClearRect'] if 'quirkyClearRect' in settings else False)
    #
    #     def generateImages(self, settings, imageCache, texture, image):
    #         m = re.match('_withpadding', texture.filename)
    #         if m:
    #             w = image.width + 2
    #             h = image.height + 2
    #             canvas = LWF.CustomCanvas()
    #             canvas.width = 2
    #             canvas.height = h
    #             canvas.name = self.getCanvasName()
    #             ctx = canvas.getContext()
    #             canvas.widthPadding = True
    #             ctx.drawImage(image, 0, 0, image.width, image.height, 1, 1, image.width, image.height)
    #             imageCache[texture.filename] = canvas
    #         super().generateImages(settings, imageCache, texture, image)
    #         return
