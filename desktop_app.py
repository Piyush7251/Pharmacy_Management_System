"""
AegisPharm Enterprise — Next-Generation Hardware-Accelerated Desktop Application.
Powered by Microsoft Edge Chromium WebView2 & Python Native RPC Bridge.
Provides butter-smooth 60fps rendering, zero-lag scrolling, modern responsive design,
and seamless desktop integration across all 5 clinical and operational roles.
"""

import os
import sys

# Ensure application root directory is on python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import webview
from core.db import init_db
from core.bridge import PharmacyBridge
from config.settings import get_settings

def run_desktop_app():
    """Launch the modern Edge Chromium desktop application."""
    # Ensure database is properly seeded and initialized
    init_db()
    
    # Instantiate Python RPC Bridge
    bridge = PharmacyBridge()
    
    # Resolve path to desktop HTML UI
    html_file = os.path.join(BASE_DIR, "ui", "desktop", "index.html")
    if not os.path.exists(html_file):
        raise FileNotFoundError(f"Desktop interface file missing at: {html_file}")
    
    # Load configuration
    cfg = get_settings()
    store_title = f"{cfg.store.name} — AegisPharm Enterprise"
    
    # Create Native OS Window with Edge Chromium backend
    window = webview.create_window(
        title=store_title,
        url=f"file://{os.path.abspath(html_file)}",
        js_api=bridge,
        width=1420,
        height=920,
        min_size=(1120, 720),
        background_color='#0B0F19' if cfg.system.default_theme == 'dark' else '#F8FAFC'
    )
    bridge.set_window(window)
    
    print("[AegisPharm] Launching hardware-accelerated Edge Chromium desktop window...")
    # Start native event loop
    webview.start(debug=False)

if __name__ == "__main__":
    run_desktop_app()
