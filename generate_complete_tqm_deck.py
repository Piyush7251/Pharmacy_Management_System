"""
TQM Pharm Enterprise — Review 1 & 2 Complete Master Deck Generator.
Author: Piyush Bhatt, Amrapali University.
Generates an executive-level 79-slide widescreen (16:9) PowerPoint presentation (.pptx)
strictly structured around the exact headings and topics from the university demonstration syllabus:
Review 1 & Review 2: Process Map, Stakeholders, Measurable Requirements, Quality Goals,
Modular Architecture, Database Design, Service Engines, UI Screens, TQM Analytics,
Pareto, Fishbone, FMEA, PDCA, and Viva Defense.
"""

import os
import win32com.client
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
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
    PURPLE_ACC = PURPLE_ACCENT

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
        """Utility for vertical card stacks (e.g. 2 to 5 cards)"""
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
        """Utility for table slides"""
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

        # Headers
        for idx, h_text in enumerate(headers):
            cell = tbl.cell(0, idx)
            cell.text = h_text
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY_DARK
            p = cell.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_WHITE

        # Rows
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
    # SLIDE 1: Title (Cover)
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
    p0.text = "SRS REVIEW 1 & 2 · PROCESS + QUALITY"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = TEAL_ACCENT
    p0.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "Process map, stakeholders,\nmeasurable requirements,\nquality goals"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "Pharmacy Management System (TQM Pharm Enterprise)\nQuality Goal: Q01 Improve Reliability & Zero-Defects"
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
    p_u3.text = "B.Tech CSE Project Review 1 & 2\nAcademic Year 2026"
    p_u3.font.size = Pt(12)
    p_u3.font.color.rgb = RGBColor(203, 213, 225)

    add_notes(s1, "Respected evaluators, I am Piyush Bhatt from Amrapali University. Today I present our complete Process + Quality review covering Review 1 and 2.")

    # =========================================================================
    # SLIDE 2: Vision, mission, quality objective
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s2, "Vision, mission, quality objective", [
        ("VISION", "A pharmacy where no expired or wrong medicine leaves the counter.", TEAL_ACCENT),
        ("MISSION", "Build a high-performance desktop and web system that records stock, blocks unsafe sales via clinical CDSS, and shows who did what.", BLUE_INFO),
        ("QUALITY OBJECTIVE OF THIS SOFTWARE", "Prevent the error at the source.\nControl the process. Monitor it with immutable logs and automated telemetry.", NAVY_DARK)
    ])
    add_notes(s2, "Our vision and mission directly translate into TQM controls: stop the error at source, control every transaction, and log everything.")

    # =========================================================================
    # SLIDE 3: Three quality ideas behind the software
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Three quality ideas behind the software")
    col_w = Inches(3.64)
    gap = Inches(0.4)
    top_pos = Inches(1.8)
    h_pos = Inches(5.1)

    cards3 = [
        ("Error prevention at source", "Poka-yoke\n\n• Blank medicine name blocked.\n• Qty > available stock blocked.\n• Expired item blocked from cart.\n• Allergen contraindication blocked.", CORAL_DANGER),
        ("Process control", "One path for work\n\n• Inwarding (GRN) → Stock (FEFO)\n  → CDSS Clinical Gate → Bill\n  → Z-Report Shift Close.\n• UI cannot skip business rules.", BLUE_INFO),
        ("Monitoring", "See and trace\n\n• Real-time dashboard alerts.\n• 24/7 cold-chain telemetry logs.\n• Immutable append-only audit trail.\n• Error logs feeding FMEA & Pareto.", TEAL_ACCENT)
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
    # SLIDE 4: Process map
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Process map")
    # Flow boxes
    stages4 = ["Supplier", "Purchase", "Stock", "Bill", "Customer", "Report"]
    box_w = Inches(1.8)
    for idx, stg in enumerate(stages4):
        x = Inches(0.8) + Inches(idx * 1.98)
        add_card(s4, x, Inches(1.8), box_w, Inches(0.8), bg_color=NAVY_DARK, border_color=TEAL_ACCENT)
        tb = s4.shapes.add_textbox(x, Inches(1.95), box_w, Inches(0.5))
        p = tb.text_frame.paragraphs[0]
        p.text = stg
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    # Controls title
    tb_c = s4.shapes.add_textbox(Inches(0.8), Inches(2.8), Inches(11.7), Inches(0.4))
    p_c = tb_c.text_frame.paragraphs[0]
    p_c.text = "Controls sitting on this process"
    p_c.font.size = Pt(14)
    p_c.font.bold = True
    p_c.font.color.rgb = NAVY_DARK

    ctrls = [
        ("On Purchase", "Batch, qty, cost, expiry must be filled. GRN dock verification against PO."),
        ("On Stock", "Low-stock threshold alerts (≤20) and 30/90-day expiry lists. 2-8°C IoT temperature monitor."),
        ("On Bill", "CDSS allergy scan + FEFO batch picking + expired lot block + atomic stock deduction + audit."),
        ("On Report", "Daily Z-Report cash drawer balancing. Measure transaction errors and expired stock %.")
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
    # SLIDE 5: SIPOC of the sale process
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "SIPOC of the sale process")
    sipoc = [
        ("S (Suppliers)", "• Supplier\n• Pharmacist\n• Doctor (eRx)\n• SQLite DB"),
        ("I (Inputs)", "• Medicine Batch\n• Dispense Qty\n• Patient EHR\n• Cashier Role\n• Payment Tender"),
        ("P (Process)", "• Validate Staff Role\n• CDSS Allergy Check\n• Pick FEFO Batch\n• Deduct Stock\n• Save + Write Audit"),
        ("O (Outputs)", "• Tax Invoice\n• 80mm Receipt\n• Decremented Stock\n• Audit Log Row\n• Delivery Order"),
        ("C (Customers)", "• Patient\n• Cashier\n• Store Owner\n• Drug Auditor")
    ]
    col_w = Inches(2.22)
    for idx, (title, content) in enumerate(sipoc):
        x = Inches(0.8) + Inches(idx * 2.37)
        add_card(s5, x, Inches(1.8), col_w, Inches(5.1))
        hb = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), col_w, Inches(0.6))
        hb.fill.solid()
        hb.fill.fore_color.rgb = NAVY_DARK if idx % 2 == 0 else TEAL_ACCENT
        hb.line.fill.background()
        tb = s5.shapes.add_textbox(x, Inches(1.85), col_w, Inches(0.5))
        p = tb.text_frame.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb2 = s5.shapes.add_textbox(x + Inches(0.1), Inches(2.5), col_w - Inches(0.2), Inches(4.2))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        for line in content.split('\n'):
            p = tf2.add_paragraph() if tf2.paragraphs[0].text else tf2.paragraphs[0]
            p.text = line
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(4)
    add_notes(s5, "SIPOC defines the Suppliers, Inputs, Process, Outputs, and Customers of our dispensing pipeline.")

    # =========================================================================
    # SLIDE 6: Stakeholders and their need
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s6, "Stakeholders and their need", [
        ("Patient", "Safe medicine without allergens or contraindications. Correct GST bill. Transparent pricing.", TEAL_ACCENT),
        ("Cashier", "Fast sub-second billing. Clear block if stock is short. Automated cash change & dynamic UPI QR.", BLUE_INFO),
        ("Pharmacist", "True physical stock. Expiry visible. Automated CDSS drug interaction & Schedule X register.", NAVY_DARK),
        ("Admin / Owner", "User roles, live terminal heartbeats, daily Z-Reports, dead-stock analysis, quality numbers.", PURPLE_ACCENT),
        ("Supplier", "Received quantity recorded against Purchase Order (GRN). Payment terms tracking.", AMBER_WARN),
        ("Auditor / Inspector", "Who changed stock or sold what. Immutable 21 CFR Part 11 audit trails & narcotic CSV export.", CORAL_DANGER)
    ])
    add_notes(s6, "Every stakeholder has explicit functional and quality requirements addressed by TQM Pharm.")

    # =========================================================================
    # SLIDE 7: Measurable requirements (viva)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Measurable requirements (viva)")
    meas_data = [
        ("No expired sale", "Expired sales in a month = 0 (100% hard block at POS cart)"),
        ("Stock is true", "Physical inventory variance < 1.5% across all SKUs"),
        ("No oversell", "Qty > stock attempts blocked = 100% (atomic transaction validation)"),
        ("Trace every change", "100% of stock, price, and dispense actions have user ID + timestamp in audit_logs"),
        ("Find a drug fast", "Database barcode/generic search latency < 50 milliseconds (exceeds <3s target)"),
        ("See risk early", "Items ≤30 days (red) and ≤90 days (amber) automatically tagged on dashboard")
    ]
    add_stacked_cards(s7, "Measurable requirements (viva) — Need → Number we can count", meas_data)
    add_notes(s7, "In viva, examiners want numbers: zero expired sales, <1.5% variance, 100% oversell blocking, <50ms search.")

    # =========================================================================
    # SLIDE 8: Measurable quality objectives
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s8, "Measurable quality objectives", [
        ("O1", "Zero expired items on any saved sales invoice.", TEAL_ACCENT),
        ("O2", "Every sale either saves fully or not at all (100% ACID transaction atomicity).", BLUE_INFO),
        ("O3", "Every user action on stock, billing, and credentials is recorded in immutable audit_logs.", NAVY_DARK),
        ("O4", "Automated database backup snapshot created at least once a day and on application exit.", AMBER_WARN),
        ("O5", "Authentication and operations fail safely. System catches exceptions; app does not crash.", CORAL_DANGER)
    ])
    add_notes(s8, "Our 5 core quality objectives form the baseline contract for system acceptance.")

    # =========================================================================
    # SLIDE 9: Assigned quality goal Q01
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s9, "Assigned quality goal Q01: Improve Reliability — five features we will build", [
        ("Auto Backup", "Automated snapshot copy of pharmacy_system.db created daily and stored in backups/.", TEAL_ACCENT),
        ("Audit Log", "Records who, action, old value, new value, terminal IP, and ISO timestamp.", BLUE_INFO),
        ("Input Validation", "Stops blank medicine names, negative prices, oversell quantities, and invalid dates.", NAVY_DARK),
        ("Error Recovery", "If database commit fails, show friendly toast alert; atomic rollback ensures no half-created bill.", AMBER_WARN),
        ("User Roles", "Store Admin, Pharmacist, Cashier, Inventory Manager, Delivery Agent only see authorized workstations.", PURPLE_ACCENT)
    ])
    add_notes(s9, "Quality Goal Q01 is Improve Reliability, delivered through 5 foundational software engineering features.")

    # =========================================================================
    # SLIDE 10: Feature → quality idea
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s10, "Feature → quality idea", [
        ("Input Validation", "Error prevention at source (Poka-Yoke error-proofing).", TEAL_ACCENT),
        ("User Roles", "Process control + accountability (Role-Based Access Control).", BLUE_INFO),
        ("Audit Log", "Monitoring + traceability (FDA 21 CFR Part 11 immutable trail).", NAVY_DARK),
        ("Error Recovery", "Reliability. ACID transaction integrity; no broken or corrupted bill.", AMBER_WARN),
        ("Auto Backup", "Reliability & Resilience. Data is never lost; disaster recovery enabled.", PURPLE_ACCENT)
    ])
    add_notes(s10, "Every software feature in TQM Pharm maps directly to a formal TQM quality principle.")

    # =========================================================================
    # SLIDE 11: Crucial mapping (say this)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s11, "Crucial mapping (say this)", [
        ("Customer need:", "Safe medication dispensing without allergic conflicts or billing errors.", TEAL_ACCENT),
        ("Measurable requirement:", "Expired sales = 0; Adverse interaction escapes = 0.", CORAL_DANGER),
        ("Process control:", "POS billing cannot skip CDSS allergy check or inventory stock/expiry validation.", NAVY_DARK),
        ("Monitoring:", "Immutable audit_logs + error_logs telemetry + real-time presence dashboard.", BLUE_INFO),
        ("Quality goal:", "Q01 Reliability & Zero-Defect architecture implemented across all 6 tiers.", PURPLE_ACCENT)
    ])
    add_notes(s11, "This is the exact logical chain for viva: Customer Need -> Measurable Requirement -> Process Control -> Monitoring -> Quality Goal.")

    # =========================================================================
    # SLIDE 12: One-line viva
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s12, "One-line viva", [
        ("Requirement:", "No expired or contraindicated medicine dispensed.", TEAL_ACCENT),
        ("Objective:", "Expired invoices this month = 0; Till variance = ₹0.00.", BLUE_INFO),
        ("How:", "Validate at intake (CDSS), control the dispensing path (FEFO), and monitor with audit and error logs.", NAVY_DARK)
    ])
    add_notes(s12, "If asked for a 10-second summary: Validate at entry, control the bill path, and monitor with audit and error logs.")

    # =========================================================================
    # SLIDE 13: CASE: Pharmacy Management System
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13, NAVY_DARK)
    tb = s13.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "CASE: Pharmacy Management System"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(14)
    p2 = tf.add_paragraph()
    p2.text = "Every folder, every screen, every table.\nSimple enough to explain from the last row."
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.space_after = Pt(14)
    p3 = tf.add_paragraph()
    p3.text = "Quality-oriented system | Modular design | TQM controls"
    p3.font.size = Pt(15)
    p3.font.bold = True
    p3.font.color.rgb = TEAL_ACCENT
    add_notes(s13, "Transition to our architectural deep-dive: examining every folder, screen, and database table.")

    # =========================================================================
    # SLIDE 14: Project Folder Structure (Visual Tree)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_bg(s14)
    add_header(s14, "Project folder structure")
    add_card(s14, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1))
    tb = s14.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.2), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    tree = """Pharmacy_Management_System/
├── core/
│   ├── bridge.py         # Unified Python RPC Bridge (38 methods)
│   ├── db.py             # SQLite persistence layer (14 normalized tables)
│   ├── api_client.py     # Presence heartbeat & background connector
│   └── logger.py         # 21 CFR Part 11 append-only audit logger
├── config/
│   └── settings.py       # Thread-safe Singleton dataclass (config.json)
├── ui/
│   ├── desktop/          # Edge Chromium WebView2 60 FPS clinical frontend
│   └── web/              # Cloud-ready FastAPI Web UI (1:1 feature parity)
├── apps/                 # Standalone workstation modules (admin, cashier, pharma, inv, deliv)
├── tests/                # 24 Automated unit & integration tests (pytest)
├── backups/              # Automated SQLite snapshot archives (.db) & CSV logs
├── main.py               # Hardware-accelerated desktop workstation entrypoint
└── web_app.py            # Asynchronous FastAPI web server runtime"""
    for line in tree.split('\n'):
        p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(10)
        p.font.name = "Consolas"
        p.font.color.rgb = TEXT_MAIN
    add_notes(s14, "Our folder structure strictly adheres to clean modular separation.")

    # =========================================================================
    # SLIDE 15: His structure is already good
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s15, "His structure is already good", [
        ("main.py", "Application boot director. Initializes settings, connects SQLite, verifies schema, mounts bridge, opens login.", TEAL_ACCENT),
        ("database/ (core/db.py)", "Central data persistence: connection pooling, WAL journaling, 14 tables, migrations, and ACID transactions.", BLUE_INFO),
        ("models/ (core/models)", "Domain entities: Staff, Medicine, Supplier, Patient EHR, Prescriptions, Invoices, Delivery.", NAVY_DARK),
        ("services/ (core/bridge.py)", "Business rules: Auth service, CDSS safety, FEFO batch picker, POS billing, GRN inwarding.", PURPLE_ACCENT),
        ("ui/ (ui/desktop + ui/web)", "User presentation: Login portal, clinical dispensing, POS cashier, inventory hub, delivery dock.", AMBER_WARN),
        ("reports/ (core/reports)", "Management decisions: Daily Z-Reports, sales ledger, expiry countdowns, audit stream.", CORAL_DANGER)
    ])
    add_notes(s15, "The structure provides a dedicated home for every single responsibility.")

    # =========================================================================
    # SLIDE 16: What each folder means
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s16, "What each folder means", [
        ("ui/", "What the user sees (presentation layer: HTML5/CSS3 glassmorphism & CustomTkinter widgets).", TEAL_ACCENT),
        ("services/ (core/bridge.py)", "Business rules & TQM algorithms (CDSS contraindication checks, FEFO sorting, tax formulas).", BLUE_INFO),
        ("models/", "What a User / Medicine / Sale / Prescription is (clean typed data structures).", NAVY_DARK),
        ("database/ (core/db.py)", "How data is stored (SQLite 3 relational engine, foreign keys, constraints, and transactions).", PURPLE_ACCENT),
        ("reports/", "Numbers for decisions (Daily Z-Reports, variance calculations, expiry risk, and tax summaries).", AMBER_WARN),
        ("main.py", "Starts the program only (orchestrates startup sequence and loads UI).", CORAL_DANGER)
    ])
    add_notes(s16, "Clear mental model: UI displays, Services decide, Database stores, Reports summarize, main boots.")

    # =========================================================================
    # SLIDE 17: Why this folder structure?
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s17, "Why this folder structure?", [
        ("• One job per folder. Easy to explain.", "Evaluators can immediately locate any feature without hunting through monolithic spaghetti code.", TEAL_ACCENT),
        ("• A bug in billing does not hide inside main.py.", "Failure isolation: bugs remain contained within their domain service without corrupting startup or storage.", BLUE_INFO),
        ("• Validation and audit have a dedicated home.", "Every input check lives in validators; every critical event logs to immutable audit trails.", NAVY_DARK),
        ("• You can build one layer at a time.", "Supports incremental agile development and test-driven verification (TDD).", PURPLE_ACCENT)
    ])
    add_notes(s17, "Modularity reduces cognitive load and guarantees long-term maintainability.")

    # =========================================================================
    # SLIDE 18: The one rule to remember
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_bg(s18, NAVY_DARK)
    tb = s18.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "The one rule to remember"
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.font.color.rgb = TEAL_ACCENT
    p1.space_after = Pt(12)
    p2 = tf.add_paragraph()
    p2.text = "The screen must not talk to the database."
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_after = Pt(20)
    p3 = tf.add_paragraph()
    p3.text = "UI  →  Service (Bridge)  →  Model / Database"
    p3.font.size = Pt(22)
    p3.font.bold = True
    p3.font.color.rgb = BLUE_INFO
    p3.space_after = Pt(14)
    p4 = tf.add_paragraph()
    p4.text = "No 'SELECT * FROM medicines' inside billing.py or any UI file.\nAll database queries are mediated by typed Python service methods."
    p4.font.size = Pt(15)
    p4.font.color.rgb = RGBColor(203, 213, 225)
    add_notes(s18, "This architectural rule guarantees security, testability, and prevents SQL injection.")

    # =========================================================================
    # SLIDE 19: What you must be able to explain
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s19, "What you must be able to explain (Viva Pillars)", [
        ("1. What each folder is for", "Explain how core, ui, config, server, and tests decouple presentation, domain logic, and persistence.", TEAL_ACCENT),
        ("2. How a click travels: UI → Service → Database", "Trace button click from UI event, through RPC Bridge validation, CDSS check, to SQLite ACID commit.", BLUE_INFO),
        ("3. What data sits in each table", "Explain our 14 normalized tables: staff, medicines, prescriptions, invoices, delivery, telemetry, Z-reports.", NAVY_DARK),
        ("4. How this is TQM, not only CRUD", "Show Poka-Yoke error blocking, FEFO batch expiry optimization, 2-8°C cold chain telemetry, and shift Z-Report balancing.", PURPLE_ACCENT)
    ])
    add_notes(s19, "These 4 questions represent the core of the evaluation viva.")

    # =========================================================================
    # SLIDE 20: Suggested full folder structure
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    set_bg(s20)
    add_header(s20, "Suggested full folder structure")
    # 3-column layout
    col_w = Inches(3.64)
    cols = [
        ("Core & Database", "├── main.py\n├── config/\n│   └── settings.py\n├── database/ (core/)\n│   ├── db.py\n│   ├── schema.py\n│   └── migrations.py\n├── models/\n│   ├── user.py\n│   ├── medicine.py\n│   ├── supplier.py\n│   ├── customer.py\n│   ├── sale.py\n│   └── purchase.py"),
        ("Services & UI", "├── services/ (bridge.py)\n│   ├── auth_service.py\n│   ├── medicine_service.py\n│   ├── search_service.py\n│   ├── sales_service.py\n│   ├── purchase_service.py\n│   ├── inventory_service.py\n│   └── report_service.py\n├── ui/\n│   ├── login.py\n│   ├── dashboard.py\n│   ├── medicines.py\n│   ├── billing.py\n│   └── users.py"),
        ("Reports & Utils", "├── reports/\n│   ├── sales_report.py\n│   ├── inventory_report.py\n│   ├── expiry_report.py\n│   └── tqm_report.py\n├── utils/\n│   ├── validators.py\n│   ├── logger.py\n│   ├── security.py\n│   └── helpers.py\n├── assets/\n│   ├── icons/\n│   └── logo/")
    ]
    for idx, (title, text) in enumerate(cols):
        x = Inches(0.8) + Inches(idx * 4.04)
        add_card(s20, x, Inches(1.8), col_w, Inches(5.1))
        hb = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), col_w, Inches(0.6))
        hb.fill.solid()
        hb.fill.fore_color.rgb = NAVY_DARK if idx % 2 == 0 else TEAL_ACCENT
        hb.line.fill.background()
        tb = s20.shapes.add_textbox(x, Inches(1.85), col_w, Inches(0.5))
        p = tb.text_frame.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb2 = s20.shapes.add_textbox(x + Inches(0.1), Inches(2.5), col_w - Inches(0.2), Inches(4.2))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        for line in text.split('\n'):
            p = tf2.add_paragraph() if tf2.paragraphs[0].text else tf2.paragraphs[0]
            p.text = line
            p.font.size = Pt(9.5)
            p.font.name = "Consolas"
            p.font.color.rgb = TEXT_MAIN
    add_notes(s20, "Detailed file layout mapped across Core, Services, UI, Reports, and Utils.")

    # =========================================================================
    # SLIDE 21: What each file does — start + config + database
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s21, "What each file does — start + config + database", [
        ("main.py", "Starts the application. Loads settings, connects DB, verifies tables, and presents login.", TEAL_ACCENT),
        ("config/settings.py", "Application name, DB path, expiry threshold days (30/90), reorder level, invoice prefix.", BLUE_INFO),
        ("database/db.py", "Opens SQLite, runs parameterized queries, commits/rollbacks ACID transactions, closes connections.", NAVY_DARK),
        ("database/schema.py", "Creates 14 normalized tables with primary keys, checks, foreign keys, and default values.", PURPLE_ACCENT),
        ("database/migrations.py", "Applies ALTER TABLE schema migrations without wiping existing patient, stock, or audit data.", AMBER_WARN)
    ])
    add_notes(s21, "The startup, configuration, and database layer handle infrastructure cleanly.")

    # =========================================================================
    # SLIDE 22: What each file does — models
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s22, "What each file does — models", [
        ("models/user.py", "Staff user entity: ID, full name, username, hashed password, assigned role, active status.", TEAL_ACCENT),
        ("models/medicine.py", "Pharmaceutical entity: SKU, generic, batch lot, stock qty, cost, MRP, expiry date, rack, cold-chain flag.", BLUE_INFO),
        ("models/supplier.py", "Distributor entity: ID, corporate name, GSTIN, phone, email, address, credit payment terms.", NAVY_DARK),
        ("models/customer.py (patient)", "Patient entity: ID, name, phone, allergy array (Penicillin), chronic diseases, loyalty points.", PURPLE_ACCENT),
        ("models/sale.py", "Invoice entity: Invoice ID, cashier, subtotal, GST split, payment method (Cash/UPI/Card), items JSON.", AMBER_WARN),
        ("models/purchase.py", "Goods Receipt Note (GRN) entity: PO reference, supplier, received date, items list, total value.", CORAL_DANGER)
    ])
    add_notes(s22, "Models represent pure business objects decoupled from presentation and raw SQL.")

    # =========================================================================
    # SLIDE 23: What each file does — services
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s23, "What each file does — services", [
        ("auth_service.py", "Authentication, logout, SHA-256 password hashing, RBAC role check, session heartbeats.", TEAL_ACCENT),
        ("medicine_service.py", "Add, edit, deactivate medicines; adjust stock delta; verify expiry dates before cart addition.", BLUE_INFO),
        ("search_service.py", "Sub-50ms search by brand name, generic molecule, manufacturer, or USB barcode scan.", NAVY_DARK),
        ("sales_service.py", "Create invoice, validate stock availability, compute GST tax split, deduct stock, append audit row.", PURPLE_ACCENT),
        ("purchase_service.py", "Receive supplier shipment against PO, verify inward batch details, atomically increment stock.", AMBER_WARN),
        ("inventory_service.py", "FEFO batch ledger, low stock alerts (≤20 units), expired list, 30/90-day countdown tags.", BLUE_INFO),
        ("report_service.py", "Aggregate revenue totals, cash drawer reconciliation (Z-Report), expiry write-offs, quality KPIs.", CORAL_DANGER)
    ])
    add_notes(s23, "Services encapsulate all business logic, clinical rules, and transaction boundaries.")

    # =========================================================================
    # SLIDE 24: What each file does — UI screens
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s24, "What each file does — UI screens", [
        ("ui/login.py", "Workstation Persona Grid: visual station tiles for 1-click credential loading and terminal assignment.", TEAL_ACCENT),
        ("ui/dashboard.py", "KPI command center: today's sales, low-stock count, near-expiry alerts, online terminal ticker.", BLUE_INFO),
        ("ui/medicines.py", "Pharmaceutical catalog table with Add/Edit/Deactivate modals and visual countdown badges.", NAVY_DARK),
        ("ui/inventory.py", "Stock ledger views: All batches, Low stock, Expired, 30 days, 90 days, and manual adjustments.", PURPLE_ACCENT),
        ("ui/suppliers.py & customers.py", "Distributor directory and patient EHR profiles with registered drug allergies.", AMBER_WARN),
        ("ui/purchases.py & search.py", "Goods Receipt Note (GRN) inwarding modal and instant multi-parameter barcode search box.", BLUE_INFO),
        ("ui/billing.py & users.py", "POS checkout with 1-click eRx import, split payment, thermal receipt, and Admin user manager.", CORAL_DANGER)
    ])
    add_notes(s24, "Every screen handles user interaction and calls backend service methods.")

    # =========================================================================
    # SLIDE 25: What each file does — reports + utils + assets
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s25, "What each file does — reports + utils + assets", [
        ("reports/sales_report.py & inventory_report.py", "Daily/weekly sales summaries, top-selling medications, stock valuation, and fast/slow movers.", TEAL_ACCENT),
        ("reports/expiry_report.py & tqm_report.py", "Expired batches, 30/90-day risk lists, billing error rate, stockout %, and return accuracy.", BLUE_INFO),
        ("utils/validators.py", "Poka-Yoke gatekeepers: stop blank names, negative prices, oversell quantities, bad dates.", NAVY_DARK),
        ("utils/logger.py & security.py", "Technical error logging into error_logs; SHA-256 password hashing; session tokens.", PURPLE_ACCENT),
        ("utils/helpers.py & assets/", "Currency formatting (₹), ISO date parser, thermal receipt layout, and clinical medical icons.", AMBER_WARN)
    ])
    add_notes(s25, "Reports provide business intelligence; utils enforce quality gates; assets ensure visual consistency.")

    # =========================================================================
    # SLIDE 26: How a click uses these files
    # =========================================================================
    s26 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s26, "How a click uses these files (End-to-End Trace)", [
        ("1. Screen (UI)", "billing.py takes dispensed medicine and quantity requested from cashier input or barcode scan.", TEAL_ACCENT),
        ("2. Service (Bridge)", "sales_service.py checks business rules: verifies staff role authorization and cashier terminal ID.", BLUE_INFO),
        ("3. Extra Service (CDSS)", "medicine_service.py cross-checks patient EHR for penicillin allergies and evaluates drug-drug interactions.", NAVY_DARK),
        ("4. Utils (Validators)", "validators.py rejects negative quantities or requests exceeding available batch balance (qty > stock).", CORAL_DANGER),
        ("5. Database (ACID)", "db.py executes atomic transaction: creates sales invoice row and decrements inventory batch together.", PURPLE_ACCENT),
        ("6. Proof (Audit)", "audit_logs and error_logs receive append-only timestamped event rows with user ID.", AMBER_WARN),
        ("7. Later (TQM Analytics)", "tqm_report.py, Pareto chart, and FMEA table read logs to measure reliability and prevent future failures.", BLUE_INFO)
    ])
    add_notes(s26, "Examiners love this slide: tracing a user click across all 7 layers of the architecture.")

    # =========================================================================
    # SLIDE 27: Why this structure exists
    # =========================================================================
    s27 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s27, "Why this structure exists", [
        ("One folder = one job", "Easy viva explanation. Easy bug localization. Clean separation of concerns.", TEAL_ACCENT),
        ("UI has no SQL", "Screens only show and ask. Eliminates SQL injection vulnerabilities and tight coupling.", BLUE_INFO),
        ("Services hold rules", "Stock limits, expiry lockouts, CDSS allergy logic, and pricing calculations live in services.", NAVY_DARK),
        ("Utils + reports", "Stop bad data at entry and continuously measure software reliability and process quality.", PURPLE_ACCENT)
    ])
    add_notes(s27, "Summary of architectural benefits: maintainability, security, and quality governance.")

    # =========================================================================
    # SLIDE 28: Architecture 1 — request goes down
    # =========================================================================
    s28 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s28, "Architecture 1 — request goes down", [
        ("USER / ADMIN LAYER", "Interacts via Workstation Persona (Admin, Pharmacist, Cashier, Inventory, Delivery).", NAVY_DARK),
        ("UI LAYER", "Login Portal / Clinical Queue / POS Billing / Inventory Hub / Delivery Dock.", TEAL_ACCENT),
        ("SERVICE LAYER", "Business rules, CDSS allergy scanning, FEFO batch prioritization, and tax calculations.", BLUE_INFO),
        ("MODEL & UTILITY LAYER", "User / Medicine / Sale / Patient objects + Validators / Security / Tamper-evident Logger.", PURPLE_ACCENT),
        ("DATABASE LAYER", "SQLite 3 ACID relational engine with Write-Ahead Logging (WAL) and foreign key integrity.", AMBER_WARN),
        ("REPORTS / ANALYTICS", "Sales Ledger / Stock Valuation / Expiry Risk / Daily Z-Report Cash Reconciliation.", CORAL_DANGER)
    ])
    add_notes(s28, "Layered flow: requests cascade downwards through strict interfaces to the database.")

    # =========================================================================
    # SLIDE 29: Architecture 2 — quality loop
    # =========================================================================
    s29 = prs.slides.add_slide(blank_layout)
    set_bg(s29)
    add_header(s29, "Architecture 2 — quality loop")
    add_card(s29, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1))
    tb = s29.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.2), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔄 TOTAL QUALITY MANAGEMENT FEEDBACK LOOP"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(10)

    loop_points = [
        ("1. Operational Execution: ", "UI Layer → Service Layer → SQLite Database processes everyday sales, purchases, and dispensing."),
        ("2. Data Generation: ", "Every transaction generates structured transaction records, audit_logs rows, and error_logs events."),
        ("3. Continuous Quality Analysis: ", "Data from work automatically feeds Pareto 80/20 analysis, Fishbone root cause diagrams, and FMEA tables."),
        ("4. Process Improvement (PDCA): ", "Insights drive software validation updates, tighter input restrictions, and supervisor training."),
        ("5. Standardized Outcome: ", "Errors decrease month over month; software continuously moves toward Crosby's Zero-Defect standard.")
    ]
    for bold_txt, norm_txt in loop_points:
        p2 = tf.add_paragraph()
        r1 = p2.add_run()
        r1.text = bold_txt
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = NAVY_DARK
        r2 = p2.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(6)
    add_notes(s29, "Architecture 2 shows the closed quality loop: transaction data feeds TQM analysis to continuously improve.")

    # =========================================================================
    # SLIDE 30: main.py — start the program only
    # =========================================================================
    s30 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s30, "main.py — start the program only (Director, not the worker)", [
        ("1. Load settings.py", "Reads config.json or initializes system default parameters (DB path, thresholds, ports).", TEAL_ACCENT),
        ("2. Open database", "Initializes SQLite connection pool with Write-Ahead Logging (WAL) and thread safety.", BLUE_INFO),
        ("3. Run schema / migrations", "Verifies all 14 tables exist and runs column migrations without touching existing data.", NAVY_DARK),
        ("4. Mount Unified RPC Bridge", "Exposes 38 Python methods to frontend JavaScript without external framework overhead.", PURPLE_ACCENT),
        ("5. Open login.py (Desktop Window)", "Spawns 60 FPS hardware-accelerated Edge Chromium WebView2 window defaulting to Light Mode.", AMBER_WARN)
    ])
    add_notes(s30, "main.py acts as the director orchestrating startup without containing business logic.")

    # =========================================================================
    # SLIDE 31: config / settings.py
    # =========================================================================
    s31 = prs.slides.add_slide(blank_layout)
    set_bg(s31)
    add_header(s31, "config / settings.py — Values that may change")
    cfg_data = [
        ("APP_NAME", "TQM Pharm Enterprise"),
        ("DB_PATH", "data/pharmacy_system.db"),
        ("EXPIRY_WARNING_DAYS", "30 (Critical Red) / 90 (Attention Amber)"),
        ("REORDER_LEVEL", "20 units (Automated low stock trigger)"),
        ("COLD_CHAIN_MIN_TEMP", "2.0 °C"),
        ("COLD_CHAIN_MAX_TEMP", "8.0 °C"),
        ("INVOICE_PREFIX", "INV-2026-"),
        ("VERSION", "1.0.0 (Review 1 & 2 Release Candidate)")
    ]
    add_table_slide(s31, "config / settings.py — Values that may change", ["Configuration Key", "Runtime Value"], cfg_data, [4.0, 7.333])
    add_notes(s31, "Settings are isolated into a single dataclass singleton rather than hardcoded across the codebase.")

    # =========================================================================
    # SLIDE 32: database / db.py
    # =========================================================================
    s32 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s32, "database / db.py (Core SQLite Engine)", [
        ("1. Opens the SQLite file", "Thread-safe connection factory (`check_same_thread=False`) with row factories returning dict-like records.", TEAL_ACCENT),
        ("2. Runs SQL when a service asks", "Executes parameterized SQL queries (`?` placeholders) strictly preventing SQL injection attacks.", BLUE_INFO),
        ("3. Starts and ends an ACID transaction", "Manages `BEGIN TRANSACTION`, `COMMIT`, and `ROLLBACK` ensuring full transactional atomicity.", NAVY_DARK),
        ("4. Closes the connection", "Clean connection lifecycle management ensuring zero database locks or memory leaks.", PURPLE_ACCENT)
    ])
    add_notes(s32, "database/db.py is our low-level persistence engine enforcing ACID guarantees.")

    # =========================================================================
    # SLIDE 33: database / schema.py — tables we create
    # =========================================================================
    s33 = prs.slides.add_slide(blank_layout)
    set_bg(s33)
    add_header(s33, "database / schema.py — tables we create")
    tbls33 = [
        ("staff (users)", "medicines"),
        ("suppliers", "patients (customers)"),
        ("purchase_orders", "prescriptions"),
        ("invoices (sales)", "delivery_orders"),
        ("narcotic_register", "temperature_logs"),
        ("refill_schedules", "active_sessions"),
        ("audit_logs", "z_reports")
    ]
    col_w = Inches(5.75)
    for idx, (t1, t2) in enumerate(tbls33):
        y = Inches(1.8) + Inches(idx * 0.72)
        for c_idx, t_name in enumerate([t1, t2]):
            x = Inches(0.8) + Inches(c_idx * 5.95)
            add_card(s33, x, y, col_w, Inches(0.62), bg_color=CARD_BG, border_color=BORDER_COLOR)
            tb = s33.shapes.add_textbox(x + Inches(0.2), y + Inches(0.08), col_w - Inches(0.4), Inches(0.45))
            p = tb.text_frame.paragraphs[0]
            p.text = f"📁 Table {idx*2 + c_idx + 1}: {t_name}"
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = NAVY_DARK
    add_notes(s33, "All 14 normalized relational tables created automatically on first run.")

    # =========================================================================
    # SLIDE 34: database / migrations.py (important)
    # =========================================================================
    s34 = prs.slides.add_slide(blank_layout)
    set_bg(s34)
    add_header(s34, "database / migrations.py (important)")
    add_card(s34, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb1 = s34.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "VERSION 1 (Initial Release)"
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = NAVY_DARK
    p1.space_after = Pt(10)
    v1_fields = ["medicines:", "• id / name", "• price", "• quantity"]
    for l in v1_fields:
        p = tf1.add_paragraph()
        p.text = l
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN

    add_card(s34, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb2 = s34.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "LATER VERSION (Migrated Schema)"
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = TEAL_ACCENT
    p2.space_after = Pt(10)
    v2_fields = ["Same table + Added Columns without data loss:", "• barcode", "• batch_no", "• expiry_date", "• days_to_expiry", "• cold_chain", "• interactions"]
    for l in v2_fields:
        p = tf2.add_paragraph()
        p.text = l
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
    add_notes(s34, "Migrations allow schema evolution without dropping tables or losing live records.")

    # =========================================================================
    # SLIDE 35: Why migrations.py matters
    # =========================================================================
    s35 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s35, "Why migrations.py matters", [
        ("1. Test data is not wiped", "If you only edit schema.py and recreate the DB, existing test and patient data is wiped.", TEAL_ACCENT),
        ("2. Migration adds columns to the live file", "Executes dynamic `ALTER TABLE` checks; existing rows receive safe default values.", BLUE_INFO),
        ("3. Review line for evaluators:", "'The database layer can grow and adapt without destroying operational records.'", NAVY_DARK),
        ("4. TQM link:", "Directly implements Maintainability, Data Integrity, and Continuous Process Control.", PURPLE_ACCENT)
    ])
    add_notes(s35, "Evaluation highlight: preserving test and clinical records during schema updates.")

    # =========================================================================
    # SLIDE 36: models/ — what exists in the shop
    # =========================================================================
    s36 = prs.slides.add_slide(blank_layout)
    set_bg(s36)
    add_header(s36, "models/ — what exists in the shop (A model is the object. Not SQL. Not screen.)")
    models36 = [
        ("user.py", "Staff user: ID, name, username, hashed password, role, branch, active status."),
        ("medicine.py", "Drug item: SKU, generic, category, batch, qty, cost, MRP, expiry, cold-chain flag."),
        ("supplier.py", "Distributor: Who we buy stock from, phone, email, GSTIN, payment terms."),
        ("customer.py (patient)", "Patient: Name, phone, recorded drug allergies (Penicillin), chronic conditions."),
        ("sale.py", "One sales invoice + its line items, cashier, payment method, tax split."),
        ("purchase.py", "One purchase order / GRN consignment bill from a supplier + items.")
    ]
    for idx, (m_file, m_desc) in enumerate(models36):
        r = idx // 3
        c_i = idx % 3
        x = Inches(0.8) + Inches(c_i * 3.98)
        y = Inches(1.8) + Inches(r * 2.6)
        add_card(s36, x, y, Inches(3.78), Inches(2.4))
        hb = s36.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(3.78), Inches(0.5))
        hb.fill.solid()
        hb.fill.fore_color.rgb = NAVY_DARK if idx % 2 == 0 else TEAL_ACCENT
        hb.line.fill.background()
        tb = s36.shapes.add_textbox(x, y + Inches(0.05), Inches(3.78), Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        p.text = m_file
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb2 = s36.shapes.add_textbox(x + Inches(0.15), y + Inches(0.6), Inches(3.48), Inches(1.7))
        p2 = tb2.text_frame.paragraphs[0]
        p2.text = m_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN
    add_notes(s36, "Models represent pure business objects decoupled from presentation and SQL.")

    # =========================================================================
    # SLIDE 37: users table — example
    # =========================================================================
    s37 = prs.slides.add_slide(blank_layout)
    users_data = [
        ("STF-01", "Dr. Rajesh Kulkarni", "admin", "Admin", "Active"),
        ("STF-02", "Pooja Sharma, R.Ph", "pharmacist", "Pharmacist", "Active"),
        ("STF-03", "Amit Deshmukh", "cashier", "Cashier", "Active"),
        ("STF-04", "Vikram Patel", "inventory", "Inventory", "Active"),
        ("STF-05", "Suresh Kumar", "delivery", "Delivery", "Active")
    ]
    add_table_slide(s37, "users table — example", ["user_id", "name", "username", "role", "status"], users_data, [1.8, 3.2, 2.2, 2.2, 1.933])
    add_notes(s37, "Concrete data showing all 5 active operational roles in TQM Pharm.")

    # =========================================================================
    # SLIDE 38: users table — other columns
    # =========================================================================
    s38 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s38, "users table — other columns", [
        ("password_hash", "Never store plaintext '123456'. Passwords are verified against cryptographic hashes.", TEAL_ACCENT),
        ("phone / email", "Employee contact profile used for statutory shift notifications, not login handles.", BLUE_INFO),
        ("branch", "Assigned retail pharmacy branch (e.g. 'Apex Central - Branch #01') supporting multi-store expansion.", NAVY_DARK),
        ("role", "Strict Role-Based Access Control: Admin / Pharmacist / Cashier / Inventory / Delivery.", PURPLE_ACCENT)
    ])
    add_notes(s38, "Security columns guarantee non-repudiation and prevent unauthorized privilege escalation.")

    # =========================================================================
    # SLIDE 39: medicines table — example
    # =========================================================================
    s39 = prs.slides.add_slide(blank_layout)
    med_data = [
        ("MED-001", "Augmentin 625 Duo", "AUG-2026-X1", "140", "2026-12-01 (Healthy)"),
        ("MED-002", "Humalog Insulin 100IU", "INS-2026-H2", "8", "2026-10-05 (Critical <30d)"),
        ("MED-003", "Cetirizine 10mg", "CET-2027-C1", "250", "2027-03-20 (Healthy)"),
        ("MED-004", "ORS Hydration Sachet", "ORS-2026-D1", "45", "2026-09-30 (Expired)"),
        ("MED-005", "Alprax 0.5mg (Sched X)", "NDP-2026-A1", "30", "2026-11-15 (Dual PIN)")
    ]
    add_table_slide(s39, "medicines table — example", ["id", "name", "batch", "qty", "expiry"], med_data, [1.8, 3.5, 2.2, 1.5, 2.333])
    add_notes(s39, "Notice batch-level granularity: batch lot, stock on hand, and expiry countdown status.")

    # =========================================================================
    # SLIDE 40: medicines — full field list
    # =========================================================================
    s40 = prs.slides.add_slide(blank_layout)
    set_bg(s40)
    add_header(s40, "medicines — full field list")
    fields40 = [
        ("medicine_id", "name"),
        ("generic_name", "category"),
        ("manufacturer", "batch_no"),
        ("purchase_price", "selling_price (MRP)"),
        ("quantity", "reorder_level"),
        ("mfg_date", "expiry_date"),
        ("days_to_expiry", "rack_coordinate"),
        ("cold_chain (2-8°C)", "interactions JSON")
    ]
    col_w = Inches(5.75)
    for idx, (f1, f2) in enumerate(fields40):
        y = Inches(1.8) + Inches(idx * 0.63)
        for c_idx, f_name in enumerate([f1, f2]):
            x = Inches(0.8) + Inches(c_idx * 5.95)
            add_card(s40, x, y, col_w, Inches(0.55), bg_color=CARD_BG, border_color=BORDER_COLOR)
            tb = s40.shapes.add_textbox(x + Inches(0.2), y + Inches(0.06), col_w - Inches(0.4), Inches(0.4))
            p = tb.text_frame.paragraphs[0]
            p.text = f"• {f_name}"
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = NAVY_DARK
    add_notes(s40, "All 16 schema attributes supporting clinical safety, FEFO picking, and IoT storage.")

    # =========================================================================
    # SLIDE 41: suppliers table — example
    # =========================================================================
    s41 = prs.slides.add_slide(blank_layout)
    supp_data = [
        ("SUP-001", "Apex Medico Distributors", "+91 98201 11111", "Mumbai HQ", "30 Days Net"),
        ("SUP-002", "Care Pharma Logistics", "+91 98201 22222", "Pune Hub", "15 Days Net"),
        ("SUP-003", "BioCold Vaccines India", "+91 98201 33333", "Haldwani / Delhi", "Immediate COD")
    ]
    add_table_slide(s41, "suppliers table — example", ["id", "name", "phone", "city / branch", "payment_terms"], supp_data, [1.5, 3.5, 2.2, 2.2, 1.933])
    add_notes(s41, "Distributor directory storing vendor contacts, GSTIN numbers, and credit terms.")

    # =========================================================================
    # SLIDE 42: customers table — example
    # =========================================================================
    s42 = prs.slides.add_slide(blank_layout)
    cust_data = [
        ("PAT-001", "Walk-in Counter Patient", "—", "OTC Cash sale, no chronic history"),
        ("PAT-002", "Suresh Patil", "+91 98220 44551", "Allergic: ['Penicillin', 'Amoxicillin']"),
        ("PAT-003", "Ananya Verma", "+91 98111 77882", "Chronic: Diabetes Type 2 (Insulin Refill)")
    ]
    add_table_slide(s42, "customers table — example (patients & EHR)", ["id", "name", "phone", "notes / clinical allergies"], cust_data, [1.5, 3.2, 2.5, 4.133])
    add_notes(s42, "Patient records include EHR allergy arrays directly powering CDSS Poka-Yoke error blocking.")

    # =========================================================================
    # SLIDE 43: purchases + purchase_items
    # =========================================================================
    s43 = prs.slides.add_slide(blank_layout)
    po_data = [
        ("PO-2026-01", "Apex Medico", "2026-09-10", "Augmentin 625 Duo", "100 units"),
        ("PO-2026-01", "Apex Medico", "2026-09-10", "Cetirizine 10mg", "60 units"),
        ("PO-2026-02", "BioCold Vaccines", "2026-09-14", "Humalog Insulin", "10 vials")
    ]
    add_table_slide(s43, "purchases + purchase_items (GRN Inwarding)", ["purchase_id", "supplier", "date", "item", "qty"], po_data, [2.0, 2.8, 2.2, 2.8, 1.533])
    add_notes(s43, "Purchase orders record dockside inwarding against supplier consignments.")

    # =========================================================================
    # SLIDE 44: sales + sale_items — example
    # =========================================================================
    s44 = prs.slides.add_slide(blank_layout)
    sales_data = [
        ("INV-2026-1045", "Amit (Cashier)", "Augmentin 625 Duo", "2 strips", "₹ 400.00"),
        ("INV-2026-1045", "Amit (Cashier)", "Cetirizine 10mg", "1 strip", "₹ 25.00"),
        ("INV-2026-1044", "Amit (Cashier)", "ORS Hydration Sachet", "3 packs", "₹ 90.00")
    ]
    add_table_slide(s44, "sales + sale_items — example", ["invoice", "cashier", "item", "qty", "amount"], sales_data, [2.2, 2.5, 3.0, 1.8, 1.833])
    add_notes(s44, "Invoices link cashier ID, sold batch items, and statutory GST totals.")

    # =========================================================================
    # SLIDE 45: audit_logs — example
    # =========================================================================
    s45 = prs.slides.add_slide(blank_layout)
    audit_data = [
        ("Pooja (Pharma)", "UPDATE_STOCK", "Augmentin: 140 → 138 units", "10:42"),
        ("Amit (Cashier)", "SALE", "INV-2026-1045 ₹ 425.00 (UPI QR)", "11:15"),
        ("Dr. Rajesh (Admin)", "ADD_USER", "Created Suresh / Delivery", "09:05"),
        ("Pooja (Pharma)", "BLOCK_SALE", "BLOCKED: Amoxicillin (Penicillin allergy)", "11:40")
    ]
    add_table_slide(s45, "audit_logs — example (21 CFR Part 11 compliant)", ["who", "action", "detail", "time"], audit_data, [2.5, 2.5, 4.8, 1.533])
    add_notes(s45, "Append-only audit trail recording every clinical block, sale, and stock adjustment.")

    # =========================================================================
    # SLIDE 46: error_logs — for FMEA later
    # =========================================================================
    s46 = prs.slides.add_slide(blank_layout)
    err_data = [
        ("E01", "qty > stock attempt", "18 times", "11:12 (Blocked by validators)"),
        ("E02", "blank medicine name", "7 times", "10:03 (Blocked by Poka-Yoke)"),
        ("E03", "expired item selected", "11 times", "11:40 (Blocked by FEFO guard)"),
        ("E04", "duplicate barcode scan", "4 times", "09:50 (Unique constraint)"),
        ("E05", "login authentication failed", "9 times", "08:21 (Security audit)")
    ]
    add_table_slide(s46, "error_logs — for FMEA later", ["code", "problem", "count", "last seen / action taken"], err_data, [1.5, 3.5, 2.2, 4.133])
    add_notes(s46, "Error telemetry counts feed directly into our FMEA table and Pareto analysis.")

    # =========================================================================
    # SLIDE 47: services/ — the work happens here
    # =========================================================================
    s47 = prs.slides.add_slide(blank_layout)
    set_bg(s47)
    add_header(s47, "services/ — the work happens here (UI asks. Service decides. Database stores.)")
    srvs47 = [
        ("auth_service", "medicine_service"),
        ("search_service", "sales_service"),
        ("purchase_service", "inventory_service"),
        ("cdss_service", "report_service")
    ]
    col_w = Inches(5.75)
    for idx, (s1, s2) in enumerate(srvs47):
        y = Inches(1.8) + Inches(idx * 1.25)
        for c_idx, s_name in enumerate([s1, s2]):
            x = Inches(0.8) + Inches(c_idx * 5.95)
            add_card(s47, x, y, col_w, Inches(1.1), bg_color=CARD_BG, border_color=BORDER_COLOR)
            bar = s47.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), Inches(1.1))
            bar.fill.solid()
            bar.fill.fore_color.rgb = TEAL_ACCENT if c_idx == 0 else BLUE_INFO
            bar.line.fill.background()
            tb = s47.shapes.add_textbox(x + Inches(0.25), y + Inches(0.12), col_w - Inches(0.4), Inches(0.86))
            tf = tb.text_frame
            p = tf.paragraphs[0]
            p.text = f"⚙️ {s_name}.py"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = NAVY_DARK
            p2 = tf.add_paragraph()
            p2.text = "Encapsulates domain logic, validation checks, and ACID storage calls."
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_MUTED
    add_notes(s47, "Services represent the brain of the application mediating between UI and storage.")

    # =========================================================================
    # SLIDE 48: auth_service.py
    # =========================================================================
    s48 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s48, "auth_service.py", [
        ("• Login and logout", "Authenticates staff against SQLite database and cleans up active sessions on exit.", TEAL_ACCENT),
        ("• Check password hash", "Verifies supplied password against salted SHA-256 hash without plaintext storage.", BLUE_INFO),
        ("• Read the user role", "Extracts RBAC role: Admin, Pharmacist, Cashier, Inventory Manager, Delivery Agent.", NAVY_DARK),
        ("• Allow or block a screen", "Workstation route shields enforce role authorization before UI views render.", PURPLE_ACCENT),
        ("• Start a simple session", "Registers terminal session UUID, machine IP, and initiates 5s presence heartbeat.", AMBER_WARN)
    ])
    add_notes(s48, "Authentication and RBAC security enforced on every request.")

    # =========================================================================
    # SLIDE 49: medicine_service.py
    # =========================================================================
    s49 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s49, "medicine_service.py", [
        ("• Add / update / deactivate a medicine", "Manages lifecycle of pharmaceutical SKUs with category and Schedule flags.", TEAL_ACCENT),
        ("• Change stock after purchase or sale", "Performs atomic stock increments on inwarding and decrements on billing.", BLUE_INFO),
        ("• Check expiry before a sale", "Enforces strict lockout: medicines with days_to_expiry ≤ 0 cannot be added to cart.", CORAL_DANGER),
        ("• Check reorder level", "Flags low stock warning tags when on-hand quantity drops below 20 units.", AMBER_WARN),
        ("• Never let UI write the row directly", "All inventory mutations must pass through validated service methods.", NAVY_DARK)
    ])
    add_notes(s49, "Inventory rules guarantee zero expired sales and automated stock replenishment alerts.")

    # =========================================================================
    # SLIDE 50: search_service.py
    # =========================================================================
    s50 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s50, "search_service.py", [
        ("• Search by brand name", "Sub-string matching for fast autocomplete during counter prescription intake.", TEAL_ACCENT),
        ("• Search by generic molecule name", "Enables therapeutic substitution (e.g. Paracetamol across brand trade names).", BLUE_INFO),
        ("• Search by manufacturer", "Finds stock by pharmaceutical laboratory (e.g. Cipla, Sun Pharma, Abbott).", NAVY_DARK),
        ("• Search by barcode scanner", "Instant USB HID hardware scanner lookup (<10ms query execution).", PURPLE_ACCENT),
        ("• Multi-parameter filter", "Filter simultaneously by therapeutic category, expiry band (<30d), and low stock.", AMBER_WARN)
    ])
    add_notes(s50, "Lightning-fast search keeps customer counter checkout under 3 seconds.")

    # =========================================================================
    # SLIDE 51: sales_service.py
    # =========================================================================
    s51 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s51, "sales_service.py", [
        ("• Create sales invoice", "Initializes fiscal invoice header with unique sequence number (INV-YYYY-XXXX).", TEAL_ACCENT),
        ("• Add sale items", "Attaches batch lots, sold units, unit prices, and calculates 5% GST tax split.", BLUE_INFO),
        ("• Check stock and expiry", "Performs pre-commit assertion: guarantees viable expiry and stock availability.", CORAL_DANGER),
        ("• Calculate totals & split tender", "Computes subtotal, CGST, SGST, cash change return, or dynamic UPI QR string.", NAVY_DARK),
        ("• Atomic Transaction Execution", "Saves invoice + cuts stock + appends audit log in one single ACID commit.", PURPLE_ACCENT)
    ])
    add_notes(s51, "Sales service manages the entire billing transaction atomically.")

    # =========================================================================
    # SLIDE 52: purchase_service.py
    # =========================================================================
    s52 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s52, "purchase_service.py", [
        ("• Create purchase from a supplier", "Records Goods Receipt Note (GRN) linked to supplier code and invoice number.", TEAL_ACCENT),
        ("• Add purchase items", "Captures SKU, inward batch number, manufacturing date, and calendar expiry.", BLUE_INFO),
        ("• Increase medicine quantity", "Atomically updates batch inventory ledger and re-computes days to expiry.", NAVY_DARK),
        ("• Save batch and expiry from the bill", "Guarantees full batch traceability from distributor dock to customer handoff.", PURPLE_ACCENT),
        ("• Write audit: PURCHASE", "Records immutable procurement entry in audit_logs for drug inspectors.", AMBER_WARN)
    ])
    add_notes(s52, "Inwarding service guarantees batch traceability from supplier dock to counter.")

    # =========================================================================
    # SLIDE 53: inventory_service.py
    # =========================================================================
    s53 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s53, "inventory_service.py", [
        ("• Current stock ledger", "Real-time query of all active pharmaceutical batches with storage rack coordinates.", TEAL_ACCENT),
        ("• Low stock list", "Isolates SKUs with on-hand units ≤ reorder threshold (≤20) for automated purchase orders.", AMBER_WARN),
        ("• Expired list", "Isolates expired batches (days ≤ 0) for quarantine and return to vendor.", CORAL_DANGER),
        ("• Near-expiry 30 / 90 days", "Applies FEFO priority flags to ensure oldest viable lots are dispensed first.", BLUE_INFO),
        ("• Stock movement analytics", "Tracks velocity of fast-moving vs stagnant dead-stock items.", PURPLE_ACCENT)
    ])
    add_notes(s53, "Inventory service eliminates dead-stock write-offs and automates reorders.")

    # =========================================================================
    # SLIDE 54: report_service.py
    # =========================================================================
    s54 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s54, "report_service.py", [
        ("• Ask database for grouped numbers", "Runs optimized SQL aggregations (`SUM`, `COUNT`, `GROUP BY`) for reporting.", TEAL_ACCENT),
        ("• Give clean data to report screens", "Formats raw currency, date timestamps, and tax splits for UI presentation.", BLUE_INFO),
        ("• Sales totals, stock value, expiry counts", "Calculates gross revenue, inventory holding valuation, and expiry loss risk.", NAVY_DARK),
        ("• Quality counts from error_logs", "Aggregates error frequency (E01-E05) directly into Pareto and FMEA metrics.", PURPLE_ACCENT),
        ("• Daily Z-Report Cash Balancing", "Computes expected drawer cash and flags live physical cash variance (Balanced/Short).", AMBER_WARN)
    ])
    add_notes(s54, "Report service translates raw data into executive and clinical decisions.")

    # =========================================================================
    # SLIDE 55: ui/ — what the person sees
    # =========================================================================
    s55 = prs.slides.add_slide(blank_layout)
    set_bg(s55)
    add_header(s55, "ui/ — what the person sees (A screen only: shows data, takes input, calls a service, shows result.)")
    screens55 = [
        ("login", "dashboard", "medicines", "inventory", "suppliers"),
        ("customers", "purchases", "search", "billing", "users")
    ]
    col_w = Inches(2.22)
    for r_idx, row in enumerate(screens55):
        y = Inches(1.8) + Inches(r_idx * 2.6)
        for c_idx, sc_name in enumerate(row):
            x = Inches(0.8) + Inches(c_idx * 2.37)
            add_card(s55, x, y, col_w, Inches(2.4))
            hb = s55.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, col_w, Inches(0.5))
            hb.fill.solid()
            hb.fill.fore_color.rgb = NAVY_DARK if (r_idx + c_idx) % 2 == 0 else TEAL_ACCENT
            hb.line.fill.background()
            tb = s55.shapes.add_textbox(x, y + Inches(0.06), col_w, Inches(0.4))
            p = tb.text_frame.paragraphs[0]
            p.text = sc_name.upper()
            p.alignment = PP_ALIGN.CENTER
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = TEXT_WHITE

            tb2 = s55.shapes.add_textbox(x + Inches(0.1), y + Inches(0.6), col_w - Inches(0.2), Inches(1.7))
            p2 = tb2.text_frame.paragraphs[0]
            p2.text = f"Screen {sc_name}.py: Takes user events, validates input format, calls {sc_name}_service."
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_MAIN
    add_notes(s55, "All 10 UI screens adhere to the same clean event-driven architecture.")

    # =========================================================================
    # SLIDE 56: ui / login.py
    # =========================================================================
    s56 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s56, "ui / login.py", [
        ("Pharmacy Management System Login Portal", "Clean White/Light theme by default with instant Dark Mode toggle.", TEAL_ACCENT),
        ("Username & Password Input", "Custom styled entry fields with Show/Hide password toggle and keyboard Enter binding.", BLUE_INFO),
        ("Workstation Persona Grid (Fast Login)", "Interactive tiles for Admin, Pharmacist, Cashier, Inventory, and Delivery pre-filling credentials.", NAVY_DARK),
        ("Terminal Location Selector", "Assigns workstation to physical counter terminal (Counter A, Clinical Kiosk, Inwarding Bay).", PURPLE_ACCENT),
        ("Calls auth_service.py", "Transmits credentials for SHA-256 verification and initiates presence heartbeats.", AMBER_WARN)
    ])
    add_notes(s56, "Login screen boots directly to our persona grid for seamless role-based demonstration.")

    # =========================================================================
    # SLIDE 57: ui / dashboard.py
    # =========================================================================
    s57 = prs.slides.add_slide(blank_layout)
    set_bg(s57)
    add_header(s57, "ui / dashboard.py — Real-Time KPI Command Center")
    kpis = [
        ("Today sales", "₹ 18,450.00", TEAL_ACCENT),
        ("Low stock", "12 items", AMBER_WARN),
        ("Near expiry", "7 batches", BLUE_INFO),
        ("Expired", "0 dispensed (3 blocked)", CORAL_DANGER)
    ]
    col_w = Inches(2.78)
    for idx, (title, val, col) in enumerate(kpis):
        x = Inches(0.8) + Inches(idx * 2.98)
        add_card(s57, x, Inches(1.8), col_w, Inches(1.8))
        tb = s57.shapes.add_textbox(x + Inches(0.15), Inches(1.95), col_w - Inches(0.3), Inches(1.5))
        tf = tb.text_frame
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK
        p2 = tf.add_paragraph()
        p2.text = val
        p2.font.size = Pt(20)
        p2.font.bold = True
        p2.font.color.rgb = col

    # Bottom menu / recent panel
    add_card(s57, Inches(0.8), Inches(3.9), Inches(11.733), Inches(3.0))
    tb_b = s57.shapes.add_textbox(Inches(1.1), Inches(4.1), Inches(11.2), Inches(2.6))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "Left Navigation Menu: Dashboard | Medicines | Inventory | Purchases | Billing | Customers | Suppliers | Reports | Quality | Users"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(10)
    p2 = tf_b.add_paragraph()
    p2.text = "Recent Transactions Audit Feed:\n• INV-2026-1045: ₹ 385.00 | Cashier: Amit | Tender: Dynamic UPI QR | Time: 11:15\n• INV-2026-1044: ₹ 720.00 | Cashier: Amit | Tender: Cash (Change ₹ 280) | Time: 11:10\n• BLOCKED: Amoxicillin dispense attempt for allergic patient Suresh Patil | Time: 11:05"
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_MAIN
    add_notes(s57, "Dashboard displays live financial and clinical KPIs with immediate audit trail visibility.")

    # =========================================================================
    # SLIDE 58: ui / medicines.py
    # =========================================================================
    s58 = prs.slides.add_slide(blank_layout)
    med_tbl = [
        ("Augmentin 625 Duo", "AUG-2026-X1", "140", "2026-12-01", "HEALTHY (Green)"),
        ("Humalog Insulin 100IU", "INS-2026-H2", "8", "2026-10-05", "CRITICAL <30d (Red)"),
        ("Cetirizine 10mg", "CET-2027-C1", "250", "2027-03-20", "HEALTHY (Green)"),
        ("ORS Hydration Sachet", "ORS-2026-D1", "45", "2026-09-30", "EXPIRED (Locked)")
    ]
    add_table_slide(s58, "ui / medicines.py — Actions: Add | Edit | Deactivate | Refresh", ["Name", "Batch", "Qty", "Expiry", "Status"], med_tbl, [3.2, 2.2, 1.5, 2.2, 2.233])
    add_notes(s58, "Medicines screen shows color-coded expiry countdowns. No direct SQL on this screen.")

    # =========================================================================
    # SLIDE 59: ui / inventory.py
    # =========================================================================
    s59 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s59, "ui / inventory.py — Real-Time Stock Ledger Views", [
        ("All Stock", "Comprehensive multi-batch inventory ledger displaying rack coordinates and unit costs.", TEAL_ACCENT),
        ("Low Stock (Qty ≤ Reorder Level)", "Filtered view showing SKUs requiring immediate distributor purchase order generation.", AMBER_WARN),
        ("Expired (Days ≤ 0)", "Quarantined stock mathematically locked from addition to cashier POS cart.", CORAL_DANGER),
        ("Expires in 30 Days (Critical Tier)", "Near-expiry batches flagged in red for prioritized clearance dispensing.", BLUE_INFO),
        ("Expires in 90 Days (Attention Tier)", "Batches flagged in amber for supplier exchange or promotional bundling.", PURPLE_ACCENT)
    ])
    add_notes(s59, "Inventory views allow managers to isolate stock by operational risk tiers.")

    # =========================================================================
    # SLIDE 60: ui / suppliers.py and customers.py
    # =========================================================================
    s60 = prs.slides.add_slide(blank_layout)
    set_bg(s60)
    add_header(s60, "ui / suppliers.py and customers.py")
    add_card(s60, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb1 = s60.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "📦 SUPPLIERS MANAGEMENT"
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = TEAL_ACCENT
    p1.space_after = Pt(10)
    s_points = [
        "• Supplier Directory: List + Add + Edit vendor profiles.",
        "• Contact Data: Name, phone, city, GSTIN, and DL number.",
        "• Purchase History: Open purchase orders and shipment invoices.",
        "• Decoupling Rule: Calls no stock math directly; manages distributor contracts only."
    ]
    for p_t in s_points:
        p = tf1.add_paragraph()
        p.text = p_t
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)

    add_card(s60, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb2 = s60.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "🩺 CUSTOMERS & PATIENT EHR"
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = BLUE_INFO
    p2.space_after = Pt(10)
    c_points = [
        "• Patient Profiles: Walk-in counter clients and registered chronic patients.",
        "• EHR Allergy Registry: Tracks known allergies (e.g. Penicillin, Sulfa, NSAIDs).",
        "• Chronic Therapy: Chronic condition tags driving automated 30-day refill reminders.",
        "• Compliance: Essential for customer returns, drug recalls, and clinical safety."
    ]
    for p_t in c_points:
        p = tf2.add_paragraph()
        p.text = p_t
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)
    add_notes(s60, "Suppliers manage distributor partnerships; Customers store critical clinical EHR allergy data.")

    # =========================================================================
    # SLIDE 61: ui / purchases.py
    # =========================================================================
    s61 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s61, "ui / purchases.py (Goods Receipt Note Workflow)", [
        ("1. Pick Supplier", "Select distributor from verified supplier directory (e.g. Apex Medico).", TEAL_ACCENT),
        ("2. Add Inward Items", "Input received medicine, batch lot, received quantity, cost price, and expiry date.", BLUE_INFO),
        ("3. Validate", "Validators ensure non-zero quantities, future expiry date, and valid PO reference.", NAVY_DARK),
        ("4. purchase_service saves and increases stock", "Executes single ACID transaction incrementing batch inventory and recalculating FEFO index.", PURPLE_ACCENT),
        ("5. Audit: PURCHASE", "Writes immutable audit_logs row capturing inward consignment parameters.", AMBER_WARN)
    ])
    add_notes(s61, "Purchases screen enforces dockside verification before stock enters the live inventory.")

    # =========================================================================
    # SLIDE 62: ui / search.py
    # =========================================================================
    s62 = prs.slides.add_slide(blank_layout)
    set_bg(s62)
    add_header(s62, "ui / search.py — Instant Multi-Filter Search Engine")
    add_card(s62, Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.1))
    tb_s = s62.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(11.3), Inches(0.8))
    p = tb_s.text_frame.paragraphs[0]
    p.text = "🔍 Search box: Brand Name / Generic Molecule / USB Barcode Scanner (<50ms)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT

    # 4 Filter cards
    s_filters = [
        ("Filter by Category", "Isolate Antibiotics, Analgesics, Antidiabetics, Cardiovascular, or OTC products.", BLUE_INFO),
        ("Filter by Expiry Band", "Quick toggles for Critical (<30 days), Attention (<90 days), and Expired batches.", CORAL_DANGER),
        ("Low Stock Only", "Isolate batches with inventory ≤ reorder threshold for immediate purchase.", AMBER_WARN),
        ("1-Click Dispatch to Billing", "Select search result directly into POS billing cart without manual typing.", NAVY_DARK)
    ]
    for idx, (f_title, f_desc, col) in enumerate(s_filters):
        r = idx // 2
        c_i = idx % 2
        x = Inches(0.8) + Inches(c_i * 5.95)
        y = Inches(3.2) + Inches(r * 1.9)
        add_card(s62, x, y, Inches(5.75), Inches(1.7))
        tb = s62.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), Inches(5.35), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f_title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = col
        p2 = tf.add_paragraph()
        p2.text = f_desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_MAIN
    add_notes(s62, "Search screen allows cashiers and pharmacists to locate medicines instantly with multi-filters.")

    # =========================================================================
    # SLIDE 63: ui / billing.py — main process screen
    # =========================================================================
    s63 = prs.slides.add_slide(blank_layout)
    set_bg(s63)
    add_header(s63, "ui / billing.py — main process screen")
    bill_steps = [
        ("1. Search medicine / 1-Click eRx", "Barcode scan or 1-click import of approved prescription from clinical queue."),
        ("2. Show available qty + expiry", "Displays stock on hand with automated FEFO nearest-expiry batch selection."),
        ("3. Type quantity", "Cashier enters required dosage units with real-time stock ceiling validation."),
        ("4. Validate (Poka-Yoke)", "Blocks negative numbers, oversell requests, expired stock, and patient allergies."),
        ("5. sales_service does the rest", "Atomically deducts stock, calculates 5% GST tax split, generates invoice."),
        ("6. Print / Show thermal receipt", "Generates 80mm ESC/POS receipt modal with dynamic UPI QR and change calculator.")
    ]
    for idx, (b_title, b_desc) in enumerate(bill_steps):
        r = idx // 3
        c_i = idx % 3
        x = Inches(0.8) + Inches(c_i * 3.98)
        y = Inches(1.8) + Inches(r * 2.6)
        add_card(s63, x, y, Inches(3.78), Inches(2.4))
        hb = s63.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(3.78), Inches(0.5))
        hb.fill.solid()
        hb.fill.fore_color.rgb = NAVY_DARK if (r + c_i) % 2 == 0 else TEAL_ACCENT
        hb.line.fill.background()
        tb = s63.shapes.add_textbox(x, y + Inches(0.06), Inches(3.78), Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        p.text = b_title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb2 = s63.shapes.add_textbox(x + Inches(0.15), y + Inches(0.6), Inches(3.48), Inches(1.7))
        p2 = tb2.text_frame.paragraphs[0]
        p2.text = b_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN
    add_notes(s63, "Billing is our main operational screen with zero SQL and 100% Poka-Yoke protection.")

    # =========================================================================
    # SLIDE 64: ui / users.py (Admin only)
    # =========================================================================
    s64 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s64, "ui / users.py (Admin only: Staff Governance & RBAC)", [
        ("1. Add user", "Create new staff accounts with unique employee ID, full legal name, and login handle.", TEAL_ACCENT),
        ("2. Set role: Admin / Pharmacist / Cashier / Inventory / Delivery", "Assign workstation permissions strictly enforcing separation of clinical and financial duties.", BLUE_INFO),
        ("3. Activate or block account", "1-Click toggle (`Active` / `Suspended`) to terminate compromised credentials instantly.", CORAL_DANGER),
        ("4. Never show the real password", "Displays password masked; stores salted cryptographic hash in database.", NAVY_DARK),
        ("5. Calls auth_service + audit", "Every credential creation, password reset, or status change writes to audit_logs.", PURPLE_ACCENT)
    ])
    add_notes(s64, "Admin screen enforces Role-Based Access Control and audit accountability.")

    # =========================================================================
    # SLIDE 65: reports/
    # =========================================================================
    s65 = prs.slides.add_slide(blank_layout)
    set_bg(s65)
    add_header(s65, "reports/ — Business Intelligence & Compliance Engine")
    r_modules = [
        ("sales_report.py", "Daily, weekly, monthly gross revenue\nTop-selling medicines by volume\nPayment tender breakdown (Cash/UPI/Card)\nTax collections (CGST / SGST liability)", TEAL_ACCENT),
        ("inventory_report.py", "Total stock valuation at cost & MRP\nFast-moving vs slow-moving stock analysis\nReorder threshold shortfall alerts\nStock adjustment audit history", BLUE_INFO),
        ("expiry_report.py", "Expired batches scheduled for quarantine\nCritical 30-day countdown risk list\nAttention 90-day supplier exchange list\nEstimated expiry capital at risk", CORAL_DANGER),
        ("tqm_report.py", "Transaction error rate (E01-E05)\nStockout percentage over time\nCustomer return accuracy analysis\nLogs feeding Pareto and FMEA matrices", NAVY_DARK)
    ]
    for idx, (title, points, col) in enumerate(r_modules):
        r = idx // 2
        c_i = idx % 2
        x = Inches(0.8) + Inches(c_i * 5.95)
        y = Inches(1.8) + Inches(r * 2.6)
        add_card(s65, x, y, Inches(5.75), Inches(2.4))
        bar = s65.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), Inches(2.4))
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()
        tb = s65.shapes.add_textbox(x + Inches(0.25), y + Inches(0.12), Inches(5.35), Inches(2.16))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK
        p1.space_after = Pt(4)
        for line in points.split('\n'):
            p = tf.add_paragraph()
            p.text = "• " + line
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(2)
    add_notes(s65, "Reports suite provides financial, inventory, expiry, and quality analytics.")

    # =========================================================================
    # SLIDE 66: utils/
    # =========================================================================
    s66 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s66, "utils/ — Technical Utilities & Defensive Engineering", [
        ("validators.py", "Is name blank? Price < 0? Qty > stock? Expiry < mfg date? Stops malformed requests at entry.", TEAL_ACCENT),
        ("logger.py", "Tamper-evident operational logger writing technical errors to error_logs and events to audit_logs.", BLUE_INFO),
        ("security.py", "Cryptographic hashing (SHA-256), permission checking, session UUID tokens, and PIN verification.", NAVY_DARK),
        ("helpers.py", "Indian Rupee formatting (₹), ISO date parser, automatic invoice number sequencer (INV-2026-XXXX).", PURPLE_ACCENT)
    ])
    add_notes(s66, "Utils encapsulate defensive programming routines used across all modules.")

    # =========================================================================
    # SLIDE 67: assets/
    # =========================================================================
    s67 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s67, "assets/ — Visual Identity & Design Consistency", [
        ("icons/", "Standardized clinical iconography: medicine pill, cash POS, inventory box, delivery rider, reports chart.", TEAL_ACCENT),
        ("logo/", "High-resolution corporate pharmacy emblem: `pharmacy_logo.png` featured on login and thermal receipts.", BLUE_INFO),
        ("Consistent Layout Across Screens", "Same sidebar navigation, status badges, and color tokens (Green/Amber/Red) on every workstation.", NAVY_DARK),
        ("Quality Link:", "Interface consistency is an essential human-factors quality point: reduces cognitive burden and operator error.", PURPLE_ACCENT)
    ])
    add_notes(s67, "Consistency in UI design prevents operational mistakes during hectic counter shifts.")

    # =========================================================================
    # SLIDE 68: Software feature → TQM concept
    # =========================================================================
    s68 = prs.slides.add_slide(blank_layout)
    tqm_map_data = [
        ("Modular architecture", "Process / system approach (Deming)"),
        ("Validation & CDSS", "Error prevention at source / Poka-Yoke (Shingo)"),
        ("Audit log (21 CFR Part 11)", "Traceability & transparency"),
        ("User roles & RBAC", "Accountability & operational governance"),
        ("Inventory FEFO & IoT 2-8°C", "Process control & biological preservation"),
        ("Expiry risk alerts (<30d)", "Proactive risk prevention"),
        ("Quality dashboard", "Data-driven decision making (Juran)"),
        ("Pareto chart", "Root-cause prioritization (80/20 Rule)"),
        ("PDCA cycle", "Continuous quality improvement (Kaizen)"),
        ("Customer / patient EHR", "Customer / patient focus (Zero Defects)")
    ]
    add_table_slide(s68, "Software feature → TQM concept", ["Software Feature", "Formal TQM Concept / Principle"], tqm_map_data, [5.0, 6.333])
    add_notes(s68, "This table is the cornerstone of Review 1 and 2: demonstrating that software features map to academic quality concepts.")

    # =========================================================================
    # SLIDE 69: Quality dashboard
    # =========================================================================
    s69 = prs.slides.add_slide(blank_layout)
    set_bg(s69)
    add_header(s69, "Quality dashboard — Real-Time Quality Metrics")
    q_metrics = [
        ("Stock accuracy", "99.2%", "Zero unrecorded shrinkage", TEAL_ACCENT),
        ("Billing errors", "0.0%", "Poka-Yoke blocks bad data", CORAL_DANGER),
        ("Expired stock dispensed", "0.0%", "100% FEFO cart lockout", BLUE_INFO),
        ("Low stock items", "12 items", "Automated reorder POs sent", AMBER_WARN),
        ("Complaints registered", "0 items", "Resolved at clinical intake", PURPLE_ACCENT),
        ("Returns & damaged", "2 items", "Logged with vendor exchange", NAVY_DARK)
    ]
    for idx, (title, val, desc, col) in enumerate(q_metrics):
        r = idx // 3
        c_i = idx % 3
        x = Inches(0.8) + Inches(c_i * 3.98)
        y = Inches(1.8) + Inches(r * 2.6)
        add_card(s69, x, y, Inches(3.78), Inches(2.4))
        tb = s69.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(3.38), Inches(2.0))
        tf = tb.text_frame
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK
        p2 = tf.add_paragraph()
        p2.text = val
        p2.font.size = Pt(28)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.space_after = Pt(4)
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_MUTED
    add_notes(s69, "Quality dashboard provides live data-driven metrics for management.")

    # =========================================================================
    # SLIDE 70: Pareto — from error_logs and returns
    # =========================================================================
    s70 = prs.slides.add_slide(blank_layout)
    set_bg(s70)
    add_header(s70, "Pareto — from error_logs and returns (Fix the top bars first. That is 80/20.)")
    pareto_data = [
        ("1. Wrong medicine attempt (Look-alike/sound-alike)", "18 attempts (45%)", "Targeted by CDSS allergy & generic search confirmation"),
        ("2. Qty > available stock (Oversell attempt)", "12 attempts (30%)", "Targeted by atomic stock ceiling validation"),
        ("3. Near expiry selection (<30 days)", "6 attempts (15%)", "Targeted by automated FEFO batch sorting"),
        ("4. Damaged packaging on delivery", "3 instances (7%)", "Targeted by pre-dispatch insulated checklist"),
        ("5. Other miscellaneous entry slips", "1 instance (3%)", "Targeted by UI field format validators")
    ]
    add_table_slide(s70, "Pareto — from error_logs and returns (Fix top bars first — 80/20)", ["Failure Mode (Error Type)", "Incident Count & Cumulative %", "Software TQM Countermeasure"], pareto_data, [4.0, 3.0, 4.333])
    add_notes(s70, "Pareto 80/20 analysis: resolving the top 2 error categories eliminates 75% of all dispensing failures.")

    # =========================================================================
    # SLIDE 71: Fishbone — why billing errors happen
    # =========================================================================
    s71 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s71, "Fishbone (Ishikawa) — why billing errors happen (Effect: Dispensing Error)", [
        ("People (Staff)", "Rushed cashiers during peak rush hours; new untrained dispensers misreading doctors' handwriting.", TEAL_ACCENT),
        ("Process (Workflow)", "Lack of pre-dispense confirmation step; absence of standardized clinical sign-off protocols.", BLUE_INFO),
        ("Software (System)", "Legacy search showing similar sounding medicines without allergy cross-checks; UI freezing during print.", NAVY_DARK),
        ("Data (Integrity)", "Missing batch lot numbers; inaccurate physical expiry dates; unrecorded customer drug allergies.", CORAL_DANGER),
        ("Machine (Hardware)", "Slow workstation PCs; unresponsive barcode scanners; missed mouse clicks on tiny UI buttons.", AMBER_WARN)
    ])
    add_notes(s71, "Fishbone diagram dissects root causes across People, Process, Software, Data, and Machine.")

    # =========================================================================
    # SLIDE 72: FMEA — from automated error logs
    # =========================================================================
    s72 = prs.slides.add_slide(blank_layout)
    fmea_data = [
        ("Sell expired medicine", "10 (Fatal)", "4 (Occasional)", "3 (Moderate)", "120 (Critical)", "Hard block: cart checkout locked"),
        ("Dispense allergen drug", "10 (Fatal)", "3 (Low)", "4 (Moderate)", "120 (Critical)", "CDSS warning dialog & override block"),
        ("Qty > stock oversell", "8 (Severe)", "5 (Frequent)", "3 (Moderate)", "120 (Critical)", "Pre-save inventory assertion check"),
        ("Duplicate barcode scan", "6 (Moderate)", "2 (Rare)", "2 (High)", "24 (Low)", "Unique constraint on SKU barcode"),
        ("Login brute-force attempt", "7 (High)", "3 (Low)", "2 (High)", "42 (Low)", "15-second lockout & audit alert")
    ]
    add_table_slide(s72, "FMEA — from automated error logs (RPN = Severity x Occurrence x Detection)", ["Failure Mode", "S (1-10)", "O (1-10)", "D (1-10)", "RPN", "Implemented Action / Control"], fmea_data, [2.5, 1.2, 1.2, 1.2, 1.5, 3.733])
    add_notes(s72, "FMEA quantifies risk: our hard blocks reduce high-RPN failure modes from 120 down to zero in practice.")

    # =========================================================================
    # SLIDE 73: How logs feed FMEA
    # =========================================================================
    s73 = prs.slides.add_slide(blank_layout)
    add_stacked_cards(s73, "How logs feed FMEA", [
        ("1. Cashier attempts an invalid action or system blocks it", "Operator attempts to add expired drug or dispense penicillin to allergic patient.", TEAL_ACCENT),
        ("2. error_logs / audit_logs get an append-only row", "System writes event timestamp, user ID, error code (E01-E05), and transaction details.", BLUE_INFO),
        ("3. tqm_report counts each code frequency", "Automated SQL aggregator groups errors and calculates monthly occurrence metrics.", NAVY_DARK),
        ("4. High count = high Occurrence rating (O)", "Dynamic feedback loop updates the Occurrence score in the FMEA register.", PURPLE_ACCENT),
        ("5. Prioritized engineering action", "High RPN items trigger software updates and staff retraining under TQM governance.", AMBER_WARN)
    ])
    add_notes(s73, "Closed feedback loop: telemetry logs automatically compute FMEA occurrence ratings.")

    # =========================================================================
    # SLIDE 74: PDCA on the same problem
    # =========================================================================
    s74 = prs.slides.add_slide(blank_layout)
    set_bg(s74)
    add_header(s74, "PDCA on the same problem (Deming Cycle: Oversell & Expiry Defects)")
    pdca_cards = [
        ("PLAN", "Problem Identified:\nToo many qty > stock and near-expiry selection errors occurring during peak counter hours.", TEAL_ACCENT),
        ("DO", "Software Implementation:\nImplement automated FEFO batch selection and display live available stock with pre-save locks.", BLUE_INFO),
        ("CHECK", "Empirical Verification:\nMonitor error_logs code E01 and E03 over the next trading month. Validate zero error escapes.", AMBER_WARN),
        ("ACT", "Standardization:\nCodify the FEFO algorithm and pre-save locks as mandatory enterprise baseline standards.", NAVY_DARK)
    ]
    for idx, (stage, body, col) in enumerate(pdca_cards):
        r = idx // 2
        c_i = idx % 2
        x = Inches(0.8) + Inches(c_i * 5.95)
        y = Inches(1.8) + Inches(r * 2.6)
        add_card(s74, x, y, Inches(5.75), Inches(2.4))
        bar = s74.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), Inches(2.4))
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()
        tb = s74.shapes.add_textbox(x + Inches(0.25), y + Inches(0.12), Inches(5.35), Inches(2.16))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = stage
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.space_after = Pt(6)
        for line in body.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(2)
    add_notes(s74, "Deming's Plan-Do-Check-Act cycle applied to continuously eliminate inventory defects.")

    # =========================================================================
    # SLIDE 75: Sale flow
    # =========================================================================
    s75 = prs.slides.add_slide(blank_layout)
    set_bg(s75)
    add_header(s75, "Sale flow (Complete Customer Dispensing Sequence)")
    sale_flow = [
        ("Login", "Cashier authenticates at Front Counter A terminal."),
        ("Billing", "Opens POS express billing terminal; barcode focus."),
        ("Search", "Scans barcode or 1-clicks approved prescription."),
        ("Qty", "Enters required units; auto FEFO batch selection."),
        ("Valid?", "Validators check non-blank, non-negative inputs."),
        ("Stock?", "Asserts quantity requested <= available batch balance."),
        ("Expiry?", "Asserts batch days_to_expiry > 0 (No expired lot)."),
        ("Save + Audit", "Commits ACID invoice, cuts stock, writes audit_log.")
    ]
    for idx, (title, desc) in enumerate(sale_flow):
        r = idx // 4
        c_i = idx % 4
        x = Inches(0.8) + Inches(c_i * 2.98)
        y = Inches(1.8) + Inches(r * 2.6)
        add_card(s75, x, y, Inches(2.78), Inches(2.4))
        hb = s75.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(2.78), Inches(0.45))
        hb.fill.solid()
        hb.fill.fore_color.rgb = NAVY_DARK if (r + c_i) % 2 == 0 else TEAL_ACCENT
        hb.line.fill.background()
        tb = s75.shapes.add_textbox(x, y + Inches(0.05), Inches(2.78), Inches(0.35))
        p = tb.text_frame.paragraphs[0]
        p.text = f"{idx+1}. {title}"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb2 = s75.shapes.add_textbox(x + Inches(0.1), y + Inches(0.55), Inches(2.58), Inches(1.75))
        p2 = tb2.text_frame.paragraphs[0]
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN
    add_notes(s75, "8 sequential stages guaranteeing that every completed sale is clinical, fiscal, and audit verified.")

    # =========================================================================
    # SLIDE 76: Purchase flow
    # =========================================================================
    s76 = prs.slides.add_slide(blank_layout)
    set_bg(s76)
    add_header(s76, "Purchase flow (Goods Receipt & Inwarding Pipeline)")
    purch_flow = [
        ("Supplier", "Select distributor from approved master directory."),
        ("Purchase", "Open consignment inwarding modal with PO reference."),
        ("Receive & Validate", "Inspect medicine name, batch, qty, cost, and expiry."),
        ("Increase Stock", "Atomically increment stock ledger in SQLite database."),
        ("Inventory", "Batch becomes available for FIFO/FEFO dispensing."),
        ("Low Stock?", "System evaluates if inventory remains below reorder level."),
        ("Near Expiry?", "Calculates days to expiry and assigns visual tag."),
        ("Alert Dashboard", "Updates manager dashboard with updated stock count.")
    ]
    for idx, (title, desc) in enumerate(purch_flow):
        r = idx // 4
        c_i = idx % 4
        x = Inches(0.8) + Inches(c_i * 2.98)
        y = Inches(1.8) + Inches(r * 2.6)
        add_card(s76, x, y, Inches(2.78), Inches(2.4))
        hb = s76.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(2.78), Inches(0.45))
        hb.fill.solid()
        hb.fill.fore_color.rgb = NAVY_DARK if (r + c_i) % 2 == 0 else BLUE_INFO
        hb.line.fill.background()
        tb = s76.shapes.add_textbox(x, y + Inches(0.05), Inches(2.78), Inches(0.35))
        p = tb.text_frame.paragraphs[0]
        p.text = f"{idx+1}. {title}"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb2 = s76.shapes.add_textbox(x + Inches(0.1), y + Inches(0.55), Inches(2.58), Inches(1.75))
        p2 = tb2.text_frame.paragraphs[0]
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN
    add_notes(s76, "Procurement workflow ensuring accurate stock counts and automated replenishment updates.")

    # =========================================================================
    # SLIDE 77: Build this much first
    # =========================================================================
    s77 = prs.slides.add_slide(blank_layout)
    set_bg(s77)
    add_header(s77, "Build this much first (Review 1 Scope Delivered)")
    first_blocks = [
        ("1. Login + Roles", "Staff authentication across 5 RBAC roles with terminal location selectors."),
        ("2. Medicines + Stock Fields", "Complete batch schema (batch lot, days to expiry, rack coordinate, cold chain)."),
        ("3. Billing with 3 Checks", "Stock ceiling check, expiry hard lockout, and CDSS allergy interception."),
        ("4. Expiry + Low-Stock Tiles", "Color-coded countdown badges (<30d Red, <90d Yellow, >90d Green)."),
        ("5. Audit + Error Log", "Append-only event stream recording every transaction and security attempt."),
        ("6. One Quality Page", "Executive quality dashboard displaying stock accuracy and till reconciliation.")
    ]
    for idx, (title, desc) in enumerate(first_blocks):
        r = idx // 2
        c_i = idx % 2
        x = Inches(0.8) + Inches(c_i * 5.95)
        y = Inches(1.8) + Inches(r * 1.7)
        add_card(s77, x, y, Inches(5.75), Inches(1.5))
        tb = s77.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), Inches(5.35), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = TEAL_ACCENT
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN
    add_notes(s77, "Review 1 delivers 100% of the foundational architecture and live working system.")

    # =========================================================================
    # SLIDE 78: Review 1 vs later
    # =========================================================================
    s78 = prs.slides.add_slide(blank_layout)
    set_bg(s78)
    add_header(s78, "Review 1 vs later (Project Maturity Roadmap)")
    add_card(s78, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.4))
    tb1 = s78.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.2), Inches(2.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "NOW (Review 1 Deliverables):"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = TEAL_ACCENT
    p1.space_after = Pt(8)
    r1_points = [
        "✓ GitHub Repository Setup & Version Control (`origin main` synced).",
        "✓ 6-Tier Modular Architecture (`core/`, `ui/`, `server/`, `config/`, `tests/`).",
        "✓ IEEE 830 Software Requirements Specification (SRS DOCX, PDF, and Markdown).",
        "✓ 14 Normalized Relational Tables in SQLite with ACID transactions.",
        "✓ Fully Operational Working Application: Native Desktop (WebView2) & Web Portal (FastAPI).",
        "✓ Complete End-to-End Sales Flow & 24/24 Automated Pytest Tests Passing."
    ]
    for pt in r1_points:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN

    add_card(s78, Inches(0.8), Inches(4.5), Inches(11.733), Inches(2.4))
    tb2 = s78.shapes.add_textbox(Inches(1.1), Inches(4.7), Inches(11.2), Inches(2.0))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "LATER REVIEWS (Review 2 & Final Review Scope):"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = BLUE_INFO
    p2.space_after = Pt(8)
    r2_points = [
        "• Extended Longitudinal FMEA Analytics: Automated recalculation of Occurrence based on monthly error logs.",
        "• Automated Pareto Chart Generator: Real-time graphical generation of 80/20 root cause distributions.",
        "• Fishbone Cause-and-Effect Root Cause Registry for clinical contraindication incidents.",
        "• Deming PDCA Cycle Execution Logs: Formally tracking corrective actions from Check to Act standards.",
        "• Cloud Multi-Branch Database Replication and Mobile Patient Prescription Intake App."
    ]
    for pt in r2_points:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
    add_notes(s78, "Clear demarcation between Review 1 deliverables (completed) and Review 2 roadmap.")

    # =========================================================================
    # SLIDE 79: One sentence for viva
    # =========================================================================
    s79 = prs.slides.add_slide(blank_layout)
    set_bg(s79, NAVY_DARK)
    tb = s79.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "One sentence for viva"
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.font.color.rgb = TEAL_ACCENT
    p1.space_after = Pt(14)

    sentences = [
        "The UI never writes SQL.",
        "Validation stops bad data.",
        "Audit records who did what.",
        "Expired stock cannot be sold.",
        "Logs become Pareto, FMEA, PDCA."
    ]
    for s_txt in sentences:
        p = tf.add_paragraph()
        p.text = s_txt
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(6)

    p_end = tf.add_paragraph()
    p_end.text = "\nThank you respected professors and evaluators. (Candidate: Piyush Bhatt, Amrapali University)"
    p_end.font.size = Pt(14)
    p_end.font.bold = True
    p_end.font.color.rgb = RGBColor(148, 163, 184)
    add_notes(s79, "Memorize this slide for your closing statement: The UI never writes SQL. Validation stops bad data. Audit records who did what. Expired stock cannot be sold. Logs become Pareto, FMEA, PDCA.")

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TQM Pharm_TQM_Presentation_Piyush_Bhatt.pptx")
    prs.save(output_path)
    print(f"[SUCCESS] Complete 79-Slide PowerPoint generated successfully at: {output_path}")

    # Export to PDF via PowerPoint COM
    try:
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TQM Pharm_TQM_Presentation_Piyush_Bhatt.pdf")
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        deck = ppt_app.Presentations.Open(os.path.abspath(output_path), WithWindow=False)
        deck.SaveAs(os.path.abspath(pdf_path), 32)
        deck.Close()
        ppt_app.Quit()
        print(f"[SUCCESS] Complete 79-Slide PDF generated successfully at: {pdf_path}")
    except Exception as e:
        print(f"[WARNING] PowerPoint COM export failed: {e}")

if __name__ == "__main__":
    build_presentation()
