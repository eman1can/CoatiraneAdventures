import os

files = ['../../text_main.py']

imports = []

while len(files) > 0:
    file_name = files.pop()
    print('Search', file_name)
    file = open(file_name, 'r', encoding='utf-8')
    for line in file:
        if line.startswith('from'):
            module, import_list = line[5:-1].split(' import ')
            if '#' in import_list:
                import_list = import_list[:import_list.index('#')].strip()
            if os.path.exists('../../src/' + module.replace('.', '/') + '.py'):
                files.append('../../src/' + module.replace('.', '/') + '.py')
            else:
                if module not in imports:
                    imports.append(module)
        if line.startswith('import'):
            import_list = line[6:].strip()
            for import_name in import_list.split(', '):
                if import_name not in imports:
                    imports.append(import_name)
            # print('\t', import_list)
    file.close()
imports.sort()
for import_name in imports:
    print('\'' + import_name + '\'', end=', ')
