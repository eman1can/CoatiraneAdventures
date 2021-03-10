from kivy.properties import NumericProperty, ObjectProperty, StringProperty, DictProperty


class Key:

    def __init__(self):

        self.slotIndex = -1
        self.name = None

    def set(self, slotIndex, name):
        if name is None:
            raise Exception("IllegalArgumentException: name cannot be None")
        self.slotIndex = slotIndex
        self.name = name

    def __lt__(self, key):
        if self.slotIndex == key.slotIndex:
            return self.name < key.name
        return self.slotIndex < key.slotIndex

    def __gt__(self, key):
        if self.slotIndex == key.slotIndex:
            return self.name > key.name
        return self.slotIndex > key.slotIndex

    def __hash__(self):
        return hash((self.slotIndex, self.name))

    def __eq__(self, other):
        return (self.slotIndex, self.name) == (other.slotIndex, other.name)

    def __str__(self):
        return str(self.slotIndex) + ":" + self.name


class Skin:

    def __init__(self, name):

        self.lookup = Key()
        self.name = None
        self.attachments = {}

        super(Skin, self).__init__()
        if name is None:
            raise Exception("name cannot be None")
        self.name = name

    def addAttachment(self, slotIndex, name, attachment):
        if attachment is None:
            raise Exception("attachment cannot be None")
        if slotIndex < 0:
            raise Exception("slotIndex must be >= 0")
        key = Key()
        key.set(slotIndex, name)
        self.attachments[key] = attachment

    def getAttachment(self, slotIndex, name):
        if slotIndex < 0:
            raise Exception("slotIndex must be >= 0")
        self.lookup.set(slotIndex, name)
        try:
            return self.attachments[self.lookup]
        except KeyError:
            return None

    def findNamesForSlot(self, slotIndex, names):
        if names is None:
            raise Exception("names cannot be None")
        if slotIndex < 0:
            raise Exception("slotIndex must be >= 0")
        for key in self.attachments.keys():
            if key.slotIndex == slotIndex:
                names.append(key.name)

    def findAttachmentsForSlot(self, slotIndex, attachments):
        if attachments is None:
            raise Exception("attachments cannot be None")
        if slotIndex < 0:
            raise Exception("slotIndex must be >= 0")
        for key, attachment in self.attachments.items():
            if key.slotIndex == slotIndex:
                attachments.append(attachment)

    def clear(self):
        self.attachments.clear()

    def getName(self):
        return self.name

    def __str__(self):
        return self.name

    def attachAll(self, skeleton, oldSkin):
        for key, attachment in oldSkin.attachments.items():
            slot = skeleton.slots[key.slotIndex]
            if slot.attachment == attachment:
                attachment = self.getAttachment(key.slotIndex, key.name)
                if attachment is not None:
                    slot.setAttachment(attachment)
