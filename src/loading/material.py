from game.material import Material


def load_material_chunk(chunk, loader, program_type, callbacks):
    info_string, format_string, defining_effect, sub_effect = chunk.split('\n')
    material_type, identifier, name, min_hardness, max_hardness = info_string.split(', ')
    raw_form, processed_form = format_string.split('#')

    material = Material(material_type, identifier, name, min_hardness, max_hardness, raw_form, processed_form, defining_effect, sub_effect)
    loader.append('materials', identifier, material)

    for callback in callbacks:
        if callback is not None:
            callback()
