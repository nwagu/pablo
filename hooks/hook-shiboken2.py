from PyInstaller.utils.hooks import collect_data_files

datas = [ ('virtualenv/Lib/site-packages/shiboken2/support/*', 'support'),
        ('virtualenv/Lib/site-packages/PySide2/support/*', 'support') ]