__all__ = ('HeaderCompat',)


class HeaderCompat:
    def __init__(self):
        self.id_0 = 0x0
        self.id_1 = 0x0
        self.id_2 = 0x0
        self.id_3 = 0x0
        self.format_version_0 = 0x0
        self.format_version_1 = 0x0
        self.format_version_2 = 0x0
        self.option = 0x0

        self.width = 0
        self.height = 0
        self.frame_rate = 0
        self.root_movie_id = 0
        self.name_string_id = 0
        self.background_color = 0

        self.string_bytes = None
        self.animation_bytes = None
        self.translate = None
        self.matrix = None
        self.color = None
        self.alpha_transform = None
        self.color_transform = None
        self.object_data = None
        self.texture = None
        self.texture_fragment = None
        self.bitmap = None
        self.bitmap_ex = None
        self.font = None
        self.text_property = None
        self.text = None
        self.particle_data = None
        self.particle = None
        self.program_object = None
        self.graphic_object = None
        self.graphic = None
        self.animation = None
        self.button_condition = None
        self.button = None
        self.label = None
        self.instance_name = None
        self.event_data = None
        self.place = None
        self.control_move_m = None
        self.control_move_c = None
        self.control_move_mc = None
        self.control = None
        self.frame = None
        self.movie_clip_event = None
        self.movie = None
        self.movie_linkage = None
        self.string_data = None

        self.lwf_length = 0

    def __str__(self):
        return f"Header Compat <Width: {self.width}, Height: {self.height}, Frame Rate: {self.frame_rate}, Root Movie Id: {self.root_movie_id}, Name String Id: {self.name_string_id}, Background Color: {self.background_color}"
