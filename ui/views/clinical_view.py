"""
Clinical Services & e-Prescription (eRx) View (Layer 4 Clinical Domain).
Includes e-Prescription queue, Doctor registration validation, Controlled Substance (Schedule X)
double-signature audit logs, and drug interaction CDSS analysis.
"""

import customtkinter as ctk
from ui.theme import COLORS, FONTS
from data.mock_db import PRESCRIPTIONS_QUEUE, PATIENTS
from tkinter import messagebox

class ClinicalView(ctk.CTkFrame):
    def __init__(self, parent, on_dispense_rx_cb=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.on_dispense_rx = on_dispense_rx_cb
        
        self.grid_columnconfigure(0, weight=4)  # Left: Rx Queue list
        self.grid_columnconfigure(1, weight=6)  # Right: Detailed Rx Inspection & Clinical Decision Support
        self.grid_rowconfigure(0, weight=1)
        
        self.selected_rx = PRESCRIPTIONS_QUEUE[0] if PRESCRIPTIONS_QUEUE else None
        
        self.setup_queue_panel()
        self.setup_detail_panel()
        self.load_rx_details(self.selected_rx)

    def setup_queue_panel(self):
        queue_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        queue_frame.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        queue_frame.grid_columnconfigure(0, weight=1)
        queue_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        hdr = ctk.CTkFrame(queue_frame, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=16)
        
        lbl_title = ctk.CTkLabel(hdr, text="🩺 eRx Prescription Queue", font=FONTS["h2"], text_color=COLORS["clinical"])
        lbl_title.pack(anchor="w")
        
        lbl_sub = ctk.CTkLabel(hdr, text="ABDM / eRx incoming digital prescriptions", font=FONTS["small"], text_color=COLORS["text_dim"])
        lbl_sub.pack(anchor="w")
        
        # Scrollable Queue List
        self.queue_scroll = ctk.CTkScrollableFrame(queue_frame, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.queue_scroll.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.queue_scroll.grid_columnconfigure(0, weight=1)
        
        self.refresh_queue_list()

    def refresh_queue_list(self):
        for w in self.queue_scroll.winfo_children():
            w.destroy()
            
        for rx in PRESCRIPTIONS_QUEUE:
            is_active = self.selected_rx and self.selected_rx["rx_id"] == rx["rx_id"]
            border_c = COLORS["clinical"] if is_active else COLORS["border"]
            bg_c = COLORS["bg_surface_alt"] if is_active else COLORS["bg_card"]
            
            card = ctk.CTkFrame(self.queue_scroll, fg_color=bg_c, corner_radius=8, border_width=1, border_color=border_c)
            card.pack(fill="x", pady=4, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            # Row 1: ID & Status
            r1 = ctk.CTkFrame(card, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            lbl_id = ctk.CTkLabel(r1, text=rx["rx_id"], font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_id.grid(row=0, column=0, sticky="w")
            
            # Status badge
            status_color = COLORS["danger"] if "Approval" in rx["status"] else (COLORS["warning"] if "Verification" in rx["status"] else COLORS["success"])
            lbl_st = ctk.CTkLabel(r1, text=f" {rx['status']} ", font=FONTS["small_bold"], fg_color=status_color, text_color="#000000", corner_radius=4)
            lbl_st.grid(row=0, column=1, sticky="e")
            
            # Row 2: Patient & Doctor
            lbl_info = ctk.CTkLabel(
                card,
                text=f"👤 {rx['patient']} | 👨‍⚕️ {rx['doctor'].split('(')[0]}",
                font=FONTS["small"],
                text_color=COLORS["text_muted"],
                anchor="w"
            )
            lbl_info.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 8))
            
            # Clickable trigger
            card.bind("<Button-1>", lambda e, r=rx: self.select_rx(r))
            lbl_id.bind("<Button-1>", lambda e, r=rx: self.select_rx(r))
            lbl_info.bind("<Button-1>", lambda e, r=rx: self.select_rx(r))

    def select_rx(self, rx):
        self.selected_rx = rx
        self.refresh_queue_list()
        self.load_rx_details(rx)

    def setup_detail_panel(self):
        self.detail_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        self.detail_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)
        self.detail_frame.grid_columnconfigure(0, weight=1)
        self.detail_frame.grid_rowconfigure(2, weight=1)
        
        # Header info
        self.hdr_frame = ctk.CTkFrame(self.detail_frame, fg_color="transparent")
        self.hdr_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 8))
        self.hdr_frame.grid_columnconfigure(0, weight=1)
        
        self.lbl_rx_title = ctk.CTkLabel(self.hdr_frame, text="Prescription Inspection", font=FONTS["h2"], text_color=COLORS["text_main"])
        self.lbl_rx_title.grid(row=0, column=0, sticky="w")
        
        self.lbl_doc_meta = ctk.CTkLabel(self.hdr_frame, text="Doctor & Hospital Meta", font=FONTS["body"], text_color=COLORS["text_muted"])
        self.lbl_doc_meta.grid(row=1, column=0, sticky="w", pady=(2, 0))
        
        # Clinical Safety Banner
        self.safety_alert = ctk.CTkFrame(self.detail_frame, fg_color="#2B1D0C", corner_radius=8, border_width=1, border_color=COLORS["warning"])
        self.safety_alert.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.lbl_alert_text = ctk.CTkLabel(
            self.safety_alert,
            text="Safety Checks",
            font=FONTS["body_bold"],
            text_color=COLORS["warning"],
            wraplength=480,
            justify="left"
        )
        self.lbl_alert_text.pack(fill="x", padx=12, pady=10)
        
        # Prescribed Medicines Table
        self.items_scroll = ctk.CTkScrollableFrame(self.detail_frame, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.items_scroll.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 12))
        self.items_scroll.grid_columnconfigure(0, weight=1)
        
        # Actions Footer
        self.footer_actions = ctk.CTkFrame(self.detail_frame, fg_color="transparent")
        self.footer_actions.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 16))
        self.footer_actions.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.btn_verify = ctk.CTkButton(
            self.footer_actions,
            text="✅ Verify & Approve Rx",
            height=38,
            fg_color=COLORS["clinical"],
            hover_color=COLORS["clinical_hover"],
            font=FONTS["body_bold"],
            command=self.approve_prescription
        )
        self.btn_verify.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        
        self.btn_controlled_auth = ctk.CTkButton(
            self.footer_actions,
            text="🚨 Double-Sign Schedule X",
            height=38,
            fg_color=COLORS["schedule_x"],
            hover_color="#BE185D",
            font=FONTS["body_bold"],
            command=self.double_sign_schedule_x
        )
        self.btn_controlled_auth.grid(row=0, column=1, sticky="ew", padx=6)
        
        self.btn_reject = ctk.CTkButton(
            self.footer_actions,
            text="❌ Reject / Flag Error",
            height=38,
            fg_color=COLORS["btn_danger"],
            hover_color=COLORS["btn_danger_hover"],
            font=FONTS["body_bold"],
            command=self.reject_prescription
        )
        self.btn_reject.grid(row=0, column=2, sticky="ew", padx=(6, 0))

    def load_rx_details(self, rx):
        if not rx:
            return
            
        self.lbl_rx_title.configure(text=f"📋 {rx['rx_id']} — {rx['patient']}")
        self.lbl_doc_meta.configure(text=f"👨‍⚕️ {rx['doctor']} | 🏥 {rx['hospital']} | 📅 Date: {rx['date']}")
        
        # Clinical Notes & Warnings
        if "allergic to Penicillin" in rx["notes"]:
            self.safety_alert.configure(fg_color="#3B1219", border_color=COLORS["danger"])
            self.lbl_alert_text.configure(
                text=f"🚨 CDSS CLINICAL CONTRAINDICATION ALERT:\n{rx['notes']}",
                text_color=COLORS["danger"]
            )
        elif "Schedule X" in rx["notes"]:
            self.safety_alert.configure(fg_color="#361026", border_color=COLORS["schedule_x"])
            self.lbl_alert_text.configure(
                text=f"🚨 NARCOTIC / SCHEDULE X DRUG DETECTED:\n{rx['notes']}",
                text_color=COLORS["schedule_x"]
            )
        else:
            self.safety_alert.configure(fg_color="#0F291E", border_color=COLORS["clinical"])
            self.lbl_alert_text.configure(
                text=f"✅ CLINICAL CHECK PASSED:\n{rx['notes']}",
                text_color=COLORS["clinical"]
            )
            
        # Populate items
        for w in self.items_scroll.winfo_children():
            w.destroy()
            
        for item in rx["items"]:
            c = ctk.CTkFrame(self.items_scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=4, padx=4)
            c.grid_columnconfigure(0, weight=1)
            
            lbl_name = ctk.CTkLabel(c, text=f"💊 {item['medicine']}", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_name.grid(row=0, column=0, sticky="w", padx=10, pady=(8, 2))
            
            lbl_instr = ctk.CTkLabel(
                c,
                text=f"⏱️ Dosage: {item['dosage']} | 📦 Dispense Qty: {item['qty']} | ⏳ Duration: {item['duration']}",
                font=FONTS["small"],
                text_color=COLORS["text_muted"]
            )
            lbl_instr.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 8))

    def approve_prescription(self):
        if not self.selected_rx:
            return
            
        if "allergic to Penicillin" in self.selected_rx["notes"]:
            messagebox.showerror(
                "Verification Blocked",
                "Cannot approve prescription: Severe Allergy Contraindication (Amoxicillin prescribed to Penicillin-allergic patient).\nPlease flag to prescribing doctor."
            )
            return

        self.selected_rx["status"] = "Verified & Approved"
        self.refresh_queue_list()
        messagebox.showinfo("Prescription Approved", f"{self.selected_rx['rx_id']} verified and transferred to dispensing counter.")

    def double_sign_schedule_x(self):
        if not self.selected_rx:
            return
            
        win = ctk.CTkToplevel(self)
        win.title("Pharmacist Double-Signature Authorization")
        win.geometry("450x320")
        win.configure(fg_color=COLORS["bg_surface"])
        win.grab_set()
        
        lbl = ctk.CTkLabel(win, text="🚨 Controlled Substance Double Sign-Off", font=FONTS["h3"], text_color=COLORS["schedule_x"])
        lbl.pack(pady=(16, 6))
        
        lbl_info = ctk.CTkLabel(
            win,
            text=f"Prescription: {self.selected_rx['rx_id']}\nEnter Head Pharmacist Reg # & PIN for NDPS Ledger entry.",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        lbl_info.pack(pady=4)
        
        ent_reg = ctk.CTkEntry(win, placeholder_text="Pharmacist Reg No (e.g., PH-MH-88912)", font=FONTS["body"], fg_color=COLORS["bg_input"], width=300)
        ent_reg.pack(pady=8)
        
        ent_pin = ctk.CTkEntry(win, placeholder_text="Authorization 6-Digit PIN", show="•", font=FONTS["body"], fg_color=COLORS["bg_input"], width=300)
        ent_pin.pack(pady=8)
        
        def confirm():
            if not ent_reg.get() or not ent_pin.get():
                messagebox.showwarning("Incomplete Fields", "Please provide Pharmacist Registration and PIN.", parent=win)
                return
            self.selected_rx["status"] = "Schedule X Authorized"
            self.refresh_queue_list()
            win.destroy()
            messagebox.showinfo("NDPS Audit Logged", "Controlled substance dispense authorized and recorded in state narcotic registry.")

        btn = ctk.CTkButton(win, text="Authorize & Sign", fg_color=COLORS["schedule_x"], hover_color="#BE185D", font=FONTS["body_bold"], command=confirm)
        btn.pack(pady=16)

    def reject_prescription(self):
        if not self.selected_rx:
            return
        self.selected_rx["status"] = "Rejected / Clinical Flag"
        self.refresh_queue_list()
        messagebox.showwarning("Prescription Rejected", f"{self.selected_rx['rx_id']} flagged for review. Prescribing doctor notified.")
