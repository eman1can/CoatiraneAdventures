from game.equipment import ToolClass, WeaponClass, ArmorClass, EQUIPMENT_TOOL, EQUIPMENT_WEAPON, EQUIPMENT_ARMOR


def load_equipment_chunk(chunk, loader, program_type, callbacks):
    equipment_type = int(chunk[0])
    equipment_id, equipment = None, None
    if equipment_type == EQUIPMENT_TOOL:
        metadata, description = chunk.split('\n')
        equipment_id, name, tool_type = metadata.split(', ')[1:]
        equipment = ToolClass(equipment_id, name, int(tool_type), description, 1.0)
    elif equipment_type == EQUIPMENT_WEAPON:
        metadata, description, weights = chunk.split('\n')
        equipment_id, name, weapon_type = metadata.split(', ')[1:]
        weight_values = []
        for weight in weights.split(','):
            weight_values.append(float(weight))
        equipment = WeaponClass(equipment_id, name, int(weapon_type), description, weight_values)
    elif equipment_type == EQUIPMENT_ARMOR:
        metadata, description, weights = chunk.split('\n')
        equipment_id, name, armor_type = metadata.split(', ')[1:]
        weight_values = []
        for weight in weights.split(', '):
            weight_values.append(float(weight))
        equipment = ArmorClass(equipment_id, name, int(armor_type), description, weight_values)

    loader.append('equipment', equipment_id, equipment)

    for callback in callbacks:
        if callback is not None:
            callback()
