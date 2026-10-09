"""
AegisPharm Enterprise — Unified Desktop Application Entry Point.
Dual-theme support (Default: White / Light Mode, with one-click Dark Mode toggle).
Provides secure authentication, role-based dashboard routing, and real-time presence tracking.
"""

import sys
import os

# Add workspace directory to python path for modular imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from ui.theme import COLORS, FONTS
from ui.views.login_view import LoginView
from ui.views.admin_dashboard_view import AdminDashboardView
from ui.views.pharmacist_dashboard_view import PharmacistDashboardView
from ui.views.cashier_dashboard_view import CashierDashboardView
from ui.views.inventory_dashboard_view import InventoryDashboardView
from ui.views.delivery_dashboard_view import DeliveryDashboardView
from core.api_client import AppConnector
from core.db import init_db

# Default theme: White / Light Mode
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class PharmacyApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AegisPharm Enterprise — Pharmacy Management System")
        self.geometry("1400x900")
        self.minsize(1100, 720)
        self.configure(fg_color=COLORS["bg_base"])
        
        # Initialize database
        init_db()
        
        self.current_theme = "Light"
        self.current_user = None
        self.connector = None
        self.current_dashboard = None
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Start at Login Screen
        self.show_login_screen()

    def toggle_theme(self):
        """Toggle between Light (White) and Dark appearance modes."""
        if self.current_theme == "Light":
            self.current_theme = "Dark"
            ctk.set_appearance_mode("Dark")
            if hasattr(self, "btn_theme"):
                self.btn_theme.configure(text="☀️ Light Mode")
        else:
            self.current_theme = "Light"
            ctk.set_appearance_mode("Light")
            if hasattr(self, "btn_theme"):
                self.btn_theme.configure(text="🌙 Dark Mode")

    def show_login_screen(self):
        # Clean up any existing session
        if self.connector:
            self.connector.stop()
            self.connector = None
            
        self.current_user = None
        
        # Clear all widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.login_view = LoginView(
            self,
            on_login_success_cb=self.handle_login_success,
            toggle_theme_cb=self.toggle_theme,
            current_theme=self.current_theme
        )
        self.login_view.grid(row=0, column=0, sticky="nsew")

    def handle_login_success(self, user_data):
        self.current_user = user_data
        
        # Start real-time presence connector for this user session
        self.connector = AppConnector(
            user_id=user_data["id"],
            user_name=user_data["name"],
            role=user_data["role"],
            app_name=f"{user_data['role']} Terminal"
        )
        self.connector.start()
        
        # Transition to Main Dashboard UI
        self.load_role_dashboard()

    def load_role_dashboard(self):
        # Clear login view
        for widget in self.winfo_children():
            widget.destroy()
            
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Top Bar
        self.grid_rowconfigure(1, weight=1)  # Dashboard Content
        
        # 1. Global Top Navigation Bar
        topbar = ctk.CTkFrame(
            self,
            height=60,
            corner_radius=0,
            fg_color=COLORS["bg_surface"],
            border_width=1,
            border_color=COLORS["border"]
        )
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_propagate(False)
        topbar.grid_columnconfigure(1, weight=1)
        
        # Left: Brand & Branch
        left_info = ctk.CTkFrame(topbar, fg_color="transparent")
        left_info.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        
        lbl_brand = ctk.CTkLabel(
            left_info,
            text="💊 AegisPharm Enterprise",
            font=FONTS["h2"],
            text_color=COLORS["clinical"]
        )
        lbl_brand.pack(side="left")
        
        lbl_branch = ctk.CTkLabel(
            left_info,
            text=f"  •  🏬 {self.current_user.get('branch', 'Apex Central - Branch #01')}",
            font=FONTS["small_bold"],
            text_color=COLORS["text_dim"]
        )
        lbl_branch.pack(side="left")
        
        # Right: Theme Switcher, User Profile Badge & Logout
        right_info = ctk.CTkFrame(topbar, fg_color="transparent")
        right_info.grid(row=0, column=1, sticky="e", padx=20, pady=10)
        
        theme_btn_text = "🌙 Dark Mode" if self.current_theme == "Light" else "☀️ Light Mode"
        self.btn_theme = ctk.CTkButton(
            right_info,
            text=theme_btn_text,
            width=100,
            height=32,
            font=FONTS["small_bold"],
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_secondary_hover"],
            text_color=COLORS["btn_secondary_text"],
            command=self.toggle_theme
        )
        self.btn_theme.pack(side="left", padx=(0, 14))
        
        role_icon = "👑" if "Admin" in self.current_user["role"] else ("🩺" if "Pharmacist" in self.current_user["role"] else ("💳" if "Cashier" in self.current_user["role"] else "📦"))
        
        # User profile chip
        user_chip = ctk.CTkFrame(right_info, fg_color=COLORS["badge_bg"], corner_radius=6, border_width=1, border_color=COLORS["border"])
        user_chip.pack(side="left", padx=(0, 12))
        
        lbl_user = ctk.CTkLabel(
            user_chip,
            text=f" {role_icon} {self.current_user['name']}  |  {self.current_user['role']} ",
            font=FONTS["small_bold"],
            text_color=COLORS["text_main"],
            padx=10,
            pady=4
        )
        lbl_user.pack()
        
        btn_logout = ctk.CTkButton(
            right_info,
            text="🚪 Sign Out",
            width=85,
            height=32,
            font=FONTS["small_bold"],
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_danger"],
            text_color=COLORS["btn_secondary_text"],
            command=self.logout
        )
        btn_logout.pack(side="left")
        
        # 2. Main Dashboard Content Container
        content_container = ctk.CTkFrame(self, fg_color=COLORS["bg_base"])
        content_container.grid(row=1, column=0, sticky="nsew")
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_rowconfigure(0, weight=1)
        
        # 3. Route to Specific Role Dashboard
        role = self.current_user.get("role", "")
        
        if "Admin" in role:
            self.current_dashboard = AdminDashboardView(content_container, self.current_user, self.connector)
        elif "Pharmacist" in role:
            self.current_dashboard = PharmacistDashboardView(content_container, self.current_user, self.connector)
        elif "Cashier" in role:
            self.current_dashboard = CashierDashboardView(content_container, self.current_user, self.connector)
        elif "Inventory" in role:
            self.current_dashboard = InventoryDashboardView(content_container, self.current_user, self.connector)
        elif "Delivery" in role:
            self.current_dashboard = DeliveryDashboardView(content_container, self.current_user, self.connector)
        else:
            self.current_dashboard = CashierDashboardView(content_container, self.current_user, self.connector)
            
        self.current_dashboard.grid(row=0, column=0, sticky="nsew")

    def logout(self):
        if self.connector:
            self.connector.log_event("User Logout", f"{self.current_user['name']} signed out from terminal", level="INFO")
            self.connector.stop()
            self.connector = None
        self.show_login_screen()

    def on_close(self):
        if self.connector:
            self.connector.stop()
        self.destroy()


if __name__ == "__main__":
    app = PharmacyApplication()
    app.mainloop()
