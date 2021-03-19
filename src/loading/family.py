from game.domain import Domain


def load_family_chunk(chunk, loader, program_type, callbacks):
    # Need to flush out WHAT a family actually is before this will take shape.
    # Will most likely be families of friends that this person has encountered?
    #   That data would be better kept in a database though.
    # Might change to take over domains. Domains need to be loaded before load though and not in a loaded save. So probably not.
    for callback in callbacks:
        if callback is not None:
            callback()
    return None


def load_domains(program_type):
    file_string = ""
    with open(f'data/{program_type}/Domains.txt', 'r') as file:
        for line in file:
            file_string += line
    domains = []
    domain_data = file_string.split('-\n')
    for domain in domain_data:
        name, description, small_description = domain.split('~\n')
        domains.append(Domain(name.strip(), description.strip(), small_description.strip()))
    return domains
