import json
import os
import sys

from spine import SkeletonData
from spine import BoneData
from spine import SlotData
from spine import Skin
from spine import AttachmentLoader

from spine import animation as Animation
from spine.Color import Color
from spine.blendmode import BlendMode
def readCurve(timeline, keyframeIndex, valueMap):
    try:
        curve = valueMap['curve']
    except KeyError:
        return timeline

    if curve == 'stepped':
        timeline.setStepped(keyframeIndex)
    else:
        timeline.setCurve(keyframeIndex,
                          float(curve[0]),
                          float(curve[1]),
                          float(curve[2]),
                          float(curve[3]))
    return timeline


class SkeletonJson(object):
    def __init__(self, attachmentLoader):
        super(SkeletonJson, self).__init__()
        self.attachmentLoader = attachmentLoader
        self.scale = 1.0
        self.flipY = False

    def readSkeletonDataFile(self, file, path=None):
        if path:
           file = '{path}/{file}'.format(path=path, file=file)

        file = os.path.realpath(file)

        jasonPayload = None

        with open(file, 'r') as jsonFile:
            jsonPayload = ''.join(jsonFile.readlines())

        return self.readSkeletonData(jsonPayload=jsonPayload)


    def readSkeletonData(self, jsonPayload):
        try:
            root = json.loads(jsonPayload)
        except ValueError:
            if os.path.isfile(jsonPayload):
                print('The API has changed.  You need to load skeleton data with readSkeletonDataFile(), not readSkeletonData()')
                sys.exit()
        skeletonData = SkeletonData.SkeletonData()

        #skeleton
        skeletonMap = root.get('skeleton')
        if skeletonMap is not None:
            print("Skeleton:")
            skeletonData.setHash(skeletonMap.get('hash', None))
            print("\tHash: ", skeletonData.getHash())
            skeletonData.setVersion(skeletonMap.get('spine', None))
            print("\tVersion: ", skeletonData.getVersion())
            skeletonData.setWidth(skeletonMap.get('width', 0.0))
            print("\tWidth: ", str(skeletonData.getWidth()))
            skeletonData.setHeight(skeletonMap.get('height', 0.0))
            print("\tHeight: ", str(skeletonData.getHeight()))
            skeletonData.setImagesPath(skeletonMap.get('images', None))
            print("\tImages Path: ", skeletonData.getImagesPath())

        for boneMap in root.get('bones', []):
            boneData = BoneData.BoneData(name=boneMap['name'], parent=None)
            print("Bone:\n\tName: ", boneData.getName())
            if 'parent' in boneMap:
                boneData.setParent(skeletonData.findBone(boneMap['parent']))
                if not boneData.getParent():
                    raise Exception('Parent bone not found: ' % boneMap['name'])
                print("\tparent: ", boneData.getParent().getName())

            boneData.setLength(float(boneMap.get('length', 0.0)) * self.scale)
            print("\tLength: ", boneData.getLength())
            boneData.setX(float(boneMap.get('x', 0.0)) * self.scale)
            print("\tX: ", boneData.getX())
            boneData.setY(float(boneMap.get('y', 0.0)) * self.scale)
            print("\tY: ", boneData.getY())
            boneData.setRotation(float(boneMap.get('rotation', 0.0)))
            print("\tRotation: ", boneData.getRotation())
            boneData.setScaleX(float(boneMap.get('scaleX', 1.0)))
            print("\tScaleX: ", boneData.getScaleX())
            boneData.setScaleY(float(boneMap.get('scaleY', 1.0)))
            print("\tScaleY: ", boneData.getScaleY())
            boneData.setFlipX(bool(boneMap.get('flipX', False)))
            print("\tFlipX: ", boneData.getFlipX())
            boneData.setFlipY(bool(boneMap.get('flipY', False)))
            print("\tFlipY: ", boneData.getFlipY())
            boneData.setInheritScale(bool(boneMap.get('inheritScale', True)))
            print("\tInheritScale: ", boneData.getInheritScale())
            boneData.setInheritRotation(bool(boneMap.get('inheritRotation', True)))
            print("\tInheritRotation: ", boneData.getInheritRotation())
            if 'color' in boneMap:
                color = boneMap['color']
                boneData.getColor().set(Color.valueOf(str(color)))
                print("\tColor: ", boneData.getColor().toString())
            skeletonData.bones.append(boneData)

        for slotMap in root.get('slots', []):
            slotName = slotMap['name']
            boneName = slotMap['bone']
            boneData = skeletonData.findBone(boneName)

            if not BoneData:
                raise Exception('Slot bone not found: ', boneName)
            slotData = SlotData.SlotData(name=slotName, boneData=boneData)
            print("Slot:\n\tName: ", slotData.getName(), "\n\tBone: ", slotData.getBoneData().getName())
            if 'color' in slotMap:
                s = slotMap['color']
                slotData.getColor().setFromString(slotMap['color'])
                print("\tColor: " + slotData.getColor().toString())

            if 'attachment' in slotMap:
                slotData.setAttachmentName(slotMap['attachment'])
                print("\tAttachment: " + slotData.getAttachmentName())

            if 'blend' in slotMap:
                slotData.setBlendMode(BlendMode.valueOf(slotMap['blend']))
                print("\tBlend Mode: " + slotData.getBlendMode().toString())

            skeletonData.slots.append(slotData)

        skinsMap = root.get('skins', {})
        for skinName in skinsMap.keys():
            skin = Skin.Skin(skinName)
            skeletonData.skins.append(skin)
            if skinName == 'default':
                skeletonData.defaultSkin = skin

            slotMap = skinsMap[skinName]
            for slotName in slotMap.keys():
                slotIndex = skeletonData.findSlotIndex(slotName)
                if slotIndex is -1:
                    raise Exception("Slot not found!")
                attachmentsMap = slotMap[slotName]
                for attachmentName in attachmentsMap.keys():
                    attachmentMap = attachmentsMap[attachmentName]
                    scale = self.scale
                    type = None
                    name = attachmentMap.get('name', attachmentName)
                    path = attachmentMap.get('path', name)
                    typeString = attachmentMap.get('type', 'region')
                    if typeString == 'region':
                        print("region")
                        type = AttachmentLoader.AttachmentType.region
                        # region = self.attachmentLoader.newAttachment(type, attachmentMap.get('name', attachmentName))
                    elif typeString == 'boundingbox':
                        print("boundingbox")
                        type = AttachmentLoader.AttachmentType.boundingBox
                    elif typeString == 'mesh':
                        print("mesh")
                        type = AttachmentLoader.AttachmentType.mesh
                    elif typeString == 'skinnedmesh':
                        print("skinnedmesh")
                        type = AttachmentLoader.AttachmentType.skinnedMesh
                    # typeString = attachmentMap.get('type', 'region')
                    # #update to different attachment methods
                    # if typeString == 'region':
                    #     type = AttachmentLoader.AttachmentType.region
                    # elif typeString == 'regionSequence':
                    #     type = AttachmentLoader.AttachmentType.regionSequence
                    # else:
                    #     raise Exception('Unknown attachment type: %s (%s)' % (attachment['type'],
                    #                                                               attachmentName))
                    #
                    attachment = self.attachmentLoader.newAttachment(type, attachmentMap.get('name', attachmentName))
                    #
                    if type == AttachmentLoader.AttachmentType.region:
                        regionAttachment = attachment
                        regionAttachment.name = attachmentName
                        regionAttachment.x = float(attachmentMap.get('x', 0.0)) * self.scale
                        regionAttachment.y = float(attachmentMap.get('y', 0.0)) * self.scale
                        regionAttachment.scaleX = float(attachmentMap.get('scaleX', 1.0))
                        regionAttachment.scaleY = float(attachmentMap.get('scaleY', 1.0))
                        regionAttachment.rotation = float(attachmentMap.get('rotation', 0.0))
                        regionAttachment.width = float(attachmentMap.get('width', 32)) * self.scale
                        regionAttachment.height = float(attachmentMap.get('height', 32)) * self.scale
                    skin.addAttachment(slotIndex, attachmentName, attachment)

        animations = root.get('animations', {})
        for animationName in animations:
            animationMap = animations.get(animationName, {})
            animationData = self.readAnimation(name=animationName,
                                               root=animationMap,
                                               skeletonData=skeletonData)
            skeletonData.animations.append(animationData)

        return skeletonData


    def readAnimation(self, name, root, skeletonData):
        if not skeletonData:
            raise Exception('skeletonData cannot be null.')

        timelines =  []
        scale = self.scale
        duration = 0.0

        bones = root.get('bones', {})

        for boneName in bones.keys():
            boneIndex = skeletonData.findBoneIndex(boneName)
            if boneIndex == -1:
                raise Exception('Bone not found: %s' % boneName)

            timelineMap = bones[boneName]

            for timelineName in timelineMap.keys():
                values = timelineMap[timelineName]

                if timelineName == 'rotate':
                    timeline = Animation.Timeline.RotateTimeline(len(values))
                    timeline.boneIndex = boneIndex

                    keyframeIndex = 0
                    for valueMap in values:
                        time = valueMap['time']
                        timeline.setKeyframe(keyframeIndex, time, valueMap['angle'])
                        timeline = readCurve(timeline, keyframeIndex, valueMap)
                        keyframeIndex += 1
                    timelines.append(timeline)
                    if timeline.getDuration() > duration:
                        duration = timeline.getDuration()
                elif timelineName == 'translate' or timelineName == 'scale':
                    timeline = None
                    timelineScale = 1.0
                    if timelineName == 'scale':
                        timeline = Animation.Timeline.ScaleTimeline(len(values))
                    else:
                        timeline = Animation.Timeline.TranslateTimeline(len(values))
                        timelineScale = scale
                    timeline.boneIndex = boneIndex

                    keyframeIndex = 0
                    for valueMap in values:
                        time = valueMap['time']
                        timeline.setKeyframe(keyframeIndex,
                                             time,
                                             valueMap.get('x', 0.0) * timelineScale,
                                             valueMap.get('y', 0.0) * timelineScale)
                        timeline = readCurve(timeline, keyframeIndex, valueMap)
                        keyframeIndex += 1
                    timelines.append(timeline)
                    if timeline.getDuration() > duration:
                        duration = timeline.getDuration()
                elif timlineName == 'flipX' or timelineName == 'flipY':
                    timeline = None
                    x = bool(timelineName == 'flipX')
                    if x:
                        timeline = Animation.Timeline.FlipXTimeline(len(values))
                    else:
                        timeilne = Animation.Timelilne.FLipYTimeline(len(values))
                    timeline.boneIndex = boneIndex

                    keyframeIndex = 0
                    for valuemap in values:
                        time = valueMap['time']
                        timeline.setKeyframe(keyframeIndex, time, valueMap.get('flip', False))
                        keyframeIndex += 1
                    timeline.append(timeline)
                    if timeline.getDuration() > duration:
                        duration = timeline.getDuration()
                else:
                    raise Exception('Invalid timeline type for a bone: %s (%s)' % (timelineName, boneName))


        slots = root.get('slots', {})

        for slotName in slots.keys():
            slotIndex = skeletonData.findSlotIndex(slotName)
            if slotIndex == -1:
                raise Exception('Slot not found: ', slotName)

            timelineMap = slots[slotName]
            for timelineName in timelineMap.keys():
                values = timelineMap[timelineName]
                if timelineName == 'color':
                    timeline = Animation.Timeline.ColorTimeline(len(values))
                    timeline.slotIndex = slotIndex

                    keyframeIndex = 0
                    for valueMap in values:
                        timeline.setKeyframe(keyframeIndex,
                                             valueMap['time'],
                                             int(valueMap['color'][0:2], 16),
                                             int(valueMap['color'][2:4], 16),
                                             int(valueMap['color'][4:6], 16),
                                             int(valueMap['color'][6:8], 16))
                        timeline = readCurve(timeline, keyframeIndex, valueMap)
                        keyframeIndex += 1
                    timelines.append(timeline)
                    if timeline.getDuration() > duration:
                        duration = timeline.getDuration()

                elif timelineName == 'attachment':
                    timeline = Animation.Timeline.AttachmentTimeline(len(values))
                    timeline.slotIndex = slotIndex

                    keyframeIndex = 0
                    for valueMap in values:
                        valueName = valueMap['name']
                        timeline.setKeyframe(keyframeIndex, valueMap['time'], '' if not valueName else valueName)
                        keyframeIndex += 1
                    timelines.append(timeline)
                    if timeline.getDuration() > duration:
                        duration = timeline.getDuration()
                else:
                    raise Exception('Invalid timeline type for a slot: %s (%s)' % (timelineName, slotName))

        # Add Skin, Ik, Event, DrawOrder Timelines

        animation = Animation.Animation(name, timelines, duration)
        return animation



# import json
# import os
# import sys
#
# from spine import SkeletonData
# from spine import BoneData
# from spine import SlotData
# from spine import Skin
# from spine import AttachmentLoader
#
# from spine import animation as Animation
# from spine.Color import Color
# from spine.blendmode import BlendMode
#
#
# def readCurve(timeline, keyframeIndex, valueMap):
#     try:
#         curve = valueMap['curve']
#     except KeyError:
#         return timeline
#
#     if curve == 'stepped':
#         timeline.setStepped(keyframeIndex)
#     else:
#         timeline.setCurve(keyframeIndex,
#                           float(curve[0]),
#                           float(curve[1]),
#                           float(curve[2]),
#                           float(curve[3]))
#     return timeline
#
#
# class SkeletonJson(object):
#     def __init__(self, attachmentLoader):
#         super(SkeletonJson, self).__init__()
#         self.attachmentLoader = attachmentLoader
#         self.scale = 1.0
#         self.flipY = False
#
#     def readSkeletonDataFile(self, file, path=None):
#         if path:
#             file = '{path}/{file}'.format(path=path, file=file)
#
#         file = os.path.realpath(file)
#
#         jasonPayload = None
#
#         with open(file, 'r') as jsonFile:
#             jsonPayload = ''.join(jsonFile.readlines())
#
#         return self.readSkeletonData(jsonPayload=jsonPayload)
#
#     def readSkeletonData(self, jsonPayload):
#         try:
#             root = json.loads(jsonPayload)
#         except ValueError:
#             if os.path.isfile(jsonPayload):
#                 print(
#                     'The API has changed.  You need to load skeleton data with readSkeletonDataFile(), not readSkeletonData()')
#                 sys.exit()
#
#         skeletonData = SkeletonData.SkeletonData()
#
#         for boneMap in root.get('bones', []):
#             boneData = BoneData.BoneData(name=boneMap['name'], parent=None)
#
#             if 'parent' in boneMap:
#                 boneData.parent = skeletonData.findBone(boneMap['parent'])
#                 if not boneData.parent:
#                     raise Exception('Parent bone not found: %s' % boneMap['name'])
#
#             boneData.length = float(boneMap.get('length', 0.0)) * self.scale
#             boneData.x = float(boneMap.get('x', 0.0)) * self.scale
#             boneData.y = float(boneMap.get('y', 0.0)) * self.scale
#             boneData.rotation = float(boneMap.get('rotation', 0.0))
#             boneData.scaleX = float(boneMap.get('scaleX', 1.0))
#             boneData.scaleY = float(boneMap.get('scaleY', 1.0))
#             skeletonData.bones.append(boneData)
#
#         for slotMap in root.get('slots', []):
#             slotName = slotMap['name']
#             boneName = slotMap['bone']
#             boneData = skeletonData.findBone(boneName)
#
#             if not BoneData:
#                 raise Exception('Slot bone not found: %s' % boneName)
#             slotData = SlotData.SlotData(name=slotName, boneData=boneData)
#
#             if 'color' in slotMap:
#                 s = slotMap['color']
#                 slotData.r = int(slotMap['color'][0:2], 16)
#                 slotData.g = int(slotMap['color'][2:4], 16)
#                 slotData.b = int(slotMap['color'][4:6], 16)
#                 slotData.a = int(slotMap['color'][6:8], 16)
#
#             if 'attachment' in slotMap:
#                 slotData.attachmentName = slotMap['attachment']
#
#             skeletonData.slots.append(slotData)
#
#         skinsMap = root.get('skins', {})
#         for skinName in skinsMap.keys():
#             skin = Skin.Skin(skinName)
#             skeletonData.skins.append(skin)
#             if skinName == 'default':
#                 skeletonData.defaultSkin = skin
#
#             slotMap = skinsMap[skinName]
#             for slotName in slotMap.keys():
#                 slotIndex = skeletonData.findSlotIndex(slotName)
#
#                 attachmentsMap = slotMap[slotName]
#                 for attachmentName in attachmentsMap.keys():
#                     attachmentMap = attachmentsMap[attachmentName]
#
#                     type = None
#
#                     typeString = attachmentMap.get('type', 'region')
#
#                     if typeString == 'region':
#                         type = AttachmentLoader.AttachmentType.region
#                     elif typeString == 'regionSequence':
#                         type = AttachmentLoader.AttachmentType.regionSequence
#                     else:
#                         raise Exception('Unknown attachment type: %s (%s)' % (attachment['type'],
#                                                                               attachmentName))
#
#                     attachment = self.attachmentLoader.newAttachment(type,
#                                                                      attachmentMap.get('name', attachmentName))
#
#                     if type == AttachmentLoader.AttachmentType.region or type == AttachmentLoader.AttachmentType.regionSequence:
#                         regionAttachment = attachment
#                         regionAttachment.name = attachmentName
#                         regionAttachment.x = float(attachmentMap.get('x', 0.0)) * self.scale
#                         regionAttachment.y = float(attachmentMap.get('y', 0.0)) * self.scale
#                         regionAttachment.scaleX = float(attachmentMap.get('scaleX', 1.0))
#                         regionAttachment.scaleY = float(attachmentMap.get('scaleY', 1.0))
#                         regionAttachment.rotation = float(attachmentMap.get('rotation', 0.0))
#                         regionAttachment.width = float(attachmentMap.get('width', 32)) * self.scale
#                         regionAttachment.height = float(attachmentMap.get('height', 32)) * self.scale
#                     skin.addAttachment(slotIndex, attachmentName, attachment)
#
#         animations = root.get('animations', {})
#         for animationName in animations:
#             animationMap = animations.get(animationName, {})
#             animationData = self.readAnimation(name=animationName,
#                                                root=animationMap,
#                                                skeletonData=skeletonData)
#             skeletonData.animations.append(animationData)
#
#         return skeletonData
#
#     def readAnimation(self, name, root, skeletonData):
#         if not skeletonData:
#             raise Exception('skeletonData cannot be null.')
#
#         timelines = []
#         duration = 0.0
#
#         bones = root.get('bones', {})
#
#         for boneName in bones.keys():
#             boneIndex = skeletonData.findBoneIndex(boneName)
#             if boneIndex == -1:
#                 raise Exception('Bone not found: %s' % boneName)
#
#             timelineMap = bones[boneName]
#
#             for timelineName in timelineMap.keys():
#                 values = timelineMap[timelineName]
#
#                 if timelineName == 'rotate':
#                     timeline = Animation.Timeline.RotateTimeline(len(values))
#                     timeline.boneIndex = boneIndex
#
#                     keyframeIndex = 0
#                     for valueMap in values:
#                         time = valueMap['time']
#                         timeline.setKeyframe(keyframeIndex, time, valueMap['angle'])
#                         timeline = readCurve(timeline, keyframeIndex, valueMap)
#                         keyframeIndex += 1
#                     timelines.append(timeline)
#                     if timeline.getDuration() > duration:
#                         duration = timeline.getDuration()
#                 elif timelineName == 'translate' or timelineName == 'scale':
#                     timeline = None
#                     timelineScale = 1.0
#                     if timelineName == 'scale':
#                         timeline = Animation.Timeline.ScaleTimeline(len(values))
#                     else:
#                         timeline = Animation.Timeline.TranslateTimeline(len(values))
#                         timelineScale = self.scale
#                     timeline.boneIndex = boneIndex
#
#                     keyframeIndex = 0
#                     for valueMap in values:
#                         time = valueMap['time']
#                         timeline.setKeyframe(keyframeIndex,
#                                              valueMap['time'],
#                                              valueMap.get('x', 0.0),
#                                              valueMap.get('y', 0.0))
#                         timeline = readCurve(timeline, keyframeIndex, valueMap)
#                         keyframeIndex += 1
#                     timelines.append(timeline)
#                     if timeline.getDuration() > duration:
#                         duration = timeline.getDuration()
#                 else:
#                     raise Exception('Invalid timeline type for a bone: %s (%s)' % (timelineName, boneName))
#
#         slots = root.get('slots', {})
#
#         for slotName in slots.keys():
#             slotIndex = skeletonData.findSlotIndex(slotName)
#             if slotIndex == -1:
#                 raise Exception('Slot not found: %s' % slotName)
#
#             timelineMap = slots[slotName]
#             for timelineName in timelineMap.keys():
#                 values = timelineMap[timelineName]
#                 if timelineName == 'color':
#                     timeline = Animation.Timeline.ColorTimeline(len(values))
#                     timeline.slotIndex = slotIndex
#
#                     keyframeIndex = 0
#                     for valueMap in values:
#                         timeline.setKeyframe(keyframeIndex,
#                                              valueMap['time'],
#                                              int(valueMap['color'][0:2], 16),
#                                              int(valueMap['color'][2:4], 16),
#                                              int(valueMap['color'][4:6], 16),
#                                              int(valueMap['color'][6:8], 16))
#                         timeline = readCurve(timeline, keyframeIndex, valueMap)
#                         keyframeIndex += 1
#                     timelines.append(timeline)
#                     if timeline.getDuration() > duration:
#                         duration = timeline.getDuration()
#
#                 elif timelineName == 'attachment':
#                     timeline = Animation.Timeline.AttachmentTimeline(len(values))
#                     timeline.slotIndex = slotIndex
#
#                     keyframeIndex = 0
#                     for valueMap in values:
#                         valueName = valueMap['name']
#                         timeline.setKeyframe(keyframeIndex, valueMap['time'], '' if not valueName else valueName)
#                         keyframeIndex += 1
#                     timelines.append(timeline)
#                     if timeline.getDuration() > duration:
#                         duration = timeline.getDuration()
#                 else:
#                     raise Exception('Invalid timeline type for a slot: %s (%s)' % (timelineName, slotName))
#
#         animation = Animation.Animation(name, timelines, duration)
#         return animation