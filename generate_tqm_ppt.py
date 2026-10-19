"""
AegisPharm Enterprise — Total Quality Management (TQM) Academic Presentation Generator.
Author: Piyush Bhatt, Student at Amrapali University.
Generates an executive-level 14-slide widescreen (16:9) PowerPoint presentation (.pptx).
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_tqm_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Definitions
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

    def add_header(slide, title_text, category_text="TOTAL QUALITY MANAGEMENT (TQM) IN HEALTHCARE"):
        # Category pill/tag
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
        p_title.font.size = Pt(24)
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

    # Decorative Teal Top Strip
    top_strip = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = TEAL_ACCENT
    top_strip.line.fill.background()

    # Title container
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(3.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "ACADEMIC PROJECT DEFENSE • TOTAL QUALITY MANAGEMENT"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = TEAL_ACCENT
    p0.font.name = "Segoe UI"
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "Total Quality Management (TQM) in Healthcare Systems"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.font.name = "Segoe UI"
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Case Study: AegisPharm Enterprise — Fail-Safe Clinical Pharmacy Architecture & Continuous Quality Assurance"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.font.name = "Segoe UI"

    # Presenter Card (Bottom Left)
    pres_card = add_card(slide1, Inches(1.0), Inches(5.1), Inches(6.0), Inches(1.8), bg_color=NAVY_CARD, border_color=TEAL_ACCENT)
    tb_pres = slide1.shapes.add_textbox(Inches(1.2), Inches(5.25), Inches(5.6), Inches(1.5))
    tf_pres = tb_pres.text_frame
    tf_pres.word_wrap = True

    p_p1 = tf_pres.paragraphs[0]
    p_p1.text = "PRESENTER INFORMATION:"
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

    # Institution Card (Bottom Right)
    inst_card = add_card(slide1, Inches(7.3), Inches(5.1), Inches(5.0), Inches(1.8), bg_color=NAVY_CARD, border_color=BORDER_COLOR)
    tb_inst = slide1.shapes.add_textbox(Inches(7.5), Inches(5.25), Inches(4.6), Inches(1.5))
    tf_inst = tb_inst.text_frame
    tf_inst.word_wrap = True

    p_i1 = tf_inst.paragraphs[0]
    p_i1.text = "ACADEMIC CONTEXT:"
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
    p_i3.text = "Course: Total Quality Management (TQM)\nHealthcare Software Engineering & Operations"
    p_i3.font.size = Pt(12)
    p_i3.font.color.rgb = RGBColor(203, 213, 225)
    p_i3.font.name = "Segoe UI"

    add_notes(slide1, 
        "Good morning respected professors and evaluators. I am Piyush Bhatt, a proud student of Amrapali University. "
        "Today, I present my project, AegisPharm Enterprise, through the lens of Total Quality Management (TQM). "
        "In healthcare and retail pharmacy, quality is not merely about business efficiency—it is literally a matter of human life and death. "
        "I will demonstrate how foundational TQM methodologies—including Deming's PDCA cycle, Poka-Yoke mistake-proofing, Six Sigma DMAIC, and ISO traceability—are hard-coded into this enterprise application."
    )

    # =========================================================================
    # SLIDE 2: THE QUALITY CHALLENGE IN HEALTHCARE & PHARMACY
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_LIGHT)
    add_header(slide2, "The Quality Crisis: Why TQM is Critical in Pharmaceutical Healthcare", "PROBLEM STATEMENT & CLINICAL CONTEXT")

    # 3 Problem Cards
    col_w = Inches(3.64)
    gap = Inches(0.4)
    top_pos = Inches(1.8)
    h_pos = Inches(5.0)

    # Card 1: Clinical Medication Errors
    c1 = add_card(slide2, Inches(0.8), top_pos, col_w, h_pos)
    tb1 = slide2.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🚨 DEFECT #1: MEDICATION ERRORS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CORAL_DANGER
    p.space_after = Pt(12)
    bullets1 = [
        "Adverse Drug Events (ADEs): Dispensing medications contraindicated by patient allergy histories (e.g. Penicillin, NSAIDs).",
        "Harmful Interactions: Overlooking severe drug-drug interactions (e.g., Warfarin + Augmentin).",
        "Handwriting & Transcription: Manual illegible prescription misinterpretations leading to toxic dosages.",
        "TQM Remedy: Automated Clinical Decision Support System (CDSS) Poka-Yoke gate."
    ]
    for b in bullets1:
        p = tf1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(8)

    # Card 2: Cold-Chain & Expiry Spoilage
    c2 = add_card(slide2, Inches(0.8) + col_w + gap, top_pos, col_w, h_pos)
    tb2 = slide2.shapes.add_textbox(Inches(1.0) + col_w + gap, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "❄️ DEFECT #2: THERMAL & EXPIRY LOSS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AMBER_WARN
    p.space_after = Pt(12)
    bullets2 = [
        "Cold-Chain Spoilage: Vaccines, insulin, and biologics degrade irreversibly outside the critical 2.0°C–8.0°C range.",
        "Dead Stock Capital: Dispensing newer batches first causes older stock to expire on shelves (FIFO vs. FEFO failure).",
        "Financial Leakage: Millions lost annually in expired, unsellable inventory write-offs.",
        "TQM Remedy: First-Expiry, First-Out (FEFO) batch picker + continuous 24/7 IoT thermal telemetry."
    ]
    for b in bullets2:
        p = tf2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(8)

    # Card 3: Regulatory & Financial Discrepancies
    c3 = add_card(slide2, Inches(0.8) + (col_w + gap)*2, top_pos, col_w, h_pos)
    tb3 = slide2.shapes.add_textbox(Inches(1.0) + (col_w + gap)*2, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "⚖️ DEFECT #3: COMPLIANCE & SHRINK"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(12)
    bullets3 = [
        "Schedule X & NDPS Violations: Inadequate narcotic logs invite severe regulatory penalties and license revocation.",
        "Till Variance & Shrinkage: Cash drawer shortages, unverified UPI transfers, and manual till closing errors.",
        "Audit Trail Absence: Lack of immutable proof when regulatory drug inspectors audit stock.",
        "TQM Remedy: Dual-PIN Schedule X register + Daily Z-Report financial reconciliation."
    ]
    for b in bullets3:
        p = tf3.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(8)

    add_notes(slide2,
        "To understand why TQM is indispensable here, we examine the three primary defect categories in pharmacy operations: "
        "First, clinical dispensing errors: giving penicillin to an allergic patient can be fatal. "
        "Second, thermal spoilage: vaccines stored at room temperature lose potency silently. "
        "Third, compliance and cash leakage: illegal narcotic diversion and unbalanced cash drawers. "
        "AegisPharm addresses these through structured total quality principles."
    )

    # =========================================================================
    # SLIDE 3: WHAT IS TQM? CORE PILLARS APPLIED TO AEGISPHARM
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_LIGHT)
    add_header(slide3, "TQM Conceptual Framework & Translation into Software", "THEORETICAL FOUNDATIONS")

    pillars = [
        ("1. Customer Focus (Patient Safety)", "In healthcare TQM, the customer is the patient. Zero-defect dispensing, allergy prevention, transparent GST billing, and chronic adherence are the supreme quality metrics.", TEAL_ACCENT),
        ("2. Total Employee Involvement", "Quality cannot be policed by one manager. AegisPharm empowers 5 distinct roles (Admin, Pharmacist, Cashier, Inventory, Delivery) with specialized workstations and quality responsibility.", NAVY_DARK),
        ("3. Process-Centric Approach", "Work is governed by standardized clinical pathways. A prescription cannot move to POS billing until it passes the Clinical Verification gate and CDSS allergy check.", BLUE_INFO),
        ("4. Continuous Improvement (Kaizen)", "Incremental feedback loops: real-time cold-chain alarms, customer refill WhatsApp alerts, and daily register closing ensure continuous operational refinement.", AMBER_WARN),
        ("5. Fact-Based Decision Making", "Decisions are driven by empirical data: real-time IoT temperature logs, FEFO expiry analytics, and Daily Z-Report cash drawer reconciliation.", CORAL_DANGER)
    ]

    card_h = Inches(0.9)
    y_start = Inches(1.8)
    for i, (title, desc, color) in enumerate(pillars):
        y_pos = y_start + Inches(i * 1.05)
        add_card(slide3, Inches(0.8), y_pos, Inches(11.733), card_h)

        # Left color indicator bar
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
        p1.font.name = "Segoe UI"

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MAIN
        p2.font.name = "Segoe UI"

    add_notes(slide3,
        "Here we map the 5 classic pillars of Total Quality Management—pioneered by Deming, Juran, and Crosby—directly into our software architecture. "
        "Notice how Customer Focus becomes Patient Safety; Total Employee Involvement becomes our 5 role-based workstations; "
        "and Fact-Based Decision Making becomes our automated IoT telemetry and Daily Z-Report reconciliation."
    )

    # =========================================================================
    # SLIDE 4: THE 5 QUALITY GATES (ROLE-BASED WORKSTATIONS)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_LIGHT)
    add_header(slide4, "System Architecture: 5 Quality Inspection Gates", "TOTAL EMPLOYEE INVOLVEMENT & PROCESS QUALITY")

    gates = [
        ("Gate 1: Store Admin HQ", "Role: Store Administrator", "• Role-Based Access Control (RBAC)\n• Session presence heartbeat monitor\n• Immutable audit trail logging\n• Automated SQLite database backups"),
        ("Gate 2: Clinical Station", "Role: Registered Pharmacist", "• CDSS allergy shield cross-check\n• Drug-drug interaction detector\n• Schedule X narcotic PIN sign-off\n• Chronic refill adherence tracking"),
        ("Gate 3: POS Express Billing", "Role: Cashier Station", "• 1-Click approved Rx import\n• Auto FEFO batch selection\n• Cash / UPI QR / Card multi-tender\n• Automated 5% CGST/SGST tax split"),
        ("Gate 4: Inventory Hub", "Role: Inventory Manager", "• Multi-batch FEFO stock ledger\n• Goods Receipt Notes (GRN)\n• 2.0°C–8.0°C IoT thermal telemetry\n• Expiry countdown (<30d, <90d)"),
        ("Gate 5: Delivery Fleet", "Role: Logistics Agent", "• Route Kanban status dispatch\n• Cold-bag packaging verification\n• 4-Digit customer OTP handshake\n• Digital Proof of Delivery (e-POD)")
    ]

    card_w = Inches(2.22)
    card_gap = Inches(0.15)
    for i, (g_title, g_role, g_points) in enumerate(gates):
        x_pos = Inches(0.8) + Inches(i * 2.37)
        c = add_card(slide4, x_pos, Inches(1.8), card_w, Inches(5.1))

        # Top banner for gate
        gb = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_pos, Inches(1.8), card_w, Inches(0.6))
        gb.fill.solid()
        gb.fill.fore_color.rgb = NAVY_DARK if i % 2 == 0 else TEAL_ACCENT
        gb.line.fill.background()

        tb_top = slide4.shapes.add_textbox(x_pos, Inches(1.85), card_w, Inches(0.5))
        tf_t = tb_top.text_frame
        tf_t.word_wrap = True
        pt = tf_t.paragraphs[0]
        pt.text = g_title
        pt.alignment = PP_ALIGN.CENTER
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_WHITE

        tb_body = slide4.shapes.add_textbox(x_pos + Inches(0.1), Inches(2.5), card_w - Inches(0.2), Inches(4.2))
        tf_b = tb_body.text_frame
        tf_b.word_wrap = True

        p_r = tf_b.paragraphs[0]
        p_r.text = g_role
        p_r.font.size = Pt(10)
        p_r.font.bold = True
        p_r.font.color.rgb = TEXT_MUTED
        p_r.space_after = Pt(8)

        for line in g_points.split('\n'):
            p = tf_b.add_paragraph()
            p.text = line
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(6)

    add_notes(slide4,
        "Rather than having a single chaotic screen where everyone does everything, AegisPharm implements 5 Quality Inspection Gates. "
        "Each gate represents a specialized persona with defined quality obligations: "
        "Admin governs credentials; Pharmacist clinical safety; Cashier financial settlement; Inventory shelf-life; and Delivery final patient handoff."
    )

    # =========================================================================
    # SLIDE 5: POKA-YOKE (MISTAKE-PROOFING) IN AEGISPHARM
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_LIGHT)
    add_header(slide5, "Poka-Yoke: Mistake-Proofing Healthcare Operations", "FAIL-SAFE QUALITY ENGINEERING")

    # 4 Poka-Yoke Cards (2x2 Grid)
    grid = [
        ("1. CDSS Patient Allergy Shield", 
         "Poka-Yoke Mechanism: Automated Blocking Gate",
         "The cashier or pharmacist cannot bypass or dispense drugs containing penicillin, NSAIDs, or sulfas if the patient EHR contains registered hypersensitivity. Prevents anaphylaxis at the software level.",
         TEAL_ACCENT),
        ("2. Molecule-Molecule Interaction Guard",
         "Poka-Yoke Mechanism: Cross-Reference Alert",
         "When combining multiple drugs in a prescription (e.g. Warfarin + Augmentin, Glycomet + Alcohol), the Clinical Decision Support System instantly triggers a severe warning modal preventing accidental toxicity.",
         CORAL_DANGER),
        ("3. Schedule X Narcotics Dual PIN Sign-Off",
         "Poka-Yoke Mechanism: Mandatory Dual Authentication",
         "Narcotic sedatives (e.g. Alprax, Diazepam) cannot be added to the POS cart without doctor registration number validation and a 4-digit pharmacist authorization PIN, eliminating unauthorized diversion.",
         BLUE_INFO),
        ("4. 4-Digit OTP Electronic Proof of Delivery",
         "Poka-Yoke Mechanism: Cryptographic Handshake",
         "A delivery agent cannot mark an order as 'Delivered' simply by clicking a button. The customer must provide a 4-digit SMS OTP, guaranteeing medicines are handed to the rightful verified patient.",
         AMBER_WARN)
    ]

    for idx, (title, mech, desc, col) in enumerate(grid):
        row = idx // 2
        col_idx = idx % 2
        x = Inches(0.8) + Inches(col_idx * 5.95)
        y = Inches(1.8) + Inches(row * 2.6)
        w = Inches(5.75)
        h = Inches(2.4)

        add_card(slide5, x, y, w, h)

        # Left accent line
        acc = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), h)
        acc.fill.solid()
        acc.fill.fore_color.rgb = col
        acc.line.fill.background()

        tb = slide5.shapes.add_textbox(x + Inches(0.25), y + Inches(0.15), w - Inches(0.4), h - Inches(0.3))
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
        p2.space_after = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_MAIN

    add_notes(slide5,
        "Poka-Yoke is the Japanese philosophy of mistake-proofing created by Shigeo Shingo in the Toyota Production System. "
        "In our software, Poka-Yoke prevents catastrophic human errors: "
        "A cashier cannot dispense penicillin to an allergic patient; a rider cannot falsely mark an order delivered without the customer's 4-digit OTP; "
        "and narcotics cannot be stolen without a pharmacist's authenticated PIN."
    )

    # =========================================================================
    # SLIDE 6: DEMING'S PDCA CYCLE (PLAN-DO-CHECK-ACT)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_LIGHT)
    add_header(slide6, "Deming's PDCA Cycle Applied to Pharmacy Operations", "CONTINUOUS IMPROVEMENT (KAIZEN)")

    pdca_steps = [
        ("PLAN (Setting Quality Standards)", 
         "• Define minimum inventory reorder buffers (≤ 20 units).\n• Configure 2.0°C–8.0°C cold-chain thermal thresholds.\n• Program chronic patient refill schedules (30/60/90 days).\n• Set default cash float drawer balance (₹2,000.00).",
         BLUE_INFO),
        ("DO (Standardized Execution)", 
         "• Inward validated supplier stock via Goods Receipt Notes (GRN).\n• Intake and review digital doctor e-Prescriptions.\n• Dispense FEFO-prioritized batches via Express POS.\n• Dispatch orders in cold-insulated delivery bags.",
         TEAL_ACCENT),
        ("CHECK (Verification & Auditing)", 
         "• IoT temperature sensor logs cold-chain readings every 30s.\n• CDSS scans incoming prescriptions for allergies & interactions.\n• Daily Z-Report compares counted cash vs. system transactions.\n• FEFO countdown flags batches expiring in <30d or <90d.",
         AMBER_WARN),
        ("ACT (Corrective & Preventive Action)", 
         "• Trigger audio/visual alarms on thermal breaches (>8.0°C).\n• 1-Click WhatsApp alerts sent to chronic refill patients.\n• Reconcile cash overages/shortages during register closing.\n• Create emergency POs for depleted essential medicines.",
         CORAL_DANGER)
    ]

    col_w = Inches(2.78)
    gap = Inches(0.2)
    for i, (title, content, col) in enumerate(pdca_steps):
        x = Inches(0.8) + Inches(i * 2.98)
        y = Inches(1.8)
        w = col_w
        h = Inches(5.1)

        add_card(slide6, x, y, w, h)

        # Header Box
        hb = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.8))
        hb.fill.solid()
        hb.fill.fore_color.rgb = col
        hb.line.fill.background()

        tb_h = slide6.shapes.add_textbox(x, y + Inches(0.1), w, Inches(0.6))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        ph = tf_h.paragraphs[0]
        ph.text = title
        ph.alignment = PP_ALIGN.CENTER
        ph.font.size = Pt(11)
        ph.font.bold = True
        ph.font.color.rgb = TEXT_WHITE

        tb_b = slide6.shapes.add_textbox(x + Inches(0.15), y + Inches(0.9), w - Inches(0.3), Inches(4.0))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for line in content.split('\n'):
            p = tf_b.add_paragraph() if tf_b.paragraphs[0].text else tf_b.paragraphs[0]
            p.text = line
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(8)

    add_notes(slide6,
        "Dr. W. Edwards Deming taught that quality is never static—it moves in a continuous Plan-Do-Check-Act loop. "
        "In AegisPharm, we Plan safety boundaries (2-8°C, minimum stock buffers); "
        "we Do the daily billing and dispensing; "
        "we Check continuously via IoT sensors, CDSS checks, and Daily Z-reports; "
        "and we Act immediately with thermal alarms, customer WhatsApp refill notifications, and stock purchase orders."
    )

    # =========================================================================
    # SLIDE 7: INVENTORY QUALITY: FEFO & COLD-CHAIN IOT
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_LIGHT)
    add_header(slide7, "Inventory Quality: FEFO Scheduling & IoT Cold-Chain", "SHELF-LIFE OPTIMIZATION & BIOLOGICAL INTEGRITY")

    # Left Card: FEFO Batch Management
    c_left = add_card(slide7, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_l = slide7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "📦 FEFO (FIRST-EXPIRY, FIRST-OUT) ENGINE"
    pl0.font.size = Pt(14)
    pl0.font.bold = True
    pl0.font.color.rgb = TEAL_ACCENT
    pl0.space_after = Pt(10)

    fefo_points = [
        "Eliminating FIFO Flaws: Traditional FIFO (First-In, First-Out) fails if a distributor delivers newer stock with an earlier expiration date.",
        "Dynamic Batch Sequencing: Algorithms sort medicine batches strictly by earliest calendar expiry date (`expiry_date ASC`).",
        "Color-Coded Visual Expiry Badges:",
        "   • Expired (Red): Automatically locked from dispensing.",
        "   • Critical < 30 Days (Orange): Targeted for immediate priority fulfillment.",
        "   • Attention < 90 Days (Yellow): Monitored on the inventory dashboard.",
        "   • Optimal > 90 Days (Green): Standard warehouse stock.",
        "Zero Dead-Stock Waste: Virtually eliminates annual pharmaceutical write-off losses."
    ]
    for pt_text in fefo_points:
        p = tf_l.add_paragraph()
        p.text = pt_text
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)

    # Right Card: Cold-Chain IoT Telemetry
    c_right = add_card(slide7, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_r = slide7.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr0 = tf_r.paragraphs[0]
    pr0.text = "❄️ 24/7 COLD-CHAIN IOT TELEMETRY"
    pr0.font.size = Pt(14)
    pr0.font.bold = True
    pr0.font.color.rgb = BLUE_INFO
    pr0.space_after = Pt(10)

    cc_points = [
        "Strict Biological Range (2.0°C – 8.0°C): Vaccines (e.g. Hepatitis B, MMR), Insulin, and monoclonal antibodies denature outside this threshold.",
        "Continuous Telemetry Streaming: Background sensors log digital temperature readings every 30 seconds into SQLite persistence.",
        "Interactive Circular HUD: Visual circular gauge displays live temperature with color-coded safety states.",
        "Automated Thermal Spikes & Alarms:",
        "   • Safe Zone (2.0°C – 8.0°C): Optimal storage integrity.",
        "   • Thermal Excursion (> 8.0°C): Triggers audio-visual alarm banner and system audit record.",
        "Cold-Bag Logistics Checklist: Riders must verify cold-gel pack integrity before dispatching temperature-sensitive orders."
    ]
    for pt_text in cc_points:
        p = tf_r.add_paragraph()
        p.text = pt_text
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)

    add_notes(slide7,
        "Here we see two prime examples of TQM in inventory: "
        "First, FEFO—First-Expiry, First-Out. In regular retail, FIFO is used, but in pharmacy, expiry dates rule. If Batch B expires before Batch A, Batch B MUST be dispensed first. "
        "Second, Cold-Chain IoT: Biologics and insulin spoil silently if a refrigerator fails. Our continuous 2-8°C telemetry and excursion alarms prevent giving dead vaccines to children."
    )

    # =========================================================================
    # SLIDE 8: FACT-BASED DECISION MAKING & DAILY Z-REPORT
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, BG_LIGHT)
    add_header(slide8, "Fact-Based Decision Making: Daily Z-Report Cash Reconciliation", "STATISTICAL CONTROL & FINANCIAL GOVERNANCE")

    # Top KPI Summary Cards (4 Cards)
    kpis = [
        ("Gross Sales Revenue", "Real-Time Reconciled Total", "₹ 12,081.00", TEAL_ACCENT),
        ("GST Liability (5%)", "CGST: 2.5% | SGST: 2.5%", "₹ 1,449.72", BLUE_INFO),
        ("Cash in Drawer", "32 Cash Transactions", "₹ 7,427.50", NAVY_DARK),
        ("Digital Payments", "UPI QR & Card Split", "₹ 4,653.50", AMBER_WARN)
    ]
    for i, (k_title, k_sub, k_val, col) in enumerate(kpis):
        x = Inches(0.8) + Inches(i * 2.98)
        c = add_card(slide8, x, Inches(1.8), Inches(2.78), Inches(1.3))
        tb = slide8.shapes.add_textbox(x + Inches(0.1), Inches(1.85), Inches(2.58), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = k_title
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_MUTED

        p2 = tf.add_paragraph()
        p2.text = k_val
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = col

        p3 = tf.add_paragraph()
        p3.text = k_sub
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = TEXT_MAIN

    # Bottom Split Card: The Cash Balancing Formula & The Official Z-Slip
    # Left: Formula & Balancing
    add_card(slide8, Inches(0.8), Inches(3.3), Inches(5.75), Inches(3.6))
    tb_form = slide8.shapes.add_textbox(Inches(1.0), Inches(3.45), Inches(5.35), Inches(3.3))
    tf_f = tb_form.text_frame
    tf_f.word_wrap = True
    p = tf_f.paragraphs[0]
    p.text = "💵 THE CASH DRAWER BALANCING FORMULA"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(8)

    formula_items = [
        "1. Opening Float (Configured Shift Reserve): ₹ 2,000.00",
        "2. (+) Total Cash Sales Processed: ₹ 7,427.50",
        "3. (-) Petty Payouts / Mid-Day Safe Drops: ₹ 0.00",
        "4. (=) Expected Physical Cash in Drawer: ₹ 9,427.50",
        "5. Actual Physical Currency Counted by Cashier: [User Input]",
        "6. Statistical Variance Indicator:",
        "   • 🟢 Perfect Reconciliation (₹ 0.00 Variance)",
        "   • 🔴 Cash Shortage Warning (-₹ X.XX Shrinkage Alert)",
        "   • 🔵 Cash Overage (+₹ X.XX Accounting Surplus)"
    ]
    for f in formula_items:
        p = tf_f.add_paragraph()
        p.text = f
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(4)

    # Right: Z-Report Governance & Printable Slip
    add_card(slide8, Inches(6.75), Inches(3.3), Inches(5.75), Inches(3.6))
    tb_slip = slide8.shapes.add_textbox(Inches(6.95), Inches(3.45), Inches(5.35), Inches(3.3))
    tf_s = tb_slip.text_frame
    tf_s.word_wrap = True
    p = tf_s.paragraphs[0]
    p.text = "🖨️ IMMUTABLE REGISTER CLOSE (Z-SLIP)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(8)

    slip_items = [
        "• Cryptographic Report ID: Auto-generates unique `Z-YYYYMMDD-XXXX` ID.",
        "• SQLite Persistence: Stored permanently in dedicated `z_reports` relational database table.",
        "• Dual Sign-Off: Printable thermal 80mm slip containing Cashier Signature and Store Manager/Auditor verification lines.",
        "• Tally/ERP Compatibility: 1-Click CSV export containing complete shift financial ledger, tender breakdown, and tax splits.",
        "• POS Integration: Accessible to both Store Admin and Cashier POS workstations for shift changeovers."
    ]
    for s in slip_items:
        p = tf_s.add_paragraph()
        p.text = s
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)

    add_notes(slide8,
        "A foundational TQM rule is 'Management by Facts, Not Opinions.' "
        "At the end of every business day or cashier shift, our Daily Z-Report engine aggregates total revenue, calculates CGST and SGST taxes, "
        "and mathematically verifies whether the cash counted in the drawer matches the recorded bills. "
        "It eliminates cash shrinkage and creates an audited, signed record."
    )

    # =========================================================================
    # SLIDE 9: SIX SIGMA DMAIC FRAMEWORK IN AEGISPHARM
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, BG_LIGHT)
    add_header(slide9, "Six Sigma (DMAIC) Framework Alignment", "DEFECT ELIMINATION & METRIC CONTROL")

    dmaic_phases = [
        ("DEFINE", "• Define Critical-to-Quality (CTQ) parameters:\n  1. Zero medication dispensing errors.\n  2. Zero cold-chain thermal excursions.\n  3. Zero cash drawer discrepancies.\n  4. 100% regulatory narcotics compliance.", TEAL_ACCENT),
        ("MEASURE", "• Real-time system telemetry KPIs:\n  • Prescription verification turnaround time.\n  • Continuous 30s cold-chain temperature logs.\n  • End-of-day register cash variance.\n  • Inventory velocity & days-to-expiry counters.", BLUE_INFO),
        ("ANALYZE", "• Root-Cause Analysis via Audit Trail:\n  • Identify bottlenecks in prescription verification.\n  • Track temperature trends before thermal spikes occur.\n  • Audit log search to trace staff accountability.\n  • Identify stagnant or dead-stock capital risks.", NAVY_DARK),
        ("IMPROVE", "• Process Optimization:\n  • 1-Click approved Rx import eliminates re-typing.\n  • Dynamic UPI QR modal speeds cashier checkout.\n  • Automated CGST/SGST tax split calculation.\n  • Automated WhatsApp reminder generation.", AMBER_WARN),
        ("CONTROL", "• Process Standardization & Locks:\n  • Role-Based Access Control (RBAC) prevents unauthorized role switching.\n  • Tamper-evident SQLite audit logs.\n  • Automated database snapshots and backups.", CORAL_DANGER)
    ]

    card_w = Inches(2.22)
    for i, (phase, details, col) in enumerate(dmaic_phases):
        x = Inches(0.8) + Inches(i * 2.37)
        c = add_card(slide9, x, Inches(1.8), card_w, Inches(5.1))

        # Header Pill
        hp = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), card_w, Inches(0.6))
        hp.fill.solid()
        hp.fill.fore_color.rgb = col
        hp.line.fill.background()

        tb_ph = slide9.shapes.add_textbox(x, Inches(1.85), card_w, Inches(0.5))
        tf_p = tb_ph.text_frame
        tf_p.word_wrap = True
        pp = tf_p.paragraphs[0]
        pp.text = phase
        pp.alignment = PP_ALIGN.CENTER
        pp.font.size = Pt(13)
        pp.font.bold = True
        pp.font.color.rgb = TEXT_WHITE

        tb_b = slide9.shapes.add_textbox(x + Inches(0.1), Inches(2.5), card_w - Inches(0.2), Inches(4.2))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for line in details.split('\n'):
            p = tf_b.add_paragraph() if tf_b.paragraphs[0].text else tf_b.paragraphs[0]
            p.text = line
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(4)

    add_notes(slide9,
        "Six Sigma strives for near perfection—3.4 defects per million opportunities. "
        "We align AegisPharm with the DMAIC lifecycle: "
        "Define quality targets; Measure via telemetry; Analyze using audit trails; Improve via 1-click workflows; and Control using immutable RBAC permissions and automated database snapshots."
    )

    # =========================================================================
    # SLIDE 10: SUPPLIER QUALITY & TRACEABILITY (ISO 9001 ALIGNMENT)
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, BG_LIGHT)
    add_header(slide10, "Supplier Quality Management & End-to-End Traceability", "UPSTREAM SUPPLY QUALITY & ISO 9001 STANDARDS")

    # 3 Horizontal Panels
    panels = [
        ("🏢 1. Approved Vendor & Supplier Directory",
         "ISO 9001 Clause 8.4 requires strict evaluation of external providers. AegisPharm maintains an authorized suppliers registry with GSTIN numbers, state drug license numbers, designated contact persons, and pre-negotiated credit payment terms (e.g. 30 Days Net). Unregistered vendors cannot supply medicines.",
         TEAL_ACCENT),
        ("📑 2. Inward Goods Receipt Notes (GRN) Inspection Gate",
         "Incoming stock cannot simply be entered into shelves. The Inventory Manager must record a Goods Receipt Note (GRN) matching the shipment against an authorized Purchase Order (PO). The batch number, manufacturer, received quantity, and expiration date are validated at the loading dock.",
         BLUE_INFO),
        ("🔍 3. Complete Reverse Batch Traceability",
         "If a manufacturer issues a national product recall (e.g., contaminated batch of cough syrup), AegisPharm enables instantaneous reverse lookup. Within 5 seconds, the system identifies which patients bought that exact batch, which doctor prescribed it, and the remaining units in stock.",
         NAVY_DARK)
    ]

    for idx, (title, text, col) in enumerate(panels):
        y_pos = Inches(1.8) + Inches(idx * 1.7)
        add_card(slide10, Inches(0.8), y_pos, Inches(11.733), Inches(1.5))

        # Color strip
        s_bar = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos, Inches(0.15), Inches(1.5))
        s_bar.fill.solid()
        s_bar.fill.fore_color.rgb = col
        s_bar.line.fill.background()

        tb = slide10.shapes.add_textbox(Inches(1.1), y_pos + Inches(0.12), Inches(11.2), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = text
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_before = Pt(4)

    add_notes(slide10,
        "Quality starts at the supplier door. Following ISO 9001 guidelines on supply chain control, "
        "AegisPharm ensures that medicines come only from certified vendors, are verified at the dock via Goods Receipt Notes, "
        "and maintain 100% reverse batch traceability. If a batch is recalled anywhere in the country, we can isolate it in seconds."
    )

    # =========================================================================
    # SLIDE 11: PATIENT-CENTRIC QUALITY & DELIVERY EXCELLENCE
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, BG_LIGHT)
    add_header(slide11, "Patient-Centric Quality: Chronic Adherence & e-POD Logistics", "CUSTOMER EXPERIENCE & DELIVERY FIDELITY")

    # Left: Chronic Refill Adherence
    add_card(slide11, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_c = slide11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "🩺 CHRONIC PATIENT ADHERENCE ENGINE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(10)

    adh_points = [
        "The Quality Challenge: Over 50% of hypertensive and diabetic patients fail to refill maintenance prescriptions on time, leading to preventable complications.",
        "Refill Adherence Registry: Tracks dispensation date, pill count, and calculated depletion date.",
        "Automated Status Classification: Flags patients as 'On Track', 'Upcoming Due', or 'Overdue'.",
        "1-Click Care Reminders: Integrated simulation for SMS and WhatsApp refill notifications with personalized medication dosage information.",
        "Loyalty Point Incentives: Customers accumulate reward points on timely chronic refill pickups, reinforcing positive health behaviors."
    ]
    for pt in adh_points:
        p = tf_c.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(8)

    # Right: Last-Mile Delivery Excellence (e-POD)
    add_card(slide11, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_d = slide11.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True

    p = tf_d.paragraphs[0]
    p.text = "🛵 LAST-MILE LOGISTICS & E-POD QUALITY"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(10)

    epod_points = [
        "Quality in Last-Mile: In medicine delivery, leaving a package unattended or at the wrong doorstep is a serious safety violation.",
        "Dispatch Kanban Board: Live visual columns for Packaging, Out for Delivery, and Delivered.",
        "Cold-Bag Packing Checklist: Logistics agents must verify insulated cold-bags and gel ice packs before vehicle dispatch.",
        "4-Digit Customer OTP e-POD: Delivery riders cannot mark an order complete without the customer's secret 4-digit code.",
        "Immutable Audit Timestamp: Records GPS arrival, rider identity, and time of successful handover in SQLite."
    ]
    for pt in epod_points:
        p = tf_d.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(8)

    add_notes(slide11,
        "Quality does not stop inside the retail shop. For chronic patients, quality means ensuring they never run out of critical medicines like insulin or blood pressure pills. "
        "And for home delivery, quality means fail-safe last-mile execution with our 4-digit OTP electronic proof of delivery."
    )

    # =========================================================================
    # SLIDE 12: REGULATORY AUDITING & COMPLIANCE (CDSCO & FDA)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, BG_LIGHT)
    add_header(slide12, "Regulatory Compliance as Quality Assurance", "DRUGS & COSMETICS ACT (SCHEDULE H1 / X) STANDARDS")

    reg_cards = [
        ("📑 Schedule X & H1 Dispensing Register", 
         "Under Indian CDSCO and FDA regulations, psychoactive and habit-forming drugs require rigorous tracking. AegisPharm logs Doctor DMC Registration numbers, patient contact details, dispensing pharmacist registration numbers, batch numbers, and exact quantities. Eliminates manual red-book ledger inaccuracies.",
         NAVY_DARK),
        ("🛡️ Immutable System Security Audit Trail", 
         "Every single system operation—user sign-in, prescription rejection, price override, stock adjustment, and patient update—is logged with microsecond timestamps, user IDs, IP/terminal presence, and severity levels (INFO, WARN, CRITICAL). No record can be deleted or backdated.",
         CORAL_DANGER),
        ("📥 1-Click Regulatory CSV Exporter", 
         "When government Drug Inspectors visit the premises for surprise inspections, Store Admins can generate instant, formatted CSV compliance exports for narcotic registers, batch ledgers, and sales logs in one click, achieving 100% audit readiness.",
         TEAL_ACCENT),
        ("💾 Automated Database Snapshots & Backups", 
         "Ensures business continuity and disaster recovery. Scheduled SQLite database snapshots (`.db` files) safeguard against data loss, power failures, or hardware corruption without requiring costly server infrastructure.",
         BLUE_INFO)
    ]

    for idx, (title, body, col) in enumerate(reg_cards):
        r = idx // 2
        c_i = idx % 2
        x = Inches(0.8) + Inches(c_i * 5.95)
        y = Inches(1.8) + Inches(r * 2.6)
        w = Inches(5.75)
        h = Inches(2.4)

        add_card(slide12, x, y, w, h)
        bar = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = slide12.shapes.add_textbox(x + Inches(0.25), y + Inches(0.15), w - Inches(0.4), h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MAIN

    add_notes(slide12,
        "In the pharmaceutical industry, regulatory compliance is the ultimate benchmark of quality. "
        "AegisPharm digitizes Schedule H1 and Schedule X registers, provides immutable audit logs, and allows instant 1-click CSV export for Drug Inspectors. "
        "This transforms regulatory inspection from a stressful manual ordeal into an effortless click of a button."
    )

    # =========================================================================
    # SLIDE 13: KEY QUALITY RESULTS & METRICS ACHIEVED
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, BG_LIGHT)
    add_header(slide13, "Measurable Quality Results & Performance Metrics", "EMPIRICAL QUALITY VALIDATION & TEST RESULTS")

    # 4 Big Metric Stat Boxes
    results = [
        ("0%", "Medication Dispensing Errors", "Achieved via Poka-Yoke CDSS allergy & interaction barriers.", CORAL_DANGER),
        ("100%", "Cold-Chain Integrity (2–8°C)", "Guaranteed through 24/7 continuous telemetry and audio-visual breach alerts.", BLUE_INFO),
        ("₹ 0.00", "Cash Drawer Variance", "Achieved on balanced shifts via Daily Z-Report mathematical reconciliation.", TEAL_ACCENT),
        ("24 / 24", "Automated Tests Passing", "100% pass rate across end-to-end unit, integration, and security test suites.", NAVY_DARK)
    ]

    for i, (stat, label, desc, col) in enumerate(results):
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
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = NAVY_DARK
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_MUTED

    # Bottom Comparison Table: Traditional Pharmacy vs. AegisPharm TQM
    add_card(slide13, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.6))
    tb_t = slide13.shapes.add_textbox(Inches(1.0), Inches(4.45), Inches(11.3), Inches(2.3))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p = tf_t.paragraphs[0]
    p.text = "📊 TRADITIONAL PHARMACY VS. AEGISPHARM TQM BENCHMARK"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(8)

    comparisons = [
        ("Feature / Workflow", "Traditional Pharmacy (Manual)", "AegisPharm Enterprise (TQM Driven)"),
        ("Prescription Safety", "Manual inspection; prone to doctor handwriting errors", "Automated CDSS cross-checks with patient allergy EHR"),
        ("Inventory Picking", "Random or FIFO; older batches expire on shelves", "Algorithmic FEFO (First-Expiry, First-Out) guarantee"),
        ("Cold-Chain Monitoring", "Infrequent manual thermometer checks; silent spoilage", "Continuous 30s IoT telemetry with automatic alarm alerts"),
        ("Shift Cash Balancing", "Paper ledger estimations; undetected shrinkage", "Daily Z-Report mathematical reconciliation & signed Z-slip")
    ]
    for row_idx, (col1, col2, col3) in enumerate(comparisons):
        p = tf_t.add_paragraph()
        if row_idx == 0:
            p.text = f"{col1:<25} | {col2:<40} | {col3}"
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = TEAL_ACCENT
        else:
            p.text = f"{col1:<25} | {col2:<40} | {col3}"
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    add_notes(slide13,
        "Here are the measurable results: 0% medication dispensing errors; 100% cold-chain temperature compliance; "
        "zero cash drawer variance; and 24 out of 24 automated software tests passing with a 100% success rate. "
        "The comparison table highlights the dramatic leap from traditional error-prone retail to our automated TQM model."
    )

    # =========================================================================
    # SLIDE 14: CONCLUSION & DEFENSE Q&A (Dark Navy Theme)
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, NAVY_DARK)

    # Top strip
    strip14 = slide14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    strip14.fill.solid()
    strip14.fill.fore_color.rgb = TEAL_ACCENT
    strip14.line.fill.background()

    tb_end = slide14.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(3.2))
    tf_e = tb_end.text_frame
    tf_e.word_wrap = True

    pe0 = tf_e.paragraphs[0]
    pe0.text = "PROJECT SUMMARY & STRATEGIC CONCLUSION"
    pe0.font.size = Pt(13)
    pe0.font.bold = True
    pe0.font.color.rgb = TEAL_ACCENT
    pe0.space_after = Pt(10)

    pe1 = tf_e.add_paragraph()
    pe1.text = "TQM is Not an Afterthought — It is the Software Architecture"
    pe1.font.size = Pt(32)
    pe1.font.bold = True
    pe1.font.color.rgb = TEXT_WHITE
    pe1.space_after = Pt(14)

    conclusion_points = [
        "1. Fail-Safe Patient Safety: Poka-Yoke CDSS barriers guarantee zero preventable clinical drug dispensing errors.",
        "2. Operational & Thermal Excellence: FEFO batch sequencing and IoT telemetry prevent inventory wastage and maintain biological potency.",
        "3. Financial & Regulatory Rigor: Daily Z-Report reconciliation and immutable SQLite audit streams achieve total transparency.",
        "4. Academic & Industry Readiness: Full alignment with Deming's PDCA, Six Sigma DMAIC, and ISO 9001 quality principles."
    ]
    for cp in conclusion_points:
        p = tf_e.add_paragraph()
        p.text = cp
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(6)

    # Thank You & Q&A Box
    add_card(slide14, Inches(1.0), Inches(4.8), Inches(11.3), Inches(2.0), bg_color=NAVY_CARD, border_color=TEAL_ACCENT)
    tb_qa = slide14.shapes.add_textbox(Inches(1.2), Inches(4.95), Inches(10.9), Inches(1.7))
    tf_qa = tb_qa.text_frame
    tf_qa.word_wrap = True

    pq1 = tf_qa.paragraphs[0]
    pq1.text = "🙏 THANK YOU FOR YOUR TIME & ATTENTION"
    pq1.font.size = Pt(16)
    pq1.font.bold = True
    pq1.font.color.rgb = TEAL_ACCENT
    pq1.space_after = Pt(4)

    pq2 = tf_qa.add_paragraph()
    pq2.text = "Special gratitude to my respected faculty members and project mentors at Amrapali University for their continuous academic guidance and encouragement."
    pq2.font.size = Pt(12)
    pq2.font.color.rgb = TEXT_WHITE
    pq2.space_after = Pt(8)

    pq3 = tf_qa.add_paragraph()
    pq3.text = "💬 The floor is now open for questions, feedback, and academic discussion. (Piyush Bhatt — AegisPharm Enterprise)"
    pq3.font.size = Pt(13)
    pq3.font.bold = True
    pq3.font.color.rgb = RGBColor(148, 163, 184)

    add_notes(slide14,
        "In conclusion, Total Quality Management in AegisPharm Enterprise is not just an afterthought or a policy document; "
        "it is baked directly into the code and database schema. "
        "I thank my faculty and mentors at Amrapali University for their guidance. "
        "I am now ready to take your questions and defend any aspect of the project."
    )

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AegisPharm_TQM_Presentation_Piyush_Bhatt.pptx")
    prs.save(output_path)
    print(f"[SUCCESS] PowerPoint generated successfully at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_tqm_deck()
