from kivy.graphics.texture import Texture
import os

from src.spine.skeleton.skeletonbinary import SkeletonBinary
from src.spine.skeleton.skeleton import Skeleton
from src.spine.utils.textureatlas import AtlasRegion
from src.spine.utils.filehandle import FileHandle
from src.spine.utils.textureatlas import TextureAtlasData, TextureAtlas


class SkeletonTextureAtlas(TextureAtlas):
    def __init__(self, fake_region, *args):
        super().__init__(*args)
        self.fake = fake_region

    def findRegion(self, name):
        region = super().findRegion(name)
        if region is None:
            region = self.fake
        return region


class SkeletonLoader:
    def load_skeleton(self, filename, reload, scale=1):
        if filename is None:
            return
        skeletonFile = FileHandle(filename)

        pixmap = Texture.create(size=(32, 32), colorfmt=u'rgba')
        buffer = u'\0xFF\0xFF\0xFF\0x54' * 32 * 32
        observe = lambda texture: texture.blit_buffer(bytes(buffer, encoding='utf-8'))
        pixmap.add_reload_observer(observe)
        observe(pixmap)
        fake = AtlasRegion(pixmap, 0, 0, 32, 32)

        atlasFileName = skeletonFile.pathWithoutExtension()
        if atlasFileName.endswith('.json'):
            atlasFileName = os.path.splitext(atlasFileName)[0]
        try:
            atlasFile = FileHandle(atlasFileName + '.atlas')
        except IOError:
            atlasFile = FileHandle(atlasFileName + '.atlas.txt')
        data = TextureAtlasData(atlasFile, atlasFile.parent(), False, TextureAtlas())
        atlas = SkeletonTextureAtlas(fake, data)

        # try:
        extension = skeletonFile.extension()
        if extension.lower() == 'json' or extension.lower() == 'txt':
            raise Exception("Json Not Implemented!")
            # json = SkeletonJson(atlas)
            # json.setScale(scale)
            # skeletonData = json.readSkeletonData(skeletonFile)
        else:
            binary = SkeletonBinary(atlas)
            binary.setScale(scale)
            skeletonData = binary.readSkeletonData(skeletonFile, False)
        # except Exception as e:
        #     print(f"Error loading Skeleton {skeletonFile.full_path()}: {e}")
        #     return

        skeleton = Skeleton(skeletonData)
        skeleton.setToSetupPose()
        skeleton.updateWorldTransform()
        return skeleton
