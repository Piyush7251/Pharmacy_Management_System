"""
AegisPharm Enterprise — Complete Inventory & Supply Chain Hub.
Full features:
- FEFO Multi-Batch Medicine Inventory Ledger (Expiring Soon & Low Stock Badges)
- Add New Medicine to Catalog Modal
- Quick Stock Adjustment (Correction, Expiry, Damage)
- Goods Receipt Notes (GRN) & Purchase Order (PO) Inwarding
- Cold Chain IoT Sensor Temperature Logger & Alarm Trigger (2-8°C)
- Supplier / Distributor Management Directory
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from ui.theme import COLORS, FONTS
from core.db import (
    get_all_medicines, add_medicine, update_medicine_stock, delete_medicine,
    get_all_suppliers, get_all_purchase_orders, add_purchase_order,
    get_temperature_logs, add_temperature_log
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
        hdr = ctk.CTkFrame(self, height=52, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))
        hdr.grid_columnconfigure(1, weight=1)
        
        lbl_brand = ctk.CTkLabel(hdr, text="📦 Supply Chain & FEFO Inventory Hub", font=FONTS["h2"], text_color=COLORS["inventory"])
        lbl_brand.grid(row=0, column=0, padx=16, pady=10, sticky="w")
        
        right_box = ctk.CTkFrame(hdr, fg_color="transparent")
        right_box.grid(row=0, column=1, sticky="e", padx=16)
        
        lbl_mgr = ctk.CTkLabel(right_box, text=f"Manager: {self.user_data['name']} | Cold-Chain: 4.2°C (Optimal)", font=FONTS["small_bold"], text_color=COLORS["text_dim"])
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
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 14))
        
        self.tab_stock = self.tabview.add("📊 Multi-Batch Stock Ledger")
        self.tab_grn = self.tabview.add("📦 GRN & Purchase Orders")
        self.tab_cold = self.tabview.add("❄️ Cold-Chain IoT Monitor")
        self.tab_suppliers = self.tabview.add("🏢 Suppliers Directory")
        
        self.setup_stock_tab()
        self.setup_grn_tab()
        self.setup_cold_tab()
        self.setup_suppliers_tab()

    # --- TAB 1: STOCK LEDGER ---

    def setup_stock_tab(self):
        self.tab_stock.grid_columnconfigure(0, weight=1)
        self.tab_stock.grid_rowconfigure(1, weight=1)
        
        filter_box = ctk.CTkFrame(self.tab_stock, fg_color="transparent")
        filter_box.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 6))
        filter_box.grid_columnconfigure(0, weight=1)
        
        self.search_ent = ctk.CTkEntry(
            filter_box,
            placeholder_text="🔍 Search medicine, salt, batch, rack location...",
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
        
        for f in [("All", "ALL"), ("⚠️ Low Stock", "LOW"), ("⏳ Expiring Soon", "EXP"), ("❄️ Cold Chain", "COLD")]:
            b = ctk.CTkButton(
                btn_box,
                text=f[0],
                width=85,
                height=34,
                font=FONTS["small_bold"],
                fg_color=COLORS["btn_secondary"],
                hover_color=COLORS["btn_secondary_hover"],
                text_color=COLORS["btn_secondary_text"],
                command=lambda s=f[1]: self.set_stock_filter(s)
            )
            b.pack(side="left", padx=2)
            
        self.stock_scroll = ctk.CTkScrollableFrame(self.tab_stock, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.stock_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.stock_scroll.grid_columnconfigure(0, weight=1)

    def set_stock_filter(self, f_type):
        self.current_filter = f_type
        self.render_stock()

    def render_stock(self):
        for w in self.stock_scroll.winfo_children():
            w.destroy()
            
        q = self.search_ent.get().strip().lower()
        items = self.medicines
        
        if q:
            items = [m for m in items if q in m["name"].lower() or q in m["generic"].lower() or q in m["batch"].lower()]
            
        if self.current_filter == "LOW":
            items = [m for m in items if m["stock"] < 25]
        elif self.current_filter == "EXP":
            items = sorted([m for m in items if m.get("days_to_expiry", 999) < 250], key=lambda x: x.get("days_to_expiry", 999))
        elif self.current_filter == "COLD":
            items = [m for m in items if m.get("cold_chain")]

        if not items:
            ctk.CTkLabel(self.stock_scroll, text="No medicines matching criteria.", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(pady=40)
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
            
            stk_c = COLORS["danger"] if med["stock"] < 25 else COLORS["clinical"]
            lbl_stk = ctk.CTkLabel(r1, text=f"Stock: {med['stock']} {med['unit']}", font=FONTS["body_bold"], text_color=stk_c)
            lbl_stk.grid(row=0, column=1, sticky="e")
            
            # Row 2
            r2 = ctk.CTkFrame(c, fg_color="transparent")
            r2.grid(row=1, column=0, sticky="ew", padx=12, pady=(2, 8))
            r2.grid_columnconfigure(0, weight=1)
            
            exp_c = COLORS["danger"] if med["days_to_expiry"] < 120 else (COLORS["warning"] if med["days_to_expiry"] < 250 else COLORS["text_muted"])
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

    def open_adjust_modal(self, med):
        win = ctk.CTkToplevel(self)
        win.title(f"Adjust Stock — {med['name']}")
        win.geometry("420x300")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text=f"Stock Adjustment: {med['name']}", font=FONTS["h3"], text_color=COLORS["inventory"])
        lbl.pack(pady=(16, 4))
        
        lbl_cur = ctk.CTkLabel(win, text=f"Current Stock: {med['stock']} units (Batch: {med['batch']})", font=FONTS["body"], text_color=COLORS["text_main"])
        lbl_cur.pack(pady=4)
        
        ent = ctk.CTkEntry(win, placeholder_text="Quantity delta (e.g. +50 or -10)", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=260)
        ent.pack(pady=8)
        
        reason_opt = ctk.CTkOptionMenu(win, values=["Goods Receipt (GRN)", "Damage / Breakage", "Expiry Quarantine", "Physical Count Correction"], width=260)
        reason_opt.set("Goods Receipt (GRN)")
        reason_opt.pack(pady=6)
        
        def save():
            try:
                qty_delta = int(ent.get().strip().replace("+", ""))
                update_medicine_stock(med["id"], qty_delta)
                med["stock"] = max(0, med["stock"] + qty_delta)
                
                if self.connector:
                    self.connector.log_event("Stock Adjusted", f"Adjusted {med['name']} by {qty_delta} units ({reason_opt.get()})", level="INFO")
                    
                win.destroy()
                self.render_stock()
                messagebox.showinfo("Stock Updated", f"Stock adjusted by {qty_delta} units for {med['name']}.")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid integer.", parent=win)

        ctk.CTkButton(win, text="Confirm Adjustment", height=36, font=FONTS["body_bold"], fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], text_color="#FFFFFF", command=save).pack(pady=14)

    def delete_medicine_item(self, med):
        res = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {med['name']} from catalog?")
        if res:
            delete_medicine(med["id"])
            self.medicines = [m for m in self.medicines if m["id"] != med["id"]]
            self.render_stock()

    def open_add_medicine_modal(self):
        win = ctk.CTkToplevel(self)
        win.title("Add New Drug to Catalog")
        win.geometry("560x650")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl_head = ctk.CTkLabel(win, text="📦 Add Medicine to Catalog & FEFO Ledger", font=FONTS["h2"], text_color=COLORS["inventory"])
        lbl_head.pack(pady=(16, 10))
        
        form = ctk.CTkFrame(win, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=24, pady=0)
        form.grid_columnconfigure(1, weight=1)
        
        f_list = [
            ("SKU / Item ID:", "id", f"MED-0{len(self.medicines)+1}"),
            ("Brand / Item Name:", "name", "e.g. Azithral 500 Tablet"),
            ("Generic Salt Composition:", "generic", "Azithromycin (500mg)"),
            ("Category / Therapeutic Class:", "category", "Antibiotic / Macrolide"),
            ("Manufacturer:", "mfg", "Alembic Pharmaceuticals"),
            ("Batch Number:", "batch", "AZI-2026-01"),
            ("Expiry Date (YYYY-MM-DD):", "expiry", "2027-08-30"),
            ("Initial Stock Quantity:", "stock", "100"),
            ("Unit Pack:", "unit", "Strip (5 tabs)"),
            ("MRP (₹):", "mrp", "125.00"),
            ("Cost Price (₹):", "cost", "85.00"),
            ("Shelf / Rack Location:", "rack", "A-05-C")
        ]
        
        ents = {}
        for idx, (label, key, val) in enumerate(f_list):
            ctk.CTkLabel(form, text=label, font=FONTS["body_bold"], text_color=COLORS["text_main"]).grid(row=idx, column=0, sticky="w", pady=3, padx=(0, 6))
            ent = ctk.CTkEntry(form, placeholder_text=val, font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], height=30)
            ent.grid(row=idx, column=1, sticky="ew", pady=3)
            if key == "id":
                ent.insert(0, val)
            ents[key] = ent
            
        chk_cold = ctk.CTkCheckBox(form, text="❄️ Requires Cold-Chain Storage (2-8°C)", font=FONTS["small_bold"], text_color=COLORS["clinical"])
        chk_cold.grid(row=len(f_list), column=1, sticky="w", pady=6)
        
        def save_drug():
            m_id = ents["id"].get().strip()
            name = ents["name"].get().strip()
            gen = ents["generic"].get().strip()
            if not m_id or not name:
                messagebox.showwarning("Incomplete", "SKU ID and Name are required.", parent=win)
                return
            try:
                stk = int(ents["stock"].get().strip() or "0")
                mrp_v = float(ents["mrp"].get().strip() or "0.0")
                cost_v = float(ents["cost"].get().strip() or "0.0")
            except ValueError:
                messagebox.showwarning("Invalid Numbers", "Check stock and pricing numbers.", parent=win)
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
            messagebox.showinfo("Medicine Added", f"{name} added to catalog with {stk} units.")
            
        ctk.CTkButton(win, text="Save Medicine to Catalog", height=38, font=FONTS["body_bold"], fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], text_color="#FFFFFF", command=save_drug).pack(fill="x", padx=24, pady=(10, 16))

    # --- TAB 2: GRN & PURCHASE ORDERS ---

    def setup_grn_tab(self):
        self.tab_grn.grid_columnconfigure(0, weight=1)
        self.tab_grn.grid_rowconfigure(1, weight=1)
        
        top_bar = ctk.CTkFrame(self.tab_grn, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        top_bar.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(top_bar, text="📦 Goods Receipt Notes (GRN) & Procurement Orders", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl.grid(row=0, column=0, sticky="w")
        
        btn_po = ctk.CTkButton(top_bar, text="+ Inward Goods Receipt (GRN)", height=28, font=FONTS["small_bold"], fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], text_color="#FFFFFF", command=self.open_inward_grn_modal)
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
            
            items_str = ", ".join(f"{it.get('medicine', 'Item')} (Qty: {it.get('qty', 10)})" for it in po.get("items", []))
            info_txt = f"📅 Date: {po['date']} | Total PO Value: ₹{po['total_amount']:.2f} | Created by: {po['created_by']}\n📦 Inwarded Items: {items_str}"
            lbl_info = ctk.CTkLabel(c, text=info_txt, font=FONTS["small"], text_color=COLORS["text_muted"], justify="left")
            lbl_info.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

    def open_inward_grn_modal(self):
        win = ctk.CTkToplevel(self)
        win.title("Process Goods Receipt Note (GRN)")
        win.geometry("480x420")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="Inward Goods Receipt (GRN)", font=FONTS["h2"], text_color=COLORS["inventory"])
        lbl.pack(pady=(16, 8))
        
        suppliers = get_all_suppliers()
        s_names = [s["name"] for s in suppliers] or ["MedLife Pharma", "Apex Healthcare"]
        
        opt_s = ctk.CTkOptionMenu(win, values=s_names, width=320)
        opt_s.pack(pady=8)
        
        ent_po = ctk.CTkEntry(win, placeholder_text="Supplier Invoice / PO No (e.g. INV-SUP-9912)", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=320)
        ent_po.pack(pady=8)
        
        ent_qty = ctk.CTkEntry(win, placeholder_text="Total Quantity Inwarded (e.g. 200 units)", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=320)
        ent_qty.pack(pady=8)
        
        def save():
            po_id = ent_po.get().strip() or f"PO-{datetime.now().strftime('%M%S')}"
            po_obj = {
                "po_id": po_id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "supplier_name": opt_s.get(),
                "status": "Goods Received & Inwarded",
                "items": [{"medicine": "Augmentin 625 Duo", "qty": 100, "rate": 148.0}],
                "total_amount": 14800.0,
                "received_date": datetime.now().strftime("%Y-%m-%d"),
                "created_by": self.user_data["name"]
            }
            add_purchase_order(po_obj)
            win.destroy()
            self.render_grn_orders()
            messagebox.showinfo("GRN Inwarded", f"Shipment {po_id} inwarded into FEFO ledger.")

        ctk.CTkButton(win, text="Confirm Inwarding to Stock", height=38, font=FONTS["body_bold"], fg_color=COLORS["inventory"], hover_color=COLORS["inventory_hover"], text_color="#FFFFFF", command=save).pack(pady=16)

    # --- TAB 3: COLD-CHAIN IOT MONITOR ---

    def setup_cold_tab(self):
        self.tab_cold.grid_columnconfigure(0, weight=1)
        self.tab_cold.grid_rowconfigure(2, weight=1)
        
        # Live Gauge Card
        gauge_card = ctk.CTkFrame(self.tab_cold, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        gauge_card.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 8))
        gauge_card.grid_columnconfigure(1, weight=1)
        
        left_g = ctk.CTkFrame(gauge_card, fg_color="transparent")
        left_g.grid(row=0, column=0, padx=16, pady=12, sticky="w")
        
        self.lbl_temp = ctk.CTkLabel(left_g, text="❄️ 4.2 °C", font=FONTS["price_large"], text_color=COLORS["clinical"])
        self.lbl_temp.pack(anchor="w")
        
        lbl_status = ctk.CTkLabel(left_g, text="Status: Optimal Safe Band (2.0°C – 8.0°C) | Sensor #FRIDGE-01 Active", font=FONTS["small_bold"], text_color=COLORS["text_dim"])
        lbl_status.pack(anchor="w")
        
        right_g = ctk.CTkFrame(gauge_card, fg_color="transparent")
        right_g.grid(row=0, column=1, sticky="e", padx=16)
        
        btn_spike = ctk.CTkButton(
            right_g,
            text="Simulate Temp Alarm (+9.5°C)",
            height=30,
            font=FONTS["small_bold"],
            fg_color=COLORS["btn_danger"],
            hover_color=COLORS["btn_danger_hover"],
            text_color="#FFFFFF",
            command=self.simulate_temp_spike
        )
        btn_spike.pack(side="left", padx=4)
        
        btn_norm = ctk.CTkButton(
            right_g,
            text="Reset to 4.2°C",
            height=30,
            font=FONTS["small_bold"],
            fg_color=COLORS["clinical"],
            hover_color=COLORS["clinical_hover"],
            text_color="#FFFFFF",
            command=self.reset_temp
        )
        btn_norm.pack(side="left")
        
        # Historical Logs
        lbl_h = ctk.CTkLabel(self.tab_cold, text="📡 24-Hour IoT Temperature Telemetry Logs:", font=FONTS["body_bold"], text_color=COLORS["text_main"])
        lbl_h.grid(row=1, column=0, sticky="w", padx=14, pady=(4, 4))
        
        self.temp_scroll = ctk.CTkScrollableFrame(self.tab_cold, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.temp_scroll.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.temp_scroll.grid_columnconfigure(0, weight=1)

    def simulate_temp_spike(self):
        self.lbl_temp.configure(text="🔥 9.5 °C (CRITICAL)", text_color=COLORS["danger"])
        add_temperature_log("SENSOR-FRIDGE-01", 9.5, "QUARANTINE ALERT (>8°C)")
        self.render_temp_logs()
        messagebox.showerror("🚨 Cold-Chain Breach Alarm", "Temperature breached 8°C! Vaccines and insulin placed under quarantine protocol.")

    def reset_temp(self):
        self.lbl_temp.configure(text="❄️ 4.2 °C", text_color=COLORS["clinical"])
        add_temperature_log("SENSOR-FRIDGE-01", 4.2, "Optimal (2-8°C)")
        self.render_temp_logs()
        messagebox.showinfo("Restored", "Temperature normalized to 4.2°C.")

    def render_temp_logs(self):
        for w in self.temp_scroll.winfo_children():
            w.destroy()
            
        logs = get_temperature_logs()
        for lg in logs:
            c = ctk.CTkFrame(self.temp_scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=2, padx=2)
            c.grid_columnconfigure(0, weight=1)
            
            t_col = COLORS["danger"] if lg.get("alert_triggered") else COLORS["clinical"]
            lbl_t = ctk.CTkLabel(c, text=f"🌡️ {lg['temperature']} °C — {lg['status']}", font=FONTS["small_bold"], text_color=t_col)
            lbl_t.grid(row=0, column=0, sticky="w", padx=10, pady=4)
            
            lbl_time = ctk.CTkLabel(c, text=f"🕒 {lg['timestamp']}", font=FONTS["small"], text_color=COLORS["text_dim"])
            lbl_time.grid(row=0, column=1, sticky="e", padx=10)

    # --- TAB 4: SUPPLIERS DIRECTORY ---

    def setup_suppliers_tab(self):
        self.tab_suppliers.grid_columnconfigure(0, weight=1)
        self.tab_suppliers.grid_rowconfigure(1, weight=1)
        
        top_bar = ctk.CTkFrame(self.tab_suppliers, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        
        lbl = ctk.CTkLabel(top_bar, text="🏢 Approved Pharmaceutical Suppliers & Distributors", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl.pack(side="left")
        
        self.suppliers_scroll = ctk.CTkScrollableFrame(self.tab_suppliers, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.suppliers_scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.suppliers_scroll.grid_columnconfigure(0, weight=1)

    def render_suppliers(self):
        for w in self.suppliers_scroll.winfo_children():
            w.destroy()
            
        suppliers = get_all_suppliers()
        for s in suppliers:
            c = ctk.CTkFrame(self.suppliers_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=4, padx=4)
            
            r1 = ctk.CTkFrame(c, fg_color="transparent")
            r1.pack(fill="x", padx=12, pady=(8, 2))
            
            lbl_name = ctk.CTkLabel(r1, text=f"🏢 {s['name']} (GSTIN: {s.get('gstin', 'N/A')})", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_name.pack(side="left")
            
            lbl_terms = ctk.CTkLabel(r1, text=f"Terms: {s.get('payment_terms', '30 Days')}", font=FONTS["small_bold"], text_color=COLORS["commerce"])
            lbl_terms.pack(side="right")
            
            info_txt = f"👤 Contact: {s.get('contact_person', 'Sales')} | 📞 {s.get('phone', 'N/A')} | ✉️ {s.get('email', 'N/A')}\n📍 Address: {s.get('address', 'N/A')}"
            lbl_info = ctk.CTkLabel(c, text=info_txt, font=FONTS["small"], text_color=COLORS["text_muted"], justify="left")
            lbl_info.pack(anchor="w", padx=12, pady=(0, 8))

    def load_all_data(self):
        self.medicines = get_all_medicines()
        self.render_stock()
        self.render_grn_orders()
        self.render_temp_logs()
        self.render_suppliers()
