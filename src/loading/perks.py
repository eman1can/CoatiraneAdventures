from game.skill_tree_perk import Perk


def load_perk_chunk(chunk, loader, program_type, callbacks):
    perk_info, requirements, description = chunk.split('\n', 2)
    perk_id, name, tree, level = perk_info.split(', ')
    required_perks_list = requirements.split('#')

    perk = Perk(perk_id, name, tree, level, description, required_perks_list)

    loader.append('perks', perk_id, perk)
    for callback in callbacks:
        if callback is not None:
            callback()
