"""
AegisPharm Enterprise — Admin Command Center & Staff User Management Dashboard.
Enables Admin to manage staff user accounts (create/edit user ID, password, role),
monitor real-time online presence/terminals, inspect audit logs, and view storewide KPIs.
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import json
import requests
from ui.theme import COLORS, FONTS
from core.db import get_connection, get_all_staff, create_staff_user, update_staff_user, delete_staff_user

class AdminDashboardView(ctk.CTkFrame):
    def __init__(self, parent, user_data, connector=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.user_data = user_data
        self.connector = connector
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.setup_header()
        self.setup_kpis()
        self.setup_tabs()
        
        self.start_auto_refresh()

    def setup_header(self):
        hdr = ctk.CTkFrame(self, height=60, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        hdr.grid_columnconfigure(1, weight=1)
        
        lbl_title = ctk.CTkLabel(
            hdr,
            text="👑 Admin Command Center & System Management",
            font=FONTS["h2"],
            text_color=COLORS["warning"]
        )
        lbl_title.grid(row=0, column=0, padx=16, pady=12, sticky="w")
        
        right_box = ctk.CTkFrame(hdr, fg_color="transparent")
        right_box.grid(row=0, column=1, sticky="e", padx=16)
        
        self.lbl_server_status = ctk.CTkLabel(
            right_box,
            text="🟢 Gateway Server: Connected",
            font=FONTS["small_bold"],
            text_color=COLORS["clinical"]
        )
        self.lbl_server_status.pack(side="left", padx=10)
        
        btn_refresh = ctk.CTkButton(
            right_box,
            text="🔄 Refresh All",
            width=100,
            height=30,
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_secondary_hover"],
            font=FONTS["small_bold"],
            command=self.refresh_all
        )
        btn_refresh.pack(side="left")

    def setup_kpis(self):
        kpi_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        kpi_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 10))
        kpi_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        self.kpi_staff = self.create_kpi_card(kpi_frame, 0, "Online Staff / Terminals", "0 Active", COLORS["clinical"])
        self.kpi_sales = self.create_kpi_card(kpi_frame, 1, "Today's Gross Sales", "₹ 48,920.50", COLORS["commerce"])
        self.kpi_rx = self.create_kpi_card(kpi_frame, 2, "Pending Rx Checks", "3 Pending", COLORS["warning"])
        self.kpi_stock = self.create_kpi_card(kpi_frame, 3, "Low Stock Alerts", "4 Critical", COLORS["danger"])
        self.kpi_deliv = self.create_kpi_card(kpi_frame, 4, "Active Delivery Routes", "3 Dispatched", COLORS["operations"])

    def create_kpi_card(self, parent, col, title, value, color):
        c = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        c.grid(row=0, column=col, sticky="ew", padx=6, pady=8)
        
        lbl_t = ctk.CTkLabel(c, text=title, font=FONTS["small"], text_color=COLORS["text_dim"])
        lbl_t.pack(anchor="w", padx=10, pady=(6, 2))
        
        lbl_v = ctk.CTkLabel(c, text=value, font=FONTS["h2"], text_color=color)
        lbl_v.pack(anchor="w", padx=10, pady=(0, 6))
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
        self.tabview.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))
        
        # Tabs
        self.tab_users = self.tabview.add("👥 Staff & User Management")
        self.tab_presence = self.tabview.add("🟢 Live Online Presence")
        self.tab_audit = self.tabview.add("📡 Live Audit Stream")
        
        self.setup_users_tab()
        self.setup_presence_tab()
        self.setup_audit_tab()

    # --- TAB 1: USER & ROLE MANAGEMENT ---

    def setup_users_tab(self):
        self.tab_users.grid_columnconfigure(0, weight=1)
        self.tab_users.grid_rowconfigure(1, weight=1)
        
        # Action Bar
        act_bar = ctk.CTkFrame(self.tab_users, fg_color="transparent")
        act_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 8))
        act_bar.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(
            act_bar,
            text="Manage Staff Credentials, Roles & Terminal Permissions",
            font=FONTS["h3"],
            text_color=COLORS["text_main"]
        )
        lbl.grid(row=0, column=0, sticky="w")
        
        btn_add = ctk.CTkButton(
            act_bar,
            text="+ Create New User",
            height=34,
            font=FONTS["body_bold"],
            fg_color=COLORS["clinical"],
            hover_color=COLORS["clinical_hover"],
            command=self.open_create_user_modal
        )
        btn_add.grid(row=0, column=1, sticky="e")
        
        # Users Scrollable List
        self.users_scroll = ctk.CTkScrollableFrame(self.tab_users, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.users_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.users_scroll.grid_columnconfigure(0, weight=1)
        
        self.refresh_users_table()

    def refresh_users_table(self):
        for w in self.users_scroll.winfo_children():
            w.destroy()
            
        staff_list = get_all_staff()
        if not staff_list:
            lbl_empty = ctk.CTkLabel(self.users_scroll, text="No users found.", font=FONTS["body"], text_color=COLORS["text_dim"])
            lbl_empty.pack(pady=40)
            return

        for u in staff_list:
            card = ctk.CTkFrame(self.users_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", pady=4, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            # Row 1: Name, Role Badge, Status
            r1 = ctk.CTkFrame(card, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            role_icon = "👑" if "Admin" in u["role"] else ("🩺" if "Pharmacist" in u["role"] else ("💳" if "Cashier" in u["role"] else "📦"))
            lbl_name = ctk.CTkLabel(r1, text=f"{role_icon} {u['name']} (ID: {u['id']})", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_name.grid(row=0, column=0, sticky="w")
            
            lbl_role = ctk.CTkLabel(r1, text=f" {u['role']} ", font=FONTS["small_bold"], fg_color=COLORS["badge_bg"], text_color=COLORS["commerce"], corner_radius=4)
            lbl_role.grid(row=0, column=1, padx=6)
            
            st_color = COLORS["clinical"] if u.get("status") == "Active" else COLORS["danger"]
            lbl_st = ctk.CTkLabel(r1, text=f" {u.get('status', 'Active')} ", font=FONTS["small_bold"], fg_color=st_color, text_color="#000000", corner_radius=4)
            lbl_st.grid(row=0, column=2, sticky="e")
            
            # Row 2: Credentials info & Contacts
            r2 = ctk.CTkFrame(card, fg_color="transparent")
            r2.grid(row=1, column=0, sticky="ew", padx=12, pady=(2, 10))
            r2.grid_columnconfigure(0, weight=1)
            
            cred_txt = f"🔑 Username: {u['username']} | Password: {'•'*len(u.get('password', '****'))} | 🏬 {u.get('branch', 'Main')} | 📞 {u.get('phone', 'N/A')}"
            lbl_cred = ctk.CTkLabel(r2, text=cred_txt, font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_cred.grid(row=0, column=0, sticky="w")
            
            # Action Buttons
            btn_box = ctk.CTkFrame(r2, fg_color="transparent")
            btn_box.grid(row=0, column=1, sticky="e")
            
            btn_edit = ctk.CTkButton(
                btn_box,
                text="✏️ Edit Credentials",
                width=110,
                height=26,
                fg_color=COLORS["btn_secondary"],
                hover_color=COLORS["btn_secondary_hover"],
                font=FONTS["small"],
                command=lambda user=u: self.open_edit_user_modal(user)
            )
            btn_edit.pack(side="left", padx=(0, 6))
            
            if u["username"] != "admin":
                btn_del = ctk.CTkButton(
                    btn_box,
                    text="🗑️ Delete",
                    width=70,
                    height=26,
                    fg_color=COLORS["btn_danger"],
                    hover_color=COLORS["btn_danger_hover"],
                    font=FONTS["small"],
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
        lbl_head.pack(pady=(20, 10))
        
        # Form Container
        form = ctk.CTkFrame(win, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=30, pady=0)
        form.grid_columnconfigure(1, weight=1)
        
        fields = [
            ("Staff ID:", "ent_id", f"STF-0{len(get_all_staff()) + 1}"),
            ("Full Name:", "ent_name", "e.g., Dr. Anjali Deshmukh"),
            ("Username:", "ent_username", "e.g., anjali.pharma"),
            ("Password:", "ent_password", "Assign password"),
            ("Email:", "ent_email", "staff@aegispharm.com"),
            ("Phone:", "ent_phone", "+91 98201 00000"),
            ("Branch:", "ent_branch", "Apex Central - Branch #01")
        ]
        
        entries = {}
        for idx, (label_text, key, placeholder) in enumerate(fields):
            lbl = ctk.CTkLabel(form, text=label_text, font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl.grid(row=idx, column=0, sticky="w", pady=6, padx=(0, 10))
            
            ent = ctk.CTkEntry(form, placeholder_text=placeholder, font=FONTS["body"], fg_color=COLORS["bg_input"], height=34)
            ent.grid(row=idx, column=1, sticky="ew", pady=6)
            if key == "ent_id":
                ent.insert(0, placeholder)
            entries[key] = ent

        # Role Selector
        lbl_role = ctk.CTkLabel(form, text="Assigned Role:", font=FONTS["body_bold"], text_color=COLORS["text_main"])
        lbl_role.grid(row=len(fields), column=0, sticky="w", pady=6, padx=(0, 10))
        
        role_opt = ctk.CTkOptionMenu(
            form,
            values=["Admin", "Pharmacist", "Cashier", "Inventory Manager", "Delivery Agent"],
            fg_color=COLORS["btn_secondary"],
            button_color=COLORS["btn_secondary_hover"],
            font=FONTS["body_bold"],
            height=34
        )
        role_opt.set("Pharmacist")
        role_opt.grid(row=len(fields), column=1, sticky="ew", pady=6)
        
        def save():
            s_id = entries["ent_id"].get().strip()
            name = entries["ent_name"].get().strip()
            uname = entries["ent_username"].get().strip()
            pwd = entries["ent_password"].get().strip()
            email = entries["ent_email"].get().strip()
            phone = entries["ent_phone"].get().strip()
            branch = entries["ent_branch"].get().strip()
            role = role_opt.get()
            
            if not s_id or not name or not uname or not pwd:
                messagebox.showwarning("Incomplete Fields", "Staff ID, Full Name, Username, and Password are required.", parent=win)
                return
                
            success, err = create_staff_user(s_id, name, role, uname, pwd, email, phone, branch)
            if not success:
                messagebox.showerror("Error Creating User", f"Could not create user: {err}", parent=win)
                return
                
            if self.connector:
                self.connector.log_event("User Created", f"Admin created user {uname} ({role})", level="INFO")
                
            self.refresh_users_table()
            win.destroy()
            messagebox.showinfo("User Created", f"Staff user '{name}' ({uname}) created successfully!\nThey can now login with password '{pwd}'.")

        btn_save = ctk.CTkButton(win, text="Save & Create Account", height=40, font=FONTS["body_bold"], fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], command=save)
        btn_save.pack(fill="x", padx=30, pady=(10, 20))

    def open_edit_user_modal(self, user):
        win = ctk.CTkToplevel(self)
        win.title(f"Edit Credentials — {user['name']}")
        win.geometry("500x540")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl_head = ctk.CTkLabel(win, text=f"✏️ Edit Credentials: {user['name']}", font=FONTS["h2"], text_color=COLORS["commerce"])
        lbl_head.pack(pady=(20, 10))
        
        form = ctk.CTkFrame(win, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=30, pady=0)
        form.grid_columnconfigure(1, weight=1)
        
        # Name
        lbl_n = ctk.CTkLabel(form, text="Full Name:", font=FONTS["body_bold"])
        lbl_n.grid(row=0, column=0, sticky="w", pady=6)
        ent_n = ctk.CTkEntry(form, font=FONTS["body"], fg_color=COLORS["bg_input"], height=34)
        ent_n.grid(row=0, column=1, sticky="ew", pady=6)
        ent_n.insert(0, user["name"])
        
        # Username
        lbl_u = ctk.CTkLabel(form, text="Username:", font=FONTS["body_bold"])
        lbl_u.grid(row=1, column=0, sticky="w", pady=6)
        ent_u = ctk.CTkEntry(form, font=FONTS["body"], fg_color=COLORS["bg_input"], height=34)
        ent_u.grid(row=1, column=1, sticky="ew", pady=6)
        ent_u.insert(0, user["username"])
        
        # Password
        lbl_p = ctk.CTkLabel(form, text="New Password:", font=FONTS["body_bold"])
        lbl_p.grid(row=2, column=0, sticky="w", pady=6)
        ent_p = ctk.CTkEntry(form, font=FONTS["body"], fg_color=COLORS["bg_input"], height=34)
        ent_p.grid(row=2, column=1, sticky="ew", pady=6)
        ent_p.insert(0, user.get("password", "password123"))
        
        # Role
        lbl_r = ctk.CTkLabel(form, text="Role:", font=FONTS["body_bold"])
        lbl_r.grid(row=3, column=0, sticky="w", pady=6)
        role_opt = ctk.CTkOptionMenu(form, values=["Admin", "Pharmacist", "Cashier", "Inventory Manager", "Delivery Agent"], height=34)
        role_opt.set(user["role"])
        role_opt.grid(row=3, column=1, sticky="ew", pady=6)
        
        # Status
        lbl_s = ctk.CTkLabel(form, text="Status:", font=FONTS["body_bold"])
        lbl_s.grid(row=4, column=0, sticky="w", pady=6)
        status_opt = ctk.CTkOptionMenu(form, values=["Active", "Suspended"], height=34)
        status_opt.set(user.get("status", "Active"))
        status_opt.grid(row=4, column=1, sticky="ew", pady=6)
        
        def save_edit():
            name = ent_n.get().strip()
            uname = ent_u.get().strip()
            pwd = ent_p.get().strip()
            role = role_opt.get()
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
            messagebox.showinfo("Updated", f"Credentials for {uname} updated successfully!")

        btn = ctk.CTkButton(win, text="Save Changes", height=40, font=FONTS["body_bold"], fg_color=COLORS["commerce"], hover_color=COLORS["commerce_hover"], command=save_edit)
        btn.pack(fill="x", padx=30, pady=(10, 20))

    def handle_delete_user(self, user_id):
        res = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {user_id}?")
        if not res:
            return
        delete_staff_user(user_id)
        if self.connector:
            self.connector.log_event("User Deleted", f"Admin deleted user {user_id}", level="WARN")
        self.refresh_users_table()
        messagebox.showinfo("Deleted", "Staff account removed.")

    # --- TAB 2: LIVE PRESENCE & TERMINALS ---

    def setup_presence_tab(self):
        self.tab_presence.grid_columnconfigure(0, weight=1)
        self.tab_presence.grid_rowconfigure(0, weight=1)
        
        self.presence_scroll = ctk.CTkScrollableFrame(self.tab_presence, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.presence_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.presence_scroll.grid_columnconfigure(0, weight=1)

    def refresh_presence(self):
        users = []
        try:
            res = requests.get("http://127.0.0.1:8000/api/presence/active", timeout=1.0)
            if res.status_code == 200:
                users = res.json()
        except Exception:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM active_sessions ORDER BY login_time DESC")
            rows = cur.fetchall()
            conn.close()
            now = datetime.now()
            for r in rows:
                last_hb = datetime.strptime(r["last_heartbeat"], "%Y-%m-%d %H:%M:%S")
                diff = (now - last_hb).total_seconds()
                users.append({
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

        for w in self.presence_scroll.winfo_children():
            w.destroy()
            
        online_count = sum(1 for u in users if u.get("is_online"))
        self.kpi_staff.configure(text=f"{online_count} Terminals Active")

        if not users:
            lbl_empty = ctk.CTkLabel(self.presence_scroll, text="No active staff sessions detected.", font=FONTS["body"], text_color=COLORS["text_dim"])
            lbl_empty.pack(pady=40)
            return

        for u in users:
            is_on = u.get("is_online", False)
            status_color = COLORS["clinical"] if is_on else COLORS["danger"]
            badge_text = "🟢 ONLINE" if is_on else f"🔴 DISCONNECTED ({u.get('seconds_since_heartbeat', 0)}s ago)"
            
            card = ctk.CTkFrame(self.presence_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", pady=4, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            r1 = ctk.CTkFrame(card, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            role_icon = "👑" if "Admin" in u["role"] else ("🩺" if "Pharmacist" in u["role"] else ("💳" if "Cashier" in u["role"] else "📦"))
            lbl_n = ctk.CTkLabel(r1, text=f"{role_icon} {u['name']}", font=FONTS["body_bold"])
            lbl_n.grid(row=0, column=0, sticky="w")
            
            lbl_r = ctk.CTkLabel(r1, text=f" {u['role']} ", font=FONTS["small_bold"], fg_color=COLORS["badge_bg"], corner_radius=4)
            lbl_r.grid(row=0, column=1, padx=6)
            
            lbl_st = ctk.CTkLabel(r1, text=badge_text, font=FONTS["small_bold"], text_color=status_color)
            lbl_st.grid(row=0, column=2, sticky="e")
            
            r2 = ctk.CTkFrame(card, fg_color="transparent")
            r2.grid(row=1, column=0, sticky="ew", padx=12, pady=(2, 10))
            
            info_txt = f"🖥️ Terminal: {u['terminal_name']} ({u.get('ip_address', '127.0.0.1')}) | 🕒 Logged in: {u['login_time']}\n⚡ Current Action: {u.get('last_action', 'Active')}"
            lbl_act = ctk.CTkLabel(r2, text=info_txt, font=FONTS["small"], text_color=COLORS["text_muted"], justify="left")
            lbl_act.pack(anchor="w")

    # --- TAB 3: AUDIT EVENT STREAM ---

    def setup_audit_tab(self):
        self.tab_audit.grid_columnconfigure(0, weight=1)
        self.tab_audit.grid_rowconfigure(0, weight=1)
        
        self.audit_scroll = ctk.CTkScrollableFrame(self.tab_audit, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.audit_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.audit_scroll.grid_columnconfigure(0, weight=1)

    def refresh_audit(self):
        logs = []
        try:
            res = requests.get("http://127.0.0.1:8000/api/audit/logs?limit=40", timeout=1.0)
            if res.status_code == 200:
                logs = res.json()
        except Exception:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 40")
            logs = [dict(r) for r in cur.fetchall()]
            conn.close()

        for w in self.audit_scroll.winfo_children():
            w.destroy()

        for lg in logs:
            c = ctk.CTkFrame(self.audit_scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=3, padx=2)
            
            ts = lg["timestamp"].split()[-1] if " " in lg["timestamp"] else lg["timestamp"]
            lvl_col = COLORS["danger"] if lg.get("level") == "CRITICAL" else (COLORS["warning"] if lg.get("level") == "WARN" else COLORS["info"])
            
            lbl_top = ctk.CTkLabel(c, text=f"[{ts}] {lg['user_name']} ({lg['role']}) — {lg['action']}", font=FONTS["small_bold"], text_color=lvl_col)
            lbl_top.pack(anchor="w", padx=10, pady=(6, 2))
            
            lbl_det = ctk.CTkLabel(c, text=lg.get("details", ""), font=FONTS["small"], text_color=COLORS["text_dim"], justify="left")
            lbl_det.pack(anchor="w", padx=10, pady=(0, 6))

    def refresh_kpis(self):
        try:
            res = requests.get("http://127.0.0.1:8000/api/stats", timeout=1.0)
            if res.status_code == 200:
                d = res.json()
                self.kpi_sales.configure(text=d["today_sales"])
                self.kpi_rx.configure(text=f"{d['pending_rx_count']} Pending")
                self.kpi_stock.configure(text=f"{d['low_stock_count']} Critical")
                self.kpi_deliv.configure(text=f"{d['active_deliveries']} In Route")
        except Exception:
            pass

    def refresh_all(self):
        self.refresh_users_table()
        self.refresh_presence()
        self.refresh_audit()
        self.refresh_kpis()

    def start_auto_refresh(self):
        self.refresh_presence()
        self.refresh_audit()
        self.refresh_kpis()
        self.after(3000, self.start_auto_refresh)
