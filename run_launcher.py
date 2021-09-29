from os import environ, getcwd, listdir
from subprocess import CalledProcessError, check_output
import sys

base_path = getcwd()
if 'exe' in sys.argv[0]:
    launcher = f'"{base_path}\\Launcher.exe"'
    game = f'"{base_path}\\Game.exe"'
    crash_reporter = f'"{base_path}\\Crash Reporter.exe"'
else:
    launcher = f'python "{base_path}\\launcher.py"'
    game = f'python "{base_path}\\main.py"'
    crash_reporter = f'python "{base_path}\\crash_reporter.py"'

# Add src to python path
base_path = getcwd()
sys.path.insert(0, f'{base_path}\\src')
sys.path.insert(0, f'{base_path}\\res')
environ['KIVY_HOME'] = f'{base_path}\\data'

# data_path = expanduser('~\\Saved Games\\Coatirane Adventures\\')

while True:
    try:
        check_output(launcher)
        path = base_path[:base_path.rindex('\\')]

        try:
            check_output(game)
            sys.exit(0)
        except CalledProcessError as e:
            log_path = f'{base_path}\\data\\logs'
            files = []
            for file in listdir(log_path):
                files.append((*file[20:28].split('-'), int(file[29:-4])))
            file = max(*files)

            log_file = f'"{log_path}\\coatiraneadventures_{file[0]}-{file[1]}-{file[2]}_{file[3]}.txt"'

            check_output(f'{crash_reporter} {log_file}')
    except CalledProcessError:
        sys.exit(0)
