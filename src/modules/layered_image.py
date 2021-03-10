from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import AliasProperty, DictProperty, ListProperty
from kivy.resources import resource_find
from kivy.uix.widget import Widget
from kivy.core.image import Image as CoreImage

from refs import Refs


class LayeredImage(Widget):
    data = ListProperty([])

    textures = DictProperty({})
    images = ListProperty([])

    def force_reload(self):
        self.on_data()

    def on_data(self, *args):
        self.textures = {}
        for widget in self.data:
            image_id = widget['id']
            source = widget['source']
            try:
                image = CoreImage(source)
            except Exception:
                Refs.log(f'Image: Error loading {source}', 'error')
                continue
            self.images.append(image)
            self.textures[image_id] = image.texture
            del image
        # print(self.textures)
        self.get_image_sizes()
        self.get_image_poses()

    def get_image_sizes(self, *largs):
        image_sizes = {}
        self.image_gaps = {}
        for widget in self.data:
            image_id = widget['id']
            w_h, h_h = widget['size_hint']
            wgap, hgap = 0, 0
            if 'keep_ratio' in widget:
                width, height = w_h * self.width, h_h * self.height
            else:
                mwidth, mheight = w_h * self.width, h_h * self.height
                if image_id not in self.textures:
                    continue
                tex_size = self.textures[image_id].size
                if tex_size[0] > tex_size[1]:
                    width = mwidth
                    height = tex_size[1] / tex_size[0] * mwidth
                    hgap = mheight - height
                else:
                    width = tex_size[0] / tex_size[1] * mheight
                    height = mheight
                    wgap = mwidth - width
            image_sizes[image_id] = [width, height]
            self.image_gaps[image_id] = [wgap / 2, hgap / 2]
        return image_sizes

    image_sizes = AliasProperty(get_image_sizes, bind=('size', 'size_hint'))

    def get_image_poses(self, *largs):
        image_poses = {}
        for widget in self.data:
            image_id = widget['id']
            if image_id not in self.image_sizes:
                continue
            p_h = widget['pos_hint']
            x, y = 0, 0
            for key, value in p_h.items():
                if key == 'x':
                    x = value * self.width + self.image_gaps[image_id][0]
                elif key == 'right':
                    x = value * self.width - self.image_sizes[image_id][0] - self.image_gaps[image_id][0]
                elif key == 'center_x':
                    x = value * self.width - self.image_sizes[image_id][0] / 2 + self.image_gaps[image_id][0]
                elif key == 'y':
                    y = value * self.height + self.image_gaps[image_id][1]
                elif key == 'top':
                    y = value * self.height - self.image_sizes[image_id][1] - self.image_gaps[image_id][1]
                elif key == 'center_y':
                    y = value * self.height - self.image_sizes[image_id][1] / 2 + self.image_gaps[image_id][1]
            image_poses[image_id] = [x, y]
        return image_poses

    image_poses = AliasProperty(get_image_poses, bind=('pos', 'pos_hint'))

    def make_rectangles(self):
        # TODO: Update rectangles on change
        self.canvas.clear()
        for image_id, texture in self.textures.items():
            size = self.image_sizes[image_id]
            pos = self.image_poses[image_id]
            # print(texture, size, pos)
            self.canvas.add(Rectangle(texture=texture, size=size, pos=pos))
        return None

    rectangle = AliasProperty(make_rectangles, bind=('textures', 'image_sizes', 'image_poses'))