""" This hook is written to correct a bug in PySide2.
See: https://github.com/pyinstaller/pyinstaller/issues/4040#issuecomment-465736128
It loads the shiboken2 source files to the application created by PyInstaller."""

from PyInstaller.utils.hooks import collect_data_files

datas = [ ('virtualenv/Lib/site-packages/shiboken2/support', 'support') ] 
# TODO Find a way to use the collect_data_files function to achieve the above
# datas = collect_data_files('shiboken2', include_py_files=True, subdir='support')