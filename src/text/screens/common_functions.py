from math import ceil

from refs import END_OPT_C, OPT_C


def get_plain_size(string):
    parts = string.split('[')
    size = 0
    for part in parts:
        if ']' in part:
            size += len(part.split(']')[1])
        else:
            size += len(part)
    return size


def center(string, length, size):
    count = size - length
    for x in range(count):
        if x % 2 == 0:
            string += ' '
        else:
            string = ' ' + string
    return string


def ljust(string, length, size):
    count = size - length
    for x in range(count):
        string += ' '
    return string


def rjust(string, length, size):
    count = size - length
    for x in range(count):
        string = ' ' + string
    return string


def item_page_list(option_index, page_name, page_num, item_list, fail_text, current_text, item_string_function, page_num_first=True, size_check=5):
    display_text, _options = '', {}

    arrow_text = ''
    if len(item_list) > size_check:
        # We want to enable pages of items...
        left = page_num != 0
        right = page_num != ceil(len(item_list) / size_check) - 1

        left_string = f'{OPT_C}{option_index}{END_OPT_C} Prev Page'
        right_string = f'Next Page {OPT_C}{option_index + 1}{END_OPT_C}'

        if left:
            if page_num_first:
                _options[str(option_index)] = f'{page_name}:{page_num - 1}'
            else:
                _options[str(option_index)] = f'{page_name}#{page_num - 1}'
        else:
            left_string = f'[s]{left_string}[/s]'

        if right:
            if page_num_first:
                _options[str(option_index + 1)] = f'{page_name}:{page_num + 1}'
            else:
                _options[str(option_index + 1)] = f'{page_name}#{page_num + 1}'
        else:
            right_string = f'[s]{right_string}[/s]'

        arrow_text = f'\n\t←──── {left_string} | {right_string} ────→'

        item_list = item_list[page_num * size_check:(page_num + 1) * size_check]
        option_index = page_num * size_check + 2 + option_index
    elif len(item_list) == 0:
        display_text += fail_text

    for item in item_list:
        item_text, item_option = item_string_function(item, option_index, current_text, page_name, page_num)

        display_text += item_text
        if item_option is not None:
            if isinstance(item_option, dict):
                _options.update(item_option)
                option_index += len(item_option)
            else:
                _options[str(option_index)] = item_option
                option_index += 1
    display_text += arrow_text
    return display_text, _options
