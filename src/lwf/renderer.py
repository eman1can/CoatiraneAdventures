__all__ = ('Renderer', 'TextRenderer', 'RendererFactory')

from kivy.cache import Cache
from kivy.graphics.opengl import GL_DST_ALPHA, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE_MINUS_DST_COLOR, GL_DST_COLOR, GL_ONE, GL_ZERO
from kivy.graphics.transformation import Matrix as KivyMatrix

from kivy.core.image import Image
from kivy.graphics import Color, MatrixInstruction, PopMatrix, PushMatrix, Scale, Translate
from kivy.graphics.vertex_instructions import Mesh


class Renderer:
    def __init__(self, lwf):
        self.lwf = lwf

    def destruct(self):
        pass

    def update(self, matrix, color_transform):
        pass

    def render(self, matrix, color_transform, rendering_index, rendering_count, visible):
        pass

    def __str__(self):
        return f"Renderer <>"


class BitmapRenderer(Renderer):
    def __init__(self, l, texture, vertices):
        super().__init__(l)

        self._factory = l.renderer_factory
        self._texture = texture
        self._vertices = vertices

    def render(self, matrix, color_transform, rendering_index, rendering_count, visible):
        if not visible:
            return

        bitmap = Mesh(vertices=self._vertices, indices=(1, 0, 2, 1, 2, 3), mode='triangle_fan', texture=self._texture)
        self._factory.render(bitmap, matrix, color_transform)


class TextRenderer(Renderer):
    def __init__(self, lwf):
        super().__init__(lwf)

    def set_text(self, text):
        pass

    def __str__(self):
        return f"TextRenderer <>"


class RendererFactory:
    def __init__(self, display, base_path, texture_handler):
        self._display = display
        self._base_path = base_path
        self._texture_handler = texture_handler

    def set_display(self, display):
        self._display = display

    def set_blend_mode(self, blend_mode):
        self._blend_mode = blend_mode

    def set_mask_mode(self, mask_mode):
        self._mask_mode = mask_mode

    def get_blend_mode(self):
        return self._blend_mode

    def load_texture(self, data, texture_id, lwf_name):
        t = data.textures[texture_id]
        path = self._base_path + '/' + t.filename
        if self._texture_handler is not None:
            return self._texture_handler(t.filename, lwf_name)
        return Image(path).texture

    def load_fragment(self, data, fragment_id, name):
        f = data.texture_fragments[fragment_id]
        texture = self.load_texture(data, f.texture_id, name)
        if 'eff' in f.filename:
            # We have premultiplied alpha

            print('Have pre?')

        return texture, f.vertices

    def construct_bitmap(self, lwf, obj_id, texture_fragment_id):
        if texture_fragment_id == -1:
            return
        texture, vertices = self.load_fragment(lwf.data, texture_fragment_id, lwf.custom_name)
        return BitmapRenderer(lwf, texture, vertices)

    def construct_bitmap_ex(self, lwf, obj_id, bitmap_ex):
        bitmap_renderer = BitmapRenderer(lwf, bitmap_ex, self._display)
        self._display.add_widget(bitmap_renderer)
        return bitmap_renderer

    def construct_particle(self, lwf, obj_id, particle):
        print('Particle unimplemented')

    def construct_text(self, lwf, obj_id, text):
        print('text unimplemented')

    def begin_render(self, lwf):
        self._display.canvas.add(PushMatrix())
        self._display.canvas.add(Translate(self._display.x, self._display.y, 0))

    def render(self, node, matrix, color_transform):
        self._display.canvas.add(PushMatrix())
        self._display.canvas.add(Color(*color_transform.c[:4]))
        matrix_instruction = MatrixInstruction()
        dmatrix = KivyMatrix()
        dmatrix.set(flat=[
            matrix.scale_x, -matrix.skew_1, 0, 0,
            matrix.skew_0, -matrix.scale_y, 0, 0,
            0, 0, 1, 0,
            matrix.translate_x, -matrix.translate_y, 0, 1])
        matrix_instruction.matrix = dmatrix
        self._display.canvas.add(matrix_instruction)
        self._display.canvas.add(node)
        self._display.canvas.add(Color(1, 1, 1, 1))
        self._display.canvas.add(PopMatrix())

    def end_render(self, lwf):
        self._display.canvas.add(PopMatrix())

    def destruct(self):
        pass

    def fit_for_height(self, lwf, w, h):
        self.scale_for_height(lwf, w, h)
        offset_x = (w - lwf.width * lwf.scale_by_stage) / 2.0
        offset_y = -h + (h - lwf.height * lwf.scale_by_stage) / 2.0
        lwf.property.move(offset_x, offset_y)

    def fit_for_width(self, lwf, w, h):
        self.scale_for_width(lwf, w, h)
        offset_x = (w - lwf.width * lwf.scale_by_stage) / 2.0
        offset_y = -h + (h - lwf.height * lwf.scale_by_stage) / 2.0
        lwf.property.move(offset_x, offset_y)

    def scale_for_height(self, lwf, w, h):
        scale = h / lwf.height
        lwf.scale_by_stage = scale
        lwf.property.scale(scale, scale)

    def scale_for_width(self, lwf, w, h):
        scale = w / lwf.width
        lwf.scale_by_stage = scale
        lwf.property.scale(scale, scale)
