from kivy.graphics import Mesh
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import BooleanProperty

# GL_ONE = 1
# GL_SRC_ALPHA = 770
# GL_ONE_MINUS_SRC_ALPHA = 7

from kivy.graphics.opengl import glBlendFunc, GL_ONE, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from src.spine.attachment.regionattachment import RegionAttachment
from src.spine.attachment.meshattachment import MeshAttachment
from src.spine.attachment.skinnedmeshattachment import SkinnedMeshAttachment
from src.spine.attachment.skeletonattachment import SkeletonAttachment


class SkeletonRenderer:
    def __init__(self):
        self.quadTriangles = [0, 1, 2, 2, 3, 0]
        self.empty = InstructionGroup()
        self.preMultipliedAlpha = False

    def setPremultipliedAlpha(self, premultipliedAlpha):
        self.preMultipliedAlpha = premultipliedAlpha

    def draw(self, canvas, skeleton):
        if skeleton.clear_color.a == 0:
            return
        canvas.add(skeleton.clear_color)
        # premultipliedAlpha = self.preMultipliedAlpha
        # srcFunc = GL_ONE if self.preMultipliedAlpha else GL_SRC_ALPHA
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        additive = False
        for slot in skeleton.drawOrder:
            attachment = slot.getAttachment()
            if attachment is None:
                continue

            if isinstance(attachment, SkeletonAttachment):
                print("WARNING")
                attachmentSkeleton = attachment.getSkeleton()
                if attachmentSkeleton is None:
                    continue
                bone = slot.getBone()
                rootBone = attachmentSkeleton.getRootBone()
                oldScaleX = rootBone.getScaleX()
                oldScaleY = rootBone.getScaleY()
                oldRotation = rootBone.getRotation()
                attachmentSkeleton.setPosition(skeleton.getX() + bone.getWorldX(), skeleton.getY() + bone.getWorldY())
                rootBone.setScaleX(1 + bone.getWorldScaleX() - oldScaleX)
                rootBone.setScaleY(1 + bone.getWorldScaleY() - oldScaleY)
                rootBone.setRotation(oldRotation + bone.getWorldRotation())
                attachmentSkeleton.updateWorldTransform()

                self.draw(canvas, attachmentSkeleton)

                attachmentSkeleton.setPosition(0, 0)
                rootBone.setScaleX(oldScaleX)
                rootBone.setScaleY(oldScaleY)
                rootBone.setRotation(oldRotation)
            else:
                attachment.updateWorldVertices(slot, self.preMultipliedAlpha)
                if not attachment.is_tex_set():
                    attachment.set_texture(attachment.getRegion().getTexture())
                canvas.add(attachment.getMesh())

        # # Add any missing mesh groups
        # for mesh in meshes:
        #     if mesh not in canvas.children:
        #         canvas.add(mesh)
        #
        # # Remove any extra mesh groups
        # for group in canvas.children:
        #     if group not in meshes:
        #         canvas.remove(group)
        #
        # # Sort the mesh groups according to drawOrder
        # for index, mesh in enumerate(meshes):
        #     group = canvas.children[index]
        #     if mesh != group:
        #         index_next = canvas.children.index(mesh)
        #         canvas.children[index_next] = group
        #         canvas.children[index] = mesh
