"""
AegisPharm Enterprise — Modern Dual-Theme Login Screen (Default: Clean White Mode).
Supports instant theme switching between Light and Dark mode.
"""

import customtkinter as ctk
from ui.theme import COLORS, FONTS
from core.db import authenticate_user

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, on_login_success_cb, toggle_theme_cb=None, current_theme="Light"):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.on_login_success = on_login_success_cb
        self.toggle_theme = toggle_theme_cb
        self.current_theme = current_theme
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()

    def setup_ui(self):
        # Center container card with clean subtle shadow/border
        center_card = ctk.CTkFrame(
            self,
            width=500,
            fg_color=COLORS["bg_surface"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"]
        )
        center_card.grid(row=0, column=0, padx=20, pady=20)
        center_card.grid_columnconfigure(0, weight=1)
        
        # Top right theme toggle button
        if self.toggle_theme:
            theme_btn_text = "🌙 Dark Mode" if self.current_theme == "Light" else "☀️ Light Mode"
            btn_th = ctk.CTkButton(
                center_card,
                text=theme_btn_text,
                width=100,
                height=26,
                font=FONTS["small_bold"],
                fg_color=COLORS["btn_secondary"],
                hover_color=COLORS["btn_secondary_hover"],
                text_color=COLORS["btn_secondary_text"],
                command=self._on_toggle_theme
            )
            btn_th.grid(row=0, column=0, sticky="e", padx=20, pady=(16, 0))
            self.btn_theme_toggle = btn_th

        # 1. Branding Header
        brand_box = ctk.CTkFrame(center_card, fg_color="transparent")
        brand_box.grid(row=1, column=0, sticky="ew", padx=30, pady=(12, 12))
        
        lbl_logo = ctk.CTkLabel(
            brand_box,
            text="💊 AegisPharm",
            font=FONTS["h1"],
            text_color=COLORS["clinical"]
        )
        lbl_logo.pack(anchor="center")
        
        lbl_sub = ctk.CTkLabel(
            brand_box,
            text="Enterprise Healthcare POS, ERP & Clinical Suite",
            font=FONTS["body"],
            text_color=COLORS["text_muted"]
        )
        lbl_sub.pack(anchor="center", pady=(4, 0))
        
        lbl_instr = ctk.CTkLabel(
            brand_box,
            text="Enter your assigned staff credentials to load your dashboard.",
            font=FONTS["small"],
            text_color=COLORS["text_dim"],
            wraplength=400,
            justify="center"
        )
        lbl_instr.pack(anchor="center", pady=(6, 0))
        
        # 2. Error Banner
        self.err_banner = ctk.CTkFrame(center_card, fg_color="transparent")
        self.err_banner.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 6))
        self.lbl_err = ctk.CTkLabel(self.err_banner, text="", font=FONTS["small_bold"], text_color=COLORS["danger"])
        self.lbl_err.pack()
        
        # 3. Form Inputs
        form_box = ctk.CTkFrame(center_card, fg_color="transparent")
        form_box.grid(row=3, column=0, sticky="ew", padx=30, pady=0)
        form_box.grid_columnconfigure(0, weight=1)
        
        # Username
        lbl_u = ctk.CTkLabel(form_box, text="Username or Staff ID", font=FONTS["body_bold"], text_color=COLORS["text_main"])
        lbl_u.grid(row=0, column=0, sticky="w", pady=(0, 4))
        
        self.ent_username = ctk.CTkEntry(
            form_box,
            placeholder_text="e.g. admin, pharmacist, cashier",
            font=FONTS["body"],
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_main"],
            border_color=COLORS["border"],
            height=40
        )
        self.ent_username.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        self.ent_username.bind("<Return>", lambda e: self.ent_password.focus())
        
        # Password
        lbl_p = ctk.CTkLabel(form_box, text="Password", font=FONTS["body_bold"], text_color=COLORS["text_main"])
        lbl_p.grid(row=2, column=0, sticky="w", pady=(0, 4))
        
        self.ent_password = ctk.CTkEntry(
            form_box,
            placeholder_text="••••••••",
            show="•",
            font=FONTS["body"],
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_main"],
            border_color=COLORS["border"],
            height=40
        )
        self.ent_password.grid(row=3, column=0, sticky="ew", pady=(0, 18))
        self.ent_password.bind("<Return>", lambda e: self.do_login())
        
        # Login Button
        self.btn_login = ctk.CTkButton(
            form_box,
            text="🔓 Sign In to Dashboard",
            height=42,
            font=FONTS["body_bold"],
            fg_color=COLORS["clinical"],
            hover_color=COLORS["clinical_hover"],
            text_color="#FFFFFF",
            command=self.do_login
        )
        self.btn_login.grid(row=4, column=0, sticky="ew", pady=(0, 18))
        
        # 4. Quick Demo Role Selector
        demo_box = ctk.CTkFrame(center_card, fg_color=COLORS["bg_surface_alt"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        demo_box.grid(row=4, column=0, sticky="ew", padx=30, pady=(0, 24))
        
        lbl_demo = ctk.CTkLabel(demo_box, text="⚡ Quick Demo Roles (1-Click Fill & Login):", font=FONTS["small_bold"], text_color=COLORS["text_dim"])
        lbl_demo.pack(anchor="w", padx=12, pady=(10, 6))
        
        btn_grid = ctk.CTkFrame(demo_box, fg_color="transparent")
        btn_grid.pack(fill="x", padx=8, pady=(0, 10))
        btn_grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        roles = [
            ("👑 Admin", "admin", "admin123", COLORS["admin"]),
            ("🩺 Pharmacist", "pharmacist", "pharma123", COLORS["clinical"]),
            ("💳 Cashier", "cashier", "cash123", COLORS["commerce"]),
            ("📦 Inventory", "inventory", "inv123", COLORS["inventory"]),
            ("🛵 Delivery", "delivery", "deliv123", COLORS["operations"]),
        ]
        
        for idx, (label, uname, pwd, col) in enumerate(roles):
            r = idx // 3
            c = idx % 3
            b = ctk.CTkButton(
                btn_grid,
                text=label,
                height=30,
                fg_color=COLORS["bg_card"],
                hover_color=COLORS["border"],
                text_color=col,
                border_width=1,
                border_color=COLORS["border"],
                font=FONTS["small_bold"],
                command=lambda u=uname, p=pwd: self.fill_and_login(u, p)
            )
            b.grid(row=r, column=c, padx=3, pady=3, sticky="ew")

    def _on_toggle_theme(self):
        if self.toggle_theme:
            self.toggle_theme()
            self.current_theme = "Dark" if self.current_theme == "Light" else "Light"
            if hasattr(self, "btn_theme_toggle"):
                self.btn_theme_toggle.configure(text="☀️ Light Mode" if self.current_theme == "Dark" else "🌙 Dark Mode")

    def fill_and_login(self, username, password):
        self.ent_username.delete(0, "end")
        self.ent_username.insert(0, username)
        self.ent_password.delete(0, "end")
        self.ent_password.insert(0, password)
        self.do_login()

    def do_login(self):
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()
        
        if not username or not password:
            self.show_error("Please enter both username and password.")
            return
            
        user = authenticate_user(username, password)
        if not user:
            self.show_error("Invalid username or password. Please try again.")
            return
            
        self.lbl_err.configure(text="")
        if self.on_login_success:
            self.on_login_success(user)

    def show_error(self, message):
        self.lbl_err.configure(text=f"⚠️ {message}")
