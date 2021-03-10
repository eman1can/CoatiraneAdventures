from math import radians

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager
from kivy.graphics.transformation import Matrix
from kivy.properties import StringProperty, ObjectProperty, ReferenceListProperty, NumericProperty, ListProperty
from kivy.uix.scatterlayout import ScatterLayout
from kivy.vector import Vector
from kivy.uix.popup import Popup

from PIL import Image as PILImage

import os


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(ScreenManager):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    filename = StringProperty(None)

    def __init__(self, **kwargs):
        self._popup = None
        super().__init__(**kwargs)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.filename = os.path.join(path, filename[0])
        self.dismiss_popup()
        self.current = 'confirm_page'

    def goto_first_crop(self):
        self.ids.first_crop_scatter.source = self.filename
        self.current = 'first_crop'

    def goto_second_crop(self):
        self.ids.second_crop_scatter.source = self.filename
        self.current = 'second_crop'

    def goto_confirm(self):
        cw, ch, cx, cy = self.ids.first_crop_scatter.get_image_crop()
        self.ids.slide_image.set_crop(cw, ch, cx, cy)

        cw, ch, cx, cy = self.ids.second_crop_scatter.get_image_crop()
        self.ids.preview_image.set_crop(cw, ch, cx, cy)
        self.current = 'confirm_crop_page'

    def save_crops(self):
        # Load image with PIL
        full_image = PILImage.open(self.filename)
        # Get the image name
        name_raw = self.ids.character_name.text
        name = name_raw.lower().replace(' ', '_')

        # Get image type
        if self.filename[-3:] == 'jpg':
            type = 'jpeg'
        else:
            type = 'png'

        # Save full image to output
        full_image.save('output/' + name + '_full.png', type)

        # Crop the image to the slide
        cw, ch, cx, cy = self.ids.first_crop_scatter.get_image_crop()
        slide_image = full_image.crop((cx - cw / 2, cy - ch / 2, cx - cw / 2 + cw, cy - ch / 2 + ch))
        slide_image.save('output/' + name + '_slide.png', type)

        # crop the image to the preview
        cw, ch, cx, cy = self.ids.second_crop_scatter.get_image_crop()
        preview_image = full_image.crop((cx - cw / 2, cy - ch / 2, cx - cw / 2 + cw, cy - ch / 2 + ch))
        preview_image.save('output/' + name + '_preview.png', type)

        self.ids.character_name.text = ''
        self.ids.first_crop_scatter.scale = 1


class CropScatter(ScatterLayout):
    image_width = NumericProperty(1)
    image_height = NumericProperty(1)
    image_size = ReferenceListProperty(image_width, image_height)
    image_x = NumericProperty(0)
    image_y = NumericProperty(0)
    image_pos = ReferenceListProperty(image_x, image_y)

    crop_width = NumericProperty(0)
    crop_height = NumericProperty(0)
    crop_size = ReferenceListProperty(crop_width, crop_height)
    crop_x = NumericProperty(0)
    crop_y = NumericProperty(0)
    crop_pos = ReferenceListProperty(crop_x, crop_y)
    frame_width = NumericProperty(0)
    frame_height = NumericProperty(0)
    frame_size = ReferenceListProperty(frame_width, frame_height)

    texture = ObjectProperty(None)

    source = StringProperty(None)

    def transform_with_touch(self, touch):
        # just do a simple one finger drag
        changed = False
        if len(self._touches) == self.translation_touches:
            # _last_touch_pos has last pos in correct parent space,
            # just like incoming touch
            dx = (touch.x - self._last_touch_pos[touch][0]) \
                * self.do_translation_x
            dy = (touch.y - self._last_touch_pos[touch][1]) \
                * self.do_translation_y
            dx = dx / self.translation_touches
            dy = dy / self.translation_touches
            self.apply_image_transform(x=dx, y=dy)
            changed = True

        if len(self._touches) == 1:
            return changed

        # we have more than one touch... list of last known pos
        points = [Vector(self._last_touch_pos[t]) for t in self._touches
                  if t is not touch]
        # add current touch last
        points.append(Vector(touch.pos))

        # we only want to transform if the touch is part of the two touches
        # farthest apart! So first we find anchor, the point to transform
        # around as another touch farthest away from current touch's pos
        anchor = max(points[:-1], key=lambda p: p.distance(touch.pos))

        # now we find the touch farthest away from anchor, if its not the
        # same as touch. Touch is not one of the two touches used to transform
        farthest = max(points, key=anchor.distance)
        if farthest is not points[-1]:
            return changed

        # ok, so we have touch, and anchor, so we can actually compute the
        # transformation
        old_line = Vector(*touch.ppos) - anchor
        new_line = Vector(*touch.pos) - anchor
        if not old_line.length():   # div by zero
            return changed

        angle = radians(new_line.angle(old_line)) * self.do_rotation
        if angle:
            changed = True
        # self.apply_image_transform(Matrix().rotate(angle, 0, 0, 1), anchor=anchor)

        if self.do_scale:
            scale = new_line.length() / old_line.length()
            new_scale = scale * self.scale
            if new_scale < self.scale_min:
                scale = self.scale_min / self.scale
            elif new_scale > self.scale_max:
                scale = self.scale_max / self.scale
            self.apply_image_transform(scale=scale, anchor=anchor)
            changed = True
        return changed

    def apply_image_transform(self, x=0, y=0, scale=1, post_multiply=False, anchor=(0, 0)):

        # Test if the x move is valid
        # t = Matrix().translate(anchor[0], anchor[1], 0)
        t = Matrix()
        t = t.translate(x, 0, 0)
        # t = t.multiply(Matrix().translate(-anchor[0], -anchor[1], 0))

        if not self.test_valid(t.multiply(self.transform)):
            x = 0

        # Test if the y move is valid
        # t = Matrix().translate(anchor[0], anchor[1], 0)
        t = Matrix()
        t = t.translate(0, y, 0)
        # t = t.multiply(Matrix().translate(-anchor[0], -anchor[1], 0))

        if not self.test_valid(t.multiply(self.transform)):
            y = 0

        # Test if the scale is valid
        # t = Matrix()
        # t = t.translate(x, y, 0)
        t = Matrix().translate(anchor[0], anchor[1], 0)
        t = t.scale(scale, scale, scale)
        t = t.multiply(Matrix().translate(-anchor[0], -anchor[1], 0))

        if not self.test_valid(t.multiply(self.transform)):
            scale = 1

        # Compile final matrix
        t = Matrix().translate(anchor[0], anchor[1], 0)
        t = t.translate(x, y, 0)
        t = t.scale(scale, scale, scale)
        t = t.multiply(Matrix().translate(-anchor[0], -anchor[1], 0))

        if post_multiply:
            self.transform = self.transform.multiply(t)
        else:
            self.transform = t.multiply(self.transform)

    def test_valid(self, matrix):
        crop_x, crop_y = (self.width - self.crop_width) / 2, (self.height - self.crop_height) / 2
        x, y, z = matrix.transform_point(self.image_x, self.image_y, 0)
        mx, my, mz = matrix.transform_point(self.image_x + self.image_width, self.image_y + self.image_height, 0)

        if x > crop_x:
            return False
        if y > crop_y:
            return False
        if mx < crop_x + self.crop_width:
            return False
        if my < crop_y + self.crop_height:
            return False
        return True

    def on_texture(self, instance, value):
        self.calculate()

    def on_size(self, *args):
        self.calculate()

    def calculate(self):
        if 'image' not in self.ids or self.ids.image.texture is None:
            return
        width, height = self.ids.image.texture.size
        frame_width, frame_height = self.width, self.height
        if width > height:
            self.image_width = frame_width
            self.image_height = height / width * frame_width
            self.frame_size = frame_width, frame_width
            self.image_y = (self.height - self.image_height) / 2
            self.crop_size = self.image_height, self.image_height
        else:
            self.image_height = frame_height
            self.image_width = width / height * frame_height
            self.frame_size = frame_height, frame_height
            self.image_x = (self.width - self.image_width) / 2
            self.crop_size = self.image_width, self.image_width


    def get_image_crop(self):
        x, y, z = self.transform.transform_point(self.image_x, self.image_y, 0)
        mx, my, mz = self.transform.transform_point(self.image_x + self.image_width, self.image_y + self.image_height, 0)
        ccenx, cceny = (self.width - self.crop_width) / 2 + self.crop_width / 2, (self.height - self.crop_height) / 2 + self.crop_height / 2

        cx, cy = (self.width - self.crop_width) / 2, (self.height - self.crop_height) / 2
        cmx, cmy = cx + self.crop_width, cy + self.crop_height

        cw = int(round(self.texture.width * ((cmx - cx) / (mx - x))))
        ch = int(round(self.texture.height * ((cmy - cy) / (my - y))))
        cenx, ceny = int(round((ccenx - x) * (self.texture.width / (mx - x)))), int(round((cceny - y) * (self.texture.height / (my - y))))
        return cw, ch, cenx, ceny


class FirstCropScatter(CropScatter):
    def calculate(self):
        if 'image' not in self.ids or self.ids.image.texture is None:
            return
        width, height = self.ids.image.texture.size
        frame_width, frame_height = self.width, self.height
        if width > height:
            self.image_width = frame_width
            self.image_height = height / width * frame_width
            self.frame_size = frame_width, frame_width
            self.image_y = (self.height - self.image_height) / 2
            self.crop_size = self.image_height, self.image_height
        else:
            self.image_height = frame_height
            self.image_width = width / height * frame_height
            self.frame_size = frame_height, frame_height
            self.image_x = (self.width - self.image_width) / 2
            self.crop_size = self.image_width, self.image_width

        w = 250 / 935 * self.image_height
        if w > self.image_width:
            h = 935 / 250 * self.image_width
            w = 250 / 935 * h
        else:
            h = 935 / 250 * w
        self.crop_size = w, h


class CroppedImage(Image):
    texture_width = NumericProperty(0)
    texture_height = NumericProperty(0)
    texture_size = ReferenceListProperty(texture_width, texture_height)
    texture_x = NumericProperty(0)
    texture_y = NumericProperty(0)
    texture_pos = ReferenceListProperty(texture_x, texture_y)

    crop_width = NumericProperty(0)
    crop_height = NumericProperty(0)
    crop_size = ReferenceListProperty(crop_width, crop_height)

    crop_x = NumericProperty(0)
    crop_y = NumericProperty(0)
    crop_pos = ReferenceListProperty(crop_x, crop_y)

    source = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tw, self.th = 1, 1
        self.cw, self.ch = 1, 1
        self.cx, self.cy = 0, 0

    def on_texture(self, instance, value):
        if self.texture is None:
            return
        self.tw = self.texture.width
        self.th = self.texture.height
        self.calculate_image_size()

    def set_crop(self, cw, ch, cx, cy):
        self.cw, self.ch, self.cx, self.cy = cw, ch, cx, cy
        self.calculate_image_size()

    def on_size(self, *args):
        self.calculate_image_size()

    def on_pos(self, *args):
        self.calculate_image_size()

    def calculate_image_size(self):
        self.crop_height = self.height
        self.crop_width = self.cw / self.ch * self.height
        if self.crop_width > self.width:
            self.crop_width = self.width
            self.crop_height = self.ch / self.cw * self.width
            scale = self.width / self.cw
        else:
            scale = self.height / self.ch
        self.crop_x, self.crop_y = self.width / 2 - self.crop_width / 2, self.height / 2 - self.crop_height / 2
        self.texture_width = self.tw * scale
        self.texture_height = self.th * scale
        self.texture_x = self.x + -(self.cx - self.cw / 2) * scale + self.crop_x
        self.texture_y = self.y + -(self.cy - self.ch / 2) * scale + self.crop_y


class CharacterCropper(App):
    def build(self):
        return Builder.load_file('CharacterCropper.kv')


if __name__ == "__main__":
    CharacterCropper().run()
