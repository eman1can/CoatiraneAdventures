from game.effect import parse_effect
from game.material import Material


def parse_effect_string(effect_string):
    effect_definition, description = effect_string.split('#')
    effect = parse_effect(0, effect_definition.split('*'))
    return effect, description


def parse_effects(full_effect_string):
    effects = []
    if full_effect_string == 'none':
        return effects
    for effect_string in full_effect_string.split(','):
        material_effect = parse_effect_string(effect_string)
        effects.append(material_effect)
    return effects


def load_material_chunk(chunk, loader, program_type, callbacks):
    info_string, format_string, defining_effect, sub_effect, values_string = chunk.split('\n')
    material_type, identifier, name, min_hardness, max_hardness = info_string.split(', ')
    raw_form, processed_form = format_string.split('#')
    material_values = values_string.split(', ')
    for x in range(len(material_values)):
        material_values[x] = int(material_values[x])

    defining_effects = parse_effects(defining_effect)
    sub_effects = parse_effects(sub_effect)

    material = Material(int(material_type), identifier, name, min_hardness, max_hardness, raw_form, processed_form, defining_effects, sub_effects, material_values)
    loader.append('materials', identifier, material)

    for callback in callbacks:
        if callback is not None:
            callback()
