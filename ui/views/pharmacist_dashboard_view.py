"""
AegisPharm Enterprise — Pharmacist Clinical & Dispensing Dashboard View.
Dual-theme enabled (Clean White Light Mode & Sleek Dark Mode).
"""

import customtkinter as ctk
from tkinter import messagebox
import json
from ui.theme import COLORS, FONTS
from core.db import get_connection

class PharmacistDashboardView(ctk.CTkFrame):
    def __init__(self, parent, user_data, connector=None):
        super().__init__(parent, fg_color=COLORS["bg_base"])
        self.user_data = user_data
        self.connector = connector
        
        self.selected_rx = None
        self.prescriptions = []
        
        self.grid_columnconfigure(0, weight=4)  # Left: Rx Queue
        self.grid_columnconfigure(1, weight=6)  # Right: Clinical Inspection & CDSS
        self.grid_rowconfigure(1, weight=1)
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Header Banner
        hdr = ctk.CTkFrame(self, height=52, fg_color=COLORS["bg_surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(14, 8))
        hdr.grid_columnconfigure(1, weight=1)
        
        lbl_brand = ctk.CTkLabel(hdr, text="🩺 Pharmacist Clinical Station (eRx & CDSS)", font=FONTS["h2"], text_color=COLORS["clinical"])
        lbl_brand.grid(row=0, column=0, padx=16, pady=10, sticky="w")
        
        lbl_staff = ctk.CTkLabel(hdr, text=f"Pharmacist: {self.user_data['name']} ({self.user_data['id']})", font=FONTS["small_bold"], text_color=COLORS["text_dim"])
        lbl_staff.grid(row=0, column=1, sticky="e", padx=16)
        
        # Left Panel: Prescriptions Queue
        left = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        left.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=(0, 16))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=1)
        
        l_hdr = ctk.CTkFrame(left, fg_color="transparent")
        l_hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=12)
        
        lbl_q = ctk.CTkLabel(l_hdr, text="📥 Incoming e-Prescription Queue", font=FONTS["h3"], text_color=COLORS["text_main"])
        lbl_q.pack(anchor="w")
        
        self.rx_scroll = ctk.CTkScrollableFrame(left, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.rx_scroll.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        self.rx_scroll.grid_columnconfigure(0, weight=1)
        
        # Right Panel: Detailed Inspection & CDSS Action
        right = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        right.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=(0, 16))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)
        
        # Rx Title
        self.lbl_rx_header = ctk.CTkLabel(right, text="Prescription Inspection", font=FONTS["h2"], text_color=COLORS["text_main"])
        self.lbl_rx_header.grid(row=0, column=0, sticky="w", padx=20, pady=(14, 2))
        
        self.lbl_doc_info = ctk.CTkLabel(right, text="Doctor & Clinic Details", font=FONTS["body"], text_color=COLORS["text_muted"])
        self.lbl_doc_info.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 8))
        
        # Prescription Items Table
        self.items_scroll = ctk.CTkScrollableFrame(right, fg_color=COLORS["bg_base"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        self.items_scroll.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 12))
        self.items_scroll.grid_columnconfigure(0, weight=1)
        
        # Action Buttons
        act_box = ctk.CTkFrame(right, fg_color="transparent")
        act_box.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 16))
        act_box.grid_columnconfigure((0, 1, 2), weight=1)
        
        btn_appr = ctk.CTkButton(act_box, text="✅ Approve & Push to POS", height=38, fg_color=COLORS["clinical"], hover_color=COLORS["clinical_hover"], text_color="#FFFFFF", font=FONTS["body_bold"], command=self.approve_rx)
        btn_appr.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        
        btn_sign = ctk.CTkButton(act_box, text="🚨 Double-Sign Schedule X", height=38, fg_color=COLORS["schedule_x"], hover_color="#BE185D", text_color="#FFFFFF", font=FONTS["body_bold"], command=self.double_sign_sch_x)
        btn_sign.grid(row=0, column=1, sticky="ew", padx=6)
        
        btn_rej = ctk.CTkButton(act_box, text="❌ Flag / Reject", height=38, fg_color=COLORS["btn_danger"], hover_color=COLORS["btn_danger_hover"], text_color="#FFFFFF", font=FONTS["body_bold"], command=self.reject_rx)
        btn_rej.grid(row=0, column=2, sticky="ew", padx=(6, 0))

    def load_data(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM prescriptions ORDER BY date DESC")
        rows = cur.fetchall()
        conn.close()
        
        self.prescriptions = []
        for r in rows:
            d = dict(r)
            d["items"] = json.loads(d["items"])
            self.prescriptions.append(d)
            
        self.render_queue()
        if self.prescriptions:
            self.select_rx(self.prescriptions[0])

    def render_queue(self):
        for w in self.rx_scroll.winfo_children():
            w.destroy()
            
        for rx in self.prescriptions:
            is_active = self.selected_rx and self.selected_rx["rx_id"] == rx["rx_id"]
            card = ctk.CTkFrame(
                self.rx_scroll,
                fg_color=COLORS["bg_surface_alt"] if is_active else COLORS["bg_card"],
                corner_radius=8,
                border_width=1,
                border_color=COLORS["clinical"] if is_active else COLORS["border"]
            )
            card.pack(fill="x", pady=4, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            r1 = ctk.CTkFrame(card, fg_color="transparent")
            r1.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 2))
            r1.grid_columnconfigure(0, weight=1)
            
            lbl_id = ctk.CTkLabel(r1, text=rx["rx_id"], font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_id.grid(row=0, column=0, sticky="w")
            
            st_color = COLORS["danger"] if "Approval" in rx["status"] else (COLORS["warning"] if "Verification" in rx["status"] else COLORS["success"])
            lbl_st = ctk.CTkLabel(r1, text=f" {rx['status']} ", font=FONTS["small_bold"], fg_color=st_color, text_color="#FFFFFF", corner_radius=4)
            lbl_st.grid(row=0, column=1, sticky="e")
            
            lbl_info = ctk.CTkLabel(card, text=f"👤 {rx['patient_name']} | 👨‍⚕️ {rx['doctor_name'].split('(')[0]}", font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_info.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 8))
            
            card.bind("<Button-1>", lambda e, r=rx: self.select_rx(r))
            lbl_id.bind("<Button-1>", lambda e, r=rx: self.select_rx(r))
            lbl_info.bind("<Button-1>", lambda e, r=rx: self.select_rx(r))

    def select_rx(self, rx):
        self.selected_rx = rx
        self.render_queue()
        if self.connector:
            self.connector.update_action(f"Inspecting Rx: {rx['rx_id']} ({rx['patient_name']})")
            
        self.lbl_rx_header.configure(text=f"📋 {rx['rx_id']} — {rx['patient_name']}")
        self.lbl_doc_info.configure(text=f"👨‍⚕️ {rx['doctor_name']} | 🏥 {rx['hospital']} | 📅 {rx['date']}")
        
        for w in self.items_scroll.winfo_children():
            w.destroy()
            
        for it in rx["items"]:
            c = ctk.CTkFrame(self.items_scroll, fg_color=COLORS["bg_card"], corner_radius=6, border_width=1, border_color=COLORS["border"])
            c.pack(fill="x", pady=4, padx=4)
            
            lbl_m = ctk.CTkLabel(c, text=f"💊 {it['medicine']}", font=FONTS["body_bold"], text_color=COLORS["text_main"])
            lbl_m.pack(anchor="w", padx=10, pady=(6, 2))
            
            lbl_d = ctk.CTkLabel(c, text=f"⏱️ Dosage: {it['dosage']} | Dispense Qty: {it['qty']} | Duration: {it['duration']}", font=FONTS["small"], text_color=COLORS["text_muted"])
            lbl_d.pack(anchor="w", padx=10, pady=(0, 6))

    def approve_rx(self):
        if not self.selected_rx:
            return
        if "allergic to Penicillin" in self.selected_rx.get("notes", ""):
            messagebox.showerror("Contraindication Alert", "Cannot approve: Patient is allergic to Penicillin. Flagged by CDSS.")
            return
            
        self.selected_rx["status"] = "Verified & Approved"
        if self.connector:
            self.connector.log_event("Rx Verified", f"Pharmacist approved {self.selected_rx['rx_id']} for {self.selected_rx['patient_name']}", level="INFO")
            self.connector.update_action(f"Approved Rx {self.selected_rx['rx_id']}")
        self.render_queue()
        messagebox.showinfo("Approved", f"Prescription {self.selected_rx['rx_id']} approved and pushed to POS counter.")

    def double_sign_sch_x(self):
        if not self.selected_rx:
            return
        self.selected_rx["status"] = "Schedule X Authorized"
        if self.connector:
            self.connector.log_event("Narcotic Sign-off", f"Pharmacist double-signed Schedule X Rx {self.selected_rx['rx_id']}", level="WARN")
            self.connector.update_action(f"Double-signed Schedule X {self.selected_rx['rx_id']}")
        self.render_queue()
        messagebox.showinfo("Authorized", "Schedule X dispensation authorized and recorded in NDPS audit register.")

    def reject_rx(self):
        if not self.selected_rx:
            return
        self.selected_rx["status"] = "Rejected / Clinical Flag"
        if self.connector:
            self.connector.log_event("Rx Rejected", f"Pharmacist rejected {self.selected_rx['rx_id']} due to clinical review", level="WARN")
        self.render_queue()
        messagebox.showwarning("Rejected", f"Prescription {self.selected_rx['rx_id']} rejected.")
