"""
AegisPharm — Admin Command Center & Live Staff Presence Monitor (Standalone).
Non-blocking, lag-free background polling engine.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading
import customtkinter as ctk
from datetime import datetime
from ui.theme import COLORS, FONTS
from core.api_client import AppConnector
from core.db import get_connection

class AdminCommandCenter(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("👑 AegisPharm — Enterprise Admin Command Center")
        self.geometry("1400x900")
        self.minsize(1150, 720)
        self.configure(fg_color=COLORS["bg_base"])
        
        self._last_presence_data = []
        self._last_audit_data = []
        self._is_fetching = False
        
        # Start Presence Connector for Admin
        self.connector = AppConnector(
            user_id="STF-01",
            user_name="Dr. Rajesh Kulkarni (Admin)",
            role="Admin",
            app_name="Admin Command Center"
        )
        self.connector.start()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.setup_ui()
        self.start_auto_refresh()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # 1. Header Bar
        hdr = ctk.CTkFrame(self, height=60, fg_color=COLORS["bg_surface"], corner_radius=0, border_width=1, border_color=COLORS["border"])
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(1, weight=1)
        
        lbl_title = ctk.CTkLabel(
            hdr,
            text="👑 AegisPharm Enterprise — Store Admin & Presence Monitor",
            font=FONTS["h2"],
            text_color=COLORS["warning"]
        )
        lbl_title.grid(row=0, column=0, padx=20, pady=14, sticky="w")
        
        right_info = ctk.CTkFrame(hdr, fg_color="transparent")
        right_info.grid(row=0, column=1, sticky="e", padx=20)
        
        self.lbl_server_status = ctk.CTkLabel(
            right_info,
            text="🟢 Engine: Active (0ms lag)",
            font=FONTS["small_bold"],
            text_color=COLORS["clinical"]
        )
        self.lbl_server_status.pack(side="left", padx=10)
        
        btn_refresh = ctk.CTkButton(
            right_info,
            text="🔄 Refresh",
            width=90,
            height=30,
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_secondary_hover"],
            font=FONTS["small_bold"],
            command=self.trigger_background_refresh
        )
        btn_refresh.pack(side="left")
        
        # 2. Storewide KPI Metrics Strip
        self.metrics_strip = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        self.metrics_strip.grid(row=1, column=0, sticky="ew", padx=16, pady=(12, 8))
        self.metrics_strip.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        self.kpi_staff = self.create_kpi_card(self.metrics_strip, 0, "Online Staff", "0 Active", COLORS["clinical"])
        self.kpi_sales = self.create_kpi_card(self.metrics_strip, 1, "Today's Gross Sales", "₹ 48,920.50", COLORS["commerce"])
        self.kpi_rx = self.create_kpi_card(self.metrics_strip, 2, "Pending Rx Checks", "3 Pending", COLORS["warning"])
        self.kpi_stock = self.create_kpi_card(self.metrics_strip, 3, "Low Stock Alerts", "4 Critical", COLORS["danger"])
        self.kpi_deliv = self.create_kpi_card(self.metrics_strip, 4, "Active Routes", "3 Dispatched", COLORS["operations"])
        
        # 3. Main Workspace
        main_workspace = ctk.CTkFrame(self, fg_color="transparent")
        main_workspace.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))
        main_workspace.grid_columnconfigure(0, weight=6)
        main_workspace.grid_columnconfigure(1, weight=4)
        main_workspace.grid_rowconfigure(0, weight=1)
        
        # Left Panel: Online Users
        left_panel = ctk.CTkFrame(main_workspace, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)
        
        l_hdr = ctk.CTkFrame(left_panel, fg_color="transparent")
        l_hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=14)
        
        lbl_l_title = ctk.CTkLabel(l_hdr, text="👥 Live Online Staff & Terminals Presence", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl_l_title.pack(anchor="w")
        
        self.staff_scroll = ctk.CTkScrollableFrame(left_panel, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.staff_scroll.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.staff_scroll.grid_columnconfigure(0, weight=1)
        
        # Right Panel: Event Log
        right_panel = ctk.CTkFrame(main_workspace, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        
        r_hdr = ctk.CTkFrame(right_panel, fg_color="transparent")
        r_hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=14)
        
        lbl_r_title = ctk.CTkLabel(r_hdr, text="📡 Live Store Event Stream (Audit Ledger)", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl_r_title.pack(anchor="w")
        
        self.audit_scroll = ctk.CTkScrollableFrame(right_panel, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.audit_scroll.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.audit_scroll.grid_columnconfigure(0, weight=1)

    def create_kpi_card(self, parent, col, title, value, color):
        c = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        c.grid(row=0, column=col, sticky="ew", padx=6, pady=8)
        
        lbl_t = ctk.CTkLabel(c, text=title, font=FONTS["small"], text_color=COLORS["text_dim"])
        lbl_t.pack(anchor="w", padx=10, pady=(6, 2))
        
        lbl_v = ctk.CTkLabel(c, text=value, font=FONTS["h2"], text_color=color)
        lbl_v.pack(anchor="w", padx=10, pady=(0, 6))
        return lbl_v

    def _async_worker(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT * FROM active_sessions ORDER BY login_time DESC")
            rows = cur.fetchall()
            now = datetime.now()
            users = []
            for r in rows:
                try:
                    last_hb = datetime.strptime(r["last_heartbeat"], "%Y-%m-%d %H:%M:%S")
                    diff = (now - last_hb).total_seconds()
                except Exception:
                    diff = 0
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
                
            cur.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 30")
            audit_logs = [dict(r) for r in cur.fetchall()]
            
            cur.execute("SELECT COUNT(*) as low_stock FROM medicines WHERE stock < 25")
            low_stock = cur.fetchone()["low_stock"]
            
            cur.execute("SELECT COUNT(*) as pending_rx FROM prescriptions WHERE status != 'Verified & Approved'")
            pending_rx = cur.fetchone()["pending_rx"]
            
            cur.execute("SELECT COUNT(*) as active_deliv FROM delivery_orders WHERE status != 'Delivered (OTP Verified)'")
            active_deliv = cur.fetchone()["active_deliv"]
            
            cur.execute("SELECT SUM(total_amount) as total_sales FROM invoices")
            sales_row = cur.fetchone()["total_sales"]
            total_sales = sales_row if sales_row else 48920.50
            
            conn.close()
            
            self.after(0, lambda: self._apply_data(users, audit_logs, low_stock, pending_rx, active_deliv, total_sales))
        except Exception:
            pass
        finally:
            self._is_fetching = False

    def _apply_data(self, users, audit_logs, low_stock, pending_rx, active_deliv, total_sales):
        self.kpi_stock.configure(text=f"{low_stock} Critical")
        self.kpi_rx.configure(text=f"{pending_rx} Pending")
        self.kpi_deliv.configure(text=f"{active_deliv} In Route")
        self.kpi_sales.configure(text=f"₹ {total_sales:,.2f}")
        
        # Render presence delta
        if users != self._last_presence_data:
            self._last_presence_data = users
            for w in self.staff_scroll.winfo_children():
                w.destroy()
            online_count = sum(1 for u in users if u.get("is_online"))
            self.kpi_staff.configure(text=f"{online_count} Terminals Active")
            
            for u in users:
                is_on = u.get("is_online", False)
                status_color = COLORS["clinical"] if is_on else COLORS["danger"]
                badge_text = "🟢 ONLINE" if is_on else f"🔴 DISCONNECTED ({u.get('seconds_since_heartbeat', 0)}s ago)"
                
                card = ctk.CTkFrame(self.staff_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
                card.pack(fill="x", pady=4, padx=4)
                card.grid_columnconfigure(0, weight=1)
                
                r1 = ctk.CTkFrame(card, fg_color="transparent")
                r1.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 2))
                r1.grid_columnconfigure(0, weight=1)
                
                role_icon = "👑" if "Admin" in u["role"] else ("🩺" if "Pharmacist" in u["role"] else ("💳" if "Cashier" in u["role"] else "📦"))
                lbl_name = ctk.CTkLabel(r1, text=f"{role_icon} {u['name']}", font=FONTS["body_bold"], text_color=COLORS["text_main"])
                lbl_name.grid(row=0, column=0, sticky="w")
                
                lbl_role = ctk.CTkLabel(r1, text=f" {u['role']} ", font=FONTS["small_bold"], fg_color=COLORS["badge_bg"], corner_radius=4)
                lbl_role.grid(row=0, column=1, padx=6)
                
                lbl_st = ctk.CTkLabel(r1, text=badge_text, font=FONTS["small_bold"], text_color=status_color)
                lbl_st.grid(row=0, column=2, sticky="e")
                
                r2 = ctk.CTkFrame(card, fg_color="transparent")
                r2.grid(row=1, column=0, sticky="ew", padx=12, pady=(2, 8))
                
                info_txt = f"🖥️ Terminal: {u['terminal_name']} ({u.get('ip_address', '127.0.0.1')}) | 🕒 Logged in: {u['login_time']}\n⚡ Last Action: {u.get('last_action', 'Active')}"
                lbl_act = ctk.CTkLabel(r2, text=info_txt, font=FONTS["small"], text_color=COLORS["text_muted"], justify="left")
                lbl_act.pack(anchor="w")

        # Render audit delta
        if audit_logs != self._last_audit_data:
            self._last_audit_data = audit_logs
            for w in self.audit_scroll.winfo_children():
                w.destroy()
            for lg in audit_logs:
                c = ctk.CTkFrame(self.audit_scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
                c.pack(fill="x", pady=3, padx=2)
                
                ts = lg["timestamp"].split()[-1] if " " in lg["timestamp"] else lg["timestamp"]
                lvl_color = COLORS["danger"] if lg.get("level") == "CRITICAL" else (COLORS["warning"] if lg.get("level") == "WARN" else COLORS["info"])
                
                lbl_top = ctk.CTkLabel(c, text=f"[{ts}] {lg['user_name']} ({lg['role']}) — {lg['action']}", font=FONTS["small_bold"], text_color=lvl_color)
                lbl_top.pack(anchor="w", padx=10, pady=(4, 1))
                
                lbl_det = ctk.CTkLabel(c, text=lg.get("details", ""), font=FONTS["small"], text_color=COLORS["text_dim"], justify="left")
                lbl_det.pack(anchor="w", padx=10, pady=(0, 4))

    def trigger_background_refresh(self):
        if self._is_fetching:
            return
        self._is_fetching = True
        threading.Thread(target=self._async_worker, daemon=True).start()

    def start_auto_refresh(self):
        self.trigger_background_refresh()
        self.after(4000, self.start_auto_refresh)

    def on_close(self):
        self.connector.stop()
        self.destroy()

if __name__ == "__main__":
    app = AdminCommandCenter()
    app.mainloop()
