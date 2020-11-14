# Internal Imports
import math
# External Imports
from typing import List

from ..Format import Format
from ..LWFContainer import LWFContainer
from ..objects.Bitmap import Bitmap
from ..objects.BitmapClip import BitmapClip, BitmapClips
from ..objects.BitmapEx import BitmapEx
from ..objects.Button import Button
from ..objects.Event import EventHandlerDictionary, EventHandlers, CalculateBoundsCallbacks
from ..objects.Graphic import Graphic
from ..objects.IObject import IObject
from ..objects.Label import LabelData, CurrentLabels, CurrentLabelCache
from ..objects.Object import Object
from ..objects.Particle import Particle
from ..objects.ProgramObject import ProgramObject
from ..objects.Property import Property
from ..objects.Text import Text, Texts
from ..utils.Constants import INT32_MINVALUE, FLOAT_MINVALUE, FLOAT_MAXVALUE
from ..utils.Type import Action, Dictionary, SortedDictionary, Matrix, Point, DetachDict, Bounds, ColorTransform
from ..utils.Utility import Utility


# from ..LWF import LWF


class MovieCommand(Action):
    pass


class MovieCommands(Dictionary):
    pass


class MovieEventHandler(Action):
    pass


class MovieEventHandlers:
    load = None
    postLoad = None
    unload = None
    enterFrame = None
    update = None
    render = None
    empty = False

    class Type:
        LOAD = 0
        POSTLOAD = 1
        UNLOAD = 2
        ENTERFRAME = 3
        UPDATE = 4
        RENDER = 5

    def __init__(self):
        self.load = MovieEventHandlerDictionary()
        self.postLoad = MovieEventHandlerDictionary()
        self.unload = MovieEventHandlerDictionary()
        self.enterFrame = MovieEventHandlerDictionary()
        self.update = MovieEventHandlerDictionary()
        self.render = MovieEventHandlerDictionary()
        self.empty = True

    def Clear(self, *args):
        if len(args) == 0:
            self.load.clear()
            self.postLoad.clear()
            self.unload.clear()
            self.enterFrame.clear()
            self.update.clear()
            self.render.clear()
            self.empty = True
        else:
            if args[0] == self.Type.LOAD:
                self.load.clear()
            elif args[0] == self.Type.POSTLOAD:
                self.postLoad.clear()
            elif args[0] == self.Type.UNLOAD:
                self.unload.clear()
            elif args[0] == self.Type.ENTERFRAME:
                self.enterFrame.clear()
            elif args[0] == self.Type.UPDATE:
                self.update.clear()
            elif args[0] == self.Type.RENDER:
                self.render.clear()
            self.UpdateEmpty()

    def Add(self, arg0, load=None, p=None, u=None, e=None, up=None, r=None):
        if not isinstance(arg0, int):
            handlers = arg0
            if handlers is None:
                return

            print(handlers.load)
            for hk, hv in handlers.load.items():
                self.load[hk] = hv
            for hk, hv in handlers.postLoad.items():
                self.postLoad[hk] = hv
            for hk, hv in handlers.unload.items():
                self.unload[hk] = hv
            for hk, hv in handlers.enterFrame.items():
                self.enterFrame[hk] = hv
            for hk, hv in handlers.update.items():
                self.update[hk] = hv
            for hk, hv in handlers.render.items():
                self.render[hk] = hv
            self.UpdateEmpty()
        else:
            key = arg0
            if load is not None:
                self.load[key] = load
            if p is not None:
                self.load[key] = p
            if u is not None:
                self.load[key] = u
            if e is not None:
                self.load[key] = e
            if up is not None:
                self.load[key] = up
            if r is not None:
                self.load[key] = r
            self.UpdateEmpty()

    def Remove(self, key):
        self.load.remove(key)
        self.postLoad.remove(key)
        self.unload.remove(key)
        self.enterFrame.remove(key)
        self.update.remove(key)
        self.render.remove(key)
        self.UpdateEmpty()

    def Call(self, htype, target):
        dictionary = None
        if htype == self.Type.LOAD:
            dictionary = self.load
        elif htype == self.Type.POSTLOAD:
            dictionary = self.postLoad
        elif htype == self.Type.UNLOAD:
            dictionary = self.unload
        elif htype == self.Type.ENTERFRAME:
            dictionary = self.enterFrame
        elif htype == self.Type.UPDATE:
            dictionary = self.update
        elif htype == self.Type.RENDER:
            dictionary = self.render
        if dictionary is not None:
            dictionary = MovieEventHandlerDictionary(dictionary)
            for h in dictionary.values():
                h(target)

    def UpdateEmpty(self):
        self.empty = True
        if len(self.load) > 0:
            self.empty = False
            return
        if len(self.postLoad) > 0:
            self.empty = False
            return
        if len(self.unload) > 0:
            self.empty = False
            return
        if len(self.enterFrame) > 0:
            self.empty = False
            return
        if len(self.update) > 0:
            self.empty = False
            return
        if len(self.render) > 0:
            self.empty = False
            return

    def Empty(self):
        return self.empty


class MovieEventHandlerDictionary(Dictionary):
    pass


class MovieEventHandlersDictionary(Dictionary):
    pass


class AttachedMovies(Dictionary):
    pass


class AttachedMovieList(SortedDictionary):
    pass


class AttachedMovieDescendingList(SortedDictionary):
    def __iter__(self):
        self.position = len(self.keys()) - 1
        return self

    def __next__(self):
        self.position -= 1
        return self.position < len(self.keys())

    def current(self):
        return self.keys()[self.position]


class AttachedLWFs(Dictionary):
    pass


class AttachedLWFList(SortedDictionary):
    pass


class AttachedLWFDescendingList(SortedDictionary):
    def __iter__(self):
        self.position = len(self.keys()) - 1
        return self

    def __next__(self):
        self.position -= 1
        return self.position < len(self.keys())

    def current(self):
        return self.keys()[self.position]


class Movie(IObject):
    m_data = 0
    m_instanceHead = None
    m_instanceTail = None
    m_displayList: List[(Object or None)] = None
    m_eventHandlers = None
    m_handler = None
    m_calculateBoundsCallbacks = None
    m_attachedMovies = None
    m_attachedMovieList = None
    m_attachedMovieDescendingList = None
    m_detachedMovies = None
    m_attachedLWFs = None
    m_attachedLWFList = None
    m_attachedLWFDescendingList = None
    m_detachedLWFs = None
    m_texts = None
    m_bitmapClips = None
    m_bounds = None
    m_currentBounds = None
    m_attachName = None
    m_totalFrames = 0
    m_currentFrameInternal = 0
    m_currentFrameCurrent = 0
    m_execedFrame = 0
    m_animationPlayedFrame = 0
    m_depth = 0
    m_lastControlOffset = 0
    m_lastControls = 0
    m_lastControlAnimationOffset = 0
    m_movieExecCount = 0
    m_postExecCount = 0
    m_blendMode = 0
    m_active = 0
    m_visible = 0
    m_playing = 0
    m_jumped = 0
    m_overriding = 0
    m_hasButton = 0
    m_postLoaded = 0
    m_lastHasButton = 0
    m_skipped = 0
    m_attachMovieExeced = 0
    m_attachMoviePostExeced = 0
    m_needsUpdateAttachedLWFs = 0
    m_requestedCalculateBounds = 0
    m_matrix0 = None
    m_matrix1 = None
    m_matrixForAttachedLWFs = None
    m_colorTransform0 = None
    m_colorTransform1 = None
    m_colorTransformForAttachedLWFs = None
    m_currentLabelsCache = None
    m_currentLabelCache = None
    m_property = None

    def __init__(self, lwf, parent, objId, instId, matrixId=0, colorTransformId=0, attached=False, handler=None,
                 n=None):
        super().__init__(lwf, parent, Format.Object.Type.ATTACHEDMOVIE if attached else Format.Object.Type.MOVIE, objId,
                         instId)
        self.m_data = lwf.data.movies[objId]
        self.m_matrixId = matrixId
        self.m_colorTransformId = colorTransformId
        self.m_totalFrames = self.m_data.frames
        if not (n is None or n == ""):
            self.m_name = n
        self.m_currentFrameInternal = -1
        self.m_execedFrame = -1
        self.m_animationPlayedFrame = -1
        self.m_lastControlOffset = -1
        self.m_lastControls = -1
        self.m_lastHasButton = False
        self.m_lastControlAnimationOffset = -1
        self.m_skipped = False
        self.m_postLoaded = False
        self.m_active = True
        self.m_visible = True
        self.m_playing = True
        self.m_jumped = False
        self.m_overriding = False
        self.m_attachMovieExeced = False
        self.m_attachMoviePostExeced = False
        self.m_movieExecCount = -1
        self.m_postExecCount = -1
        self.m_blendMode = int(Format.Constant.BLEND_MODE_NORMAL)
        self.m_requestedCalculateBounds = False
        self.m_calculateBoundsCallbacks = CalculateBoundsCallbacks()

        self.m_property = Property(lwf)

        self.m_matrix0 = Matrix()
        self.m_matrix1 = Matrix()
        self.m_matrixForAttachedLWFs = Matrix()
        self.m_colorTransform0 = ColorTransform()
        self.m_colorTransform1 = ColorTransform()
        self.m_colorTransformForAttachedLWFs = ColorTransform()

        self.m_displayList = [None for _ in range(self.m_data.depths)]

        self.m_eventHandlers = EventHandlers()
        self.m_handler = MovieEventHandlers()
        self.m_handler.Add(lwf.GetMovieEventHandlers(self))
        self.m_handler.Add(handler)

        self.PlayAnimation(Format.MovieClipEvent.ClipEvent.LOAD)
        if not self.m_handler.Empty():
            self.m_handler.Call(MovieEventHandlers.Type.LOAD, self)

        lwf.ExecMovieCommand()

    @property
    def data(self):
        return self.m_data

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
    def blendMode(self):
        return self.m_blendMode

    @blendMode.setter
    def blendMode(self, value):
        self.m_blendMode = value

    @property
    def currentFrame(self):
        return self.m_currentFrameInternal + 1

    @property
    def totalFrames(self):
        return self.m_totalFrames

    @property
    def playing(self):
        return self.m_playing

    @property
    def visible(self):
        return self.m_visible

    @property
    def hasButton(self):
        return self.m_totalFrames

    def SetHandlers(self, handler):
        self.m_handler.Clear()
        self.m_handler.Add(handler)

    def GlobalToLocal(self, point):
        invert = Matrix()
        if self.m_property.hasMatrix:
            m = Matrix()
            m = Utility.CalcMatrix(m, self.m_matrix, self.m_property.matrix)
        else:
            m = self.m_matrix
        Utility.InvertMatrix(invert, m)
        px, py = Utility.CalcMatrixToPoint(point.x, point.y, invert)
        return Point(px, py)

    def LocalToGlobal(self, point):
        if self.m_property.hasMatrix:
            m = Matrix()
            m = Utility.CalcMatrix(m, self.m_matrix, self.m_property.matrix)
        else:
            m = self.m_matrix
        px, py = Utility.CalcMatrixToPoint(point.x, point.y, m)
        return Point(px, py)

    def ExecObject(self, dlDepth, objId, matrixId, colorTransformId, instId, dlBlendMode, updateBlendMode=False):
        print("Update Movie Object")
        if objId == -1:
            return
        data = self.m_lwf.data
        dataObject = data.objects[objId]
        dataObjectId = dataObject.objectId
        obj = self.m_displayList[dlDepth]
        if obj is not None and (obj.type != dataObject.objectType or obj.objectId != dataObjectId or (
                obj.IsMovie() and obj.instanceId != instId)):
            if self.m_texts is not None and obj.IsText():
                self.EraseText(obj.objectId)
            obj.Destroy()
            obj = None
        if obj is None:
            if dataObject.objectType == Format.Object.Type.BUTTON:
                obj = Button(self.m_lwf, self, dataObjectId, instId, matrixId, colorTransformId)
            elif dataObject.objectType == Format.Object.Type.GRAPHIC:
                obj = Graphic(self.m_lwf, self, dataObjectId)
            elif dataObject.objectType == Format.Object.Type.MOVIE:
                obj = Movie(self.m_lwf, self, dataObjectId, instId, matrixId, colorTransformId)
                obj.blendMode = dlBlendMode
            elif dataObject.objectType == Format.Object.Type.BITMAP:
                obj = Bitmap(self.m_lwf, self, dataObjectId)
            elif dataObject.objectType == Format.Object.Type.BITMAPEX:
                obj = BitmapEx(self.m_lwf, self, dataObjectId)
            elif dataObject.objectType == Format.Object.Type.TEXT:
                obj = Text(self.m_lwf, self, dataObjectId, instId)
            elif dataObject.objectType == Format.Object.Type.PARTICLE:
                obj = Particle(self.m_lwf, self, dataObjectId)
            elif dataObject.objectType == Format.Object.Type.PROGRAMOBJECT:
                obj = ProgramObject(self.m_lwf, self, dataObjectId)
        if obj.IsMovie() and updateBlendMode:
            obj.blendMode = dlBlendMode
        if obj.IsMovie() or obj.IsButton():
            instance = obj
            instance.linkInstance = None
            if self.m_instanceHead is None:
                self.m_instanceHead = instance
            else:
                self.m_instanceTail.linkInstance = instance
            self.m_instanceTail = instance
            if obj.IsButton():
                self.m_hasButton = True
        if self.m_texts is not None and obj.IsText():
            self.InsertText(obj.objectId)
        self.m_displayList[dlDepth] = obj
        obj.execCount = self.m_movieExecCount
        obj.Exec(matrixId, colorTransformId)

    def Override(self, overriding):
        self.m_overriding = overriding

    def Exec(self, matrixId=0, colorTransformId=0):
        print("Movie Update")
        self.m_attachMovieExeced = False
        self.m_attachMoviePostExeced = False
        super().Exec(matrixId, colorTransformId)

    def PostExec(self, progressing):
        print("Movie Post Exec")
        self.m_hasButton = False
        if not self.m_active:
            return

        self.m_execedFrame = -1
        postExeced = self.m_postExecCount == self.m_lwf.execCount
        if progressing and self.m_playing and not self.m_jumped and not postExeced:
            self.m_currentFrameInternal += 1
        while True:
            if self.m_currentFrameInternal < 0 or self.m_currentFrameInternal >= self.m_totalFrames:
                self.m_currentFrameInternal = 0
            if self.m_currentFrameInternal == self.m_execedFrame:
                break
            self.m_currentFrameCurrent = self.m_currentFrameInternal
            self.m_execedFrame = self.m_currentFrameCurrent
            data = self.m_lwf.data
            frame = data.frames[self.m_data.frameOffset + self.m_currentFrameCurrent]
            print("Got a frame?", frame.controls, frame.controlOffset)
            if self.m_lastControlOffset == frame.controlOffset and self.m_lastControls == frame.controls:
                controlAnimationOffset = self.m_lastControlAnimationOffset
                if self.m_skipped:
                    instance = self.m_instanceHead
                    while instance is not None:
                        if instance.IsMovie():
                            movie = instance
                            movie.m_attachMovieExeced = False
                            movie.m_attachMoviePostExeced = False
                        elif instance.IsButton():
                            instance.EnterFrame()
                        instance = instance.linkInstance
                    self.m_hasButton = self.m_lastHasButton
                else:
                    for dlDepth in range(0, self.m_data.depths):
                        obj = self.m_displayList[dlDepth]
                        if obj is not None:
                            if not postExeced:
                                obj.matrixIdChanged = False
                                obj.colorTransformIdChanged = False
                            if obj.IsMovie():
                                movie = obj
                                movie.m_attachMovieExeced = False
                                movie.m_attachMoviePostExeced = False
                            elif obj.IsButton():
                                obj: Button
                                obj.EnterFrame()
                                self.m_hasButton = True
                    self.m_lastHasButton = self.m_hasButton
                    self.m_skipped = True
            else:
                self.m_movieExecCount += 1
                self.m_instanceHead = None
                self.m_instanceTail = None
                self.m_lastControlOffset = frame.controlOffset
                self.m_lastControls = frame.controls
                controlAnimationOffset = -1
                for i in range(0, frame.controls):
                    control = data.controls[frame.controlOffset + i]
                    if control.controlType == Format.Control.Type.MOVE:
                        p = data.places[control.controlId]
                        self.ExecObject(p.depth, p.objectId, p.matrixId, 0, p.instanceId, p.blendMode)
                    elif control.controlType == Format.Control.Type.MOVEM:
                        ctrl = data.controlMoveMs[control.controlId]
                        p = data.places[ctrl.placeId]
                        self.ExecObject(p.depth, p.objectId, ctrl.matrixId, 0, p.instanceId, p.blendMode)
                    elif control.controlType == Format.Control.Type.MOVEC:
                        ctrl = data.controlMoveCs[control.controlId]
                        p = data.places[ctrl.placeId]
                        self.ExecObject(p.depth, p.objectId, ctrl.matrixId, ctrl.colorTransformId, p.instanceId,
                                        p.blendMode)
                    elif control.controlType == Format.Control.Type.MOVEMC:
                        ctrl = data.controlMoveMCs[control.controlId]
                        p = data.places[ctrl.placeId]
                        self.ExecObject(p.depth, p.objectId, ctrl.matrixId, ctrl.colorTransformId, p.instanceId,
                                        p.blendMode)
                    elif control.controlType == Format.Control.Type.MOVEMCB:
                        ctrl = data.controlMoveMCBs[control.controlId]
                        p = data.places[ctrl.placeId]
                        self.ExecObject(p.depth, p.objectId, ctrl.matrixId, ctrl.colorTransformId, p.instanceId,
                                        ctrl.blendMode, True)
                    elif control.controlType == Format.Control.Type.ANIMATION:
                        if controlAnimationOffset == -1:
                            controlAnimationOffset = i
                self.m_lastControlAnimationOffset = controlAnimationOffset
                self.m_lastHasButton = self.m_hasButton

                for dlDepth in range(0, self.m_data.depths):
                    obj = self.m_displayList[dlDepth]
                    if obj is not None and obj.execCount != self.m_movieExecCount:
                        if self.m_texts is not None and obj.IsText():
                            self.EraseText(obj.objectId)
                        obj.Destroy()
                        self.m_displayList[dlDepth] = None
            self.m_attachMovieExeced = True
            if self.m_attachedMovies is not None:
                for movie in self.m_attachedMovieList.values():
                    if movie is not None:
                        movie.Exec()

            instance = self.m_instanceHead
            while instance is not None:
                if instance.IsMovie():
                    movie = instance
                    movie.PostExec(progressing)
                    if not self.m_hasButton and movie.m_hasButton:
                        self.m_hasButton = True
                instance = instance.linkInstance

            self.m_attachMoviePostExeced = True
            if self.m_attachedMovies is not None:
                for attachName, v in self.m_detachedMovies:
                    boolean, movie = self.m_attachedMovies.TryGetValue(attachName)
                    if boolean:
                        self.DeleteAttachedMovie(self, movie, True, False)
                self.m_detachedMovies.clear()
                for movie in self.m_attachedMovieList.values():
                    if movie is not None:
                        movie.PostExec(progressing)
                        if not self.m_hasButton and movie.m_hasButton:
                            self.m_hasButton = True
            if self.m_attachedLWFs is not None:
                self.m_hasButton = True
            if not self.m_postLoaded:
                self.m_postLoaded = True
                if not self.m_handler.Empty():
                    self.m_handler.Call(MovieEventHandlers.Type.POSTLOAD, self)
            if controlAnimationOffset != -1 and self.m_execedFrame == self.m_currentFrameInternal:
                animationPlayed = self.m_animationPlayedFrame == self.m_currentFrameCurrent and not self.m_jumped
                if not animationPlayed:
                    for i in range(controlAnimationOffset, frame.controls):
                        control = data.controls[frame.controlOffset + i]
                        self.m_lwf.PlayAnimation(control.controlId, self)
            self.m_animationPlayedFrame = self.m_currentFrameCurrent
            if self.m_currentFrameCurrent == self.m_currentFrameInternal:
                self.m_jumped = False

        self.PlayAnimation(Format.MovieClipEvent.ClipEvent.ENTERFRAME)
        if not self.m_handler.Empty():
            self.m_handler.Call(MovieEventHandlers.Type.ENTERFRAME, self)
            self.m_postExecCount = self.m_lwf.execCount

    def ExecAttachedLWF(self, tick, currentProgress):
        hasButton = False
        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie():
                hasButton |= instance.ExecAttachedLWF(tick, currentProgress)
            instance = instance.linkInstance

        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    hasButton |= movie.ExecAttachedLWF(tick, currentProgress)
        if self.m_attachedLWFs is not None:
            for attachName, v in self.m_detachedLWFs:
                boolean, lwfContainer = self.m_attachedLWFs.TryGetValue(attachName)
                if boolean:
                    self.DeleteAttachedLWF(self, lwfContainer, True, False)
            self.m_detachedLWFs.clear()
            for lwfContainer in self.m_attachedLWFList.values():
                child = lwfContainer.child
                if child.tick == self.m_lwf.tick:
                    child.progress = currentProgress
                self.m_lwf.RenderObject(child.ExecInternal(tick))
                hasButton |= child.rootMovie.hasButton
        return hasButton

    def UpdateObject(self, obj, m, c, matrixChanged, colorTransformChanged):
        if obj.IsMovie() and obj.m_property.hasMatrix:
            objm = m
        elif matrixChanged or not obj.updated or obj.matrixIdChanged:
            objm = Utility.CalcMatrix(self.m_lwf, self.m_matrix1, m, obj.matrixId)
        else:
            objm = None
        if obj.IsMovie() and obj.m_property.hasColorTransform():
            objc = c
        elif colorTransformChanged or not obj.updated or obj.colorTransformIdChanged:
            objc = Utility.CalcColorTransform(self.m_lwf, self.m_colorTransform1, c, obj.colorTransformId)
        else:
            objc = None
        obj.Update(objm, objc)

    def Update(self, m, c):
        if not self.m_active:
            return

        if self.m_overriding:
            matrixChanged = True
            colorTransformChanged = True
        else:
            matrixChanged = self.m_matrix.SetWithComparing(m)
            colorTransformChanged = self.m_colorTransform.SetWithComparing(c)

        if self.m_property.hasMatrix:
            matrixChanged = True
            m = Utility.CalcMatrix(self.m_matrix0, self.m_matrix, self.m_property.matrix)
        else:
            m = self.m_matrix

        if self.m_property.hasColorTransform:
            colorTransformChanged = True
            c = Utility.CalcColorTransform(self.m_colorTransform0, self.m_colorTransform,
                                           self.m_property.colorTransform)
        else:
            c = self.m_colorTransform

        if self.m_attachedLWFs is not None:
            self.m_needsUpdateAttachedLWFs = False
            self.m_needsUpdateAttachedLWFs |= self.m_matrixForAttachedLWFs.SetWithComparing(m)
            self.m_needsUpdateAttachedLWFs |= self.m_colorTransformForAttachedLWFs.SetWithComparing(c)

        for dlDepth in range(0, self.m_data.depths):
            obj = self.m_displayList[dlDepth]
            if obj is not None:
                self.UpdateObject(obj, m, c, matrixChanged, colorTransformChanged)

        if self.m_bitmapClips is not None:
            for bitmapClip in self.m_bitmapClips.values():
                if bitmapClip is not None:
                    bitmapClip.Update(m, c)

        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    self.UpdateObject(movie, m, c, matrixChanged, colorTransformChanged)

    def PostUpdate(self):
        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie():
                instance.PostUpdate()
            instance = instance.linkInstance
        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    movie.PostUpdate()

        if self.m_requestedCalculateBounds:
            self.m_currentBounds = Bounds(FLOAT_MAXVALUE, FLOAT_MINVALUE, FLOAT_MAXVALUE, FLOAT_MINVALUE)
            self.Inspect((lambda o, hy, d, r: self.CalculateBounds(o)), 0, 0, 0)
            if self.lwf.lwfproperty.hasMatrix:
                invert = Matrix()
                Utility.InvertMatrix(invert, self.lwf.lwfproperty.matrix)
                x, y = Utility.CalcMatrixToPoint(self.m_currentBounds.xMin, self.m_currentBounds.yMin, invert)
                self.m_currentBounds.xMin = x
                self.m_currentBounds.yMin = y
                x, y = Utility.CalcMatrixToPoint(self.m_currentBounds.xMax, self.m_currentBounds.yMax, invert)
                self.m_currentBounds.xMax = x
                self.m_currentBounds.yMax = y
            self.m_bounds = self.m_currentBounds
            self.m_currentBounds = None
            self.m_requestedCalculateBounds = False
            if len(self.m_calculateBoundsCallbacks) is not 0:
                for h in self.m_calculateBoundsCallbacks:
                    h(self)
                self.m_calculateBoundsCallbacks.clear()

        if not self.m_handler.Empty():
            self.m_handler.Call(MovieEventHandlers.Type.UPDATE, self)

    def UpdateAttachedLWF(self):
        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie():
                instance.UpdateAttachedLWF()
            instance = instance.linkInstance

        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    movie.updateAttachedLWF()

        if self.m_attachedLWFs is not None:
            for lwfContainer in self.m_attachedLWFList.values():
                if lwfContainer is None:
                    continue
                child = lwfContainer.child
                needsUpdateAttachedLWFs = child.needsUpdate or self.m_needsUpdateAttachedLWFs
                if needsUpdateAttachedLWFs:
                    child.Update(self.m_matrixForAttachedLWFs, self.m_colorTransformForAttachedLWFs)
                if child.isLWFAttached:
                    child.rootMovie.UpdateAttachedLWF()
                if needsUpdateAttachedLWFs:
                    child.rootMovie.PostUpdate()

    def CalculateBounds(self, o):
        if o.type == Format.Object.Type.GRAPHIC:
            for obj in o.displayList:
                self.CalculateBounds(obj)
        elif o.type == Format.Object.Type.BITMAP or o.type == Format.Object.Type.BITMAPEX:
            tfId = -1
            if o.type == Format.Object.Type.BITMAP:
                if o.objectId < len(o.lwf.data.bitmaps):
                    tfId = o.lwf.data.bitmaps[o.objectId].textureFragmentId
            else:
                if o.objectId < len(o.lwf.data.bitmapExs):
                    tfId = o.lwf.data.bitmapExs[o.objectId].textureFragmentId
            if tfId >= 0:
                tf = o.lwf.data.textureFragments[tfId]
                self.UpdateBounds(o.matrix, tf.x, tf.x + tf.w, tf.y, tf.y + tf.h)
        elif o.type == Format.Object.Type.BUTTON:
            self.UpdateBounds(o.matrix, 0, o.width, 0, o.height)
        elif o.type == Format.Object.Type.TEXT:
            text = o.lwf.data.texts[o.objectId]
            self.UpdateBounds(o.matrix, 0, text.width, 0, text.height)
        elif o.type == Format.Object.Type.PROGRAMOBJECT:
            pobj = o.lwf.data.programObjects[o.objectId]
            self.UpdateBounds(o.matrix, 0, pobj.width, 0, pobj.height)

    def UpdateBounds(self, m, *args):
        if len(args) == 4:  # type 1
            self.UpdateBounds(m, args[0], args[2])  # xMin, yMin
            self.UpdateBounds(m, args[0], args[3])  # xMin, yMax
            self.UpdateBounds(m, args[1], args[2])  # xMax, yMin
            self.UpdateBounds(m, args[1], args[3])  # xMax, yMax
        elif len(args) == 2:  # type 2
            x, y = Utility.CalcMatrixToPoint(args[0], args[1], m)
            if x < self.m_currentBounds.xMin:
                self.m_currentBounds.xMin = x
            elif x > self.m_currentBounds.xMax:
                self.m_currentBounds.xMax = x
            if y < self.m_currentBounds.yMin:
                self.m_currentBounds.yMin = y
            elif y > self.m_currentBounds.yMax:
                self.m_currentBounds.yMax = y

    def LinkButton(self):
        if not self.m_visible or not self.m_active or not self.m_hasButton:
            return
        for dlDepth in range(0, self.m_data.depths):
            obj = self.m_displayList[dlDepth]
            if obj is not None:
                if obj.IsButton():
                    obj.LinkButton()
                elif obj.IsMovie():
                    if obj.m_hasButton:
                        obj.LinkButton()
        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None and movie.m_hasButton:
                    movie.linkButton()

        if self.m_attachedLWFs is not None:
            for lwfContainer in self.m_attachedLWFList.values():
                if lwfContainer is not None:
                    lwfContainer.LinkButton()

    def Render(self, v, rOffset):
        print("render")
        if not self.m_visible or not self.m_active:
            v = False

        useBlendMode = False
        useMaskMode = False
        if self.m_blendMode != int(Format.Constant.BLEND_MODE_NORMAL):
            if self.m_blendMode == int(Format.Constant.BLEND_MODE_ADD) \
                    or self.m_blendMode == int(Format.Constant.BLEND_MODE_MULTIPLY) \
                    or self.m_blendMode == int(Format.Constant.BLEND_MODE_SCREEN) \
                    or self.m_blendMode == int(Format.Constant.BLEND_MODE_SUBTRACT):
                self.m_lwf.BeginBlendMode(self.m_blendMode)
                useBlendMode = True
            elif self.m_blendMode == int(Format.Constant.BLEND_MODE_ERASE) \
                    or self.m_blendMode == int(Format.Constant.BLEND_MODE_LAYER) \
                    or self.m_blendMode == int(Format.Constant.BLEND_MODE_MASK):
                self.m_lwf.BeginMaskMode(self.m_blendMode)
                useMaskMode = True

        if v and not self.m_handler.Empty():
            self.m_handler.Call(MovieEventHandlers.Type.RENDER, self)

        if self.m_property.hasRenderingOffset:
            self.m_lwf.RenderOffset()
            rOffset = self.m_property.renderingOffset

        if rOffset == INT32_MINVALUE:
            self.m_lwf.ClearRenderOffset()

        for dlDepth in range(0, self.m_data.depths):
            obj = self.m_displayList[dlDepth]
            if obj is not None:
                print("Render Object")
                obj.Render(v, rOffset)

        if self.m_bitmapClips is not None:
            for bitmapClip in self.m_bitmapClips.values():
                if bitmapClip is not None:
                    bitmapClip.Render(v and bitmapClip.visible, rOffset)

        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    movie.Render(v, rOffset)

        if self.m_attachedLWFs is not None:
            for lwfContainer in self.m_attachedMovieList.values():
                if lwfContainer is not None:
                    child = lwfContainer.child
                    child.SetAttachVisible(v)
                    self.m_lwf.RenderObject(child.Render(self.m_lwf.renderingIndex, self.m_lwf.renderingCount, rOffset))

        if useBlendMode:
            self.m_lwf.EndBlendMode()
        if useMaskMode:
            self.m_lwf.EndMaskMode()

    def Inspect(self, inspector, hierarchy, inspectDepth, rOffset):
        if self.m_property.hasRenderingOffset:
            self.m_lwf.RenderOffset()
            rOffset = self.m_property.renderingOffset
        if rOffset == INT32_MINVALUE:
            self.m_lwf.ClearRenderOffset()

        inspector(self, hierarchy, inspectDepth, rOffset)

        hierarchy += 1

        d = 0
        for d in range(0, self.m_data.depths):
            obj = self.m_displayList[d]
            if obj is not None:
                obj.Inspect(inspector, hierarchy, d, rOffset)
        if self.m_bitmapClips is not None:
            for bitmapClip in self.m_bitmapClips.values():
                if bitmapClip is not None:
                    bitmapClip.Inspect(inspector, hierarchy, d, rOffset)
                    d += 1
        if self.m_attachedMovies is not None:
            for movie in self.m_attachedMovieList.values():
                if movie is not None:
                    movie.Inspect(inspector, hierarchy, d, rOffset)
                    d += 1

        if self.m_attachedLWFs is not None:
            for lwfContainer in self.m_attachedLWFList.values():
                if lwfContainer is not None:
                    child = lwfContainer.child
                    self.m_lwf.RenderObject(child.Inspect(inspector, hierarchy, d, rOffset))
                    d += 1

    def Destroy(self):
        for dlDepth in range(0, self.m_data.depths):
            obj = self.m_displayList[dlDepth]
            if obj is not None:
                obj.Destroy()

        if self.m_bitmapClips is not None:
            for k, v in self.m_bitmapClips:
                if v is not None:
                    v.Destroy()
            self.m_bitmapClips = None

        if self.m_attachedMovies is not None:
            for k, v in self.m_attachedMovies:
                v.Destroy()
            self.m_attachedMovies = None
            self.m_detachedMovies = None
            self.m_attachedMovieList = None

        if self.m_attachedLWFs is not None:
            for k, v in self.m_attachedLWFs:
                if v.child.detachHandler is not None:
                    v.detachHandler(v.child)
            self.m_attachedLWFs = None
            self.m_detachedLWFs = None
            self.m_attachedLWFList = None

        self.PlayAnimation(Format.MovieClipEvent.ClipEvent.UNLOAD)
        if not self.m_handler.Empty():
            self.m_handler.Call(MovieEventHandlers.Type.UNLOAD, self)

        self.m_displayList = None
        self.m_property = None
        super().Destroy()

    def PlayAnimation(self, clipEvent):
        clipEvents = self.m_lwf.data.movieClipEvents
        for i in range(0, self.m_data.clipEvents):
            c = clipEvents[self.m_data.clipEventId + i]
            if (c.clipEvent & int(clipEvent)) != 0:
                self.m_lwf.PlayAnimation(c.animationId, self)

    def SearchFrame(self, arg):
        return self.m_lwf.SearchFrame(self, arg)

    def SearchMovieInstance(self, arg, recursive=True):
        if isinstance(arg, int):
            stringId = arg
            if stringId == -1:
                return None
            instance = self.m_instanceHead
            while instance is not None:
                if instance.IsMovie() and self.m_lwf.GetInstanceNameStringId(instance.instanceId) == stringId:
                    return instance
                elif recursive and instance.IsMovie():
                    i = instance.SearchMovieInstance(stringId, recursive)
                    if i is not None:
                        return i
                instance = instance.linkInstance
        else:
            instanceName = arg
            stringId = self.m_lwf.GetStringId(instanceName)
            if stringId != -1:
                return self.SearchMovieInstance(stringId, recursive)

            if self.m_attachedMovies is not None:
                for movie in self.m_attachedMovieList.values():
                    if movie is not None:
                        if movie.attachName == instanceName:
                            return movie
                        elif recursive:
                            descendant = movie.SearchMovieInstance(instanceName, recursive)
                            if descendant is not None:
                                return descendant
            if self.m_attachedLWFs is not None:
                for lwfContainer in self.m_attachedLWFList.values():
                    if lwfContainer is not None:
                        child = lwfContainer.child
                        if child.attachName == instanceName:
                            return child.rootMovie
                        elif recursive:
                            descendant = child.rootMovie.SearchMovieInstance(instanceName, recursive)
                            if descendant is not None:
                                return descendant
        return None

    def __getitem__(self, instanceName):
        return self.SearchMovieInstance(instanceName, False)

    def SearchMovieInstanceByInstanceId(self, instId, recursive):
        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie() and instance.instanceId == instId:
                return instance
            elif recursive and instance.IsMovie():
                i = instance.SearchMovieInstanceByInstanceId(instId, recursive)
                if i is not None:
                    return i
            instance = instance.linkInstance
        return None

    def SearchButtonInstance(self, arg, recursive=True):
        if isinstance(arg, int):
            stringId = arg
            if stringId == -1:
                return None
            instance = self.m_instanceHead
            while instance is not None:
                if instance.IsButton() and self.m_lwf.GetInstanceNameStringId(instance.instanceId) == stringId:
                    return instance
                elif recursive and instance.IsMovie():
                    i = instance.SearchButtonInstance(stringId, recursive)
                    if i is not None:
                        return i
                instance = instance.linkInstance
        else:
            instanceName = arg
            stringId = self.m_lwf.GetStringId(instanceName)
            if stringId != -1:
                return self.SearchButtonInstance(stringId, recursive)

            if self.m_attachedMovies is not None and recursive:
                for movie in self.m_attachedMovieList.values():
                    if movie is not None:
                        button = movie.SearchButtonInstance(instanceName, recursive)
                        if button is not None:
                            return button
            if self.m_attachedLWFs is not None:
                for lwfContainer in self.m_attachedLWFList.values():
                    if lwfContainer is not None:
                        child = lwfContainer.child
                        button = child.rootMovie.SearchButtonInstance(instanceName, recursive)
                        if button is not None:
                            return button
        return None

    def SearchButtonInstanceByInstanceId(self, instId, recursive):
        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsButton() and instance.instanceId == instId:
                return instance
            elif recursive and instance.IsMovie():
                i = instance.SearchButtonInstanceByInstanceId(instId, recursive)
                if i is not None:
                    return i
            instance = instance.linkInstance
        return None

    def InsertText(self, objId):
        text = self.lwf.data.texts[objId]
        if text.nameStringId != -1:
            self.m_texts[self.lwf.data.srings[text.nameStringId]] = True

    def EraseText(self, objId):
        text = self.lwf.data.texts[objId]
        if text.nameStringId != -1:
            self.m_texts.remove(self.lwf.data.strings[text.nameStringId])

    def SearchText(self, textName):
        if self.m_texts is not None:
            self.m_texts = Texts()
            for dlDepth in range(0, self.data.depths):
                obj = self.m_displayList[dlDepth]
                if obj is not None and obj.IsText():
                    self.InsertText(obj.objectId)

        boolean, v = self.m_texts.TryGetValue(textName)
        if boolean:
            return True
        return False

    def AddEventHandler(self, eventName, handler):
        if isinstance(handler, MovieEventHandler):
            eventId = self.m_lwf.GetEventOffset()
            if eventName == "load":
                self.m_handler.Add(eventId, load=handler)
                return eventId
            elif eventName == "postLoad":
                self.m_handler.Add(eventId, p=handler)
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
            else:
                return -1
        else:
            eventId = self.m_lwf.GetEventOffset()
            boolean, dictionary = self.m_eventHandlers.TryGetValue(eventName)
            if not boolean:
                dictionary = EventHandlerDictionary()
                self.m_eventHandlers[eventName] = dictionary
            dictionary.Add(eventId, handler)
            return eventId

    def RemoveEventHandler(self, eventName, buttonId):
        if eventName == "load" or \
                eventName == "postLoad" or \
                eventName == "unload" or \
                eventName == "enterFrame" or \
                eventName == "update" or \
                eventName == "render":
            self.m_handler.Remove(buttonId)
        else:
            boolean, dictionary = self.m_eventHandlers.TryGetValue(eventName)
            if boolean:
                dictionary.Remove(buttonId)

    def ClearEventHandler(self, eventName):
        if eventName == "load":
            self.m_handler.Clear(MovieEventHandlers.Type.LOAD)
        elif eventName == "postLoad":
            self.m_handler.Clear(MovieEventHandlers.Type.POSTLOAD)
        elif eventName == "unload":
            self.m_handler.Clear(MovieEventHandlers.Type.UNLOAD)
        elif eventName == "enterframe":
            self.m_handler.Clear(MovieEventHandlers.Type.ENTERFRAME)
        elif eventName == "update":
            self.m_handler.Clear(MovieEventHandlers.Type.UPDATE)
        elif eventName == "render":
            self.m_handler.Clear(MovieEventHandlers.Type.RENDER)
        else:
            self.m_eventHandlers.remove(eventName)

    def SetEventHandler(self, eventName, eventHandler):
        self.ClearEventHandler(eventName)
        return self.AddEventHandler(eventName, eventHandler)

    def DispatchEvent(self, eventName):
        if eventName == "load":
            self.m_handler.Call(MovieEventHandlers.Type.LOAD, self)
        elif eventName == "postLoad":
            self.m_handler.Call(MovieEventHandlers.Type.POSTLOAD, self)
        elif eventName == "unload":
            self.m_handler.Call(MovieEventHandlers.Type.UNLOAD, self)
        elif eventName == "enterframe":
            self.m_handler.Call(MovieEventHandlers.Type.ENTERFRAME, self)
        elif eventName == "update":
            self.m_handler.Call(MovieEventHandlers.Type.UPDATE, self)
        elif eventName == "render":
            self.m_handler.Call(MovieEventHandlers.Type.RENDER, self)
        else:
            boolean, dictionary = self.m_eventHandlers.TryGetValue(eventName)
            if boolean:
                dictionary = EventHandlerDictionary(dictionary)
                for k, v in dictionary.items():
                    v()

    def RequestCalculateBounds(self, callback=None):
        self.m_requestedCalculateBounds = True
        self.m_calculateBoundsCallbacks.append(callback)
        self.m_bounds = None
        return

    def GetBounds(self):
        return self.m_bounds

    def CacheCurrentLabels(self):
        if self.m_currentLabelsCache is not None:
            return
        self.m_currentLabelsCache = CurrentLabels()
        labels = self.m_lwf.GetMovieLabels(self)
        if labels is None:
            return

        for k, v in labels:
            labelData = LabelData()
            labelData.frame = v + 1
            labelData.name = self.m_lwf.data.strings[k]
            self.m_currentLabelsCache.append(labelData)

        def anon(a, b):
            return a.frame - b.frame

        self.m_currentLabelsCache.Sort(anon)

    def GetCurrentLabel(self):
        self.CacheCurrentLabels()

        if len(self.m_currentLabelsCache) == 0:
            return None

        currentFrameTmp = self.currentFrame
        if currentFrameTmp < 1:
            currentFrameTmp = 1

        if self.m_currentLabelCache is None:
            self.m_currentLabelCache = CurrentLabelCache()

        boolean, labelName = self.m_currentLabelCache.TryGetValue(currentFrameTmp)
        if not boolean:
            firstLabel = self.m_currentLabelsCache[0]
            lastLabel = self.m_currentLabelsCache[len(self.m_currentLabelsCache) - 1]
            if currentFrameTmp < firstLabel.frame:
                labelName = ""
            elif currentFrameTmp == firstLabel.frame:
                labelName = firstLabel.name
            elif currentFrameTmp >= lastLabel.frame:
                labelName = lastLabel.name
            else:
                left = 0
                ln = self.m_currentLabelsCache[left].frame
                r = len(self.m_currentLabelsCache) - 1
                rn = self.m_currentLabelsCache[r].frame
                while True:
                    if (left == r) or (r - left == 1):
                        if currentFrameTmp < ln:
                            labelName = ""
                        elif currentFrameTmp == rn:
                            labelName = self.m_currentLabelsCache[r].name
                        else:
                            labelName = self.m_currentLabelsCache[left].name
                        break
                    n = int(math.floor((r - left) / 2.0) + left)
                    nn = self.m_currentLabelsCache[n].frame
                    if currentFrameTmp < nn:
                        r = n
                        rn = nn
                    elif currentFrameTmp > nn:
                        left = n
                        ln = nn
                    else:
                        labelName = self.m_currentLabelsCache[n].name
                        break
        return None if (labelName == "" or labelName is None) else labelName

    def GetCurrentLabels(self):
        self.CacheCurrentLabels()
        return self.m_currentLabelsCache

    # lwf_movieprop -----------------------------------------------------------

    @property
    def x(self):
        if self.m_property.hasMatrix:
            return self.m_property.matrix.translateX
        else:
            return Utility.GetX(self)

    @x.setter
    def x(self, value):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.MoveTo(value, self.m_property.matrix.translateY)

    @property
    def y(self):
        if self.m_property.hasMatrix:
            return self.m_property.matrix.translateY
        else:
            return Utility.GetY(self)

    @y.setter
    def y(self, value):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.MoveTo(self.m_property.matrix.translateX, value)

    @property
    def scaleX(self):
        if self.m_property.hasMatrix:
            return self.m_property.m_scaleX
        else:
            return Utility.GetScaleX(self)

    @scaleX.setter
    def scaleX(self, value):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.ScaleTo(value, self.m_property.m_scaleY)

    @property
    def scaleY(self):
        if self.m_property.hasMatrix:
            return self.m_property.m_scaleY
        else:
            return Utility.GetScaleY(self)

    @scaleY.setter
    def scaleY(self, value):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.ScaleTo(self.m_property.m_scaleX, value)

    @property
    def rotation(self):
        if self.m_property.hasMatrix:
            return self.m_property.m_rotation
        else:
            return Utility.GetRotation(self)

    @rotation.setter
    def rotation(self, value):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.RotateTo(value)

    @property
    def alpha(self):
        if self.m_property.hasColorTransform:
            return self.m_property.colorTransform.multi.alpha
        else:
            return Utility.GetAlpha(self)

    @alpha.setter
    def alpha(self, value):
        if not self.m_property.hasColorTransform:
            Utility.SyncColorTransform(self)
        self.m_property.SetAlpha(value)

    @property
    def red(self):
        if self.m_property.hasColorTransform:
            return self.m_property.colorTransform.multi.red
        else:
            return Utility.GetRed(self)

    @red.setter
    def red(self, value):
        if not self.m_property.hasColorTransform:
            Utility.SyncColorTransform(self)
        self.m_property.SetAlpha(value)

    @property
    def green(self):
        if self.m_property.hasColorTransform:
            return self.m_property.colorTransform.multi.green
        else:
            return Utility.GetGreen(self)

    @green.setter
    def green(self, value):
        if not self.m_property.hasColorTransform:
            Utility.SyncColorTransform(self)
        self.m_property.SetAlpha(value)

    @property
    def blue(self):
        if self.m_property.hasColorTransform:
            return self.m_property.colorTransform.multi.blue
        else:
            return Utility.GetBlue(self)

    @blue.setter
    def blue(self, value):
        if not self.m_property.hasColorTransform:
            Utility.SyncColorTransform(self)
        self.m_property.SetAlpha(value)

    # lwf_movieop -------------------------------------------------------------

    def Play(self):
        self.m_playing = True
        return self

    def Stop(self):
        self.m_playing = False
        return self

    def NextFrame(self):
        self.m_jumped = True
        self.Stop()
        self.m_currentFrameInternal += 1
        return self

    def PrevFrame(self):
        self.m_jumped = True
        self.Stop()
        self.m_currentFrameInternal -= 1
        return self

    def GotoFrame(self, frameNo):
        self.GotoFrameInternal(frameNo - 1)
        return self

    def GotoFrameInternal(self, frameNo):
        self.m_jumped = True
        self.Stop()
        self.m_currentFrameInternal = frameNo
        return self

    def SetVisible(self, visible):
        self.m_visible = visible
        self.m_lwf.SetPropertyDirty()
        return self

    def GotoLabel(self, arg):
        if isinstance(arg, int):
            self.GotoFrame(self.m_lwf.SearchFrame(self, arg))
        else:
            self.GotoLabel(self.m_lwf.GetStringId(arg))
        return self

    def GotoAndStop(self, arg):
        if isinstance(arg, int):
            self.GotoFrame(arg)
        else:
            self.GotoFrame(self.m_lwf.SearchFrame(self, self.m_lwf.GetStringId(arg)))
        self.Stop()
        return self

    def GotoAndPlay(self, arg):
        if isinstance(arg, int):
            self.GotoFrame(arg)
        else:
            self.GotoFrame(self.m_lwf.SearchFrame(self, self.m_lwf.GetStringId(arg)))
        self.Play()
        return self

    def Move(self, vx, vy):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.Move(vx, vy)
        return self

    def MoveTo(self, vx, vy):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.MoveTo(vx, vy)
        return self

    def Rotate(self, degree):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.Rotate(degree)
        return self

    def RotateTo(self, degree):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.RotateTo(degree)
        return self

    def Scale(self, vx, vy):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.Scale(vx, vy)
        return self

    def ScaleTo(self, vx, vy):
        if not self.m_property.hasMatrix:
            Utility.SyncMatrix(self)
        self.m_property.ScaleTo(vx, vy)
        return self

    def SetMatrix(self, m, sx=1, sy=1, r=0):
        self.m_property.SetMatrix(m, sx, sy, r)
        return self

    def SetAlpha(self, v):
        if not self.m_property.hasColorTransform:
            Utility.SyncColorTransform(self)
        self.m_property.SetAlpha(v)
        return self

    def SetColorTransform(self, c):
        self.m_property.SetColorTransform(c)
        return self

    def SetRenderingOffset(self, rOffset):
        self.m_property.SetRenderingOffset(rOffset)
        return self

    # lwf_movieat -------------------------------------------------------------

    def ReorderAttachedMovieList(self, reorder, index, movie):
        self.m_attachedMovieList = AttachedMovieList(self.m_attachedMovieList)
        self.m_attachedMovieList[index] = movie
        self.m_attachedMovieDescendingList[index] = index
        if reorder:
            mlist = self.m_attachedMovieList
            self.m_attachedMovieList = AttachedMovieList()
            self.m_attachedMovieDescendingList = AttachedMovieDescendingList()
            i = 0
            for m in mlist.values():
                m.depth = i
                self.m_attachedMovieList[i] = m
                self.m_attachedMovieDescendingList[i] = i
                i += 1

    @staticmethod
    def DeleteAttachedMovie(parent, movie, destroy=True, deleteFromDetachedMovies=True):
        attachName = movie.attachName
        attachDepth = movie.depth
        parent.m_attachedMovies.remove(attachName)
        parent.m_attachedMovieList.remove(attachDepth)
        parent.m_attachedMovieDescendingList.remove(attachDepth)
        if deleteFromDetachedMovies:
            parent.m_detachedMovies.remove(attachName)
        if destroy:
            movie.Destroy()

    def AttachMovieInternal(self, movie, attachName, attachDepth=-1, reorder=False):
        if self.m_attachedMovies is None:
            self.m_attachedMovies = AttachedMovies()
            self.m_detachedMovies = DetachDict()
            self.m_attachedMovieList = AttachedMovieList()
            self.m_attachedMovieDescendingList = AttachedMovieDescendingList()

        boolean, attachedMovie = self.m_attachedMovies.TryGetValue(attachName)
        if boolean:
            self.DeleteAttachedMovie(self, attachedMovie)

        if not reorder and attachDepth >= 0:
            boolean, attachedMovie = self.m_attachedMovieList.TryGetValue(attachDepth)
            if boolean:
                self.DeleteAttachedMovie(self, attachedMovie)

        movie.m_attachName = attachName
        if attachDepth >= 0:
            movie.depth = attachDepth
        else:
            e = iter(self.m_attachedMovieDescendingList)
            if next(e):
                e: SortedDictionary
                movie.depth = e.current() + 1
            else:
                movie.depth = 0
        self.m_attachedMovies[attachName] = movie
        self.ReorderAttachedMovieList(reorder, movie.depth, movie)

        return movie

    def AttachMovie(self, arg, attachName, attachDepth=-1, reorder=False,
                    load=None, postLoad=None, unload=None, enterFrame=None, update=None, render=None):
        if not isinstance(arg, Movie):
            linkageName = arg
            movieId = self.m_lwf.SearchMovieLinkage(self.m_lwf.GetStringId(linkageName))
            if movieId == -1:
                return None

            handlers = MovieEventHandlers()
            handlers.Add(self.m_lwf.GetEventOffset(), load, postLoad, unload, enterFrame, update, render)
            movie = Movie(self.m_lwf, self, movieId, -1, 0, 0, True, handlers, attachName)
            if self.m_attachMovieExeced:
                movie.Exec()
            if self.m_attachMoviePostExeced:
                movie.PostExec(True)

            return self.AttachMovieInternal(movie, attachName, attachDepth, reorder)
        else:
            movie = arg
            self.DeleteAttachedMovie(movie.parent, movie, False)
            handlers = MovieEventHandlers()
            handlers.Add(self.m_lwf.GetEventOffset(), load, postLoad, unload, enterFrame, update, render)
            movie.SetHandlers(handlers)

            movie.m_name = attachName
            return self.AttachMovieInternal(movie, attachName, attachDepth, reorder)

    def AttachEmptyMovie(self, attachName, attachDepth=-1, reorder=False, load=None, postLoad=None, unload=None,
                         enterFrame=None, update=None, render=None):
        return self.AttachMovie("_empty", attachName, attachDepth, reorder, load, postLoad, unload, enterFrame, update,
                                render)

    def SwapAttachedMovieDepth(self, depth0, depth1):
        if self.m_attachedMovies is None:
            return

        boolean, attachedMovie0 = self.m_attachedMovieList.TryGetValue(depth0)
        boolean, attachedMovie1 = self.m_attachedMovieList.TryGetValue(depth1)

        if attachedMovie0 is not None:
            attachedMovie0.depth = depth1

        if attachedMovie1 is not None:
            attachedMovie1.depth = depth0
        self.m_attachedMovieList[depth0] = attachedMovie1
        self.m_attachedMovieList[depth1] = attachedMovie0

    def GetAttachedMovie(self, arg):
        if self.m_attachedMovies is not None:
            boolean, movie = self.m_attachedMovieList.TryGetValue(arg)
            if boolean:
                return movie

    def SearchAttachedMovie(self, attachName, recursive=True):
        movie = self.GetAttachedMovie(attachName)
        if movie is not None:
            return movie

        if not recursive:
            return None

        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie():
                i = instance.SearchAttachedMovie(attachName, recursive)
                if i is not None:
                    return i
            instance = instance.linkInstance
        return None

    def DetachMovie(self, arg):
        if isinstance(arg, int):
            if self.m_detachedMovies is not None:
                boolean, movie = self.m_attachedMovieList.TryGetValue(arg)
                if boolean:
                    self.m_detachedMovies[movie.attachName] = True
        elif isinstance(arg, Movie):
            if self.m_detachedMovies is not None and arg is not None and arg.attachName is not None:
                self.m_detachedMovies[arg.attachName] = True
        else:
            if self.m_detachedMovies is not None:
                self.m_detachedMovies[arg] = True

    def DetachFromParent(self):
        if self.m_type != Format.Object.Type.ATTACHEDMOVIE:
            return

        self.m_active = False
        if self.m_parent is not None:
            self.m_parent.DetachMovie(self)

    def ReorderAttachedLWFLList(self, reorder, index, lwfContainer):
        self.m_attachedLWFList = AttachedLWFList(self.m_attachedLWFList)
        self.m_attachedLWFList[index] = lwfContainer
        self.m_attachedLWFDescendingList[index] = index
        if reorder:
            llist = self.m_attachedLWFList
            self.m_attachedLWFList = AttachedLWFList()
            self.m_attachedLWFDescendingList = AttachedLWFDescendingList()
            i = 0
            for l in llist.values():
                l.child.depth = i
                self.m_attachedLWFList[i] = l
                self.m_attachedLWFDescendingList[i] = i
                i += 1

    @staticmethod
    def DeleteAttachedLWF(parent, lwfContainer, destroy=True, deleteFromDetachedLWFs=True):
        attachName = lwfContainer.child.attachName
        attachDepth = lwfContainer.child.depth
        parent.m_attachedLWFs.remove(attachName)
        parent.m_attachedLWFList.remove(attachDepth)
        parent.m_attachedLWFDescendingList.remove(attachDepth)
        if deleteFromDetachedLWFs:
            parent.m_detachedLWFs.remove(attachName)
        if destroy:
            if lwfContainer.child.detachHandler is not None:
                lwfContainer.child.detachHandler(lwfContainer.child)
                lwfContainer.child.parent = None
                lwfContainer.detachHandler = None
                lwfContainer.child.attachName = None
                lwfContainer.child.depth = -1
            else:
                lwfContainer.child.Destroy()
            lwfContainer.Destroy()

    def AttachLWF(self, arg0, attachName, attachDepth=-1, reorder=False, arg1=None):
        if not isinstance(arg0, LWF):
            path = arg0
            texturePrefix = arg1
            if self.m_lwf.lwfLoader is None:
                return None

            child = self.m_lwf.lwfLoader(path, texturePrefix)
            if child is None:
                return None

            self.AttachLWF(child, attachName, attachDepth, reorder, lambda l: l.Destroy())
            return child
        else:
            child = arg0
            detachHandler = arg1

            if self.m_attachedLWFs is None:
                self.m_attachedLWFs = AttachedLWFs()
                self.m_detachedLWFs = DetachDict()
                self.m_attachedLWFList = AttachedLWFList()
                self.m_attachedLWFDescendingList = AttachedMovieDescendingList()

            if child.parent is not None:
                boolean, lwfContainer = child.parent.m_attachedLwfs.TryGetValue(child.attachName)
                self.DeleteAttachedLWF(child.parent, lwfContainer, False)
            boolean, lwfContainer = self.m_attachedLWFs.TryGetValue(attachName)
            if boolean:
                self.DeleteAttachedLWF(self, lwfContainer)

            if not reorder and attachDepth >= 0:
                boolean, lwfContainer = self.m_attachedLWFList.TryGetValue(attachDepth)
                if boolean:
                    self.DeleteAttachedLWF(self, lwfContainer)

            lwfContainer = LWFContainer(self, child)

            if child.interactive:
                self.m_lwf.SetInteractive()
            child.parent = self
            child.SetRoot(self.m_lwf.__root)
            child.detachHandler = detachHandler
            child.attachname = attachName
            if attachDepth >= 0:
                child.depth = attachDepth
            else:
                e = iter(self.m_attachedLWFDescendingList)
                if next(e):
                    e: SortedDictionary
                    child.depth = e.current() + 1
                else:
                    child.depth = 0
            self.m_attachedLWFs[attachName] = lwfContainer
            self.ReorderAttachedLWFLList(reorder, child.depth, lwfContainer)

            self.m_lwf.SetLWFAttached()

            return

    def SwapAttachedLWFDepth(self, depth0, depth1):
        if self.m_attachedLWFs is None:
            return

        boolean, attachedLWF0 = self.m_attachedLWFList.TryGetValue(depth0)
        boolean, attachedLWF1 = self.m_attachedLWFList.TryGetValue(depth1)
        if attachedLWF0 is not None:
            attachedLWF0.child.depth = depth1
        if attachedLWF1 is not None:
            attachedLWF1.child.depth = depth0
        self.m_attachedLWFList[depth0] = attachedLWF1
        self.m_attachedLWFList[depth1] = attachedLWF0

    def GetAttachedLWF(self, arg):
        if self.m_attachedLWFs is not None:
            boolean, lwfContainer = self.m_attachedLWFList.TryGetValue(arg)
            if boolean:
                return lwfContainer.child
        return None

    def SearchAttachedLWF(self, attachName, recursive=True):
        attachedLWF = self.GetAttachedLWF(attachName)
        if attachedLWF is not None:
            return attachedLWF

        if not recursive:
            return None

        instance = self.m_instanceHead
        while instance is not None:
            if instance.IsMovie():
                i = instance.SearchAttachedLWF(attachName, recursive)
                if i is not None:
                    return i
            instance = instance.linkInstance
        return None

    def DetachLWF(self, arg):
        if isinstance(arg, int):
            if self.m_detachedLWFs is not None:
                boolean, lwfContainer = self.m_attachedLWFList.TryGetValue(arg)
                if boolean:
                    self.m_detachedLWFs[lwfContainer.child.attachName] = True
        elif isinstance(arg, LWF):
            if self.m_detachedLWFs is not None and arg is not None and arg.attachName is not None:
                self.m_detachedLWFs[arg.attachName] = True
        else:
            if self.m_detachedLWFs is not None:
                self.m_detachedLWFs[arg] = True

    def DetachAllLWFs(self):
        if self.m_detachedLWFs is not None:
            for lwfContainer in self.m_attachedLWFs.values():
                self.m_detachedLWFs[lwfContainer.child.attachName] = True

    def RemoveMovieClup(self):
        if self.m_type == Format.Object.Type.ATTACHEDMOVIE:
            self.DetachFromParent()
        elif self.m_lwf.attachName is not None and self.m_lwf.parent is not None:
            self.m_lwf.parent.DetachLWF(self.m_lwf.attachName)

    def AttachBitmap(self, linkageName, depth):
        boolean, bitmapId = self.m_lwf.data.bitmapMap.TryGetValue(linkageName)
        if not boolean:
            return None
        bitmap = BitmapClip(self.m_lwf, self, bitmapId)
        if self.m_bitmapClips is not None:
            self.DetachBitmap(depth)
        else:
            self.m_bitmapClips = BitmapClips()
        self.m_bitmapClips[depth] = bitmap
        bitmap.depth = depth
        bitmap.name = linkageName
        return bitmap

    def GetAttachedBitMaps(self):
        return self.m_bitmapClips

    def GetAttachedBitmap(self, depth):
        if self.m_bitmapClips is None:
            return None
        boolean, bitmap = self.m_bitmapClips.TryGetValue(depth)
        return bitmap

    def SwapAttachedBitmapDepth(self, depth0, depth1):
        if self.m_bitmapClips is None:
            return

        boolean, bitmapClip0 = self.m_bitmapClips.TryGetValue(depth0)
        boolean, bitmapClip1 = self.m_bitmapClips.TryGetValue(depth1)
        if bitmapClip0 is not None:
            bitmapClip0.depth = depth1
            self.m_bitmapClips[depth1] = bitmapClip0
        else:
            self.m_bitmapClips.remove(depth1)
        if bitmapClip1 is not None:
            bitmapClip1.depth = depth0
            self.m_bitmapClips[depth0] = bitmapClip1
        else:
            self.m_bitmapClips.remove(depth0)

    def DetachBitmap(self, depth):
        if self.m_bitmapClips is None:
            return
        boolean, bitmapClip = self.m_bitmapClips.TryGetValue(depth)
        if not boolean:
            return
        bitmapClip.Destroy()
        self.m_bitmapClips.remove(depth)
