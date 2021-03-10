from src.spine.attachment.attachmentloader import AttachmentLoader
from src.spine.attachment.regionattachment import RegionAttachment
from src.spine.attachment.meshattachment import MeshAttachment
from src.spine.attachment.skinnedmeshattachment import SkinnedMeshAttachment
from src.spine.attachment.boundingbox import BoundingBoxAttachment


class AtlasAttachmentLoader(AttachmentLoader):

    def __init__(self, atlas):

        self.atlas = None

        if atlas is None:
            raise Exception("atlas cannot be None")
        self.atlas = atlas

    def newRegionAttachment(self, skin, name, path):
        region = self.atlas.findRegion(path)
        if region is None:
            raise Exception(f"Region not found in atlas: {path} (region attachment: {name})")
        attachment = RegionAttachment(name)
        attachment.setRegion(region)
        return attachment

    def newMeshAttachment(self, skin, name, path):
        region = self.atlas.findRegion(path)
        if region is None:
            raise Exception(f"Region not found in atlas: {path} (mesh attachment: {name})")
        attachment = MeshAttachment(name)
        attachment.setRegion(region)
        return attachment

    def newSkinnedMeshAttachment(self, skin, name, path):
        region = self.atlas.findRegion(path)
        if region is None:
            raise Exception(f"Region not found in atlas: {path} (skinned mesh attachment: {name})")
        attachment = SkinnedMeshAttachment(name)
        attachment.setRegion(region)
        return attachment

    def newBoundingBoxAttachment(self, skin, name):
        return BoundingBoxAttachment(name)