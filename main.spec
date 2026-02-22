# -*- mode: python ; coding: utf-8 -*-
import sys

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('BOTBOSS.png', '.'), ('BOTBOSS_LOGO.png', '.')],
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
    name='BOTBOSS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='BOTBOSS_LOGO.ico' if sys.platform == 'win32' else None,
)

# สำหรับ macOS: สร้าง .app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='BOTBOSS.app',
        icon='BOTBOSS_LOGO.icns' if os.path.exists('BOTBOSS_LOGO.icns') else None,
        bundle_identifier='com.botboss.app',
        info_plist={
            'CFBundleName': 'BOTBOSS',
            'CFBundleDisplayName': 'BOTBOSS',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': 'True',
        },
    )
