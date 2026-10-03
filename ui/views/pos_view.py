"""
POS & Counter Dispensing View (Commerce & Billing Layer).
Features fast item search, cart management, instant allergy & drug-interaction warning banners,
split-tender payments, and receipt generation.
"""

import customtkinter as ctk
from ui.theme import COLORS, FONTS
from data.mock_db import MEDICINES_CATALOG, PATIENTS
from tkinter import messagebox

class POSView(ctk.CTkFrame):
    def __init__(self, parent, show_notification_cb=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.show_notification = show_notification_cb
        
        self.cart = []
        self.selected_patient = PATIENTS[0]  # Default patient with known penicillin allergy
        
        self.grid_columnconfigure(0, weight=6)  # Left: Product search & catalog
        self.grid_columnconfigure(1, weight=4)  # Right: Cart & Billing summary
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_left_panel()
        self.setup_right_panel()
        self.refresh_catalog_table(MEDICINES_CATALOG)

    def setup_left_panel(self):
        left_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(2, weight=1)
        
        # Header & Patient Selector
        top_bar = ctk.CTkFrame(left_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        top_bar.grid_columnconfigure(1, weight=1)
        
        lbl_title = ctk.CTkLabel(top_bar, text="🛒 POS Counter & Dispensing", font=FONTS["h2"], text_color=COLORS["commerce"])
        lbl_title.grid(row=0, column=0, sticky="w")
        
        # Patient Card summary
        patient_frame = ctk.CTkFrame(top_bar, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border_light"])
        patient_frame.grid(row=0, column=1, sticky="e", padx=(10, 0))
        
        self.lbl_patient_info = ctk.CTkLabel(
            patient_frame,
            text=f"👤 Patient: {self.selected_patient['name']} | Allergies: {', '.join(self.selected_patient['allergies']) or 'None'}",
            font=FONTS["small_bold"],
            text_color=COLORS["danger"] if self.selected_patient['allergies'] else COLORS["text_muted"],
            padx=12,
            pady=6
        )
        self.lbl_patient_info.pack(side="left")
        
        btn_change_pat = ctk.CTkButton(
            patient_frame,
            text="Change Patient",
            width=100,
            height=26,
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_secondary_hover"],
            font=FONTS["small"],
            command=self.open_patient_selector
        )
        btn_change_pat.pack(side="right", padx=(0, 6), pady=4)
        
        # Search Box & Category Filters
        search_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search medicine name, generic composition, barcode, or rack...",
            font=FONTS["body"],
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            height=38
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        btn_clear = ctk.CTkButton(
            search_frame,
            text="Clear",
            width=70,
            height=38,
            fg_color=COLORS["btn_secondary"],
            hover_color=COLORS["btn_secondary_hover"],
            command=self.clear_search
        )
        btn_clear.grid(row=0, column=1)
        
        # Medicine Catalog Scrollable List
        self.catalog_scroll = ctk.CTkScrollableFrame(
            left_frame,
            fg_color=COLORS["bg_base"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.catalog_scroll.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.catalog_scroll.grid_columnconfigure(0, weight=1)

    def setup_right_panel(self):
        right_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)
        
        # Cart Header
        cart_header = ctk.CTkFrame(right_frame, fg_color="transparent")
        cart_header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        cart_header.grid_columnconfigure(0, weight=1)
        
        lbl_cart = ctk.CTkLabel(cart_header, text="🧾 Active Bill / Prescription", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl_cart.grid(row=0, column=0, sticky="w")
        
        btn_clear_cart = ctk.CTkButton(
            cart_header,
            text="Clear Cart",
            width=80,
            height=26,
            fg_color=COLORS["btn_danger"],
            hover_color=COLORS["btn_danger_hover"],
            font=FONTS["small"],
            command=self.clear_cart
        )
        btn_clear_cart.grid(row=0, column=1)
        
        # Clinical Decision Support System (CDSS) Safety Banner
        self.cdss_banner = ctk.CTkFrame(right_frame, fg_color="transparent", corner_radius=8)
        self.cdss_banner.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        self.lbl_cdss_warning = ctk.CTkLabel(
            self.cdss_banner,
            text="🛡️ CDSS Clinical Safety: No active interactions detected.",
            font=FONTS["small_bold"],
            text_color=COLORS["clinical"],
            wraplength=380,
            justify="left"
        )
        self.lbl_cdss_warning.pack(fill="x", padx=10, pady=6)
        
        # Cart Items Scrollable Frame
        self.cart_scroll = ctk.CTkScrollableFrame(
            right_frame,
            fg_color=COLORS["bg_base"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.cart_scroll.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 12))
        self.cart_scroll.grid_columnconfigure(0, weight=1)
        
        # Bottom Summary & Checkout Frame
        summary_frame = ctk.CTkFrame(right_frame, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        summary_frame.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 16))
        
        # Breakdown
        self.lbl_subtotal = ctk.CTkLabel(summary_frame, text="Subtotal: ₹ 0.00", font=FONTS["body"], text_color=COLORS["text_muted"])
        self.lbl_subtotal.pack(anchor="w", padx=16, pady=(10, 2))
        
        self.lbl_gst = ctk.CTkLabel(summary_frame, text="Estimated GST (12%): ₹ 0.00", font=FONTS["small"], text_color=COLORS["text_dim"])
        self.lbl_gst.pack(anchor="w", padx=16, pady=2)
        
        self.lbl_total = ctk.CTkLabel(summary_frame, text="Total Payable: ₹ 0.00", font=FONTS["price_large"], text_color=COLORS["commerce"])
        self.lbl_total.pack(anchor="w", padx=16, pady=(4, 12))
        
        # Payment Buttons Row
        pay_btn_row = ctk.CTkFrame(summary_frame, fg_color="transparent")
        pay_btn_row.pack(fill="x", padx=16, pady=(0, 12))
        pay_btn_row.grid_columnconfigure((0, 1), weight=1)
        
        btn_upi = ctk.CTkButton(
            pay_btn_row,
            text="⚡ UPI / QR Pay",
            height=42,
            fg_color=COLORS["clinical"],
            hover_color=COLORS["clinical_hover"],
            font=FONTS["body_bold"],
            command=lambda: self.process_payment("UPI / QR")
        )
        btn_upi.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        
        btn_cash = ctk.CTkButton(
            pay_btn_row,
            text="💵 Cash / Card",
            height=42,
            fg_color=COLORS["btn_primary"],
            hover_color=COLORS["btn_primary_hover"],
            font=FONTS["body_bold"],
            command=lambda: self.process_payment("Cash / Card")
        )
        btn_cash.grid(row=0, column=1, sticky="ew", padx=(6, 0))

    def refresh_catalog_table(self, items):
        for widget in self.catalog_scroll.winfo_children():
            widget.destroy()
            
        if not items:
            lbl_empty = ctk.CTkLabel(self.catalog_scroll, text="No medicines matching search query.", font=FONTS["body"], text_color=COLORS["text_dim"])
            lbl_empty.pack(pady=40)
            return

        for med in items:
            card = ctk.CTkFrame(self.catalog_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", pady=4, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            # Top row: Name, Schedule Badge, MRP
            header_row = ctk.CTkFrame(card, fg_color="transparent")
            header_row.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
            header_row.grid_columnconfigure(0, weight=1)
            
            name_text = f"{med['name']}"
            lbl_name = ctk.CTkLabel(header_row, text=name_text, font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_name.grid(row=0, column=0, sticky="w")
            
            # Badge Schedule
            sch_color = COLORS["danger"] if "Schedule X" in med["schedule"] else (COLORS["inventory"] if "Schedule H" in med["schedule"] else COLORS["info"])
            lbl_sch = ctk.CTkLabel(header_row, text=f" {med['schedule']} ", font=FONTS["small_bold"], fg_color=sch_color, text_color="#000000", corner_radius=4)
            lbl_sch.grid(row=0, column=1, padx=(6, 12))
            
            lbl_mrp = ctk.CTkLabel(header_row, text=f"₹ {med['mrp']:.2f}", font=FONTS["h3"], text_color=COLORS["clinical"])
            lbl_mrp.grid(row=0, column=2, sticky="e")
            
            # Details: Generic, Batch, Expiry, Stock, Rack
            detail_text = f"🧪 {med['generic']}\n📦 Batch: {med['batch']} | Exp: {med['expiry']} | 📍 Rack: {med['rack']} | Stock: {med['stock']} {med['unit']}"
            lbl_details = ctk.CTkLabel(card, text=detail_text, font=FONTS["small"], text_color=COLORS["text_muted"], justify="left")
            lbl_details.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
            
            # Action Row
            act_row = ctk.CTkFrame(card, fg_color="transparent")
            act_row.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))
            
            # Cold chain tag if any
            if med.get("cold_chain"):
                lbl_cold = ctk.CTkLabel(act_row, text="❄️ Cold Chain (2-8°C)", font=FONTS["small_bold"], text_color=COLORS["info"])
                lbl_cold.pack(side="left")
            
            btn_add = ctk.CTkButton(
                act_row,
                text="+ Dispense / Add to Bill",
                height=28,
                width=160,
                fg_color=COLORS["btn_primary"],
                hover_color=COLORS["btn_primary_hover"],
                font=FONTS["small_bold"],
                command=lambda m=med: self.add_to_cart(m)
            )
            btn_add.pack(side="right")

    def on_search(self, event=None):
        q = self.search_entry.get().strip().lower()
        if not q:
            self.refresh_catalog_table(MEDICINES_CATALOG)
            return
            
        filtered = [
            m for m in MEDICINES_CATALOG
            if q in m["name"].lower() or q in m["generic"].lower() or q in m["batch"].lower() or q in m["rack"].lower()
        ]
        self.refresh_catalog_table(filtered)

    def clear_search(self):
        self.search_entry.delete(0, "end")
        self.refresh_catalog_table(MEDICINES_CATALOG)

    def add_to_cart(self, med):
        # Check if already in cart
        for item in self.cart:
            if item["med"]["id"] == med["id"]:
                item["qty"] += 1
                self.update_cart_ui()
                return
                
        self.cart.append({
            "med": med,
            "qty": 1
        })
        self.update_cart_ui()

    def update_cart_ui(self):
        for widget in self.cart_scroll.winfo_children():
            widget.destroy()
            
        if not self.cart:
            lbl_empty = ctk.CTkLabel(self.cart_scroll, text="Cart is empty.\nAdd medicines from catalog.", font=FONTS["body"], text_color=COLORS["text_dim"])
            lbl_empty.pack(pady=40)
            self.lbl_subtotal.configure(text="Subtotal: ₹ 0.00")
            self.lbl_gst.configure(text="Estimated GST: ₹ 0.00")
            self.lbl_total.configure(text="Total Payable: ₹ 0.00")
            self.check_cdss_safety()
            return
            
        subtotal = 0.0
        gst_total = 0.0
        
        for idx, item in enumerate(self.cart):
            med = item["med"]
            qty = item["qty"]
            item_total = med["mrp"] * qty
            subtotal += item_total
            gst_total += item_total * (med["gst_pct"] / 100.0)
            
            c_row = ctk.CTkFrame(self.cart_scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
            c_row.pack(fill="x", pady=4, padx=2)
            c_row.grid_columnconfigure(0, weight=1)
            
            # Item Name & Price
            r1 = ctk.CTkFrame(c_row, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=8, pady=(6, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            lbl_n = ctk.CTkLabel(r1, text=f"{med['name']}", font=FONTS["small_bold"], text_color=COLORS["text_main"])
            lbl_n.grid(row=0, column=0, sticky="w")
            
            lbl_p = ctk.CTkLabel(r1, text=f"₹ {item_total:.2f}", font=FONTS["small_bold"], text_color=COLORS["clinical"])
            lbl_p.grid(row=0, column=1, sticky="e")
            
            # Qty controls
            r2 = ctk.CTkFrame(c_row, fg_color="transparent")
            r2.grid(row=1, column=0, sticky="ew", padx=8, pady=(2, 6))
            
            lbl_rate = ctk.CTkLabel(r2, text=f"@ ₹{med['mrp']:.2f}", font=FONTS["small"], text_color=COLORS["text_dim"])
            lbl_rate.pack(side="left")
            
            btn_del = ctk.CTkButton(
                r2, text="🗑️", width=26, height=22, fg_color=COLORS["btn_danger"], hover_color=COLORS["btn_danger_hover"],
                command=lambda i=idx: self.remove_cart_item(i)
            )
            btn_del.pack(side="right", padx=(4, 0))
            
            btn_plus = ctk.CTkButton(
                r2, text="+", width=26, height=22, fg_color=COLORS["btn_secondary"], hover_color=COLORS["btn_secondary_hover"],
                command=lambda i=idx: self.change_qty(i, 1)
            )
            btn_plus.pack(side="right", padx=(2, 0))
            
            lbl_q = ctk.CTkLabel(r2, text=f"{qty}", font=FONTS["small_bold"], width=24)
            lbl_q.pack(side="right", padx=2)
            
            btn_minus = ctk.CTkButton(
                r2, text="-", width=26, height=22, fg_color=COLORS["btn_secondary"], hover_color=COLORS["btn_secondary_hover"],
                command=lambda i=idx: self.change_qty(i, -1)
            )
            btn_minus.pack(side="right")
            
        grand_total = subtotal
        self.lbl_subtotal.configure(text=f"Subtotal: ₹ {subtotal:.2f}")
        self.lbl_gst.configure(text=f"Included GST (~12%): ₹ {gst_total:.2f}")
        self.lbl_total.configure(text=f"Total Payable: ₹ {grand_total:.2f}")
        
        self.check_cdss_safety()

    def change_qty(self, index, delta):
        if 0 <= index < len(self.cart):
            self.cart[index]["qty"] += delta
            if self.cart[index]["qty"] <= 0:
                self.cart.pop(index)
            self.update_cart_ui()

    def remove_cart_item(self, index):
        if 0 <= index < len(self.cart):
            self.cart.pop(index)
            self.update_cart_ui()

    def clear_cart(self):
        self.cart = []
        self.update_cart_ui()

    def check_cdss_safety(self):
        """Clinical Decision Support System rule validation."""
        warnings = []
        
        # 1. Check Allergy against Patient Profile
        if self.selected_patient and self.selected_patient.get("allergies"):
            patient_allergies = [a.lower() for a in self.selected_patient["allergies"]]
            for item in self.cart:
                med = item["med"]
                # E.g. Penicillin allergy vs Amoxicillin
                if any("penicillin" in a for a in patient_allergies) and "amoxicillin" in med["generic"].lower():
                    warnings.append(f"🚨 CRITICAL ALLERGY: {self.selected_patient['name']} is ALLERGIC to Penicillin! ({med['name']} contains Amoxicillin)")
                if any("aspirin" in a for a in patient_allergies) and ("nsaid" in med["generic"].lower() or "aspirin" in med["generic"].lower()):
                    warnings.append(f"🚨 CRITICAL ALLERGY: Patient allergic to NSAIDs/Aspirin! ({med['name']})")
                    
        # 2. Check Drug-Drug Interactions among items in Cart
        cart_med_names = [item["med"]["name"] for item in self.cart]
        for item in self.cart:
            for inter in item["med"].get("interactions", []):
                for other in cart_med_names:
                    if inter.lower() in other.lower():
                        warnings.append(f"⚠️ DRUG INTERACTION: {item['med']['name']} interacts with {other}!")
                        
        if warnings:
            self.cdss_banner.configure(fg_color="#3B1219")  # Dark red
            self.lbl_cdss_warning.configure(
                text="\n".join(warnings),
                text_color=COLORS["danger"]
            )
        else:
            self.cdss_banner.configure(fg_color="#0F291E")  # Dark green
            self.lbl_cdss_warning.configure(
                text="🛡️ CDSS Clinical Safety: Passed. No severe contraindications found.",
                text_color=COLORS["clinical"]
            )

    def open_patient_selector(self):
        win = ctk.CTkToplevel(self)
        win.title("Select Patient Profile")
        win.geometry("500x400")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="Select Patient from EHR Registry", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl.pack(pady=(16, 8))
        
        scroll = ctk.CTkScrollableFrame(win, fg_color=COLORS["bg_base"])
        scroll.pack(fill="both", expand=True, padx=16, pady=8)
        
        for p in PATIENTS:
            card = ctk.CTkFrame(scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", pady=4, padx=4)
            
            p_text = f"👤 {p['name']} ({p['age']}y/{p['gender']})\n📞 {p['phone']} | Allergies: {', '.join(p['allergies']) or 'None'}"
            lbl_p = ctk.CTkLabel(card, text=p_text, font=FONTS["small"], justify="left")
            lbl_p.pack(side="left", padx=10, pady=8)
            
            btn_sel = ctk.CTkButton(
                card,
                text="Select",
                width=70,
                height=28,
                fg_color=COLORS["btn_primary"],
                hover_color=COLORS["btn_primary_hover"],
                command=lambda pat=p: self.set_patient(pat, win)
            )
            btn_sel.pack(side="right", padx=10)

    def set_patient(self, patient, window):
        self.selected_patient = patient
        self.lbl_patient_info.configure(
            text=f"👤 Patient: {patient['name']} | Allergies: {', '.join(patient['allergies']) or 'None'}",
            text_color=COLORS["danger"] if patient['allergies'] else COLORS["text_muted"]
        )
        self.check_cdss_safety()
        window.destroy()

    def process_payment(self, method):
        if not self.cart:
            messagebox.showwarning("Cart Empty", "Please add medicines to cart before completing payment.")
            return
            
        # If critical allergy, confirm pharmacist override
        if "CRITICAL ALLERGY" in self.lbl_cdss_warning.cget("text"):
            res = messagebox.askyesno(
                "🚨 Critical Allergy Detected",
                "A severe patient allergy alert is active for items in this bill.\n\nDo you want to override with Pharmacist Authorization PIN?"
            )
            if not res:
                return

        total_val = sum(i["med"]["mrp"] * i["qty"] for i in self.cart)
        invoice_id = "INV-2026-" + str(1000 + len(self.cart) * 12)
        
        messagebox.showinfo(
            "✅ Payment Successful & Invoice Generated",
            f"Invoice: {invoice_id}\nPayment Method: {method}\nAmount: ₹ {total_val:.2f}\nPatient: {self.selected_patient['name']}\n\nGST E-Invoice & SMS Receipt dispatched!"
        )
        
        if self.show_notification:
            self.show_notification(f"Invoice {invoice_id} generated for ₹{total_val:.2f}")
            
        self.clear_cart()
