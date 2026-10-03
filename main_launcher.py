"""
AegisPharm Enterprise — Master Suite Launcher & Application Hub.
Allows you to start the Central Gateway Server and launch individual role-based desktop applications
(Admin, Pharmacist, Cashier, Inventory, Delivery) or run them all concurrently.
"""

import sys
import os
import subprocess
import threading
import time
import requests
import customtkinter as ctk
from ui.theme import COLORS, FONTS

# Set appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_SCRIPT = os.path.join(BASE_DIR, "server", "gateway_server.py")
APPS = {
    "admin": {
        "title": "👑 Admin Command Center",
        "desc": "Live staff online monitor, presence tracking, storewide metrics & audit stream",
        "script": os.path.join(BASE_DIR, "apps", "admin_app.py"),
        "color": COLORS["admin"] if "admin" in COLORS else "#FBBF24"
    },
    "pharmacist": {
        "title": "🩺 Pharmacist Clinical Station",
        "desc": "eRx queue, CDSS drug safety/allergy checks & Schedule X double sign-off",
        "script": os.path.join(BASE_DIR, "apps", "pharmacist_app.py"),
        "color": COLORS["clinical"]
    },
    "cashier": {
        "title": "💳 Cashier POS & Billing Terminal",
        "desc": "High-speed barcode checkout, GST invoicing, UPI/Cash payments & live sync",
        "script": os.path.join(BASE_DIR, "apps", "cashier_app.py"),
        "color": COLORS["commerce"]
    },
    "inventory": {
        "title": "📦 Inventory & FEFO Supply Chain",
        "desc": "Multi-batch stock ledger, cold-chain temperature logs & GRN inwarding",
        "script": os.path.join(BASE_DIR, "apps", "inventory_app.py"),
        "color": COLORS["inventory"]
    },
    "delivery": {
        "title": "🛵 Delivery & Fulfilment App",
        "desc": "Active home delivery routes, cold-chain handover & OTP e-POD confirmation",
        "script": os.path.join(BASE_DIR, "apps", "delivery_app.py"),
        "color": COLORS["operations"]
    }
}

class MasterSuiteLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AegisPharm Enterprise — Multi-App Control Portal")
        self.geometry("1100x780")
        self.minsize(900, 640)
        self.configure(fg_color=COLORS["bg_base"])
        
        self.server_proc = None
        
        self.setup_ui()
        self.check_server_status()
        
        # Automatically launch server in background thread if not already running
        self.auto_start_server()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # 1. Top Hero Header
        hero = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        hero.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        hero.grid_columnconfigure(0, weight=1)
        
        lbl_h1 = ctk.CTkLabel(hero, text="⚡ AegisPharm Enterprise Multi-App Suite", font=FONTS["h1"], text_color=COLORS["text_main"])
        lbl_h1.pack(anchor="w", padx=20, pady=(16, 2))
        
        lbl_h2 = ctk.CTkLabel(
            hero,
            text="Distributed multi-role desktop ecosystem connected via Central Gateway Server.",
            font=FONTS["body"],
            text_color=COLORS["text_muted"]
        )
        lbl_h2.pack(anchor="w", padx=20, pady=(0, 16))
        
        # 2. Server Control Strip
        server_strip = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        server_strip.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))
        server_strip.grid_columnconfigure(1, weight=1)
        
        self.lbl_server = ctk.CTkLabel(server_strip, text="🟢 Gateway Server: Initializing (http://127.0.0.1:8000)...", font=FONTS["body_bold"], text_color=COLORS["clinical"])
        self.lbl_server.grid(row=0, column=0, padx=20, pady=14, sticky="w")
        
        btn_box = ctk.CTkFrame(server_strip, fg_color="transparent")
        btn_box.grid(row=0, column=1, sticky="e", padx=20)
        
        btn_all = ctk.CTkButton(
            btn_box,
            text="🚀 Launch All Apps",
            height=34,
            fg_color=COLORS["clinical"],
            hover_color=COLORS["clinical_hover"],
            font=FONTS["body_bold"],
            command=self.launch_all_apps
        )
        btn_all.pack(side="left", padx=(0, 8))
        
        btn_restart = ctk.CTkButton(
            btn_box,
            text="🔄 Restart Server",
            height=34,
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_secondary_hover"],
            font=FONTS["small_bold"],
            command=self.restart_server
        )
        btn_restart.pack(side="left")
        
        # 3. App Selection Grid (Scrollable)
        app_scroll = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg_base"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        app_scroll.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        app_scroll.grid_columnconfigure(0, weight=1)
        
        for key, app_info in APPS.items():
            card = ctk.CTkFrame(app_scroll, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", pady=6, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            # Left: Details
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.grid(row=0, column=0, sticky="w", padx=16, pady=16)
            
            lbl_title = ctk.CTkLabel(info_frame, text=app_info["title"], font=FONTS["h2"], text_color=app_info["color"])
            lbl_title.pack(anchor="w")
            
            lbl_desc = ctk.CTkLabel(info_frame, text=app_info["desc"], font=FONTS["body"], text_color=COLORS["text_muted"])
            lbl_desc.pack(anchor="w", pady=(4, 0))
            
            # Right: Launch Button
            btn_launch = ctk.CTkButton(
                card,
                text="Launch App ↗",
                width=140,
                height=42,
                font=FONTS["body_bold"],
                fg_color=app_info["color"],
                hover_color=COLORS["btn_primary_hover"],
                text_color="#000000" if app_info["color"] in [COLORS["clinical"], COLORS["inventory"], "#FBBF24"] else "#FFFFFF",
                command=lambda s=app_info["script"]: self.launch_app(s)
            )
            btn_launch.grid(row=0, column=1, sticky="e", padx=20, pady=16)

    def auto_start_server(self):
        try:
            res = requests.get("http://127.0.0.1:8000/", timeout=0.8)
            if res.status_code == 200:
                self.lbl_server.configure(text="🟢 Gateway Server: Online (http://127.0.0.1:8000)", text_color=COLORS["clinical"])
                return
        except Exception:
            pass
            
        # Start server background process
        threading.Thread(target=self._run_server, daemon=True).start()

    def _run_server(self):
        try:
            self.server_proc = subprocess.Popen([sys.executable, SERVER_SCRIPT])
            time.sleep(2)
            self.lbl_server.configure(text="🟢 Gateway Server: Online (http://127.0.0.1:8000)", text_color=COLORS["clinical"])
        except Exception as e:
            self.lbl_server.configure(text=f"⚠️ Gateway Server: Error starting ({e})", text_color=COLORS["danger"])

    def check_server_status(self):
        try:
            res = requests.get("http://127.0.0.1:8000/", timeout=0.8)
            if res.status_code == 200:
                self.lbl_server.configure(text="🟢 Gateway Server: Online (http://127.0.0.1:8000)", text_color=COLORS["clinical"])
            else:
                self.lbl_server.configure(text="🟡 Gateway Server: Degraded", text_color=COLORS["warning"])
        except Exception:
            self.lbl_server.configure(text="🟡 Gateway Server: Local DB Fallback Active", text_color=COLORS["warning"])
            
        self.after(5000, self.check_server_status)

    def restart_server(self):
        if self.server_proc:
            try:
                self.server_proc.terminate()
            except Exception:
                pass
        self._run_server()

    def launch_app(self, script_path):
        subprocess.Popen([sys.executable, script_path])

    def launch_all_apps(self):
        for app_info in APPS.values():
            subprocess.Popen([sys.executable, app_info["script"]])


if __name__ == "__main__":
    hub = MasterSuiteLauncher()
    hub.mainloop()
