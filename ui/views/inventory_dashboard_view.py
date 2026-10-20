"""
TQM Pharm Enterprise — Complete Inventory & Supply Chain Hub.
Full features:
- FEFO Multi-Batch Medicine Inventory Ledger:
    * Search, Category & Expiry Filtering
    * Real-time Total Valuation KPI Banner (MRP & Cost)
    * Export Full Inventory Ledger to CSV
    * Quick Stock Adjustment Modal with Instant DB Sync & Audit Logging
- Goods Receipt Notes (GRN) & Purchase Order (PO) Inwarding:
    * Select Supplier, Enter Inward Quantity & Batch
    * Real-time Stock Increment in Central SQLite Database
- Cold Chain IoT Sensor Temperature Logger & Canvas Telemetry Chart:
    * Visual Smooth Spline Temperature Graph with 2-8°C Optimal Band
    * Interactive Temperature Spike Alarm Simulation (+9.5°C) & Cooling Normalization
- Supplier / Distributor Management Directory with Search & Registration Modal
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
import csv
from ui.theme import COLORS, FONTS
from ui.components.toast import show_toast
from ui.components.chart_canvas import ColdChainChartCanvas
from core.db import (
    get_all_medicines, add_medicine, update_medicine_stock, delete_medicine,
    get_all_suppliers, get_all_purchase_orders, add_purchase_order,
    get_temperature_logs, add_temperature_log, get_connection
)

class InventoryDashboardView(ctk.CTkFrame):
    def __init__(self, parent, user_data, connector=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.user_data = user_data
        self.connector = connector
        
        self.medicines = []
        self.current_filter = "ALL"
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.setup_header()
        self.setup_tabs()
        self.load_all_data()

    def setup_header(self):
        hdr = ctk.CTkFrame(self, height=54, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 6))
        hdr.grid_columnconfigure(1, weight=1)
        
        lbl_brand = ctk.CTkLabel(hdr, text="📦 Medicines Stock & Inventory", font=FONTS["h2"], text_color=COLORS["inventory"])
        lbl_brand.grid(row=0, column=0, padx=16, pady=10, sticky="w")
        
        right_box = ctk.CTkFrame(hdr, fg_color="transparent")
        right_box.grid(row=0, column=1, sticky="e", padx=16)
        
        lbl_mgr = ctk.CTkLabel(right_box, text=f"Manager: {self.user_data['name']} | ❄️ Fridge: 4.2°C (Normal)", font=FONTS["small_bold"], text_color=COLORS["text_dim"])
        lbl_mgr.pack(side="left", padx=(0, 10))
        
        btn_add_med = ctk.CTkButton(
            right_box,
            text="+ Add New Medicine",
            height=30,
            font=FONTS["small_bold"],
            fg_color=COLORS["inventory"],
            hover_color=COLORS["inventory_hover"],
            text_color="#FFFFFF",
            command=self.open_add_medicine_modal
        )
        btn_add_med.pack(side="left")

    def setup_tabs(self):
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=COLORS["bg_surface"],
            segmented_button_fg_color=COLORS["bg_card"],
            segmented_button_selected_color=COLORS["inventory"],
            segmented_button_selected_hover_color=COLORS["inventory_hover"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 12))
        
        self.tab_stock = self.tabview.add("📊 Stock List & Batches")
        self.tab_grn = self.tabview.add("📦 Supplier Orders (Stock In)")
        self.tab_cold = self.tabview.add("❄️ Fridge Temperature (2-8°C)")
        self.tab_suppliers = self.tabview.add("🏢 Medicine Suppliers")
        
        self.setup_stock_tab()
        self.setup_grn_tab()
        self.setup_cold_tab()
        self.setup_suppliers_tab()

    # --- TAB 1: STOCK LEDGER ---

    def setup_stock_tab(self):
        self.tab_stock.grid_columnconfigure(0, weight=1)
        self.tab_stock.grid_rowconfigure(2, weight=1)
        
        filter_box = ctk.CTkFrame(self.tab_stock, fg_color="transparent")
        filter_box.grid(row=0, column=0, sticky="ew", padx=10, pady=(6, 4))
        filter_box.grid_columnconfigure(0, weight=1)
        
        self.search_ent = ctk.CTkEntry(
            filter_box,
            placeholder_text="🔍 Search by medicine name, salt, batch, or rack...",
            font=FONTS["body"],
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_main"],
            border_color=COLORS["border"],
            height=36
        )
        self.search_ent.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.search_ent.bind("<KeyRelease>", lambda e: self.render_stock())
        
        btn_box = ctk.CTkFrame(filter_box, fg_color="transparent")
        btn_box.grid(row=0, column=1)
        
        for f in [("All Medicines", "ALL"), ("⚠️ Low Stock", "LOW"), ("⏳ Expiring Soon", "EXP"), ("❄️ Needs Fridge", "COLD")]:
            b = ctk.CTkButton(
                btn_box,
                text=f[0],
                width=95,
                height=34,
                font=FONTS["small_bold"],
                fg_color=COLORS["btn_secondary"],
                hover_color=COLORS["btn_secondary_hover"],
                text_color=COLORS["btn_secondary_text"],
                command=lambda s=f[1]: self.set_stock_filter(s)
            )
            b.pack(side="left", padx=2)
            
        btn_exp = ctk.CTkButton(
            btn_box,
            text="💾 Export CSV",
            width=85,
            height=34,
            font=FONTS["small_bold"],
            fg_color=COLORS["inventory"],
            hover_color=COLORS["inventory_hover"],
            text_color="#FFFFFF",
            command=self.export_stock_csv
        )
        btn_exp.pack(side="left", padx=(4, 0))
            
        # Inventory Valuation KPI Strip
        self.val_strip = ctk.CTkFrame(self.tab_stock, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.val_strip.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 6))
        
        self.lbl_valuation = ctk.CTkLabel(
            self.val_strip,
            text="📊 Loading Stock Valuation...",
            font=FONTS["body_bold"],
            text_color=COLORS["inventory"]
        )
        self.lbl_valuation.pack(anchor="w", padx=12, pady=6)
            
        self.stock_scroll = ctk.CTkScrollableFrame(self.tab_stock, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.stock_scroll.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.stock_scroll.grid_columnconfigure(0, weight=1)

    def set_stock_filter(self, f_type):
        self.current_filter = f_type
        self.render_stock()

    def render_stock(self):
        for w in self.stock_scroll.winfo_children():
            w.destroy()
            
        q = self.search_ent.get().strip().lower() if hasattr(self, "search_ent") else ""
        items = self.medicines
        
        if q:
            items = [m for m in items if q in m["name"].lower() or q in m["generic"].lower() or q in m["batch"].lower()]
            
        if self.current_filter == "LOW":
            items = [m for m in items if m["stock"] <= 25]
        elif self.current_filter == "EXP":
            items = sorted([m for m in items if m.get("days_to_expiry", 999) <= 250], key=lambda x: x.get("days_to_expiry", 999))
        elif self.current_filter == "COLD":
            items = [m for m in items if m.get("cold_chain")]

        # Update Valuation Stats
        tot_mrp = sum(m["mrp"] * m["stock"] for m in items)
        tot_cost = sum(m["cost_price"] * m["stock"] for m in items)
        tot_units = sum(m["stock"] for m in items)
        self.lbl_valuation.configure(
            text=f"📊 Showing {len(items)} items ({tot_units} units in stock)  |  Selling Value (MRP): ₹{tot_mrp:,.2f}  |  Purchase Cost: ₹{tot_cost:,.2f}"
        )

        if not items:
            ctk.CTkLabel(self.stock_scroll, text="No medicines matching search or filter.", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(pady=40)
            return

        for med in items:
            c = ctk.CTkFrame(self.stock_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=4, padx=4)
            c.grid_columnconfigure(0, weight=1)
            
            # Row 1
            r1 = ctk.CTkFrame(c, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            lbl_n = ctk.CTkLabel(r1, text=f"{med['name']}", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_n.grid(row=0, column=0, sticky="w")
            
            stk_c = COLORS["danger"] if med["stock"] <= 20 else COLORS["clinical"]
            lbl_stk = ctk.CTkLabel(r1, text=f"Stock: {med['stock']} {med['unit']}", font=FONTS["body_bold"], text_color=stk_c)
            lbl_stk.grid(row=0, column=1, sticky="e")
            
            # Row 2
            r2 = ctk.CTkFrame(c, fg_color="transparent")
            r2.grid(row=1, column=0, sticky="ew", padx=12, pady=(2, 8))
            r2.grid_columnconfigure(0, weight=1)
            
            exp_c = COLORS["danger"] if med["days_to_expiry"] <= 90 else (COLORS["warning"] if med["days_to_expiry"] <= 200 else COLORS["text_muted"])
            det_txt = f"📦 Batch: {med['batch']} | ⏳ Exp: {med['expiry']} ({med['days_to_expiry']}d) | 📍 Rack: {med['rack']} | ₹ MRP: {med['mrp']:.2f} (Cost: ₹{med['cost_price']:.2f})"
            lbl_d = ctk.CTkLabel(r2, text=det_txt, font=FONTS["small"], text_color=exp_c, justify="left")
            lbl_d.grid(row=0, column=0, sticky="w")
            
            btn_box = ctk.CTkFrame(r2, fg_color="transparent")
            btn_box.grid(row=0, column=1, sticky="e")
            
            btn_adj = ctk.CTkButton(
                btn_box,
                text="Adjust Stock",
                width=90,
                height=26,
                font=FONTS["small_bold"],
                fg_color=COLORS["btn_secondary"],
                hover_color=COLORS["btn_secondary_hover"],
                text_color=COLORS["btn_secondary_text"],
                command=lambda m=med: self.open_adjust_modal(m)
            )
            btn_adj.pack(side="left", padx=(0, 4))
            
            btn_del = ctk.CTkButton(
                btn_box,
                text="🗑️",
                width=30,
                height=26,
                fg_color=COLORS["btn_danger"],
                hover_color=COLORS["btn_danger_hover"],
                text_color="#FFFFFF",
                command=lambda m=med: self.delete_medicine_item(m)
            )
            btn_del.pack(side="left")

    def export_stock_csv(self):
        if not self.medicines:
            show_toast(self, "Empty Catalog", "No medicines to export.", "warning")
            return
            
        path = filedialog.asksaveasfilename(
            title="Export Inventory Ledger",
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")],
            initialfile="TQM Pharm_Stock_Ledger.csv"
        )
        if path:
            fields = ["id", "name", "generic", "category", "schedule", "manufacturer", "batch", "expiry", "days_to_expiry", "stock", "unit", "mrp", "cost_price", "rack", "cold_chain"]
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(self.medicines)
            show_toast(self, "Inventory Exported", f"Successfully saved {len(self.medicines)} batches to {path}.", "success")

    def open_adjust_modal(self, med):
        win = ctk.CTkToplevel(self)
        win.title(f"Adjust Stock — {med['name']}")
        win.geometry("440x320")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text=f"Update Stock: {med['name']}", font=FONTS["h3"], text_color=COLORS["inventory"])
        lbl.pack(pady=(16, 4))
        
        lbl_cur = ctk.CTkLabel(win, text=f"Current Stock: {med['stock']} units (Batch: {med['batch']})", font=FONTS["body"], text_color=COLORS["text_main"])
        lbl_cur.pack(pady=4)
        
        ent = ctk.CTkEntry(win, placeholder_text="Quantity change (e.g. +50 or -10)", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=280, height=36)
        ent.pack(pady=8)
        ent.focus()
        
        reason_opt = ctk.CTkOptionMenu(win, values=["Stock Arrival / New Batch", "Damaged / Broken", "Expired Stock", "Count Correction"], width=280)
        reason_opt.set("Count Correction")
        reason_opt.pack(pady=6)
        
        def save():
            try:
                raw_txt = ent.get().strip().replace("+", "")
                qty_delta = int(raw_txt)
                update_medicine_stock(med["id"], qty_delta)
                med["stock"] = max(0, med["stock"] + qty_delta)
                
                if self.connector:
                    self.connector.log_event("Stock Adjusted", f"Adjusted {med['name']} by {qty_delta} units ({reason_opt.get()})", level="INFO")
                    
                win.destroy()
                self.render_stock()
                show_toast(self, "Stock Updated", f"{med['name']} stock updated by {qty_delta:+d} units.", "success")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Enter a valid number.", parent=win)
                
        ctk.CTkButton(win, text="Confirm Stock Change", height=38, font=FONTS["body_bold"], fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], text_color="#FFFFFF", command=save).pack(pady=16)

    def delete_medicine_item(self, med):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {med['name']} (Batch {med['batch']})?")
        if confirm:
            delete_medicine(med["id"])
            self.medicines = [m for m in self.medicines if m["id"] != med["id"]]
            self.render_stock()
            show_toast(self, "Medicine Removed", f"{med['name']} deleted from stock list.", "info")

    def open_add_medicine_modal(self):
        win = ctk.CTkToplevel(self)
        win.title("Add New Medicine to Stock")
        win.geometry("540x640")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl_head = ctk.CTkLabel(win, text="📦 Add New Medicine to Stock", font=FONTS["h2"], text_color=COLORS["inventory"])
        lbl_head.pack(pady=(16, 8))
        
        form = ctk.CTkFrame(win, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=24, pady=0)
        form.grid_columnconfigure(1, weight=1)
        
        fields = [
            ("Item ID:", "id", f"MED-00{len(self.medicines)+1}"),
            ("Medicine Name:", "name", "Dolo 650 Tablet"),
            ("Formula / Salt:", "generic", "Paracetamol (650mg)"),
            ("Category:", "category", "Pain Relief / Fever"),
            ("Manufacturer:", "mfg", "Micro Labs"),
            ("Batch Number:", "batch", "DLO-992"),
            ("Expiry Date (YYYY-MM-DD):", "expiry", "2027-08-30"),
            ("Initial Stock:", "stock", "150"),
            ("Packaging Unit:", "unit", "Strip (15 tabs)"),
            ("Selling Price MRP (₹):", "mrp", "34.50"),
            ("Purchase Cost (₹):", "cost", "22.00"),
            ("Rack / Shelf:", "rack", "D-04-B")
        ]
        
        ents = {}
        for idx, (lbl_t, key, d_val) in enumerate(fields):
            lbl = ctk.CTkLabel(form, text=lbl_t, font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl.grid(row=idx, column=0, sticky="w", pady=2, padx=(0, 6))
            
            ent = ctk.CTkEntry(form, font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], height=30)
            ent.grid(row=idx, column=1, sticky="ew", pady=2)
            ent.insert(0, d_val)
            ents[key] = ent
            
        chk_cold = ctk.CTkCheckBox(form, text="Requires Refrigerator Storage (2-8°C)", font=FONTS["small_bold"], text_color=COLORS["clinical"])
        chk_cold.grid(row=len(fields), column=0, columnspan=2, sticky="w", pady=8)
        
        def save_drug():
            m_id = ents["id"].get().strip()
            name = ents["name"].get().strip()
            gen = ents["generic"].get().strip()
            
            if not m_id or not name:
                messagebox.showwarning("Incomplete", "Item ID and Medicine Name are required.", parent=win)
                return
            try:
                stk = int(ents["stock"].get().strip() or "0")
                mrp_v = float(ents["mrp"].get().strip() or "0.0")
                cost_v = float(ents["cost"].get().strip() or "0.0")
            except ValueError:
                messagebox.showwarning("Invalid Numbers", "Check stock and price numbers.", parent=win)
                return
                
            med_obj = {
                "id": m_id,
                "name": name,
                "generic": gen,
                "category": ents["category"].get().strip() or "General",
                "schedule": "Schedule H",
                "manufacturer": ents["mfg"].get().strip() or "Pharma India",
                "batch": ents["batch"].get().strip() or "BAT-01",
                "expiry": ents["expiry"].get().strip() or "2027-12-31",
                "days_to_expiry": 450,
                "stock": stk,
                "unit": ents["unit"].get().strip() or "Strip",
                "mrp": mrp_v,
                "cost_price": cost_v,
                "gst_pct": 12,
                "rack": ents["rack"].get().strip() or "General Rack",
                "cold_chain": bool(chk_cold.get()),
                "interactions": []
            }
            add_medicine(med_obj)
            self.medicines.append(med_obj)
            win.destroy()
            self.render_stock()
            show_toast(self, "Medicine Added", f"{name} added to stock ({stk} units).", "success")
            
        ctk.CTkButton(win, text="Save Medicine to Stock", height=38, font=FONTS["body_bold"], fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], text_color="#FFFFFF", command=save_drug).pack(fill="x", padx=24, pady=(6, 16))

    # --- TAB 2: SUPPLIER ORDERS ---

    def setup_grn_tab(self):
        self.tab_grn.grid_columnconfigure(0, weight=1)
        self.tab_grn.grid_rowconfigure(1, weight=1)
        
        top_bar = ctk.CTkFrame(self.tab_grn, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        top_bar.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(top_bar, text="📦 Supplier Purchase Orders & Stock Intake", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl.grid(row=0, column=0, sticky="w")
        
        btn_po = ctk.CTkButton(top_bar, text="+ Receive Stock from Supplier", height=28, font=FONTS["small_bold"], fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], text_color="#FFFFFF", command=self.open_inward_grn_modal)
        btn_po.grid(row=0, column=1, sticky="e")
        
        self.grn_scroll = ctk.CTkScrollableFrame(self.tab_grn, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.grn_scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.grn_scroll.grid_columnconfigure(0, weight=1)

    def render_grn_orders(self):
        for w in self.grn_scroll.winfo_children():
            w.destroy()
            
        pos = get_all_purchase_orders()
        for po in pos:
            c = ctk.CTkFrame(self.grn_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=4, padx=4)
            c.grid_columnconfigure(0, weight=1)
            
            r1 = ctk.CTkFrame(c, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            lbl_title = ctk.CTkLabel(r1, text=f"📋 {po['po_id']} — {po['supplier_name']}", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_title.grid(row=0, column=0, sticky="w")
            
            st_col = COLORS["clinical"] if "Received" in po["status"] else COLORS["warning"]
            lbl_st = ctk.CTkLabel(r1, text=f" {po['status']} ", font=FONTS["small_bold"], fg_color=st_col, text_color="#FFFFFF", corner_radius=4)
            lbl_st.grid(row=0, column=1, sticky="e")
            
            items_str = ", ".join(f"{it.get('medicine', 'Item')} (Qty: {it.get('qty', 10)})" if isinstance(it, dict) else str(it) for it in po.get("items", []))
            info_txt = f"📅 Date: {po['date']} | Total Value: ₹{po['total_amount']:.2f} | Received by: {po['created_by']}\n📦 Medicines Received: {items_str}"
            lbl_info = ctk.CTkLabel(c, text=info_txt, font=FONTS["small"], text_color=COLORS["text_muted"], justify="left")
            lbl_info.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

    def open_inward_grn_modal(self):
        win = ctk.CTkToplevel(self)
        win.title("Receive Stock from Supplier")
        win.geometry("500x460")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="Receive Stock from Supplier", font=FONTS["h2"], text_color=COLORS["inventory"])
        lbl.pack(pady=(16, 8))
        
        suppliers = get_all_suppliers()
        s_names = [s["name"] for s in suppliers] or ["MedLife Pharma Distributors", "Apex Healthcare Supply Co."]
        
        opt_s = ctk.CTkOptionMenu(win, values=s_names, width=340)
        opt_s.pack(pady=6)
        
        ent_po = ctk.CTkEntry(win, placeholder_text="Supplier Bill / Order No (e.g. PO-2026-904)", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=340)
        ent_po.pack(pady=6)
        ent_po.insert(0, f"PO-2026-{datetime.now().strftime('%M%S')}")
        
        med_names = [m["name"] for m in self.medicines] or ["Augmentin 625 Duo Tablet"]
        opt_med = ctk.CTkOptionMenu(win, values=med_names, width=340)
        opt_med.pack(pady=6)
        
        ent_qty = ctk.CTkEntry(win, placeholder_text="Quantity Received (e.g. 100)", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=340)
        ent_qty.pack(pady=6)
        ent_qty.insert(0, "100")
        
        ent_rate = ctk.CTkEntry(win, placeholder_text="Unit Purchase Price (₹)", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=340)
        ent_rate.pack(pady=6)
        ent_rate.insert(0, "145.00")
        
        def save():
            try:
                qty_val = int(ent_qty.get().strip() or "100")
                rate_val = float(ent_rate.get().strip() or "145.00")
            except ValueError:
                messagebox.showwarning("Invalid", "Check quantity and rate numbers.", parent=win)
                return
                
            po_id = ent_po.get().strip() or f"PO-{datetime.now().strftime('%M%S')}"
            selected_med = opt_med.get()
            
            po_obj = {
                "po_id": po_id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "supplier_name": opt_s.get(),
                "status": "Received & Added to Stock",
                "items": [{"medicine": selected_med, "qty": qty_val, "rate": rate_val}],
                "total_amount": qty_val * rate_val,
                "received_date": datetime.now().strftime("%Y-%m-%d"),
                "created_by": self.user_data["name"]
            }
            add_purchase_order(po_obj)
            
            # Increment stock in DB
            match_med = next((m for m in self.medicines if m["name"] == selected_med), None)
            if match_med:
                update_medicine_stock(match_med["id"], qty_val)
                match_med["stock"] += qty_val
                
            win.destroy()
            self.render_grn_orders()
            self.render_stock()
            show_toast(self, "Stock Received", f"{po_id}: Added +{qty_val} units of {selected_med}.", "success")

        ctk.CTkButton(win, text="Add to Stock", height=38, font=FONTS["body_bold"], fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], text_color="#FFFFFF", command=save).pack(pady=16)

    # --- TAB 3: FRIDGE TEMPERATURE MONITOR ---

    def setup_cold_tab(self):
        self.tab_cold.grid_columnconfigure(0, weight=1)
        self.tab_cold.grid_rowconfigure(2, weight=1)
        
        # Interactive Controls Strip
        ctrl_card = ctk.CTkFrame(self.tab_cold, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        ctrl_card.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        ctrl_card.grid_columnconfigure(1, weight=1)
        
        left_c = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        left_c.grid(row=0, column=0, padx=14, pady=8, sticky="w")
        
        ctk.CTkLabel(left_c, text="❄️ Medicine Refrigerator #01 (Vaccines & Insulin)", font=FONTS["body_bold"], text_color=COLORS["clinical"]).pack(anchor="w")
        ctk.CTkLabel(left_c, text="Temperature Sensor: Safe Range is 2°C to 8°C", font=FONTS["small"], text_color=COLORS["text_dim"]).pack(anchor="w")
        
        right_c = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        right_c.grid(row=0, column=1, sticky="e", padx=14)
        
        btn_spike = ctk.CTkButton(
            right_c,
            text="⚠️ Test High Temp Alarm (9.5°C)",
            height=30,
            font=FONTS["small_bold"],
            fg_color=COLORS["btn_danger"],
            hover_color=COLORS["btn_danger_hover"],
            text_color="#FFFFFF",
            command=self.simulate_temp_spike
        )
        btn_spike.pack(side="left", padx=4)
        
        btn_norm = ctk.CTkButton(
            right_c,
            text="❄️ Reset to Normal (4.2°C)",
            height=30,
            font=FONTS["small_bold"],
            fg_color=COLORS["clinical"],
            hover_color=COLORS["clinical_hover"],
            text_color="#FFFFFF",
            command=self.reset_temp
        )
        btn_norm.pack(side="left", padx=4)
        
        # Embedded Canvas Chart Component
        logs = get_temperature_logs(20)
        self.chart_widget = ColdChainChartCanvas(self.tab_cold, logs=logs, height=200)
        self.chart_widget.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        
        # Historical Table
        self.temp_scroll = ctk.CTkScrollableFrame(self.tab_cold, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.temp_scroll.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 10))
        self.temp_scroll.grid_columnconfigure(0, weight=1)

    def simulate_temp_spike(self):
        add_temperature_log("SENSOR-FRIDGE-01", 9.5, "QUARANTINE ALERT (>8°C)")
        logs = get_temperature_logs(20)
        self.chart_widget.update_logs(logs)
        self.render_temp_logs()
        show_toast(self, "🚨 Temperature Warning!", "Fridge reached 9.5°C! Above safe limit of 8°C.", "danger")

    def reset_temp(self):
        add_temperature_log("SENSOR-FRIDGE-01", 4.2, "Optimal (2-8°C)")
        logs = get_temperature_logs(20)
        self.chart_widget.update_logs(logs)
        self.render_temp_logs()
        show_toast(self, "Normal Temperature", "Fridge restored to safe 4.2°C.", "success")

    def render_temp_logs(self):
        for w in self.temp_scroll.winfo_children():
            w.destroy()
            
        logs = get_temperature_logs(20)
        for lg in logs:
            c = ctk.CTkFrame(self.temp_scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=2, padx=2)
            c.grid_columnconfigure(0, weight=1)
            
            t_col = COLORS["danger"] if lg.get("alert_triggered") else COLORS["clinical"]
            lbl_t = ctk.CTkLabel(c, text=f"🌡️ {lg['temperature']} °C — {lg['status']}", font=FONTS["small_bold"], text_color=t_col)
            lbl_t.grid(row=0, column=0, sticky="w", padx=10, pady=4)
            
            lbl_time = ctk.CTkLabel(c, text=f"🕒 {lg['timestamp']}", font=FONTS["small"], text_color=COLORS["text_dim"])
            lbl_time.grid(row=0, column=1, sticky="e", padx=10)

    # --- TAB 4: MEDICINE SUPPLIERS ---

    def setup_suppliers_tab(self):
        self.tab_suppliers.grid_columnconfigure(0, weight=1)
        self.tab_suppliers.grid_rowconfigure(2, weight=1)
        
        top_bar = ctk.CTkFrame(self.tab_suppliers, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
        top_bar.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(top_bar, text="🏢 Registered Medicine Suppliers & Distributors", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl.grid(row=0, column=0, sticky="w")
        
        btn_add_s = ctk.CTkButton(top_bar, text="+ Add Supplier", height=28, font=FONTS["small_bold"], fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], text_color="#FFFFFF", command=self.open_add_supplier_modal)
        btn_add_s.grid(row=0, column=1, sticky="e")
        
        self.ent_sup_search = ctk.CTkEntry(
            self.tab_suppliers,
            placeholder_text="🔍 Search suppliers by name, contact, or GST...",
            font=FONTS["small"],
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_main"],
            border_color=COLORS["border"],
            height=32
        )
        self.ent_sup_search.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        self.ent_sup_search.bind("<KeyRelease>", lambda e: self.render_suppliers())
        
        self.suppliers_scroll = ctk.CTkScrollableFrame(self.tab_suppliers, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.suppliers_scroll.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.suppliers_scroll.grid_columnconfigure(0, weight=1)

    def render_suppliers(self):
        for w in self.suppliers_scroll.winfo_children():
            w.destroy()
            
        suppliers = get_all_suppliers()
        q = self.ent_sup_search.get().strip().lower() if hasattr(self, "ent_sup_search") else ""
        if q:
            suppliers = [s for s in suppliers if q in s["name"].lower() or q in s.get("contact_person", "").lower() or q in s.get("gstin", "").lower()]

        for s in suppliers:
            c = ctk.CTkFrame(self.suppliers_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=4, padx=4)
            
            r1 = ctk.CTkFrame(c, fg_color="transparent")
            r1.pack(fill="x", padx=12, pady=(8, 2))
            
            lbl_name = ctk.CTkLabel(r1, text=f"🏢 {s['name']} (GSTIN: {s.get('gstin', 'N/A')})", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_name.pack(side="left")
            
            lbl_terms = ctk.CTkLabel(r1, text=f"Terms: {s.get('payment_terms', '30 Days Net')}", font=FONTS["small_bold"], text_color=COLORS["commerce"])
            lbl_terms.pack(side="right")
            
            info_txt = f"👤 Contact: {s.get('contact_person', 'Sales')} | 📞 {s.get('phone', 'N/A')} | ✉️ {s.get('email', 'N/A')}\n📍 Address: {s.get('address', 'N/A')}"
            lbl_info = ctk.CTkLabel(c, text=info_txt, font=FONTS["small"], text_color=COLORS["text_muted"], justify="left")
            lbl_info.pack(anchor="w", padx=12, pady=(0, 8))

    def open_add_supplier_modal(self):
        win = ctk.CTkToplevel(self)
        win.title("Add Medicine Supplier")
        win.geometry("480x480")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="Add New Medicine Supplier", font=FONTS["h2"], text_color=COLORS["inventory"])
        lbl.pack(pady=(16, 10))
        
        form = ctk.CTkFrame(win, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=24, pady=0)
        form.grid_columnconfigure(1, weight=1)
        
        fields = [
            ("Company Name:", "name", "Sunrise Pharma Wholesalers"),
            ("Contact Person:", "contact", "Manish Joshi"),
            ("Phone Number:", "phone", "+91 98220 99881"),
            ("Email Address:", "email", "orders@sunrisepharma.com"),
            ("GST Number:", "gstin", "27AABCS8899D1Z4"),
            ("Warehouse Address:", "address", "Unit 12, Logistic Hub, Bhiwandi")
        ]
        ents = {}
        for idx, (label, key, val) in enumerate(fields):
            lbl = ctk.CTkLabel(form, text=label, font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl.grid(row=idx, column=0, sticky="w", pady=4, padx=(0, 8))
            
            ent = ctk.CTkEntry(form, font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], height=32)
            ent.grid(row=idx, column=1, sticky="ew", pady=4)
            ent.insert(0, val)
            ents[key] = ent
            
        def save():
            name = ents["name"].get().strip()
            if not name:
                messagebox.showwarning("Incomplete", "Supplier Name is required.", parent=win)
                return
            s_id = f"SUP-{len(get_all_suppliers())+1:02d}"
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("INSERT INTO suppliers VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (s_id, name, ents["contact"].get().strip(), ents["phone"].get().strip(),
                             ents["email"].get().strip(), ents["gstin"].get().strip(),
                             ents["address"].get().strip(), "30 Days Net"))
                conn.commit()
                conn.close()
                win.destroy()
                self.render_suppliers()
                show_toast(self, "Supplier Registered", f"{name} ({s_id}) added to suppliers.", "success")
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=win)
                
        ctk.CTkButton(win, text="Save Supplier", height=38, font=FONTS["body_bold"], fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], text_color="#FFFFFF", command=save).pack(fill="x", padx=24, pady=16)

    def load_all_data(self):
        self.medicines = get_all_medicines()
        self.render_stock()
        self.render_grn_orders()
        self.render_temp_logs()
        self.render_suppliers()
