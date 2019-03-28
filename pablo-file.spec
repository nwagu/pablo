# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['src/main.py'],
        pathex=['C:\\Users\\cn\\Desktop\\Pablo\\src', 'C:\\Users\\cn\\Desktop\\Pablo\\virtualenv\\Lib\\site-packages\\shiboken2'],
        binaries = [],
        datas = [],
        hiddenimports=['typing', 'inspect'],
        hookspath=['hooks'],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher,
        noarchive=False)


pyz = PYZ(a.pure, 
        a.zipped_data,
        cipher=block_cipher)

exe = EXE(pyz,
        Tree('src/files', prefix='src/files'),
        Tree('src/images', prefix='src/images'),
        Tree('src/themes', prefix='src/themes'),
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        name='pablo',
        debug=True,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=True,
        icon='src/images/icon.ico',
        version='version.txt')
