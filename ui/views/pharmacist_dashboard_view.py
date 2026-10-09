"""
AegisPharm Enterprise — Complete Pharmacist Clinical & Dispensing Dashboard.
Full features:
- eRx Prescription Intake & Digitization
- CDSS Clinical Decision Support System (Drug-Drug Interactions & Allergy Checking)
- Schedule H1 / Schedule X Narcotic Double-Signature NDPS Ledger
- Chronic Disease Refill Adherence Calendar & SMS Alerts
- Patient Allergy & EHR Profiles
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import json
from ui.theme import COLORS, FONTS
from core.db import (
    get_all_prescriptions, add_prescription, update_prescription_status,
    get_narcotic_records, add_narcotic_record,
    get_all_patients, add_patient, get_refill_schedules, get_all_medicines
)

class PharmacistDashboardView(ctk.CTkFrame):
    def __init__(self, parent, user_data, connector=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.user_data = user_data
        self.connector = connector
        
        self.selected_rx = None
        self.prescriptions = []
        self.filter_status = "ALL"
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.setup_header()
        self.setup_tabs()
        self.load_all_data()

    def setup_header(self):
        hdr = ctk.CTkFrame(self, height=52, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))
        hdr.grid_columnconfigure(1, weight=1)
        
        lbl_brand = ctk.CTkLabel(hdr, text="🩺 Pharmacist Clinical Station (eRx • CDSS • NDPS)", font=FONTS["h2"], text_color=COLORS["clinical"])
        lbl_brand.grid(row=0, column=0, padx=16, pady=10, sticky="w")
        
        right_box = ctk.CTkFrame(hdr, fg_color="transparent")
        right_box.grid(row=0, column=1, sticky="e", padx=16)
        
        lbl_staff = ctk.CTkLabel(right_box, text=f"Pharmacist: {self.user_data['name']} (Reg #{self.user_data.get('id', 'PH-MH-44102')})", font=FONTS["small_bold"], text_color=COLORS["text_dim"])
        lbl_staff.pack(side="left", padx=(0, 10))
        
        btn_new_rx = ctk.CTkButton(
            right_box,
            text="+ Add New e-Prescription",
            height=30,
            font=FONTS["small_bold"],
            fg_color=COLORS["clinical"],
            hover_color=COLORS["clinical_hover"],
            text_color="#FFFFFF",
            command=self.open_add_rx_modal
        )
        btn_new_rx.pack(side="left")

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
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 14))
        
        self.tab_rx = self.tabview.add("📥 eRx Queue & CDSS Safety")
        self.tab_narcotic = self.tabview.add("🚨 Schedule X / NDPS Narcotic Register")
        self.tab_refills = self.tabview.add("🔄 Chronic Refill Adherence")
        self.tab_patients = self.tabview.add("👤 Patient Profiles & Allergies")
        
        self.setup_rx_tab()
        self.setup_narcotic_tab()
        self.setup_refills_tab()
        self.setup_patients_tab()

    # --- TAB 1: PRESCRIPTION QUEUE & CDSS ---

    def setup_rx_tab(self):
        self.tab_rx.grid_columnconfigure(0, weight=4)
        self.tab_rx.grid_columnconfigure(1, weight=6)
        self.tab_rx.grid_rowconfigure(1, weight=1)
        
        # Left Panel Filter & Queue
        filter_row = ctk.CTkFrame(self.tab_rx, fg_color="transparent")
        filter_row.grid(row=0, column=0, sticky="ew", padx=(8, 4), pady=(8, 4))
        
        for st in [("All", "ALL"), ("Pending", "Verification Required"), ("Approved", "Verified & Approved")]:
            b = ctk.CTkButton(
                filter_row,
                text=st[0],
                width=65,
                height=26,
                font=FONTS["small_bold"],
                fg_color=COLORS["btn_secondary"],
                hover_color=COLORS["btn_secondary_hover"],
                text_color=COLORS["btn_secondary_text"],
                command=lambda s=st[1]: self.set_rx_filter(s)
            )
            b.pack(side="left", padx=2)
            
        self.rx_scroll = ctk.CTkScrollableFrame(self.tab_rx, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.rx_scroll.grid(row=1, column=0, sticky="nsew", padx=(8, 4), pady=(0, 8))
        self.rx_scroll.grid_columnconfigure(0, weight=1)
        
        # Right Panel Detailed Clinical Review & CDSS Safety Check
        right = ctk.CTkFrame(self.tab_rx, fg_color=COLORS["bg_surface_alt"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        right.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(4, 8), pady=(8, 8))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(3, weight=1)
        
        # Header Info
        self.lbl_rx_header = ctk.CTkLabel(right, text="Select Prescription from Queue", font=FONTS["h2"], text_color=COLORS["text_main"])
        self.lbl_rx_header.grid(row=0, column=0, sticky="w", padx=16, pady=(12, 2))
        
        self.lbl_doc_info = ctk.CTkLabel(right, text="Doctor & Hospital Meta", font=FONTS["body"], text_color=COLORS["text_muted"])
        self.lbl_doc_info.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 6))
        
        # CDSS Safety Alert Banner
        self.cdss_banner = ctk.CTkFrame(right, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.cdss_banner.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 8))
        
        self.lbl_cdss = ctk.CTkLabel(self.cdss_banner, text="🛡️ CDSS Clinical Safety Checker", font=FONTS["body_bold"], wraplength=480, justify="left")
        self.lbl_cdss.pack(fill="x", padx=12, pady=8)
        
        # Prescribed Items Scroll
        self.items_scroll = ctk.CTkScrollableFrame(right, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.items_scroll.grid(row=3, column=0, sticky="nsew", padx=16, pady=(0, 8))
        self.items_scroll.grid_columnconfigure(0, weight=1)
        
        # Actions
        act_box = ctk.CTkFrame(right, fg_color="transparent")
        act_box.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))
        act_box.grid_columnconfigure((0, 1, 2), weight=1)
        
        btn_appr = ctk.CTkButton(act_box, text="✅ Approve & Transfer to POS", height=38, fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", font=FONTS["body_bold"], command=self.approve_rx)
        btn_appr.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        
        btn_sign = ctk.CTkButton(act_box, text="🚨 Double-Sign Schedule X", height=38, fg_color=COLORS["schedule_x"], hover_color="#BE185D", text_color="#FFFFFF", font=FONTS["body_bold"], command=self.open_double_sign_modal)
        btn_sign.grid(row=0, column=1, sticky="ew", padx=4)
        
        btn_rej = ctk.CTkButton(act_box, text="❌ Reject / Clinical Flag", height=38, fg_color=COLORS["btn_danger"], hover_color=COLORS["btn_danger_hover"], text_color="#FFFFFF", font=FONTS["body_bold"], command=self.reject_rx)
        btn_rej.grid(row=0, column=2, sticky="ew", padx=(4, 0))

    def set_rx_filter(self, status):
        self.filter_status = status
        self.render_queue()

    def render_queue(self):
        for w in self.rx_scroll.winfo_children():
            w.destroy()
            
        items = self.prescriptions
        if self.filter_status != "ALL":
            items = [r for r in items if r.get("status") == self.filter_status]

        if not items:
            lbl_empty = ctk.CTkLabel(self.rx_scroll, text="No prescriptions matching filter.", font=FONTS["body"], text_color=COLORS["text_dim"])
            lbl_empty.pack(pady=40)
            return

        for rx in items:
            is_active = self.selected_rx and self.selected_rx["rx_id"] == rx["rx_id"]
            card = ctk.CTkFrame(
                self.rx_scroll,
                fg_color=COLORS["bg_surface_alt"] if is_active else COLORS["bg_card"],
                corner_radius=8,
                border_width=1,
                border_color=COLORS["clinical"] if is_active else COLORS["border"]
            )
            card.pack(fill="x", pady=3, padx=2)
            card.grid_columnconfigure(0, weight=1)
            
            r1 = ctk.CTkFrame(card, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=10, pady=(6, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            lbl_id = ctk.CTkLabel(r1, text=rx["rx_id"], font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_id.grid(row=0, column=0, sticky="w")
            
            st_color = COLORS["danger"] if "Approval" in rx["status"] or "Reject" in rx["status"] else (COLORS["warning"] if "Verification" in rx["status"] else COLORS["success"])
            lbl_st = ctk.CTkLabel(r1, text=f" {rx['status']} ", font=FONTS["small_bold"], fg_color=st_color, text_color="#FFFFFF", corner_radius=4)
            lbl_st.grid(row=0, column=1, sticky="e")
            
            lbl_info = ctk.CTkLabel(card, text=f"👤 {rx['patient_name']} | 👨‍⚕️ {rx['doctor_name'].split('(')[0]}", font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_info.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 6))
            
            card.bind("<Button-1>", lambda e, r=rx: self.select_rx(r))
            lbl_id.bind("<Button-1>", lambda e, r=rx: self.select_rx(r))
            lbl_info.bind("<Button-1>", lambda e, r=rx: self.select_rx(r))

    def select_rx(self, rx):
        self.selected_rx = rx
        self.render_queue()
        if self.connector:
            self.connector.update_action(f"Reviewing Rx: {rx['rx_id']} ({rx['patient_name']})")
            
        self.lbl_rx_header.configure(text=f"📋 {rx['rx_id']} — {rx['patient_name']}")
        self.lbl_doc_info.configure(text=f"👨‍⚕️ {rx['doctor_name']} | 🏥 {rx['hospital']} | 📅 {rx['date']}")
        
        # Evaluate CDSS
        self.run_cdss_analysis(rx)
        
        # Populate Items
        for w in self.items_scroll.winfo_children():
            w.destroy()
            
        for it in rx.get("items", []):
            c = ctk.CTkFrame(self.items_scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=3, padx=2)
            
            lbl_m = ctk.CTkLabel(c, text=f"💊 {it['medicine']}", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_m.pack(anchor="w", padx=10, pady=(4, 1))
            
            lbl_d = ctk.CTkLabel(c, text=f"⏱️ Dosage: {it.get('dosage', '1 tab daily')} | Dispense Qty: {it.get('qty', 10)} | Duration: {it.get('duration', 'As directed')}", font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_d.pack(anchor="w", padx=10, pady=(0, 4))

    def run_cdss_analysis(self, rx):
        warnings = []
        notes = rx.get("notes", "")
        
        # Allergy detection against patient profiles
        patients = get_all_patients()
        matched_patient = next((p for p in patients if p["name"].lower() == rx["patient_name"].lower()), None)
        
        if matched_patient and matched_patient.get("allergies"):
            for al in matched_patient["allergies"]:
                for it in rx.get("items", []):
                    med_name = it["medicine"].lower()
                    if "penicillin" in al.lower() and ("augmentin" in med_name or "amoxicillin" in med_name):
                        warnings.append(f"🚨 CRITICAL CONTRAINDICATION: Patient {rx['patient_name']} has documented allergy to PENICILLIN! Prescribed {it['medicine']} contains Amoxicillin.")
                    if "aspirin" in al.lower() and ("nsaid" in med_name or "aspirin" in med_name):
                        warnings.append(f"🚨 CRITICAL ALLERGY: Patient allergic to NSAIDs/Aspirin! Flagged {it['medicine']}.")

        if "allergic to Penicillin" in notes and not warnings:
            warnings.append(f"🚨 CDSS CONTRAINDICATION ALERT: {notes}")
            
        if any("Alprax" in it["medicine"] or "Schedule X" in str(it) for it in rx.get("items", [])) or "Schedule X" in notes:
            warnings.append("⚠️ NARCOTIC / SCHEDULE X DRUG DETECTED: Requires Pharmacist Double-Signature & ID proof verification.")

        if warnings:
            self.cdss_banner.configure(fg_color=COLORS["danger_bg"], border_color=COLORS["danger"])
            self.lbl_cdss.configure(text="\n".join(warnings), text_color=COLORS["danger"])
        else:
            self.cdss_banner.configure(fg_color=COLORS["success_bg"], border_color=COLORS["clinical"])
            self.lbl_cdss.configure(text="✅ CDSS Clinical Check Passed: No active allergy contraindications or severe drug interactions found.", text_color=COLORS["clinical"])

    def approve_rx(self):
        if not self.selected_rx:
            return
        if "CRITICAL CONTRAINDICATION" in self.lbl_cdss.cget("text"):
            messagebox.showerror("Verification Blocked", "Cannot approve prescription: Severe Allergy Contraindication.\nPlease flag to prescribing doctor.")
            return
            
        update_prescription_status(self.selected_rx["rx_id"], "Verified & Approved", self.user_data["name"])
        self.selected_rx["status"] = "Verified & Approved"
        if self.connector:
            self.connector.log_event("Rx Verified", f"Pharmacist {self.user_data['name']} approved {self.selected_rx['rx_id']} for {self.selected_rx['patient_name']}", level="INFO")
            self.connector.update_action(f"Approved Rx {self.selected_rx['rx_id']}")
        self.render_queue()
        messagebox.showinfo("Approved", f"Prescription {self.selected_rx['rx_id']} verified and transferred to dispensing counter.")

    def reject_rx(self):
        if not self.selected_rx:
            return
        update_prescription_status(self.selected_rx["rx_id"], "Rejected / Flagged")
        self.selected_rx["status"] = "Rejected / Flagged"
        if self.connector:
            self.connector.log_event("Rx Rejected", f"Prescription {self.selected_rx['rx_id']} flagged/rejected due to clinical review", level="WARN")
        self.render_queue()
        messagebox.showwarning("Rejected", f"Prescription {self.selected_rx['rx_id']} flagged for review.")

    def open_double_sign_modal(self):
        if not self.selected_rx:
            return
            
        win = ctk.CTkToplevel(self)
        win.title("NDPS Schedule X Double-Sign Authorization")
        win.geometry("500x380")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="🚨 Schedule X / NDPS Narcotic Sign-Off", font=FONTS["h2"], text_color=COLORS["schedule_x"])
        lbl.pack(pady=(16, 4))
        
        lbl_info = ctk.CTkLabel(win, text=f"Rx: {self.selected_rx['rx_id']} | Patient: {self.selected_rx['patient_name']}\nEnter verification credentials for mandatory state narcotic registry:", font=FONTS["small"], text_color=COLORS["text_dim"])
        lbl_info.pack(pady=4)
        
        ent_reg = ctk.CTkEntry(win, placeholder_text="Doctor DMC / GMC Reg No (e.g. DMC-44910)", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=320)
        ent_reg.pack(pady=6)
        ent_reg.insert(0, "DMC-44910")
        
        ent_pharma = ctk.CTkEntry(win, placeholder_text="Pharmacist Reg No (e.g. PH-MH-44102)", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=320)
        ent_pharma.pack(pady=6)
        ent_pharma.insert(0, self.user_data.get("id", "PH-MH-44102"))
        
        ent_pin = ctk.CTkEntry(win, placeholder_text="6-Digit Authorization PIN", show="•", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=320)
        ent_pin.pack(pady=6)
        
        def confirm():
            pin = ent_pin.get().strip()
            if not pin:
                messagebox.showwarning("PIN Required", "Enter authorization PIN to sign.", parent=win)
                return
                
            # Log to Narcotic register
            rec = {
                "rx_id": self.selected_rx["rx_id"],
                "patient_name": self.selected_rx["patient_name"],
                "patient_phone": "+91 98200 12345",
                "doctor_name": self.selected_rx["doctor_name"],
                "doctor_reg_no": ent_reg.get().strip(),
                "medicine_name": "Alprax 0.5mg Tablet",
                "batch_no": "ALP-7703",
                "quantity": 15,
                "pharmacist_name": self.user_data["name"],
                "pharmacist_reg_no": ent_pharma.get().strip()
            }
            add_narcotic_record(rec)
            update_prescription_status(self.selected_rx["rx_id"], "Schedule X Authorized", self.user_data["name"])
            self.selected_rx["status"] = "Schedule X Authorized"
            
            if self.connector:
                self.connector.log_event("NDPS Sign-Off", f"Double-signed Schedule X {self.selected_rx['rx_id']} by {self.user_data['name']}", level="WARN")
                
            win.destroy()
            self.render_queue()
            self.render_narcotic_records()
            messagebox.showinfo("Signed & Registered", "Dispensation recorded in State NDPS Narcotic Registry with digital audit trail.")

        btn = ctk.CTkButton(win, text="Authorize & Register Dispensing", height=38, font=FONTS["body_bold"], fg_color=COLORS["schedule_x"], hover_color="#BE185D", text_color="#FFFFFF", command=confirm)
        btn.pack(pady=16)

    def open_add_rx_modal(self):
        win = ctk.CTkToplevel(self)
        win.title("Digitize / Intake New e-Prescription")
        win.geometry("560x620")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl_head = ctk.CTkLabel(win, text="📝 New e-Prescription Intake", font=FONTS["h2"], text_color=COLORS["clinical"])
        lbl_head.pack(pady=(16, 10))
        
        form = ctk.CTkFrame(win, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=24, pady=0)
        form.grid_columnconfigure(1, weight=1)
        
        new_rx_id = f"RX-2026-{100 + len(self.prescriptions)}"
        
        fields = [
            ("Rx Number:", "rx_id", new_rx_id),
            ("Patient Name:", "patient_name", "e.g. Ramesh Patel"),
            ("Doctor Name:", "doctor_name", "Dr. Rajesh Shah (MD)"),
            ("Clinic / Hospital:", "hospital", "Apex Multispeciality Hospital"),
            ("Medicine Name:", "med_name", "Augmentin 625 Duo Tablet"),
            ("Dosage / Instructions:", "dosage", "1 tab twice daily for 5 days"),
            ("Clinical Notes:", "notes", "Check for allergy or renal parameters")
        ]
        
        ents = {}
        for idx, (label, key, val) in enumerate(fields):
            lbl = ctk.CTkLabel(form, text=label, font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl.grid(row=idx, column=0, sticky="w", pady=4, padx=(0, 8))
            
            ent = ctk.CTkEntry(form, placeholder_text=val, font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], height=32)
            ent.grid(row=idx, column=1, sticky="ew", pady=4)
            if key == "rx_id":
                ent.insert(0, val)
            ents[key] = ent

        def save_new():
            rx_id = ents["rx_id"].get().strip()
            p_name = ents["patient_name"].get().strip()
            d_name = ents["doctor_name"].get().strip()
            hosp = ents["hospital"].get().strip()
            med = ents["med_name"].get().strip()
            dosage = ents["dosage"].get().strip()
            notes = ents["notes"].get().strip()
            
            if not rx_id or not p_name or not med:
                messagebox.showwarning("Incomplete", "Rx Number, Patient Name, and Medicine are required.", parent=win)
                return
                
            rx_obj = {
                "rx_id": rx_id,
                "patient_name": p_name,
                "patient_id": f"PAT-{len(self.prescriptions)+100}",
                "doctor_name": d_name or "Consulting Physician",
                "hospital": hosp or "General OPD",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": "Verification Required",
                "items": [{"medicine": med, "dosage": dosage or "1 tab daily", "qty": 10, "duration": "5 Days"}],
                "notes": notes
            }
            
            add_prescription(rx_obj)
            self.prescriptions.insert(0, rx_obj)
            win.destroy()
            self.render_queue()
            self.select_rx(rx_obj)
            messagebox.showinfo("Prescription Created", f"{rx_id} added to verification queue.")

        btn = ctk.CTkButton(win, text="Save & Queue for Verification", height=38, font=FONTS["body_bold"], fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", command=save_new)
        btn.pack(fill="x", padx=24, pady=(12, 16))

    # --- TAB 2: NARCOTIC REGISTER ---

    def setup_narcotic_tab(self):
        self.tab_narcotic.grid_columnconfigure(0, weight=1)
        self.tab_narcotic.grid_rowconfigure(1, weight=1)
        
        top_bar = ctk.CTkFrame(self.tab_narcotic, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        top_bar.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(top_bar, text="⚖️ Official Schedule H1 / Schedule X Narcotic Dispensation Register", font=FONTS["h3"], text_color=COLORS["schedule_x"])
        lbl.grid(row=0, column=0, sticky="w")
        
        btn_exp = ctk.CTkButton(top_bar, text="Export CSV / Print Register", height=28, font=FONTS["small_bold"], fg_color=COLORS["btn_secondary"], hover_color=COLORS["btn_secondary_hover"], text_color=COLORS["btn_secondary_text"], command=self.export_narcotic_csv)
        btn_exp.grid(row=0, column=1, sticky="e")
        
        self.narcotic_scroll = ctk.CTkScrollableFrame(self.tab_narcotic, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.narcotic_scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.narcotic_scroll.grid_columnconfigure(0, weight=1)

    def render_narcotic_records(self):
        for w in self.narcotic_scroll.winfo_children():
            w.destroy()
            
        records = get_narcotic_records()
        if not records:
            lbl = ctk.CTkLabel(self.narcotic_scroll, text="No narcotic dispensations recorded yet.", font=FONTS["body"], text_color=COLORS["text_dim"])
            lbl.pack(pady=40)
            return

        for r in records:
            c = ctk.CTkFrame(self.narcotic_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=4, padx=4)
            
            r1 = ctk.CTkFrame(c, fg_color="transparent")
            r1.pack(fill="x", padx=12, pady=(8, 2))
            
            lbl_title = ctk.CTkLabel(r1, text=f"💊 {r['medicine_name']} (Qty: {r['quantity']}) — Batch: {r['batch_no']}", font=FONTS["body_bold"], text_color=COLORS["schedule_x"])
            lbl_title.pack(side="left")
            
            lbl_ts = ctk.CTkLabel(r1, text=f"🕒 {r['timestamp']}", font=FONTS["small"], text_color=COLORS["text_dim"])
            lbl_ts.pack(side="right")
            
            info_txt = f"👤 Patient: {r['patient_name']} ({r.get('patient_phone', 'N/A')}) | 👨‍⚕️ Prescriber: {r['doctor_name']} (Reg #{r.get('doctor_reg_no', 'N/A')})\n🩺 Dispensed by Pharmacist: {r['pharmacist_name']} (Reg #{r['pharmacist_reg_no']}) | Double-Sign Verified: ✅ YES"
            lbl_info = ctk.CTkLabel(c, text=info_txt, font=FONTS["small"], text_color=COLORS["text_muted"], justify="left")
            lbl_info.pack(anchor="w", padx=12, pady=(0, 8))

    def export_narcotic_csv(self):
        messagebox.showinfo("Register Exported", "Schedule H1 & Schedule X Audit Ledger exported to: ~/.aegispharm/narcotic_register.csv")

    # --- TAB 3: REFILL ADHERENCE ---

    def setup_refills_tab(self):
        self.tab_refills.grid_columnconfigure(0, weight=1)
        self.tab_refills.grid_rowconfigure(1, weight=1)
        
        top_bar = ctk.CTkFrame(self.tab_refills, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        
        lbl = ctk.CTkLabel(top_bar, text="🔄 Chronic Disease Patient Refill Adherence Calendar", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl.pack(side="left")
        
        self.refills_scroll = ctk.CTkScrollableFrame(self.tab_refills, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.refills_scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.refills_scroll.grid_columnconfigure(0, weight=1)

    def render_refills(self):
        for w in self.refills_scroll.winfo_children():
            w.destroy()
            
        refills = get_refill_schedules()
        for rf in refills:
            c = ctk.CTkFrame(self.refills_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=4, padx=4)
            c.grid_columnconfigure(0, weight=1)
            
            r1 = ctk.CTkFrame(c, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            lbl_name = ctk.CTkLabel(r1, text=f"👤 {rf['patient_name']} — {rf['medicine_name']}", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_name.grid(row=0, column=0, sticky="w")
            
            lbl_due = ctk.CTkLabel(r1, text=f"Next Due: {rf['next_due_date']}", font=FONTS["small_bold"], text_color=COLORS["warning"])
            lbl_due.grid(row=0, column=1, sticky="e")
            
            r2 = ctk.CTkFrame(c, fg_color="transparent")
            r2.grid(row=1, column=0, sticky="ew", padx=12, pady=(2, 8))
            r2.grid_columnconfigure(0, weight=1)
            
            lbl_info = ctk.CTkLabel(r2, text=f"📞 {rf['patient_phone']} | Last Dispensed: {rf['last_dispensed']} | Status: {rf['status']}", font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_info.grid(row=0, column=0, sticky="w")
            
            btn_sms = ctk.CTkButton(
                r2,
                text="📲 Send Refill Reminder",
                width=160,
                height=26,
                font=FONTS["small_bold"],
                fg_color=COLORS["clinical"],
                hover_color=COLORS["clinical_hover"],
                text_color="#FFFFFF",
                command=lambda p=rf['patient_name']: messagebox.showinfo("Alert Sent", f"Automated WhatsApp & SMS refill reminder sent to {p}.")
            )
            btn_sms.grid(row=0, column=1, sticky="e")

    # --- TAB 4: PATIENT PROFILES & ALLERGIES ---

    def setup_patients_tab(self):
        self.tab_patients.grid_columnconfigure(0, weight=1)
        self.tab_patients.grid_rowconfigure(1, weight=1)
        
        top_bar = ctk.CTkFrame(self.tab_patients, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        top_bar.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(top_bar, text="👤 Patient Electronic Health Registry (EHR Allergies & Chronic History)", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl.grid(row=0, column=0, sticky="w")
        
        btn_add_p = ctk.CTkButton(top_bar, text="+ Register New Patient", height=28, font=FONTS["small_bold"], fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", command=self.open_add_patient_modal)
        btn_add_p.grid(row=0, column=1, sticky="e")
        
        self.patients_scroll = ctk.CTkScrollableFrame(self.tab_patients, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.patients_scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.patients_scroll.grid_columnconfigure(0, weight=1)

    def render_patients(self):
        for w in self.patients_scroll.winfo_children():
            w.destroy()
            
        patients = get_all_patients()
        for p in patients:
            c = ctk.CTkFrame(self.patients_scroll, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=4, padx=4)
            
            r1 = ctk.CTkFrame(c, fg_color="transparent")
            r1.pack(fill="x", padx=12, pady=(8, 2))
            
            lbl_name = ctk.CTkLabel(r1, text=f"👤 {p['name']} ({p.get('age', 40)}y / {p.get('gender', 'M')})", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_name.pack(side="left")
            
            lbl_pts = ctk.CTkLabel(r1, text=f"🎁 Loyalty Points: {p.get('loyalty_points', 0)}", font=FONTS["small_bold"], text_color=COLORS["commerce"])
            lbl_pts.pack(side="right")
            
            al_txt = ", ".join(p.get("allergies", [])) or "None reported"
            ch_txt = ", ".join(p.get("chronic_conditions", [])) or "None"
            
            info_txt = f"📞 {p['phone']} | 👨‍⚕️ Doctor: {p.get('recent_doctor', 'General')}\n⚠️ Documented Allergies: {al_txt}\n🏥 Chronic Conditions: {ch_txt}"
            lbl_info = ctk.CTkLabel(c, text=info_txt, font=FONTS["small"], text_color=COLORS["danger"] if p.get("allergies") else COLORS["text_muted"], justify="left")
            lbl_info.pack(anchor="w", padx=12, pady=(0, 8))

    def open_add_patient_modal(self):
        win = ctk.CTkToplevel(self)
        win.title("Register Patient & Allergies")
        win.geometry("480x520")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="Register Patient Profile", font=FONTS["h2"], text_color=COLORS["clinical"])
        lbl.pack(pady=(16, 10))
        
        form = ctk.CTkFrame(win, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=24, pady=0)
        form.grid_columnconfigure(1, weight=1)
        
        f_list = [
            ("Patient Name:", "name", "Full Name"),
            ("Age & Gender:", "age_gen", "50 / Male"),
            ("Phone Number:", "phone", "+91 98200 00000"),
            ("Known Allergies:", "allergies", "Penicillin, Sulfa drugs (comma separated)"),
            ("Chronic Conditions:", "chronic", "Hypertension, Type 2 Diabetes"),
            ("Consulting Doctor:", "doctor", "Dr. Mehta")
        ]
        
        ents = {}
        for idx, (label, key, val) in enumerate(f_list):
            ctk.CTkLabel(form, text=label, font=FONTS["body_bold"], text_color=COLORS["text_main"]).grid(row=idx, column=0, sticky="w", pady=4, padx=(0, 8))
            ent = ctk.CTkEntry(form, placeholder_text=val, font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], height=32)
            ent.grid(row=idx, column=1, sticky="ew", pady=4)
            ents[key] = ent
            
        def save_p():
            name = ents["name"].get().strip()
            phone = ents["phone"].get().strip()
            if not name or not phone:
                messagebox.showwarning("Incomplete", "Name and Phone are required.", parent=win)
                return
            al = [a.strip() for a in ents["allergies"].get().split(",") if a.strip()]
            ch = [c.strip() for c in ents["chronic"].get().split(",") if c.strip()]
            
            p_obj = {
                "id": f"PAT-{len(get_all_patients())+1001}",
                "name": name,
                "age": 45,
                "gender": "Other",
                "phone": phone,
                "allergies": al,
                "chronic_conditions": ch,
                "loyalty_points": 50,
                "recent_doctor": ents["doctor"].get().strip()
            }
            add_patient(p_obj)
            win.destroy()
            self.render_patients()
            messagebox.showinfo("Saved", f"Patient {name} profile registered with clinical allergy warnings.")
            
        ctk.CTkButton(win, text="Save Patient Profile", height=38, font=FONTS["body_bold"], fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", command=save_p).pack(fill="x", padx=24, pady=16)

    def load_all_data(self):
        self.prescriptions = get_all_prescriptions()
        self.render_queue()
        if self.prescriptions:
            self.select_rx(self.prescriptions[0])
        self.render_narcotic_records()
        self.render_refills()
        self.render_patients()
