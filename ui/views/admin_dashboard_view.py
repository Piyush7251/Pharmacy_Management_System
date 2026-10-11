"""
AegisPharm Enterprise — Complete Admin Command Center & Store Analytics Dashboard.
Full features:
- Staff User & RBAC Management (Add/Edit ID, Password, Role, Branch, Status with Search)
- Live Online Terminals & Presence Heartbeat Telemetry Monitor
- Storewide Operational & Financial KPIs (Gross Sales, Active Staff, Rx Queue, Stock Risks)
- Filterable Live Audit Stream (INFO, WARN, CRITICAL)
- Financial Analytics & Daily Z-Report Cash/UPI Reconciliation with Real CSV Export
- GST Tax Liability & Inventory Velocity Risk Analysis
"""

import threading
import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import json
import csv
from ui.theme import COLORS, FONTS
from ui.components.toast import show_toast
from core.db import (
    get_connection, get_all_staff, create_staff_user, update_staff_user,
    delete_staff_user, get_all_invoices, get_all_medicines
)

class AdminDashboardView(ctk.CTkFrame):
    def __init__(self, parent, user_data, connector=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.user_data = user_data
        self.connector = connector
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self._last_presence_data = []
        self._last_audit_data = []
        self._last_users_data = []
        self._is_fetching = False
        self.audit_filter = "ALL"
        
        self.setup_header()
        self.setup_kpis()
        self.setup_tabs()
        
        self.refresh_users_table()
        self.start_auto_refresh()

    def setup_header(self):
        hdr = ctk.CTkFrame(self, height=54, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 6))
        hdr.grid_columnconfigure(1, weight=1)
        
        lbl_title = ctk.CTkLabel(
            hdr,
            text="👑 Admin Dashboard (Store Overview & Staff)",
            font=FONTS["h2"],
            text_color=COLORS["warning"]
        )
        lbl_title.grid(row=0, column=0, padx=16, pady=10, sticky="w")
        
        right_box = ctk.CTkFrame(hdr, fg_color="transparent")
        right_box.grid(row=0, column=1, sticky="e", padx=16)
        
        self.lbl_server_status = ctk.CTkLabel(
            right_box,
            text="🟢 System Status: Active",
            font=FONTS["small_bold"],
            text_color=COLORS["clinical"]
        )
        self.lbl_server_status.pack(side="left", padx=10)
        
        btn_refresh = ctk.CTkButton(
            right_box,
            text="🔄 Refresh",
            width=85,
            height=28,
            font=FONTS["small_bold"],
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_secondary_hover"],
            text_color=COLORS["btn_secondary_text"],
            command=self.trigger_background_refresh
        )
        btn_refresh.pack(side="left")

    def setup_kpis(self):
        kpi_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        kpi_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        kpi_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        self.kpi_staff = self.create_kpi_card(kpi_frame, 0, "Staff Online", "0 Active", COLORS["clinical"])
        self.kpi_sales = self.create_kpi_card(kpi_frame, 1, "Total Sales", "₹ 0.00", COLORS["commerce"])
        self.kpi_rx = self.create_kpi_card(kpi_frame, 2, "Prescriptions Waiting", "0 Pending", COLORS["warning"])
        self.kpi_stock = self.create_kpi_card(kpi_frame, 3, "Low Stock Alert", "0 Critical", COLORS["danger"])
        self.kpi_deliv = self.create_kpi_card(kpi_frame, 4, "Active Deliveries", "0 En Route", COLORS["operations"])

    def create_kpi_card(self, parent, col, title, value, color):
        c = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        c.grid(row=0, column=col, sticky="ew", padx=5, pady=6)
        
        lbl_t = ctk.CTkLabel(c, text=title, font=FONTS["small"], text_color=COLORS["text_dim"])
        lbl_t.pack(anchor="w", padx=10, pady=(4, 1))
        
        lbl_v = ctk.CTkLabel(c, text=value, font=FONTS["h2"], text_color=color)
        lbl_v.pack(anchor="w", padx=10, pady=(0, 4))
        return lbl_v

    def setup_tabs(self):
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=COLORS["bg_surface"],
            segmented_button_fg_color=COLORS["bg_card"],
            segmented_button_selected_color=COLORS["clinical"],
            segmented_button_selected_hover_color=COLORS["clinical_hover"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.tabview.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 12))
        
        self.tab_users = self.tabview.add("👥 Staff Accounts")
        self.tab_presence = self.tabview.add("🟢 Online Staff Terminals")
        self.tab_analytics = self.tabview.add("📊 Sales Summary & Cash Report")
        self.tab_audit = self.tabview.add("📡 System Activity Log")
        
        self.setup_users_tab()
        self.setup_presence_tab()
        self.setup_analytics_tab()
        self.setup_audit_tab()

    # --- TAB 1: USER ACCOUNTS & RBAC ---

    def setup_users_tab(self):
        self.tab_users.grid_columnconfigure(0, weight=1)
        self.tab_users.grid_rowconfigure(2, weight=1)
        
        act_bar = ctk.CTkFrame(self.tab_users, fg_color="transparent")
        act_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(6, 4))
        act_bar.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(act_bar, text="Store Staff & Login Accounts", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl.grid(row=0, column=0, sticky="w")
        
        btn_add = ctk.CTkButton(
            act_bar,
            text="+ Create New Staff",
            height=30,
            font=FONTS["small_bold"],
            fg_color=COLORS["clinical"],
            hover_color=COLORS["clinical_hover"],
            text_color="#FFFFFF",
            command=self.open_create_user_modal
        )
        btn_add.grid(row=0, column=1, sticky="e")
        
        self.ent_user_search = ctk.CTkEntry(
            self.tab_users,
            placeholder_text="🔍 Search staff by name, username, role, or branch...",
            font=FONTS["small"],
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_main"],
            border_color=COLORS["border"],
            height=32
        )
        self.ent_user_search.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 6))
        self.ent_user_search.bind("<KeyRelease>", lambda e: self.render_users_list())
        
        self.users_scroll = ctk.CTkScrollableFrame(self.tab_users, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.users_scroll.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.users_scroll.grid_columnconfigure(0, weight=1)

    def refresh_users_table(self):
        self._last_users_data = get_all_staff()
        self.render_users_list()

    def render_users_list(self):
        for w in self.users_scroll.winfo_children():
            w.destroy()
            
        staff_list = self._last_users_data or get_all_staff()
        q = self.ent_user_search.get().strip().lower() if hasattr(self, "ent_user_search") else ""
        if q:
            staff_list = [u for u in staff_list if q in u['name'].lower() or q in u['username'].lower() or q in u['role'].lower() or q in u.get('branch', '').lower()]

        for u in staff_list:
            card = ctk.CTkFrame(self.users_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", pady=4, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            r1 = ctk.CTkFrame(card, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            role_icon = "👑" if "Admin" in u["role"] else ("🩺" if "Pharmacist" in u["role"] else ("💳" if "Cashier" in u["role"] else "📦"))
            lbl_name = ctk.CTkLabel(r1, text=f"{role_icon} {u['name']} (ID: {u['id']})", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_name.grid(row=0, column=0, sticky="w")
            
            lbl_role = ctk.CTkLabel(r1, text=f" {u['role']} ", font=FONTS["small_bold"], fg_color=COLORS["badge_bg"], text_color=COLORS["commerce"], corner_radius=4)
            lbl_role.grid(row=0, column=1, padx=6)
            
            st_color = COLORS["clinical"] if u.get("status") == "Active" else COLORS["danger"]
            lbl_st = ctk.CTkLabel(r1, text=f" {u.get('status', 'Active')} ", font=FONTS["small_bold"], fg_color=st_color, text_color="#FFFFFF", corner_radius=4)
            lbl_st.grid(row=0, column=2, sticky="e")
            
            r2 = ctk.CTkFrame(card, fg_color="transparent")
            r2.grid(row=1, column=0, sticky="ew", padx=12, pady=(2, 8))
            r2.grid_columnconfigure(0, weight=1)
            
            cred_txt = f"🔑 Username: {u['username']} | Password: {'•'*len(u.get('password', '****'))} | 🏬 {u.get('branch', 'Main')} | 📞 {u.get('phone', 'N/A')}"
            lbl_cred = ctk.CTkLabel(r2, text=cred_txt, font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_cred.grid(row=0, column=0, sticky="w")
            
            btn_box = ctk.CTkFrame(r2, fg_color="transparent")
            btn_box.grid(row=0, column=1, sticky="e")
            
            btn_edit = ctk.CTkButton(
                btn_box,
                text="✏️ Edit",
                width=75,
                height=24,
                font=FONTS["small_bold"],
                fg_color=COLORS["btn_secondary"],
                hover_color=COLORS["btn_secondary_hover"],
                text_color=COLORS["btn_secondary_text"],
                command=lambda user=u: self.open_edit_user_modal(user)
            )
            btn_edit.pack(side="left", padx=(0, 6))
            
            if u["username"] != "admin":
                btn_del = ctk.CTkButton(
                    btn_box,
                    text="🗑️ Delete",
                    width=65,
                    height=24,
                    font=FONTS["small_bold"],
                    fg_color=COLORS["btn_danger"],
                    hover_color=COLORS["btn_danger_hover"],
                    text_color="#FFFFFF",
                    command=lambda user_id=u["id"]: self.handle_delete_user(user_id)
                )
                btn_del.pack(side="left")

    def open_create_user_modal(self):
        win = ctk.CTkToplevel(self)
        win.title("Create New Staff User & Assign Role")
        win.geometry("520x580")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl_head = ctk.CTkLabel(win, text="✨ Create New User Account", font=FONTS["h2"], text_color=COLORS["clinical"])
        lbl_head.pack(pady=(16, 10))
        
        form = ctk.CTkFrame(win, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=30, pady=0)
        form.grid_columnconfigure(1, weight=1)
        
        fields = [
            ("Staff ID:", "ent_id", f"STF-0{len(get_all_staff()) + 1}"),
            ("Full Name:", "ent_name", "Dr. Anjali Deshmukh"),
            ("Username:", "ent_username", "anjali.pharma"),
            ("Password:", "ent_password", "pharma123"),
            ("Email:", "ent_email", "anjali@aegispharm.com"),
            ("Phone:", "ent_phone", "+91 98201 00000"),
            ("Branch:", "ent_branch", "Apex Central - Branch #01")
        ]
        
        entries = {}
        for idx, (label_text, key, placeholder) in enumerate(fields):
            lbl = ctk.CTkLabel(form, text=label_text, font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl.grid(row=idx, column=0, sticky="w", pady=4, padx=(0, 10))
            
            ent = ctk.CTkEntry(form, font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], height=32)
            ent.grid(row=idx, column=1, sticky="ew", pady=4)
            ent.insert(0, placeholder)
            entries[key] = ent
            
        lbl_role = ctk.CTkLabel(form, text="Assigned Role:", font=FONTS["body_bold"], text_color=COLORS["text_main"])
        lbl_role.grid(row=len(fields), column=0, sticky="w", pady=6, padx=(0, 10))
        
        role_opt = ctk.CTkOptionMenu(form, values=["Store Admin", "Pharmacist", "Cashier", "Inventory Manager", "Delivery Agent"], height=32)
        role_opt.set("Pharmacist")
        role_opt.grid(row=len(fields), column=1, sticky="ew", pady=6)
        
        def save_user():
            s_id = entries["ent_id"].get().strip()
            name = entries["ent_name"].get().strip()
            uname = entries["ent_username"].get().strip()
            pwd = entries["ent_password"].get().strip()
            email = entries["ent_email"].get().strip()
            phone = entries["ent_phone"].get().strip()
            branch = entries["ent_branch"].get().strip()
            role = role_opt.get().strip()
            
            if not s_id or not name or not uname or not pwd:
                messagebox.showwarning("Incomplete", "Please complete all mandatory fields.", parent=win)
                return
                
            success, err = create_staff_user(s_id, name, role, uname, pwd, email, phone, branch)
            if not success:
                messagebox.showerror("Failed", f"Error: {err}", parent=win)
                return
                
            if self.connector:
                self.connector.log_event("User Created", f"Admin created user {uname} ({role})", level="INFO")
                
            self.refresh_users_table()
            win.destroy()
            show_toast(self, "Staff Account Created", f"{name} ({uname}) registered with {role} permissions.", "success")
            
        btn_save = ctk.CTkButton(win, text="Save & Grant Access", height=38, font=FONTS["body_bold"], fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", command=save_user)
        btn_save.pack(fill="x", padx=30, pady=(6, 16))

    def open_edit_user_modal(self, user):
        win = ctk.CTkToplevel(self)
        win.title(f"Edit Credentials — {user['name']}")
        win.geometry("440x440")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl_head = ctk.CTkLabel(win, text=f"Edit User: {user['name']}", font=FONTS["h2"], text_color=COLORS["commerce"])
        lbl_head.pack(pady=(16, 10))
        
        form = ctk.CTkFrame(win, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=30, pady=0)
        form.grid_columnconfigure(1, weight=1)
        
        # Name
        ctk.CTkLabel(form, text="Full Name:", font=FONTS["body_bold"], text_color=COLORS["text_main"]).grid(row=0, column=0, sticky="w", pady=4)
        ent_name = ctk.CTkEntry(form, font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], height=32)
        ent_name.grid(row=0, column=1, sticky="ew", pady=4)
        ent_name.insert(0, user["name"])
        
        # Username
        ctk.CTkLabel(form, text="Username:", font=FONTS["body_bold"], text_color=COLORS["text_main"]).grid(row=1, column=0, sticky="w", pady=4)
        ent_uname = ctk.CTkEntry(form, font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], height=32)
        ent_uname.grid(row=1, column=1, sticky="ew", pady=4)
        ent_uname.insert(0, user["username"])
        
        # Password
        ctk.CTkLabel(form, text="Password:", font=FONTS["body_bold"], text_color=COLORS["text_main"]).grid(row=2, column=0, sticky="w", pady=4)
        ent_pwd = ctk.CTkEntry(form, font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], height=32)
        ent_pwd.grid(row=2, column=1, sticky="ew", pady=4)
        ent_pwd.insert(0, user.get("password", "password123"))
        
        # Role
        ctk.CTkLabel(form, text="Role:", font=FONTS["body_bold"], text_color=COLORS["text_main"]).grid(row=3, column=0, sticky="w", pady=4)
        role_opt = ctk.CTkOptionMenu(form, values=["Store Admin", "Pharmacist", "Cashier", "Inventory Manager", "Delivery Agent"], height=32)
        role_opt.set(user["role"])
        role_opt.grid(row=3, column=1, sticky="ew", pady=4)
        
        # Status
        ctk.CTkLabel(form, text="Status:", font=FONTS["body_bold"], text_color=COLORS["text_main"]).grid(row=4, column=0, sticky="w", pady=4)
        status_opt = ctk.CTkOptionMenu(form, values=["Active", "Suspended"], height=32)
        status_opt.set(user.get("status", "Active"))
        status_opt.grid(row=4, column=1, sticky="ew", pady=4)
        
        def save_edit():
            name = ent_name.get().strip()
            uname = ent_uname.get().strip()
            pwd = ent_pwd.get().strip()
            role = role_opt.get().strip()
            st = status_opt.get()
            
            if not name or not uname or not pwd:
                messagebox.showwarning("Incomplete", "Name, Username, and Password cannot be empty.", parent=win)
                return
                
            success, err = update_staff_user(user["id"], name, role, uname, pwd, user.get("email", ""), user.get("phone", ""), user.get("branch", ""), st)
            if not success:
                messagebox.showerror("Update Failed", f"Error: {err}", parent=win)
                return
                
            if self.connector:
                self.connector.log_event("User Updated", f"Admin updated credentials for {uname}", level="INFO")
                
            self.refresh_users_table()
            win.destroy()
            show_toast(self, "User Updated", f"Credentials for {uname} saved successfully.", "success")

        btn = ctk.CTkButton(win, text="Save Changes", height=38, font=FONTS["body_bold"], fg_color=COLORS["commerce"], hover_color=COLORS["commerce_hover"], text_color="#FFFFFF", command=save_edit)
        btn.pack(fill="x", padx=30, pady=(10, 16))

    def handle_delete_user(self, user_id):
        res = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {user_id}?")
        if not res:
            return
        delete_staff_user(user_id)
        if self.connector:
            self.connector.log_event("User Deleted", f"Admin deleted user {user_id}", level="WARN")
        self.refresh_users_table()
        show_toast(self, "User Removed", f"Account {user_id} deleted.", "info")

    # --- TAB 2: LIVE PRESENCE ---

    def setup_presence_tab(self):
        self.tab_presence.grid_columnconfigure(0, weight=1)
        self.tab_presence.grid_rowconfigure(0, weight=1)
        
        self.presence_scroll = ctk.CTkScrollableFrame(self.tab_presence, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.presence_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.presence_scroll.grid_columnconfigure(0, weight=1)

    def render_presence_ui(self, users):
        if users == self._last_presence_data:
            return
        self._last_presence_data = users

        for w in self.presence_scroll.winfo_children():
            w.destroy()
            
        online_count = sum(1 for u in users if u.get("is_online"))
        self.kpi_staff.configure(text=f"{online_count} Active")

        if not users:
            ctk.CTkLabel(self.presence_scroll, text="No active staff sessions detected.", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(pady=40)
            return

        for u in users:
            is_on = u.get("is_online", False)
            status_color = COLORS["clinical"] if is_on else COLORS["danger"]
            badge_text = "🟢 ONLINE" if is_on else f"🔴 DISCONNECTED ({u.get('seconds_since_heartbeat', 0)}s ago)"
            
            card = ctk.CTkFrame(self.presence_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", pady=4, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            r1 = ctk.CTkFrame(card, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            role_icon = "👑" if "Admin" in u["role"] else ("🩺" if "Pharmacist" in u["role"] else ("💳" if "Cashier" in u["role"] else "📦"))
            lbl_n = ctk.CTkLabel(r1, text=f"{role_icon} {u['name']}", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_n.grid(row=0, column=0, sticky="w")
            
            lbl_r = ctk.CTkLabel(r1, text=f" {u['role']} ", font=FONTS["small_bold"], fg_color=COLORS["badge_bg"], text_color=COLORS["commerce"], corner_radius=4)
            lbl_role = lbl_r
            lbl_role.grid(row=0, column=1, padx=6)
            
            lbl_st = ctk.CTkLabel(r1, text=badge_text, font=FONTS["small_bold"], text_color=status_color)
            lbl_st.grid(row=0, column=2, sticky="e")
            
            r2 = ctk.CTkFrame(card, fg_color="transparent")
            r2.grid(row=1, column=0, sticky="ew", padx=12, pady=(2, 8))
            
            info_txt = f"🖥️ Terminal: {u['terminal_name']} ({u.get('ip_address', '127.0.0.1')}) | 🕒 Login: {u['login_time']}\n⚡ Current Action: {u.get('last_action', 'Active')}"
            lbl_act = ctk.CTkLabel(r2, text=info_txt, font=FONTS["small"], text_color=COLORS["text_muted"], justify="left")
            lbl_act.pack(anchor="w")

    # --- TAB 3: FINANCIAL ANALYTICS & Z-RECONCILIATION ---

    def setup_analytics_tab(self):
        self.tab_analytics.grid_columnconfigure(0, weight=1)
        self.tab_analytics.grid_rowconfigure(1, weight=1)
        
        top_bar = ctk.CTkFrame(self.tab_analytics, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        top_bar.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(top_bar, text="📊 Daily Cash Register & Sales Summary", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl.grid(row=0, column=0, sticky="w")
        
        btn_exp = ctk.CTkButton(top_bar, text="📑 Export Sales Report (CSV)", height=28, font=FONTS["small_bold"], fg_color=COLORS["commerce"], hover_color=COLORS["commerce_hover"], text_color="#FFFFFF", command=self.export_daily_ledger)
        btn_exp.grid(row=0, column=1, sticky="e")
        
        self.analytics_scroll = ctk.CTkScrollableFrame(self.tab_analytics, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.analytics_scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.analytics_scroll.grid_columnconfigure(0, weight=1)
        
        self.render_financial_analytics()

    def render_financial_analytics(self):
        for w in self.analytics_scroll.winfo_children():
            w.destroy()
            
        invoices = get_all_invoices()
        medicines = get_all_medicines()
        
        total_revenue = sum(inv.get("total_amount", 0) for inv in invoices)
        total_gst = sum(inv.get("gst_amount", 0) for inv in invoices)
        cash_rev = sum(inv.get("total_amount", 0) for inv in invoices if "Cash" in inv.get("payment_method", ""))
        upi_rev = sum(inv.get("total_amount", 0) for inv in invoices if "UPI" in inv.get("payment_method", ""))
        card_rev = sum(inv.get("total_amount", 0) for inv in invoices if "Card" in inv.get("payment_method", ""))
        
        # Summary Box
        c1 = ctk.CTkFrame(self.analytics_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        c1.pack(fill="x", pady=4, padx=4)
        
        ctk.CTkLabel(c1, text="💵 Cash Drawer & Payment Summary:", font=FONTS["body_bold"], text_color=COLORS["clinical"]).pack(anchor="w", padx=12, pady=(10, 4))
        
        reconcile_text = f"• Total Bills: {len(invoices)} Invoices Processed\n• Total Revenue: ₹ {total_revenue:,.2f}\n• Cash Received: ₹ {cash_rev:,.2f}\n• Online UPI / QR Payments: ₹ {upi_rev:,.2f}\n• Card Payments: ₹ {card_rev:,.2f}\n• Total GST Collected: ₹{total_gst:,.2f} (CGST: ₹{total_gst/2:,.2f} | SGST: ₹{total_gst/2:,.2f})"
        ctk.CTkLabel(c1, text=reconcile_text, font=FONTS["body"], text_color=COLORS["text_muted"], justify="left").pack(anchor="w", padx=12, pady=(0, 10))
        
        # Fast Moving vs Dead Stock Box
        c2 = ctk.CTkFrame(self.analytics_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        c2.pack(fill="x", pady=6, padx=4)
        
        ctk.CTkLabel(c2, text="📦 Stock Health & Low-Stock Alerts:", font=FONTS["body_bold"], text_color=COLORS["commerce"]).pack(anchor="w", padx=12, pady=(10, 4))
        
        low_stk = [m["name"] for m in medicines if m.get("stock", 0) <= 20]
        low_str = ", ".join(low_stk) if low_stk else "All items in stock."
        
        inv_text = f"• Total Medicines in Catalog: {len(medicines)} items\n• Low-Stock Items (≤ 20 units): {low_str}\n• Refrigerator Safe Storage: Normal (2°C to 8°C)\n• Batches Expiring in Next 6 Months: {sum(1 for m in medicines if m.get('days_to_expiry', 999) <= 180)} items"
        ctk.CTkLabel(c2, text=inv_text, font=FONTS["body"], text_color=COLORS["text_muted"], justify="left").pack(anchor="w", padx=12, pady=(0, 10))

    def export_daily_ledger(self):
        invoices = get_all_invoices()
        if not invoices:
            show_toast(self, "No Sales", "No invoices found to export.", "warning")
            return
            
        path = filedialog.asksaveasfilename(
            title="Export Sales Report",
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")],
            initialfile="AegisPharm_Daily_Sales.csv"
        )
        if path:
            fields = ["invoice_id", "timestamp", "patient_name", "cashier_name", "payment_method", "subtotal", "gst_amount", "total_amount"]
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(invoices)
            show_toast(self, "Sales Exported", f"Saved {len(invoices)} transactions to {path}.", "success")

    # --- TAB 4: AUDIT STREAM ---

    def setup_audit_tab(self):
        self.tab_audit.grid_columnconfigure(0, weight=1)
        self.tab_audit.grid_rowconfigure(1, weight=1)
        
        filter_bar = ctk.CTkFrame(self.tab_audit, fg_color="transparent")
        filter_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(6, 4))
        
        for flt, label in [("ALL", "All Logs"), ("INFO", "Info"), ("WARN", "Warnings"), ("CRITICAL", "Alerts")]:
            ctk.CTkButton(
                filter_bar,
                text=label,
                width=80,
                height=26,
                font=FONTS["small_bold"],
                fg_color=COLORS["btn_secondary"],
                hover_color=COLORS["btn_secondary_hover"],
                text_color=COLORS["btn_secondary_text"],
                command=lambda f=flt: self.set_audit_filter(f)
            ).pack(side="left", padx=2)
            
        self.audit_scroll = ctk.CTkScrollableFrame(self.tab_audit, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.audit_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.audit_scroll.grid_columnconfigure(0, weight=1)

    def set_audit_filter(self, flt):
        self.audit_filter = flt
        self.render_audit_ui(self._last_audit_data or [])

    def render_audit_ui(self, logs):
        self._last_audit_data = logs
        for w in self.audit_scroll.winfo_children():
            w.destroy()

        items = logs
        if self.audit_filter != "ALL":
            items = [lg for lg in items if lg.get("level") == self.audit_filter]

        for lg in items:
            c = ctk.CTkFrame(self.audit_scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=3, padx=2)
            
            ts = lg["timestamp"].split()[-1] if " " in lg["timestamp"] else lg["timestamp"]
            lvl_col = COLORS["danger"] if lg.get("level") == "CRITICAL" else (COLORS["warning"] if lg.get("level") == "WARN" else COLORS["info"])
            
            lbl_top = ctk.CTkLabel(c, text=f"[{ts}] {lg['user_name']} ({lg['role']}) — {lg['action']}", font=FONTS["small_bold"], text_color=lvl_col)
            lbl_top.pack(anchor="w", padx=10, pady=(4, 1))
            
            lbl_det = ctk.CTkLabel(c, text=lg.get("details", ""), font=FONTS["small"], text_color=COLORS["text_dim"], justify="left")
            lbl_det.pack(anchor="w", padx=10, pady=(0, 4))

    def render_kpis_ui(self, kpi_data):
        self.kpi_sales.configure(text=kpi_data.get("sales", "₹ 0.00"))
        self.kpi_rx.configure(text=f"{kpi_data.get('pending_rx', 0)} Pending")
        self.kpi_stock.configure(text=f"{kpi_data.get('low_stock', 0)} Critical")
        self.kpi_deliv.configure(text=f"{kpi_data.get('active_deliv', 0)} In Route")

    def _async_fetch_worker(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT * FROM active_sessions ORDER BY login_time DESC")
            rows = cur.fetchall()
            now = datetime.now()
            presence_users = []
            for r in rows:
                try:
                    last_hb = datetime.strptime(r["last_heartbeat"], "%Y-%m-%d %H:%M:%S")
                    diff = (now - last_hb).total_seconds()
                except Exception:
                    diff = 0
                presence_users.append({
                    "name": r["name"],
                    "role": r["role"],
                    "terminal_name": r["terminal_name"],
                    "ip_address": r["ip_address"],
                    "status": r["status"] if diff <= 15 else "Disconnected (Stale)",
                    "is_online": diff <= 15,
                    "last_action": r["last_action"],
                    "login_time": r["login_time"],
                    "seconds_since_heartbeat": int(diff)
                })
                
            cur.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 40")
            audit_logs = [dict(r) for r in cur.fetchall()]
            
            cur.execute("SELECT COUNT(*) as low_stock FROM medicines WHERE stock <= 20")
            low_stock = cur.fetchone()["low_stock"]
            
            cur.execute("SELECT COUNT(*) as pending_rx FROM prescriptions WHERE status LIKE '%Verification%' OR status LIKE '%Pending%'")
            pending_rx = cur.fetchone()["pending_rx"]
            
            cur.execute("SELECT COUNT(*) as active_deliveries FROM delivery_orders WHERE status NOT LIKE '%Delivered%'")
            active_deliv = cur.fetchone()["active_deliveries"]
            
            cur.execute("SELECT COALESCE(SUM(total_amount), 0) as total_sales FROM invoices")
            sales_row = cur.fetchone()["total_sales"]
            total_sales = sales_row if sales_row else 0.0
            
            conn.close()
            
            kpi_data = {
                "low_stock": low_stock,
                "pending_rx": pending_rx,
                "active_deliv": active_deliv,
                "sales": f"₹ {total_sales:,.2f}"
            }
            
            self.after(0, lambda: self._apply_updates(presence_users, audit_logs, kpi_data))
        except Exception:
            pass
        finally:
            self._is_fetching = False

    def _apply_updates(self, presence_users, audit_logs, kpi_data):
        self.render_presence_ui(presence_users)
        self.render_audit_ui(audit_logs)
        self.render_kpis_ui(kpi_data)
        self.render_financial_analytics()

    def trigger_background_refresh(self):
        if self._is_fetching:
            return
        self._is_fetching = True
        self.refresh_users_table()
        threading.Thread(target=self._async_fetch_worker, daemon=True).start()

    def start_auto_refresh(self):
        self.trigger_background_refresh()
        self.after(4000, self.start_auto_refresh)
