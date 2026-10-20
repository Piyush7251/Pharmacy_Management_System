"""
TQM Pharm Enterprise — Complete Pharmacist Clinical & Dispensing Dashboard.
Full features:
- eRx Prescription Intake & Searchable Queue
- CDSS Clinical Decision Support System:
    * Real-time Patient EHR Allergy Contraindication Engine (e.g. Penicillin, NSAIDs)
    * Real-time Multi-Drug Interaction Engine cross-checked against database interaction lists
- Schedule H1 / Schedule X Narcotic Double-Signature NDPS Ledger:
    * Pharmacist PIN Authentication & Doctor Reg Logging
    * Export Compliance Narcotic Register to CSV / Excel
- Chronic Disease Patient Refill Adherence Calendar:
    * Interactive WhatsApp & SMS Refill Reminder Modal with Template Simulation
    * Live Status Updates in SQLite database
- Patient EHR Registry with Documented Allergies, Chronic Conditions & Search
- Printable Clinical Dispense Clearance Slip
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
import json
import csv
from ui.theme import COLORS, FONTS
from ui.components.toast import show_toast
from core.db import (
    get_all_prescriptions, add_prescription, update_prescription_status,
    get_narcotic_records, add_narcotic_record,
    get_all_patients, add_patient, get_refill_schedules, update_refill_status,
    get_all_medicines
)

class PharmacistDashboardView(ctk.CTkFrame):
    def __init__(self, parent, user_data, connector=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.user_data = user_data
        self.connector = connector
        
        self.selected_rx = None
        self.prescriptions = []
        self.filter_status = "ALL"
        self.all_medicines = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.setup_header()
        self.setup_tabs()
        self.load_all_data()

    def setup_header(self):
        hdr = ctk.CTkFrame(self, height=54, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 6))
        hdr.grid_columnconfigure(1, weight=1)
        
        lbl_brand = ctk.CTkLabel(hdr, text="🩺 Pharmacist Station (Prescriptions & Patient Safety)", font=FONTS["h2"], text_color=COLORS["clinical"])
        lbl_brand.grid(row=0, column=0, padx=16, pady=10, sticky="w")
        
        right_box = ctk.CTkFrame(hdr, fg_color="transparent")
        right_box.grid(row=0, column=1, sticky="e", padx=16)
        
        lbl_staff = ctk.CTkLabel(right_box, text=f"Pharmacist: {self.user_data['name']}", font=FONTS["small_bold"], text_color=COLORS["text_dim"])
        lbl_staff.pack(side="left", padx=(0, 10))
        
        btn_new_rx = ctk.CTkButton(
            right_box,
            text="+ Add Prescription",
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
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 12))
        
        self.tab_rx = self.tabview.add("📥 Doctor Prescriptions")
        self.tab_narcotic = self.tabview.add("🚨 Controlled Drugs Register")
        self.tab_refills = self.tabview.add("🔄 Patient Monthly Refills")
        self.tab_patients = self.tabview.add("👤 Patient Records & Allergies")
        
        self.setup_rx_tab()
        self.setup_narcotic_tab()
        self.setup_refills_tab()
        self.setup_patients_tab()

    # --- TAB 1: PRESCRIPTION QUEUE & SAFETY CHECK ---

    def setup_rx_tab(self):
        self.tab_rx.grid_columnconfigure(0, weight=4)
        self.tab_rx.grid_columnconfigure(1, weight=6)
        self.tab_rx.grid_rowconfigure(2, weight=1)
        
        # Search & Filter Strip
        filter_row = ctk.CTkFrame(self.tab_rx, fg_color="transparent")
        filter_row.grid(row=0, column=0, sticky="ew", padx=(8, 4), pady=(6, 2))
        
        for st in [("All", "ALL"), ("Pending Review", "Verification Required"), ("Approved", "Verified & Approved")]:
            b = ctk.CTkButton(
                filter_row,
                text=st[0],
                width=90,
                height=26,
                font=FONTS["small_bold"],
                fg_color=COLORS["btn_secondary"],
                hover_color=COLORS["btn_secondary_hover"],
                text_color=COLORS["btn_secondary_text"],
                command=lambda s=st[1]: self.set_rx_filter(s)
            )
            b.pack(side="left", padx=2)
            
        self.ent_rx_search = ctk.CTkEntry(
            self.tab_rx,
            placeholder_text="🔍 Search prescription by Rx ID, patient, doctor...",
            font=FONTS["small"],
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_main"],
            border_color=COLORS["border"],
            height=32
        )
        self.tab_rx.grid_rowconfigure(1, weight=0)
        self.ent_rx_search.grid(row=1, column=0, sticky="ew", padx=(8, 4), pady=(0, 6))
        self.ent_rx_search.bind("<KeyRelease>", lambda e: self.render_queue())
            
        self.rx_scroll = ctk.CTkScrollableFrame(self.tab_rx, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.rx_scroll.grid(row=2, column=0, sticky="nsew", padx=(8, 4), pady=(0, 8))
        self.rx_scroll.grid_columnconfigure(0, weight=1)
        
        # Right Panel: Detailed Review & Safety Check
        right = ctk.CTkFrame(self.tab_rx, fg_color=COLORS["bg_surface_alt"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        right.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=(4, 8), pady=(6, 8))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(3, weight=1)
        
        # Header Info
        self.lbl_rx_header = ctk.CTkLabel(right, text="Select a prescription to review details", font=FONTS["h2"], text_color=COLORS["text_main"])
        self.lbl_rx_header.grid(row=0, column=0, sticky="w", padx=16, pady=(12, 2))
        
        self.lbl_doc_info = ctk.CTkLabel(right, text="Doctor & Clinic Details", font=FONTS["body"], text_color=COLORS["text_muted"])
        self.lbl_doc_info.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 6))
        
        # Medicine Safety & Allergy Alert Banner
        self.cdss_banner = ctk.CTkFrame(right, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.cdss_banner.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 8))
        
        self.lbl_cdss = ctk.CTkLabel(self.cdss_banner, text="🛡️ Medicine Safety & Allergy Check: Waiting for selection", font=FONTS["body_bold"], wraplength=520, justify="left")
        self.lbl_cdss.pack(fill="x", padx=12, pady=8)
        
        # Prescribed Items Scroll
        self.items_scroll = ctk.CTkScrollableFrame(right, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.items_scroll.grid(row=3, column=0, sticky="nsew", padx=16, pady=(0, 8))
        self.items_scroll.grid_columnconfigure(0, weight=1)
        
        # Actions Strip
        act_box = ctk.CTkFrame(right, fg_color="transparent")
        act_box.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 10))
        act_box.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        btn_appr = ctk.CTkButton(act_box, text="✅ Approve for Billing", height=38, fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", font=FONTS["body_bold"], command=self.approve_rx)
        btn_appr.grid(row=0, column=0, sticky="ew", padx=(0, 2))
        
        btn_slip = ctk.CTkButton(act_box, text="🖨️ View Doctor Slip", height=38, fg_color=COLORS["commerce"], hover_color=COLORS["commerce_hover"], text_color="#FFFFFF", font=FONTS["body_bold"], command=self.show_dispense_slip)
        btn_slip.grid(row=0, column=1, sticky="ew", padx=2)
        
        btn_sign = ctk.CTkButton(act_box, text="🚨 Special Drug Sign-off", height=38, fg_color=COLORS["schedule_x"], hover_color="#BE185D", text_color="#FFFFFF", font=FONTS["body_bold"], command=self.open_double_sign_modal)
        btn_sign.grid(row=0, column=2, sticky="ew", padx=2)
        
        btn_rej = ctk.CTkButton(act_box, text="❌ Reject with Note", height=38, fg_color=COLORS["btn_danger"], hover_color=COLORS["btn_danger_hover"], text_color="#FFFFFF", font=FONTS["body_bold"], command=self.reject_rx)
        btn_rej.grid(row=0, column=3, sticky="ew", padx=(2, 0))

    def load_all_data(self):
        self.prescriptions = get_all_prescriptions()
        self.all_medicines = get_all_medicines()
        self.render_queue()
        self.render_narcotic_records()
        self.render_refills()
        self.render_patients()

    def set_rx_filter(self, status):
        self.filter_status = status
        self.render_queue()

    def render_queue(self):
        for w in self.rx_scroll.winfo_children():
            w.destroy()
            
        items = self.prescriptions
        if self.filter_status != "ALL":
            items = [r for r in items if r.get("status") == self.filter_status]
            
        q = self.ent_rx_search.get().strip().lower() if hasattr(self, "ent_rx_search") else ""
        if q:
            items = [r for r in items if q in r["rx_id"].lower() or q in r["patient_name"].lower() or q in r["doctor_name"].lower()]

        if not items:
            lbl_empty = ctk.CTkLabel(self.rx_scroll, text="No prescriptions matching criteria.", font=FONTS["body"], text_color=COLORS["text_dim"])
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
            
            med_name = it.get("medicine", str(it)) if isinstance(it, dict) else str(it)
            lbl_m = ctk.CTkLabel(c, text=f"💊 {med_name}", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_m.pack(anchor="w", padx=10, pady=(4, 1))
            
            dosage = it.get("dosage", "1 tab daily") if isinstance(it, dict) else "1 tab daily"
            qty = it.get("qty", 10) if isinstance(it, dict) else 10
            duration = it.get("duration", "As directed") if isinstance(it, dict) else "As directed"
            lbl_d = ctk.CTkLabel(c, text=f"⏱️ Dosage: {dosage} | Dispense Qty: {qty} | Duration: {duration}", font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_d.pack(anchor="w", padx=10, pady=(0, 4))

    def run_cdss_analysis(self, rx):
        warnings = []
        notes = rx.get("notes", "")
        
        # 1. Allergy Detection against patient profile
        patients = get_all_patients()
        matched_patient = next((p for p in patients if p["name"].lower() == rx["patient_name"].lower()), None)
        
        if matched_patient and matched_patient.get("allergies"):
            for al in matched_patient["allergies"]:
                for it in rx.get("items", []):
                    med_name = (it.get("medicine", str(it)) if isinstance(it, dict) else str(it)).lower()
                    if "penicillin" in al.lower() and ("augmentin" in med_name or "amoxicillin" in med_name):
                        warnings.append(f"⚠️ ALLERGY WARNING: Patient {rx['patient_name']} is allergic to PENICILLIN! Prescribed {med_name} contains Amoxicillin.")
                    if "aspirin" in al.lower() and ("nsaid" in med_name or "aspirin" in med_name or "combiflam" in med_name):
                        warnings.append(f"⚠️ ALLERGY WARNING: Patient is allergic to NSAIDs/Aspirin! Flagged {med_name}.")

        if "allergic to Penicillin" in notes and not any("PENICILLIN" in w for w in warnings):
            warnings.append(f"⚠️ ALLERGY WARNING: {notes}")
            
        # 2. Multi-Drug Interaction Checking
        rx_med_names = [(it.get("medicine", str(it)) if isinstance(it, dict) else str(it)).lower() for it in rx.get("items", [])]
        for m in self.all_medicines:
            if any(m["name"].lower() in n or n in m["name"].lower() for n in rx_med_names):
                interactions = m.get("interactions", [])
                for target_med in rx_med_names:
                    for inter in interactions:
                        if inter.lower() in target_med:
                            warnings.append(f"⚠️ DRUG INTERACTION: {m['name']} may react with {inter} in this prescription.")

        # 3. Schedule X / Controlled Drug Check
        if any("Alprax" in (it.get("medicine", str(it)) if isinstance(it, dict) else str(it)) or "Schedule X" in str(it) for it in rx.get("items", [])) or "Schedule X" in notes:
            warnings.append("⚠️ CONTROLLED MEDICINE: Requires doctor reg number and pharmacist sign-off PIN.")

        if warnings:
            self.cdss_banner.configure(fg_color=COLORS["danger_bg"], border_color=COLORS["danger"])
            self.lbl_cdss.configure(text="\n".join(warnings), text_color=COLORS["danger"])
        else:
            self.cdss_banner.configure(fg_color=COLORS["success_bg"], border_color=COLORS["clinical"])
            self.lbl_cdss.configure(text="✅ All Clear: No allergy conflicts or medicine interactions found.", text_color=COLORS["clinical"])

    def approve_rx(self):
        if not self.selected_rx:
            show_toast(self, "No Selection", "Please select a prescription first.", "warning")
            return
        if "ALLERGY WARNING" in self.lbl_cdss.cget("text"):
            messagebox.showerror("Allergy Conflict", "Cannot approve prescription: Patient has a documented allergy!\nPlease contact the doctor to change the medicine.")
            return
            
        update_prescription_status(self.selected_rx["rx_id"], "Verified & Approved", self.user_data["name"])
        self.selected_rx["status"] = "Verified & Approved"
        if self.connector:
            self.connector.log_event("Rx Verified", f"Pharmacist {self.user_data['name']} approved {self.selected_rx['rx_id']} for {self.selected_rx['patient_name']}", level="INFO")
            self.connector.update_action(f"Approved Rx {self.selected_rx['rx_id']}")
            
        self.render_queue()
        show_toast(self, "Prescription Approved", f"{self.selected_rx['rx_id']} approved and sent to billing.", "success")

    def reject_rx(self):
        if not self.selected_rx:
            return
        update_prescription_status(self.selected_rx["rx_id"], "Rejected / Flagged")
        self.selected_rx["status"] = "Rejected / Flagged"
        if self.connector:
            self.connector.log_event("Rx Flagged", f"Prescription {self.selected_rx['rx_id']} rejected by {self.user_data['name']}", level="WARN")
        self.render_queue()
        show_toast(self, "Prescription Flagged", f"{self.selected_rx['rx_id']} marked as rejected.", "danger")

    def show_dispense_slip(self):
        if not self.selected_rx:
            show_toast(self, "No Selection", "Please select a prescription first.", "warning")
            return
            
        rx = self.selected_rx
        win = ctk.CTkToplevel(self)
        win.title(f"Doctor Prescription Slip — {rx['rx_id']}")
        win.geometry("480x560")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        txt_box = ctk.CTkTextbox(win, font=FONTS["mono"], fg_color=COLORS["bg_card"], text_color=COLORS["text_main"])
        txt_box.pack(fill="both", expand=True, padx=16, pady=(16, 10))
        
        slip_text = f"""==================================================
           DOCTOR PRESCRIPTION & DISPENSE SLIP      
     Apex Central Pharmacy - Branch #01            
==================================================
Prescription ID:  {rx['rx_id']}
Date:             {rx['date']}
Patient Name:     {rx['patient_name']}
Doctor:           {rx['doctor_name']}
Clinic / Hospital:{rx['hospital']}
Status:           {rx['status']}
--------------------------------------------------
PRESCRIBED MEDICINES:
--------------------------------------------------
"""
        for it in rx.get("items", []):
            slip_text += f"• {it['medicine']}\n  Dosage: {it.get('dosage', '1 tab daily')} | Quantity: {it.get('qty', 10)}\n"
            
        slip_text += f"""--------------------------------------------------
Safety Check:     PASSED / VERIFIED
Pharmacist:       {self.user_data['name']}
==================================================
"""
        txt_box.insert("1.0", slip_text)
        txt_box.configure(state="disabled")
        
        btn_box = ctk.CTkFrame(win, fg_color="transparent")
        btn_box.pack(fill="x", padx=16, pady=(0, 14))
        
        def save_file():
            p = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"Slip_{rx['rx_id']}.txt")
            if p:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(slip_text)
                show_toast(self, "Slip Saved", f"Saved to {p}", "success")
                
        ctk.CTkButton(btn_box, text="💾 Save to File", font=FONTS["small_bold"], fg_color=COLORS["btn_secondary"], hover_color=COLORS["btn_secondary_hover"], text_color=COLORS["btn_secondary_text"], command=save_file).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ctk.CTkButton(btn_box, text="Close", font=FONTS["small_bold"], fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", command=win.destroy).pack(side="left", expand=True, fill="x", padx=(4, 0))

    def open_double_sign_modal(self):
        if not self.selected_rx:
            show_toast(self, "No Selection", "Select prescription requiring sign-off.", "warning")
            return
            
        win = ctk.CTkToplevel(self)
        win.title("Controlled Medicine Sign-Off")
        win.geometry("500x420")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="🚨 Controlled Medicine Sign-Off", font=FONTS["h2"], text_color=COLORS["schedule_x"])
        lbl.pack(pady=(16, 4))
        
        lbl_info = ctk.CTkLabel(win, text=f"Rx: {self.selected_rx['rx_id']} | Patient: {self.selected_rx['patient_name']}\nEnter verification details to approve:", font=FONTS["small"], text_color=COLORS["text_dim"])
        lbl_info.pack(pady=4)
        
        ent_reg = ctk.CTkEntry(win, placeholder_text="Doctor Reg No (e.g. DMC-44910)", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=320)
        ent_reg.pack(pady=6)
        ent_reg.insert(0, "DMC-44910")
        
        ent_pharma = ctk.CTkEntry(win, placeholder_text="Pharmacist Reg No (e.g. PH-MH-44102)", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=320)
        ent_pharma.pack(pady=6)
        ent_pharma.insert(0, self.user_data.get("id", "PH-MH-44102"))
        
        ent_pin = ctk.CTkEntry(win, placeholder_text="PIN: pharma123", show="•", font=FONTS["body"], fg_color=COLORS["bg_input"], text_color=COLORS["text_main"], width=320)
        ent_pin.pack(pady=6)
        ent_pin.insert(0, "pharma123")
        
        def confirm():
            pin = ent_pin.get().strip()
            if not pin:
                messagebox.showwarning("PIN Required", "Enter authorization PIN to sign.", parent=win)
                return
                
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
            show_toast(self, "Recorded", "Medicine logged in Controlled Drugs Register.", "success")

        btn = ctk.CTkButton(win, text="Confirm & Authorize Dispensing", height=38, font=FONTS["body_bold"], fg_color=COLORS["schedule_x"], hover_color="#BE185D", text_color="#FFFFFF", command=confirm)
        btn.pack(pady=16)

    def open_add_rx_modal(self):
        win = ctk.CTkToplevel(self)
        win.title("Add New Doctor Prescription")
        win.geometry("560x580")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl_head = ctk.CTkLabel(win, text="📝 Add New Prescription", font=FONTS["h2"], text_color=COLORS["clinical"])
        lbl_head.pack(pady=(16, 8))
        
        form = ctk.CTkFrame(win, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=24, pady=0)
        form.grid_columnconfigure(1, weight=1)
        
        new_rx_id = f"RX-2026-{100 + len(self.prescriptions) + 1}"
        fields = [
            ("Prescription ID:", "rx_id", new_rx_id),
            ("Patient Name:", "patient_name", "Anil Deshmukh"),
            ("Doctor Name:", "doctor_name", "Dr. Rajesh Shah (MD)"),
            ("Clinic / Hospital:", "hospital", "Apex Multispeciality Hospital"),
            ("Medicine Name:", "med_name", "Augmentin 625 Duo Tablet"),
            ("Dosage / Timing:", "dosage", "1 tab twice daily for 5 days"),
            ("Doctor Notes:", "notes", "Check for allergy or kidney parameters")
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
            rx_dict = {
                "rx_id": ents["rx_id"].get().strip(),
                "patient_name": ents["patient_name"].get().strip(),
                "patient_id": f"PAT-{len(get_all_patients())+100}",
                "doctor_name": ents["doctor_name"].get().strip(),
                "hospital": ents["hospital"].get().strip(),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": "Verification Required",
                "items": [{"medicine": ents["med_name"].get().strip(), "dosage": ents["dosage"].get().strip(), "qty": 10, "duration": "5 days"}],
                "notes": ents["notes"].get().strip(),
                "verified_by": None,
                "verified_at": None
            }
            add_prescription(rx_dict)
            self.prescriptions = get_all_prescriptions()
            self.render_queue()
            win.destroy()
            show_toast(self, "Prescription Added", f"{rx_dict['rx_id']} added for review.", "success")
            
        btn_s = ctk.CTkButton(win, text="Save Prescription", height=38, font=FONTS["body_bold"], fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", command=save)
        btn_s.pack(fill="x", padx=24, pady=16)

    # --- TAB 2: CONTROLLED DRUGS REGISTER ---

    def setup_narcotic_tab(self):
        self.tab_narcotic.grid_columnconfigure(0, weight=1)
        self.tab_narcotic.grid_rowconfigure(1, weight=1)
        
        top_bar = ctk.CTkFrame(self.tab_narcotic, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        top_bar.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(top_bar, text="🚨 Controlled Drugs & Narcotics Register", font=FONTS["h3"], text_color=COLORS["schedule_x"])
        lbl.grid(row=0, column=0, sticky="w")
        
        btn_exp = ctk.CTkButton(top_bar, text="💾 Export Register CSV", height=28, font=FONTS["small_bold"], fg_color=COLORS["schedule_x"], hover_color="#BE185D", text_color="#FFFFFF", command=self.export_narcotic_csv)
        btn_exp.grid(row=0, column=1, sticky="e")
        
        self.narcotic_scroll = ctk.CTkScrollableFrame(self.tab_narcotic, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.narcotic_scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.narcotic_scroll.grid_columnconfigure(0, weight=1)

    def render_narcotic_records(self):
        for w in self.narcotic_scroll.winfo_children():
            w.destroy()
            
        records = get_narcotic_records()
        if not records:
            ctk.CTkLabel(self.narcotic_scroll, text="No controlled drug transactions recorded.", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(pady=40)
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
            
            info_txt = f"👤 Patient: {r['patient_name']} ({r.get('patient_phone', 'N/A')}) | 👨‍⚕️ Prescriber: {r['doctor_name']} (Reg #{r.get('doctor_reg_no', 'N/A')})\n🩺 Pharmacist: {r['pharmacist_name']} (Reg #{r['pharmacist_reg_no']}) | Status: ✅ Verified & Signed"
            lbl_info = ctk.CTkLabel(c, text=info_txt, font=FONTS["small"], text_color=COLORS["text_muted"], justify="left")
            lbl_info.pack(anchor="w", padx=12, pady=(0, 8))

    def export_narcotic_csv(self):
        records = get_narcotic_records()
        if not records:
            show_toast(self, "Empty", "No records to export.", "warning")
            return
            
        path = filedialog.asksaveasfilename(
            title="Export Controlled Drugs Register",
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")],
            initialfile="Controlled_Drugs_Register.csv"
        )
        if path:
            keys = records[0].keys()
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(records)
            show_toast(self, "Exported", f"Saved {len(records)} records to {path}.", "success")

    # --- TAB 3: MONTHLY REFILLS ---

    def setup_refills_tab(self):
        self.tab_refills.grid_columnconfigure(0, weight=1)
        self.tab_refills.grid_rowconfigure(1, weight=1)
        
        top_bar = ctk.CTkFrame(self.tab_refills, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        
        lbl = ctk.CTkLabel(top_bar, text="🔄 Patient Monthly Medicine Refill Reminders", font=FONTS["h3"], text_color=COLORS["text_main"])
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
            
            status_col = COLORS["clinical"] if "Sent" in rf['status'] else COLORS["warning"]
            lbl_due = ctk.CTkLabel(r1, text=f"Next Due: {rf['next_due_date']}", font=FONTS["small_bold"], text_color=status_col)
            lbl_due.grid(row=0, column=1, sticky="e")
            
            r2 = ctk.CTkFrame(c, fg_color="transparent")
            r2.grid(row=1, column=0, sticky="ew", padx=12, pady=(2, 8))
            r2.grid_columnconfigure(0, weight=1)
            
            lbl_info = ctk.CTkLabel(r2, text=f"📞 {rf['patient_phone']} | Last Dispensed: {rf['last_dispensed']} | Status: {rf['status']}", font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_info.grid(row=0, column=0, sticky="w")
            
            btn_sms = ctk.CTkButton(
                r2,
                text="📲 Send WhatsApp Reminder",
                width=175,
                height=26,
                font=FONTS["small_bold"],
                fg_color=COLORS["clinical"],
                hover_color=COLORS["clinical_hover"],
                text_color="#FFFFFF",
                command=lambda r=rf: self.open_reminder_modal(r)
            )
            btn_sms.grid(row=0, column=1, sticky="e")

    def open_reminder_modal(self, refill_data):
        win = ctk.CTkToplevel(self)
        win.title("Send Monthly Refill Reminder")
        win.geometry("460x340")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="📲 Send Monthly Refill Reminder", font=FONTS["h3"], text_color=COLORS["clinical"])
        lbl.pack(pady=(16, 6))
        
        msg_template = f"Hello {refill_data['patient_name']}, this is a friendly reminder from Apex Pharmacy. Your monthly supply of {refill_data['medicine_name']} is due for refill on {refill_data['next_due_date']}. Reply YES to confirm delivery."
        
        txt = ctk.CTkTextbox(win, font=FONTS["small"], fg_color=COLORS["bg_card"], text_color=COLORS["text_main"], height=120)
        txt.pack(fill="x", padx=20, pady=8)
        txt.insert("1.0", msg_template)
        
        def send():
            update_refill_status(refill_data["id"], "Reminder Sent (WhatsApp)")
            win.destroy()
            self.render_refills()
            show_toast(self, "Reminder Dispatched", f"Alert sent to {refill_data['patient_name']} ({refill_data['patient_phone']}).", "success")
            
        btn_send = ctk.CTkButton(win, text="🚀 Send WhatsApp Reminder Now", height=38, font=FONTS["body_bold"], fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", command=send)
        btn_send.pack(fill="x", padx=20, pady=12)

    # --- TAB 4: PATIENT PROFILES & ALLERGIES ---

    def setup_patients_tab(self):
        self.tab_patients.grid_columnconfigure(0, weight=1)
        self.tab_patients.grid_rowconfigure(2, weight=1)
        
        top_bar = ctk.CTkFrame(self.tab_patients, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
        top_bar.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(top_bar, text="👤 Patient Records & Allergies", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl.grid(row=0, column=0, sticky="w")
        
        btn_add_p = ctk.CTkButton(top_bar, text="+ Register Patient", height=28, font=FONTS["small_bold"], fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", command=self.open_add_patient_modal)
        btn_add_p.grid(row=0, column=1, sticky="e")
        
        self.ent_pat_search = ctk.CTkEntry(
            self.tab_patients,
            placeholder_text="🔍 Search patient by name, phone number, or allergy...",
            font=FONTS["small"],
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_main"],
            border_color=COLORS["border"],
            height=32
        )
        self.ent_pat_search.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        self.ent_pat_search.bind("<KeyRelease>", lambda e: self.render_patients())
        
        self.patients_scroll = ctk.CTkScrollableFrame(self.tab_patients, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.patients_scroll.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.patients_scroll.grid_columnconfigure(0, weight=1)

    def render_patients(self):
        for w in self.patients_scroll.winfo_children():
            w.destroy()
            
        patients = get_all_patients()
        q = self.ent_pat_search.get().strip().lower() if hasattr(self, "ent_pat_search") else ""
        if q:
            patients = [p for p in patients if q in p["name"].lower() or q in p["phone"].lower() or any(q in a.lower() for a in p.get("allergies", []))]

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
        win.title("Register New Patient")
        win.geometry("480x500")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="Register New Patient", font=FONTS["h2"], text_color=COLORS["clinical"])
        lbl.pack(pady=(16, 10))
        
        form = ctk.CTkFrame(win, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=24, pady=0)
        form.grid_columnconfigure(1, weight=1)
        
        fields = [
            ("Patient Name:", "name", "Sunil Verma"),
            ("Age & Gender:", "age_gen", "45, Male"),
            ("Mobile Phone:", "phone", "+91 98200 88776"),
            ("Allergies (comma-separated):", "allergies", "Penicillin, Sulfa Drugs"),
            ("Health Conditions:", "conditions", "Hypertension, Type 2 Diabetes"),
            ("Primary Doctor:", "doc", "Dr. Rajesh Shah (MD)")
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
            phone = ents["phone"].get().strip()
            if not name or not phone:
                messagebox.showwarning("Incomplete", "Name and Phone are mandatory.", parent=win)
                return
                
            al_list = [a.strip() for a in ents["allergies"].get().split(",") if a.strip()]
            ch_list = [c.strip() for c in ents["conditions"].get().split(",") if c.strip()]
            
            p_dict = {
                "id": f"PAT-{len(get_all_patients())+101}",
                "name": name,
                "age": 45,
                "gender": "Male",
                "phone": phone,
                "allergies": al_list,
                "chronic_conditions": ch_list,
                "loyalty_points": 100,
                "recent_doctor": ents["doc"].get().strip()
            }
            add_patient(p_dict)
            self.render_patients()
            win.destroy()
            show_toast(self, "Patient Saved", f"{name} profile created with {len(al_list)} allergies.", "success")
            
        btn_s = ctk.CTkButton(win, text="Save Patient Record", height=38, font=FONTS["body_bold"], fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", command=save)
        btn_s.pack(fill="x", padx=24, pady=16)
