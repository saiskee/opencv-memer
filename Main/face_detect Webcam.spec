# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/khurana/Desktop/Memify/Main/face_detect_Webcam.py'],
             pathex=['/Users/khurana/Downloads/PyInstaller-3.1.1/face_detect_Webcam'],
             binaries=None,
             datas=[('/Users/khurana/Desktop/Memify/Main/*.xml', '.'),
             ('/Users/khurana/Desktop/Memify/Main/*.png','.'),
             ('/Users/khurana/Desktop/Memify/Main/*.mp4','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Memify',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Memify')
