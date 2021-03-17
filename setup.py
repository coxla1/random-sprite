import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    'includes': ['sprites', 'utils'],
    'excludes': ['mkl', 'babel', 'matplotlib', 'Cython', 'numpy', 'pandas', 'PySide2', 'PyQt5'],
    'zip_include_packages': ['*'],
    'zip_exclude_packages': ['pyz3r', 'random' ,'os', 'shutil', 'tkinter', 'threading', 'json', 'asyncio', 'webbrowser', 'PIL', 'urllib.request', 'io'],
    'include_files': [('data/icon.ico', 'data/icon.ico'), ('data/sprites.txt', 'data/sprites.txt'), ('data/version.txt', 'data/version.txt')],
    'optimize': 2,
    }

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(  name = 'Seed downloader',
        version = '1.0',
        description = 'Tool to download seeds and use weighted random sprites',
        options = {'build_exe': build_exe_options},
        executables = [Executable('gui.py', base=base, icon='data/icon.ico', target_name='Downloader')])