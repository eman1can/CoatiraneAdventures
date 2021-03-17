from game.housing import Housing


def load_housing_chunk(chunk, loader, program_type, callbacks):
    lines = chunk.strip().split('\n')
    identifier, name, limit, cost = lines[0].split(', ')
    description = lines[1]
    for line in lines[2:-1]:
        description += '\n' + line
    features, installed_features = lines[-1].split('#')

    if features == 'none':
        features_array = []
    elif ',' in features:
        features_array = features.split(', ')
    else:
        features_array = [features]

    if installed_features == 'none':
        installed_features_array = []
    elif ',' in installed_features:
        installed_features_array = installed_features.split(', ')
    else:
        installed_features_array = [installed_features]

    housing = Housing(identifier, name, description, int(limit), features_array, installed_features_array, int(cost))
    loader.append('housing', identifier, housing)

    for callback in callbacks:
        if callback is not None:
            callback()
    return None
