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
        self.time_scale = 1
        self.mixTime = 0.0
        self.mixDuration = 0.0
        self.mix = 1

        self.handlers = {
            'end': {},
            'complete': {},
            'start': {},
            'event': {}
        }

        super().__init__()

    def reset(self):
        self.next = None
        self.previous = None
        self.animation = None

        self.time_scale = 1
        self.lastTime = -1
        self.time = 0

        self.handlers = {
            'end':      {},
            'complete': {},
            'start':    {},
            'event':    {}
        }

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

    def add_handler(self, type, key, handler):
        self.handlers[type][key] = handler

    def add_event_handler(self, event, key, handler):
        if event not in self.handlers['event']:
            self.handlers['event'][event] = {}
        self.handlers['event'][event][key] = handler

    def remove_handler(self, type, key):
        self.handlers[type].pop(key)

    def remove_event_handler(self, event, key):
        self.handlers['event'][event].pop(key)

    def getLastTime(self):
        return self.lastTime

    def setLastTime(self, lastTime):
        self.lastTime = lastTime

    def getMix(self):
        return self.mix

    def setMix(self, mix):
        self.mix = mix

    def get_time_scale(self):
        return self.time_scale

    def set_time_scale(self, new_time_scale):
        self.time_scale = new_time_scale

    def getNext(self):
        return self.next

    def setNext(self, next):
        self.next = next

    def isComplete(self):
        return self.time >= self.endTime

    def __str__(self):
        return "<none>" if self.animation is None else self.animation.name


class TrackEntryPool(Pool):
    def new_object(self):
        return TrackEntry()


class AnimationState:

    def __init__(self, data):

        self.data = None
        self.tracks = Array()
        self.events = Array()

        self.handlers = {
            'start': {},
            'end': {},
            'complete': {},
            'event': {}
        }

        self.time_scale = 1

        self.trackEntryPool = TrackEntryPool()

        if data is None:
            raise Exception("Data cannot be None")
        self.data = data

    def update(self, delta):
        delta *= self.time_scale
        for i in range(len(self.tracks)):
            current = self.tracks.get(i)
            if current is None:
                continue

            current.time += delta * current.time_scale
            if current.previous is not None:
                previousDelta = delta * current.previous.time_scale
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
            # print(self.events)
            for ii in range(len(self.events)):
                event = self.events.get(ii)
                # print('Event: ', event.getName())
                if event.getName() in self.handlers['event']:
                    dead_handlers = []
                    for handler_key, handler in self.handlers['event'][event.getName()].items():
                        if handler(i, event):
                            dead_handlers.append(handler_key)
                    for handler_key in dead_handlers:
                        self.handlers['event'][event.getName()].pop(handler_key)
                    del dead_handlers
                    if current is not None and event.getName() in current.handlers['event']:
                        dead_handlers = []
                        for handler_key, handler in current.handlers['event'][event.getName()].items():
                            if handler(i, event):
                                dead_handlers.append(handler_key)
                        for handler_key in dead_handlers:
                            self.handlers['event'][event.getName()].pop(handler_key)
                        del dead_handlers

            if (lastTime % endTime > time % endTime) if loop else lastTime < endTime <= time:
                count = int(time / endTime)
                for handler in self.handlers['complete'].values():
                    handler(i, count)
                if current is not None:
                    for handler in current.handlers['complete'].values():
                        handler(i, count)

            current.lastTime = current.time

    def clearTracks(self):
        for i in range(len(self.tracks)):
            self.clearTrack(i)
        self.tracks.clear()

    def clearTrack(self, track_index):
        if track_index >= len(self.tracks):
            return
        current = self.tracks.get(track_index)
        if current is None:
            return

        for handler in self.handlers['end'].values():
            handler(track_index)
        if current is not None:
            for handler in current.handlers['end'].values():
                handler(track_index)

        self.tracks.set(track_index, None)

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

            for handler in self.handlers['end'].values():
                handler(index)
            for handler in current.handlers['end'].values():
                handler(index)

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

        for handler in self.handlers['start'].values():
            handler(index)
        if current is not None:
            for handler in current.handlers['start'].values():
                handler(index)

    def getAnimationList(self):
        return self.data.getSkeletonData().getAnimationNames()

    def setAnimation(self, track_index, animationarg, loop):
        if isinstance(animationarg, str):
            animation = self.data.getSkeletonData().findAnimation(animationarg)
            if animation is None:
                raise Exception(f"Animation not found: {animationarg}")
        else:
            animation = animationarg

        current = self.expandToIndex(track_index)
        if current is not None:
            self.freeAll(current.next)

        entry = self.trackEntryPool.obtain()
        entry.animation = animation
        entry.loop = loop
        entry.endTime = animation.getDuration()
        self.setCurrent(track_index, entry)
        return entry

    def addAnimation(self, track_index, animationarg, loop, delay):
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

        last = self.expandToIndex(track_index)
        if last is not None:
            while last.next is not None:
                last = last.next
            last.next = entry
        else:
            self.tracks.set(track_index, entry)

        if delay <= 0:
            if last != None:
                delay += last.endTime - self.data.getMix(last.animation, animation)
            else:
                delay = 0
        entry.delay = delay

        return entry

    def getCurrent(self, track_index):
        if track_index >= len(self.tracks):
            return None
        return self.tracks.get(track_index)

    def add_handler(self, type, key, handler):
        self.handlers[type][key] = handler

    def add_event_handler(self, event, key, handler):
        if event not in self.handlers['event']:
            self.handlers['event'][event] = {}
        self.handlers['event'][event][key] = handler

    def remove_handler(self, type, key):
        self.handlers[type].pop(key)

    def remove_event_handler(self, event, key):
        self.handlers['event'][event].pop(key)

    def get_time_scale(self):
        return self.time_scale

    def set_time_scale(self, new_time_scale):
        self.time_scale = new_time_scale

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
