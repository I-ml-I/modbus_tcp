import os
import shutil

from pynt import task
from pyside2uic import compileUiDir


ui_folder = os.path.join('app', 'ui')
compiled_ui_folder = os.path.join('app', 'compiled_ui')


@task()
def compile_ui():
    ''' compile ui files '''

    compileUiDir(ui_folder, recurse=True)


@task(compile_ui)
def move_compiled_ui():
    ''' move compiled .py files '''

    ui_files = os.listdir(ui_folder)
    for file in ui_files:
        if(file.endswith('.py')):
            shutil.move(os.path.join(ui_folder ,file), os.path.join(compiled_ui_folder, file))

@task(move_compiled_ui)
def build():
    ''' build .py files '''
    import os
    import subprocess

    # TODO add os check
    subprocess.run([
        'python', '-OO', '-m', 'PyInstaller',  # set __debug__ to false and removing docstrings
        'app\\main.spec',  # entry script
        '--log-level=CRITICAL',  # pyinstaller progress log
        '--onefile', '-y', '--distpath=tmp/dist', '--workpath=tmp/build'
#        'pyinstaller', '--onefile', '--add-data', 'modbus_tcp/licenses/*.txt;licenses/', 'main.py'
    ])


__DEFAULT__ = build
