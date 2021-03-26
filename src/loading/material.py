from game.material import Material


def load_material_chunk(chunk, loader, program_type, callbacks):
    info_string, format_string, defining_effect, sub_effect, values_string = chunk.split('\n')
    material_type, identifier, name, min_hardness, max_hardness = info_string.split(', ')
    raw_form, processed_form = format_string.split('#')
    material_values = values_string.split(', ')
    for x in range(len(material_values)):
        material_values[x] = int(material_values[x])

    material = Material(int(material_type), identifier, name, min_hardness, max_hardness, raw_form, processed_form, defining_effect, sub_effect, material_values)
    loader.append('materials', identifier, material)

    for callback in callbacks:
        if callback is not None:
            callback()
