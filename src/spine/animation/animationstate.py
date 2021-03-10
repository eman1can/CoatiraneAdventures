from src.spine.utils.pool import Pool, Poolable
from src.spine.utils.array import Array


class TrackEntry(Poolable):

    def __init__(self):

        self.next = None
        self.previous = None
        self.animation = None
        self.loop = False
        self.delay = 0.0
        self.time = 0.0
        self.lastTime = -1
        self.endTime = 0.0
        self.timeScale = 1
        self.mixTime = 0.0
        self.mixDuration = 0.0
        self.listener = None
        self.mix = 1

        super().__init__()

    def reset(self):
        self.next = None
        self.previous = None
        self.animation = None
        self.listener = None
        self.timeScale = 1
        self.lastTime = -1
        self.time = 0

    def getAnimation(self):
        return self.animation

    def setAnimation(self, animation):
        self.animation = animation

    def getLoop(self):
        return self.loop

    def setLoop(self, loop):
        self.loop = loop

    def getDelay(self):
        return self.delay

    def setDelay(self, delay):
        self.delay = delay

    def getTime(self):
        return self.time

    def setTime(self, time):
        self.time = time

    def getEndTime(self):
        return self.endTime

    def setEndTime(self, endTime):
        self.endTime = endTime

    def getListener(self):
        return self.listener

    def setListener(self, listener):
        self.listener = listener

    def getLastTime(self):
        return self.lastTime

    def setLastTime(self, lastTime):
        self.lastTime = lastTime

    def getMix(self):
        return self.mix

    def setMix(self, mix):
        self.mix = mix

    def getTimeScale(self):
        return self.timeScale

    def setTimeScale(self, timeScale):
        self.timeScale = timeScale

    def getNext(self):
        return self.next

    def setNext(self, next):
        self.next = next

    def isComplete(self):
        return self.time >= self.endTime

    def __str__(self):
        return "<none>" if self.animation is None else self.animation.name


class AnimationStateListener:
    def event(self, trackIndex, event):
        pass

    def complete(self, trackIndex, loopCount):
        pass

    def start(self, trackIndex):
        pass

    def end(self, trackIndex):
        pass


class AnimationStateAdapter(AnimationStateListener):
    def event(self, trackIndex, event):
        pass

    def complete(self, trackIndex, loopCount):
        pass

    def start(self, trackIndex):
        pass

    def end(self, trackIndex):
        pass


class TrackEntryPool(Pool):
    def newObject(self):
        return TrackEntry()


class AnimationState:

    def __init__(self, data):

        self.data = None
        self.tracks = Array()
        self.events = Array()
        self.listeners = Array()
        self.timeScale = 1

        self.trackEntryPool = TrackEntryPool()

        if data is None:
            raise Exception("Data cannot be None")
        self.data = data

    def update(self, delta):
        delta *= self.timeScale
        for i in range(len(self.tracks)):
            current = self.tracks.get(i)
            if current is None:
                continue

            current.time += delta * current.timeScale
            if current.previous is not None:
                previousDelta = delta * current.previous.timeScale
                current.previous.time += previousDelta
                current.mixTime += previousDelta

            next = current.next
            if next is not None:
                next.time = current.lastTime - next.delay
                if next.time >= 0:
                    self.setCurrent(i, next)
            else:
                if not current.loop and current.lastTime >= current.endTime:
                    self.clearTrack(i)

    def apply(self, skeleton):
        listenerCount = len(self.listeners)

        for i in range(len(self.tracks)):
            current = self.tracks.get(i)
            if current is None:
                continue

            self.events.size = 0
            time = current.time
            lastTime = current.lastTime
            endTime = current.endTime
            loop = current.loop
            if not loop and time > endTime:
                time = endTime

            previous = current.previous
            if previous is None:
                current.animation.mix(skeleton, lastTime, time, loop, self.events, current.mix)
            else:
                previousTime = previous.time
                if not previous.loop and previousTime > previous.endTime:
                    previousTime = previous.endTime
                previous.animation.apply(skeleton, previousTime, previousTime, previous.loop, None)

                alpha = current.mixTime / current.mixDuration * current.mix
                if alpha >= 1:
                    alpha = 1
                    self.trackEntryPool.free(previous)
                    current.previous = None
                current.animation.mix(skeleton, lastTime, time, loop, self.events, alpha)

            for ii in range(len(self.events)):
                event = self.events.get(ii)
                if current.listener is not None:
                    current.listener.event(i, event)
                for iii in range(listenerCount):
                    self.listeners.get(iii).event(i, event)

            if (lastTime % endTime > time % endTime) if loop else lastTime < endTime <= time:
                count = int(time / endTime)
                if current.listener is not None:
                    current.listener.complete(i, count)
                for ii in range(len(self.listeners)):
                    self.listeners.get(ii).complete(i, count)

            current.lastTime = current.time

    def clearTracks(self):
        for i in range(len(self.tracks)):
            self.clearTrack(i)
        self.tracks.clear()

    def clearTrack(self, trackIndex):
        if trackIndex >= len(self.tracks):
            return
        current = self.tracks.get(trackIndex)
        if current is None:
            return

        if current.listener is not None:
            current.listener.end(trackIndex)
        for i in range(len(self.listeners)):
            self.listeners.get(i).end(trackIndex)

        self.tracks.set(trackIndex, None)

        self.freeAll(current)
        if current.previous is not None:
            self.trackEntryPool.free(current.previous)

    def freeAll(self, entry):
        while entry is not None:
            next = entry.next
            self.trackEntryPool.free(entry)
            entry = next

    def expandToIndex(self, index):
        if index < len(self.tracks):
            return self.tracks.get(index)
        self.tracks.ensureCapacity(index - len(self.tracks) + 1)
        self.tracks.size = index + 1
        return None

    def setCurrent(self, index, entry):
        current = self.expandToIndex(index)
        if current is not None:
            previous = current.previous
            current.previous = None

            if current.listener is not None:
                current.listener.end(index)
            for i in range(len(self.listeners)):
                self.listeners.get(i).end(index)

            entry.mixDuration = self.data.getMix(current.animation, entry.animation)
            if entry.mixDuration > 0:
                entry.mixTime = 0
                if previous is not None and current.mixTime / current.mixDuration < 0.5:
                    entry.previous = previous
                    previous = current
                else:
                    entry.previous = current
            else:
                self.trackEntryPool.free(current)

            if previous is not None:
                self.trackEntryPool.free(previous)
        self.tracks.set(index, entry)

        if entry.listener is not None:
            entry.listener.start(index)
            for i in range(len(self.listeners)):
                self.listeners.get(i).start(index)

    def setAnimation(self, trackIndex, animationarg, loop):
        if isinstance(animationarg, str):
            animation = self.data.getSkeletonData().findAnimation(animationarg)
            if animation is None:
                raise Exception(f"Animation not found: {animationarg}")
        else:
            animation = animationarg

        current = self.expandToIndex(trackIndex)
        if current is not None:
            self.freeAll(current.next)

        entry = self.trackEntryPool.obtain()
        entry.animation = animation
        entry.loop = loop
        entry.endTime = animation.getDuration()
        self.setCurrent(trackIndex, entry)
        return entry

    def addAnimation(self, trackIndex, animationarg, loop, delay):
        if isinstance(animationarg, str):
            animation = self.data.getSkeletonData().findAnimation(animationarg)
            if animation is None:
                raise Exception(f"Animation not found: {animationarg}")
        else:
            animation = animationarg

        entry = self.trackEntryPool.obtain()
        entry.animation = animation
        entry.loop = loop
        entry.endTime = animation.getDuration()

        last = self.expandToIndex(trackIndex)
        if last is not None:
            while last.next is not None:
                last = last.next
            last.next = entry
        else:
            self.tracks.set(trackIndex, entry)

        if delay <= 0:
            if last != None:
                delay += last.endTime - self.data.getMix(last.animation, animation)
            else:
                delay = 0
        entry.delay = delay

        return entry

    def getCurrent(self, trackIndex):
        if trackIndex >= len(self.tracks):
            return None
        return self.tracks.get(trackIndex)

    def addListener(self, listener):
        if listener is None:
            raise Exception("listener cannot be None")
        self.listeners.add(listener)

    def removeListener(self, listener):
        self.listeners.removeValue(listener, True)

    def getTimeScale(self):
        return self.timeScale

    def setTimeScale(self, timeScale):
        self.timeScale = timeScale

    def getData(self):
        return self.data

    def getTracks(self):
        return self.tracks

    def __str__(self):
        buffer = ""
        for i in range(len(self.tracks)):
            entry = self.tracks.get(i)
            if entry is None:
                continue
            if len(buffer) > 0:
                buffer += ", "
            buffer += str(entry)
        if len(buffer) == 0:
            return "<None>"
        return buffer
