# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['local_network_share.py'],
             pathex=['C:\\Users\\chao\\Documents\\PROJECTS\\python\\局域网文字共享'],
             binaries=[],
             datas=[('./config.py', '.'),('./share.ico', '.'),
                    ('public', 'public'),('copypaste/templates', 'copypaste/templates')],
             hiddenimports=['pecan'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PIL','numpy'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='局域网文本共享',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          icon='share.ico',
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               icon='share.ico',
               upx=True,
               upx_exclude=[],
               name='局域网文本共享')
