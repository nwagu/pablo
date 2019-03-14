# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
        ('files', 'files'),
        ('themes', 'themes'),
        ('images', 'images')
         ]

a = Analysis(['pablo.py'],
        pathex=['C:\\Users\\cn\\Desktop\\Pablo', 'C:\\Users\\cn\\Desktop\\Pablo\\virtualenv\\Lib\\site-packages\\shiboken2'],
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
        Tree('files', prefix='files'),
        Tree('images', prefix='images'),
        Tree('themes', prefix='themes'),
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        name='pablo',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=True )
