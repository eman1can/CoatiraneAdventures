from refs import Refs


def profile_header():
    name = Refs.gc.get_name()
    domain = Refs.gc.get_domain()
    skill_level = Refs.gc.get_skill_level()

    return f'{name} - {domain} - Perks Unlocked {skill_level}'


def time_header():
    time = Refs.gc.get_time()
    renown = Refs.gc.get_renown()
    varenth = Refs.gc.format_number(int(Refs.gc.get_varenth()))

    if Refs.gc.get_inventory().has_item('pocket_watch'):
        header = f'{time} - {varenth} Varenth - Renown {renown}'
    else:
        header = f'{varenth} Varenth - Renown {renown}'
    return header


def time_header_simple():
    return str(Refs.gc.get_time())


def dungeon_header(direction=None):
    if direction is not None and Refs.gc.get_inventory().has_item('compass'):
        text = {-1: 'You are lost!', 0: 'West', 1: 'South', 2: 'North', 3: 'East'}[direction]
        return f'Currently Facing: {text}'
    return ''
