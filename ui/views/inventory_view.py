"""
Inventory & Procurement View (Layer 4 Supply Chain Domain).
Features FEFO (First-Expired, First-Out) tracking, batch expiry risk badges,
cold chain temperature status, reorder thresholds, and stock replenishment.
"""

import customtkinter as ctk
from ui.theme import COLORS, FONTS
from data.mock_db import MEDICINES_CATALOG
from tkinter import messagebox

class InventoryView(ctk.CTkFrame):
    def __init__(self, parent, show_notification_cb=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.show_notification = show_notification_cb
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.current_filter = "ALL"
        
        self.setup_header()
        self.setup_filter_bar()
        self.setup_inventory_table()
        self.refresh_table()

    def setup_header(self):
        hdr = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        hdr.grid_columnconfigure(0, weight=1)
        
        top_row = ctk.CTkFrame(hdr, fg_color="transparent")
        top_row.pack(fill="x", padx=16, pady=12)
        top_row.grid_columnconfigure(0, weight=1)
        
        lbl_title = ctk.CTkLabel(top_row, text="📦 Multi-Branch Inventory & FEFO Batch Ledger", font=FONTS["h2"], text_color=COLORS["inventory"])
        lbl_title.grid(row=0, column=0, sticky="w")
        
        btn_add_stock = ctk.CTkButton(
            top_row,
            text="+ Receive New Goods (GRN)",
            font=FONTS["body_bold"],
            fg_color=COLORS["inventory"],
            hover_color=COLORS["inventory_hover"],
            command=self.open_add_stock_modal
        )
        btn_add_stock.grid(row=0, column=1, sticky="e")
        
        # Summary Metrics Bar
        metrics_frame = ctk.CTkFrame(hdr, fg_color="transparent")
        metrics_frame.pack(fill="x", padx=16, pady=(0, 12))
        metrics_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        total_skus = len(MEDICINES_CATALOG)
        low_stock = sum(1 for m in MEDICINES_CATALOG if m["stock"] < 25)
        exp_soon = sum(1 for m in MEDICINES_CATALOG if m["days_to_expiry"] < 180)
        cold_items = sum(1 for m in MEDICINES_CATALOG if m.get("cold_chain"))
        
        self.create_metric_card(metrics_frame, 0, "Total SKUs", f"{total_skus} Active", COLORS["info"])
        self.create_metric_card(metrics_frame, 1, "Low Stock Alert", f"{low_stock} Items < Min", COLORS["danger"])
        self.create_metric_card(metrics_frame, 2, "FEFO Expiring Soon", f"{exp_soon} Batches (<6m)", COLORS["warning"])
        self.create_metric_card(metrics_frame, 3, "Cold-Chain Integrity", f"{cold_items} Monitored (4.2°C)", COLORS["clinical"])

    def create_metric_card(self, parent, col, title, value, color):
        c = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        c.grid(row=0, column=col, sticky="ew", padx=4, pady=4)
        
        lbl_t = ctk.CTkLabel(c, text=title, font=FONTS["small"], text_color=COLORS["text_dim"])
        lbl_t.pack(anchor="w", padx=10, pady=(6, 0))
        
        lbl_v = ctk.CTkLabel(c, text=value, font=FONTS["body_bold"], text_color=color)
        lbl_v.pack(anchor="w", padx=10, pady=(0, 6))

    def setup_filter_bar(self):
        filter_bar = ctk.CTkFrame(self, fg_color="transparent")
        filter_bar.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        filter_bar.grid_columnconfigure(0, weight=1)
        
        # Search Entry
        self.search_ent = ctk.CTkEntry(
            filter_bar,
            placeholder_text="🔍 Filter by Medicine name, Batch No, Manufacturer, or Rack...",
            font=FONTS["body"],
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            height=36
        )
        self.search_ent.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_ent.bind("<KeyRelease>", lambda e: self.refresh_table())
        
        # Quick Filter Buttons
        btn_all = ctk.CTkButton(filter_bar, text="All Stock", width=90, height=36, fg_color=COLORS["btn_secondary"], command=lambda: self.set_filter("ALL"))
        btn_all.grid(row=0, column=1, padx=2)
        
        btn_low = ctk.CTkButton(filter_bar, text="⚠️ Low Stock", width=100, height=36, fg_color=COLORS["btn_secondary"], command=lambda: self.set_filter("LOW"))
        btn_low.grid(row=0, column=2, padx=2)
        
        btn_exp = ctk.CTkButton(filter_bar, text="⏳ FEFO Priority", width=110, height=36, fg_color=COLORS["btn_secondary"], command=lambda: self.set_filter("FEFO"))
        btn_exp.grid(row=0, column=3, padx=2)
        
        btn_cold = ctk.CTkButton(filter_bar, text="❄️ Cold Chain", width=100, height=36, fg_color=COLORS["btn_secondary"], command=lambda: self.set_filter("COLD"))
        btn_cold.grid(row=0, column=4, padx=2)

    def set_filter(self, f_type):
        self.current_filter = f_type
        self.refresh_table()

    def setup_inventory_table(self):
        table_container = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        table_container.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)
        
        # Table Header
        hdr_row = ctk.CTkFrame(table_container, fg_color=COLORS["bg_card"], height=38, corner_radius=6)
        hdr_row.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        hdr_row.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        
        cols = ["Item / Generic Name", "Category / Schedule", "Batch & Expiry", "Stock Level", "Rack Location", "MRP / Cost", "Actions"]
        for i, col in enumerate(cols):
            lbl = ctk.CTkLabel(hdr_row, text=col, font=FONTS["small_bold"], text_color=COLORS["text_dim"])
            lbl.grid(row=0, column=i, sticky="w" if i < 5 else "e", padx=6, pady=8)
            
        self.table_scroll = ctk.CTkScrollableFrame(table_container, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.table_scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.table_scroll.grid_columnconfigure(0, weight=1)

    def refresh_table(self):
        for w in self.table_scroll.winfo_children():
            w.destroy()
            
        q = self.search_ent.get().strip().lower()
        items = MEDICINES_CATALOG
        
        if q:
            items = [m for m in items if q in m["name"].lower() or q in m["generic"].lower() or q in m["batch"].lower() or q in m["rack"].lower()]
            
        if self.current_filter == "LOW":
            items = [m for m in items if m["stock"] < 25]
        elif self.current_filter == "FEFO":
            items = sorted([m for m in items if m["days_to_expiry"] < 300], key=lambda x: x["days_to_expiry"])
        elif self.current_filter == "COLD":
            items = [m for m in items if m.get("cold_chain")]

        if not items:
            lbl_empty = ctk.CTkLabel(self.table_scroll, text="No inventory items match filter criteria.", font=FONTS["body"], text_color=COLORS["text_dim"])
            lbl_empty.pack(pady=40)
            return

        for med in items:
            row = ctk.CTkFrame(self.table_scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
            row.pack(fill="x", pady=3, padx=2)
            row.grid_columnconfigure(0, weight=3) # Name
            row.grid_columnconfigure(1, weight=2) # Category
            row.grid_columnconfigure(2, weight=2) # Batch/Exp
            row.grid_columnconfigure(3, weight=2) # Stock
            row.grid_columnconfigure(4, weight=2) # Rack
            row.grid_columnconfigure(5, weight=2) # Price
            row.grid_columnconfigure(6, weight=2) # Actions
            
            # Col 0: Name & Generic
            col0 = ctk.CTkFrame(row, fg_color="transparent")
            col0.grid(row=0, column=0, sticky="w", padx=8, pady=8)
            lbl_n = ctk.CTkLabel(col0, text=med["name"], font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_n.pack(anchor="w")
            lbl_g = ctk.CTkLabel(col0, text=med["generic"][:35] + ("..." if len(med["generic"]) > 35 else ""), font=FONTS["small"], text_color=COLORS["text_dim"])
            lbl_g.pack(anchor="w")
            
            # Col 1: Category & Schedule
            col1 = ctk.CTkFrame(row, fg_color="transparent")
            col1.grid(row=0, column=1, sticky="w", padx=8, pady=8)
            lbl_c = ctk.CTkLabel(col1, text=med["category"], font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_c.pack(anchor="w")
            lbl_s = ctk.CTkLabel(col1, text=med["schedule"], font=FONTS["small_bold"], text_color=COLORS["inventory"])
            lbl_s.pack(anchor="w")
            
            # Col 2: Batch & FEFO Expiry
            col2 = ctk.CTkFrame(row, fg_color="transparent")
            col2.grid(row=0, column=2, sticky="w", padx=8, pady=8)
            lbl_b = ctk.CTkLabel(col2, text=f"🏷️ {med['batch']}", font=FONTS["small_bold"], text_color=COLORS["text_muted"])
            lbl_b.pack(anchor="w")
            exp_text = f"Exp: {med['expiry']}"
            exp_color = COLORS["danger"] if med["days_to_expiry"] < 120 else (COLORS["warning"] if med["days_to_expiry"] < 250 else COLORS["clinical"])
            lbl_e = ctk.CTkLabel(col2, text=exp_text, font=FONTS["small"], text_color=exp_color)
            lbl_e.pack(anchor="w")
            
            # Col 3: Stock level
            col3 = ctk.CTkFrame(row, fg_color="transparent")
            col3.grid(row=0, column=3, sticky="w", padx=8, pady=8)
            stk_color = COLORS["danger"] if med["stock"] < 25 else COLORS["clinical"]
            lbl_stk = ctk.CTkLabel(col3, text=f"{med['stock']} {med['unit'].split()[0]}", font=FONTS["body_bold"], text_color=stk_color)
            lbl_stk.pack(anchor="w")
            
            # Col 4: Rack location
            col4 = ctk.CTkFrame(row, fg_color="transparent")
            col4.grid(row=0, column=4, sticky="w", padx=8, pady=8)
            lbl_rk = ctk.CTkLabel(col4, text=f"📍 {med['rack']}", font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_rk.pack(anchor="w")
            
            # Col 5: Price
            col5 = ctk.CTkFrame(row, fg_color="transparent")
            col5.grid(row=0, column=5, sticky="e", padx=8, pady=8)
            lbl_pr = ctk.CTkLabel(col5, text=f"₹ {med['mrp']:.2f}", font=FONTS["body_bold"], text_color=COLORS["commerce"])
            lbl_pr.pack(anchor="e")
            lbl_cost = ctk.CTkLabel(col5, text=f"Cost: ₹{med['cost_price']:.2f}", font=FONTS["small"], text_color=COLORS["text_dim"])
            lbl_cost.pack(anchor="e")
            
            # Col 6: Actions
            col6 = ctk.CTkFrame(row, fg_color="transparent")
            col6.grid(row=0, column=6, sticky="e", padx=8, pady=8)
            btn_adj = ctk.CTkButton(
                col6,
                text="Adjust / PO",
                width=85,
                height=26,
                fg_color=COLORS["btn_secondary"],
                hover_color=COLORS["btn_secondary_hover"],
                font=FONTS["small"],
                command=lambda m=med: self.adjust_stock(m)
            )
            btn_adj.pack()

    def adjust_stock(self, med):
        win = ctk.CTkToplevel(self)
        win.title(f"Stock Adjustment: {med['name']}")
        win.geometry("400x280")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text=f"Adjust Stock: {med['name']}", font=FONTS["h3"], text_color=COLORS["inventory"])
        lbl.pack(pady=(16, 4))
        
        lbl_cur = ctk.CTkLabel(win, text=f"Current Stock: {med['stock']} units", font=FONTS["body"])
        lbl_cur.pack(pady=4)
        
        ent = ctk.CTkEntry(win, placeholder_text="Enter additional received units (e.g. 50)", font=FONTS["body"], fg_color=COLORS["bg_input"], width=260)
        ent.pack(pady=10)
        
        def save():
            try:
                added = int(ent.get().strip())
                med["stock"] += added
                self.refresh_table()
                win.destroy()
                messagebox.showinfo("Stock Updated", f"Successfully added {added} units to {med['name']}.")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid integer quantity.", parent=win)

        btn = ctk.CTkButton(win, text="Save Adjustment", fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], command=save)
        btn.pack(pady=12)

    def open_add_stock_modal(self):
        messagebox.showinfo(
            "Goods Receipt Note (GRN)",
            "GRN Entry Module:\nScans supplier barcode, matches Purchase Order (PO-2026-819), and enters batch to FEFO registry."
        )
