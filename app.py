"""
Pharmacy Management System — Main Desktop Application Frontend (Python / CustomTkinter).
Enterprise architecture desktop client matching the 6-layer system specifications.
"""

import sys
import os

# Add workspace directory to python path for modular imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from ui.theme import COLORS, FONTS
from ui.views.pos_view import POSView
from ui.views.clinical_view import ClinicalView
from ui.views.inventory_view import InventoryView
from ui.views.operations_view import OperationsView
from data.mock_db import DAILY_STATS

# Set global CustomTkinter appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PharmacyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AegisPharm Enterprise — Pharmacy Management System")
        self.geometry("1380x880")
        self.minsize(1100, 700)
        self.configure(fg_color=COLORS["bg_base"])
        
        self.active_role = "Pharmacist"
        
        # Grid layout: Sidebar (col 0), Main Content (col 1)
        self.grid_columnconfigure(0, weight=0)  # Fixed sidebar
        self.grid_columnconfigure(1, weight=1)  # Expandable content
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_sidebar()
        self.setup_main_area()
        
        # Default view: POS Counter
        self.switch_view("pos")

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=260,
            corner_radius=0,
            fg_color=COLORS["bg_sidebar"],
            border_width=1,
            border_color=COLORS["border"]
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(6, weight=1)  # Push footer to bottom
        
        # Brand Logo & Title
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.grid(row=0, column=0, sticky="ew", padx=16, pady=(20, 24))
        
        lbl_logo = ctk.CTkLabel(
            brand_frame,
            text="💊 AegisPharm",
            font=FONTS["h1"],
            text_color=COLORS["clinical"]
        )
        lbl_logo.pack(anchor="w")
        
        lbl_sub = ctk.CTkLabel(
            brand_frame,
            text="Enterprise Healthcare POS & ERP",
            font=FONTS["small"],
            text_color=COLORS["text_dim"]
        )
        lbl_sub.pack(anchor="w")
        
        # Navigation Buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("pos", "🛒 POS & Dispensing", COLORS["commerce"]),
            ("clinical", "🩺 Clinical & eRx Queue", COLORS["clinical"]),
            ("inventory", "📦 Inventory & FEFO", COLORS["inventory"]),
            ("operations", "🛵 Fulfilment & Operations", COLORS["operations"])
        ]
        
        for idx, (key, label, color) in enumerate(nav_items, start=1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                anchor="w",
                height=44,
                corner_radius=8,
                fg_color="transparent",
                hover_color=COLORS["bg_surface_alt"],
                text_color=COLORS["text_muted"],
                font=FONTS["body_bold"],
                command=lambda k=key: self.switch_view(k)
            )
            btn.grid(row=idx, column=0, sticky="ew", padx=12, pady=4)
            self.nav_buttons[key] = btn

        # System Status in Sidebar Footer
        footer = ctk.CTkFrame(self.sidebar, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        footer.grid(row=7, column=0, sticky="ew", padx=12, pady=16)
        
        lbl_stat_title = ctk.CTkLabel(footer, text="⚡ Live Infrastructure", font=FONTS["small_bold"], text_color=COLORS["text_main"])
        lbl_stat_title.pack(anchor="w", padx=10, pady=(8, 2))
        
        lbl_stat_db = ctk.CTkLabel(footer, text="• PostgreSQL: Connected (Primary)", font=FONTS["small"], text_color=COLORS["clinical"])
        lbl_stat_db.pack(anchor="w", padx=10, pady=1)
        
        lbl_stat_temp = ctk.CTkLabel(footer, text="• Cold-Chain: 4.2°C (Optimal)", font=FONTS["small"], text_color=COLORS["info"])
        lbl_stat_temp.pack(anchor="w", padx=10, pady=(1, 8))

    def setup_main_area(self):
        self.main_container = ctk.CTkFrame(self, fg_color=COLORS["bg_base"])
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
        # Top App Bar with Persona / Role Switcher & Live Stats
        self.topbar = ctk.CTkFrame(
            self.main_container,
            height=60,
            corner_radius=0,
            fg_color=COLORS["bg_surface"],
            border_width=1,
            border_color=COLORS["border"]
        )
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.grid_propagate(False)
        self.topbar.grid_columnconfigure(1, weight=1)
        
        # Left side: Active Store & Branch
        branch_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        branch_frame.grid(row=0, column=0, sticky="w", padx=20, pady=12)
        
        lbl_branch = ctk.CTkLabel(
            branch_frame,
            text="🏬 Apex Central Pharmacy — Branch #01",
            font=FONTS["body_bold"],
            text_color=COLORS["text_main"]
        )
        lbl_branch.pack(side="left")
        
        # Right side: Role Switcher & Live Clock/User
        right_top = ctk.CTkFrame(self.topbar, fg_color="transparent")
        right_top.grid(row=0, column=1, sticky="e", padx=20, pady=12)
        
        lbl_role_tag = ctk.CTkLabel(right_top, text="Persona / Role:", font=FONTS["small"], text_color=COLORS["text_dim"])
        lbl_role_tag.pack(side="left", padx=(0, 8))
        
        self.role_menu = ctk.CTkOptionMenu(
            right_top,
            values=["Pharmacist (Clinical)", "Cashier (POS)", "Store Admin", "Delivery Ops"],
            fg_color=COLORS["btn_secondary"],
            button_color=COLORS["btn_secondary_hover"],
            font=FONTS["small_bold"],
            width=180,
            command=self.on_role_change
        )
        self.role_menu.set("Pharmacist (Clinical)")
        self.role_menu.pack(side="left")
        
        # Content Container for dynamic view switching
        self.content_view = ctk.CTkFrame(self.main_container, fg_color=COLORS["bg_base"])
        self.content_view.grid(row=1, column=0, sticky="nsew")
        self.content_view.grid_columnconfigure(0, weight=1)
        self.content_view.grid_rowconfigure(0, weight=1)
        
        # Instantiate views
        self.views = {
            "pos": POSView(self.content_view, show_notification_cb=self.show_toast),
            "clinical": ClinicalView(self.content_view),
            "inventory": InventoryView(self.content_view, show_notification_cb=self.show_toast),
            "operations": OperationsView(self.content_view, show_notification_cb=self.show_toast)
        }
        
        for v in self.views.values():
            v.grid(row=0, column=0, sticky="nsew")

    def switch_view(self, key):
        # Update nav buttons highlight
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color=COLORS["bg_surface_alt"], text_color=COLORS["text_main"])
            else:
                btn.configure(fg_color="transparent", text_color=COLORS["text_muted"])
                
        # Bring active view to front
        view = self.views.get(key)
        if view:
            view.tkraise()

    def on_role_change(self, selected_role):
        self.active_role = selected_role
        self.show_toast(f"Switched role to: {selected_role}")
        
        if "Cashier" in selected_role:
            self.switch_view("pos")
        elif "Clinical" in selected_role:
            self.switch_view("clinical")
        elif "Admin" in selected_role:
            self.switch_view("inventory")
        elif "Delivery" in selected_role:
            self.switch_view("operations")

    def show_toast(self, message):
        print(f"[AegisPharm Notification]: {message}")


if __name__ == "__main__":
    app = PharmacyApp()
    app.mainloop()
