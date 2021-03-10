import os
from kivy.graphics import Color

from src.spine.animation import ColorTimeline, AttachmentTimeline, RotateTimeline, ScaleTimeline, TranslateTimeline, FlipXTimeline, FlipYTimeline, IkConstraintTimeline, FfdTimeline, DrawOrderTimeline, EventTimeline, Animation
from src.spine.animation.eventdata import EventData
from src.spine.animation.event import Event
from src.spine.atlas.atlasattachmentloader import AtlasAttachmentLoader
from src.spine.attachment.attachmentloader import AttachmentLoader
from src.spine.attachment.attachmenttype import AttachmentType
from src.spine.attachment.meshattachment import MeshAttachment
from src.spine.bone.bonedata import BoneData
from src.spine.skeleton.skeletondata import SkeletonData
from src.spine.slot.slotdata import SlotData
from src.spine.skin import Skin
from src.spine.utils import DataInput
from src.spine.utils.filehandle import FileHandle
from src.spine.ikconstraint.ikconstraintdata import IkConstraintData


class SkeletonBinary:
    TIMELINE_SCALE = 0
    TIMELINE_ROTATE = 1
    TIMELINE_TRANSLATE = 2
    TIMELINE_ATTACHMENT = 3
    TIMELINE_COLOR = 4
    TIMELINE_FLIPX = 5
    TIMELINE_FLIPY = 6

    CURVE_LINEAR = 0
    CURVE_STEPPED = 1
    CURVE_BEZIER = 2

    def __init__(self, arg):

        self.tempColor = Color()

        self.attachmentLoader = None
        self.scale = 1

        if isinstance(arg, AttachmentLoader):
            self.attachmentLoader = arg
        else:
            self.attachmentLoader = AtlasAttachmentLoader(arg)

    def getScale(self):
        return self.scale

    def setScale(self, scale):
        self.scale = scale

    def rgba8888ToColor(self, color, value):
        color.r = ((value & 0xff000000) >> 24) / 255
        color.g = ((value & 0x00ff0000) >> 16) / 255
        color.b = ((value & 0x0000ff00) >> 8) / 255
        color.a = (value & 0x000000ff) / 255

    def readSkeletonData(self, file: FileHandle, debug=False):
        if file is None:
            raise Exception("IllegalArgumentException: File cannot be null")
        scale = self.scale

        skeletonData = SkeletonData()
        skeletonData.name = file.nameWithoutExtension()

        if debug:
            print(f"Reading binary Skeleton: {file.name()}")
        open_file = open(str(file.full_path()), "rb", 512)
        input = DataInput(open_file)
        try:
            skeletonData.hash = input.readString()
            if debug:
                print(f"Hash: {skeletonData.hash}")
            skeletonData.version = input.readString()
            if debug:
                print(f"Version: '''{skeletonData.version}'''")
            skeletonData.width = input.readFloat()
            if debug:
                print(f"Width: {float(skeletonData.width)}")
            skeletonData.height = input.readFloat()
            if debug:
                print(f"Height: {float(skeletonData.height)}")

            nonessential = input.readBoolean()

            if nonessential:
                skeletonData.imagesPath = input.readString()

            # Bones
            for i in range(input.readVarInt(True)):
                name = input.readString()
                parent = None
                parentIndex = input.readVarInt(True) - 1
                if parentIndex != -1:
                    parent = skeletonData.bones[parentIndex]
                boneData = BoneData(name, parent)
                boneData.x = input.readFloat() * scale
                boneData.y = input.readFloat() * scale
                boneData.scaleX = input.readFloat()
                boneData.scaleY = input.readFloat()
                boneData.rotation = input.readFloat()
                boneData.length = input.readFloat() * scale
                boneData.flipX = input.readBoolean()
                boneData.flipY = input.readBoolean()
                boneData.inheritScale = input.readBoolean()
                boneData.inheritRotation = input.readBoolean()
                if nonessential:
                    self.rgba8888ToColor(boneData.color, input.readInt())
                skeletonData.bones.append(boneData)

            # Ik Constraints
            for i in range(input.readVarInt(True)):
                ikConstraintData = IkConstraintData(input.readString())
                for ii in range(input.readVarInt(True)):
                    ikConstraintData.bones.append(skeletonData.bones[input.readVarInt(True)])
                ikConstraintData.target = skeletonData.bones[input.readVarInt(True)]
                ikConstraintData.mix = input.readFloat()
                ikConstraintData.bendDirection = input.readByte()
                skeletonData.ikConstraints.append(ikConstraintData)

            # Slots
            # print("Slots:")
            for i in range(input.readVarInt(True)):
                slotName = input.readString()
                # print(f"\tName: {slotName}")
                boneData = skeletonData.bones[input.readVarInt(True)]
                # print(f"\tBoneName: {boneData.name}")
                slotData = SlotData(slotName, boneData)
                self.rgba8888ToColor(slotData.color, input.readInt())
                slotData.attachmentName = input.readString()
                # print(f"\tAttachment Name: {slotData.attachmentName}")
                slotData.additiveBlending = input.readBoolean()
                skeletonData.slots.append(slotData)

            # Default Skin
            defaultSkin = self.readSkin(input, "default", nonessential)
            if defaultSkin is not None:
                skeletonData.defaultSkin = defaultSkin
                skeletonData.skins.append(defaultSkin)

            # Skins
            for i in range(input.readVarInt(True)):
                skeletonData.skins.append(self.readSkin(input, input.readString(), nonessential))

            # Events
            for i in range(input.readVarInt(True)):
                eventData = EventData(input.readString())
                eventData.intValue = input.readVarInt(False)
                eventData.floatValue = input.readFloat()
                eventData.stringVale = input.readString()
                skeletonData.events.append(eventData)

            # Animations
            for i in range(input.readVarInt(True)):
                self.readAnimation(input.readString(), input, skeletonData)
        except IOError:
            raise Exception("Error reading Skeleton file")
        finally:
            try:
                open_file.close()
            except IOError:
                pass
        return skeletonData

    def readSkin(self, input, skinName, nonessential):
        slotCount = input.readVarInt(True)
        if slotCount == 0:
            return None
        skin = Skin(skinName)
        for i in range(slotCount):
            slotIndex = input.readVarInt(True)
            for ii in range(input.readVarInt(True)):
                name = input.readString()
                skin.addAttachment(slotIndex, name, self.readAttachment(input, skin, name, nonessential))
        return skin

    def readAttachment(self, input, skin, attachmentName, nonessential):
        scale = self.scale

        name = input.readString()
        if name is None:
            name = attachmentName

        # print("Attachment Name:", name)

        type = AttachmentType(input.readByte())
        # print("Attachment Type: ", type)
        if type == AttachmentType.region:
            path = input.readString()
            if path is None:
                path = name
            region = self.attachmentLoader.newRegionAttachment(skin, name, path)
            if region is None:
                return None
            region.setPath(path)
            region.setX(input.readFloat() * scale)
            region.setY(input.readFloat() * scale)
            region.setScaleX(input.readFloat())
            region.setScaleY(input.readFloat())
            region.setRotation(input.readFloat())
            region.setWidth(input.readFloat() * scale)
            region.setHeight(input.readFloat() * scale)
            self.rgba8888ToColor(region.getColor(), input.readInt())
            region.updateOffset()
            return region
        elif type == AttachmentType.boundingbox:
            box = self.attachmentLoader.newBoundingBoxAttachment(skin, name)
            if box is None:
                return None
            box.setVertices(self.readFloatArray(input, scale))
            return box
        elif type == AttachmentType.mesh:
            path = input.readString()
            if path is None:
                path = name
            mesh = self.attachmentLoader.newMeshAttachment(skin, name, path)
            if mesh is None:
                return None
            mesh.setPath(path)
            uvs = self.readFloatArray(input, 1)
            triangles = self.readShortArray(input)
            vertices = self.readFloatArray(input, scale)
            mesh.setVertices(vertices)
            mesh.setTriangles(triangles)
            mesh.setRegionUVs(uvs)
            mesh.updateUVs()
            self.rgba8888ToColor(mesh.getColor(), input.readInt())
            mesh.setHullLength(input.readVarInt(True) * 2)
            if nonessential:
                mesh.setEdges(self.readIntArray(input))
                mesh.setWidth(input.readFloat() * scale)
                mesh.setHeight(input.readFloat() * scale)
            return mesh
        elif type == AttachmentType.skinnedmesh:
            path = input.readString()
            if path is None:
                path = name
            mesh = self.attachmentLoader.newSkinnedMeshAttachment(skin, name, path)
            if mesh is None:
                return None
            mesh.setPath(path)
            uvs = self.readFloatArray(input, 1)
            triangles = self.readShortArray(input)

            vertexCount = input.readVarInt(True)
            weights = []
            bones = []
            i = 0
            while i < vertexCount:
                boneCount = int(input.readFloat())
                bones.append(boneCount)
                nn = i + boneCount * 4
                while i < nn:
                    bones.append(int(input.readFloat()))
                    weights.append(input.readFloat() * scale)
                    weights.append(input.readFloat() * scale)
                    weights.append(input.readFloat())
                    i += 4
                i += 1
            mesh.setBones(bones)
            mesh.setWeights(weights)
            mesh.setTriangles(triangles)
            mesh.setRegionUVs(uvs)
            mesh.updateUVs()
            self.rgba8888ToColor(mesh.getColor(), input.readInt())
            mesh.setHullLength(input.readVarInt(True) * 2)
            if nonessential:
                mesh.setEdges(self.readIntArray(input))
                mesh.setWidth(input.readFloat() * scale)
                mesh.setHeight(input.readFloat() * scale)
            return mesh
        return None

    def readFloatArray(self, input, scale):
        length = input.readVarInt(True)
        array = []
        if scale == 1:
            for i in range(length):
                # print("Got num", num)
                array.append(input.readFloat())
        else:
            for i in range(length):
                # print("Got num", num)
                array.append(input.readFloat() * scale)
                # print("Scale", scale)
        return array

    def readShortArray(self, input):
        array = []
        for i in range(input.readVarInt(True)):
            array.append(input.readShort())
        return array

    def readIntArray(self, input):
        array = []
        for i in range(input.readVarInt(True)):
            array.append(input.readVarInt(True))
        return array

    def readAnimation(self, name, input, skeletonData):
        timelines = []
        scale = self.scale
        duration = 0
        try:
            # Slot Timelines
            for i in range(input.readVarInt(True)):
                slotIndex = input.readVarInt(True)
                for ii in range(input.readVarInt(True)):
                    timelineType = input.readByte()
                    frameCount = input.readVarInt(True)
                    if timelineType == self.TIMELINE_COLOR:
                        timeline = ColorTimeline(frameCount)
                        timeline.slotIndex = slotIndex
                        for frameIndex in range(frameCount):
                            time = input.readFloat()
                            self.rgba8888ToColor(self.tempColor, input.readInt())
                            timeline.setFrame(frameIndex, time, self.tempColor.r, self.tempColor.g, self.tempColor.b, self.tempColor.a)
                            if frameIndex < frameCount - 1:
                                self.readCurve(input, frameIndex, timeline)
                        timelines.append(timeline)
                        duration = max(duration, timeline.getFrames()[frameCount * 5 - 5])
                    elif timelineType == self.TIMELINE_ATTACHMENT:
                        timeline = AttachmentTimeline(frameCount)
                        timeline.slotIndex = slotIndex
                        for frameIndex in range(frameCount):
                            timeline.setFrame(frameIndex, input.readFloat(), input.readString())
                        timelines.append(timeline)
                        duration = max(duration, timeline.getFrames()[frameCount - 1])
            # Bone Timelines
            for i in range(input.readVarInt(True)):
                boneIndex = input.readVarInt(True)
                for ii in range(input.readVarInt(True)):
                    timelineType = input.readByte()
                    frameCount = input.readVarInt(True)
                    if timelineType == self.TIMELINE_ROTATE:
                        timeline = RotateTimeline(frameCount)
                        timeline.boneIndex = boneIndex
                        for frameIndex in range(frameCount):
                            timeline.setFrame(frameIndex, input.readFloat(), input.readFloat())
                            if frameIndex < frameCount - 1:
                                self.readCurve(input, frameIndex, timeline)
                        timelines.append(timeline)
                        duration = max(duration, timeline.getFrames()[frameCount * 2 - 2])
                    elif timelineType == self.TIMELINE_TRANSLATE or timelineType == self.TIMELINE_SCALE:
                        timelineScale = 1
                        if timelineType == self.TIMELINE_SCALE:
                            timeline = ScaleTimeline(frameCount)
                        else:
                            timeline = TranslateTimeline(frameCount)
                            timelineScale = scale
                        timeline.boneIndex = boneIndex
                        for frameIndex in range(frameCount):
                            timeline.setFrame(frameIndex, input.readFloat(), input.readFloat() * timelineScale, input.readFloat() * timelineScale)
                            if frameIndex < frameCount - 1:
                                self.readCurve(input, frameIndex, timeline)
                        timelines.append(timeline)
                        duration = max(duration, timeline.getFrames()[frameCount * 3 - 3])
                    elif timelineType == self.TIMELINE_FLIPX or self.TIMELINE_FLIPY:
                        timeline = FlipXTimeline(frameCount) if timelineType == self.TIMELINE_FLIPX else FlipYTimeline(frameCount)
                        timeline.boneIndex = boneIndex
                        for frameIndex in range(frameCount):
                            timeline.setFrame(frameIndex, input.readFloat(), input.readBoolean())
                        timelines.append(timeline)
                        duration = max(duration, timeline.getFrames()[frameCount * 2 - 2])

            # IK timelines
            for i in range(input.readVarInt(True)):
                ikConstraint = skeletonData.ikConstraints[input.readVarInt(True)]
                frameCount = input.readVarInt(True)
                timeline = IkConstraintTimeline(frameCount)
                timeline.ikConstraintIndex = skeletonData.getIkConstraints().index(ikConstraint)
                for frameIndex in range(frameCount):
                    timeline.setFrame(frameIndex, input.readFloat(), input.readFloat(), input.readByte())
                    if frameIndex < frameCount - 1:
                        self.readCurve(input, frameIndex, timeline)
                timelines.append(timeline)
                duration = max(duration, timeline.getFrames()[frameCount * 3 - 3])

            # FFD timelines
            for i in range(input.readVarInt(True)):
                skin = skeletonData.skins[input.readVarInt(True)]
                for ii in range(input.readVarInt(True)):
                    slotIndex = input.readVarInt(True)
                    for iii in range(input.readVarInt(True)):
                        attachment = skin.getAttachment(slotIndex, input.readString())
                        frameCount = input.readVarInt(True)
                        timeline = FfdTimeline(frameCount)
                        timeline.slotIndex = slotIndex
                        timeline.attachment = attachment
                        for frameIndex in range(frameCount):
                            time = input.readFloat()
                            if isinstance(attachment, MeshAttachment):
                                vertexCount = len(attachment.getVertices())
                            else:
                                vertexCount = int(len(attachment.getWeights()) / 3 * 2)

                            end = input.readVarInt(True)
                            if end == 0:
                                if isinstance(attachment, MeshAttachment):
                                    vertices = attachment.getVertices()
                                else:
                                    vertices = [0.0 for _ in range(vertexCount)]
                            else:
                                vertices = [0.0 for _ in range(vertexCount)]
                                start = input.readVarInt(True)
                                end += start
                                if scale == 1:
                                    for v in range(start, end):
                                        vertices[v] = input.readFloat()
                                else:
                                    for v in range(start, end):
                                        vertices[v] = input.readFloat() * scale
                                if isinstance(attachment, MeshAttachment):
                                    meshVertices = attachment.getVertices()
                                    for v in range(len(vertices)):
                                        vertices[v] += meshVertices[v]
                            timeline.setFrame(frameIndex, time, vertices)
                            if frameIndex < frameCount - 1:
                                self.readCurve(input, frameIndex, timeline)
                        timelines.append(timeline)
                        duration = max(duration, timeline.getFrames()[frameCount - 1])

            # Draw order timeline
            drawOrderCount = input.readVarInt(True)
            # print(f"There are {drawOrderCount} drawOrder timelines")
            if drawOrderCount > 0:
                timeline = DrawOrderTimeline(drawOrderCount)
                slotCount = len(skeletonData.slots)
                for i in range(drawOrderCount):
                    offsetCount = input.readVarInt(True)
                    # print(f"OffsetCount: {offsetCount}")
                    drawOrder = [0 for x in range(slotCount)]
                    for ii in range(slotCount - 1, -1, -1):
                        drawOrder[ii] = -1
                    unchanged = [0 for x in range(slotCount - offsetCount)]
                    originalIndex, unchangedIndex = 0, 0
                    for ii in range(offsetCount):
                        slotIndex = input.readVarInt(True)
                        # print(f"slotIndex: {slotIndex}")
                        while originalIndex != slotIndex:
                            unchanged[unchangedIndex] = originalIndex
                            unchangedIndex += 1
                            originalIndex += 1
                        add_index = input.readVarInt(True)
                        # print(f"OrigIndex, add_index: {originalIndex}, {add_index}")
                        drawOrder[originalIndex + add_index] = originalIndex
                        originalIndex += 1
                    while originalIndex < slotCount:
                        unchanged[unchangedIndex] = originalIndex
                        unchangedIndex += 1
                        originalIndex += 1
                    for ii in range(slotCount - 1, -1, -1):
                        if drawOrder[ii] == -1:
                            unchangedIndex -= 1
                            drawOrder[ii] = unchanged[unchangedIndex]
                    timeline.setFrame(i, input.readFloat(), drawOrder)
                timelines.append(timeline)
                duration = max(duration, timeline.getFrames()[drawOrderCount - 1])

            # Event timelines
            eventCount = input.readVarInt(True)
            if eventCount > 0:
                timeline = EventTimeline(eventCount)
                for i in range(eventCount):
                    time = input.readFloat()
                    eventData = skeletonData.events[input.readVarInt(True)]
                    event = Event(eventData)
                    event.intValue = input.readVarInt(False)
                    event.floatValue = input.readFloat()
                    event.stringValue = input.readString() if input.readBoolean() else eventData.stringValue
                    timeline.setFrame(i, time, event)
                timelines.append(timeline)
                duration = max(duration, timeline.getFrames()[eventCount - 1])
        except IOError:
            raise Exception("Error reading skeleton file.")
        skeletonData.animations.append(Animation(name, timelines, duration))

    def readCurve(self, input, frameIndex, timeline):
        value = input.readByte()
        if value == self.CURVE_STEPPED:
            timeline.setStepped(frameIndex)
        elif value == self.CURVE_BEZIER:
            self.setCurve(timeline, frameIndex, input.readFloat(), input.readFloat(), input.readFloat(), input.readFloat())

    def setCurve(self, timeline, frameIndex, cx1, cy1, cx2, cy2):
        timeline.setCurve(frameIndex, cx1, cy1, cx2, cy2)