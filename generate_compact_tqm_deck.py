"""
AegisPharm Enterprise — Executive 18-Slide TQM Master Presentation Generator.
Author: Piyush Bhatt, Amrapali University.
Generates an executive, concise 18-slide presentation synthesizing all Review 1 & 2 topics:
Vision, Mission, Quality Objectives, Process Map, SIPOC, Stakeholders, Goal Q01,
Modular 6-Tier Architecture, Database Design (14 Tables), CRUD Matrix, Service Layer,
Quality Dashboard, Pareto, Fishbone, FMEA, PDCA, Working Demo Guide, and Viva Defense.
"""

import os
import win32com.client
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_compact_deck():
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

    def add_header(slide, title_text, category_text="SRS REVIEW 1 & 2 · PROCESS + QUALITY"):
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

    def add_stacked_cards(slide, title, cards_data, category="SRS REVIEW 1 & 2 · PROCESS + QUALITY"):
        set_bg(slide)
        add_header(slide, title, category)
        n = len(cards_data)
        total_h = 5.2
        gap = 0.18
        h = (total_h - gap * (n - 1)) / n
        y = 1.75
        for heading, body, *opt in cards_data:
            col = opt[0] if opt else TEAL_ACCENT
            c = add_card(slide, Inches(0.8), Inches(y), Inches(11.733), Inches(h))
            bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(y), Inches(0.12), Inches(h))
            bar.fill.solid()
            bar.fill.fore_color.rgb = col
            bar.line.fill.background()

            tb = slide.shapes.add_textbox(Inches(1.1), Inches(y + 0.08), Inches(11.2), Inches(h - 0.16))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = heading
            p.font.size = Pt(12.5 if n <= 4 else 11.5)
            p.font.bold = True
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(2)

            for line in body.split('\n'):
                p2 = tf.add_paragraph()
                p2.text = line
                p2.font.size = Pt(11 if n <= 4 else 10)
                p2.font.color.rgb = TEXT_MAIN
                p2.space_after = Pt(2)
            y += h + gap

    def add_table_slide(slide, title, headers, rows_data, col_widths=None, category="SRS REVIEW 1 & 2 · PROCESS + QUALITY"):
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
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_WHITE

        for r_idx, row in enumerate(rows_data, start=1):
            bg = BG_LIGHT if r_idx % 2 == 1 else CARD_BG
            for c_idx, val in enumerate(row):
                cell = tbl.cell(r_idx, c_idx)
                cell.text = str(val)
                cell.fill.solid()
                cell.fill.fore_color.rgb = bg
                p = cell.text_frame.paragraphs[0]
                p.font.size = Pt(10)
                p.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 1: Title (Executive Cover)
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
    p0.text = "SRS REVIEW 1 & 2 · PROCESS + QUALITY EVALUATION"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = TEAL_ACCENT
    p0.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "AegisPharm Enterprise"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "Process Map, Stakeholders, Measurable Requirements & Quality Goals (TQM Architecture)\nAssigned Goal: Q01 Improve Reliability & Zero-Defects"
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
    add_notes(s1, "Respected evaluators, I am Piyush Bhatt from Amrapali University. Today I present our condensed Process + Quality review covering Review 1 and 2.")

    # =========================================================================
    # SLIDE 2: Vision, Mission & Quality Objectives
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s2, "Vision, Mission & Quality Objectives", [
        ("VISION", "A healthcare dispensary where zero expired, contraindicated, or unrecorded medications ever cross the counter.", TEAL_ACCENT),
        ("MISSION", "Engineer an enterprise-grade local-first operating system that automates FEFO inventory, blocks clinical contraindications (CDSS), validates narcotics, and maintains immutable audit logs.", BLUE_INFO),
        ("QUALITY OBJECTIVE OF THIS SOFTWARE", "Prevent errors at the source (Poka-Yoke error-proofing).\nControl the process with deterministic rules. Monitor all transactions with immutable logs and real-time IoT telemetry.", NAVY_DARK)
    ])
    add_notes(s2, "Our vision and mission directly translate into TQM controls: stop the error at source, control every transaction, and log everything.")

    # =========================================================================
    # SLIDE 3: Three Quality Ideas Behind the Software
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Three Quality Ideas Behind the Software")
    col_w = Inches(3.64)
    gap = Inches(0.4)
    top_pos = Inches(1.8)
    h_pos = Inches(5.1)

    cards3 = [
        ("Error Prevention at Source", "Poka-yoke Mistake Proofing\n\n• Blank medicine names hard blocked.\n• Qty > available stock blocked.\n• Expired items blocked from cart.\n• Patient allergen contraindications (Penicillin) locked.", CORAL_DANGER),
        ("Process Control", "One Deterministic Work Path\n\n• Supplier (GRN) → Stock (FEFO)\n  → CDSS Clinical Gate → POS Bill\n  → Daily Z-Report Shift Close.\n• UI cannot skip or bypass business rules.", BLUE_INFO),
        ("Continuous Monitoring", "See, Trace & Feedback\n\n• Live dashboard KPI alerts.\n• 24/7 cold-chain IoT logs (2-8°C).\n• 21 CFR Part 11 immutable audit trail.\n• Error logs feeding FMEA & Pareto.", TEAL_ACCENT)
    ]
    for idx, (title, body, col) in enumerate(cards3):
        x = Inches(0.8) + Inches(idx * 4.04)
        add_card(s3, x, top_pos, col_w, h_pos)
        bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top_pos, col_w, Inches(0.6))
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = s3.shapes.add_textbox(x, top_pos + Inches(0.08), col_w, Inches(0.5))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb2 = s3.shapes.add_textbox(x + Inches(0.15), top_pos + Inches(0.75), col_w - Inches(0.3), h_pos - Inches(0.9))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        for line in body.split('\n'):
            p = tf2.add_paragraph() if tf2.paragraphs[0].text else tf2.paragraphs[0]
            p.text = line
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(4)
    add_notes(s3, "Three pillars: Error prevention at source, process control, and continuous monitoring.")

    # =========================================================================
    # SLIDE 4: Process Map & Controls Across the Pipeline
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Process Map & Controls Across the Pipeline")
    stages4 = ["Supplier", "Purchase (GRN)", "Stock (FEFO)", "Bill (POS)", "Customer / Fleet", "Z-Report Close"]
    box_w = Inches(1.8)
    for idx, stg in enumerate(stages4):
        x = Inches(0.8) + Inches(idx * 1.98)
        add_card(s4, x, Inches(1.8), box_w, Inches(0.8), bg_color=NAVY_DARK, border_color=TEAL_ACCENT)
        tb = s4.shapes.add_textbox(x, Inches(1.95), box_w, Inches(0.5))
        p = tb.text_frame.paragraphs[0]
        p.text = stg
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    tb_c = s4.shapes.add_textbox(Inches(0.8), Inches(2.8), Inches(11.7), Inches(0.4))
    p_c = tb_c.text_frame.paragraphs[0]
    p_c.text = "Controls sitting on this process (Quality Gates)"
    p_c.font.size = Pt(14)
    p_c.font.bold = True
    p_c.font.color.rgb = NAVY_DARK

    ctrls = [
        ("On Inwarding (GRN)", "Batch lot, quantity, cost price, expiry must be filled. Dockside supplier verification against PO."),
        ("On Stock Ledger", "FEFO dynamic sorting; low-stock thresholds (≤20); 30/90-day expiry tags; 2-8°C IoT temperature alarms."),
        ("On POS Billing", "CDSS allergy cross-check; expired lot hard lockout; atomic transaction stock deduction; audit logging."),
        ("On Shift Close (Report)", "Daily Z-Report mathematical cash balancing; till variance detection; error logs feeding FMEA.")
    ]
    for idx, (c_name, c_desc) in enumerate(ctrls):
        r = idx // 2
        c_i = idx % 2
        x = Inches(0.8) + Inches(c_i * 5.95)
        y = Inches(3.4) + Inches(r * 1.7)
        add_card(s4, x, y, Inches(5.75), Inches(1.5))
        tb = s4.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), Inches(5.35), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = c_name
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = TEAL_ACCENT
        p2 = tf.add_paragraph()
        p2.text = c_desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(2)
    add_notes(s4, "Every step of our process map has active software controls sitting on it.")

    # =========================================================================
    # SLIDE 5: SIPOC & Stakeholder Requirements Matrix
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "SIPOC & Stakeholder Requirements Matrix")
    
    # Left: SIPOC
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_s = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True
    p = tf_s.paragraphs[0]
    p.text = "📊 SIPOC OF THE DISPENSING PROCESS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(8)
    sipoc_pts = [
        ("Suppliers: ", "Pharmaceutical distributors, attending doctors, SQLite database."),
        ("Inputs: ", "e-Prescription, batch lot, dispense qty, patient allergy EHR, cashier role."),
        ("Process: ", "Validate role → CDSS scan → FEFO pick → Deduct stock → Save + Audit."),
        ("Outputs: ", "Official GST invoice, thermal receipt, decremented stock, delivery order."),
        ("Customers: ", "Patient, cashier counter, store owner, state drug inspectors.")
    ]
    for b_t, n_t in sipoc_pts:
        p2 = tf_s.add_paragraph()
        r1 = p2.add_run()
        r1.text = b_t
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = NAVY_DARK
        r2 = p2.add_run()
        r2.text = n_t
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(6)

    # Right: Stakeholders
    add_card(s5, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_st = s5.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True
    p = tf_st.paragraphs[0]
    p.text = "👥 STAKEHOLDERS & CORE NEEDS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(8)
    stk_pts = [
        ("Patient: ", "Safe medication without allergens; transparent GST billing."),
        ("Cashier: ", "Fast sub-second billing; automated change return & dynamic UPI QR."),
        ("Pharmacist: ", "Real-time stock; CDSS allergy alerts; Schedule X narcotic register."),
        ("Admin / Owner: ", "Staff RBAC; live terminal presence; shift Z-Report cash balancing."),
        ("Auditor / Inspector: ", "21 CFR Part 11 immutable audit trail & 1-click narcotic CSV export.")
    ]
    for b_t, n_t in stk_pts:
        p2 = tf_st.add_paragraph()
        r1 = p2.add_run()
        r1.text = b_t
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = NAVY_DARK
        r2 = p2.add_run()
        r2.text = n_t
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(6)
    add_notes(s5, "SIPOC defines the operational boundaries; Stakeholder needs define acceptance criteria.")

    # =========================================================================
    # SLIDE 6: Measurable Requirements & Assigned Quality Goal Q01
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Measurable Requirements & Assigned Goal Q01")
    
    # Left: Measurable Viva Requirements
    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb1 = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🎯 MEASURABLE REQUIREMENTS (VIVA)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(8)
    viva_nums = [
        ("No Expired Sale: ", "Expired sales in a month = 0 (100% hard block at POS cart)."),
        ("Stock is True: ", "Physical inventory variance < 1.5% across all SKUs."),
        ("No Oversell: ", "Qty > stock attempts blocked = 100% via atomic assertion."),
        ("Trace Every Change: ", "100% of stock/price edits have user ID + timestamp in audit_logs."),
        ("Fast Search: ", "Barcode & generic search latency < 50ms (exceeds <3s target)."),
        ("Early Risk Flag: ", "Items ≤30d (red) and ≤90d (amber) automatically tagged on UI.")
    ]
    for b_t, n_t in viva_nums:
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

    # Right: Assigned Quality Goal Q01
    add_card(s6, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb2 = s6.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🏆 ASSIGNED QUALITY GOAL Q01: IMPROVE RELIABILITY"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(8)
    q01_pts = [
        ("1. Auto Backup: ", "Automated snapshot copy of pharmacy_system.db created daily in backups/."),
        ("2. Audit Log: ", "Captures who, action, old value, new value, terminal IP, and ISO timestamp."),
        ("3. Input Validation: ", "Stops blank names, negative prices, oversell quantities, bad dates."),
        ("4. Error Recovery: ", "Atomic rollback on commit failure; no half-created bill; friendly toasts."),
        ("5. User Roles (RBAC): ", "Store Admin, Pharmacist, Cashier, Inventory, Delivery strictly isolated.")
    ]
    for b_t, n_t in q01_pts:
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
    add_notes(s6, "In viva, examiners want numbers and core features. We deliver 5 concrete reliability features.")

    # =========================================================================
    # SLIDE 7: Modular 6-Tier Architecture & The Golden Rule
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Modular 6-Tier Architecture & The Golden Rule")
    
    # Left: Folder Structure
    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_tr = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_tr = tb_tr.text_frame
    tf_tr.word_wrap = True
    p = tf_tr.paragraphs[0]
    p.text = "📁 6-TIER FOLDER ARCHITECTURE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(8)
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

    # Right: Golden Rule
    add_card(s7, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1), bg_color=NAVY_CARD, border_color=TEAL_ACCENT)
    tb_gr = s7.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_gr = tb_gr.text_frame
    tf_gr.word_wrap = True
    p = tf_gr.paragraphs[0]
    p.text = "⭐ THE ONE RULE TO REMEMBER"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(8)

    p2 = tf_gr.add_paragraph()
    p2.text = "\"The screen must not talk to the database.\""
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_after = Pt(12)

    p3 = tf_gr.add_paragraph()
    p3.text = "UI  →  Service (Bridge)  →  Model / Database"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = BLUE_INFO
    p3.space_after = Pt(12)

    gr_reasons = [
        "• No SQL queries inside billing.py or any UI template.",
        "• All database operations are mediated by typed Python methods.",
        "• Failure isolation: UI bugs cannot corrupt database ACID commits.",
        "• Modularity allows independent testing and zero regression."
    ]
    for r in gr_reasons:
        p = tf_gr.add_paragraph()
        p.text = r
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(4)
    add_notes(s7, "The golden architectural rule: The screen must not talk to the database.")

    # =========================================================================
    # SLIDE 8: How a Click Travels (The 7-Step Pipeline)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s8, "How a Click Travels (The 7-Step Architectural Pipeline)", [
        ("1. Screen (UI Layer)", "billing.py captures user click, requested medicine SKU, and dosage quantity from input/barcode.", TEAL_ACCENT),
        ("2. Service (Bridge Layer)", "sales_service checks role authorization, verifies terminal session, and initiates transaction.", BLUE_INFO),
        ("3. CDSS Engine (Clinical Layer)", "medicine_service cross-checks patient EHR for penicillin/NSAID allergies and drug interactions.", CORAL_DANGER),
        ("4. Utils (Validators Layer)", "validators.py rejects bad inputs: checks non-blank, non-negative, and quantity <= available stock.", AMBER_WARN),
        ("5. Database (Storage Layer)", "db.py executes single ACID transaction: writes sales invoice and atomically cuts stock quantity.", NAVY_DARK),
        ("6. Proof (Audit Layer)", "audit_logs and error_logs receive append-only timestamped records containing user ID and payload.", PURPLE_ACCENT),
        ("7. Later (TQM Analytics Layer)", "tqm_report, Pareto charts, and FMEA tables aggregate logs to monitor and eliminate recurring defects.", BLUE_INFO)
    ])
    add_notes(s8, "Examiners love tracing a click from UI event to database commit and audit logging.")

    # =========================================================================
    # SLIDE 9: Database Design & Relational Schema (14 Tables)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "Database Design & Relational Schema (14 Tables)")
    
    # 2 Column Table Summary
    col_w = Inches(5.75)
    t_left = [
        ("1. staff", "Credentials, assigned RBAC role, branch, active status."),
        ("2. medicines", "SKU, generic, batch, expiry, days left, stock, MRP, rack."),
        ("3. prescriptions", "Patient name, doctor, items JSON, CDSS status, clinical notes."),
        ("4. invoices", "Fiscal tax invoices, cashier, subtotal, GST split, total."),
        ("5. delivery_orders", "Dispatch route, address, rider, cold-bag check, 4-digit OTP."),
        ("6. patients", "EHR profiles, contact phone, chronic diseases, recorded allergies."),
        ("7. suppliers", "Distributor directory, GSTIN, contact phone, payment terms.")
    ]
    t_right = [
        ("8. purchase_orders", "GRN inwarding, supplier, batch items JSON, total amount."),
        ("9. narcotic_register", "Schedule X: Doctor DMC Reg No, Pharmacist PIN, quantity."),
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
        p.text = "CORE RELATIONAL ENTITIES" if c_idx == 0 else "COMPLIANCE & TELEMETRY ENTITIES"
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
    add_notes(s9, "All 14 normalized tables in SQLite with migrations support ensuring existing test data is never wiped.")

    # =========================================================================
    # SLIDE 10: Role-Based CRUD Operations Matrix
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    crud_matrix = [
        ("Staff & RBAC", "CRUD", "R", "R", "R", "R"),
        ("Medicines & Stock", "CRUD", "R", "R, U (Deduct)", "CRUD", "R"),
        ("Prescriptions Queue", "R", "CRUD (Validate)", "R, U (Dispensed)", "R", "R"),
        ("Invoices & POS", "R", "R", "CR (Bill & Print)", "R", "R"),
        ("Delivery Orders", "R, D", "R", "C (Dispatch)", "R", "RU (OTP Verify)"),
        ("Narcotic Register", "R (Export CSV)", "CR (Double Sign)", "R", "R", "No Access"),
        ("Daily Z-Reports", "R, U (Audit Sign)", "No Access", "CR (Shift Close)", "No Access", "No Access")
    ]
    add_table_slide(s10, "Role-Based CRUD Operations Matrix", ["Module / Entity", "👑 Store Admin", "🩺 Pharmacist", "💳 Cashier", "📦 Inventory", "🛵 Delivery"], crud_matrix, [2.333, 1.8, 1.8, 1.8, 1.8, 1.8])
    add_notes(s10, "CRUD operations are partitioned by role to prevent unauthorized data mutations.")

    # =========================================================================
    # SLIDE 11: Software Features → TQM Concept Mapping
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    tqm_concepts = [
        ("Modular Architecture (6-Tier)", "System Approach / Process Organization (Deming)"),
        ("CDSS Allergy & Drug-Drug Shield", "Poka-Yoke Error Proofing at Source (Shingo)"),
        ("FEFO Batch Sequencing Algorithm", "Process Control & Inventory Wastage Elimination"),
        ("24/7 Cold-Chain IoT (2-8°C)", "Quality Assurance & Biological Preservation"),
        ("Daily Z-Report Till Reconciliation", "Fact-Based Management & Fiscal Governance (Juran)"),
        ("Immutable Audit Logs (21 CFR Part 11)", "Traceability, Accountability & Non-Repudiation"),
        ("Automated Error Logs & Telemetry", "Root-Cause Prioritization (Pareto 80/20) & FMEA"),
        ("Customer / Patient EHR Profiles", "Customer / Patient Focus (Zero-Defects Philosophy)")
    ]
    add_table_slide(s11, "Software Features → TQM Concept Mapping", ["Implemented Software Feature", "Academic TQM Quality Principle / Concept"], tqm_concepts, [5.0, 6.333])
    add_notes(s11, "This table connects software features directly to university quality management concepts.")

    # =========================================================================
    # SLIDE 12: Quality Dashboard & Operational Benchmarks
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_header(s12, "Quality Dashboard & Operational Benchmarks")
    q_metrics = [
        ("Stock Accuracy", "99.2%", "Zero unrecorded shrinkage", TEAL_ACCENT),
        ("Billing Errors", "0.0%", "Poka-Yoke blocks bad data", CORAL_DANGER),
        ("Expired Sales", "0.0%", "100% FEFO cart lockout", BLUE_INFO),
        ("Till Variance", "₹ 0.00", "Z-Report cash balanced", NAVY_DARK)
    ]
    col_w = Inches(2.78)
    for idx, (title, val, desc, col) in enumerate(q_metrics):
        x = Inches(0.8) + Inches(idx * 2.98)
        add_card(s12, x, Inches(1.8), col_w, Inches(1.8))
        tb = s12.shapes.add_textbox(x + Inches(0.15), Inches(1.95), col_w - Inches(0.3), Inches(1.5))
        tf = tb.text_frame
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK
        p2 = tf.add_paragraph()
        p2.text = val
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = col
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = TEXT_MUTED

    benchmarks = [
        ("Quality Dimension", "Traditional Retail Pharmacy (Manual)", "AegisPharm Enterprise (TQM Driven)"),
        ("Prescription Safety", "Manual check; vulnerable to handwriting errors", "Automated CDSS cross-checks with patient allergy EHR"),
        ("Inventory Picking", "Random or FIFO; older batches expire on shelves", "Algorithmic FEFO (First-Expiry, First-Out) guarantee"),
        ("Cold-Chain Monitoring", "Infrequent manual thermometer checks; silent loss", "Continuous 30s IoT telemetry with automatic alarm alerts"),
        ("Shift Cash Balancing", "Paper ledger estimations; undetected shrinkage", "Daily Z-Report mathematical reconciliation & signed Z-slip")
    ]
    add_card(s12, Inches(0.8), Inches(3.9), Inches(11.733), Inches(3.0))
    tb_b = s12.shapes.add_textbox(Inches(1.0), Inches(4.0), Inches(11.3), Inches(2.8))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "📊 TRADITIONAL PHARMACY VS. AEGISPHARM TQM BENCHMARK"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(6)
    for r_idx, (c1, c2, c3) in enumerate(benchmarks):
        p = tf_b.add_paragraph()
        p.text = f"{c1:<22} | {c2:<44} | {c3}"
        p.font.size = Pt(9.5)
        p.font.bold = (r_idx == 0)
        p.font.color.rgb = TEAL_ACCENT if r_idx == 0 else TEXT_MAIN
        p.space_after = Pt(2)
    add_notes(s12, "Empirical quality metrics prove that AegisPharm eliminates common manual dispensary vulnerabilities.")

    # =========================================================================
    # SLIDE 13: Quality Analysis Tools: Pareto (80/20) & Fishbone
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13)
    add_header(s13, "Quality Analysis Tools: Pareto (80/20) & Fishbone")
    
    # Left: Pareto 80/20
    add_card(s13, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb1 = s13.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
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
    add_card(s13, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb2 = s13.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
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
    add_notes(s13, "Pareto and Fishbone tools identify why errors happen and guide our software controls.")

    # =========================================================================
    # SLIDE 14: FMEA (Failure Mode and Effects Analysis) & Feedback Loops
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_bg(s14)
    add_header(s14, "FMEA & How Telemetry Logs Feed Risk Reduction")
    
    # Left: FMEA Table
    add_card(s14, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb1 = s14.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
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

    # Right: How Logs Feed FMEA
    add_card(s14, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb2 = s14.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🔄 HOW ERROR LOGS FEED FMEA & IMPROVEMENT"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(6)
    feed_steps = [
        ("1. Attempt Blocked: ", "Cashier attempts bad action or system encounters exception."),
        ("2. Log Appended: ", "error_logs and audit_logs record error code (E01-E05) + user."),
        ("3. Aggregation: ", "tqm_report counts monthly frequency of each error code."),
        ("4. Dynamic Occurrence: ", "High frequency automatically raises Occurrence (O) score in FMEA."),
        ("5. Prioritized Action: ", "High RPN items trigger software updates and staff retraining.")
    ]
    for b_t, n_t in feed_steps:
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
    add_notes(s14, "FMEA quantifies risks; error logs dynamically feed the Occurrence metric.")

    # =========================================================================
    # SLIDE 15: Deming PDCA Cycle & Transaction Flows
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_bg(s15)
    add_header(s15, "Deming PDCA Cycle & Transaction Workflows")
    
    # Left: PDCA Cycle
    add_card(s15, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb1 = s15.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🔁 DEMING PDCA QUALITY CYCLE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(6)
    pdca_items = [
        ("PLAN: ", "Identify excessive oversell and near-expiry mistakes during peak rush."),
        ("DO: ", "Deploy automated FEFO batch picker and pre-save stock balance locks."),
        ("CHECK: ", "Monitor monthly counts of error codes E01 and E03 in error_logs."),
        ("ACT: ", "Standardize FEFO logic across all terminals as mandatory baseline policy.")
    ]
    for b_t, n_t in pdca_items:
        p2 = tf1.add_paragraph()
        r1 = p2.add_run()
        r1.text = b_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = TEAL_ACCENT
        r2 = p2.add_run()
        r2.text = n_t
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)

    # Right: Transaction Flows
    add_card(s15, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb2 = s15.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "⚡ SALE & PURCHASE WORKFLOW SEQUENCES"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(6)
    flows = [
        ("Dispensing Sale Flow: ", "Login → POS Billing → Barcode / 1-Click eRx → Qty → Validate → Stock Check → Expiry Check → ACID Commit & Thermal Receipt."),
        ("Consignment Purchase Flow: ", "Supplier Pick → Inwarding Modal (GRN) → Batch & Expiry Entry → Validate → Stock Increment → Reorder Evaluation → Telemetry Alert.")
    ]
    for b_t, n_t in flows:
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
        p2.space_after = Pt(6)
    add_notes(s15, "PDCA guarantees Kaizen (continuous improvement); sales and purchase flows show clean operational steps.")

    # =========================================================================
    # SLIDE 16: Working Application Live Demo: Setup & Personas
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_bg(s16)
    add_header(s16, "Working Application Demo Guide: Setup & Personas")
    
    # Left: Startup Commands
    add_card(s16, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb1 = s16.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🚀 APPLICATION LAUNCH COMMANDS"
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

    # Right: Personas Table
    personas = [
        ("👑 Admin", "`admin` / `admin123`", "RBAC, live heartbeats, Z-Report balancing"),
        ("🩺 Pharmacist", "`pharmacist` / `pharma123`", "CDSS allergy scan, Schedule X narcotic sign-off"),
        ("💳 Cashier", "`cashier` / `cash123`", "1-Click eRx import, FEFO batch, UPI QR, receipt"),
        ("📦 Inventory", "`inventory` / `inv123`", "Multi-batch ledger, GRN inwarding, 2-8°C IoT"),
        ("🛵 Delivery", "`delivery` / `deliv123`", "Kanban dispatch, cold-bag check, OTP e-POD")
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
    add_notes(s16, "The live demo setup: commands to boot tests, desktop app, web app, and pre-seeded credentials.")

    # =========================================================================
    # SLIDE 17: Live Demonstration Workflow: Quality Gates in Action
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s17, "Live Demonstration Workflow: Quality Gates in Action", [
        ("Phase 1: Clinical Pharmacist & CDSS Gate", "Review incoming eRx queue. Trigger CDSS Allergy Interception (Penicillin warning blocks checkout). Execute Schedule X Narcotic double sign-off with Doctor DMC No + Pharmacist PIN.", TEAL_ACCENT),
        ("Phase 2: POS Cashier Express Billing", "1-Click import approved eRx into cart. Verify automatic FEFO nearest-expiry batch selection. Tender checkout: enter Cash (auto change calc) or Dynamic UPI QR. Print 80mm GST receipt.", BLUE_INFO),
        ("Phase 3: Inventory FEFO & Cold-Chain IoT", "Inspect batch ledger with countdown badges (<30d Red, <90d Yellow). Click 'Simulate Temp Spike' (9.4°C) on Chamber A fridge → observe immediate visual alert & log entry.", CORAL_DANGER),
        ("Phase 4: Fulfilment Fleet & OTP Handover", "Advance order on Kanban dispatch board. Verify insulated cold-bag checklist. Enter customer 4-digit SMS OTP (1234) to confirm electronic Proof-of-Delivery (e-POD).", AMBER_WARN),
        ("Phase 5: Admin Command Center & Z-Report Close", "Monitor live terminal presence heartbeats. Open Daily Z-Report module: enter physical cash counted, verify variance (Balanced ₹0.00), sign and lock shift register.", NAVY_DARK)
    ])
    add_notes(s17, "This 5-phase script guides the live application demonstration before examiners.")

    # =========================================================================
    # SLIDE 18: Review 1 vs Review 2 Roadmap & Golden Viva Closing
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
    p0.text = "REVIEW 1 VS REVIEW 2 ROADMAP & VIVA CONCLUSION"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = TEAL_ACCENT
    p0.space_after = Pt(6)

    p1 = tf.add_paragraph()
    p1.text = "Review 1 Delivered vs Review 2 Horizon"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(8)

    roadmap = [
        ("Review 1 Delivered (Now): ", "Complete 6-tier architecture, IEEE 830 SRS, 14 tables, working desktop & web UIs, CDSS allergy interception, FEFO batch dispensing, Daily Z-Report till balancing, 24/24 passing tests."),
        ("Review 2 Scope (Horizon): ", "Longitudinal FMEA occurrence tracking from error logs, automated real-time Pareto charts, Ishikawa incident registry, and multi-branch cloud database replication.")
    ]
    for b_t, n_t in roadmap:
        p2 = tf.add_paragraph()
        r1 = p2.add_run()
        r1.text = b_t
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = TEAL_LIGHT
        r2 = p2.add_run()
        r2.text = n_t
        r2.font.size = Pt(10)
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
    add_notes(s18, "Closing statement: Review 1 is 100% delivered. Deliver the golden sentence and open for questions.")

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AegisPharm_TQM_Presentation_Piyush_Bhatt.pptx")
    prs.save(output_path)
    print(f"[SUCCESS] Compact 18-Slide PowerPoint generated successfully at: {output_path}")

    # Export to PDF via PowerPoint COM
    try:
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AegisPharm_TQM_Presentation_Piyush_Bhatt.pdf")
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        deck = ppt_app.Presentations.Open(os.path.abspath(output_path), WithWindow=False)
        deck.SaveAs(os.path.abspath(pdf_path), 32)
        deck.Close()
        ppt_app.Quit()
        print(f"[SUCCESS] Compact 18-Slide PDF generated successfully at: {pdf_path}")
    except Exception as e:
        print(f"[WARNING] PowerPoint COM export failed: {e}")

if __name__ == "__main__":
    build_compact_deck()
