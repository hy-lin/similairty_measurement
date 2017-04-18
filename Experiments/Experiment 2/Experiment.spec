# -*- mode: python -*-

block_cipher = None


a = Analysis(['src\\Experiment.py'],
             pathex=['C:\\Users\\Hsuan-Yu Lin\\Documents\\GitHub\\similairty_measurement\\Experiments\\Experiment 2'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Experiment',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='src\\resources\\uzh.ico')
