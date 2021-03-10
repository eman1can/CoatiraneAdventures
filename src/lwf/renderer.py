from kivy.graphics.context_instructions import Scale, Translate, Color, MatrixInstruction, PushMatrix, PopMatrix
from kivy.graphics.transformation import Matrix
from kivy.graphics.vertex_instructions import Rectangle, Ellipse

from src.lwf.core.format.bitmap.ex import FormatBitmapEx
from src.lwf.core.data import Data
from src.lwf.core.renderer import IRendererFactory
from kivy.core.image import Image


class ResourceCache:
    m_instance = None

    @staticmethod
    def sharedLWFResourceCache():
        if not ResourceCache.m_instance:
            ResourceCache.m_instance = ResourceCache()
        return ResourceCache.m_instance

    def __init__(self):
        self.m_addColorShader = None
        self.m_addColorPAShader = None
        self.m_fontPathPrefix = "fonts/"
        self.m_particePathPrefix = "particles/"

    def loadLWFData(self, path):
        file = open(path, 'rb')
        if file is None:
            return None
        data = Data(file.read())
        if not data.check():
            return None
        return data


class KivyRenderer:
    def __init__(self, lwf, bitmap, canvas):
        b = lwf.data.bitmaps[bitmap.objectId]
        if b.textureFragmentId == -1:
            return

        bx = FormatBitmapEx()
        bx.matrixId = b.matrixId
        bx.textureFragmentId = b.textureFragmentId
        bx.u = 0
        bx.v = 0
        bx.w = 1
        bx.h = 1

        f = lwf.data.textureFragments[b.textureFragmentId]
        t = lwf.data.textures[f.textureId]

        texturePath = t.filename
        filename = lwf.data.path + texturePath

        rect_coords, tex_coords = self.get_vertices(t, f, bx, False, False)

        # print(f"Looking for {filename}")
        texture = Image(filename).texture
        # self.m_mesh = Rectangle(pos=(rect_coords[0], rect_coords[1]), size=(rect_coords[2], rect_coords[3]))
        self.m_origin_transform = Translate(lwf.render_offset[0] * (lwf.scaleX / lwf.width), lwf.render_offset[1] * (lwf.scaleY / lwf.height))
        self.m_mesh = Rectangle(pos=(rect_coords[0], rect_coords[1]), size=(rect_coords[2], rect_coords[3]), tex_coords=tex_coords, texture=texture)
        # self.m_mesh = Mesh(vertices=coordinates, indices=[1, 3, 2, 0, 1], mode='triangle_fan', texture=texture)
        self.m_color = Color(1, 1, 1, 1)
        self.m_matrix = Matrix()
        self.m_inst = MatrixInstruction()
        # self.m_mesh = Mesh(vertices=vertices, indices=[1, 3, 2, 0, 1], texture=texture, mode='triangle_fan')
        self.canvas = canvas

    def get_vertices(self, t, f, bx, flippedX, flippedY):
        tw = t.width
        th = t.height
        x = f.x
        y = f.y
        u = f.u
        v = f.v
        w = f.w
        h = f.h

        bu = bx.u * w
        bv = bx.v * h
        bw = bx.w
        bh = bx.h

        x += bu
        y += bv
        u += bu
        v += bv
        w *= bw
        h *= bh

        x0 = x / t.scale
        y0 = y / t.scale
        x1 = (x + w) / t.scale
        y1 = (y + h) / t.scale

        vertices = [x0, y0, x1 - x0, y1 - y0]

        if f.rotated == 0:
            u0 = u / tw
            v0 = v / th
            u1 = (u + w) / tw
            v1 = (v + h) / th
            if flippedX:
                tu1 = u1
                u1 = u0
                u0 = tu1
            if flippedY:
                tv1 = v1
                v1 = v0
                v0 = tv1
            # tex_coords = [u1, v1, u0, v1, u0, v0, u1, v0]

            tex_coords = [u0, v0, u1, v0, u1, v1, u0, v1]
            # coordinates = [x0, y0, u0, v0, x1, y0, u1, v0, x1, y1, u1, v1, x0, y1, u0, v1]

            # tex_coords = [u1, v1, u0, v1, u1, v0, u0, v0]
            # u1  v1  u0  v1  u1  v0  u0  v0
            # blu blv bru brv tlu tlv tru trv
            # u0  v0  u1  v0  u0  v1  u1  v1
            # tru trv tlu tlv bru brv blu blv
            # tex_coords = [u0, v0, u1, v0, u0, v1, u1, v1]
        else:
            u0 = u / tw
            v0 = v / th
            u1 = (u + h) / tw
            v1 = (v + w) / th

            tex_coords = [u0, v1, u0, v0, u1, v0, u1, v1]
            # coordinates = [x0, y0, u0, v1, x0, y1, u0, v0, x1, y1, u1, v0, x1, y1, u1, v0]

            # u0  v1  u0  v0  u1  v1  u1  v0
            # blu blv bru brv tlu tlv tru trv
            # u1  v0  u1  v1  u0  v0  u0  v1
            # tru trv tlu tlv bru brv blu blv
            # tex_coords = [u1, v0, u1, v1, u0, v0, u0, v1]
        return vertices, tex_coords

    def Destruct(self):
        pass

    def Update(self, matrix, colorTransform):
        print("Update")

    def Render(self, matrix, colorTransform, renderingIndex, renderingCount, visible):
        if not visible or colorTransform.multi.alpha == 0:
            return

        # print(matrix)
        # print("")

        self.m_color.rgba = (colorTransform.multi.red, colorTransform.multi.green, colorTransform.multi.blue, colorTransform.multi.alpha)
        self.m_matrix.set(flat=[matrix.scaleX, -matrix.skew0, 0, 0, # matrix.skew0, -matrix.skew0
                          -matrix.skew1, matrix.scaleY, 0, 0, # matrix.scaleX, matrix.scaleY
                          0, 0, 1, 0,
                          matrix.translateX, matrix.translateY, 0, 1])  # matrix.translateX, matrix.translateY
        self.m_inst.matrix = self.m_matrix

        self.canvas.add(PushMatrix())
        self.canvas.add(Color(1, 0, 0, 1))
        self.canvas.add(Translate(575, 300))
        self.canvas.add(Ellipse(size=(5, 5)))
        self.canvas.add(self.m_origin_transform)
        self.canvas.add(Ellipse(size=(5, 5)))
        self.canvas.add(Scale(1, -1, 1, origin=(0, 0)))
        self.canvas.add(self.m_inst)
        self.canvas.add(self.m_color)
        self.canvas.add(self.m_mesh)
        self.canvas.add(PopMatrix())
        self.canvas.ask_update()


class KivyFactory(IRendererFactory):
    def __init__(self, data, canvas):
        self.canvas = canvas
        # texture_files = {}
        # fragment_files = {}
        # self.bitmap_contexts = []

        # for texture in data.textures:
        #     path = data.path + texture.filename
        #     texture_file = Image(path).texture
        #     texture_files[texture] = texture_file
        #
        # for fragment in data.textureFragments:
        #     t = texture_files[data.textures[fragment.textureId]]
        #     tw = t.width
        #     th = t.height
        #
        #
        #
        #     # texture_file = texture_files[data.textures[fragment.textureId]]
        #     fragment_file = texture_file.get_region(fragment.x, fragment.y, fragment.x + fragment.w, fragment.y + fragment.h)
        #     fragment_files[fragment] = fragment_file
        #
        # for bitmap in data.bitmaps:
        #     bitmap.texture_fragment = fragment_files[data.textureFragments[bitmap.textureFragmentId]]
        #     self.bitmap_contexts.append(bitmap)

    def ConstructBitmap(self, lwf, objId, bitmap):
        # print("Make Bitmap → Texture Fragment")
        # bitmap = self.bitmap_contexts[bitmap.objectId]
        return KivyRenderer(lwf, bitmap, self.canvas)

    def ConstructBitmapEx(self, lwf, objId, bitmapEx):
        print("Make BitmapEx → None")
        return None

    def ConstructText(self, lwf, objId, text):
        print("Make Text → None")
        return None

    def ConstructParticle(self, lwf, objId, particle):
        print("Make Particle → None")
        return None

    def Init(self, lwf):
        pass

    def BeginRender(self, lwf):
        self.canvas.clear()

    def EndRender(self, lwf):
        pass

    def Destruct(self, lwf):
        pass