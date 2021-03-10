__all__ = ('Data',)

from .format import Constant, ControlMoveMCB, Bitmap, Place, TextureFragment
from .tools import read_header, read_header_compat, read_array
from .tools import read_translate, read_matrix, read_color, read_alpha_transform, read_color_transform
from .tools import read_object, read_texture, read_texture_fragment, read_texture_fragment_compat, read_bitmap, read_bitmap_ex
from .tools import read_font, read_text_property, read_text, read_particle_data, read_particle, read_program_object
from .tools import read_graphic_object, read_graphic, read_animation_data, read_animation, read_button_condition, read_button
from .tools import read_label, read_instance_name, read_event, read_place_compat, read_control_move_m, read_control_move_c, read_control_move_mc, read_control_move_mcb
from .tools import read_control, read_frame, read_movie_clip_event, read_movie, read_movie_linkage, read_string_data, read_string


class Data:
    def __init__(self, *args):
        self.header = None
        self.translates = None
        self.matrices = None
        self.colors = None
        self.alpha_transforms = None
        self.color_transforms = None
        self.objects = None
        self.textures = None
        self.texture_fragments = None
        self.bitmaps = None
        self.bitmap_exs = None
        self.fonts = None
        self.text_properties = None
        self.texts = None
        self.particle_datas = None
        self.particles = None
        self.program_objects = None
        self.graphic_objects = None
        self.graphics = None
        self.animations = None
        self.button_conditions = None
        self.buttons = None
        self.labels = None
        self.instance_names = None
        self.events = None
        self.places = None
        self.control_move_ms = None
        self.control_move_cs = None
        self.control_move_mcs = None
        self.control_move_mcbs = None
        self.controls = None
        self.frames = None
        self.move_clip_events = None
        self.movies = None
        self.movie_linkages = None
        self.strings = None

        self.string_map = {}
        self.instance_name_map = {}
        self.event_map = {}
        self.movie_linkage_map = {}
        self.movie_linkage_name_map = {}
        self.program_object_map = {}
        self.label_map = {}
        self.bitmap_map = {}

        self.resource_cache = {}

        self.name = None
        self.use_script = False
        self.use_texture_atlas = False
        self.valid = False

        if len(args) == 0:
            data = [0x4c, 0x57, 0x46, 0x00, 0x12, 0x10, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x3c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x01, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0x00, 0x44, 0x01, 0x00, 0x00,
                    0x0c, 0x00, 0x00, 0x00, 0x50, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x50, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x58, 0x01, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x58, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x58, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x5c, 0x01, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x5c, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
                    0x64, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x64, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x64, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x64, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x64, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x64, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x00, 0x00,
                    0x01, 0x00, 0x00, 0x00, 0x68, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x68, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x68, 0x01, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x68, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x68, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x68, 0x01, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x68, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
                    0x70, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x01, 0x00, 0x00,
                    0x01, 0x00, 0x00, 0x00, 0x8c, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
                    0x94, 0x01, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0xa4, 0x01, 0x00, 0x00,
                    0x5f, 0x72, 0x6f, 0x6f, 0x74, 0x00, 0x6e, 0x75, 0x6c, 0x6c, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3f,
                    0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x05, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00]
            self._load(data, len(data))
        else:
            self._load(*args)

    def _load(self, data_bytes, length):
        if length < Constant.HEADER_SIZE_COMPAT_0:
            return
        p = 0
        end = p + length
        self.header, p = read_header(data_bytes, p)

        if self.header.id_0 != ord('L') and self.header.id_1 != ord('W') and self.header.id_2 == ord('F') and self.header.id_3 != Constant.FORMAT_TYPE:
            return
        v0 = self.header.format_version_0
        v1 = self.header.format_version_1
        v2 = self.header.format_version_2
        if not ((
                        v0 == Constant.FORMAT_VERSION_0 and
                        v1 == Constant.FORMAT_VERSION_1 and
                        v2 == Constant.FORMAT_VERSION_2
                ) or (
                        v0 == Constant.FORMAT_VERSION_COMPAT_0_0 and
                        v1 == Constant.FORMAT_VERSION_COMPAT_0_1 and
                        v2 == Constant.FORMAT_VERSION_COMPAT_0_2
                ) or (
                        v0 == Constant.FORMAT_VERSION_COMPAT_1_0 and
                        v1 == Constant.FORMAT_VERSION_COMPAT_1_1 and
                        v2 == Constant.FORMAT_VERSION_COMPAT_1_2
                )):
            return

        format_version = (v0 << 16) | (v1 << 8) | v2
        if format_version >= Constant.FORMAT_VERSION_141211:
            header_size = Constant.HEADER_SIZE
        else:
            header_size = Constant.HEADER_SIZE_COMPAT_0
            p = 0
            c, p = read_header_compat(data_bytes, p)
            control_move_mcb = ControlMoveMCB()
            control_move_mcb.offset = 0
            control_move_mcb.length = 0

            self.header.id_0 = c.id_0
            self.header.id_1 = c.id_1
            self.header.id_2 = c.id_2
            self.header.id_3 = c.id_3
            self.header.format_version_0 = c.format_version_0
            self.header.format_version_1 = c.format_version_1
            self.header.format_version_2 = c.format_version_2
            self.header.option = c.option

            self.header.width = c.width
            self.header.height = c.height
            self.header.frame_rate = c.frame_rate
            self.header.root_movie_id = c.root_movie_id
            self.header.name_string_id = c.name_string_id
            self.header.background_color = c.background_color

            self.header.string_bytes = c.string_bytes
            self.header.animation_bytes = c.animation_bytes
            self.header.translate = c.translate
            self.header.matrix = c.matrix
            self.header.color = c.color
            self.header.alpha_transform = c.alpha_transform
            self.header.color_transform = c.color_transform
            self.header.object_data = c.object_data
            self.header.texture = c.texture
            self.header.texture_fragment = c.texture_fragment
            self.header.bitmap = c.bitmap
            self.header.bitmap_ex = c.bitmap_ex
            self.header.font = c.font
            self.header.text_property = c.text_property
            self.header.text = c.text
            self.header.particle_data = c.particle_data
            self.header.particle = c.particle
            self.header.program_object = c.program_object
            self.header.graphic_object = c.graphic_object
            self.header.graphic = c.graphic
            self.header.animation = c.animation
            self.header.button_condition = c.button_condition
            self.header.button = c.button
            self.header.label = c.label
            self.header.instance_name = c.instance_name
            self.header.event_data = c.event_data
            self.header.place = c.place
            self.header.control_move_m = c.control_move_m
            self.header.control_move_c = c.control_move_c
            self.header.control_move_mc = c.control_move_mc
            self.header.control_move_mcb = control_move_mcb
            self.header.control = c.control
            self.header.frame = c.frame
            self.header.movie_clip_event = c.movie_clip_event
            self.header.movie = c.movie
            self.header.movie_linkage = c.movie_linkage
            self.header.string_data = c.string_data
            self.header.lwf_length = c.lwf_length

        if (self.header.option & Constant.OPTION_COMPRESSED) != 0:
            if self.header.lwf_length <= header_size:
                return

            valid, decompressed, p = Decompress(data_bytes, p, length - header_size)
            if valid:
                end = p + len(decompressed)
            else:
                return
        else:
            if length < self.header.lwf_length:
                return

        string_byte_data = data_bytes[p:p + self.header.string_bytes.length]
        p += self.header.string_bytes.length
        animation_byte_data = data_bytes[p:p + self.header.animation_bytes.length]
        p += self.header.animation_bytes.length

        self.translates, p = read_array(data_bytes, p, self.header.translate, read_translate)
        self.matrices, p = read_array(data_bytes, p, self.header.matrix, read_matrix)
        self.colors, p = read_array(data_bytes, p, self.header.color, read_color)
        self.alpha_transforms, p = read_array(data_bytes, p, self.header.alpha_transform, read_alpha_transform)
        self.color_transforms, p = read_array(data_bytes, p, self.header.color_transform, read_color_transform)
        self.objects, p = read_array(data_bytes, p, self.header.object_data, read_object)
        self.textures, p = read_array(data_bytes, p, self.header.texture, read_texture)
        if format_version >= Constant.FORMAT_VERSION_141211:
            self.texture_fragments, p = read_array(data_bytes, p, self.header.texture_fragment, read_texture_fragment)
        else:
            texture_fragment_compats, p = read_array(data_bytes, p, self.header.texture_fragment, read_texture_fragment_compat)
            self.texture_fragments = []
            for texture_fragment_compat in texture_fragment_compats:
                self.texture_fragments.append(texture_fragment_compat.convert(TextureFragment))
        self.bitmaps, p = read_array(data_bytes, p, self.header.bitmap, read_bitmap)
        self.bitmap_exs, p = read_array(data_bytes, p, self.header.bitmap_ex, read_bitmap_ex)
        self.fonts, p = read_array(data_bytes, p, self.header.font, read_font)
        self.text_properties, p = read_array(data_bytes, p, self.header.text_property, read_text_property)
        self.texts, p = read_array(data_bytes, p, self.header.text, read_text)
        self.particle_datas, p = read_array(data_bytes, p, self.header.particle_data, read_particle_data)
        self.particles, p = read_array(data_bytes, p, self.header.particle, read_particle)
        self.program_objects, p = read_array(data_bytes, p, self.header.program_object, read_program_object)
        self.graphic_objects, p = read_array(data_bytes, p, self.header.graphic_object, read_graphic_object)
        self.graphics, p = read_array(data_bytes, p, self.header.graphic, read_graphic)
        animation_data, p = read_array(data_bytes, p, self.header.animation, read_animation_data)
        self.button_conditions, p = read_array(data_bytes, p, self.header.button_condition, read_button_condition)
        self.buttons, p = read_array(data_bytes, p, self.header.button, read_button)
        self.labels, p = read_array(data_bytes, p, self.header.label, read_label)
        self.instance_names, p = read_array(data_bytes, p, self.header.instance_name, read_instance_name)
        self.events, p = read_array(data_bytes, p, self.header.event_data, read_event)
        self.place_compats, p = read_array(data_bytes, p, self.header.place, read_place_compat)
        self.control_move_ms, p = read_array(data_bytes, p, self.header.control_move_m, read_control_move_m)
        self.control_move_cs, p = read_array(data_bytes, p, self.header.control_move_c, read_control_move_c)
        self.control_move_mcs, p = read_array(data_bytes, p, self.header.control_move_mc, read_control_move_mc)
        if format_version >= Constant.FORMAT_VERSION_141211:
            self.control_move_mcbs, p = read_array(data_bytes, p, self.header.control_move_mcb, read_control_move_mcb)
        self.controls, p = read_array(data_bytes, p, self.header.control, read_control)
        self.frames, p = read_array(data_bytes, p, self.header.frame, read_frame)
        self.movie_clip_events, p = read_array(data_bytes, p, self.header.movie_clip_event, read_movie_clip_event)
        self.movies, p = read_array(data_bytes, p, self.header.movie, read_movie)
        self.movie_linkages, p = read_array(data_bytes, p, self.header.movie_linkage, read_movie_linkage)
        string_data, p = read_array(data_bytes, p, self.header.string_data, read_string_data)

        if p != end:
            return

        self.places = []
        for place_compat in self.place_compats:
            place = Place()
            place.depth = place_compat.depth & 0xffffff
            place.object_id = place_compat.object_id
            place.instance_id = place_compat.instance_id
            place.matrix_id = place_compat.matrix_id
            place.blend_mode = place_compat.depth >> 24
            self.places.append(place)

        self.strings = []
        for string_data in string_data:
            self.strings.append(read_string(string_byte_data, string_data))

        self.animations = []
        for animation_data in animation_data:
            self.animations.append(read_animation(animation_byte_data, animation_data))

        self.string_map = {}
        for index, string in enumerate(self.strings):
            self.string_map[string] = index

        self.instance_name_map = {}
        for index, instance_name in enumerate(self.instance_names):
            self.instance_name_map[instance_name.string_id] = index

        self.event_map = {}
        for index, event in enumerate(self.events):
            self.event_map[event.string_id] = index

        self.movie_linkage_map = {}
        self.movie_linkage_name_map = {}
        for index, movie_linkage in enumerate(self.movie_linkages):
            self.movie_linkage_map[movie_linkage.string_id] = index
            self.movie_linkage_name_map[movie_linkage.movie_id] = movie_linkage.string_id

        self.program_object_map = {}
        for index, program_object in enumerate(self.program_objects):
            self.program_object_map[program_object.string_id] = index

        self.label_map = []
        for index, movie in enumerate(self.movies):
            offset = movie.label_offset
            string_map = {}
            for j in range(0, movie.labels):
                label = self.labels[offset + j]
                string_map[label.string_id] = label.frame_no
            self.label_map.append(string_map)

        for texture in self.textures:
            texture.set_filename(self)

        for tfId, texture_fragment in enumerate(self.texture_fragments):
            texture_fragment.set_filename(self)
            self.bitmap_map[texture_fragment.filename] = len(self.bitmaps)
            self.bitmaps.append(Bitmap(0, tfId))

        self.name = self.strings[self.header.name_string_id]
        self.use_script = (self.header.option & Constant.OPTION_USE_LUASCRIPT) != 0
        self.use_texture_atlas = (self.header.option & Constant.OPTION_USE_TEXTUREATLAS) != 0

        self.valid = True

    def check(self):
        return self.valid

    def replace_texture(self, index, texture_replacement):
        if index < 0 or index >= len(self.textures):
            return False

        self.textures[index] = texture_replacement
        return True

    def replace_texture_fragment(self, index, texture_fragment_replacement):
        if index < 0 or index >= len(self.texture_fragments):
            return False

        self.texture_fragments[index] = texture_fragment_replacement
        return True
