from os import environ, getcwd, listdir, path
import traceback
from subprocess import CalledProcessError, call, check_output
import sys

if hasattr(sys, '_MEIPASS'):
    base_path = path.join(sys._MEIPASS)
else:
    base_path = getcwd()

environ['CA_PATH'] = base_path
if 'PYTHONPATH' in environ:
    environ['PYTHONPATH'] += f'{base_path};{base_path}\\src;'
else:
    environ['PYTHONPATH'] = f'{base_path};{base_path}\\src;'
environ['KIVY_HOME'] = base_path + '/data/'

launcher = f'python "{base_path}\\launcher.py"'
game = f'python "{base_path}\\main.py"'
crash_reporter = f'python "{base_path}\\crash_reporter.py"'

print(launcher)
print(game)
print(crash_reporter)

while True:
    try:
        check_output(launcher)
        path = base_path[:base_path.rindex('\\')]

        try:
            check_output(game)
            quit(0)
        except CalledProcessError as e:
            log_path = f'{base_path}\\data\\logs'
            files = []
            for file in listdir(log_path):
                # year, month, day, index =
                print(file)
                files.append((*file[20:28].split('-'), int(file[29:-4])))
            file = max(*files)

            log_file = f'"{log_path}\\coatiraneadventures_{file[0]}-{file[1]}-{file[2]}_{file[3]}.txt"'

            print(crash_reporter, log_file)
            print(getcwd())
            check_output(f'{crash_reporter} {log_file}')
    except CalledProcessError:
        quit(0)
