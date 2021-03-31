def get_screen(console, screen_data):
    display_text = '\n\tLOADING GAME DATA\n'

    def display_progress_bar(current, maximum):
        if current > maximum:
            current = maximum
        string = '['
        width = int(console.get_width() * 0.65)
        for x in range(int(width / maximum * current)):
            string += '='
        for x in range(int(width / maximum * current), width):
            string += ' '
        return string + f'] {current} / {maximum}'

    for bar_name, bar_values in console.loading_progress.items():
        display_text += '\n\t' + display_progress_bar(*bar_values) + ' ' + bar_name
    display_text += '\n'
    return display_text, None
