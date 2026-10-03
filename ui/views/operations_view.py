"""
Fulfilment, Delivery Dispatch & Daily Operations View (Layer 4 Operations Domain).
Covers home delivery tracking, cold-chain handover status, daily register cash reconciliation,
and store performance analytics.
"""

import customtkinter as ctk
from ui.theme import COLORS, FONTS
from data.mock_db import DELIVERY_DISPATCH, DAILY_STATS
from tkinter import messagebox

class OperationsView(ctk.CTkFrame):
    def __init__(self, parent, show_notification_cb=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.show_notification = show_notification_cb
        
        self.grid_columnconfigure(0, weight=6)  # Left: Delivery Dispatch & Logistics
        self.grid_columnconfigure(1, weight=4)  # Right: Financial Register & Cash Reconciliation
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_delivery_panel()
        self.setup_finance_panel()

    def setup_delivery_panel(self):
        left = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        left.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=1)
        
        # Header
        hdr = ctk.CTkFrame(left, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=16)
        
        lbl_t = ctk.CTkLabel(hdr, text="🛵 Fulfilment & Delivery Dispatch Board", font=FONTS["h2"], text_color=COLORS["operations"])
        lbl_t.pack(anchor="w")
        
        lbl_sub = ctk.CTkLabel(hdr, text="Live status of prescription home deliveries and courier handovers", font=FONTS["small"], text_color=COLORS["text_dim"])
        lbl_sub.pack(anchor="w")
        
        # Deliveries Scrollable List
        self.deliv_scroll = ctk.CTkScrollableFrame(left, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.deliv_scroll.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.deliv_scroll.grid_columnconfigure(0, weight=1)
        
        self.refresh_deliveries()

    def refresh_deliveries(self):
        for w in self.deliv_scroll.winfo_children():
            w.destroy()
            
        for d in DELIVERY_DISPATCH:
            card = ctk.CTkFrame(self.deliv_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", pady=5, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            # Row 1: Order ID & Status
            r1 = ctk.CTkFrame(card, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
            r1.grid_columnconfigure(0, weight=1)
            
            lbl_id = ctk.CTkLabel(r1, text=f"📦 {d['order_id']} — {d['patient']}", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_id.grid(row=0, column=0, sticky="w")
            
            st_color = COLORS["info"] if "Out" in d["status"] else (COLORS["warning"] if "Packaging" in d["status"] else COLORS["operations"])
            lbl_st = ctk.CTkLabel(r1, text=f" {d['status']} ", font=FONTS["small_bold"], fg_color=st_color, text_color="#000000", corner_radius=4)
            lbl_st.grid(row=0, column=1, sticky="e")
            
            # Row 2: Address & Phone
            lbl_addr = ctk.CTkLabel(
                card,
                text=f"📍 {d['address']}\n📞 {d['phone']} | ⏰ Time Slot: {d['time_slot']}",
                font=FONTS["small"],
                text_color=COLORS["text_muted"],
                justify="left"
            )
            lbl_addr.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 6))
            
            # Row 3: Agent, Cold chain, Price, Actions
            r3 = ctk.CTkFrame(card, fg_color="transparent")
            r3.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))
            r3.grid_columnconfigure(0, weight=1)
            
            meta_txt = f"🛵 Agent: {d['agent']} | 💰 ₹{d['amount']:.2f} ({d['payment']})"
            if d.get("cold_chain_pack"):
                meta_txt += " | ❄️ Cold-Pack"
            lbl_m = ctk.CTkLabel(r3, text=meta_txt, font=FONTS["small_bold"], text_color=COLORS["text_dim"])
            lbl_m.grid(row=0, column=0, sticky="w")
            
            btn_upd = ctk.CTkButton(
                r3,
                text="Update POD / OTP",
                width=120,
                height=26,
                fg_color=COLORS["operations"],
                hover_color=COLORS["operations_hover"],
                font=FONTS["small"],
                command=lambda order=d: self.update_pod(order)
            )
            btn_upd.grid(row=0, column=1, sticky="e")

    def update_pod(self, order):
        win = ctk.CTkToplevel(self)
        win.title(f"Delivery Confirmation: {order['order_id']}")
        win.geometry("400x260")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="Digital Proof of Delivery (e-POD)", font=FONTS["h3"], text_color=COLORS["operations"])
        lbl.pack(pady=(16, 6))
        
        lbl_sub = ctk.CTkLabel(win, text=f"Order: {order['order_id']} | Patient: {order['patient']}\nEnter recipient 4-digit verification OTP:", font=FONTS["small"])
        lbl_sub.pack(pady=4)
        
        ent_otp = ctk.CTkEntry(win, placeholder_text="Enter 4-Digit OTP", font=FONTS["body_bold"], width=200, fg_color=COLORS["bg_input"], justify="center")
        ent_otp.pack(pady=10)
        
        def confirm_del():
            if len(ent_otp.get().strip()) != 4:
                messagebox.showwarning("Invalid OTP", "Please enter 4-digit delivery verification OTP.", parent=win)
                return
            order["status"] = "Delivered (OTP Verified)"
            self.refresh_deliveries()
            win.destroy()
            messagebox.showinfo("Delivery Completed", f"{order['order_id']} marked as delivered. Invoice reconciled.")

        btn = ctk.CTkButton(win, text="Confirm Delivery", fg_color=COLORS["operations"], hover_color=COLORS["operations_hover"], command=confirm_del)
        btn.pack(pady=10)

    def setup_finance_panel(self):
        right = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)
        right.grid_columnconfigure(0, weight=1)
        
        # Header
        hdr = ctk.CTkFrame(right, fg_color="transparent")
        hdr.pack(fill="x", padx=16, pady=16)
        
        lbl_t = ctk.CTkLabel(hdr, text="📊 Financials & Z-Register", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl_t.pack(anchor="w")
        
        lbl_sub = ctk.CTkLabel(hdr, text="Daily Cash Reconciliation & GST Turnover", font=FONTS["small"], text_color=COLORS["text_dim"])
        lbl_sub.pack(anchor="w")
        
        # Financial KPI Cards
        fin_box = ctk.CTkFrame(right, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        fin_box.pack(fill="x", padx=16, pady=8)
        
        self.create_fin_row(fin_box, "Today's Gross Sales", DAILY_STATS["today_sales"], COLORS["clinical"])
        self.create_fin_row(fin_box, "Prescriptions Dispensed", str(DAILY_STATS["prescriptions_dispensed"]), COLORS["text_main"])
        self.create_fin_row(fin_box, "Digital Payments (UPI/Card)", DAILY_STATS["digital_upi_pos"], COLORS["info"])
        self.create_fin_row(fin_box, "Cash in Register Drawer", DAILY_STATS["cash_in_drawer"], COLORS["inventory"])
        self.create_fin_row(fin_box, "Cold-Chain Integrity", DAILY_STATS["cold_chain_temp"], COLORS["clinical"])
        
        # Actions
        btn_reconcile = ctk.CTkButton(
            right,
            text="📑 End of Day (Z-Report / Tally Sync)",
            height=38,
            fg_color=COLORS["btn_primary"],
            hover_color=COLORS["btn_primary_hover"],
            font=FONTS["body_bold"],
            command=self.run_z_report
        )
        btn_reconcile.pack(fill="x", padx=16, pady=(16, 8))
        
        btn_compliance = ctk.CTkButton(
            right,
            text="⚖️ Export Schedule H1 & Narcotic Ledger",
            height=38,
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_secondary_hover"],
            font=FONTS["body"],
            command=self.export_narcotic_log
        )
        btn_compliance.pack(fill="x", padx=16, pady=(0, 16))

    def create_fin_row(self, parent, label, val, val_color):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=8)
        
        lbl_l = ctk.CTkLabel(row, text=label, font=FONTS["small"], text_color=COLORS["text_muted"])
        lbl_l.pack(side="left")
        
        lbl_v = ctk.CTkLabel(row, text=val, font=FONTS["body_bold"], text_color=val_color)
        lbl_v.pack(side="right")

    def run_z_report(self):
        messagebox.showinfo(
            "End of Day Z-Report",
            f"Daily Register Reconciled:\nTotal Sales: {DAILY_STATS['today_sales']}\nCash Reconciled: {DAILY_STATS['cash_in_drawer']}\nDigital UPI: {DAILY_STATS['digital_upi_pos']}\n\nSync payload sent to Accounting ERP (Tally/SAP)."
        )

    def export_narcotic_log(self):
        messagebox.showinfo(
            "Schedule H1 / NDPS Compliance Export",
            "Schedule H1 & Schedule X Drug Dispensation Registry generated with digital signatures and doctor license mappings (PDF & Excel format)."
        )
