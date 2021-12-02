class Key:

    def __init__(self):
        self.a1 = None
        self.a2 = None

    def __hash__(self):
        return 31 * (31 + hash(self.a1)) + hash(self.a2)

    def __eq__(self, other):
        return self.a1 == other.a1 and self.a2 == other.a2


class AnimationStateData:

    def __init__(self, skeletonData):

        self.skeletonData = None
        self.animationToMixTime = {}
        self.tempKey = Key()
        self.defaultMix = 0.0

        self.skeletonData = skeletonData

    def getSkeletonData(self):
        return self.skeletonData

    def getAnimations(self):
        return self.skeletonData.getAnimationNames()

    def setMix(self, fromarg, toarg, duration):
        if isinstance(fromarg, str):
            fromName, toName = fromarg, toarg
            afrom = self.skeletonData.findAnimation(fromName)
            if afrom is None:
                raise Exception(f"Animation not found: {toName}")
            ato = self.skeletonData.findAnimation(toName)
            if ato is None:
                raise Exception(f"Animation not found: {toName}")
        else:
            afrom, ato = fromarg, toarg
        if afrom is None:
            raise Exception("From cannot be None")
        if ato is None:
            raise Exception("To cannot be None")
        key = Key()
        key.a1 = afrom
        key.a2 = ato
        self.animationToMixTime[key] = duration

    def getMix(self, afrom, ato):
        self.tempKey.a1 = afrom
        self.tempKey.a2 = ato
        try:
            return self.animationToMixTime[self.tempKey]
        except KeyError:
            return self.defaultMix

    def getDefaultMix(self):
        return self.defaultMix

    def setDefaultMix(self, defaultMix):
        self.defaultMix = defaultMix
