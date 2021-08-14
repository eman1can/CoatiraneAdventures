from struct import unpack

from lwf.format.event_data import Event
from lwf.format.alpha_transform_data import AlphaTransform
from lwf.format.animation_data import CALL, END, EVENT, GOTO_FRAME, GOTO_LABEL, NEXT_FRAME, PLAY, PREV_FRAME, SET_TARGET, STOP
from lwf.format.bitmap_data import Bitmap
from lwf.format.button_data import Button
from lwf.format.button_condition import ButtonCondition
from lwf.modules.color_transform import ColorTransform
from lwf.format.control_move_data import Control, ControlMoveC, ControlMoveM, ControlMoveMC, ControlMoveMCB
from lwf.format.font_data import Font
from lwf.format.frame_data import Frame
from lwf.format.graphic_data import Graphic
from lwf.format.graphic_object_data import GraphicObject
from lwf.format.instance_name_data import InstanceName
from lwf.format.label_data import Label
from lwf.format.movie_data import Movie
from lwf.format.movie_clip_event_data import MovieClipEvent
from lwf.format.movie_linkage_data import MovieLinkage
from lwf.format.object_data import Object
from lwf.format.particle_data import Particle
from lwf.format.particle_name_data import ParticleData
from lwf.format.place_data import Place
from lwf.format.program_object_data import ProgramObject
from lwf.format.text_data import Text
from lwf.format.text_property_data import TextProperty
from lwf.format.texture_data import Texture
from lwf.format.texture_fragment_data import TextureFragment
from lwf.format.translate_data import Translate
from lwf.modules.matrix import Matrix


def read_byte(file):
    return file.read(1)[0]


def read_bytes(file, length):
    return file.read(length)


def read_uint32(file):
    return unpack('<I', file.read(4))[0]


def read_int32(file):
    return unpack('<i', file.read(4))[0]


def read_single(file):
    return unpack('<f', file.read(4))[0]


def read_item_array(file):
    offset = read_int32(file)
    length = read_int32(file)
    return offset, length


def read_array(file, offset, length, read_item):
    if file.tell() != offset:
        raise Exception('Read Error')
    return [read_item(file) for _ in range(length)]


def read_translate(file):
    translate = Translate()
    translate.translate_x = read_single(file)
    translate.translate_y = read_single(file)
    return translate


def read_matrix(file):
    matrix = Matrix()
    matrix.scale_x = read_single(file)
    matrix.scale_y = read_single(file)
    matrix.skew_0 = read_single(file)
    matrix.skew_1 = read_single(file)
    matrix.translate_x = read_single(file)
    matrix.translate_y = read_single(file)
    return matrix


def read_color(file):
    r = read_single(file)
    g = read_single(file)
    b = read_single(file)
    a = read_single(file)
    return r, g, b, a


def read_alpha_transform(file):
    alpha_transform = AlphaTransform()
    alpha_transform.alpha = read_single(file)
    return alpha_transform


def read_color_transform(file):
    return ColorTransform(*read_color(file), *read_color(file))


def read_object(file):
    obj = Object()
    obj.object_type = read_int32(file)
    obj.object_id = read_int32(file)
    return obj


def read_texture(file):
    texture = Texture()
    texture.string_id = read_int32(file)
    texture.format = read_int32(file)
    texture.width = read_int32(file)
    texture.height = read_int32(file)
    texture.scale = read_single(file)
    return texture


def read_texture_fragment(file):
    texture_fragment = read_texture_fragment_compat(file)
    texture_fragment.ow = read_int32(file)
    texture_fragment.oh = read_int32(file)
    return texture_fragment


def read_texture_fragment_compat(file):
    texture_fragment = TextureFragment()
    texture_fragment.string_id = read_int32(file)
    texture_fragment.texture_id = read_int32(file)
    texture_fragment.rotated = read_int32(file)
    texture_fragment.x = read_int32(file)
    texture_fragment.y = read_int32(file)
    texture_fragment.u = read_int32(file)
    texture_fragment.v = read_int32(file)
    texture_fragment.w = read_int32(file)
    texture_fragment.h = read_int32(file)
    return texture_fragment


def read_bitmap(file):
    bitmap = Bitmap()
    bitmap.matrix_id = read_int32(file)
    bitmap.texture_fragment_id = read_int32(file)
    return bitmap


def read_bitmap_ex(file):
    bitmap = read_bitmap(file)
    bitmap.attribute = read_int32(file)
    bitmap.u = read_single(file)
    bitmap.v = read_single(file)
    bitmap.w = read_single(file)
    bitmap.h = read_single(file)
    return bitmap


def read_font(file):
    font = Font()
    font.string_id = read_int32(file)
    font.letter_spacing = read_single(file)
    return font


def read_text_property(file):
    text_property = TextProperty()
    text_property.max_length = read_int32(file)
    text_property.font_id = read_int32(file)
    text_property.font_height = read_int32(file)
    text_property.align = read_int32(file)
    text_property.left_margin = read_int32(file)
    text_property.right_margin = read_int32(file)
    text_property.letter_spacing = read_single(file)
    text_property.leading = read_int32(file)
    text_property.stroke_color_id = read_int32(file)
    text_property.stroke_width = read_int32(file)
    text_property.shadow_color_id = read_int32(file)
    text_property.shadow_offset_x = read_int32(file)
    text_property.shadow_offset_y = read_int32(file)
    text_property.shadow_blur = read_int32(file)
    return text_property


def read_text(file):
    text = Text()
    text.matrix_id = read_int32(file)
    text.name_string_id = read_int32(file)
    text.text_property_id = read_int32(file)
    text.string_id = read_int32(file)
    text.color_id = read_int32(file)
    text.width = read_int32(file)
    text.height = read_int32(file)
    return text


def read_particle_data(file):
    particle_data = ParticleData()
    particle_data.string_id = read_int32(file)
    return particle_data


def read_particle(file):
    particle = Particle()
    particle.matrix_id = read_int32(file)
    particle.color_transform_id = read_int32(file)
    particle.particle_data_id = read_int32(file)
    return particle


def read_program_object(file):
    program_object = ProgramObject()
    program_object.string_id = read_int32(file)
    program_object.width = read_int32(file)
    program_object.height = read_int32(file)
    program_object.matrix_id = read_int32(file)
    program_object.color_transform_id = read_int32(file)
    return program_object


def read_graphic_object(file):
    graphic_object = GraphicObject()
    graphic_object.graphic_object_type = read_int32(file)
    graphic_object.graphic_object_id = read_int32(file)
    return graphic_object


def read_graphic(file):
    graphic = Graphic()
    graphic.graphic_object_id = read_int32(file)
    graphic.graphic_objects = read_int32(file)
    return graphic


def read_button_condition(file):
    button_condition = ButtonCondition()
    button_condition.condition = read_int32(file)
    button_condition.key_code = read_int32(file)
    button_condition.animation_id = read_int32(file)
    return button_condition


def read_button(file):
    button = Button()
    button.width = read_int32(file)
    button.height = read_int32(file)
    button.matrix_id = read_int32(file)
    button.color_transform_id = read_int32(file)
    button.condition_id = read_int32(file)
    button.conditions = read_int32(file)
    return button


def read_label(file):
    label = Label()
    label.string_id = read_int32(file)
    label.frame_no = read_int32(file)
    return label


def read_instance_name(file):
    instance_name = InstanceName()
    instance_name.string_id = read_int32(file)
    return instance_name


def read_event(file):
    event = Event()
    event.string_id = read_int32(file)
    return event


def read_place_compat(file):
    place_compat = Place()
    place_compat.depth = read_int32(file)
    place_compat.object_id = read_int32(file)
    place_compat.instance_id = read_int32(file)
    place_compat.matrix_id = read_int32(file)
    place_compat.blend_mode = place_compat.depth >> 24
    place_compat.depth = place_compat.depth & 0xffffff
    return place_compat


def read_control_move_m(file):
    control_move_m = ControlMoveM()
    control_move_m.place_id = read_int32(file)
    control_move_m.matrix_id = read_int32(file)
    return control_move_m


def read_control_move_c(file):
    control_move_c = ControlMoveC()
    control_move_c.place_id = read_int32(file)
    control_move_c.color_transform_id = read_int32(file)
    return control_move_c


def read_control_move_mc(file):
    control_move_mc = ControlMoveMC()
    control_move_mc.place_id = read_int32(file)
    control_move_mc.matrix_id = read_int32(file)
    control_move_mc.color_transform_id = read_int32(file)
    return control_move_mc


def read_control_move_mcb(file):
    control_move_mcb = ControlMoveMCB()
    control_move_mcb.place_id = read_int32(file)
    control_move_mcb.matrix_id = read_int32(file)
    control_move_mcb.color_transform_id = read_int32(file)
    control_move_mcb.blend_mode = read_int32(file)
    return control_move_mcb


def read_control(file):
    control = Control()
    control.control_type = read_int32(file)
    control.control_id = read_int32(file)
    return control


def read_frame(file):
    frame = Frame()
    frame.control_offset = read_int32(file)
    frame.controls = read_int32(file)
    return frame


def read_movie_clip_event(file):
    movie_clip_event = MovieClipEvent()
    movie_clip_event.clip_event = read_int32(file)
    movie_clip_event.animation_id = read_int32(file)
    return movie_clip_event


def read_movie(file):
    movie = Movie()
    movie.depths = read_int32(file)
    movie.label_offset = read_int32(file)
    movie.labels = read_int32(file)
    movie.frame_offset = read_int32(file)
    movie.frames = read_int32(file)
    movie.clip_event_id = read_int32(file)
    movie.clip_events = read_int32(file)
    return movie


def read_movie_linkage(file):
    movie_linkage = MovieLinkage()
    movie_linkage.string_id = read_int32(file)
    movie_linkage.movie_id = read_int32(file)
    return movie_linkage


def read_string(string_byte_data, string_offset, string_length):
    return string_byte_data[string_offset:string_offset + string_length].decode('utf-8')


def read_animation(animation_byte_data, animation_offset, animation_length):
    animation_end = animation_offset + animation_length

    def int32(x):
        return unpack('<i', animation_byte_data[x:x + 4])[0]

    array = []
    while True:
        if animation_offset >= animation_end:
            return array

        code = animation_byte_data[animation_offset]
        animation_offset += 1
        array.append(int(code))

        if code in (PLAY, STOP, NEXT_FRAME, PREV_FRAME):
            pass
        elif code in (GOTO_FRAME, GOTO_LABEL, EVENT, CALL):
            array.append(int32(animation_offset))
            animation_offset += 4
        elif code == SET_TARGET:
            count = int32(animation_offset)
            array.append(count)
            animation_offset += 4
            for i in range(count):
                target = int32(animation_offset)
                animation_offset += 4
                array.append(target)
        elif code == END:
            return array
