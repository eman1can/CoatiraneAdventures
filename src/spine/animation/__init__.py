from src.spine.utils import clamp


class Timeline:
    def apply(self, skeleton, lastTime, time, events, alpha):
        pass


class CurveTimeline(Timeline):
    LINEAR = 0
    STEPPED = 1
    BEZIER = 2
    BEZIER_SEGMENTS = 10
    BEZIER_SIZE = BEZIER_SEGMENTS * 2 - 1

    def __init__(self, frameCount):

        self.curves = None

        if frameCount <= 0:
            raise Exception(f"frameCount must be > 0: {frameCount}")
        self.curves = [0.0 for _ in range((frameCount - 1) * self.BEZIER_SIZE)]

    def getFrameCount(self):
        return len(self.curves) / self.BEZIER_SIZE + 1

    def setLinear(self, frameIndex):
        self.curves[frameIndex * self.BEZIER_SIZE] = self.LINEAR

    def setStepped(self, frameIndex):
        self.curves[frameIndex * self.BEZIER_SIZE] = self.STEPPED

    def getCurveType(self, frameIndex):
        index = frameIndex * self.BEZIER_SIZE
        if index == len(self.curves):
            return self.LINEAR
        ctype = self.curves[index]
        if ctype == self.LINEAR:
            return self.LINEAR
        if ctype == self.STEPPED:
            return self.STEPPED
        return self.BEZIER

    def setCurve(self, frameIndex, cx1, cy1, cx2, cy2):
        subdiv1 = 1.0 / self.BEZIER_SEGMENTS
        subdiv2 = subdiv1 * subdiv1
        subdiv3 = subdiv2 * subdiv1
        pre1 = 3 * subdiv1
        pre2 = 3 * subdiv2
        pre4 = 6 * subdiv2
        pre5 = 6 * subdiv3
        tmp1x = -cx1 * 2 + cx2
        tmp1y = -cy1 * 2 + cy2
        tmp2x = (cx1 - cx2) * 3 + 1
        tmp2y = (cy1 - cy2) * 3 + 1
        dfx, dfy = cx1 * pre1 + tmp1x * pre2 + tmp2x * subdiv3, cy1 * pre1 + tmp1y * pre2 + tmp2y * subdiv3
        ddfx, ddfy = tmp1x * pre4 + tmp2x * pre5, tmp1y * pre4 + tmp2y * pre5
        dddfx, dddfy = tmp2x * pre5, tmp2y * pre5

        i = frameIndex * self.BEZIER_SIZE
        self.curves[i] = self.BEZIER
        i += 1
        x, y = dfx, dfy
        n = i + self.BEZIER_SIZE - 1
        while i < n:
            self.curves[i] = x
            self.curves[i + 1] = y
            dfx += ddfx
            dfy += ddfy
            ddfx += dddfx
            ddfy += dddfy
            x += dfx
            y += dfy
            i += 2

    def getCurvePercent(self, frameIndex, percent):
        i = int(frameIndex * self.BEZIER_SIZE)
        ctype = self.curves[i]
        if ctype == self.LINEAR:
            return percent
        if ctype == self.STEPPED:
            return 0
        i += 1
        start = i
        n = i + self.BEZIER_SIZE - 1
        x = 0
        while i < n:
            x = self.curves[i]
            if x >= percent:
                if i == start:
                    prevX, prevY = 0, 0
                else:
                    prevX = self.curves[i - 2]
                    prevY = self.curves[i - 1]
                return prevY + (self.curves[i + 1] - prevY) * (percent - prevX) / (x - prevX)
            i += 2
        y = self.curves[i - 1]
        return y + (1 - y) * (percent - x) / (1 - x)  # Last point is 1,1


class RotateTimeline(CurveTimeline):
    PREV_FRAME_TIME = -2
    FRAME_VALUE = 1
    FRAME_SPACING = 2

    def __init__(self, frameCount):

        self.boneIndex = 0
        self.frames = None

        super().__init__(frameCount)
        self.frames = [0.0 for _ in range(frameCount << 1)]

    def getBoneIndex(self):
        return self.boneIndex

    def setBoneIndex(self, boneIndex):
        self.boneIndex = boneIndex

    def getFrames(self):
        return self.frames

    def setFrame(self, frameIndex, time, angle):
        frameIndex *= self.FRAME_SPACING
        self.frames[frameIndex] = time
        self.frames[frameIndex + self.FRAME_VALUE] = angle

    def apply(self, skeleton, lastTime, time, events, alpha):
        if time < self.frames[0]:
            return

        bone = skeleton.bones[self.boneIndex]

        if time >= self.frames[len(self.frames) - self.FRAME_SPACING]:  # Time is after last frame
            amount = bone.data.rotation + self.frames[len(self.frames) - 1] - bone.rotation
            while amount > 180:
                amount -= 360
            while amount < -180:
                amount += 360
            bone.rotation += amount * alpha
            return

        # Interpolate between the last frame and the current frame
        frameIndex = Animation.binarySearch(self.frames, time, self.FRAME_SPACING)
        prevFrameValue = self.frames[frameIndex - 1]
        frameTime = self.frames[frameIndex]
        percent = clamp(1.0 - (time - frameTime) / (self.frames[frameIndex + self.PREV_FRAME_TIME] - frameTime), 0, 1)
        percent = self.getCurvePercent((frameIndex >> 1) - 1, percent)

        amount = self.frames[frameIndex + self.FRAME_VALUE] - prevFrameValue
        while amount > 180:
            amount -= 360
        while amount < -180:
            amount += 360
        amount = bone.data.rotation + (prevFrameValue + amount * percent) - bone.rotation
        while amount > 180:
            amount -= 360
        while amount < -180:
            amount += 360
        bone.rotation += amount * alpha


class TranslateTimeline(CurveTimeline):
    PREV_FRAME_TIME = -3
    FRAME_X = 1
    FRAME_Y = 2
    FRAME_SPACING = 3

    def __init__(self, frameCount):

        self.boneIndex = 0
        self.frames = None

        super().__init__(frameCount)
        self.frames = [0 for _ in range(frameCount * self.FRAME_SPACING)]

    def getBoneIndex(self):
        return self.boneIndex

    def setBoneIndex(self, boneIndex):
        self.boneIndex = boneIndex

    def getFrames(self):
        return self.frames

    def setFrame(self, frameIndex, time, x, y):
        frameIndex *= self.FRAME_SPACING
        self.frames[frameIndex] = time
        self.frames[frameIndex + self.FRAME_X] = x
        self.frames[frameIndex + self.FRAME_Y] = y

    def apply(self, skeleton, lastTime, time, events, alpha):
        if time < self.frames[0]:  # Time is before the first frame
            return

        bone = skeleton.bones[self.boneIndex]

        if time >= self.frames[len(self.frames) - self.FRAME_SPACING]:  # Time is after the last frame.
            bone.x += (bone.data.x + self.frames[len(self.frames) - 2] - bone.x) * alpha
            bone.y += (bone.data.y + self.frames[len(self.frames) - 1] - bone.y) * alpha
            return

            # Interpolate between the last frame and the current frame
        frameIndex = Animation.binarySearch(self.frames, time, self.FRAME_SPACING)
        prevFrameX = self.frames[frameIndex - 2]
        prevFrameY = self.frames[frameIndex - 1]
        frameTime = self.frames[frameIndex]
        percent = clamp(1.0 - (time - frameTime) / (self.frames[frameIndex + self.PREV_FRAME_TIME] - frameTime), 0, 1)
        percent = self.getCurvePercent(frameIndex / self.FRAME_SPACING - 1, percent)

        bone.x += (bone.data.x + prevFrameX + (self.frames[frameIndex + self.FRAME_X] - prevFrameX) * percent - bone.x) * alpha
        bone.y += (bone.data.y + prevFrameY + (self.frames[frameIndex + self.FRAME_Y] - prevFrameY) * percent - bone.y) * alpha


class ScaleTimeline(TranslateTimeline):
    def __init__(self, frameCount):
        super().__init__(frameCount)

    def apply(self, skeleton, lastTime, time, events, alpha):
        if time < self.frames[0]:
            return

        bone = skeleton.bones[self.boneIndex]
        if time >= self.frames[len(self.frames) - self.FRAME_SPACING]:  # Time is after last frame
            bone.scaleX += (bone.data.scaleX * self.frames[len(self.frames) - 2] - bone.scaleX) * alpha
            bone.scaleY += (bone.data.scaleY * self.frames[len(self.frames) - 1] - bone.scaleY) * alpha
            return

        # Interpolate between the last frame and the current frame
        frameIndex = Animation.binarySearch(self.frames, time, self.FRAME_SPACING)
        prevFrameX = self.frames[frameIndex - 2]
        prevFrameY = self.frames[frameIndex - 1]
        frameTime = self.frames[frameIndex]
        percent = clamp(1.0 - (time - frameTime) / (self.frames[frameIndex + self.PREV_FRAME_TIME] - frameTime), 0, 1)
        percent = self.getCurvePercent(frameIndex / self.FRAME_SPACING - 1, percent)

        bone.scaleX += (bone.data.scaleX * (prevFrameX + (self.frames[frameIndex + self.FRAME_X] - prevFrameX) * percent) - bone.scaleX) * alpha
        bone.scaleY += (bone.data.scaleY * (prevFrameY + (self.frames[frameIndex + self.FRAME_Y] - prevFrameY) * percent) - bone.scaleY) * alpha
        return


class ColorTimeline(CurveTimeline):
    PREV_FRAME_TIME = -5
    FRAME_R = 1
    FRAME_G = 2
    FRAME_B = 3
    FRAME_A = 4
    FRAME_SPACING = 5

    def __init__(self, frameCount):

        self.slotIndex = 0
        self.frames = None

        super().__init__(frameCount)
        self.frames = [0 for _ in range(frameCount * self.FRAME_SPACING)]

    def getSlotIndex(self):
        return self.slotIndex

    def setSlotIndex(self, slotIndex):
        self.slotIndex = slotIndex

    def getFrames(self):
        return self.frames

    def setFrame(self, frameIndex, time, r, g, b, a):
        frameIndex *= self.FRAME_SPACING
        self.frames[frameIndex] = time
        self.frames[frameIndex + self.FRAME_R] = r
        self.frames[frameIndex + self.FRAME_G] = g
        self.frames[frameIndex + self.FRAME_B] = b
        self.frames[frameIndex + self.FRAME_A] = a

    def apply(self, skeleton, lastTime, time, events, alpha):
        if time < self.frames[0]:  # Time is before first frame.
            return

        if time >= self.frames[len(self.frames) - 5]:  # -5
            i = len(self.frames) - 1
            r = self.frames[i - 3]  # -4
            g = self.frames[i - 2]  # -3
            b = self.frames[i - 1]  # -2
            a = self.frames[i]  # -1
        else:
            # Interpolate between the last frame and the current frame.
            frameIndex = Animation.binarySearch(self.frames, time, self.FRAME_SPACING)
            prevFrameR = self.frames[frameIndex - 4]
            prevFrameG = self.frames[frameIndex - 3]
            prevFrameB = self.frames[frameIndex - 2]
            prevFrameA = self.frames[frameIndex - 1]
            frameTime = self.frames[frameIndex]
            percent = clamp(1.0 - (time - frameTime) / (self.frames[frameIndex + self.PREV_FRAME_TIME] - frameTime), 0, 1)
            percent = self.getCurvePercent(frameIndex / self.FRAME_SPACING - 1, percent)

            r = prevFrameR + (self.frames[frameIndex + self.FRAME_R] - prevFrameR) * percent
            g = prevFrameG + (self.frames[frameIndex + self.FRAME_G] - prevFrameG) * percent
            b = prevFrameB + (self.frames[frameIndex + self.FRAME_B] - prevFrameB) * percent
            a = prevFrameA + (self.frames[frameIndex + self.FRAME_A] - prevFrameA) * percent
        color = skeleton.slots[self.slotIndex].color
        if alpha < 1:
            color.r += (r - color.r) * alpha
            color.g += (g - color.g) * alpha
            color.b += (b - color.b) * alpha
            color.a += (a - color.a) * alpha
        else:
            color.r = r
            color.g = g
            color.b = b
            color.a = a


class AttachmentTimeline(Timeline):
    MAX_VALUE = 2147483647

    def __init__(self, frameCount):

        self.slotIndex = 0
        self.frames = None
        self.attachmentNames = None

        self.frames = [0.0 for _ in range(frameCount)]
        self.attachmentNames = [0.0 for _ in range(frameCount)]

    def getFrameCount(self):
        return len(self.frames)

    def getSlotIndex(self):
        return self.slotIndex

    def setSlotIndex(self, slotIndex):
        self.slotIndex = slotIndex

    def getFrames(self):
        return self.frames

    def getAttachmentNames(self):
        return self.attachmentNames

    def setFrame(self, frameIndex, time, attachmentName):
        self.frames[frameIndex] = time
        self.attachmentNames[frameIndex] = attachmentName

    def apply(self, skeleton, lastTime, time, events, alpha):
        if time < self.frames[0]:  # Time is before first frame
            if lastTime < time:
                self.apply(skeleton, lastTime, self.MAX_VALUE, None, 0)
            return
        elif lastTime > time:
            lastTime = -1

        frameIndex = (len(self.frames) if time >= self.frames[len(self.frames) - 1] else Animation.binarySearch(self.frames, time)) - 1
        if self.frames[frameIndex] < lastTime:
            return
        attachmentName = self.attachmentNames[frameIndex]
        skeleton.slots[self.slotIndex].setAttachment(None if attachmentName is None else skeleton.getAttachment(self.slotIndex, attachmentName))


class EventTimeline(Timeline):
    MAX_VALUE = 2147483647

    def __init__(self, frameCount):

        self.frames = None
        self.events = None

        self.frames = [0.0 for _ in range(frameCount)]
        self.events = [0.0 for _ in range(frameCount)]

    def getFrameCount(self):
        return len(self.frames)

    def getFrames(self):
        return self.frames

    def getEvents(self):
        return self.events

    def setFrame(self, frameIndex, time, event):
        self.frames[frameIndex] = time
        self.events[frameIndex] = event

    def apply(self, skeleton, lastTime, time, firedEvents, alpha):
        if firedEvents is None:
            return
        frameCount = len(self.frames)

        if lastTime > time:
            self.apply(skeleton, lastTime, self.MAX_VALUE, firedEvents, alpha)
            lastTime = -1
        elif lastTime >= self.frames[frameCount - 1]:
            return
        if time < self.frames[0]:
            return

        if lastTime < self.frames[0]:
            frameIndex = 0
        else:
            frameIndex = Animation.binarySearch(self.frames, lastTime)
            frame = self.frames[frameIndex]
            while frameIndex > 0:
                if self.frames[frameIndex - 1] != frame:
                    break
                frameIndex -= 1
        while frameIndex < frameCount and time >= self.frames[frameIndex]:
            firedEvents.add(self.events[frameIndex])
            frameIndex += 1


class DrawOrderTimeline(Timeline):

    def __init__(self, frameCount):

        self.frames = None
        self.drawOrders = None

        self.frames = [0.0 for _ in range(frameCount)]
        self.drawOrders = [[] for _ in range(frameCount)]

    def getFrameCount(self):
        return len(self.frames)

    def getFrames(self):
        return self.frames

    def getDrawOrders(self):
        return self.drawOrders

    def setFrame(self, frameIndex, time, drawOrder):
        self.frames[frameIndex] = time
        self.drawOrders[frameIndex] = drawOrder

    def apply(self, skeleton, lastTime, time, events, alpha):
        if time < self.frames[0]:
            return

        if time >= self.frames[len(self.frames) - 1]:
            frameIndex = len(self.frames) - 1
        else:
            frameIndex = Animation.binarySearch(self.frames, time) - 1

        drawOrder = skeleton.drawOrder
        slots = skeleton.slots
        drawOrderToSetupIndex = self.drawOrders[frameIndex]
        if drawOrderToSetupIndex is None:
            for x, slot in enumerate(slots):
                drawOrder[x] = slot
        else:
            for i in range(len(drawOrderToSetupIndex)):
                drawOrder[i] = slots[drawOrderToSetupIndex[i]]


class FfdTimeline(CurveTimeline):

    def __init__(self, frameCount):

        self.frames = None
        self.frameVertices = None
        self.slotIndex = 0
        self.attachment = None

        super().__init__(frameCount)
        self.frames = [0.0 for _ in range(frameCount)]
        self.frameVertices = [[] for _ in range(frameCount)]

    def getSlotIndex(self):
        return self.slotIndex

    def setSlotIndex(self, slotIndex):
        self.slotIndex = slotIndex

    def getAttachment(self):
        return self.attachment

    def setAttachment(self, attachment):
        self.attachment = attachment

    def getFrames(self):
        return self.frames

    def getVertices(self):
        return self.frameVertices

    def setFrame(self, frameIndex, time, vertices):
        self.frames[frameIndex] = time
        self.frameVertices[frameIndex] = vertices

    def apply(self, skeleton, lastTime, time, events, alpha):
        slot = skeleton.slots[self.slotIndex]
        if slot.getAttachment() != self.attachment:
            return

        if time < self.frames[0]:
            return

        vertexCount = len(self.frameVertices[0])

        verticesArray = slot.getAttachmentVertices()
        if len(verticesArray) != vertexCount:
            alpha = 1
            if len(verticesArray) < vertexCount:
                vertices = verticesArray + [0 for _ in range(vertexCount - len(verticesArray))]
            else:
                vertices = verticesArray[:vertexCount]
        else:
            vertices = verticesArray

        if time >= self.frames[len(self.frames) - 1]:
            lastVertices = self.frameVertices[len(self.frames) - 1]
            if alpha < 1:
                for i in range(len(vertices)):
                    vertices[i] += (lastVertices[i] - vertices[i]) * alpha
            else:
                for i in range(vertexCount):
                    vertices[i] = lastVertices[i]
            return

        frameIndex = Animation.binarySearch(self.frames, time)
        frameTime = self.frames[frameIndex]
        percent = clamp(1.0 - (time - frameTime) / (self.frames[frameIndex - 1] - frameTime), 0, 1)
        percent = self.getCurvePercent(frameIndex - 1, percent)

        prevVertices = self.frameVertices[frameIndex - 1]
        nextVertices = self.frameVertices[frameIndex]

        if alpha < 1:
            for i in range(vertexCount):
                prev = prevVertices[i]
                vertices[i] += (prev + (nextVertices[i] - prev) * percent - vertices[i]) * alpha
        else:
            for i in range(vertexCount):
                prev = prevVertices[i]
                vertices[i] = prev + (nextVertices[i] - prev) * percent
        slot.setAttachmentVertices(vertices)


class IkConstraintTimeline(CurveTimeline):
    PREV_FRAME_TIME = -3
    PREV_FRAME_MIX = -2
    PREV_FRAME_BEND_DIRECTION = -1
    FRAME_MIX = 1
    FRAME_SPACING = 3

    def __init__(self, frameCount):

        self.ikConstraintIndex = 0
        self.frames = None

        super().__init__(frameCount)
        self.frames = [0.0 for _ in range(frameCount * self.FRAME_SPACING)]

    def getIkConstraintIndex(self):
        return self.ikConstraintIndex

    def setIkConstraintIndex(self, ikConstraint):
        self.ikConstraintIndex = ikConstraint

    def getFrames(self):
        return self.frames

    def setFrame(self, frameIndex, time, mix, bendDirection):
        frameIndex *= self.FRAME_SPACING
        self.frames[frameIndex] = time
        self.frames[frameIndex + 1] = mix
        self.frames[frameIndex + 2] = bendDirection

    def apply(self, skeleton, lastTime, time, events, alpha):
        if time < self.frames[0]:
            return

        ikConstraint = skeleton.ikConstraints[self.ikConstraintIndex]

        if time >= self.frames[len(self.frames) - self.FRAME_SPACING]:
            ikConstraint.mix += (self.frames[len(self.frames) - 2] - ikConstraint.mix) * alpha
            ikConstraint.bendDirection = int(self.frames[len(self.frames) - 1])
            return

        frameIndex = Animation.binarySearch(self.frames, time, self.FRAME_SPACING)
        prevFrameMix = self.frames[frameIndex + self.PREV_FRAME_MIX]
        frameTime = self.frames[frameIndex]
        percent = clamp(1.0 - (time - frameTime) / (self.frames[frameIndex + self.PREV_FRAME_TIME] - frameTime), 0, 1)
        percent = self.getCurvePercent(frameIndex / self.FRAME_SPACING - 1, percent)

        mix = prevFrameMix + (self.frames[frameIndex + self.FRAME_MIX] - prevFrameMix) * percent
        ikConstraint.mix += (mix - ikConstraint.mix) * alpha
        ikConstraint.bendDirection = int(self.frames[frameIndex + self.PREV_FRAME_BEND_DIRECTION])


class FlipXTimeline(Timeline):
    MAX_VALUE = 2147483647
    FRAME_SPACING = 2

    def __init__(self, frameCount):

        self.boneIndex = 0
        self.frames = None

        self.frames = [0.0 for _ in range(frameCount << 1)]

    def getBoneIndex(self):
        return self.boneIndex

    def setBoneIndex(self, boneIndex):
        self.boneIndex = boneIndex

    def getFrameCount(self):
        return len(self.frames) >> 1

    def getFrames(self):
        return self.frames

    def setFrame(self, frameIndex, time, flip):
        frameIndex *= self.FRAME_SPACING
        self.frames[frameIndex] = time
        self.frames[frameIndex + 1] = 1 if flip else 0

    def apply(self, skeleton, lastTime, time, events, alpha):
        if time < self.frames[0]:
            if lastTime < time:
                self.apply(skeleton, lastTime, self.MAX_VALUE, None, 0)
                return
        elif lastTime > time:
            lastTime = -1
        frameIndex = len(self.frames) if time >= self.frames[len(self.frames) - self.FRAME_SPACING] else Animation.binarySearch(self.frames, time, self.FRAME_SPACING) - self.FRAME_SPACING
        if self.frames[frameIndex] < lastTime:
            return
        self.setFlip(skeleton.bones.get(self.boneIndex), self.frames[frameIndex + 1] != 0)

    def setFlip(self, bone, flip):
        bone.setFlipX(flip)


class FlipYTimeline(FlipXTimeline):
    def __init__(self, frameCount):
        super().__init__(frameCount)

    def setFlip(self, bone, flip):
        bone.setFlipY(flip)


class Animation:

    def __init__(self, name, timelines, duration):

        self.name = None
        self.timelines = None
        self.duration = None

        if name is None:
            raise Exception("Name cannot be None")
        if timelines is None:
            raise Exception("timelines cannot be None")
        self.name = name
        self.timelines = timelines
        self.duration = duration

    def getTimelines(self):
        return self.timelines

    def getDuration(self):
        return self.duration

    def setDuration(self, duration):
        self.duration = duration

    def apply(self, skeleton, lastTime, time, loop, events):
        if skeleton is None:
            raise Exception("skeleton cannot be None")

        if loop and self.duration != 0:
            time %= self.duration
            lastTime %= self.duration

        for i in range(len(self.timelines)):
            self.timelines[i].apply(skeleton, lastTime, time, events, 1)

    def mix(self, skeleton, lastTime, time, loop, events, alpha):
        if skeleton is None:
            raise Exception("skeleton cannot be None")

        if loop and self.duration != 0:
            time %= self.duration
            lastTime %= self.duration

        for i in range(len(self.timelines)):
            self.timelines[i].apply(skeleton, lastTime, time, events, alpha)

    def getName(self):
        return self.name

    def __str__(self):
        return self.name

    @staticmethod
    def binarySearch(values, target, step=1):
        low = 0
        high = int(len(values) / step - 2)
        if high == 0:
            return step
        current = high >> 1
        while True:
            if values[(current + 1) * step] <= target:
                low = current + 1
            else:
                high = current
            if low == high:
                return (low + 1) * step
            current = (low + high) >> 1

    @staticmethod
    def linearSearch(values, target, step):
        for i in range(0, len(values) - step, step):
            if values[i] > target:
                return i
        return -1
