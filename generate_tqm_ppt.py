"""
AegisPharm Enterprise — Review 1: Setup, SRS & Working Application Presentation Generator.
Author: Piyush Bhatt, Student at Amrapali University.
Generates an executive-level 14-slide widescreen (16:9) PowerPoint presentation (.pptx)
strictly structured around the Review 1 Evaluation Rubric:
  - Problem Statement & Baseline Understanding
  - Quality Objectives (TQM Alignment)
  - Software Requirements Specification (SRS)
  - Scope & User Roles (5 RBAC Personas)
  - Modular Folder Architecture (6-tier Structure)
  - Database Design & System Architecture (14 Relational Tables)
  - Comprehensive CRUD Operations Matrix
  - Modules & Core Features Aligned with Quality Goals
  - Initial UI & Main System Workflow
  - Poka-Yoke & Fail-Safe Engineering
  - Working Application Live Demonstration Guide
  - Verification & 24 Automated Test Results
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_review1_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Color Palette Definitions
    NAVY_DARK = RGBColor(10, 37, 64)       # #0A2540
    NAVY_CARD = RGBColor(18, 52, 86)       # #123456
    TEAL_ACCENT = RGBColor(0, 163, 137)    # #00A389
    TEAL_LIGHT = RGBColor(220, 245, 240)   # #DCF5F0
    BG_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)      # #FFFFFF
    BORDER_COLOR = RGBColor(226, 232, 240) # #E2E8F0
    TEXT_MAIN = RGBColor(30, 41, 59)       # #1E293B
    TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B
    TEXT_WHITE = RGBColor(255, 255, 255)   # #FFFFFF
    CORAL_DANGER = RGBColor(225, 29, 72)   # #E11D48
    AMBER_WARN = RGBColor(217, 119, 6)     # #D97706
    BLUE_INFO = RGBColor(2, 132, 199)      # #0284C7

    def add_header(slide, title_text, category_text="REVIEW 1 — SETUP, SRS & WORKING APPLICATION DEMO"):
        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = TEAL_ACCENT
        p_cat.font.name = "Segoe UI"

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(23)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY_DARK
        p_title.font.name = "Segoe UI"

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
        return shape

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Theme)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY_DARK)

    # Decorative Top Teal Strip
    top_strip = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = TEAL_ACCENT
    top_strip.line.fill.background()

    # Title Box
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.3), Inches(3.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "REVIEW 1: PROJECT SETUP, SRS & WORKING APPLICATION DEMO"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = TEAL_ACCENT
    p0.font.name = "Segoe UI"
    p0.space_after = Pt(12)

    p1 = tf1.add_paragraph()
    p1.text = "AegisPharm Enterprise"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.font.name = "Segoe UI"
    p1.space_after = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "Smart Clinical Pharmacy Management System with Total Quality Management (TQM) Architecture"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.font.name = "Segoe UI"

    # Presenter Card (Bottom Left)
    add_card(slide1, Inches(1.0), Inches(5.1), Inches(6.0), Inches(1.8), bg_color=NAVY_CARD, border_color=TEAL_ACCENT)
    tb_pres = slide1.shapes.add_textbox(Inches(1.2), Inches(5.25), Inches(5.6), Inches(1.5))
    tf_pres = tb_pres.text_frame
    tf_pres.word_wrap = True

    p_p1 = tf_pres.paragraphs[0]
    p_p1.text = "PROJECT PRESENTER:"
    p_p1.font.size = Pt(11)
    p_p1.font.bold = True
    p_p1.font.color.rgb = TEAL_ACCENT
    p_p1.font.name = "Segoe UI"

    p_p2 = tf_pres.add_paragraph()
    p_p2.text = "👤 Piyush Bhatt"
    p_p2.font.size = Pt(18)
    p_p2.font.bold = True
    p_p2.font.color.rgb = TEXT_WHITE
    p_p2.font.name = "Segoe UI"

    p_p3 = tf_pres.add_paragraph()
    p_p3.text = "Student, Amrapali University, Haldwani, Uttarakhand"
    p_p3.font.size = Pt(13)
    p_p3.font.color.rgb = RGBColor(203, 213, 225)
    p_p3.font.name = "Segoe UI"

    # Academic Evaluation Context (Bottom Right)
    add_card(slide1, Inches(7.3), Inches(5.1), Inches(5.0), Inches(1.8), bg_color=NAVY_CARD, border_color=BORDER_COLOR)
    tb_inst = slide1.shapes.add_textbox(Inches(7.5), Inches(5.25), Inches(4.6), Inches(1.5))
    tf_inst = tb_inst.text_frame
    tf_inst.word_wrap = True

    p_i1 = tf_inst.paragraphs[0]
    p_i1.text = "EVALUATION MILESTONE:"
    p_i1.font.size = Pt(11)
    p_i1.font.bold = True
    p_i1.font.color.rgb = TEAL_ACCENT
    p_i1.font.name = "Segoe UI"

    p_i2 = tf_inst.add_paragraph()
    p_i2.text = "🏛️ Amrapali University"
    p_i2.font.size = Pt(18)
    p_i2.font.bold = True
    p_i2.font.color.rgb = TEXT_WHITE
    p_i2.font.name = "Segoe UI"

    p_i3 = tf_inst.add_paragraph()
    p_i3.text = "Evaluation: Review 1 — Setup, SRS & Working Application\nAcademic Year 2026"
    p_i3.font.size = Pt(12)
    p_i3.font.color.rgb = RGBColor(203, 213, 225)
    p_i3.font.name = "Segoe UI"

    add_notes(slide1, 
        "Good morning respected professors and project evaluators. I am Piyush Bhatt, student of Amrapali University. "
        "Today I present Review 1 for my project, AegisPharm Enterprise. "
        "This presentation covers our complete Project Setup, Software Requirements Specification (SRS), System Architecture, Database Design, "
        "and demonstrates our fully operational, working application with live CRUD operations and TQM quality gates."
    )

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & BASELINE UNDERSTANDING
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_LIGHT)
    add_header(slide2, "Problem Statement & Baseline Clinical Understanding", "RUBRIC: PROBLEM STATEMENT & BASELINE")

    col_w = Inches(3.64)
    gap = Inches(0.4)
    top_pos = Inches(1.8)
    h_pos = Inches(5.1)

    # Card 1: Clinical Medication Dispensing Failures
    add_card(slide2, Inches(0.8), top_pos, col_w, h_pos)
    tb1 = slide2.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🚨 1. MEDICATION DISPENSING ERRORS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CORAL_DANGER
    p.space_after = Pt(10)
    bullets1 = [
        "Clinical Reality: Over 1.3 million preventable patient injuries occur annually due to adverse drug events (ADEs).",
        "Handwriting & Transcription: Manual interpretation of handwritten prescriptions causes dosage miscalculations.",
        "Allergy Blindspots: Retail pharmacies lack real-time EHR cross-checks, risking fatal Penicillin or NSAID anaphylaxis.",
        "Baseline Remedy: Automated Clinical Decision Support System (CDSS) acting as an immutable quality shield."
    ]
    for b in bullets1:
        p = tf1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)

    # Card 2: Thermal Cold-Chain & Expiry Loss
    add_card(slide2, Inches(0.8) + col_w + gap, top_pos, col_w, h_pos)
    tb2 = slide2.shapes.add_textbox(Inches(1.0) + col_w + gap, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "❄️ 2. COLD-CHAIN & EXPIRY LOSS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AMBER_WARN
    p.space_after = Pt(10)
    bullets2 = [
        "Biological Potency Loss: Vaccines, insulin, and biologics degrade silently outside the 2.0°C–8.0°C thermal envelope.",
        "FIFO Picking Flaw: Standard retail FIFO allows older batches to sit unnoticed while newer stock is sold.",
        "Dead-Stock Write-Offs: Significant annual capital lost in expired, unsellable inventory.",
        "Baseline Remedy: Algorithmic FEFO (First-Expiry, First-Out) picking + 24/7 continuous IoT temperature telemetry."
    ]
    for b in bullets2:
        p = tf2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)

    # Card 3: Regulatory Narcotics & Till Leakage
    add_card(slide2, Inches(0.8) + (col_w + gap)*2, top_pos, col_w, h_pos)
    tb3 = slide2.shapes.add_textbox(Inches(1.0) + (col_w + gap)*2, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "⚖️ 3. NARCOTIC COMPLIANCE & TILL DRIFT"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(10)
    bullets3 = [
        "Schedule X / NDPS Violations: Inadequate tracking of habit-forming sedatives invites severe legal penalties and license revocation.",
        "Cash Drawer Shrinkage: Till variances, untracked mid-shift cash drops, and unverified digital UPI receipts.",
        "Failed Inspector Audits: Inability to generate instant batch reports during surprise CDSCO/FDA inspections.",
        "Baseline Remedy: Mandatory dual-PIN narcotic register + Daily Z-Report mathematical drawer reconciliation."
    ]
    for b in bullets3:
        p = tf3.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)

    add_notes(slide2,
        "We begin with the Problem Statement and Baseline Understanding. "
        "In healthcare, software errors aren't just bugs—they threaten patient survival. "
        "Our baseline analysis identified 3 fundamental industry failures: clinical medication errors, thermal cold-chain spoilage, "
        "and narcotic compliance/cash drawer shrinkage. AegisPharm solves these at the architectural root."
    )

    # =========================================================================
    # SLIDE 3: QUALITY OBJECTIVES & TQM ALIGNMENT
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_LIGHT)
    add_header(slide3, "Quality Objectives Aligned with TQM Principles", "RUBRIC: QUALITY OBJECTIVE")

    objectives = [
        ("Objective 1: Zero Medication Dispensing Defects (Patient Focus)", 
         "Poka-Yoke error-proofing: Implement an automated Clinical Decision Support System (CDSS) that intercepts allergen cross-reactions (Penicillin, NSAIDs, Sulfa) and toxic drug-drug interactions before an invoice can be created.",
         TEAL_ACCENT),
        ("Objective 2: 100% Cold-Chain Storage & Transport Compliance", 
         "Biological Integrity: Guarantee all thermo-sensitive pharmaceuticals are stored within the mandatory 2.0°C–8.0°C range via real-time 30s IoT telemetry streaming and automatic thermal spike alarms.",
         BLUE_INFO),
        ("Objective 3: Zero Expiry Dead-Stock Losses (FEFO Scheduling)", 
         "Process Quality: Eliminate inventory wastage by algorithmically enforcing First-Expiry, First-Out (FEFO) batch prioritization, ensuring nearest-expiry viable medicines are dispensed first.",
         AMBER_WARN),
        ("Objective 4: Zero Cash Register Discrepancy & Till Balancing", 
         "Fact-Based Management: Enforce strict shift-end financial governance through the Daily Z-Report engine, mathematically balancing opening float, sales, payouts, and counted physical currency.",
         NAVY_DARK),
        ("Objective 5: 100% Regulatory Audit Readiness (ISO 9001 & CDSCO)", 
         "Continuous Assurance: Maintain an immutable SQLite audit trail, dual-PIN Schedule X narcotic register, and 1-click CSV export ready for State Drug Inspectors.",
         CORAL_DANGER)
    ]

    card_h = Inches(0.9)
    y_start = Inches(1.8)
    for i, (title, desc, color) in enumerate(objectives):
        y_pos = y_start + Inches(i * 1.05)
        add_card(slide3, Inches(0.8), y_pos, Inches(11.733), card_h)

        bar = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos, Inches(0.15), card_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        tb = slide3.shapes.add_textbox(Inches(1.1), y_pos + Inches(0.08), Inches(11.2), card_h - Inches(0.16))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MAIN

    add_notes(slide3,
        "Here are our 5 foundational Quality Objectives, directly fulfilling the Review 1 rubric. "
        "Notice how each objective maps to a core TQM tenet: Zero dispensing defects represents Customer/Patient Focus; "
        "Cold-Chain and FEFO represent Process Quality; and the Daily Z-Report represents Fact-Based Management."
    )

    # =========================================================================
    # SLIDE 4: SOFTWARE REQUIREMENTS SPECIFICATION (SRS) OVERVIEW
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_LIGHT)
    add_header(slide4, "Software Requirements Specification (SRS) — IEEE 830", "RUBRIC: SRS (REQUIREMENTS ENGINEERING)")

    # Left Card: Functional Requirements (FR)
    add_card(slide4, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_fr = slide4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_fr = tb_fr.text_frame
    tf_fr.word_wrap = True

    p = tf_fr.paragraphs[0]
    p.text = "📋 FUNCTIONAL REQUIREMENTS (FR)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(10)

    fr_items = [
        "FR-01 (Authentication & RBAC): System shall enforce role-locked workstation sessions across 5 distinct staff personas.",
        "FR-02 (eRx Intake & CDSS): System shall validate incoming digital prescriptions and trigger blocking alerts on allergen contraindications.",
        "FR-03 (Schedule X Narcotics): System shall require Doctor DMC Reg No. and 4-digit Pharmacist PIN verification for controlled substances.",
        "FR-04 (POS & Multi-Tender): System shall support 1-click verified eRx import, barcode search, dynamic UPI QR generation, and cash change calculation.",
        "FR-05 (FEFO Batch Picker): System shall sort inventory batches by earliest calendar expiry and prevent dispensing expired SKUs.",
        "FR-06 (Cold-Chain IoT): System shall log digital temperature every 30s and trigger visual/audio alarms when temperatures exceed 8.0°C.",
        "FR-07 (Delivery e-POD): System shall require a 4-digit customer SMS OTP before an order can be marked as 'Delivered'.",
        "FR-08 (Z-Report Close): System shall reconcile shift cash, UPI, card, and CGST/SGST tax liabilities into signed, immutable records."
    ]
    for item in fr_items:
        p = tf_fr.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(4)

    # Right Card: Non-Functional Requirements (NFR)
    add_card(slide4, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_nfr = slide4.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_nfr = tb_nfr.text_frame
    tf_nfr.word_wrap = True

    p = tf_nfr.paragraphs[0]
    p.text = "⚡ NON-FUNCTIONAL REQUIREMENTS (NFR)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(10)

    nfr_items = [
        "NFR-01 (Performance & Latency): System shall execute database queries in <50ms and render desktop UI at 60 FPS via Edge Chromium WebView2.",
        "NFR-02 (Reliability & ACID Compliance): SQLite database shall ensure 100% ACID compliance with automatic timestamped snapshot backups.",
        "NFR-03 (Security & Tamper-Proofing): System shall record all user actions in an immutable append-only audit trail and prevent unauthorized role switching.",
        "NFR-04 (Maintainability & Modularity): System shall strictly follow a 6-tier modular folder architecture with decoupled bridge RPC layers.",
        "NFR-05 (Regulatory Compliance): System shall comply with Indian Drugs & Cosmetics Act (Schedule H1/X) and GST electronic invoicing standards.",
        "NFR-06 (Portability): System shall run natively as a high-performance Windows desktop application and as a modern web application."
    ]
    for item in nfr_items:
        p = tf_nfr.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(8)

    add_notes(slide4,
        "This slide presents the core of our Software Requirements Specification (SRS), formatted per IEEE 830 standards. "
        "On the left, we outline our 8 essential Functional Requirements—covering RBAC, CDSS, narcotics, FEFO, IoT, and Z-report. "
        "On the right, our Non-Functional Requirements guarantee sub-50ms latency, 60 FPS desktop rendering, and 100% ACID database reliability."
    )

    # =========================================================================
    # SLIDE 5: SCOPE & USER ROLES (ROLE-BASED ACCESS CONTROL)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_LIGHT)
    add_header(slide5, "Project Scope & Granular User Roles (RBAC)", "RUBRIC: SCOPE & USER ROLES")

    roles = [
        ("👑 Store Admin", "Console HQ", "• Manage staff accounts & passwords\n• Monitor live online terminal presence\n• Review daily Z-Report reconciliations\n• Execute SQLite snapshot backups\n• Inspect system audit stream"),
        ("🩺 Clinical Pharmacist", "Clinical Bay", "• Review incoming e-Prescriptions queue\n• CDSS allergy shield cross-checks\n• Drug-drug interaction risk analysis\n• Schedule X narcotic PIN sign-off\n• Manage chronic patient refill cycles"),
        ("💳 Cashier (POS)", "Billing Counter", "• 1-Click verified eRx import to cart\n• Auto FEFO nearest-expiry batch pick\n• Split payments (Cash, UPI QR, Card)\n• Calculate cash change return\n• Print 80mm GST tax receipt"),
        ("📦 Inventory Manager", "Supply Hub", "• Multi-batch FEFO stock ledger\n• Record Goods Receipt Notes (GRN)\n• 24/7 Cold-chain IoT fridge monitor\n• Manage supplier directory & POs\n• Track low-stock alerts (≤20 units)"),
        ("🛵 Delivery Agent", "Logistics Bay", "• Active dispatch Kanban route board\n• Verify cold-bag insulated packaging\n• 4-Digit customer OTP verification\n• Record electronic Proof-of-Delivery\n• Handover timestamp audit log")
    ]

    card_w = Inches(2.22)
    for i, (r_name, r_term, r_resp) in enumerate(roles):
        x = Inches(0.8) + Inches(i * 2.37)
        c = add_card(slide5, x, Inches(1.8), card_w, Inches(5.1))

        # Header Box
        hb = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), card_w, Inches(0.7))
        hb.fill.solid()
        hb.fill.fore_color.rgb = NAVY_DARK if i % 2 == 0 else TEAL_ACCENT
        hb.line.fill.background()

        tb_h = slide5.shapes.add_textbox(x, Inches(1.85), card_w, Inches(0.6))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        p = tf_h.paragraphs[0]
        p.text = r_name
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb_b = slide5.shapes.add_textbox(x + Inches(0.1), Inches(2.55), card_w - Inches(0.2), Inches(4.2))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True

        p_term = tf_b.paragraphs[0]
        p_term.text = f"Terminal: {r_term}"
        p_term.font.size = Pt(10)
        p_term.font.bold = True
        p_term.font.color.rgb = TEXT_MUTED
        p_term.space_after = Pt(8)

        for line in r_resp.split('\n'):
            p = tf_b.add_paragraph()
            p.text = line
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(4)

    add_notes(slide5,
        "Scope and User Roles are essential criteria in Review 1. "
        "AegisPharm establishes strict Role-Based Access Control (RBAC). "
        "Unlike generic retail software where any staff member can delete logs or sell narcotics, "
        "our 5 specialized personas enforce security and quality separation of concerns."
    )

    # =========================================================================
    # SLIDE 6: MODULAR FOLDER ARCHITECTURE & TECHNICAL BASELINE
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_LIGHT)
    add_header(slide6, "Modular Folder Architecture & Technical Baseline", "RUBRIC: MODULAR ARCHITECTURE")

    # Left Card: Directory Tree
    add_card(slide6, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_tree = slide6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_tree = tb_tree.text_frame
    tf_tree.word_wrap = True

    p = tf_tree.paragraphs[0]
    p.text = "📁 ENTERPRISE FOLDER STRUCTURE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(8)

    tree_str = """Pharmacy_Management_System/
├── core/
│   ├── bridge.py       # Unified Python RPC Bridge (38 methods)
│   ├── db.py           # SQLite persistence layer (14 tables)
│   ├── api_client.py   # Presence heartbeat AppConnector
│   └── logger.py       # Tamper-evident audit logging engine
├── config/
│   └── settings.py     # Thread-safe Singleton dataclass (config.json)
├── ui/
│   ├── desktop/        # Edge Chromium WebView2 60 FPS frontend
│   └── web/            # Full-featured FastAPI Web UI (1:1 parity)
├── apps/               # Standalone admin & operations GUI apps
├── tests/              # 24 Automated unit & integration tests
├── backups/            # Scheduled .db snapshots & CSV audit exports
├── main.py             # Hardware-accelerated desktop entrypoint
└── web_app.py          # Asynchronous FastAPI web application server"""

    for line in tree_str.split('\n'):
        p = tf_tree.add_paragraph()
        p.text = line
        p.font.size = Pt(9.5)
        p.font.name = "Consolas"
        p.font.color.rgb = TEXT_MAIN

    # Right Card: Architecture Tiers & Decoupling
    add_card(slide6, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_tiers = slide6.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_tiers = tb_tiers.text_frame
    tf_tiers.word_wrap = True

    p = tf_tiers.paragraphs[0]
    p.text = "🏗️ 6-TIER DECOUPLED ARCHITECTURE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(8)

    tiers = [
        ("Tier 1: Presentation Layer", "Modern HTML5, responsive CSS3 Glassmorphism, and vanilla ES6+ JavaScript. Clean SPA design without external framework bloat."),
        ("Tier 2: Desktop Runtime", "Microsoft Edge Chromium (WebView2) via `pywebview 5.x` providing zero-latency 60 FPS hardware acceleration."),
        ("Tier 3: Web Application Server", "Asynchronous `FastAPI 0.138.0` + `Uvicorn 0.49.0` ASGI backend with auto-generated Swagger API documentation."),
        ("Tier 4: Unified Bridge RPC", "`PharmacyBridge` exposes 38 secure, thread-safe Python methods directly to frontend JavaScript."),
        ("Tier 5: Core Domain Engines", "Autonomous engines: CDSS allergy cross-matcher, FEFO dynamic batch sorter, cold-chain IoT simulator, Daily Z-Report engine."),
        ("Tier 6: Persistence & Storage", "SQLite 3 ACID relational database with 14 normalized tables, foreign keys, and timestamped automated backups.")
    ]
    for t_name, t_desc in tiers:
        p = tf_tiers.add_paragraph()
        p.text = t_name
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        p2 = tf_tiers.add_paragraph()
        p2.text = t_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_after = Pt(4)

    add_notes(slide6,
        "Here we demonstrate our Modular Folder Architecture, answering the specific Review 1 criterion. "
        "The project is organized into clean, decoupled tiers: core logic, configuration, dual desktop/web UIs, tests, and backups. "
        "A single unified bridge serves both the desktop Edge Chromium WebView2 window and the FastAPI web server."
    )

    # =========================================================================
    # SLIDE 7: DATABASE DESIGN & SYSTEM INTEGRATION
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_LIGHT)
    add_header(slide7, "Database Design & System Integration (SQLite 3)", "RUBRIC: DATABASE / SYSTEM DESIGN")

    # Table breakdown (2 Columns of 7 tables)
    db_tables_1 = [
        ("1. staff", "PRIMARY KEY: id", "Credentials, assigned role, username, branch, and active status."),
        ("2. medicines", "PRIMARY KEY: id", "SKU, generic name, category, Schedule (H1/X/OTC), rack, stock."),
        ("3. prescriptions", "PRIMARY KEY: rx_id", "Patient name, doctor, items JSON, CDSS status, clinical sign-off."),
        ("4. invoices", "PRIMARY KEY: invoice_id", "Customer, cashier, payment method, subtotal, GST, total amount."),
        ("5. delivery_orders", "PRIMARY KEY: order_id", "Address, customer phone, rider, status, cold-bag check, OTP code."),
        ("6. patients", "PRIMARY KEY: id", "Name, contact phone, chronic conditions, loyalty points, allergy records."),
        ("7. suppliers", "PRIMARY KEY: id", "Distributor name, GSTIN, DL number, contact person, payment terms.")
    ]

    db_tables_2 = [
        ("8. purchase_orders", "PRIMARY KEY: po_id", "GRN shipment log, supplier, items JSON, total amount, inward status."),
        ("9. narcotic_register", "PRIMARY KEY: id (AUTO)", "Schedule X log: Doctor DMC Reg No, Pharmacist PIN, batch, quantity."),
        ("10. temperature_logs", "PRIMARY KEY: id (AUTO)", "24/7 cold-chain telemetry: Sensor ID, temperature (2-8°C), alert flag."),
        ("11. refill_schedules", "PRIMARY KEY: id", "Chronic adherence: Patient, medicine, last dispensed, next due date."),
        ("12. active_sessions", "PRIMARY KEY: session_id", "Live presence: User ID, role, terminal name, last heartbeat timestamp."),
        ("13. audit_logs", "PRIMARY KEY: id (AUTO)", "Immutable security log: User, role, action, details, severity level."),
        ("14. z_reports", "PRIMARY KEY: z_report_id", "Daily closing: Opening float, cash sales, payouts, variance, signed status.")
    ]

    col_w = Inches(5.75)
    # Column 1
    add_card(slide7, Inches(0.8), Inches(1.8), col_w, Inches(5.1))
    tb_db1 = slide7.shapes.add_textbox(Inches(1.0), Inches(2.0), col_w - Inches(0.4), Inches(4.7))
    tf_db1 = tb_db1.text_frame
    tf_db1.word_wrap = True
    p = tf_db1.paragraphs[0]
    p.text = "🗄️ CORE RELATIONAL TABLES (PART 1)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(6)

    for t_name, t_key, t_desc in db_tables_1:
        p = tf_db1.add_paragraph()
        p.text = f"{t_name} ({t_key})"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        p2 = tf_db1.add_paragraph()
        p2.text = t_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_after = Pt(3)

    # Column 2
    add_card(slide7, Inches(6.75), Inches(1.8), col_w, Inches(5.1))
    tb_db2 = slide7.shapes.add_textbox(Inches(6.95), Inches(2.0), col_w - Inches(0.4), Inches(4.7))
    tf_db2 = tb_db2.text_frame
    tf_db2.word_wrap = True
    p = tf_db2.paragraphs[0]
    p.text = "🗄️ COMPLIANCE & TELEMETRY TABLES (PART 2)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(6)

    for t_name, t_key, t_desc in db_tables_2:
        p = tf_db2.add_paragraph()
        p.text = f"{t_name} ({t_key})"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        p2 = tf_db2.add_paragraph()
        p2.text = t_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_after = Pt(3)

    add_notes(slide7,
        "Here is the complete Database Design and System Integration. "
        "AegisPharm utilizes SQLite 3 configured with WAL mode and foreign key constraints across 14 normalized tables. "
        "Notice the specialized tables: narcotic_register for Schedule X compliance, temperature_logs for IoT cold-chain, and z_reports for cash reconciliation."
    )

    # =========================================================================
    # SLIDE 8: COMPREHENSIVE CRUD OPERATIONS MATRIX
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, BG_LIGHT)
    add_header(slide8, "Comprehensive CRUD Operations Implementation", "RUBRIC: CRUD OPERATIONS & FUNCTIONALITY")

    crud_data = [
        ("Module / Entity", "CREATE", "READ", "UPDATE", "DELETE"),
        ("Staff & Users", "Add staff user modal (ID, Name, Role, Branch)", "Staff credentials list & live online presence", "Edit staff role, password, branch & status", "Delete unauthorized staff user with audit log"),
        ("Medicines Catalog", "Add medicine modal (SKU, Category, Batch)", "Catalog table with FEFO visual countdown badges", "Adjust physical stock delta (+/- units modal)", "Delete expired/discontinued medicine SKU"),
        ("Clinical Prescriptions", "Inward e-Prescription modal with medicine items", "Prescriptions review queue with CDSS allergy scan", "Update verification status (Approve / Reject)", "Archive processed prescriptions into sales ledger"),
        ("Narcotic Register", "Add Schedule X dispensation with Doctor Reg No", "Read narcotic audit ledger with search filter", "Update verified status with 4-digit Pharmacist PIN", "Restricted: Immutable audit records (CDSCO law)"),
        ("Invoices & POS", "Generate sales invoice with 5% CGST/SGST split", "Sales ledger history with 1-click receipt modal", "Update patient loyalty points upon purchase", "Void invoice requires supervisor override"),
        ("Deliveries & Logistics", "Create home delivery order with customer phone", "Dispatch Kanban board (Packaging/Out/Delivered)", "Advance delivery status & verify 4-digit OTP", "Cancel unassigned delivery dispatch task"),
        ("Daily Z-Report Close", "Generate official Z-Report ID (Z-YYYYMMDD-XXXX)", "Read gross sales, cash total, digital collections", "Update counted cash & calculate live variance", "Permanent archive: Immutable signed registry")
    ]

    add_card(slide8, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1))
    tb_c = slide8.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(11.3), Inches(4.8))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "⚡ COMPLETE CRUD IMPLEMENTATION ACROSS ALL CORE MODULES"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(8)

    for row_idx, (ent, c, r, u, d) in enumerate(crud_data):
        p = tf_c.add_paragraph()
        if row_idx == 0:
            p.text = f"{ent:<22} | {c:<25} | {r:<25} | {u:<25} | {d}"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = NAVY_DARK
        else:
            p.text = f"{ent:<22} | {c:<25} | {r:<25} | {u:<25} | {d}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    add_notes(slide8,
        "CRUD operations are explicitly evaluated in Review 1. "
        "As shown in this comprehensive matrix, AegisPharm implements full Create, Read, Update, and Delete operations "
        "across all 7 major functional domains—Staff, Medicines, Prescriptions, Narcotics, Billing, Deliveries, and Z-Reports. "
        "Every operation is fully wired to SQLite and verified by automated tests."
    )

    # =========================================================================
    # SLIDE 9: MODULES & CORE FEATURES ALIGNED WITH QUALITY GOALS
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, BG_LIGHT)
    add_header(slide9, "Modules Aligned with TQM Quality Goals", "RUBRIC: MODULES & QUALITY ALIGNMENT")

    # 4 Module Cards (2x2 Grid)
    modules = [
        ("🩺 Clinical Decision Support (CDSS)", 
         "Aligned TQM Goal: Zero Medication Dispensing Defects",
         "• Real-time allergen cross-checks (Penicillin, NSAIDs, Sulfa).\n• Molecule-molecule drug interaction checker.\n• Double sign-off for Schedule X narcotics (Pharmacist PIN + Doctor Reg).\n• Patient chronic disease and allergy EHR integration.",
         TEAL_ACCENT),
        ("📦 FEFO Inventory & Cold-Chain IoT", 
         "Aligned TQM Goal: Zero Biological Potency Loss & Zero Dead-Stock",
         "• Strict First-Expiry, First-Out batch sequencing algorithms.\n• Visual countdown tags (<30d Critical, <90d Attention).\n• 24/7 continuous IoT refrigerator telemetry (2.0°C–8.0°C).\n• Goods Receipt Notes (GRN) dockside supplier verification.",
         BLUE_INFO),
        ("💳 Cashier Express POS & GST Billing", 
         "Aligned TQM Goal: Service Speed, Tax Integrity & Zero Cash Leakage",
         "• 1-Click verified eRx import from clinical queue.\n• Multi-tender checkout: Cash change calculator, Dynamic UPI QR, Card.\n• Automated statutory 5% GST calculation (2.5% CGST + 2.5% SGST).\n• Instant 80mm thermal receipt printing and sales ledger.",
         NAVY_DARK),
        ("🛵 Delivery Dispatch Fleet (e-POD)", 
         "Aligned TQM Goal: 100% Last-Mile Handover Fidelity",
         "• Visual 3-column route Kanban board (Packaging, Out, Delivered).\n• Cold-bag insulated packaging verification checklist.\n• 4-Digit customer SMS OTP verification before order handoff.\n• Automatic GPS arrival and handover timestamp logging.",
         AMBER_WARN)
    ]

    for idx, (title, goal, points, col) in enumerate(modules):
        r = idx // 2
        c_i = idx % 2
        x = Inches(0.8) + Inches(c_i * 5.95)
        y = Inches(1.8) + Inches(r * 2.6)
        w = Inches(5.75)
        h = Inches(2.4)

        add_card(slide9, x, y, w, h)
        bar = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = slide9.shapes.add_textbox(x + Inches(0.25), y + Inches(0.12), w - Inches(0.4), h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK

        p2 = tf.add_paragraph()
        p2.text = goal.upper()
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.space_after = Pt(4)

        for line in points.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(2)

    add_notes(slide9,
        "Here we map our Core Modules directly to our TQM Quality Goals, satisfying the Image 3 requirement. "
        "Notice that our features are not arbitrary: CDSS directly targets zero medication defects; "
        "FEFO and IoT target zero biological spoilage; and our delivery module targets 100% last-mile fidelity."
    )

    # =========================================================================
    # SLIDE 10: INITIAL UI & MAIN SYSTEM WORKFLOW
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, BG_LIGHT)
    add_header(slide10, "Initial UI & End-to-End System Workflow", "RUBRIC: INITIAL UI & MAIN WORKFLOW")

    # Flow Steps (5 Sequential Stages)
    stages = [
        ("Stage 1: Prescription Intake", "Doctor e-Prescription uploaded\nPatient EHR allergies scanned\nEnters pending review queue", BLUE_INFO),
        ("Stage 2: Clinical CDSS Gate", "Pharmacist runs CDSS scan\nAllergy & interaction checks\nSchedule X PIN authenticated\nStatus updated to 'Approved'", TEAL_ACCENT),
        ("Stage 3: POS Express Billing", "1-Click import to Cashier cart\nAuto FEFO batch picking\nDynamic UPI QR / Cash change\nThermal 80mm GST receipt printed", NAVY_DARK),
        ("Stage 4: Cold-Chain & Fleet", "Cold-bag checklist verified\nDispatched on Kanban route\nCustomer gives 4-digit OTP\nMarked 'Delivered' (e-POD)", AMBER_WARN),
        ("Stage 5: Daily Z-Report Close", "Cash drawer counted\nVariance calculated (₹0.00)\nShift signed & closed in SQLite\nCSV exported for accounting", CORAL_DANGER)
    ]

    col_w = Inches(2.22)
    for i, (title, desc, col) in enumerate(stages):
        x = Inches(0.8) + Inches(i * 2.37)
        c = add_card(slide10, x, Inches(1.8), col_w, Inches(3.2))

        hb = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), col_w, Inches(0.6))
        hb.fill.solid()
        hb.fill.fore_color.rgb = col
        hb.line.fill.background()

        tb_h = slide10.shapes.add_textbox(x, Inches(1.85), col_w, Inches(0.5))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        p = tf_h.paragraphs[0]
        p.text = f"STEP {i+1}"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb_b = slide10.shapes.add_textbox(x + Inches(0.1), Inches(2.5), col_w - Inches(0.2), Inches(2.4))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True

        p1 = tf_b.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK
        p1.space_after = Pt(6)

        for line in desc.split('\n'):
            p = tf_b.add_paragraph()
            p.text = "• " + line
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(3)

    # Bottom UI Architecture Highlight Card
    add_card(slide10, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.7))
    tb_ui = slide10.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.5))
    tf_ui = tb_ui.text_frame
    tf_ui.word_wrap = True

    p = tf_ui.paragraphs[0]
    p.text = "🎨 USER INTERFACE DESIGN & DUAL DEPLOYMENT PARITY"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(4)

    ui_points = (
        "• Desktop UI: Rendered via Microsoft Edge Chromium WebView2 engine with hardware acceleration (60 FPS) and zero native bridge latency.\n"
        "• Web UI: Hosted asynchronously via FastAPI (Uvicorn), providing 100% feature parity on Chrome, Safari, Edge, tablets, and mobile.\n"
        "• Design System: Custom dark-mode Glassmorphism with CSS variables, responsive side navigation, interactive modals, and live clock tickers."
    )
    for line in ui_points.split('\n'):
        p = tf_ui.add_paragraph()
        p.text = line
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    add_notes(slide10,
        "Here we show the Initial UI and Main System Workflow. "
        "A prescription progresses smoothly from Stage 1 intake through Stage 2 clinical verification, Stage 3 POS billing, "
        "Stage 4 delivery dispatch with OTP, and finally Stage 5 daily Z-Report drawer reconciliation. "
        "Both our desktop and web interfaces provide 1:1 workflow parity."
    )

    # =========================================================================
    # SLIDE 11: POKA-YOKE (FAIL-SAFE QUALITY GATES)
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, BG_LIGHT)
    add_header(slide11, "Poka-Yoke: Mistake-Proofing Healthcare Operations", "FAIL-SAFE QUALITY GATES")

    poka_gates = [
        ("1. CDSS Patient Allergy Shield", 
         "Poka-Yoke Mechanism: Automated Blocking Gate",
         "The cashier or pharmacist cannot bypass or dispense drugs containing penicillin, NSAIDs, or sulfas if the patient EHR contains registered hypersensitivity. Prevents fatal anaphylaxis before billing.",
         TEAL_ACCENT),
        ("2. Molecule Interaction Guard", 
         "Poka-Yoke Mechanism: Cross-Reference Alert",
         "When combining multiple drugs in a prescription (e.g. Warfarin + Augmentin, Glycomet + Alcohol), the Clinical Decision Support System triggers a severe warning modal preventing toxic dosing.",
         CORAL_DANGER),
        ("3. Schedule X Narcotics Dual PIN", 
         "Poka-Yoke Mechanism: Mandatory Dual Authentication",
         "Narcotic sedatives (e.g. Alprax, Diazepam) cannot be added to the POS cart without doctor registration number validation and a 4-digit pharmacist authorization PIN, eliminating illegal diversion.",
         BLUE_INFO),
        ("4. 4-Digit OTP Delivery Handshake", 
         "Poka-Yoke Mechanism: Cryptographic Handshake",
         "A delivery agent cannot mark an order as 'Delivered' simply by clicking a button. The customer must provide a 4-digit SMS OTP, guaranteeing medicines are handed to the rightful patient.",
         AMBER_WARN)
    ]

    for idx, (title, mech, desc, col) in enumerate(poka_gates):
        r = idx // 2
        c_i = idx % 2
        x = Inches(0.8) + Inches(c_i * 5.95)
        y = Inches(1.8) + Inches(r * 2.6)
        w = Inches(5.75)
        h = Inches(2.4)

        add_card(slide11, x, y, w, h)
        bar = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = slide11.shapes.add_textbox(x + Inches(0.25), y + Inches(0.12), w - Inches(0.4), h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK

        p2 = tf.add_paragraph()
        p2.text = mech.upper()
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = TEXT_MAIN

    add_notes(slide11,
        "Poka-Yoke mistake-proofing is one of the most effective TQM tools we built. "
        "Our software makes human errors logically impossible: an allergic patient cannot be given penicillin, "
        "a cashier cannot accidentally select newer stock before older stock, and a rider cannot fake delivery without the customer OTP."
    )

    # =========================================================================
    # SLIDE 12: WORKING APPLICATION LIVE DEMONSTRATION GUIDE
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, BG_LIGHT)
    add_header(slide12, "Working Application Live Demonstration Guide", "RUBRIC: WORKING APPLICATION / DEMO")

    # Step-by-Step Live Demo Execution Guide (3 Columns)
    demo_steps = [
        ("Step 1: Application Launch", 
         "Desktop Launch:\n`python main.py`\n(Hardware-accelerated Edge Chromium WebView2 window)\n\nWeb Server Launch:\n`python web_app.py`\n(Access at http://127.0.0.1:8000)\n\nSwagger API Documentation:\nAccess at http://127.0.0.1:8000/docs",
         NAVY_DARK),
        ("Step 2: Role Walkthrough", 
         "1. Login as Admin (`admin`/`admin123`):\n   Inspect RBAC, terminals, audit log.\n2. Switch to Pharmacist:\n   Review eRx, trigger CDSS allergy shield.\n3. Switch to Cashier:\n   1-Click Rx import, FEFO batch selection, UPI QR modal, print 80mm GST receipt.",
         TEAL_ACCENT),
        ("Step 3: Quality Gates & Close", 
         "4. Switch to Inventory Manager:\n   Demonstrate 2–8°C thermal spike alarm, record Goods Receipt Note (GRN).\n5. Switch to Delivery Rider:\n   Advance Kanban, verify 4-digit OTP.\n6. Return to Admin / Cashier:\n   Perform Daily Z-Report cash reconciliation, balance till, print official Z-slip.",
         BLUE_INFO)
    ]

    col_w = Inches(3.64)
    gap = Inches(0.4)
    for i, (title, content, col) in enumerate(demo_steps):
        x = Inches(0.8) + Inches(i * 4.04)
        c = add_card(slide12, x, Inches(1.8), col_w, Inches(5.1))

        hb = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), col_w, Inches(0.7))
        hb.fill.solid()
        hb.fill.fore_color.rgb = col
        hb.line.fill.background()

        tb_h = slide12.shapes.add_textbox(x, Inches(1.85), col_w, Inches(0.6))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        p = tf_h.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb_b = slide12.shapes.add_textbox(x + Inches(0.15), Inches(2.6), col_w - Inches(0.3), Inches(4.2))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for line in content.split('\n'):
            p = tf_b.add_paragraph() if tf_b.paragraphs[0].text else tf_b.paragraphs[0]
            p.text = line
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(4)

    add_notes(slide12,
        "This slide serves as our live demonstration script for Review 1. "
        "I will now launch the application live: running `python main.py` opens the desktop window, "
        "and `python web_app.py` serves the browser interface. "
        "We will walk through the 5 roles, show the CDSS allergy barrier in action, demonstrate the cold-chain alarm, and close the shift using the Daily Z-Report."
    )

    # =========================================================================
    # SLIDE 13: TEST RESULTS & QUALITY VERIFICATION METRICS
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, BG_LIGHT)
    add_header(slide13, "Quality Verification & 24 Automated Test Results", "RUBRIC: IMPLEMENTED FUNCTIONALITY")

    # 4 Big Stat Metric Cards
    metrics = [
        ("24 / 24", "Automated Tests Passed", "100% pass rate across end-to-end unit, integration, and security test suites.", TEAL_ACCENT),
        ("0%", "Medication Dispensing Errors", "Achieved via automated Poka-Yoke CDSS allergy and interaction barriers.", CORAL_DANGER),
        ("100%", "Cold-Chain Integrity (2–8°C)", "Continuous 30s background telemetry streaming with instant excursion alerts.", BLUE_INFO),
        ("₹ 0.00", "Cash Drawer Variance", "Achieved on balanced registers via Daily Z-Report mathematical reconciliation.", NAVY_DARK)
    ]

    for i, (stat, label, desc, col) in enumerate(metrics):
        x = Inches(0.8) + Inches(i * 2.98)
        c = add_card(slide13, x, Inches(1.8), Inches(2.78), Inches(2.2))

        tb = slide13.shapes.add_textbox(x + Inches(0.1), Inches(1.9), Inches(2.58), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = stat
        p1.font.size = Pt(32)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.size = Pt(11.5)
        p2.font.bold = True
        p2.font.color.rgb = NAVY_DARK
        p2.space_after = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = TEXT_MUTED

    # Bottom Comparison Table: Manual Pharmacy vs. AegisPharm Enterprise
    add_card(slide13, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.6))
    tb_t = slide13.shapes.add_textbox(Inches(1.0), Inches(4.45), Inches(11.3), Inches(2.3))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p = tf_t.paragraphs[0]
    p.text = "📊 TRADITIONAL PHARMACY VS. AEGISPHARM TQM BENCHMARK"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(6)

    comparisons = [
        ("Quality Dimension", "Traditional Retail Pharmacy (Manual)", "AegisPharm Enterprise (TQM Driven)"),
        ("Prescription Safety", "Manual pharmacist check; vulnerable to handwriting errors", "Automated CDSS cross-checks with patient allergy EHR"),
        ("Inventory Picking", "Random or FIFO; older batches expire on shelves", "Algorithmic FEFO (First-Expiry, First-Out) guarantee"),
        ("Cold-Chain Monitoring", "Infrequent manual thermometer checks; silent spoilage", "Continuous 30s IoT telemetry with automatic alarm alerts"),
        ("Shift Cash Balancing", "Paper ledger estimations; undetected shrinkage", "Daily Z-Report mathematical reconciliation & signed Z-slip")
    ]
    for row_idx, (col1, col2, col3) in enumerate(comparisons):
        p = tf_t.add_paragraph()
        if row_idx == 0:
            p.text = f"{col1:<24} | {col2:<42} | {col3}"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = TEAL_ACCENT
        else:
            p.text = f"{col1:<24} | {col2:<42} | {col3}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    add_notes(slide13,
        "Here are our empirical verification metrics: "
        "Our test suite passes 24 out of 24 automated unit and integration tests with a 100% success rate. "
        "The comparison table below demonstrates how AegisPharm transforms traditional manual vulnerabilities into standardized, automated TQM safeguards."
    )

    # =========================================================================
    # SLIDE 14: CONCLUSION & REVIEW 1 DEFENSE Q&A (Dark Navy Theme)
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, NAVY_DARK)

    # Top strip
    strip14 = slide14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    strip14.fill.solid()
    strip14.fill.fore_color.rgb = TEAL_ACCENT
    strip14.line.fill.background()

    tb_end = slide14.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.3), Inches(3.4))
    tf_e = tb_end.text_frame
    tf_e.word_wrap = True

    pe0 = tf_e.paragraphs[0]
    pe0.text = "REVIEW 1 SUMMARY & STRATEGIC CONCLUSION"
    pe0.font.size = Pt(13)
    pe0.font.bold = True
    pe0.font.color.rgb = TEAL_ACCENT
    pe0.space_after = Pt(8)

    pe1 = tf_e.add_paragraph()
    pe1.text = "Review 1 Milestones Fully Delivered"
    pe1.font.size = Pt(36)
    pe1.font.bold = True
    pe1.font.color.rgb = TEXT_WHITE
    pe1.space_after = Pt(12)

    milestones = [
        "✓ Problem Statement & Quality Objectives: Clearly formulated and aligned with TQM principles.",
        "✓ Formal SRS Document: Comprehensive IEEE 830 functional and non-functional requirements specified.",
        "✓ Scope & User Roles: 5 specialized RBAC workstations with granular access control implemented.",
        "✓ Modular Folder Architecture: 6-tier decoupled structure separating core logic, config, and UIs.",
        "✓ Database & CRUD Functionality: 14 relational tables in SQLite with complete CRUD operations working live.",
        "✓ Working Application & Demo: Operational desktop (Edge Chromium) and web (FastAPI) applications demonstrated."
    ]
    for ms in milestones:
        p = tf_e.add_paragraph()
        p.text = ms
        p.font.size = Pt(12.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(5)

    # Thank You & Q&A Box
    add_card(slide14, Inches(1.0), Inches(5.0), Inches(11.3), Inches(1.8), bg_color=NAVY_CARD, border_color=TEAL_ACCENT)
    tb_qa = slide14.shapes.add_textbox(Inches(1.2), Inches(5.15), Inches(10.9), Inches(1.5))
    tf_qa = tb_qa.text_frame
    tf_qa.word_wrap = True

    pq1 = tf_qa.paragraphs[0]
    pq1.text = "🙏 THANK YOU RESPECED FACULTY & EVALUATORS"
    pq1.font.size = Pt(15)
    pq1.font.bold = True
    pq1.font.color.rgb = TEAL_ACCENT
    pq1.space_after = Pt(4)

    pq2 = tf_qa.add_paragraph()
    pq2.text = "Sincere gratitude to the Computer Science & Management faculty at Amrapali University for their academic guidance."
    pq2.font.size = Pt(12)
    pq2.font.color.rgb = TEXT_WHITE
    pq2.space_after = Pt(6)

    pq3 = tf_qa.add_paragraph()
    pq3.text = "💬 The floor is now open for questions, code inspection, and live application demonstration. (Piyush Bhatt)"
    pq3.font.size = Pt(13)
    pq3.font.bold = True
    pq3.font.color.rgb = RGBColor(148, 163, 184)

    add_notes(slide14,
        "In conclusion, we have delivered 100% of the Review 1 rubric criteria: Problem Statement, Quality Objectives, "
        "IEEE 830 SRS, Scope and Roles, Modular Architecture, Database Design, CRUD operations, and a working demo. "
        "I thank my teachers at Amrapali University and invite your questions and live demonstration requests."
    )

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AegisPharm_TQM_Presentation_Piyush_Bhatt.pptx")
    prs.save(output_path)
    print(f"[SUCCESS] PowerPoint generated successfully at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_review1_deck()
