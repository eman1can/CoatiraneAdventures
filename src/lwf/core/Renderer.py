__all__ = ('Renderer', 'IRendererFactory', 'NullRendererFactory')


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


class TextRenderer(Renderer):
    def __init__(self, lwf):
        super().__init__(lwf)

    def set_text(self, text):
        pass

    def __str__(self):
        return f"TextRenderer <>"


class IRendererFactory:
    def construct_bitmap(self, lwf, obj_id, bitmap):
        pass

    def construct_bitmap_ex(self, lwf, obj_id, bitmap_ex):
        pass

    def construct_text(self, lwf, obj_id, text):
        pass

    def construct_particle(self, lwf, obj_id, particle):
        pass

    def init(self, lwf):
        pass

    def begin_render(self, lwf):
        pass

    def end_render(self, lwf):
        pass

    def destruct(self):
        pass

    def set_blend_mode(self, blend_mode):
        pass

    def set_mask_mode(self, mask_mode):
        pass

    def fit_for_height(self, lwf, w, h):
        pass

    def fit_for_width(self, lwf, w, h):
        pass

    def scale_for_height(self, lwf, w, h):
        pass

    def scale_for_width(self, lwf, w, h):
        pass

    def __str__(self):
        return f"I Renderer Factory <>"


class NullRendererFactory(IRendererFactory):
    def construct_bitmap(self, lwf, obj_id, bitmap):
        print("Make Bitmap → None")
        return None

    def construct_bitmap_ex(self, lwf, obj_id, bitmap_ex):
        print("Make BitmapEx → None")
        return None

    def construct_text(self, lwf, obj_id, text):
        print("Make Text → None")
        return None

    def construct_particle(self, lwf, obj_id, particle):
        print("Make Particle → None")
        return None

    def init(self, lwf):
        print('Init')

    def begin_render(self, lwf):
        print('Begin Render')

    def end_render(self, lwf):
        print('End Render')

    def destruct(self):
        print('Destruct')

    def set_blend_mode(self, blend_mode):
        print('Set blend Mode')

    def set_mask_mode(self, mask_mode):
        print('Set mask mode')

    def fit_for_height(self, lwf, w, h):
        pass

    def fit_for_width(self, lwf, w, h):
        pass

    def scale_for_height(self, lwf, w, h):
        pass

    def scale_for_width(self, lwf, w, h):
        pass

    def __str__(self):
        return f"Null Renderer Factory <>"
