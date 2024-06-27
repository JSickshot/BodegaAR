from cx_Freeze import setup, Executable
import os

base = None
if os.name == 'nt':
    base = 'Win32GUI'

executables = [
    Executable('main.py', base=base, icon='ar.ico')
]

includefiles = ['pos.db']

options = {
    'build_exe': {
        'include_files': includefiles,
    }
}

setup(
    name='Nombre de tu aplicación',
    version='1.0',
    description='Descripción de tu aplicación',
    options=options,
    executables=executables
)
