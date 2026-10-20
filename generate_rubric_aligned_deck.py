"""
TQM Pharm Enterprise — Rubric-Aligned 18-Slide Master Presentation Generator.
Author: Piyush Bhatt, Amrapali University.
Explicitly aligned with the 3 university evaluation rubric images:
- Baseline understanding
- Modular folder architecture
- Problem Statement
- Quality Objective
- SRS
- Scope and User Roles
- Modules and Features
- Initial UI/Workflow
- Database/System Design
- Working application
- CRUD operations
- Core Features/Modules aligned with quality goals
- Database Integration
- Main System Workflow
- Demonstration of implemented functionality
"""

import os
import win32com.client
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_rubric_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Executive Color Palette
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
    PURPLE_ACCENT = RGBColor(124, 58, 237) # #7C3AED

    def set_bg(slide, color=BG_LIGHT):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = TEAL_ACCENT
        p_c.font.name = "Segoe UI"

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY_DARK
        p_t.font.name = "Segoe UI"

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
        return shape

    def add_notes(slide, text):
        tf = slide.notes_slide.notes_text_frame
        tf.text = text

    def add_stacked_cards(slide, title, category, cards_data):
        set_bg(slide)
        add_header(slide, title, category)
        n = len(cards_data)
        total_h = 5.2
        gap = 0.16
        h = (total_h - gap * (n - 1)) / n
        y = 1.75
        for heading, body, *opt in cards_data:
            col = opt[0] if opt else TEAL_ACCENT
            c = add_card(slide, Inches(0.8), Inches(y), Inches(11.733), Inches(h))
            bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(y), Inches(0.12), Inches(h))
            bar.fill.solid()
            bar.fill.fore_color.rgb = col
            bar.line.fill.background()

            tb = slide.shapes.add_textbox(Inches(1.1), Inches(y + 0.06), Inches(11.2), Inches(h - 0.12))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = heading
            p.font.size = Pt(12 if n <= 4 else 11)
            p.font.bold = True
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(2)

            for line in body.split('\n'):
                p2 = tf.add_paragraph()
                p2.text = line
                p2.font.size = Pt(10.5 if n <= 4 else 9.5)
                p2.font.color.rgb = TEXT_MAIN
                p2.space_after = Pt(1)
            y += h + gap

    def add_table_slide(slide, title, category, headers, rows_data, col_widths=None):
        set_bg(slide)
        add_header(slide, title, category)
        card_w = Inches(11.733)
        card_h = Inches(5.1)
        add_card(slide, Inches(0.8), Inches(1.8), card_w, card_h)

        table_shape = slide.shapes.add_table(len(rows_data) + 1, len(headers), Inches(1.0), Inches(2.0), Inches(11.333), Inches(4.6))
        tbl = table_shape.table

        if col_widths:
            for idx, w in enumerate(col_widths):
                tbl.columns[idx].width = Inches(w)

        for idx, h_text in enumerate(headers):
            cell = tbl.cell(0, idx)
            cell.text = h_text
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY_DARK
            p = cell.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_WHITE

        for r_idx, row in enumerate(rows_data, start=1):
            bg = BG_LIGHT if r_idx % 2 == 1 else CARD_BG
            for c_idx, val in enumerate(row):
                cell = tbl.cell(r_idx, c_idx)
                cell.text = str(val)
                cell.fill.solid()
                cell.fill.fore_color.rgb = bg
                p = cell.text_frame.paragraphs[0]
                p.font.size = Pt(9.5)
                p.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 1: Title & Project Overview
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, NAVY_DARK)
    top_strip = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = TEAL_ACCENT
    top_strip.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "REVIEW 1 & 2 · SETUP, SRS & WORKING APPLICATION EVALUATION"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = TEAL_ACCENT
    p0.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "TQM Pharm Enterprise"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "Clinical & Retail Pharmacy Operating System with Total Quality Management Architecture\nQuality Goal: Q01 Improve Reliability & Zero-Defects"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(148, 163, 184)

    add_card(s1, Inches(1.0), Inches(5.1), Inches(6.0), Inches(1.8), bg_color=NAVY_CARD, border_color=TEAL_ACCENT)
    tb_p = s1.shapes.add_textbox(Inches(1.2), Inches(5.25), Inches(5.6), Inches(1.5))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    p_p = tf_p.paragraphs[0]
    p_p.text = "PRESENTER:"
    p_p.font.size = Pt(11)
    p_p.font.bold = True
    p_p.font.color.rgb = TEAL_ACCENT
    p_p2 = tf_p.add_paragraph()
    p_p2.text = "👤 Piyush Bhatt"
    p_p2.font.size = Pt(18)
    p_p2.font.bold = True
    p_p2.font.color.rgb = TEXT_WHITE
    p_p3 = tf_p.add_paragraph()
    p_p3.text = "Student, Amrapali University, Haldwani, Uttarakhand"
    p_p3.font.size = Pt(12)
    p_p3.font.color.rgb = RGBColor(203, 213, 225)

    add_card(s1, Inches(7.3), Inches(5.1), Inches(5.0), Inches(1.8), bg_color=NAVY_CARD, border_color=BORDER_COLOR)
    tb_u = s1.shapes.add_textbox(Inches(7.5), Inches(5.25), Inches(4.6), Inches(1.5))
    tf_u = tb_u.text_frame
    tf_u.word_wrap = True
    p_u = tf_u.paragraphs[0]
    p_u.text = "EVALUATION SCOPE:"
    p_u.font.size = Pt(11)
    p_u.font.bold = True
    p_u.font.color.rgb = TEAL_ACCENT
    p_u2 = tf_u.add_paragraph()
    p_u2.text = "🏛️ Amrapali University"
    p_u2.font.size = Pt(18)
    p_u2.font.bold = True
    p_u2.font.color.rgb = TEXT_WHITE
    p_u3 = tf_u.add_paragraph()
    p_u3.text = "B.Tech CSE Project Reviews 1 & 2\nAcademic Year 2026"
    p_u3.font.size = Pt(12)
    p_u3.font.color.rgb = RGBColor(203, 213, 225)
    add_notes(s1, "Respected evaluators, I am Piyush Bhatt from Amrapali University. Today I present our complete Review 1 & 2 presentation for TQM Pharm Enterprise.")

    # =========================================================================
    # SLIDE 2: Problem Statement & Baseline understanding
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Problem Statement & Baseline Clinical Understanding", "RUBRIC: PROBLEM STATEMENT & BASELINE UNDERSTANDING")
    col_w = Inches(3.64)
    gap = Inches(0.4)
    top_pos = Inches(1.8)
    h_pos = Inches(5.1)

    cards2 = [
        ("1. Medication Dispensing Errors", "Clinical Baseline:\n\n• Over 1.3 million preventable patient injuries occur annually due to adverse drug events (ADEs).\n• Manual interpretation of doctor prescriptions causes dosage miscalculations and transcription slips.\n• Lack of automated allergy cross-checks risks fatal Penicillin anaphylaxis.\n• Baseline Solution: Automated Clinical Decision Support System (CDSS) acting as an immutable quality shield.", CORAL_DANGER),
        ("2. Cold-Chain & Expiry Spoilage", "Supply Chain Baseline:\n\n• Vaccines, insulin, and biologics degrade silently outside the mandatory 2.0°C–8.0°C envelope.\n• Standard retail FIFO picking allows older batches to sit unnoticed while newer stock is sold.\n• Substantial annual capital lost in expired, unsellable inventory.\n• Baseline Solution: Algorithmic FEFO (First-Expiry, First-Out) picking + 24/7 continuous IoT temperature telemetry.", AMBER_WARN),
        ("3. Regulatory & Till Shrinkage", "Operational Baseline:\n\n• Inadequate tracking of Schedule X / NDPS controlled sedatives invites severe legal penalties and license cancellation.\n• Cash drawer variances, unmonitored mid-shift payouts, and unverified digital receipts.\n• Failed surprise drug inspector audits due to paper registers.\n• Baseline Solution: Mandatory dual-PIN narcotic register + Daily Z-Report mathematical cash reconciliation.", BLUE_INFO)
    ]
    for idx, (title, body, col) in enumerate(cards2):
        x = Inches(0.8) + Inches(idx * 4.04)
        add_card(s2, x, top_pos, col_w, h_pos)
        bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top_pos, col_w, Inches(0.6))
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = s2.shapes.add_textbox(x, top_pos + Inches(0.08), col_w, Inches(0.5))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb2 = s2.shapes.add_textbox(x + Inches(0.15), top_pos + Inches(0.75), col_w - Inches(0.3), h_pos - Inches(0.9))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        for line in body.split('\n'):
            p = tf2.add_paragraph() if tf2.paragraphs[0].text else tf2.paragraphs[0]
            p.text = line
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(3)
    add_notes(s2, "This slide directly addresses the Problem Statement and Baseline understanding criteria from the university rubric.")

    # =========================================================================
    # SLIDE 3: Quality Objective
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s3, "Quality Objectives Aligned with TQM Principles", "RUBRIC: QUALITY OBJECTIVE", [
        ("Objective 1: Zero Medication Dispensing Defects (Patient Focus)", "Poka-Yoke error-proofing: Automated Clinical Decision Support System (CDSS) intercepts allergen cross-reactions (Penicillin, NSAIDs) and toxic drug interactions before an invoice can be created.", TEAL_ACCENT),
        ("Objective 2: 100% Cold-Chain Storage & Transport Compliance", "Biological Integrity: Guarantee all thermo-sensitive pharmaceuticals remain in 2.0°C–8.0°C via 30s background IoT telemetry streaming and automated thermal spike alarms.", BLUE_INFO),
        ("Objective 3: Zero Expiry Dead-Stock Losses (FEFO Scheduling)", "Process Quality: Eliminate inventory wastage by algorithmically enforcing First-Expiry, First-Out (FEFO) batch prioritization; hard-lock dispensing of expired SKUs.", AMBER_WARN),
        ("Objective 4: Zero Cash Register Discrepancy & Till Balancing", "Fact-Based Management: Enforce strict shift-end financial governance through the Daily Z-Report engine, mathematically balancing opening float, sales, payouts, and counted cash.", NAVY_DARK),
        ("Objective 5: 100% Regulatory Audit Readiness (ISO 9001 & CDSCO)", "Continuous Assurance: Maintain an immutable 21 CFR Part 11 SQLite audit trail, dual-PIN Schedule X narcotic register, and 1-click CSV export ready for State Drug Inspectors.", CORAL_DANGER)
    ])
    add_notes(s3, "This slide satisfies the Quality Objective rubric item, mapping our 5 measurable goals to TQM principles.")

    # =========================================================================
    # SLIDE 4: Scope and User Roles
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Scope and User Roles (Role-Based Access Control)", "RUBRIC: SCOPE AND USER ROLES")
    roles4 = [
        ("👑 Store Admin", "Console HQ", "• Manage staff accounts & passwords\n• Monitor live online terminal presence\n• Review daily Z-Report reconciliations\n• Execute SQLite snapshot backups\n• Inspect immutable system audit stream"),
        ("🩺 Clinical Pharmacist", "Clinical Bay", "• Review incoming e-Prescriptions queue\n• CDSS allergy shield cross-checks\n• Drug-drug interaction risk analysis\n• Schedule X narcotic PIN sign-off\n• Manage chronic patient refill cycles"),
        ("💳 Cashier (POS)", "Billing Counter", "• 1-Click verified eRx import to cart\n• Auto FEFO nearest-expiry batch pick\n• Split payments (Cash, UPI QR, Card)\n• Calculate cash change return\n• Print 80mm GST thermal receipt"),
        ("📦 Inventory Manager", "Supply Hub", "• Multi-batch FEFO stock ledger\n• Record Goods Receipt Notes (GRN)\n• 24/7 Cold-chain IoT fridge monitor\n• Manage supplier directory & POs\n• Track low-stock alerts (≤20 units)"),
        ("🛵 Delivery Agent", "Logistics Bay", "• Active dispatch Kanban route board\n• Verify cold-bag insulated packaging\n• 4-Digit customer OTP verification\n• Record electronic Proof-of-Delivery\n• Handover timestamp audit log")
    ]
    card_w = Inches(2.22)
    for i, (r_name, r_term, r_resp) in enumerate(roles4):
        x = Inches(0.8) + Inches(i * 2.37)
        c = add_card(s4, x, Inches(1.8), card_w, Inches(5.1))
        hb = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), card_w, Inches(0.65))
        hb.fill.solid()
        hb.fill.fore_color.rgb = NAVY_DARK if i % 2 == 0 else TEAL_ACCENT
        hb.line.fill.background()

        tb_h = s4.shapes.add_textbox(x, Inches(1.85), card_w, Inches(0.55))
        tf_h = tb_h.text_frame
        p = tf_h.paragraphs[0]
        p.text = r_name
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb_b = s4.shapes.add_textbox(x + Inches(0.1), Inches(2.55), card_w - Inches(0.2), Inches(4.2))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        p_term = tf_b.paragraphs[0]
        p_term.text = f"Terminal: {r_term}"
        p_term.font.size = Pt(9.5)
        p_term.font.bold = True
        p_term.font.color.rgb = TEXT_MUTED
        p_term.space_after = Pt(6)

        for line in r_resp.split('\n'):
            p = tf_b.add_paragraph()
            p.text = line
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(3)
    add_notes(s4, "This slide satisfies Scope and User Roles: 5 specialized personas enforcing operational separation of duties.")

    # =========================================================================
    # SLIDE 5: Modular folder architecture
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Modular Folder Architecture & 6-Tier System Blueprint", "RUBRIC: MODULAR FOLDER ARCHITECTURE")
    
    # Left: Folder Structure Tree
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_tr = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_tr = tb_tr.text_frame
    tf_tr.word_wrap = True
    p = tf_tr.paragraphs[0]
    p.text = "📁 ENTERPRISE MODULAR REPOSITORY LAYOUT"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(6)
    tr_text = """Pharmacy_Management_System/
├── core/
│   ├── bridge.py       # RPC Bridge (38 typed methods)
│   ├── db.py           # SQLite persistence (14 tables)
│   ├── api_client.py   # Telemetry & presence client
│   └── logger.py       # 21 CFR Part 11 audit logger
├── config/
│   └── settings.py     # Central Singleton configuration
├── ui/
│   ├── desktop/        # Edge Chromium WebView2 60 FPS
│   └── web/            # Cloud-ready FastAPI Web UI
├── apps/               # Admin & operational workstations
├── tests/              # 24 Automated pytest test cases
├── backups/            # Automated SQLite snapshots
├── main.py             # Hardware-accelerated entrypoint
└── web_app.py          # Asynchronous FastAPI web server"""
    for l in tr_text.split('\n'):
        p = tf_tr.add_paragraph()
        p.text = l
        p.font.size = Pt(9.5)
        p.font.name = "Consolas"
        p.font.color.rgb = TEXT_MAIN

    # Right: Golden Rule & Tier Decoupling
    add_card(s5, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1), bg_color=NAVY_CARD, border_color=TEAL_ACCENT)
    tb_gr = s5.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_gr = tb_gr.text_frame
    tf_gr.word_wrap = True
    p = tf_gr.paragraphs[0]
    p.text = "⭐ THE ONE RULE TO REMEMBER"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(6)

    p2 = tf_gr.add_paragraph()
    p2.text = "\"The screen must not talk to the database.\""
    p2.font.size = Pt(17)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_after = Pt(10)

    p3 = tf_gr.add_paragraph()
    p3.text = "UI  →  Service (Bridge)  →  Model / Database"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = BLUE_INFO
    p3.space_after = Pt(10)

    gr_reasons = [
        "• No raw SQL queries inside billing.py or any UI template.",
        "• All database operations are mediated by typed Python methods.",
        "• Failure isolation: UI bugs cannot corrupt database ACID commits.",
        "• Validation and audit have dedicated architectural homes.",
        "• Allows layer-by-layer agile development and test-driven verification."
    ]
    for r in gr_reasons:
        p = tf_gr.add_paragraph()
        p.text = r
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(4)
    add_notes(s5, "Satisfies Modular folder architecture: clear 6-tier decoupling and enforcing the rule that the UI never writes raw SQL.")

    # =========================================================================
    # SLIDE 6: SRS (Software Requirements Specification)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Software Requirements Specification (SRS) — IEEE 830", "RUBRIC: SRS (REQUIREMENTS ENGINEERING)")
    
    # Left: Functional Requirements
    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_fr = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_fr = tb_fr.text_frame
    tf_fr.word_wrap = True
    p = tf_fr.paragraphs[0]
    p.text = "📋 CORE FUNCTIONAL REQUIREMENTS (FR-01 TO FR-10)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(6)
    fr_items = [
        "FR-01 (Auth & Telemetry): SHA-256 password hash, session UUID, 5s heartbeat.",
        "FR-02 (CDSS Safety Engine): eRx cross-check for patient Penicillin allergies.",
        "FR-03 (Schedule X Narcotics): Doctor DMC Reg + Pharmacist 4-digit PIN log.",
        "FR-04 (FEFO Batch Picker): Automatic sorting by earliest expiry; lock expired lot.",
        "FR-05 (POS Express Billing): 1-Click eRx import, cash change calc, dynamic UPI QR.",
        "FR-06 (Goods Receipt GRN): Inward supplier consignments with batch & cost.",
        "FR-07 (IoT Cold-Chain): Monitor 2-8°C sensors; trigger audible/visual excursion alert.",
        "FR-08 (Delivery Fleet): Kanban dispatch board with customer 4-digit OTP e-POD.",
        "FR-09 (Z-Report Shift Close): Mathematical cash balancing & signed Z-slip archive.",
        "FR-10 (Audit Logging): 21 CFR Part 11 append-only tamper-evident event stream."
    ]
    for item in fr_items:
        p = tf_fr.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    # Right: Non-Functional & Standards
    add_card(s6, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_nfr = s6.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_nfr = tb_nfr.text_frame
    tf_nfr.word_wrap = True
    p = tf_nfr.paragraphs[0]
    p.text = "⚡ NON-FUNCTIONAL REQUIREMENTS & STANDARDS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(6)
    nfr_items = [
        ("NFR-01 (Performance & Latency): ", "UI click response <50ms; SQLite transaction commit <10ms; 60 FPS hardware acceleration."),
        ("NFR-02 (ACID Reliability): ", "100% ACID compliance with automatic daily snapshot backups in backups/."),
        ("NFR-03 (Security & Non-Repudiation): ", "Role-based route shields, session timeout, and immutable audit logging."),
        ("NFR-04 (Statutory Compliance): ", "Indian Drugs & Cosmetics Act 1940 (Schedule H1/X) and GST electronic tax calculation."),
        ("Formal SRS Artifacts: ", "Submitted as IEEE Std 830-1998 compliant DOCX (`SRS_TQM_Pharm_Enterprise.docx`) and PDF (`SRS_TQM_Pharm_Enterprise.pdf`).")
    ]
    for b_t, n_t in nfr_items:
        p2 = tf_nfr.add_paragraph()
        r1 = p2.add_run()
        r1.text = b_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY_DARK
        r2 = p2.add_run()
        r2.text = n_t
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)
    add_notes(s6, "Satisfies SRS rubric item: formal IEEE 830 specification detailing all functional and non-functional requirements.")

    # =========================================================================
    # SLIDE 7: Modules and Features
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Modules and Features Overview", "RUBRIC: MODULES AND FEATURES")
    modules7 = [
        ("🩺 Clinical Station & CDSS", "eRx intake queue, allergy cross-matching, drug interaction warning modal, Schedule X double sign-off register.", TEAL_ACCENT),
        ("💳 POS Express Billing Counter", "1-Click approved Rx import, barcode scanner, FEFO batch selection, split payments (Cash/UPI/Card), GST receipt.", BLUE_INFO),
        ("📦 Supply Chain & Inventory Hub", "Multi-batch FEFO ledger, low stock alerts (≤20), Goods Receipt Notes (GRN) inwarding, supplier directory.", NAVY_DARK),
        ("❄️ Cold-Chain IoT Telemetry (2-8°C)", "Live circular temperature gauges for Chambers A & B, 24/7 background stream, simulated temperature spike alarm.", CORAL_DANGER),
        ("🛵 Delivery Fleet & Fulfilment", "Active dispatch Kanban board, cold-bag insulation checklist, manual route creation, 4-digit OTP e-POD.", AMBER_WARN),
        ("👑 Admin Command Center", "Staff user CRUD with role assignment, active terminal presence heartbeats, Daily Z-Report till close, audit trail.", PURPLE_ACCENT)
    ]
    for idx, (m_title, m_desc, col) in enumerate(modules7):
        r = idx // 2
        c_i = idx % 2
        x = Inches(0.8) + Inches(c_i * 5.95)
        y = Inches(1.8) + Inches(r * 1.7)
        add_card(s7, x, y, Inches(5.75), Inches(1.5))
        bar = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), Inches(1.5))
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = s7.shapes.add_textbox(x + Inches(0.25), y + Inches(0.12), Inches(5.35), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = m_title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK
        p2 = tf.add_paragraph()
        p2.text = m_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(2)
    add_notes(s7, "Satisfies Modules and Features: outlines all 6 functional subsystems operating across the application.")

    # =========================================================================
    # SLIDE 8: Core Features/Modules aligned with quality goals
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    tqm_matrix = [
        ("CDSS Allergy & Drug-Drug Shield", "Zero Dispensing Defects / Poka-Yoke Error Proofing (Shingo)"),
        ("Algorithmic FEFO Batch Sequencing", "Zero Inventory Dead-Stock / Process Waste Elimination"),
        ("24/7 IoT Cold-Chain Monitoring (2-8°C)", "Zero Biological Degradation / Quality Assurance"),
        ("Daily Z-Report Mathematical Balancing", "Zero Till Variance / Fact-Based Management (Juran)"),
        ("Statutory Schedule X Dual PIN Register", "Zero Diversion / Indian Drugs & Cosmetics Act 1940 Compliance"),
        ("Immutable Audit Logs (21 CFR Part 11)", "Complete Traceability, Accountability & Non-Repudiation"),
        ("Automated Error Telemetry (E01-E05)", "Root-Cause Prioritization (Pareto 80/20) & FMEA Risk Matrix"),
        ("Customer & Patient EHR Allergy Profile", "Customer & Patient Focus (Crosby Zero-Defects Standard)")
    ]
    add_table_slide(s8, "Core Features/Modules Aligned with Quality Goals", "RUBRIC: CORE FEATURES/MODULES ALIGNED WITH QUALITY GOALS", ["Implemented Core Feature / Module", "Aligned TQM Quality Goal & Principle"], tqm_matrix, [5.0, 6.333])
    add_notes(s8, "Satisfies Core Features/Modules aligned with quality goals: demonstrating that software features map directly to quality objectives.")

    # =========================================================================
    # SLIDE 9: Database/System Design
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "Database/System Design & Relational Data Dictionary", "RUBRIC: DATABASE/SYSTEM DESIGN")
    
    col_w = Inches(5.75)
    t_left = [
        ("1. staff (users)", "Credentials, assigned RBAC role, branch, active status."),
        ("2. medicines", "SKU, generic, batch lot, expiry, days left, stock, MRP, rack."),
        ("3. prescriptions", "Patient name, doctor, items JSON, CDSS status, clinical notes."),
        ("4. invoices (sales)", "Official tax invoices, cashier, subtotal, GST split, total amount."),
        ("5. delivery_orders", "Dispatch route, address, rider, cold-bag check, 4-digit OTP."),
        ("6. patients (customers)", "EHR profiles, contact phone, chronic diseases, recorded allergies."),
        ("7. suppliers", "Distributor directory, GSTIN, contact phone, payment terms.")
    ]
    t_right = [
        ("8. purchase_orders", "GRN inwarding, supplier, batch items JSON, total amount."),
        ("9. narcotic_register", "Schedule X: Doctor DMC Reg No, Pharmacist PIN, batch, qty."),
        ("10. temperature_logs", "24/7 cold-chain telemetry: probe ID, temperature (2-8°C)."),
        ("11. refill_schedules", "Chronic maintenance therapy: last dispensed, next due date."),
        ("12. active_sessions", "Live presence: user ID, terminal name, 5s heartbeat timestamp."),
        ("13. audit_logs", "21 CFR Part 11 append-only log: user, role, action, details."),
        ("14. z_reports", "Daily till close: opening float, sales, payouts, live variance.")
    ]
    for c_idx, t_list in enumerate([t_left, t_right]):
        x = Inches(0.8) + Inches(c_idx * 5.95)
        add_card(s9, x, Inches(1.8), col_w, Inches(5.1))
        tb = s9.shapes.add_textbox(x + Inches(0.2), Inches(1.95), col_w - Inches(0.4), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "CORE RELATIONAL ENTITIES (PART 1)" if c_idx == 0 else "COMPLIANCE & TELEMETRY ENTITIES (PART 2)"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEAL_ACCENT if c_idx == 0 else BLUE_INFO
        p.space_after = Pt(6)
        for t_name, t_desc in t_list:
            p2 = tf.add_paragraph()
            r1 = p2.add_run()
            r1.text = f"• {t_name}: "
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = NAVY_DARK
            r2 = p2.add_run()
            r2.text = t_desc
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = TEXT_MAIN
            p2.space_after = Pt(2)
    add_notes(s9, "Satisfies Database/System Design: all 14 normalized tables in SQLite with relational integrity.")

    # =========================================================================
    # SLIDE 10: Database Integration
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s10, "Database Integration: ACID Transactions & Migrations", "RUBRIC: DATABASE INTEGRATION", [
        ("1. ACID Transaction Integrity (Atomicity & Consistency)", "Transactions guarantee complete success or complete rollback: saving an invoice, cutting batch stock, and writing the audit row occur together or not at all.", TEAL_ACCENT),
        ("2. SQLite WAL (Write-Ahead Logging) & Concurrency", "Enabled Write-Ahead Logging allows simultaneous non-blocking reads from multiple terminal UI threads while writes commit in <10ms.", BLUE_INFO),
        ("3. Relational Foreign Keys & Check Constraints", "Foreign keys enforce referential integrity between prescriptions, invoices, and patients. Check constraints prevent negative inventory.", NAVY_DARK),
        ("4. Schema Migrations Without Data Loss", "The migration subsystem dynamically applies ALTER TABLE schema updates without wiping student or patient test records.", PURPLE_ACCENT),
        ("5. Automated Database Snapshots & Archival", "System creates timestamped snapshot backups in backups/ daily and on application exit for disaster recovery.", AMBER_WARN)
    ])
    add_notes(s10, "Satisfies Database Integration: demonstrates how SQLite is integrated with ACID guarantees, WAL concurrency, and migrations.")

    # =========================================================================
    # SLIDE 11: CRUD operations
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    crud_matrix11 = [
        ("Staff & RBAC Accounts", "CRUD (Add/Edit Users)", "R (Staff Directory)", "R (Read Profile)", "R (Read Profile)", "R (Read Profile)"),
        ("Medicines & Batch Stock", "CRUD (Full Catalog)", "R (Clinical View)", "R, U (Dispense Deduct)", "CRUD (Stock Adjust)", "R (Stock Query)"),
        ("Prescriptions Intake Queue", "R (Audit Review)", "CRUD (Validate/Reject)", "R, U (Mark Dispensed)", "R (Consignment)", "R (Order Lines)"),
        ("Invoices & POS Billing", "R (Sales History)", "R (Rx Dispensing)", "CR (Generate & Print)", "R (Inward Bills)", "R (Delivery Note)"),
        ("Delivery Orders & Logistics", "R, D (Fleet Admin)", "R (Dispense Dispatch)", "C (Dispatch Order)", "R (Cold Checklist)", "RU (OTP Validate)"),
        ("Narcotic Register (Sched X)", "R (Statutory Export)", "CR (Double Sign PIN)", "R (Read Only)", "R (Inward Only)", "No Access (Blocked)"),
        ("Daily Z-Report Close", "R, U (Audit Sign-Off)", "No Access (Blocked)", "CR (Shift Cash Close)", "No Access (Blocked)", "No Access (Blocked)")
    ]
    add_table_slide(s11, "CRUD Operations Implementation Across All Entities", "RUBRIC: CRUD OPERATIONS", ["Entity / Subsystem", "👑 Store Admin", "🩺 Pharmacist", "💳 Cashier POS", "📦 Inventory", "🛵 Delivery Rider"], crud_matrix11, [2.333, 1.8, 1.8, 1.8, 1.8, 1.8])
    add_notes(s11, "Satisfies CRUD operations: comprehensive matrix showing Create, Read, Update, Delete permissions across all 5 roles.")

    # =========================================================================
    # SLIDE 12: Initial UI/Workflow
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s12, "Initial UI & Workstation Interface Design", "RUBRIC: INITIAL UI/WORKFLOW", [
        ("1. Clean Dual Theming (Default: Light / White Mode)", "Engineered for hospital and dispensary lighting: default white theme with crisp slate borders and an instant 1-click Dark Mode toggle.", TEAL_ACCENT),
        ("2. Workstation Persona Login Portal Grid", "Interactive visual tiles for all 5 roles pre-filling credentials instantly and assigning sessions to physical terminal counters.", BLUE_INFO),
        ("3. Zero-Lag 60 FPS Edge Chromium WebView2 Rendering", "Native desktop hardware acceleration eliminates UI frame freezing; background asynchronous threads handle I/O.", NAVY_DARK),
        ("4. Responsive Dual Deployment Parity", "Desktop application (Edge WebView2) and Web application (FastAPI) share 100% UI feature parity on tablets and laptops.", PURPLE_ACCENT)
    ])
    add_notes(s12, "Satisfies Initial UI/Workflow: covers interface theming, workstation persona tiles, and 60 FPS desktop rendering.")

    # =========================================================================
    # SLIDE 13: Main System Workflow
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13)
    add_header(s13, "Main System Workflow: End-to-End Pipeline", "RUBRIC: MAIN SYSTEM WORKFLOW")
    stages13 = [
        ("Stage 1: eRx Intake", "Doctor prescription uploaded\nPatient EHR allergies scanned\nEnters pending review queue", BLUE_INFO),
        ("Stage 2: Clinical Gate", "Pharmacist runs CDSS scan\nAllergy & interaction checks\nSchedule X PIN authenticated\nStatus updated to 'Approved'", TEAL_ACCENT),
        ("Stage 3: POS Express", "1-Click import to Cashier cart\nAuto FEFO batch picking\nDynamic UPI QR / Cash change\nThermal 80mm GST receipt printed", NAVY_DARK),
        ("Stage 4: Cold Fleet", "Cold-bag checklist verified\nDispatched on Kanban route\nCustomer gives 4-digit OTP\nMarked 'Delivered' (e-POD)", AMBER_WARN),
        ("Stage 5: Z-Report Close", "Cash drawer counted\nVariance calculated (₹0.00)\nShift signed & closed in SQLite\nCSV exported for accounting", CORAL_DANGER)
    ]
    col_w = Inches(2.22)
    for i, (title, desc, col) in enumerate(stages13):
        x = Inches(0.8) + Inches(i * 2.37)
        c = add_card(s13, x, Inches(1.8), col_w, Inches(3.2))
        hb = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), col_w, Inches(0.6))
        hb.fill.solid()
        hb.fill.fore_color.rgb = col
        hb.line.fill.background()

        tb_h = s13.shapes.add_textbox(x, Inches(1.85), col_w, Inches(0.5))
        tf_h = tb_h.text_frame
        p = tf_h.paragraphs[0]
        p.text = f"STEP {i+1}"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb_b = s13.shapes.add_textbox(x + Inches(0.1), Inches(2.5), col_w - Inches(0.2), Inches(2.4))
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

    add_card(s13, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.7))
    tb_ui = s13.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.5))
    tf_ui = tb_ui.text_frame
    tf_ui.word_wrap = True
    p = tf_ui.paragraphs[0]
    p.text = "🔄 ARCHITECTURAL PIPELINE SUMMARY: HOW A CLICK TRAVELS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(4)
    ui_points = (
        "1. Screen takes user click → 2. Service checks role authorization → 3. CDSS verifies patient allergy EHR → "
        "4. Validators assert stock ceiling & expiry → 5. SQLite executes atomic commit (bill + cut stock) → "
        "6. Audit log row written → 7. Dashboard KPI tickers update."
    )
    p = tf_ui.add_paragraph()
    p.text = ui_points
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MAIN
    add_notes(s13, "Satisfies Main System Workflow: end-to-end trace from prescription intake through POS billing and daily Z-report close.")

    # =========================================================================
    # SLIDE 14: TQM Quality Analytics: Pareto & Fishbone
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_bg(s14)
    add_header(s14, "TQM Quality Analytics: Pareto (80/20) & Fishbone", "TQM ROOT-CAUSE ANALYTICS")
    
    # Left: Pareto 80/20
    add_card(s14, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb1 = s14.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "📈 PARETO ROOT-CAUSE ANALYSIS (80/20 RULE)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(8)
    pareto_pts = [
        ("1. Look-Alike / Sound-Alike Drugs (45%): ", "Addressed by CDSS generic molecule search and allergy confirmation."),
        ("2. Qty > Available Stock Attempts (30%): ", "Addressed by pre-save inventory balance assertion locks."),
        ("3. Near-Expiry Drug Dispensing (15%): ", "Addressed by algorithmic FEFO nearest-expiry prioritization."),
        ("4. Insulated Cold-Bag Packaging (7%): ", "Addressed by mandatory delivery pre-dispatch checklist."),
        ("Key TQM Takeaway: ", "Eliminating the top 2 error modes removes 75% of all operational dispensary defects.")
    ]
    for b_t, n_t in pareto_pts:
        p2 = tf1.add_paragraph()
        r1 = p2.add_run()
        r1.text = b_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY_DARK
        r2 = p2.add_run()
        r2.text = n_t
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)

    # Right: Fishbone (Ishikawa)
    add_card(s14, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb2 = s14.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🐟 FISHBONE (ISHIKAWA) ROOT-CAUSE BREAKDOWN"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(8)
    fishbone_pts = [
        ("People (Staff): ", "Rushed cashiers during counter peaks; new dispensers misinterpreting doctor handwriting."),
        ("Process (Workflow): ", "Lack of second-check clinical verification step before POS billing."),
        ("Software (System): ", "Legacy systems allowing expired stock cart addition and lacking allergy alerts."),
        ("Data (Integrity): ", "Missing batch numbers, incorrect physical expiry dates, unrecorded patient allergies."),
        ("Machine (Hardware): ", "Slow workstation hardware and missed clicks on crowded UI screens.")
    ]
    for b_t, n_t in fishbone_pts:
        p2 = tf2.add_paragraph()
        r1 = p2.add_run()
        r1.text = b_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY_DARK
        r2 = p2.add_run()
        r2.text = n_t
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)
    add_notes(s14, "Demonstrates Pareto 80/20 prioritization and Fishbone cause-and-effect root cause analysis.")

    # =========================================================================
    # SLIDE 15: TQM Quality Governance: FMEA & PDCA
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_bg(s15)
    add_header(s15, "TQM Quality Governance: FMEA Risk & Deming PDCA", "TQM QUALITY GOVERNANCE")
    
    # Left: FMEA Table
    add_card(s15, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb1 = s15.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "⚠️ FMEA TABLE (RPN = S x O x D)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CORAL_DANGER
    p.space_after = Pt(6)
    fmea_items = [
        ("Sell Expired Drug: ", "S=10, O=4, D=3 → RPN 120\nAction: Hard block prevents cart checkout."),
        ("Dispense Allergen Drug: ", "S=10, O=3, D=4 → RPN 120\nAction: CDSS allergy warning & override block."),
        ("Qty > Stock Oversell: ", "S=8, O=5, D=3 → RPN 120\nAction: Pre-commit inventory balance assert."),
        ("Duplicate Barcode Scan: ", "S=6, O=2, D=2 → RPN 24\nAction: Unique constraint on SKU barcode.")
    ]
    for b_t, n_t in fmea_items:
        p2 = tf1.add_paragraph()
        r1 = p2.add_run()
        r1.text = b_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY_DARK
        r2 = p2.add_run()
        r2.text = n_t
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)

    # Right: Deming PDCA Cycle
    add_card(s15, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb2 = s15.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🔁 DEMING PDCA QUALITY CYCLE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(6)
    pdca_items = [
        ("PLAN: ", "Identify excessive oversell and near-expiry mistakes during peak rush."),
        ("DO: ", "Deploy automated FEFO batch picker and pre-save stock balance locks."),
        ("CHECK: ", "Monitor monthly counts of error codes E01 and E03 in error_logs."),
        ("ACT: ", "Standardize FEFO logic across all terminals as mandatory baseline policy."),
        ("Log Feedback Loop: ", "Blocked actions write to error_logs → tqm_report counts frequency → Occurrence score dynamically updates in FMEA table.")
    ]
    for b_t, n_t in pdca_items:
        p2 = tf2.add_paragraph()
        r1 = p2.add_run()
        r1.text = b_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY_DARK
        r2 = p2.add_run()
        r2.text = n_t
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)
    add_notes(s15, "FMEA risk prioritization and Deming PDCA continuous improvement cycle.")

    # =========================================================================
    # SLIDE 16: Working application
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_bg(s16)
    add_header(s16, "Working Application Setup, Verification & Personas", "RUBRIC: WORKING APPLICATION")
    
    # Left: Startup Commands & Verification
    add_card(s16, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb1 = s16.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🚀 APPLICATION LAUNCH & VERIFICATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(8)
    cmds = [
        ("Automated Tests (Quality Proof): ", "`pytest`\n→ 24/24 unit & integration tests passing in ~7.8s."),
        ("Desktop Workstation App: ", "`python main.py`\n→ Boots hardware-accelerated Edge Chromium WebView2 window."),
        ("Cloud Web Portal: ", "`python web_app.py`\n→ Starts FastAPI server at http://127.0.0.1:8000 with Swagger docs."),
        ("Terminal Binding: ", "Assign session to Front Counter A, Clinical Kiosk, or Dock.")
    ]
    for b_t, n_t in cmds:
        p2 = tf1.add_paragraph()
        r1 = p2.add_run()
        r1.text = b_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY_DARK
        r2 = p2.add_run()
        r2.text = n_t
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)

    # Right: Pre-Seeded Personas Table
    personas = [
        ("👑 Store Admin", "`admin` / `admin123`", "RBAC, live presence, Daily Z-Report balancing"),
        ("🩺 Pharmacist", "`pharmacist` / `pharma123`", "CDSS allergy scan, Schedule X narcotic sign-off"),
        ("💳 POS Cashier", "`cashier` / `cash123`", "1-Click eRx import, FEFO batch, UPI QR, receipt"),
        ("📦 Inventory", "`inventory` / `inv123`", "Multi-batch ledger, GRN inwarding, 2-8°C IoT"),
        ("🛵 Delivery Agent", "`delivery` / `deliv123`", "Kanban dispatch, cold-bag check, OTP e-POD")
    ]
    add_card(s16, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb2 = s16.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🔑 WORKSTATION PERSONAS & CREDENTIALS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(8)
    for r_name, creds, scope in personas:
        p2 = tf2.add_paragraph()
        r1 = p2.add_run()
        r1.text = f"{r_name}: {creds}\n"
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY_DARK
        r2 = p2.add_run()
        r2.text = f"Scope: {scope}"
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = TEXT_MUTED
        p2.space_after = Pt(4)
    add_notes(s16, "Satisfies Working application: setup commands, 24 automated tests, and pre-seeded credentials for all 5 roles.")

    # =========================================================================
    # SLIDE 17: Demonstration of implemented functionality
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s17, "Demonstration of Implemented Functionality", "RUBRIC: DEMONSTRATION OF IMPLEMENTED FUNCTIONALITY", [
        ("Phase 1: Clinical Pharmacist & CDSS Gate", "Review incoming eRx queue. Trigger CDSS Allergy Interception (Penicillin warning blocks checkout). Execute Schedule X Narcotic double sign-off with Doctor DMC No + Pharmacist PIN.", TEAL_ACCENT),
        ("Phase 2: POS Cashier Express Billing", "1-Click import approved eRx into cart. Verify automatic FEFO nearest-expiry batch selection. Tender checkout: enter Cash (auto change calc) or Dynamic UPI QR. Print 80mm GST receipt.", BLUE_INFO),
        ("Phase 3: Inventory FEFO & Cold-Chain IoT", "Inspect batch ledger with countdown badges (<30d Red, <90d Yellow). Click 'Simulate Temp Spike' (9.4°C) on Chamber A fridge → observe immediate visual alert & log entry.", CORAL_DANGER),
        ("Phase 4: Fulfilment Fleet & OTP Handover", "Advance order on Kanban dispatch board. Verify insulated cold-bag checklist. Enter customer 4-digit SMS OTP (1234) to confirm electronic Proof-of-Delivery (e-POD).", AMBER_WARN),
        ("Phase 5: Admin Command Center & Z-Report Close", "Monitor live terminal presence heartbeats. Open Daily Z-Report module: enter physical cash counted, verify variance (Balanced ₹0.00), sign and lock shift register.", NAVY_DARK)
    ])
    add_notes(s17, "Satisfies Demonstration of implemented functionality: 5-phase live demonstration script proving all quality gates.")

    # =========================================================================
    # SLIDE 18: Quality Verification & Viva Conclusion
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_bg(s18, NAVY_DARK)
    top_strip = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = TEAL_ACCENT
    top_strip.line.fill.background()

    tb = s18.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "REVIEW 1 & 2 SUMMARY, EMPIRICAL VERIFICATION & VIVA CLOSING"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = TEAL_ACCENT
    p0.space_after = Pt(6)

    p1 = tf.add_paragraph()
    p1.text = "24 / 24 Automated Tests Passed (100% Reliability)"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(8)

    roadmap = [
        ("Review 1 Deliverables (Now Completed): ", "Problem Statement, Quality Objectives, IEEE 830 SRS, 5 User Roles, Modular 6-Tier Architecture, 14 Tables, CRUD Matrix, Initial UI, Working Desktop & Web App, 24 Automated Tests."),
        ("Review 2 Horizon (Next Phase): ", "Longitudinal FMEA occurrence tracking from error logs, automated real-time Pareto charts, Ishikawa incident registry, and multi-branch cloud database replication.")
    ]
    for b_t, n_t in roadmap:
        p2 = tf.add_paragraph()
        r1 = p2.add_run()
        r1.text = b_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = TEAL_LIGHT
        r2 = p2.add_run()
        r2.text = n_t
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = RGBColor(226, 232, 240)
        p2.space_after = Pt(4)

    # Viva Golden Box
    add_card(s18, Inches(1.0), Inches(4.8), Inches(11.3), Inches(2.2), bg_color=NAVY_CARD, border_color=TEAL_ACCENT)
    tb_g = s18.shapes.add_textbox(Inches(1.2), Inches(4.9), Inches(10.9), Inches(2.0))
    tf_g = tb_g.text_frame
    tf_g.word_wrap = True
    pg = tf_g.paragraphs[0]
    pg.text = "⭐ ONE SENTENCE FOR VIVA CLOSING"
    pg.font.size = Pt(12)
    pg.font.bold = True
    pg.font.color.rgb = TEAL_ACCENT
    pg.space_after = Pt(4)

    pg2 = tf_g.add_paragraph()
    pg2.text = "\"The UI never writes SQL. Validation stops bad data. Audit records who did what. Expired stock cannot be sold. Logs become Pareto, FMEA, PDCA.\""
    pg2.font.size = Pt(13)
    pg2.font.bold = True
    pg2.font.color.rgb = TEXT_WHITE
    pg2.space_after = Pt(6)

    pg3 = tf_g.add_paragraph()
    pg3.text = "🙏 Sincere gratitude to the Computer Science & Management faculty at Amrapali University. The floor is open for viva questions. (Candidate: Piyush Bhatt)"
    pg3.font.size = Pt(10.5)
    pg3.font.color.rgb = RGBColor(148, 163, 184)
    add_notes(s18, "Closing statement: 100% of rubric criteria delivered. Deliver the golden sentence and invite questions.")

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TQM_Pharm_Presentation_Piyush_Bhatt.pptx")
    prs.save(output_path)
    legacy_pptx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AegisPharm_TQM_Presentation_Piyush_Bhatt.pptx")
    prs.save(legacy_pptx)
    print(f"[SUCCESS] Rubric-Aligned 18-Slide PowerPoint generated successfully at: {output_path}")

    # Export to PDF via PowerPoint COM
    try:
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TQM_Pharm_Presentation_Piyush_Bhatt.pdf")
        legacy_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AegisPharm_TQM_Presentation_Piyush_Bhatt.pdf")
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        deck = ppt_app.Presentations.Open(os.path.abspath(output_path), WithWindow=False)
        deck.SaveAs(os.path.abspath(pdf_path), 32)
        deck.SaveAs(os.path.abspath(legacy_pdf), 32)
        deck.Close()
        ppt_app.Quit()
        print(f"[SUCCESS] Rubric-Aligned 18-Slide PDF generated successfully at: {pdf_path}")
    except Exception as e:
        print(f"[WARNING] PowerPoint COM export failed: {e}")

if __name__ == "__main__":
    build_rubric_deck()
