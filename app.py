"""
AegisPharm Enterprise — Unified Desktop Application Entry Point.
Dual-theme support (Default: White / Light Mode, with one-click Dark Mode toggle).
Provides secure authentication, role-based dashboard routing, real-time presence tracking,
live digital clock telemetry, quick role switching, and global dynamic toast notifications.
"""

import sys
import os
from datetime import datetime

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
from ui.components.toast import show_toast
from core.api_client import AppConnector
from core.db import init_db

# Default theme: White / Light Mode
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class PharmacyApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AegisPharm Enterprise — Modern Clinical & Retail Pharmacy System")
        self.geometry("1420x920")
        self.minsize(1120, 720)
        self.configure(fg_color=COLORS["bg_base"])
        
        # Initialize database
        init_db()
        
        self.current_theme = "Light"
        self.current_user = None
        self.connector = None
        self.current_dashboard = None
        self.clock_job = None
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Start at Login Screen
        self.show_login_screen()

    def show_toast(self, title, message, toast_type="success", duration_ms=3500):
        """Display an animated floating toast notification at top-right."""
        return show_toast(self, title, message, toast_type, duration_ms)

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
        if self.clock_job:
            try:
                self.after_cancel(self.clock_job)
            except Exception:
                pass
            self.clock_job = None
            
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
        
        # Welcoming Toast
        self.show_toast(
            title=f"Welcome, {user_data['name']}",
            message=f"Logged into {user_data['role']} workstation with full permissions.",
            toast_type="success"
        )

    def switch_role(self, selected_role_text):
        """Restricted to Store Admin for supervisor inspection."""
        if not self.current_user or self.current_user.get("role") != "Admin":
            self.show_toast(
                title="Access Denied",
                message="Role switching is disabled for security compliance. Please Lock / Sign Out to change users.",
                toast_type="error"
            )
            return

        role_map = {
            "👑 Store Admin": ("Admin", "Dr. Rajesh Kulkarni", "STF-01"),
            "🩺 Pharmacist": ("Pharmacist", "Pooja Sharma, R.Ph", "STF-02"),
            "💳 Cashier (POS)": ("Cashier", "Amit Deshmukh", "STF-03"),
            "📦 Stock Manager": ("Inventory Manager", "Vikram Rathore", "STF-04"),
            "🛵 Delivery Rider": ("Delivery Agent", "Ramesh Kumar", "STF-05")
        }
        
        target = role_map.get(selected_role_text)
        if target and self.current_user:
            self.current_user["role"] = target[0]
            self.current_user["name"] = target[1]
            self.current_user["id"] = target[2]
            
            if self.connector:
                self.connector.role = target[0]
                self.connector.user_name = target[1]
                self.connector.user_id = target[2]
                self.connector.update_action(f"Supervisor inspected view {target[0]}")
                
            self.load_role_dashboard()
            self.show_toast(
                title=f"Supervisor View: {target[0]}",
                message=f"Inspecting department as {self.current_user['name']}.",
                toast_type="info"
            )

    def load_role_dashboard(self):
        if self.clock_job:
            try:
                self.after_cancel(self.clock_job)
            except Exception:
                pass
            self.clock_job = None
            
        # Clear login view
        for widget in self.winfo_children():
            widget.destroy()
            
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Top Bar
        self.grid_rowconfigure(1, weight=1)  # Dashboard Content
        
        # 1. Global Top Navigation Bar
        topbar = ctk.CTkFrame(
            self,
            height=62,
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
        left_info.grid(row=0, column=0, sticky="w", padx=16, pady=10)
        
        lbl_brand = ctk.CTkLabel(
            left_info,
            text="💊 AegisPharm",
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

        # Center-Left: Live Digital Clock & Sync Pulse
        mid_info = ctk.CTkFrame(topbar, fg_color="transparent")
        mid_info.grid(row=0, column=1, sticky="w", padx=20)
        
        self.lbl_clock = ctk.CTkLabel(
            mid_info,
            text="",
            font=FONTS["mono_bold"],
            text_color=COLORS["text_muted"]
        )
        self.lbl_clock.pack(side="left", padx=(0, 10))
        
        pulse_badge = ctk.CTkLabel(
            mid_info,
            text=" 🟢 System Online ",
            font=FONTS["small_bold"],
            fg_color=COLORS["success_bg"],
            text_color=COLORS["clinical"],
            corner_radius=6
        )
        pulse_badge.pack(side="left")
        
        self.update_clock()
        
        # Right: Theme Switcher, Certified Identity Chip & Lock Station
        right_info = ctk.CTkFrame(topbar, fg_color="transparent")
        right_info.grid(row=0, column=1, sticky="e", padx=16, pady=10)
        
        theme_btn_text = "🌙 Dark Mode" if self.current_theme == "Light" else "☀️ Light Mode"
        self.btn_theme = ctk.CTkButton(
            right_info,
            text=theme_btn_text,
            width=95,
            height=30,
            font=FONTS["small_bold"],
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_secondary_hover"],
            text_color=COLORS["btn_secondary_text"],
            command=self.toggle_theme
        )
        self.btn_theme.pack(side="left", padx=(0, 10))
        
        role_str = self.current_user.get("role", "Staff")
        role_icon = "👑" if "Admin" in role_str else ("🩺" if "Pharmacist" in role_str else ("💳" if "Cashier" in role_str else ("📦" if "Inventory" in role_str else "🛵")))
        
        # Certified Workstation Identity Chip (Read-Only RBAC)
        user_chip = ctk.CTkFrame(right_info, fg_color=COLORS["badge_bg"], corner_radius=6, border_width=1, border_color=COLORS["border"])
        user_chip.pack(side="left", padx=(0, 10))
        
        lbl_user = ctk.CTkLabel(
            user_chip,
            text=f" {role_icon} {self.current_user.get('name', 'User')}  •  [{role_str}]  •  ID: {self.current_user.get('id', 'STF-XX')} ",
            font=FONTS["small_bold"],
            text_color=COLORS["text_main"],
            padx=10,
            pady=4
        )
        lbl_user.pack()
        
        btn_logout = ctk.CTkButton(
            right_info,
            text=" 🔒 Lock / Sign Out ",
            width=115,
            height=30,
            font=FONTS["small_bold"],
            fg_color=COLORS["btn_danger"],
            hover_color=COLORS["btn_danger_hover"],
            text_color="#FFFFFF",
            corner_radius=6,
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

    def update_clock(self):
        try:
            now_str = datetime.now().strftime("%d %b %Y • %I:%M:%S %p")
            if hasattr(self, "lbl_clock") and self.lbl_clock.winfo_exists():
                self.lbl_clock.configure(text=f"🕒 {now_str}")
                self.clock_job = self.after(1000, self.update_clock)
        except Exception:
            pass

    def logout(self):
        if self.clock_job:
            try:
                self.after_cancel(self.clock_job)
            except Exception:
                pass
            self.clock_job = None
            
        if self.connector:
            self.connector.log_event("User Logout", f"{self.current_user['name']} signed out from terminal", level="INFO")
            self.connector.stop()
            self.connector = None
        self.show_login_screen()

    def on_close(self):
        if self.clock_job:
            try:
                self.after_cancel(self.clock_job)
            except Exception:
                pass
        if self.connector:
            self.connector.stop()
        self.destroy()


if __name__ == "__main__":
    app = PharmacyApplication()
    app.mainloop()
