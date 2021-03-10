from refs import Refs


def load_screen_chunk(loader, program_type, filename, callbacks):
    Refs.gc.initialize(loader)
    Refs.gc.setup_parties()

    if loader.get('save') is None:
        oc = []
        oca = []
        ocs = []
        if program_type == 'test':
            for char in Refs.gc['chars'][20:]:
                index = char.get_index()
                oc.append(index)
                if char.is_support():
                    ocs.append(index)
                else:
                    oca.append(index)
        Refs.gc.load_parties(oc, oca, ocs, None)
        Refs.gc.create_empty_parties()
    else:
        save = loader.get('save')
        oc = save['obtained_characters']
        oca = save['obtained_characters_a']
        ocs = save['obtained_characters_s']
        cp = save['parties']
        chars = list(loader.get('chars').values())
        for p in range(10):  # Each party
            for c in range(16):  # Each Char
                if cp[p + 1][c] is not None:
                    cp[p + 1][c] = chars[cp[p + 1][c]]
        Refs.gc.load_parties(oc, oca, ocs, cp)
        Refs.gc.update_data(save)

    if Refs.gs is not None:
        Refs.gs.make_screens()
    for callback in callbacks:
        if callback is not None:
            callback()
