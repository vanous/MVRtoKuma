# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.building.build_main import EXE
# (other imports like Analysis, PYZ, etc.)

if sys.platform.startswith('win'):
    exe_name = 'uk_mvr_windows'
elif sys.platform.startswith('linux'):
    exe_name = 'uk_mvr_linux'
else:
    exe_name = 'uk_mvr'

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[('tui/*.css', 'tui')],
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
    a.binaries,
    a.datas,
    [],
    name='uk_mvr_linux',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
