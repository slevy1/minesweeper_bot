import os
import shutil
import sys
from cx_Freeze import setup, Executable
from pathlib import Path

#   os.environ['TCL_LIBRARY'] = r'C:\bin\Python37-32\tcl\tcl8.6'
#os.environ['TK_LIBRARY'] = r'C:\bin\Python37-32\tcl\tk8.6'


__version__ = '1.0.0'
base = None  # to take input()
#if sys.platform == 'win32':
#    base = 'Win32GUI'

gecko_driver = Path('./geckodriver.exe')


include_files = ['geckodriver.exe']
includes = []
excludes = []
packages = ['random', 'splinter', 'time', 'json', 'selenium', 'typing', 'operator', 'datetime']

build_exe_options = {'build_exe': {
        'packages': packages,
        'includes': includes,
        'include_files': include_files,
        'include_msvcr': False,
        'excludes': excludes
    }}

bdist_msi_options = {
    'bdist_msi': {
        #'upgrade_code': "{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}",
        'add_to_path': True,
        #'environment_variables': [
        #    ("E_MYAPP_VAR", "=-*MYAPP_VAR", "1", "TARGETDIR")
        #]
    }
}

setup(
    name='MineSweeperBot',
    description='A bot that plays minesweeper on minesweeperonline.com',
    version=__version__,
    executables=[Executable('main.py', base=base)],
    options=build_exe_options
)

#path = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
#build_path = os.path.join(path, 'build', 'bdist.win-amd64')
#shutil.copy(str(gecko_driver.resolve()), build_path)
#shutil.copy(r'C:\bin\Python37-32\DLLs\tk86t.dll', build_path)

"""Any then one can either run python setup.py build_exe to generate an executable 
or python setup.py bdist_msi to generate an installer.

https://cx-freeze.readthedocs.io/en/latest/distutils.html


"""