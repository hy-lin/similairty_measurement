# -*- mode: python -*-

block_cipher = None


a = Analysis(['Experiment.py'],
             pathex=['D:\\Users\\Hsuan-Yu Lin\\Documents\\GitHub\\similairty_measurement\\Experiments\\Experiment 1\\src'],
             binaries=None,
             datas=[('resources', 'resources'), 
			('sdl_dll', 'sdl_dll')
			 ],
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
          name='Experiment',
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
               name='Experiment')
