"""
AegisPharm Enterprise — Cashier POS & Billing Terminal (Standalone).
Provides complete access to:
  1. Express Barcode & Catalog POS Counter
  2. 1-Click Approved Prescription Queue Import
  3. Multi-Tender Checkout (Cash, UPI Dynamic QR, Card)
  4. Instant GST Tax Invoice & Thermal Receipt Print Modal
  5. Home Delivery Routing Dispatch
  6. Historical Sales & Invoice Ledger
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from ui.theme import COLORS, FONTS
from core.api_client import AppConnector
from core.db import init_db
from ui.views.cashier_dashboard_view import CashierDashboardView

# Default appearance: White / Light
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class CashierPOSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("💳 AegisPharm — Cashier POS & Express Billing Terminal #01")
        self.geometry("1400x900")
        self.minsize(1100, 720)
        self.configure(fg_color=COLORS["bg_base"])
        
        # Ensure database is initialized
        init_db()
        
        self.current_theme = "Light"
        self.user_data = {
            "id": "STF-03",
            "name": "Amit Deshmukh",
            "role": "Cashier",
            "branch": "Apex Central - Billing Terminal #01"
        }
        
        # Start Presence Connector for Cashier
        self.connector = AppConnector(
            user_id=self.user_data["id"],
            user_name=self.user_data["name"],
            role=self.user_data["role"],
            app_name="POS Billing Terminal #01"
        )
        self.connector.start()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.setup_ui()

    def toggle_theme(self):
        if self.current_theme == "Light":
            self.current_theme = "Dark"
            ctk.set_appearance_mode("Dark")
            self.btn_theme.configure(text="☀️ Light Mode")
        else:
            self.current_theme = "Light"
            ctk.set_appearance_mode("Light")
            self.btn_theme.configure(text="🌙 Dark Mode")

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # Top Navigation Bar
        topbar = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=COLORS["bg_surface"], border_width=1, border_color=COLORS["border"])
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_propagate(False)
        topbar.grid_columnconfigure(1, weight=1)
        
        left_info = ctk.CTkFrame(topbar, fg_color="transparent")
        left_info.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        
        lbl_title = ctk.CTkLabel(left_info, text="💳 Cashier POS & Billing Terminal #01", font=FONTS["h2"], text_color=COLORS["commerce"])
        lbl_title.pack(side="left")
        
        lbl_branch = ctk.CTkLabel(left_info, text="  •  Counter #01 (Morning Shift)  •  Apex Central", font=FONTS["small_bold"], text_color=COLORS["text_dim"])
        lbl_branch.pack(side="left")
        
        right_info = ctk.CTkFrame(topbar, fg_color="transparent")
        right_info.grid(row=0, column=1, sticky="e", padx=20, pady=10)
        
        self.btn_theme = ctk.CTkButton(
            right_info,
            text="🌙 Dark Mode",
            width=100,
            height=32,
            font=FONTS["small_bold"],
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_secondary_hover"],
            text_color=COLORS["btn_secondary_text"],
            command=self.toggle_theme
        )
        self.btn_theme.pack(side="left", padx=(0, 12))
        
        user_chip = ctk.CTkFrame(right_info, fg_color=COLORS["badge_bg"], corner_radius=6, border_width=1, border_color=COLORS["border"])
        user_chip.pack(side="left")
        
        lbl_user = ctk.CTkLabel(
            user_chip,
            text=f" 💳 {self.user_data['name']} (Cashier) ",
            font=FONTS["small_bold"],
            text_color=COLORS["text_main"],
            padx=10,
            pady=4
        )
        lbl_user.pack()
        
        # Body: Full Featured Cashier Dashboard View
        body = ctk.CTkFrame(self, fg_color=COLORS["bg_base"])
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(0, weight=1)
        
        self.dashboard_view = CashierDashboardView(body, self.user_data, self.connector)
        self.dashboard_view.grid(row=0, column=0, sticky="nsew")

    def on_close(self):
        if self.connector:
            self.connector.stop()
        self.destroy()

if __name__ == "__main__":
    app = CashierPOSApp()
    app.mainloop()
