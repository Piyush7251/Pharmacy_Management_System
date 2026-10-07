"""
AegisPharm Enterprise — Secure Authentication & Role-Based Login Screen.
Authenticates users against the database and passes user profile & role to the main application orchestrator.
"""

import customtkinter as ctk
from ui.theme import COLORS, FONTS
from core.db import authenticate_user

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, on_login_success_cb):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.on_login_success = on_login_success_cb
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()

    def setup_ui(self):
        # Center container card
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
        
        # 1. Branding Header
        brand_box = ctk.CTkFrame(center_card, fg_color="transparent")
        brand_box.grid(row=0, column=0, sticky="ew", padx=30, pady=(32, 16))
        
        lbl_logo = ctk.CTkLabel(
            brand_box,
            text="💊 AegisPharm Enterprise",
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
            text="Please authenticate with your assigned credentials to access your terminal dashboard.",
            font=FONTS["small"],
            text_color=COLORS["text_dim"],
            wraplength=400,
            justify="center"
        )
        lbl_instr.pack(anchor="center", pady=(8, 0))
        
        # 2. Error / Feedback Banner
        self.err_banner = ctk.CTkFrame(center_card, fg_color="transparent", height=0)
        self.err_banner.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 8))
        self.lbl_err = ctk.CTkLabel(self.err_banner, text="", font=FONTS["small_bold"], text_color=COLORS["danger"])
        self.lbl_err.pack(pady=4)
        
        # 3. Form Inputs
        form_box = ctk.CTkFrame(center_card, fg_color="transparent")
        form_box.grid(row=2, column=0, sticky="ew", padx=30, pady=0)
        form_box.grid_columnconfigure(0, weight=1)
        
        # Username
        lbl_u = ctk.CTkLabel(form_box, text="Username or Staff ID", font=FONTS["body_bold"], text_color=COLORS["text_main"])
        lbl_u.grid(row=0, column=0, sticky="w", pady=(0, 4))
        
        self.ent_username = ctk.CTkEntry(
            form_box,
            placeholder_text="e.g., admin, pharmacist, cashier",
            font=FONTS["body"],
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            height=42
        )
        self.ent_username.grid(row=1, column=0, sticky="ew", pady=(0, 14))
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
            border_color=COLORS["border"],
            height=42
        )
        self.ent_password.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        self.ent_password.bind("<Return>", lambda e: self.do_login())
        
        # Login Button
        self.btn_login = ctk.CTkButton(
            form_box,
            text="🔓 Sign In to Dashboard",
            height=44,
            font=FONTS["body_bold"],
            fg_color=COLORS["clinical"],
            hover_color=COLORS["clinical_hover"],
            command=self.do_login
        )
        self.btn_login.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        
        # 4. Quick Demo Role Selector
        demo_box = ctk.CTkFrame(center_card, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        demo_box.grid(row=3, column=0, sticky="ew", padx=30, pady=(0, 30))
        
        lbl_demo = ctk.CTkLabel(demo_box, text="⚡ Quick Demo Role Logins (Single-Click Test):", font=FONTS["small_bold"], text_color=COLORS["text_dim"])
        lbl_demo.pack(anchor="w", padx=14, pady=(10, 6))
        
        btn_grid = ctk.CTkFrame(demo_box, fg_color="transparent")
        btn_grid.pack(fill="x", padx=10, pady=(0, 10))
        btn_grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        roles = [
            ("👑 Admin", "admin", "admin123", COLORS["warning"]),
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
                fg_color=COLORS["bg_surface_alt"],
                hover_color=COLORS["border_light"],
                text_color=col,
                font=FONTS["small_bold"],
                command=lambda u=uname, p=pwd: self.fill_and_login(u, p)
            )
            b.grid(row=r, column=c, padx=4, pady=4, sticky="ew")

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
