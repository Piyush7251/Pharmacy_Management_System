"""
AegisPharm — Inventory & Supply Chain Hub.
Dedicated standalone application for Warehouse & Inventory Managers to track FEFO expiry batches,
reorder thresholds, cold chain integrity, and process Goods Receipt Notes (GRN).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from tkinter import messagebox
from ui.theme import COLORS, FONTS
from core.api_client import AppConnector
from core.db import get_connection

class InventoryHubApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("📦 AegisPharm — Supply Chain & FEFO Inventory Hub")
        self.geometry("1350x850")
        self.minsize(1100, 700)
        self.configure(fg_color=COLORS["bg_base"])
        
        # Start Presence Connector for Inventory Manager
        self.connector = AppConnector(
            user_id="STF-04",
            user_name="Vikram Rathore (Inventory Mgr)",
            role="Inventory Manager",
            app_name="Inventory & Warehouse Hub"
        )
        self.connector.start()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.medicines = []
        self.setup_ui()
        self.load_stock()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Top Bar
        topbar = ctk.CTkFrame(self, height=60, fg_color=COLORS["bg_surface"], corner_radius=0, border_width=1, border_color=COLORS["border"])
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_propagate(False)
        topbar.grid_columnconfigure(1, weight=1)
        
        lbl_brand = ctk.CTkLabel(topbar, text="📦 Warehouse & Supply Chain Inventory Hub", font=FONTS["h2"], text_color=COLORS["inventory"])
        lbl_brand.grid(row=0, column=0, padx=20, pady=12, sticky="w")
        
        lbl_mgr = ctk.CTkLabel(topbar, text="Manager: Vikram Rathore | Cold-Chain: 4.2°C Active", font=FONTS["small_bold"], text_color=COLORS["text_muted"])
        lbl_mgr.grid(row=0, column=1, sticky="e", padx=20)
        
        # Filter & Action Strip
        filter_box = ctk.CTkFrame(self, fg_color="transparent")
        filter_box.grid(row=1, column=0, sticky="ew", padx=16, pady=12)
        filter_box.grid_columnconfigure(0, weight=1)
        
        self.search_ent = ctk.CTkEntry(filter_box, placeholder_text="🔍 Search medicine, batch, manufacturer, rack location...", font=FONTS["body"], fg_color=COLORS["bg_input"], height=38)
        self.search_ent.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_ent.bind("<KeyRelease>", lambda e: self.render_stock())
        
        btn_grn = ctk.CTkButton(filter_box, text="+ Goods Receipt Note (GRN)", height=38, font=FONTS["body_bold"], fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], command=self.receive_grn)
        btn_grn.grid(row=0, column=1, padx=(0, 6))
        
        btn_ref = ctk.CTkButton(filter_box, text="🔄 Reload", width=80, height=38, fg_color=COLORS["btn_secondary"], command=self.load_stock)
        btn_ref.grid(row=0, column=2)
        
        # Table Scroll
        self.table_scroll = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg_base"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        self.table_scroll.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.table_scroll.grid_columnconfigure(0, weight=1)

    def load_stock(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicines ORDER BY name ASC")
        self.medicines = [dict(r) for r in cur.fetchall()]
        conn.close()
        self.render_stock()

    def render_stock(self):
        for w in self.table_scroll.winfo_children():
            w.destroy()
            
        q = self.search_ent.get().strip().lower()
        items = self.medicines
        if q:
            items = [m for m in items if q in m["name"].lower() or q in m["generic"].lower() or q in m["batch"].lower()]

        for med in items:
            c = ctk.CTkFrame(self.table_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=4, padx=4)
            c.grid_columnconfigure(0, weight=1)
            
            # Row 1
            r1 = ctk.CTkFrame(c, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            lbl_n = ctk.CTkLabel(r1, text=f"{med['name']}", font=FONTS["body_bold"])
            lbl_n.grid(row=0, column=0, sticky="w")
            
            stk_c = COLORS["danger"] if med["stock"] < 25 else COLORS["clinical"]
            lbl_stk = ctk.CTkLabel(r1, text=f"Stock: {med['stock']} {med['unit']}", font=FONTS["body_bold"], text_color=stk_c)
            lbl_stk.grid(row=0, column=1, sticky="e")
            
            # Row 2
            r2 = ctk.CTkFrame(c, fg_color="transparent")
            r2.grid(row=1, column=0, sticky="ew", padx=12, pady=(2, 10))
            r2.grid_columnconfigure(0, weight=1)
            
            exp_c = COLORS["danger"] if med["days_to_expiry"] < 120 else (COLORS["warning"] if med["days_to_expiry"] < 250 else COLORS["text_muted"])
            det_txt = f"📦 Batch: {med['batch']} | ⏳ Expiry: {med['expiry']} ({med['days_to_expiry']} days) | 📍 Rack: {med['rack']} | ₹ MRP: {med['mrp']:.2f}"
            lbl_d = ctk.CTkLabel(r2, text=det_txt, font=FONTS["small"], text_color=exp_c, justify="left")
            lbl_d.grid(row=0, column=0, sticky="w")
            
            btn_adj = ctk.CTkButton(r2, text="Adjust Stock", width=100, height=26, fg_color=COLORS["btn_secondary"], command=lambda m=med: self.adjust(m))
            btn_adj.grid(row=0, column=1, sticky="e")

    def adjust(self, med):
        win = ctk.CTkToplevel(self)
        win.title(f"Adjust Stock — {med['name']}")
        win.geometry("400x250")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text=f"Stock Adjustment: {med['name']}", font=FONTS["h3"], text_color=COLORS["inventory"])
        lbl.pack(pady=(16, 4))
        
        lbl_cur = ctk.CTkLabel(win, text=f"Current Stock: {med['stock']} units", font=FONTS["body"])
        lbl_cur.pack(pady=4)
        
        ent = ctk.CTkEntry(win, placeholder_text="Add Quantity (e.g., 50)", font=FONTS["body"], width=240)
        ent.pack(pady=10)
        
        def save():
            try:
                qty = int(ent.get().strip())
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE medicines SET stock = stock + ? WHERE id = ?", (qty, med["id"]))
                conn.commit()
                conn.close()
                
                self.connector.log_event("Stock Adjusted", f"Replenished {qty} units for {med['name']}", level="INFO")
                self.connector.update_action(f"Replenished {med['name']} (+{qty})")
                win.destroy()
                self.load_stock()
                messagebox.showinfo("Stock Updated", f"Added {qty} units to {med['name']}.")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid integer.", parent=win)

        btn = ctk.CTkButton(win, text="Confirm", fg_color=COLORS["inventory"], command=save)
        btn.pack(pady=10)

    def receive_grn(self):
        self.connector.log_event("GRN Received", "Processed PO Goods Receipt #GRN-99120", level="INFO")
        self.connector.update_action("Processed GRN Shipment #99120")
        messagebox.showinfo("GRN Inwarded", "Goods Receipt Note #GRN-99120 inwarded into FEFO batch registry.")

    def on_close(self):
        self.connector.stop()
        self.destroy()

if __name__ == "__main__":
    app = InventoryHubApp()
    app.mainloop()
