import os
import shutil

from pynt import task
from pyside2uic import compileUiDir


ui_folder = os.path.join('modbus_tcp', 'ui')
compiled_ui_folder = os.path.join('modbus_tcp')


@task()
def compile_ui():
    ''' compile ui files '''

    compileUiDir(compiled_ui_folder, recurse=True)


@task(compile_ui)
def move_compiled_ui():
    ''' move compiled .py files '''

    ui_files = os.listdir(ui_folder)
    for file in ui_files:
        if(file.endswith('.py')):
            shutil.move(os.path.join(ui_folder ,file), os.path.join(compiled_ui_folder, file))


__DEFAULT__ = move_compiled_ui
