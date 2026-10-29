"""
TQM Pharm Enterprise — Primary Unified Desktop Application Entry Point.
Launches the modern, hardware-accelerated Edge Chromium desktop experience by default,
or starts the Web Application server with --web,
or falls back to legacy CustomTkinter interface if requested via --legacy.
"""

import sys
import os
import traceback
from datetime import datetime

# On Windows, attach to parent console if run from command line/PowerShell,
# while remaining completely silent and windowed if double-clicked in Explorer.
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.AttachConsole(-1)
    except Exception:
        pass

# Ensure stdout/stderr are safe for windowed GUI mode without console
if sys.stdout is None:
    try:
        sys.stdout = open(os.devnull, "w")
    except Exception:
        pass
if sys.stderr is None:
    try:
        sys.stderr = open(os.devnull, "w")
    except Exception:
        pass

CRASH_LOG = os.path.join(os.path.expanduser("~/.tqmpharm"), "crash_log.txt")

def log_error(msg):
    try:
        os.makedirs(os.path.dirname(CRASH_LOG), exist_ok=True)
        with open(CRASH_LOG, "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.now().isoformat()}] {msg}\n")
    except Exception:
        pass

if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    os.chdir(BASE_DIR)
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)

if __name__ == "__main__":
    try:
        if "--web" in sys.argv or "--server" in sys.argv:
            from web_app import run_web_server
            run_web_server()
        elif "--legacy" in sys.argv:
            print("[TQM Pharm] Launching in Legacy CustomTkinter mode...")
            from app import PharmacyApplication
            app = PharmacyApplication()
            app.mainloop()
        else:
            try:
                print("[TQM Pharm] Launching Next-Gen Hardware-Accelerated Desktop UI...")
                from desktop_app import run_desktop_app
                run_desktop_app()
            except Exception as e:
                log_error(f"WebView2 launch notice ({e}). Falling back to CustomTkinter...")
                print(f"[TQM Pharm] Notice: Failed to start WebView2 ({e}). Falling back to CustomTkinter...")
                from app import PharmacyApplication
                app = PharmacyApplication()
                app.mainloop()
    except Exception as fatal_e:
        log_error(f"FATAL CRASH: {traceback.format_exc()}")
        try:
            import tkinter.messagebox as mb
            mb.showerror("Application Launch Error", f"Fatal error during launch:\n\n{traceback.format_exc()}")
        except Exception:
            pass
