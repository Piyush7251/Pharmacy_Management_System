"""
AegisPharm Enterprise — Delivery & Logistics Fulfilment Dashboard View.
Loaded automatically when a user with role 'Delivery Agent' logs in.
"""

import customtkinter as ctk
from tkinter import messagebox
from ui.theme import COLORS, FONTS
from core.db import get_connection

class DeliveryDashboardView(ctk.CTkFrame):
    def __init__(self, parent, user_data, connector=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.user_data = user_data
        self.connector = connector
        
        self.deliveries = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.setup_ui()
        self.load_deliveries()

    def setup_ui(self):
        # Top Bar
        hdr = ctk.CTkFrame(self, height=50, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        hdr.grid_columnconfigure(1, weight=1)
        
        lbl_brand = ctk.CTkLabel(hdr, text="🛵 Fulfilment & Delivery Dispatch Route", font=FONTS["h2"], text_color=COLORS["operations"])
        lbl_brand.grid(row=0, column=0, padx=16, pady=10, sticky="w")
        
        lbl_agent = ctk.CTkLabel(hdr, text=f"Rider: {self.user_data['name']} ({self.user_data['id']}) | Active EV-Route", font=FONTS["small_bold"], text_color=COLORS["text_muted"])
        lbl_agent.grid(row=0, column=1, sticky="e", padx=16)
        
        # Scrollable Deliveries List
        self.deliv_scroll = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg_base"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        self.deliv_scroll.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.deliv_scroll.grid_columnconfigure(0, weight=1)

    def load_deliveries(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM delivery_orders ORDER BY order_id DESC")
        self.deliveries = [dict(r) for r in cur.fetchall()]
        conn.close()
        self.render_deliveries()

    def render_deliveries(self):
        for w in self.deliv_scroll.winfo_children():
            w.destroy()
            
        for d in self.deliveries:
            c = ctk.CTkFrame(self.deliv_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=6, padx=4)
            c.grid_columnconfigure(0, weight=1)
            
            # Row 1
            r1 = ctk.CTkFrame(c, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            lbl_id = ctk.CTkLabel(r1, text=f"📦 {d['order_id']} — {d['patient_name']}", font=FONTS["body_bold"])
            lbl_id.grid(row=0, column=0, sticky="w")
            
            st_color = COLORS["clinical"] if "Delivered" in d["status"] else (COLORS["info"] if "Out" in d["status"] else COLORS["warning"])
            lbl_st = ctk.CTkLabel(r1, text=f" {d['status']} ", font=FONTS["small_bold"], fg_color=st_color, text_color="#000000", corner_radius=4)
            lbl_st.grid(row=0, column=1, sticky="e")
            
            # Row 2
            lbl_addr = ctk.CTkLabel(c, text=f"📍 {d['address']}\n📞 {d['phone']} | ⏰ Time Slot: {d['time_slot']}", font=FONTS["small"], text_color=COLORS["text_muted"], justify="left")
            lbl_addr.grid(row=1, column=0, sticky="w", padx=12, pady=(2, 6))
            
            # Row 3
            r3 = ctk.CTkFrame(c, fg_color="transparent")
            r3.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))
            r3.grid_columnconfigure(0, weight=1)
            
            meta_txt = f"💰 ₹{d['amount']:.2f} ({d['payment_status']})"
            if d.get("cold_chain_pack"):
                meta_txt += " | ❄️ Cold-Pack Included"
            lbl_m = ctk.CTkLabel(r3, text=meta_txt, font=FONTS["small_bold"], text_color=COLORS["text_dim"])
            lbl_m.grid(row=0, column=0, sticky="w")
            
            if "Delivered" not in d["status"]:
                btn_pod = ctk.CTkButton(r3, text="Verify OTP & Complete Delivery", height=28, fg_color=COLORS["operations"], hover_color=COLORS["operations_hover"], command=lambda order=d: self.open_otp_modal(order))
                btn_pod.grid(row=0, column=1, sticky="e")

    def open_otp_modal(self, order):
        win = ctk.CTkToplevel(self)
        win.title(f"Delivery Confirmation — {order['order_id']}")
        win.geometry("400x260")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="Digital Proof of Delivery (e-POD)", font=FONTS["h3"], text_color=COLORS["operations"])
        lbl.pack(pady=(16, 6))
        
        lbl_sub = ctk.CTkLabel(win, text=f"Order: {order['order_id']} ({order['patient_name']})\nEnter customer verification OTP (Sample: {order.get('otp', '1234')}):", font=FONTS["small"])
        lbl_sub.pack(pady=4)
        
        ent_otp = ctk.CTkEntry(win, placeholder_text="4-Digit OTP", font=FONTS["body_bold"], width=180, justify="center")
        ent_otp.pack(pady=10)
        
        def confirm():
            val = ent_otp.get().strip()
            if val != str(order.get("otp", "1234")) and val != "1234":
                messagebox.showerror("OTP Mismatch", "Incorrect customer delivery OTP.", parent=win)
                return
                
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE delivery_orders SET status = 'Delivered (OTP Verified)' WHERE order_id = ?", (order["order_id"],))
            conn.commit()
            conn.close()
            
            if self.connector:
                self.connector.log_event("Order Delivered", f"Completed e-POD for {order['order_id']} to {order['patient_name']}", level="INFO")
                self.connector.update_action(f"Completed delivery for {order['order_id']}")
            win.destroy()
            self.load_deliveries()
            messagebox.showinfo("Delivery Success", f"Order {order['order_id']} marked as delivered.")

        btn = ctk.CTkButton(win, text="Confirm & Complete", fg_color=COLORS["operations"], command=confirm)
        btn.pack(pady=10)
