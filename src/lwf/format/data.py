from os.path import exists

from lwf.modules.constant import FORMAT_VERSION, FORMAT_VERSION_COMPAT_0, FORMAT_VERSION_COMPAT_1, HEADER_SIZE, OPTION_COMPRESSED, OPTION_USE_LUASCRIPT, OPTION_USE_SCRIPT, OPTION_USE_TEXTUREATLAS
from lwf.format.bitmap_data import Bitmap
from lwf.modules.read import read_alpha_transform, read_animation, read_bitmap, read_bitmap_ex, read_button, read_button_condition, read_bytes, read_array, read_byte, read_color, read_color_transform, read_control, read_control_move_c, read_control_move_m, \
    read_control_move_mc, read_control_move_mcb, read_event, read_font, read_frame, read_graphic, read_graphic_object, read_instance_name, read_int32, read_item_array, \
    read_label, read_matrix, \
    read_movie, read_movie_clip_event, read_movie_linkage, read_object, \
    read_particle, \
    read_particle_data, \
    read_place_compat, read_program_object, read_string, read_text, \
    read_text_property, \
    read_texture, \
    read_texture_fragment, \
    read_texture_fragment_compat, \
    read_translate


class Data:
    def __init__(self, path):
        self.valid = False
        if exists(path):
            file = open(path, 'rb')
            self._load(file)
            file.close()
        else:
            raise FileNotFoundError(path)

    def _load(self, file):
        id_bytes = read_bytes(file, 4)
        if id_bytes != b'LWF\x00':
            return

        format_version = read_bytes(file, 3)
        if format_version not in (FORMAT_VERSION, FORMAT_VERSION_COMPAT_0, FORMAT_VERSION_COMPAT_1):
            return

        self.option = read_byte(file)

        self.width = read_int32(file)
        self.height = read_int32(file)
        self.frame_rate = read_int32(file)
        self.root_movie_id = read_int32(file)
        self.name_string_id = read_int32(file)
        self.background_color = read_int32(file)

        string_bytes = read_item_array(file)
        animation_bytes = read_item_array(file)
        translate = read_item_array(file)
        matrix = read_item_array(file)
        color = read_item_array(file)
        alpha_transform = read_item_array(file)
        color_transform = read_item_array(file)
        object_data = read_item_array(file)
        texture = read_item_array(file)
        texture_fragment = read_item_array(file)
        bitmap = read_item_array(file)
        bitmap_ex = read_item_array(file)
        font = read_item_array(file)
        text_property = read_item_array(file)
        text = read_item_array(file)
        particle_data = read_item_array(file)
        particle = read_item_array(file)
        program_object = read_item_array(file)
        graphic_object = read_item_array(file)
        graphic = read_item_array(file)
        animation = read_item_array(file)
        button_condition = read_item_array(file)
        button = read_item_array(file)
        label = read_item_array(file)
        instance_name = read_item_array(file)
        event_data = read_item_array(file)
        place = read_item_array(file)
        control_move_m = read_item_array(file)
        control_move_c = read_item_array(file)
        control_move_mc = read_item_array(file)
        if format_version >= FORMAT_VERSION:
            control_move_mcb = read_item_array(file)
        else:
            control_move_mcb = 0, 0
        control = read_item_array(file)
        frame = read_item_array(file)
        movie_clip_event = read_item_array(file)
        movie = read_item_array(file)
        movie_linkage = read_item_array(file)
        string_data = read_item_array(file)

        lwf_length = read_int32(file)

        if format_version == FORMAT_VERSION and lwf_length <= HEADER_SIZE:
            print('LWF has no data!')
            return

        # if self.option == OPTION_USE_SCRIPT:
        #     print('LWF uses script.')
        #
        # if self.option == OPTION_USE_TEXTUREATLAS:
        #     print('LWF uses texture atlas.')

        if self.option == OPTION_COMPRESSED:
            print('LWF is compressed.')
            print('We can\'t handle this!')
            return

        # if self.option == OPTION_USE_LUASCRIPT:
        #     print('LWF uses lua script.')

        string_byte_data = read_bytes(file, string_bytes[1])
        animation_byte_data = read_bytes(file, animation_bytes[1])

        self.translates = read_array(file, *translate, read_translate)
        self.matrices = read_array(file, *matrix, read_matrix)
        self.colors = read_array(file, *color, read_color)
        self.alpha_transforms = read_array(file, *alpha_transform, read_alpha_transform)
        self.color_transforms = read_array(file, *color_transform, read_color_transform)
        self.objects = read_array(file, *object_data, read_object)
        self.textures = read_array(file, *texture, read_texture)

        if format_version >= FORMAT_VERSION:
            self.texture_fragments = read_array(file, *texture_fragment, read_texture_fragment)
        else:
            self.texture_fragments = read_array(file, *texture_fragment, read_texture_fragment_compat)

        self.bitmaps = read_array(file, *bitmap, read_bitmap)
        self.bitmap_exs = read_array(file, *bitmap_ex, read_bitmap_ex)
        self.fonts = read_array(file, *font, read_font)
        self.text_properties = read_array(file, *text_property, read_text_property)
        self.texts = read_array(file, *text, read_text)
        self.particle_datas = read_array(file, *particle_data, read_particle_data)
        self.particles = read_array(file, *particle, read_particle)
        self.program_objects = read_array(file, *program_object, read_program_object)
        self.graphic_objects = read_array(file, *graphic_object, read_graphic_object)
        self.graphics = read_array(file, *graphic, read_graphic)
        animation_data = read_array(file, *animation, read_item_array)
        self.button_conditions = read_array(file, *button_condition, read_button_condition)
        self.buttons = read_array(file, *button, read_button)
        self.labels = read_array(file, *label, read_label)
        self.instance_names = read_array(file, *instance_name, read_instance_name)
        self.events = read_array(file, *event_data, read_event)
        self.place_compats = read_array(file, *place, read_place_compat)
        self.control_move_ms = read_array(file, *control_move_m, read_control_move_m)
        self.control_move_cs = read_array(file, *control_move_c, read_control_move_c)
        self.control_move_mcs = read_array(file, *control_move_mc, read_control_move_mc)
        if format_version == FORMAT_VERSION:
            self.control_move_mcbs = read_array(file, *control_move_mcb, read_control_move_mcb)
        self.controls = read_array(file, *control, read_control)
        self.frames = read_array(file, *frame, read_frame)
        self.movie_clip_events = read_array(file, *movie_clip_event, read_movie_clip_event)
        self.movies = read_array(file, *movie, read_movie)
        self.movie_linkages = read_array(file, *movie_linkage, read_movie_linkage)
        string_data = read_array(file, *string_data, read_item_array)

        if file.tell() != lwf_length:
            return

        self.strings = [read_string(string_byte_data, *string_obj) for string_obj in string_data]

        # print(self.strings)

        def resolve_strings(self, objects):
            for object in objects:
                if object.string_id == -1:
                    print('Object with invalid stringId')
                    continue
                object.string = self.strings[object.string_id]

        resolve_strings(self, self.events)
        resolve_strings(self, self.fonts)
        resolve_strings(self, self.instance_names)
        resolve_strings(self, self.labels)
        resolve_strings(self, self.movie_linkages)
        resolve_strings(self, self.particle_datas)
        resolve_strings(self, self.program_objects)

        for text in self.texts:
            text.string = self.strings[text.string_id]
            text.name_string = self.strings[text.name_string_id]

        for texture in self.textures:
            texture.filename = self.strings[texture.string_id]

        self.bitmap_map = {}
        for tfId, texture_fragment in enumerate(self.texture_fragments):
            texture_fragment.filename = self.strings[texture_fragment.string_id]
            texture_fragment.init(self.textures[texture_fragment.texture_id])
            self.bitmap_map[texture_fragment.filename] = len(self.bitmaps)
            self.bitmaps.append(Bitmap(0, tfId))

        self.name = self.strings[self.name_string_id]

        self.animations = [read_animation(animation_byte_data, *animation_obj) for animation_obj in animation_data]
        # print('This LWF has', len(self.animations), 'animations')

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

        self.valid = True
