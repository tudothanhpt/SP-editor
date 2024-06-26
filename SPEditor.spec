# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\sp_editor\\main.py'],
    pathex=[],
    binaries=[],
    datas=[("src\\sp_editor\\database\\material_table\\*.json","sp_editor\\database\\material_table"),("src\\sp_editor\\database\\barset_table\\*.json","sp_editor\\database\\barset_table")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SPEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=["SP-EDITOR.ico"],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
