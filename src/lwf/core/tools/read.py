__all__ = ('read_animation', 'read_item_array', 'read_header', 'read_header_compat', 'read_array', 'read_translate',
           'read_matrix', 'read_color', 'read_alpha_transform', 'read_color_transform', 'read_object', 'read_texture', 'read_texture_fragment',
           'read_texture_fragment_compat', 'read_bitmap', 'read_bitmap_ex', 'read_font', 'read_text_property', 'read_text', 'read_particle_data',
           'read_particle', 'read_program_object', 'read_graphic_object', 'read_graphic', 'read_animation_data', 'read_animation', 'read_button_condition',
           'read_button', 'read_label', 'read_instance_name', 'read_event', 'read_place_compat', 'read_control_move_m', 'read_control_move_c', 'read_control_move_mc',
           'read_control_move_mcb', 'read_control', 'read_frame', 'read_movie_clip_event', 'read_movie', 'read_movie_linkage', 'read_string_data', 'read_string')

from .binary_reader import read_byte, read_int32, read_single
from ..constructs.animation import Animation as Anim
from ..format.animation import Animation
from ..format.bitmap import Bitmap, BitmapEx
from ..format.button import Button, ButtonCondition
from ..format.control import Control, ControlMoveC, ControlMoveM, ControlMoveMC, ControlMoveMCB
from ..format.event import Event
from ..format.font import Font
from ..format.frame import Frame
from ..format.graphic import Graphic, GraphicObject
from ..format.header import Header, HeaderCompat
from ..format.instance_name import InstanceName
from ..format.item_array import ItemArray
from ..format.label import Label
from ..format.movie import Movie, MovieClipEvent, MovieLinkage
from ..format.object import Object
from ..format.particle import Particle, ParticleData
from ..format.place import PlaceCompat, Place
from ..format.string import String
from ..format.text import Text
from ..format.text import TextProperty
from ..format.texture import Texture, TextureFragment, TextureFragmentCompat
from ..format.program_object import ProgramObject
from ..type import AlphaTransform, Color, ColorTransform, Matrix, Translate
from ...filelogger import log


def read_item_array(data_bytes, p):
    array = ItemArray()
    array.offset, p = read_int32(data_bytes, p)
    array.length, p = read_int32(data_bytes, p)
    return array, p


def read_header(data_bytes, p):
    header = Header()
    header.id_0, p = read_byte(data_bytes, p)
    header.id_1, p = read_byte(data_bytes, p)
    header.id_2, p = read_byte(data_bytes, p)
    header.id_3, p = read_byte(data_bytes, p)
    header.format_version_0, p = read_byte(data_bytes, p)
    header.format_version_1, p = read_byte(data_bytes, p)
    header.format_version_2, p = read_byte(data_bytes, p)
    header.option, p = read_byte(data_bytes, p)

    header.width, p = read_int32(data_bytes, p)
    header.height, p = read_int32(data_bytes, p)
    header.frame_rate, p = read_int32(data_bytes, p)
    header.root_movie_id, p = read_int32(data_bytes, p)
    header.name_string_id, p = read_int32(data_bytes, p)
    header.background_color, p = read_int32(data_bytes, p)

    header.string_bytes, p = read_item_array(data_bytes, p)
    header.animation_bytes, p = read_item_array(data_bytes, p)
    header.translate, p = read_item_array(data_bytes, p)
    header.matrix, p = read_item_array(data_bytes, p)
    header.color, p = read_item_array(data_bytes, p)
    header.alpha_transform, p = read_item_array(data_bytes, p)
    header.color_transform, p = read_item_array(data_bytes, p)
    header.object_data, p = read_item_array(data_bytes, p)
    header.texture, p = read_item_array(data_bytes, p)
    header.texture_fragment, p = read_item_array(data_bytes, p)
    header.bitmap, p = read_item_array(data_bytes, p)
    header.bitmap_ex, p = read_item_array(data_bytes, p)
    header.font, p = read_item_array(data_bytes, p)
    header.text_property, p = read_item_array(data_bytes, p)
    header.text, p = read_item_array(data_bytes, p)
    header.particle_data, p = read_item_array(data_bytes, p)
    header.particle, p = read_item_array(data_bytes, p)
    header.program_object, p = read_item_array(data_bytes, p)
    header.graphic_object, p = read_item_array(data_bytes, p)
    header.graphic, p = read_item_array(data_bytes, p)
    header.animation, p = read_item_array(data_bytes, p)
    header.button_condition, p = read_item_array(data_bytes, p)
    header.button, p = read_item_array(data_bytes, p)
    header.label, p = read_item_array(data_bytes, p)
    header.instance_name, p = read_item_array(data_bytes, p)
    header.event_data, p = read_item_array(data_bytes, p)
    header.place, p = read_item_array(data_bytes, p)
    header.control_move_m, p = read_item_array(data_bytes, p)
    header.control_move_c, p = read_item_array(data_bytes, p)
    header.control_move_mc, p = read_item_array(data_bytes, p)
    header.control_move_mcb, p = read_item_array(data_bytes, p)
    header.control, p = read_item_array(data_bytes, p)
    header.frame, p = read_item_array(data_bytes, p)
    header.movie_clip_event, p = read_item_array(data_bytes, p)
    header.movie, p = read_item_array(data_bytes, p)
    header.movie_linkage, p = read_item_array(data_bytes, p)
    header.string_data, p = read_item_array(data_bytes, p)

    header.lwf_length, p = read_int32(data_bytes, p)
    return header, p


def read_header_compat(data_bytes, p):
    header_compat = HeaderCompat()
    header_compat.id_0, p = read_byte(data_bytes, p)
    header_compat.id_1, p = read_byte(data_bytes, p)
    header_compat.id_2, p = read_byte(data_bytes, p)
    header_compat.id_3, p = read_byte(data_bytes, p)
    header_compat.format_version_0, p = read_byte(data_bytes, p)
    header_compat.format_version_1, p = read_byte(data_bytes, p)
    header_compat.format_version_2, p = read_byte(data_bytes, p)
    header_compat.option, p = read_byte(data_bytes, p)

    header_compat.width, p = read_int32(data_bytes, p)
    header_compat.height, p = read_int32(data_bytes, p)
    header_compat.frame_rate, p = read_int32(data_bytes, p)
    header_compat.root_movie_id, p = read_int32(data_bytes, p)
    header_compat.name_string_id, p = read_int32(data_bytes, p)
    header_compat.background_color, p = read_int32(data_bytes, p)

    header_compat.string_bytes, p = read_item_array(data_bytes, p)
    header_compat.animation_bytes, p = read_item_array(data_bytes, p)
    header_compat.translate, p = read_item_array(data_bytes, p)
    header_compat.matrix, p = read_item_array(data_bytes, p)
    header_compat.color, p = read_item_array(data_bytes, p)
    header_compat.alpha_transform, p = read_item_array(data_bytes, p)
    header_compat.color_transform, p = read_item_array(data_bytes, p)
    header_compat.object_data, p = read_item_array(data_bytes, p)
    header_compat.texture, p = read_item_array(data_bytes, p)
    header_compat.texture_fragment, p = read_item_array(data_bytes, p)
    header_compat.bitmap, p = read_item_array(data_bytes, p)
    header_compat.bitmap_ex, p = read_item_array(data_bytes, p)
    header_compat.font, p = read_item_array(data_bytes, p)
    header_compat.text_property, p = read_item_array(data_bytes, p)
    header_compat.text, p = read_item_array(data_bytes, p)
    header_compat.particle_data, p = read_item_array(data_bytes, p)
    header_compat.particle, p = read_item_array(data_bytes, p)
    header_compat.program_object, p = read_item_array(data_bytes, p)
    header_compat.graphic_object, p = read_item_array(data_bytes, p)
    header_compat.graphic, p = read_item_array(data_bytes, p)
    header_compat.animation, p = read_item_array(data_bytes, p)
    header_compat.button_condition, p = read_item_array(data_bytes, p)
    header_compat.button, p = read_item_array(data_bytes, p)
    header_compat.label, p = read_item_array(data_bytes, p)
    header_compat.instance_name, p = read_item_array(data_bytes, p)
    header_compat.event_data, p = read_item_array(data_bytes, p)
    header_compat.place, p = read_item_array(data_bytes, p)
    header_compat.control_move_m, p = read_item_array(data_bytes, p)
    header_compat.control_move_c, p = read_item_array(data_bytes, p)
    header_compat.control_move_mc, p = read_item_array(data_bytes, p)
    header_compat.control, p = read_item_array(data_bytes, p)
    header_compat.frame, p = read_item_array(data_bytes, p)
    header_compat.movie_clip_event, p = read_item_array(data_bytes, p)
    header_compat.movie, p = read_item_array(data_bytes, p)
    header_compat.movie_linkage, p = read_item_array(data_bytes, p)
    header_compat.string_data, p = read_item_array(data_bytes, p)

    header_compat.lwf_length, p = read_int32(data_bytes, p)
    return header_compat, p


def read_array(data_bytes, p, info, read_item):
    if p != info.offset:
        raise Exception("Read Error")
    array = []
    for index in range(0, info.length):
        obj, p = read_item(data_bytes, p)
        array.append(obj)
    return array, p


def read_translate(data_bytes, p):
    translate = Translate()
    translate.translate_x, p = read_single(data_bytes, p)
    translate.translate_y, p = read_single(data_bytes, p)
    return translate, p


def read_matrix(data_bytes, p):
    matrix = Matrix()
    matrix.scale_x, p = read_single(data_bytes, p)
    # matrix.scale_x = round(matrix.scale_x, 6)
    matrix.scale_y, p = read_single(data_bytes, p)
    # matrix.scale_y = round(matrix.scale_y, 6)
    matrix.skew_0, p = read_single(data_bytes, p)
    # matrix.skew_0 = round(matrix.skew_0, 6)
    matrix.skew_1, p = read_single(data_bytes, p)
    # matrix.skew_1 = round(matrix.skew_1, 6)
    matrix.translate_x, p = read_single(data_bytes, p)
    # matrix.translate_x = round(matrix.translate_x, 6)
    matrix.translate_y, p = read_single(data_bytes, p)
    # matrix.translate_y = round(matrix.translate_y, 6)
    log(f'Read Matrix - {matrix}')
    return matrix, p


def read_color(data_bytes, p):
    color = Color()
    color.red, p = read_single(data_bytes, p)
    color.green, p = read_single(data_bytes, p)
    color.blue, p = read_single(data_bytes, p)
    color.alpha, p = read_single(data_bytes, p)
    return color, p


def read_alpha_transform(data_bytes, p):
    alpha_transform = AlphaTransform()
    alpha_transform.alpha, p = read_single(data_bytes, p)
    return alpha_transform, p


def read_color_transform(data_bytes, p):
    color_transform = ColorTransform()
    color_transform.multi, p = read_color(data_bytes, p)
    color_transform.add, p = read_color(data_bytes, p)
    return color_transform, p


def read_object(data_bytes, p):
    obj = Object()
    obj.object_type, p = read_int32(data_bytes, p)
    obj.object_id, p = read_int32(data_bytes, p)
    return obj, p


def read_texture(data_bytes, p):
    texture = Texture()
    texture.string_id, p = read_int32(data_bytes, p)
    texture.format, p = read_int32(data_bytes, p)
    texture.width, p = read_int32(data_bytes, p)
    texture.height, p = read_int32(data_bytes, p)
    texture.scale, p = read_single(data_bytes, p)
    return texture, p


def read_texture_fragment(data_bytes, p):
    texture_fragment = TextureFragment()
    texture_fragment.string_id, p = read_int32(data_bytes, p)
    texture_fragment.texture_id, p = read_int32(data_bytes, p)
    texture_fragment.rotated, p = read_int32(data_bytes, p)
    texture_fragment.x, p = read_int32(data_bytes, p)
    texture_fragment.y, p = read_int32(data_bytes, p)
    texture_fragment.u, p = read_int32(data_bytes, p)
    texture_fragment.v, p = read_int32(data_bytes, p)
    texture_fragment.w, p = read_int32(data_bytes, p)
    texture_fragment.h, p = read_int32(data_bytes, p)
    texture_fragment.ow, p = read_int32(data_bytes, p)
    texture_fragment.oh, p = read_int32(data_bytes, p)
    return texture_fragment, p


def read_texture_fragment_compat(data_bytes, p):
    texture_fragment_compat = TextureFragmentCompat()
    texture_fragment_compat.string_id, p = read_int32(data_bytes, p)
    texture_fragment_compat.texture_id, p = read_int32(data_bytes, p)
    texture_fragment_compat.rotated, p = read_int32(data_bytes, p)
    texture_fragment_compat.x, p = read_int32(data_bytes, p)
    texture_fragment_compat.y, p = read_int32(data_bytes, p)
    texture_fragment_compat.u, p = read_int32(data_bytes, p)
    texture_fragment_compat.v, p = read_int32(data_bytes, p)
    texture_fragment_compat.w, p = read_int32(data_bytes, p)
    texture_fragment_compat.h, p = read_int32(data_bytes, p)
    return texture_fragment_compat, p


def read_bitmap(data_bytes, p):
    bitmap = Bitmap()
    bitmap.matrix_id, p = read_int32(data_bytes, p)
    bitmap.texture_fragment_id, p = read_int32(data_bytes, p)
    return bitmap, p


def read_bitmap_ex(data_bytes, p):
    bitmap_ex = BitmapEx()
    bitmap_ex.matrix_id, p = read_int32(data_bytes, p)
    bitmap_ex.texture_fragment_id, p = read_int32(data_bytes, p)
    bitmap_ex.attribute, p = read_int32(data_bytes, p)
    bitmap_ex.u, p = read_single(data_bytes, p)
    bitmap_ex.v, p = read_single(data_bytes, p)
    bitmap_ex.w, p = read_single(data_bytes, p)
    bitmap_ex.h, p = read_single(data_bytes, p)
    return bitmap_ex, p


def read_font(data_bytes, p):
    font = Font()
    font.string_id, p = read_int32(data_bytes, p)
    font.letter_spacing, p = read_single(data_bytes, p)
    return font, p


def read_text_property(data_bytes, p):
    text_property = TextProperty()
    text_property.max_length, p = read_int32(data_bytes, p)
    text_property.font_id, p = read_int32(data_bytes, p)
    text_property.font_height, p = read_int32(data_bytes, p)
    text_property.align, p = read_int32(data_bytes, p)
    text_property.left_margin, p = read_int32(data_bytes, p)
    text_property.right_margin, p = read_int32(data_bytes, p)
    text_property.letter_spacing, p = read_single(data_bytes, p)
    text_property.leading, p = read_int32(data_bytes, p)
    text_property.stroke_color_id, p = read_int32(data_bytes, p)
    text_property.stroke_width, p = read_int32(data_bytes, p)
    text_property.shadow_color_id, p = read_int32(data_bytes, p)
    text_property.shadow_offset_x, p = read_int32(data_bytes, p)
    text_property.shadow_offset_y, p = read_int32(data_bytes, p)
    text_property.shadow_blur, p = read_int32(data_bytes, p)
    return text_property, p


def read_text(data_bytes, p):
    text = Text()
    text.matrix_id, p = read_int32(data_bytes, p)
    text.name_string_id, p = read_int32(data_bytes, p)
    text.text_property_id, p = read_int32(data_bytes, p)
    text.string_id, p = read_int32(data_bytes, p)
    text.color_id, p = read_int32(data_bytes, p)
    text.width, p = read_int32(data_bytes, p)
    text.height, p = read_int32(data_bytes, p)
    return text, p


def read_particle_data(data_bytes, p):
    particle_data = ParticleData()
    particle_data.string_id, p = read_int32(data_bytes, p)
    return particle_data, p


def read_particle(data_bytes, p):
    particle = Particle()
    particle.matrix_id, p = read_int32(data_bytes, p)
    particle.color_transform_id, p = read_int32(data_bytes, p)
    particle.particle_data_id, p = read_int32(data_bytes, p)
    return particle, p


def read_program_object(data_bytes, p):
    program_object = ProgramObject()
    program_object.string_id, p = read_int32(data_bytes, p)
    program_object.width, p = read_int32(data_bytes, p)
    program_object.height, p = read_int32(data_bytes, p)
    program_object.matrix_id, p = read_int32(data_bytes, p)
    program_object.color_transform_id, p = read_int32(data_bytes, p)
    return program_object, p


def read_graphic_object(data_bytes, p):
    graphic_object = GraphicObject()
    graphic_object.graphic_object_type, p = read_int32(data_bytes, p)
    graphic_object.graphic_object_id, p = read_int32(data_bytes, p)
    return graphic_object, p


def read_graphic(data_bytes, p):
    graphic = Graphic()
    graphic.graphic_object_id, p = read_int32(data_bytes, p)
    graphic.graphic_objects, p = read_int32(data_bytes, p)
    return graphic, p


def read_animation_data(data_bytes, p):
    animation_data = Animation()
    animation_data.animation_offset, p = read_int32(data_bytes, p)
    animation_data.animation_length, p = read_int32(data_bytes, p)
    return animation_data, p


def read_button_condition(data_bytes, p):
    button_condition = ButtonCondition()
    button_condition.condition, p = read_int32(data_bytes, p)
    button_condition.key_code, p = read_int32(data_bytes, p)
    button_condition.animation_id, p = read_int32(data_bytes, p)
    return button_condition, p


def read_button(data_bytes, p):
    button = Button()
    button.width, p = read_int32(data_bytes, p)
    button.height, p = read_int32(data_bytes, p)
    button.matrix_id, p = read_int32(data_bytes, p)
    button.color_transform_id, p = read_int32(data_bytes, p)
    button.condition_id, p = read_int32(data_bytes, p)
    button.conditions, p = read_int32(data_bytes, p)
    return button, p


def read_label(data_bytes, p):
    label = Label()
    label.string_id, p = read_int32(data_bytes, p)
    label.frame_no, p = read_int32(data_bytes, p)
    return label, p


def read_instance_name(data_bytes, p):
    instance_name = InstanceName()
    instance_name.string_id, p = read_int32(data_bytes, p)
    return instance_name, p


def read_event(data_bytes, p):
    event = Event()
    event.string_id, p = read_int32(data_bytes, p)
    return event, p


def read_place_compat(data_bytes, p):
    place_compat = PlaceCompat()
    place_compat.depth, p = read_int32(data_bytes, p)
    place_compat.object_id, p = read_int32(data_bytes, p)
    place_compat.instance_id, p = read_int32(data_bytes, p)
    place_compat.matrix_id, p = read_int32(data_bytes, p)
    return place_compat, p


def read_control_move_m(data_bytes, p):
    control_move_m = ControlMoveM()
    control_move_m.place_id, p = read_int32(data_bytes, p)
    control_move_m.matrix_id, p = read_int32(data_bytes, p)
    return control_move_m, p


def read_control_move_c(data_bytes, p):
    control_move_c = ControlMoveC()
    control_move_c.place_id, p = read_int32(data_bytes, p)
    control_move_c.color_transform_id, p = read_int32(data_bytes, p)
    return control_move_c, p


def read_control_move_mc(data_bytes, p):
    control_move_mc = ControlMoveMC()
    control_move_mc.place_id, p = read_int32(data_bytes, p)
    control_move_mc.matrix_id, p = read_int32(data_bytes, p)
    control_move_mc.color_transform_id, p = read_int32(data_bytes, p)
    return control_move_mc, p


def read_control_move_mcb(data_bytes, p):
    control_move_mcb = ControlMoveMCB()
    control_move_mcb.place_id, p = read_int32(data_bytes, p)
    control_move_mcb.matrix_id, p = read_int32(data_bytes, p)
    control_move_mcb.color_transform_id, p = read_int32(data_bytes, p)
    control_move_mcb.blend_mode, p = read_int32(data_bytes, p)
    return control_move_mcb, p


def read_control(data_bytes, p):
    control = Control()
    control.control_type, p = read_int32(data_bytes, p)
    control.control_id, p = read_int32(data_bytes, p)
    return control, p


def read_frame(data_bytes, p):
    frame = Frame()
    frame.control_offset, p = read_int32(data_bytes, p)
    frame.controls, p = read_int32(data_bytes, p)
    return frame, p


def read_movie_clip_event(data_bytes, p):
    movie_clip_event = MovieClipEvent()
    movie_clip_event.clip_event, p = read_int32(data_bytes, p)
    movie_clip_event.animation_id, p = read_int32(data_bytes, p)
    return movie_clip_event, p


def read_movie(data_bytes, p):
    movie = Movie()
    movie.depths, p = read_int32(data_bytes, p)
    movie.label_offset, p = read_int32(data_bytes, p)
    movie.labels, p = read_int32(data_bytes, p)
    movie.frame_offset, p = read_int32(data_bytes, p)
    movie.frames, p = read_int32(data_bytes, p)
    movie.clip_event_id, p = read_int32(data_bytes, p)
    movie.clip_events, p = read_int32(data_bytes, p)
    return movie, p


def read_movie_linkage(data_bytes, p):
    movie_linkage = MovieLinkage()
    movie_linkage.string_id, p = read_int32(data_bytes, p)
    movie_linkage.movie_id, p = read_int32(data_bytes, p)
    return movie_linkage, p


def read_string_data(data_bytes, p):
    string_data = String()
    string_data.string_offset, p = read_int32(data_bytes, p)
    string_data.string_length, p = read_int32(data_bytes, p)
    return string_data, p


def read_string(string_byte_data, string_data):
    return string_byte_data[string_data.string_offset:string_data.string_offset+string_data.string_length].decode('utf-8')


def read_animation(animation_byte_data, animation_data):
    p = animation_data.animation_offset
    end = p + animation_data.animation_length

    array = []
    while True:
        if p >= end:
            return array
        code, p = read_byte(animation_byte_data, p)
        array.append(int(code))

        if code == Anim.PLAY or code == Anim.STOP or code == Anim.NEXT_FRAME or code == Anim.PREV_FRAME:
            pass
        elif code == Anim.GOTO_FRAME or code == Anim.GOTO_LABEL or code == Anim.EVENT or code == Anim.CALL:
            target, p = read_int32(animation_byte_data, p)
            array.append(target)
            continue
        elif code == Anim.SET_TARGET:
            count, p = read_int32(animation_byte_data, p)
            array.append(count)
            for i in range(0, int(count)):
                target, p = read_int32(animation_byte_data, p)
                array.append(target)
            continue
        elif code == Anim.END:
            return array
