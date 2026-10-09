"""
AegisPharm Enterprise — Cashier POS & Billing Dashboard View.
Dual-theme enabled (Clean White Light Mode & Sleek Dark Mode).
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import json
from ui.theme import COLORS, FONTS
from core.db import get_connection

class CashierDashboardView(ctk.CTkFrame):
    def __init__(self, parent, user_data, connector=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.user_data = user_data
        self.connector = connector
        
        self.cart = []
        self.medicines = []
        
        self.grid_columnconfigure(0, weight=6)  # Left: Product Search
        self.grid_columnconfigure(1, weight=4)  # Right: Cart & Checkout
        self.grid_rowconfigure(1, weight=1)
        
        self.setup_ui()
        self.load_inventory()

    def setup_ui(self):
        # Header Banner
        hdr = ctk.CTkFrame(self, height=52, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(14, 8))
        hdr.grid_columnconfigure(1, weight=1)
        
        lbl_brand = ctk.CTkLabel(hdr, text="💳 POS Terminal — Express Counter Checkout", font=FONTS["h2"], text_color=COLORS["commerce"])
        lbl_brand.grid(row=0, column=0, padx=16, pady=10, sticky="w")
        
        lbl_cashier = ctk.CTkLabel(hdr, text=f"Cashier: {self.user_data['name']} ({self.user_data['id']})", font=FONTS["small_bold"], text_color=COLORS["text_dim"])
        lbl_cashier.grid(row=0, column=1, sticky="e", padx=16)
        
        # Left Panel: Product Catalog & Fast Search
        left = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        left.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=(0, 16))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=1)
        
        search_box = ctk.CTkFrame(left, fg_color="transparent")
        search_box.grid(row=0, column=0, sticky="ew", padx=16, pady=12)
        search_box.grid_columnconfigure(0, weight=1)
        
        self.search_ent = ctk.CTkEntry(
            search_box,
            placeholder_text="🔍 Scan barcode or search medicine, salt, batch, rack...",
            font=FONTS["body"],
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_main"],
            border_color=COLORS["border"],
            height=38
        )
        self.search_ent.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.search_ent.bind("<KeyRelease>", lambda e: self.filter_catalog())
        
        btn_scan = ctk.CTkButton(
            search_box,
            text="📷 Barcode",
            width=80,
            height=38,
            font=FONTS["small_bold"],
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_secondary_hover"],
            text_color=COLORS["btn_secondary_text"]
        )
        btn_scan.grid(row=0, column=1)
        
        self.med_scroll = ctk.CTkScrollableFrame(left, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.med_scroll.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        self.med_scroll.grid_columnconfigure(0, weight=1)
        
        # Right Panel: Cart & Payment
        right = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        right.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=(0, 16))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)
        
        r_hdr = ctk.CTkFrame(right, fg_color="transparent")
        r_hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=12)
        r_hdr.grid_columnconfigure(0, weight=1)
        
        lbl_c_title = ctk.CTkLabel(r_hdr, text="🧾 Active Bill / Dispense", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl_c_title.grid(row=0, column=0, sticky="w")
        
        btn_clr = ctk.CTkButton(r_hdr, text="Clear", width=55, height=26, font=FONTS["small"], fg_color=COLORS["btn_danger"], hover_color=COLORS["btn_danger_hover"], text_color="#FFFFFF", command=self.clear_cart)
        btn_clr.grid(row=0, column=1, sticky="e")
        
        self.cart_scroll = ctk.CTkScrollableFrame(right, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.cart_scroll.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 10))
        self.cart_scroll.grid_columnconfigure(0, weight=1)
        
        # Bottom Totals & Payment
        bot = ctk.CTkFrame(right, fg_color=COLORS["bg_surface_alt"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        bot.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 14))
        
        self.lbl_subtotal = ctk.CTkLabel(bot, text="Subtotal: ₹ 0.00", font=FONTS["body"], text_color=COLORS["text_muted"])
        self.lbl_subtotal.pack(anchor="w", padx=14, pady=(8, 1))
        
        self.lbl_gst = ctk.CTkLabel(bot, text="GST (12%): ₹ 0.00", font=FONTS["small"], text_color=COLORS["text_dim"])
        self.lbl_gst.pack(anchor="w", padx=14, pady=1)
        
        self.lbl_total = ctk.CTkLabel(bot, text="Total: ₹ 0.00", font=FONTS["price_large"], text_color=COLORS["commerce"])
        self.lbl_total.pack(anchor="w", padx=14, pady=(2, 10))
        
        # Payment Buttons
        p_row = ctk.CTkFrame(bot, fg_color="transparent")
        p_row.pack(fill="x", padx=14, pady=(0, 10))
        p_row.grid_columnconfigure((0, 1), weight=1)
        
        btn_upi = ctk.CTkButton(p_row, text="⚡ UPI / QR", height=38, fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", font=FONTS["body_bold"], command=lambda: self.checkout("UPI / QR"))
        btn_upi.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        btn_cash = ctk.CTkButton(p_row, text="💵 Cash / Card", height=38, fg_color=COLORS["btn_primary"], hover_color=COLORS["btn_primary_hover"], text_color="#FFFFFF", font=FONTS["body_bold"], command=lambda: self.checkout("Cash / Card"))
        btn_cash.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def load_inventory(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicines ORDER BY name ASC")
        self.medicines = [dict(r) for r in cur.fetchall()]
        conn.close()
        self.render_catalog(self.medicines)

    def filter_catalog(self):
        q = self.search_ent.get().strip().lower()
        if not q:
            self.render_catalog(self.medicines)
            return
        filtered = [m for m in self.medicines if q in m["name"].lower() or q in m["generic"].lower() or q in m["batch"].lower()]
        self.render_catalog(filtered)

    def render_catalog(self, items):
        for w in self.med_scroll.winfo_children():
            w.destroy()
            
        for med in items:
            card = ctk.CTkFrame(self.med_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", pady=4, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            r1 = ctk.CTkFrame(card, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            lbl_n = ctk.CTkLabel(r1, text=med["name"], font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_n.grid(row=0, column=0, sticky="w")
            
            lbl_p = ctk.CTkLabel(r1, text=f"₹ {med['mrp']:.2f}", font=FONTS["h3"], text_color=COLORS["clinical"])
            lbl_p.grid(row=0, column=1, sticky="e")
            
            lbl_det = ctk.CTkLabel(card, text=f"🧪 {med['generic'][:45]} | 📦 Stock: {med['stock']} | 📍 Rack: {med['rack']}", font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_det.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 6))
            
            btn_add = ctk.CTkButton(card, text="+ Add to Bill", height=26, width=100, font=FONTS["small_bold"], fg_color=COLORS["btn_primary"], hover_color=COLORS["btn_primary_hover"], text_color="#FFFFFF", command=lambda m=med: self.add_to_cart(m))
            btn_add.grid(row=2, column=0, sticky="e", padx=10, pady=(0, 8))

    def add_to_cart(self, med):
        for it in self.cart:
            if it["med"]["id"] == med["id"]:
                it["qty"] += 1
                self.update_cart()
                return
        self.cart.append({"med": med, "qty": 1})
        if self.connector:
            self.connector.update_action(f"Added {med['name']} to active bill", status="Billing")
        self.update_cart()

    def update_cart(self):
        for w in self.cart_scroll.winfo_children():
            w.destroy()
            
        subtotal = sum(i["med"]["mrp"] * i["qty"] for i in self.cart)
        gst = subtotal * 0.12
        
        for idx, it in enumerate(self.cart):
            m = it["med"]
            c = ctk.CTkFrame(self.cart_scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=3, padx=2)
            
            lbl_n = ctk.CTkLabel(c, text=f"{m['name']} x{it['qty']}", font=FONTS["small_bold"], text_color=COLORS["text_main"])
            lbl_n.pack(side="left", padx=8, pady=6)
            
            lbl_pr = ctk.CTkLabel(c, text=f"₹ {m['mrp'] * it['qty']:.2f}", font=FONTS["small_bold"], text_color=COLORS["clinical"])
            lbl_pr.pack(side="right", padx=8)

        self.lbl_subtotal.configure(text=f"Subtotal: ₹ {subtotal:.2f}")
        self.lbl_gst.configure(text=f"GST (12%): ₹ {gst:.2f}")
        self.lbl_total.configure(text=f"Total: ₹ {subtotal:.2f}")

    def clear_cart(self):
        self.cart = []
        self.update_cart()

    def checkout(self, method):
        if not self.cart:
            messagebox.showwarning("Cart Empty", "Please add items to cart before checkout.")
            return
            
        total = sum(i["med"]["mrp"] * i["qty"] for i in self.cart)
        inv_id = f"INV-2026-{1000 + len(self.cart)*15}"
        
        # Save invoice to db
        conn = get_connection()
        cur = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
        INSERT INTO invoices VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (inv_id, now, "Counter Customer", self.user_data["name"], method, total*0.88, total*0.12, total, json.dumps([i['med']['name'] for i in self.cart])))
        
        # Deduct stock
        for it in self.cart:
            cur.execute("UPDATE medicines SET stock = stock - ? WHERE id = ?", (it["qty"], it["med"]["id"]))
            
        conn.commit()
        conn.close()
        
        # Broadcast event to Admin & Server
        if self.connector:
            self.connector.log_event("Invoice Generated", f"Cashier {self.user_data['name']} billed ₹{total:.2f} via {method} ({inv_id})", level="INFO")
            self.connector.update_action(f"Completed Bill {inv_id} (₹{total:.2f})", status="Online")
        
        messagebox.showinfo("Billed Successfully", f"Receipt {inv_id} generated.\nAmount: ₹{total:.2f}\nStock automatically deducted.")
        self.clear_cart()
        self.load_inventory()
