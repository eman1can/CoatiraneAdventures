from game.save_load import load_game
from refs import Refs


def load_save_chunk(loader, program_type, filename, callbacks):
    save_info = load_game(int(filename))
    loader.set('save', save_info)
    Refs.gc.initialize(loader)
    Refs.gc.update_data(save_info)

    for callback in callbacks:
        if callback is not None:
            callback()
