# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_data_files

block_cipher = None

BASE_DIR = os.path.abspath(SPECPATH if 'SPECPATH' in globals() else os.getcwd())

datas = [
    (os.path.join(BASE_DIR, 'ui', 'desktop', 'index.html'), os.path.join('ui', 'desktop')),
    (os.path.join(BASE_DIR, 'ui', 'web', 'index.html'), os.path.join('ui', 'web')),
    (os.path.join(BASE_DIR, 'ui'), 'ui'),
    (os.path.join(BASE_DIR, 'assets'), 'assets'),
    (os.path.join(BASE_DIR, 'config'), 'config'),
    (os.path.join(BASE_DIR, 'core'), 'core'),
    (os.path.join(BASE_DIR, 'apps'), 'apps'),
]

# Collect all data, binaries and hiddenimports for CustomTkinter
ctk_datas, ctk_binaries, ctk_hidden = collect_all('customtkinter')
datas += ctk_datas

# Collect all data, binaries and hiddenimports for pywebview
wv_datas, wv_binaries, wv_hidden = collect_all('webview')
datas += wv_datas

# Collect all data, binaries and hiddenimports for clr_loader / pythonnet
try:
    clr_datas, clr_binaries, clr_hidden = collect_all('clr_loader')
    datas += clr_datas
except Exception:
    clr_binaries, clr_hidden = [], []

try:
    pynet_datas, pynet_binaries, pynet_hidden = collect_all('pythonnet')
    datas += pynet_datas
except Exception:
    pynet_binaries, pynet_hidden = [], []

binaries = ctk_binaries + wv_binaries + clr_binaries + pynet_binaries

hiddenimports = [
    'webview',
    'webview.platforms',
    'webview.platforms.winforms',
    'webview.platforms.edgechromium',
    'clr',
    'clr_loader',
    'pythonnet',
    'customtkinter',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'PIL.ImageDraw',
    'sqlite3',
    'fastapi',
    'uvicorn',
    'pydantic',
    'requests',
    'core',
    'core.db',
    'core.bridge',
    'core.auth',
    'core.cdss',
    'core.logger',
    'core.api_client',
    'config',
    'config.settings',
    'ui',
    'ui.theme',
    'ui.components',
    'ui.components.toast',
    'ui.components.qr_canvas',
    'ui.views',
    'ui.views.login_view',
    'ui.views.admin_dashboard_view',
    'ui.views.pharmacist_dashboard_view',
    'ui.views.cashier_dashboard_view',
    'ui.views.inventory_dashboard_view',
    'ui.views.delivery_dashboard_view',
    'app',
    'desktop_app',
    'web_app',
] + ctk_hidden + wv_hidden + clr_hidden + pynet_hidden

a = Analysis(
    ['main.py'],
    pathex=[BASE_DIR],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'numpy', 'pytest', 'win32com'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TQM_Pharm_Enterprise',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(BASE_DIR, 'assets', 'app_icon.ico'),
)
