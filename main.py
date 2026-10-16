"""
AegisPharm Enterprise — Primary Unified Application Entry Point.
Launches the modern, hardware-accelerated Edge Chromium desktop experience by default,
or starts the Web Application server with --web,
or falls back to legacy CustomTkinter interface if requested via --legacy.
"""

import sys

if __name__ == "__main__":
    if "--web" in sys.argv or "--server" in sys.argv:
        from web_app import run_web_server
        run_web_server()
    elif "--legacy" in sys.argv:
        print("[AegisPharm] Launching in Legacy CustomTkinter mode...")
        from app import PharmacyApplication
        app = PharmacyApplication()
        app.mainloop()
    else:
        try:
            print("[AegisPharm] Launching Next-Gen Hardware-Accelerated Desktop UI...")
            from desktop_app import run_desktop_app
            run_desktop_app()
        except Exception as e:
            print(f"[AegisPharm] Notice: Failed to start WebView2 ({e}). Falling back to CustomTkinter...")
            from app import PharmacyApplication
            app = PharmacyApplication()
            app.mainloop()
