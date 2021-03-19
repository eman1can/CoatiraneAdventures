def load_crafting_recipe_chunk(chunk, loader, program_type, callbacks):

    for callback in callbacks:
        if callback is not None:
            callback()
