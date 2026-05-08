# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['Sysmox.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='sysmox',
    debug=False,
    strip=False,
    upx=False,
    console=True,
)