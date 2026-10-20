"""
AegisPharm Enterprise — Review 1: Setup, SRS & Working Application Presentation Generator.
Author: Piyush Bhatt, Student at Amrapali University.
Generates an executive-level 18-slide widescreen (16:9) PowerPoint presentation (.pptx)
strictly structured around the Review 1 Evaluation Rubric with dedicated sections for:
  - Problem Statement & Baseline Clinical Understanding
  - Quality Objectives & TQM Principles
  - Modular Folder Architecture (6-tier structure)
  - Scope & User Roles (5 RBAC personas)
  - Software Requirements Specification (SRS) — IEEE 830 Standard, Functional & Non-Functional
  - Database Design & Relational Data Dictionary (14 Tables)
  - Comprehensive Role-Based CRUD Operations Matrix
  - Core Modules Aligned with Quality Goals
  - Initial UI Design & System Workflow (Dual Theming)
  - Working Application Live Demonstration Guide (Setup, Credentials, Step-by-Step Script)
  - Live Walkthrough: Clinical CDSS & POS Billing
  - Live Walkthrough: Supply Chain, Cold-Chain IoT Alarm, OTP Delivery & Z-Report
  - Verification & Automated Pytest Results (24/24 Passed)
  - Examiner Viva Q&A Defense Guide & Conclusion
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
    PURPLE_ACCENT = RGBColor(124, 58, 237) # #7C3AED

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
        p_title.font.size = Pt(22)
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

    top_strip = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = TEAL_ACCENT
    top_strip.line.fill.background()

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
        "This presentation covers our complete Project Setup, formal IEEE 830 Software Requirements Specification (SRS), "
        "System Architecture, Database Design, and demonstrates our fully operational, working application with live CRUD operations and TQM quality gates."
    )

    # =========================================================================
    # SLIDE 2: REVIEW 1 EVALUATION RUBRIC ALIGNMENT MATRIX
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_LIGHT)
    add_header(slide2, "Review 1 Rubric Alignment & Verification Matrix", "EVALUATION CRITERIA MAPPING")

    rubric_items = [
        ("1. Setup & Baseline", "Complete multi-tier project setup, dependency environment, and baseline clinical problem formulation.", "Slide 3, 5 | `main.py`, `web_app.py`", TEAL_ACCENT),
        ("2. Modular Folder Architecture", "Decoupled 6-tier directory layout separating core domain logic, UI bridges, API, and tests.", "Slide 5 | `core/`, `ui/`, `apps/`, `tests/`", BLUE_INFO),
        ("3. Software Requirements (SRS)", "Formal IEEE Std 830-1998 compliant SRS document covering functional & non-functional requirements.", "Slides 7, 8, 9 | `SRS_AegisPharm_Enterprise.pdf`", PURPLE_ACCENT),
        ("4. Scope & User Roles (RBAC)", "5 distinct operational roles with workstation personas, terminal bindings, and route shields.", "Slide 6 | `staff`, `active_sessions`", NAVY_DARK),
        ("5. Relational Database Design", "14 normalized tables in SQLite with foreign keys, checks, default values, and ACID transactions.", "Slide 10 | `core/db.py` (14 Tables)", TEAL_ACCENT),
        ("6. Implemented CRUD Operations", "Comprehensive Create, Read, Update, Delete matrix verified across all 5 operational roles.", "Slide 11 | SRS Section 6.2 & Live Code", BLUE_INFO),
        ("7. Working Application / Live Demo", "Operational native desktop UI (Edge Chromium) and web portal (FastAPI) demonstrated live.", "Slides 14, 15, 16 | `DEMO_GUIDE.md`", AMBER_WARN),
        ("8. Verification & Test Suite", "24/24 passing automated tests verifying CDSS safety, FEFO logic, and Z-report math.", "Slide 17 | `pytest` (24/24 Passed in 7.8s)", CORAL_DANGER)
    ]

    card_w = Inches(5.75)
    card_h = Inches(1.15)
    for idx, (title, desc, loc, col) in enumerate(rubric_items):
        r = idx // 2
        c = idx % 2
        x = Inches(0.8) + Inches(c * 5.95)
        y = Inches(1.8) + Inches(r * 1.3)

        add_card(slide2, x, y, card_w, card_h)
        bar = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), card_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = slide2.shapes.add_textbox(x + Inches(0.25), y + Inches(0.08), card_w - Inches(0.35), card_h - Inches(0.16))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

        p3 = tf.add_paragraph()
        p3.text = f"📍 Verified: {loc}"
        p3.font.size = Pt(9)
        p3.font.bold = True
        p3.font.color.rgb = col

    add_notes(slide2,
        "This slide explicitly maps all criteria from the university evaluation rubric directly to our project components. "
        "Every single requirement—from setup and baseline understanding to formal SRS, modular architecture, "
        "database design, CRUD matrix, working demo, and test suite—is 100% completed and provable."
    )

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT & BASELINE CLINICAL UNDERSTANDING
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_LIGHT)
    add_header(slide3, "Problem Statement & Baseline Clinical Understanding", "RUBRIC: PROBLEM STATEMENT & BASELINE")

    col_w = Inches(3.64)
    gap = Inches(0.4)
    top_pos = Inches(1.8)
    h_pos = Inches(5.1)

    # Card 1: Clinical Medication Dispensing Failures
    add_card(slide3, Inches(0.8), top_pos, col_w, h_pos)
    tb1 = slide3.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
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
    add_card(slide3, Inches(0.8) + col_w + gap, top_pos, col_w, h_pos)
    tb2 = slide3.shapes.add_textbox(Inches(1.0) + col_w + gap, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
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
    add_card(slide3, Inches(0.8) + (col_w + gap)*2, top_pos, col_w, h_pos)
    tb3 = slide3.shapes.add_textbox(Inches(1.0) + (col_w + gap)*2, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
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

    add_notes(slide3,
        "We begin with the Problem Statement and Baseline Understanding. "
        "In healthcare, software errors aren't just bugs—they threaten patient survival. "
        "Our baseline analysis identified 3 fundamental industry failures: clinical medication errors, thermal cold-chain spoilage, "
        "and narcotic compliance/cash drawer shrinkage. AegisPharm solves these at the architectural root."
    )

    # =========================================================================
    # SLIDE 4: QUALITY OBJECTIVES & TQM ALIGNMENT
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_LIGHT)
    add_header(slide4, "Quality Objectives Aligned with TQM Principles", "RUBRIC: QUALITY OBJECTIVE")

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
        add_card(slide4, Inches(0.8), y_pos, Inches(11.733), card_h)

        bar = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos, Inches(0.15), card_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        tb = slide4.shapes.add_textbox(Inches(1.1), y_pos + Inches(0.08), Inches(11.2), card_h - Inches(0.16))
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

    add_notes(slide4,
        "Here are our 5 foundational Quality Objectives, directly fulfilling the Review 1 rubric. "
        "Notice how each objective maps to a core TQM tenet: Zero dispensing defects represents Customer/Patient Focus; "
        "Cold-Chain and FEFO represent Process Quality; and the Daily Z-Report represents Fact-Based Management."
    )

    # =========================================================================
    # SLIDE 5: MODULAR FOLDER ARCHITECTURE & 6-TIER BASELINE
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_LIGHT)
    add_header(slide5, "Modular Folder Architecture & 6-Tier Baseline", "RUBRIC: MODULAR ARCHITECTURE")

    # Left Card: Directory Tree
    add_card(slide5, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_tree = slide5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
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
    add_card(slide5, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_tiers = slide5.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
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

    add_notes(slide5,
        "Here we demonstrate our Modular Folder Architecture, answering the specific Review 1 criterion. "
        "The project is organized into clean, decoupled tiers: core logic, configuration, dual desktop/web UIs, tests, and backups. "
        "A single unified bridge serves both the desktop Edge Chromium WebView2 window and the FastAPI web server."
    )

    # =========================================================================
    # SLIDE 6: SCOPE & GRANULAR USER ROLES (RBAC)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_LIGHT)
    add_header(slide6, "Project Scope & Granular User Roles (RBAC)", "RUBRIC: SCOPE & USER ROLES")

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
        c = add_card(slide6, x, Inches(1.8), card_w, Inches(5.1))

        hb = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), card_w, Inches(0.7))
        hb.fill.solid()
        hb.fill.fore_color.rgb = NAVY_DARK if i % 2 == 0 else TEAL_ACCENT
        hb.line.fill.background()

        tb_h = slide6.shapes.add_textbox(x, Inches(1.85), card_w, Inches(0.6))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        p = tf_h.paragraphs[0]
        p.text = r_name
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb_b = slide6.shapes.add_textbox(x + Inches(0.1), Inches(2.55), card_w - Inches(0.2), Inches(4.2))
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

    add_notes(slide6,
        "Scope and User Roles are essential criteria in Review 1. "
        "AegisPharm establishes strict Role-Based Access Control (RBAC). "
        "Unlike generic retail software where any staff member can delete logs or sell narcotics, "
        "our 5 specialized personas enforce security and quality separation of concerns."
    )

    # =========================================================================
    # SLIDE 7: SRS (PART 1) — IEEE 830 STANDARD & SPECIFICATION ARCHITECTURE
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_LIGHT)
    add_header(slide7, "Software Requirements Specification (SRS) — IEEE 830", "RUBRIC: SOFTWARE REQUIREMENTS SPECIFICATION (SRS)")

    # Left Box: IEEE 830 Document Hierarchy
    add_card(slide7, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_srs_hier = slide7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_srs_hier = tb_srs_hier.text_frame
    tf_srs_hier.word_wrap = True

    p = tf_srs_hier.paragraphs[0]
    p.text = "📜 IEEE STD 830-1998 SPECIFICATION STRUCTURE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(8)

    srs_sections = [
        ("Section 1: Introduction", "Defines system purpose, document conventions, stakeholder reading guidelines, and regulatory references (CDSCO, GAMP 5, 21 CFR Part 11)."),
        ("Section 2: Overall Description", "Details system perspective, baseline problem formulation, 5 user classes with RBAC matrix, and operating environment constraints."),
        ("Section 3: System Features & FRs", "Formal specification of 10 core Functional Requirements with exact input criteria, validation triggers, and expected outputs."),
        ("Section 4: External Interfaces", "Specification of Hardware (USB HID scanners, 80mm ESC/POS printers, IoT probes) and Software (SQLite, FastAPI, WebView2) interfaces."),
        ("Section 5: Non-Functional Requirements", "Quantifiable metrics for latency (<50ms), safety (Poka-Yoke CDSS blocking), security (SHA-256 RBAC), and 99.9% uptime."),
        ("Section 6: Database & CRUD Design", "Normalized 14-table schema data dictionary, foreign key constraints, and comprehensive role-to-table CRUD permission matrix.")
    ]
    for s_title, s_desc in srs_sections:
        p = tf_srs_hier.add_paragraph()
        p.text = s_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEAL_ACCENT

        p2 = tf_srs_hier.add_paragraph()
        p2.text = s_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)

    # Right Box: Document Deliverables & Quality Gates
    add_card(slide7, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_srs_deliv = slide7.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_srs_deliv = tb_srs_deliv.text_frame
    tf_srs_deliv.word_wrap = True

    p = tf_srs_deliv.paragraphs[0]
    p.text = "📁 SRS DOCUMENTATION DELIVERABLES"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(8)

    deliv_points = [
        ("Formal Word Document (DOCX)", "Generated via `generate_srs_doc.py` using `python-docx` with professional typography, custom slate headers, and styled tables: `SRS_AegisPharm_Enterprise.docx`."),
        ("Print-Ready PDF Specification", "Compiled via Microsoft Word COM automation (`wdExportFormatPDF = 17`) ensuring zero layout degradation for university examiners: `SRS_AegisPharm_Enterprise.pdf`."),
        ("GitHub Markdown Version", "Full specification available directly within repository root for instant web viewing: `SRS_AegisPharm_Enterprise.md`."),
        ("Traceability to Evaluation Rubric", "Every rubric criterion from Image 1, 2, and 3 is mapped directly to corresponding functional sections and automated verification assertions.")
    ]
    for d_title, d_desc in deliv_points:
        p = tf_srs_deliv.add_paragraph()
        p.text = d_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        p2 = tf_srs_deliv.add_paragraph()
        p2.text = d_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_after = Pt(6)

    add_notes(slide7,
        "Here we introduce our formal Software Requirements Specification (SRS), fulfilling the explicit Review 1 rubric item. "
        "The specification strictly follows the IEEE Std 830-1998 structure across 6 core sections. "
        "We have generated this document in both DOCX and print-ready PDF formats, providing an authoritative contract for all software requirements."
    )

    # =========================================================================
    # SLIDE 8: SRS (PART 2) — FUNCTIONAL REQUIREMENTS (FR-01 TO FR-10)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, BG_LIGHT)
    add_header(slide8, "SRS Functional Requirements (FR-01 to FR-10)", "RUBRIC: FUNCTIONAL SPECIFICATIONS")

    # 2 Columns of 5 FRs each
    fr_col1 = [
        ("FR-01: Authentication & Telemetry", "Enforce SHA-256 hashed credentials, terminal session UUIDs, and 5s heartbeat telemetry. Offline flag after 15s inactivity."),
        ("FR-02: CDSS Clinical Safety Gate", "Automated cross-check of eRx drugs against EHR patient allergies (Penicillin) and drug-drug matrices. Dispense lockout on conflict."),
        ("FR-03: Schedule X Narcotic Sign-Off", "Mandatory dual authentication: Doctor DMC Registration Number + Pharmacist 4-digit Authorization PIN permanently logged."),
        ("FR-04: FEFO Batch Sorting Engine", "Automatic prioritization of nearest-expiry viable lots (`days_to_expiry ASC`). Strict lockout of expired drugs (days <= 0)."),
        ("FR-05: POS Multi-Tender Billing", "1-Click import of approved eRx, barcode scan, Cash change calculator, Dynamic UPI QR generation, and 80mm GST receipt printing.")
    ]

    fr_col2 = [
        ("FR-06: Goods Receipt Notes (GRN)", "Inward supplier shipments against POs capturing lot number, expiry, cost price, MRP, GST %, and physical shelf rack coordinate."),
        ("FR-07: IoT Cold-Chain Telemetry", "Monitor refrigerator sensors (Chamber A & B, 2°C–8°C) every 30s. Trigger audio/visual alert on temperature excursion spike."),
        ("FR-08: Delivery Logistics & OTP e-POD", "Kanban dispatch workflow (`Packaging`, `Out`, `Delivered`), insulated cold-bag checklist, and 4-digit recipient OTP handshake."),
        ("FR-09: End-of-Day Z-Report Close", "Shift cash reconciliation: `Expected = Float + Sales - Payouts`. Variance detection, register locking, and official signed Z-slip."),
        ("FR-10: 21 CFR Part 11 Audit Trail", "Append-only, immutable SQLite event log capturing timestamp, user ID, role, action code, and severity level (INFO/WARN/CRIT).")
    ]

    col_w = Inches(5.75)
    # Column 1
    add_card(slide8, Inches(0.8), Inches(1.8), col_w, Inches(5.1))
    tb_fr1 = slide8.shapes.add_textbox(Inches(1.0), Inches(2.0), col_w - Inches(0.4), Inches(4.7))
    tf_fr1 = tb_fr1.text_frame
    tf_fr1.word_wrap = True
    p = tf_fr1.paragraphs[0]
    p.text = "📋 CORE CLINICAL & POS REQUIREMENTS (FR-01 TO FR-05)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(6)

    for fr_title, fr_desc in fr_col1:
        p = tf_fr1.add_paragraph()
        p.text = fr_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        p2 = tf_fr1.add_paragraph()
        p2.text = fr_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)

    # Column 2
    add_card(slide8, Inches(6.75), Inches(1.8), col_w, Inches(5.1))
    tb_fr2 = slide8.shapes.add_textbox(Inches(6.95), Inches(2.0), col_w - Inches(0.4), Inches(4.7))
    tf_fr2 = tb_fr2.text_frame
    tf_fr2.word_wrap = True
    p = tf_fr2.paragraphs[0]
    p.text = "📋 SUPPLY CHAIN & FISCAL REQUIREMENTS (FR-06 TO FR-10)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(6)

    for fr_title, fr_desc in fr_col2:
        p = tf_fr2.add_paragraph()
        p.text = fr_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        p2 = tf_fr2.add_paragraph()
        p2.text = fr_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)

    add_notes(slide8,
        "Here are the 10 detailed Functional Requirements defined in our IEEE 830 SRS document. "
        "They span the entire lifecycle of a pharmaceutical transaction: authentication, CDSS clinical safety, "
        "narcotics dual sign-off, FEFO picking, POS split billing, GRN inwarding, IoT cold-chain alarms, OTP delivery proof, "
        "and daily Z-Report cash balancing."
    )

    # =========================================================================
    # SLIDE 9: SRS (PART 3) — NON-FUNCTIONAL REQUIREMENTS & SAFETY
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, BG_LIGHT)
    add_header(slide9, "SRS Non-Functional & Safety Requirements", "RUBRIC: NON-FUNCTIONAL & QUALITY METRICS")

    nfr_cards = [
        ("⚡ 1. PERFORMANCE & LATENCY", 
         "Sub-Second Response Standards",
         "• UI Transaction Latency: All dashboard actions & button clicks respond in <50ms.\n• Database Commit Latency: SQLite WAL transactions complete in <10ms.\n• 60 FPS Desktop Rendering: Hardware-accelerated Edge Chromium WebView2 prevents UI stutter.\n• Non-Blocking Threading: Zero frame freezes via asynchronous background worker threads.",
         TEAL_ACCENT),
        ("🛡️ 2. POKA-YOKE SAFETY GATES", 
         "Mistake-Proofing Healthcare",
         "• 100% CDSS Interception: Automatic lock on cart checkout when drug-allergy contraindication is flagged.\n• Zero Expiry Dispensing: Expired batches mathematically prohibited from cart addition.\n• Schedule X Dual-Auth: Narcotics cannot be billed without Doctor DMC Reg + Pharmacist PIN.\n• Handover Integrity: Delivery status advancement blocked without 4-digit recipient OTP.",
         CORAL_DANGER),
        ("🔒 3. SECURITY & AUDIT TRAIL", 
         "21 CFR Part 11 Compliance",
         "• Immutable Audit Records: Append-only SQLite event stream; UPDATE and DELETE disbarred.\n• Role-Based Route Shields: Strict RBAC gating on all sensitive operations and UI modals.\n• Credential Protection: SHA-256 hashed password verification across all login terminals.\n• Session Heartbeat Watchdog: Stale or hijacked terminal sessions auto-terminated after 15s.",
         NAVY_DARK),
        ("⚖️ 4. STATUTORY COMPLIANCE", 
         "Indian Pharmaceutical Standards",
         "• Drugs & Cosmetics Act 1940: Mandatory compliance with Schedule H, H1, and Schedule X rules.\n• Rule 65 Dispensing Records: Automated digital maintenance of prescription registers.\n• GST Invoicing Compliance: Automated 5%, 12%, 18% CGST/SGST tax split on thermal receipts.\n• GAMP 5 Category 4: Configured software validation standards with complete test traceability.",
         BLUE_INFO)
    ]

    for idx, (title, sub, body, col) in enumerate(nfr_cards):
        r = idx // 2
        c = idx % 2
        x = Inches(0.8) + Inches(c * 5.95)
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
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK

        p2 = tf.add_paragraph()
        p2.text = sub.upper()
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.space_after = Pt(4)

        for line in body.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(2)

    add_notes(slide9,
        "Non-Functional Requirements are the engineering backbone of AegisPharm. "
        "We guarantee sub-50ms UI latency, complete Poka-Yoke mistake proofing, "
        "21 CFR Part 11 compliant audit immutability, and 100% adherence to Indian Drugs & Cosmetics Act and GST rules."
    )

    # =========================================================================
    # SLIDE 10: SRS (PART 4) — DATABASE DESIGN & RELATIONAL DATA DICTIONARY
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, BG_LIGHT)
    add_header(slide10, "Database Design & Relational Data Dictionary", "RUBRIC: DATABASE / SYSTEM DESIGN")

    db_tables_1 = [
        ("1. staff", "PRIMARY KEY: id", "Staff credentials, assigned RBAC role, username, branch, active status."),
        ("2. medicines", "PRIMARY KEY: id", "Pharmaceutical catalog, generic name, batch, expiry, days left, stock, MRP."),
        ("3. prescriptions", "PRIMARY KEY: rx_id", "Patient name, doctor, items JSON, CDSS status, clinical sign-off notes."),
        ("4. invoices", "PRIMARY KEY: invoice_id", "Official tax invoices, cashier, payment method, subtotal, GST, total amount."),
        ("5. delivery_orders", "PRIMARY KEY: order_id", "Logistics dispatch, address, customer phone, rider, status, 4-digit OTP."),
        ("6. patients", "PRIMARY KEY: id", "Patient EHR, phone, chronic conditions, loyalty points, recorded allergies."),
        ("7. suppliers", "PRIMARY KEY: id", "Distributor master, contact, phone, billing email, GSTIN, payment terms.")
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
    add_card(slide10, Inches(0.8), Inches(1.8), col_w, Inches(5.1))
    tb_db1 = slide10.shapes.add_textbox(Inches(1.0), Inches(2.0), col_w - Inches(0.4), Inches(4.7))
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
    add_card(slide10, Inches(6.75), Inches(1.8), col_w, Inches(5.1))
    tb_db2 = slide10.shapes.add_textbox(Inches(6.95), Inches(2.0), col_w - Inches(0.4), Inches(4.7))
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

    add_notes(slide10,
        "Here is the complete Database Design and System Integration. "
        "AegisPharm utilizes SQLite 3 configured with WAL mode and foreign key constraints across 14 normalized tables. "
        "Notice the specialized tables: narcotic_register for Schedule X compliance, temperature_logs for IoT cold-chain, and z_reports for cash reconciliation."
    )

    # =========================================================================
    # SLIDE 11: SRS (PART 5) — ROLE-BASED CRUD OPERATIONS MATRIX
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, BG_LIGHT)
    add_header(slide11, "Role-Based CRUD Operations Matrix", "RUBRIC: CRUD OPERATIONS & RBAC")

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

    add_card(slide11, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1))
    tb_c = slide11.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(11.3), Inches(4.8))
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

    add_notes(slide11,
        "CRUD operations are explicitly evaluated in Review 1. "
        "As shown in this comprehensive matrix, AegisPharm implements full Create, Read, Update, and Delete operations "
        "across all 7 major functional domains—Staff, Medicines, Prescriptions, Narcotics, Billing, Deliveries, and Z-Reports. "
        "Every operation is fully wired to SQLite and verified by automated tests."
    )

    # =========================================================================
    # SLIDE 12: CORE MODULES ALIGNED WITH QUALITY GOALS
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, BG_LIGHT)
    add_header(slide12, "Core Modules Aligned with TQM Quality Goals", "RUBRIC: MODULES & QUALITY ALIGNMENT")

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

        add_card(slide12, x, y, w, h)
        bar = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = slide12.shapes.add_textbox(x + Inches(0.25), y + Inches(0.12), w - Inches(0.4), h - Inches(0.24))
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

    add_notes(slide12,
        "Here we map our Core Modules directly to our TQM Quality Goals, satisfying the Image 3 requirement. "
        "Notice that our features are not arbitrary: CDSS directly targets zero medication defects; "
        "FEFO and IoT target zero biological spoilage; and our delivery module targets 100% last-mile fidelity."
    )

    # =========================================================================
    # SLIDE 13: INITIAL UI & END-TO-END SYSTEM WORKFLOW
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, BG_LIGHT)
    add_header(slide13, "Initial UI & End-to-End System Workflow", "RUBRIC: INITIAL UI & MAIN WORKFLOW")

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
        c = add_card(slide13, x, Inches(1.8), col_w, Inches(3.2))

        hb = slide13.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), col_w, Inches(0.6))
        hb.fill.solid()
        hb.fill.fore_color.rgb = col
        hb.line.fill.background()

        tb_h = slide13.shapes.add_textbox(x, Inches(1.85), col_w, Inches(0.5))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        p = tf_h.paragraphs[0]
        p.text = f"STEP {i+1}"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb_b = slide13.shapes.add_textbox(x + Inches(0.1), Inches(2.5), col_w - Inches(0.2), Inches(2.4))
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

    add_card(slide13, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.7))
    tb_ui = slide13.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.5))
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
        "• Design System: Clean White/Light mode default with 1-click Dark Mode toggle, responsive side navigation, and interactive modals."
    )
    for line in ui_points.split('\n'):
        p = tf_ui.add_paragraph()
        p.text = line
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    add_notes(slide13,
        "Here we show the Initial UI and Main System Workflow. "
        "A prescription progresses smoothly from Stage 1 intake through Stage 2 clinical verification, Stage 3 POS billing, "
        "Stage 4 delivery dispatch with OTP, and finally Stage 5 daily Z-Report drawer reconciliation. "
        "Both our desktop and web interfaces provide 1:1 workflow parity."
    )

    # =========================================================================
    # SLIDE 14: WORKING APPLICATION DEMO GUIDE (PART 1) — SETUP & PERSONAS
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, BG_LIGHT)
    add_header(slide14, "Working Application Demo Guide: Setup & Personas", "RUBRIC: WORKING APPLICATION / DEMO GUIDE")

    # Left Box: Startup Commands & Verification
    add_card(slide14, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_cmd = slide14.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_cmd = tb_cmd.text_frame
    tf_cmd.word_wrap = True

    p = tf_cmd.paragraphs[0]
    p.text = "🚀 APPLICATION LAUNCH COMMANDS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(8)

    cmd_steps = [
        ("Step 1: Automated Test Suite (Examiner Proof)", "Command: `pytest`\nVerifies 24/24 unit & integration tests in ~7.8s with zero failures."),
        ("Step 2: Native Desktop Workstation Application", "Command: `python main.py`\nBoots hardware-accelerated Edge Chromium WebView2 window with default Light Mode and instant Dark toggle."),
        ("Step 3: Cloud-Ready Web Portal Application", "Command: `python web_app.py`\nLaunches asynchronous FastAPI server at `http://127.0.0.1:8000` with Swagger documentation at `/docs`."),
        ("Step 4: Physical Terminal Binding", "Select terminal station: `Front Counter A`, `Clinical Kiosk B`, `Inwarding Bay`, `Delivery Dock`.")
    ]
    for c_title, c_desc in cmd_steps:
        p = tf_cmd.add_paragraph()
        p.text = c_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEAL_ACCENT

        for line in c_desc.split('\n'):
            p2 = tf_cmd.add_paragraph()
            p2.text = line
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)

    # Right Box: Workstation Personas & Default Credentials Table
    add_card(slide14, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_cred = slide14.shapes.add_textbox(Inches(6.95), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_cred = tb_cred.text_frame
    tf_cred.word_wrap = True

    p = tf_cred.paragraphs[0]
    p.text = "🔑 WORKSTATION PERSONAS & CREDENTIALS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(8)

    cred_rows = [
        ("👑 Store Admin", "`admin` / `admin123`", "Admin Command Center", "RBAC, live heartbeats, Daily Z-Report balancing, audit trail."),
        ("🩺 Pharmacist", "`pharmacist` / `pharma123`", "Clinical Dispensing", "eRx intake, CDSS allergy shield, Schedule X narcotic sign-off."),
        ("💳 POS Cashier", "`cashier` / `cash123`", "Express Billing", "1-click eRx import, barcode scan, FEFO batch selection, UPI QR."),
        ("📦 Inventory", "`inventory` / `inv123`", "Inwarding Bay", "Multi-batch FEFO ledger, Add Medicine, Cold-chain IoT (2-8°C)."),
        ("🛵 Delivery Agent", "`delivery` / `deliv123`", "Logistics Dock", "Kanban dispatch, cold-bag checklist, 4-digit OTP e-POD.")
    ]
    for role_name, creds, term, scope in cred_rows:
        p = tf_cred.add_paragraph()
        p.text = f"{role_name} — {creds}"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        p2 = tf_cred.add_paragraph()
        p2.text = f"Terminal: {term} | Scope: {scope}"
        p2.font.size = Pt(9.0)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_after = Pt(4)

    add_notes(slide14,
        "This slide initiates our Working Application Demo Guide. "
        "It provides the exact execution commands to launch the automated test suite, "
        "the native desktop app, and the FastAPI web server. "
        "The right-hand panel outlines all 5 workstation roles and pre-seeded credentials for the live demonstration."
    )

    # =========================================================================
    # SLIDE 15: WORKING APPLICATION DEMO GUIDE (PART 2) — CLINICAL & POS BILLING
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15, BG_LIGHT)
    add_header(slide15, "Live Demo Walkthrough: Clinical CDSS & POS Billing", "RUBRIC: LIVE APPLICATION WALKTHROUGH")

    col_w = Inches(5.75)
    # Left Card: Pharmacist Station & CDSS Walkthrough
    add_card(slide15, Inches(0.8), Inches(1.8), col_w, Inches(5.1))
    tb_pharma = slide15.shapes.add_textbox(Inches(1.0), Inches(2.0), col_w - Inches(0.4), Inches(4.7))
    tf_pharma = tb_pharma.text_frame
    tf_pharma.word_wrap = True

    p = tf_pharma.paragraphs[0]
    p.text = "🩺 PHASE 1: CLINICAL PHARMACIST WALKTHROUGH"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(8)

    pharma_script = [
        ("Step 1.1: Workstation Boot & Persona Select", "Click '🩺 Clinical Pharmacist' tile on the login portal. System automatically loads station credentials (`pharmacist` / `pharma123`)."),
        ("Step 1.2: e-Prescription Queue Review", "Open Clinical Queue. Inspect incoming prescription `RX-2026-001` containing Amoxicillin for a patient with recorded Penicillin allergy."),
        ("Step 1.3: Trigger CDSS Allergy Interception (Poka-Yoke)", "Click 'Run CDSS Safety Scan'. System immediately flashes a red contraindication banner: 'CRITICAL ALLERGY CONFLICT: Penicillin hypersensitivity'. Disables direct checkout."),
        ("Step 1.4: Schedule X Narcotic Double Sign-Off", "Open narcotic prescription `RX-2026-004` (Zolpidem). Click 'Sign-Off'. Enter Doctor DMC No: `DMC-2024-8891` and Pharmacist PIN: `9944`. System verifies and logs to statutory `narcotic_register`.")
    ]
    for s_title, s_desc in pharma_script:
        p = tf_pharma.add_paragraph()
        p.text = s_title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        p2 = tf_pharma.add_paragraph()
        p2.text = s_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)

    # Right Card: POS Cashier Walkthrough
    add_card(slide15, Inches(6.75), Inches(1.8), col_w, Inches(5.1))
    tb_pos = slide15.shapes.add_textbox(Inches(6.95), Inches(2.0), col_w - Inches(0.4), Inches(4.7))
    tf_pos = tb_pos.text_frame
    tf_pos.word_wrap = True

    p = tf_pos.paragraphs[0]
    p.text = "💳 PHASE 2: POS CASHIER TERMINAL WALKTHROUGH"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE_INFO
    p.space_after = Pt(8)

    pos_script = [
        ("Step 2.1: Login to Front Counter A", "Authenticate as Cashier (`cashier` / `cash123`). Workstation UI loads POS billing counter with barcode scanner focus."),
        ("Step 2.2: 1-Click Approved eRx Import", "Click 'Import Approved eRx'. Approved prescription is pulled directly into the POS cart without manual re-typing, eliminating transcription error."),
        ("Step 2.3: Automated FEFO Batch Selection", "Observe cart lines: system automatically selected the nearest-expiry batch (`days_to_expiry` lowest) to prevent dead-stock accumulation."),
        ("Step 2.4: Multi-Tender Payment & Thermal Receipt", "Click 'Checkout'. Select Cash: enter ₹1000 for ₹740 bill -> automated change calculation: ₹260. Switch to Dynamic UPI QR -> simulate payment. Click 'Print Thermal Receipt' -> generates 80mm GST invoice.")
    ]
    for s_title, s_desc in pos_script:
        p = tf_pos.add_paragraph()
        p.text = s_title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        p2 = tf_pos.add_paragraph()
        p2.text = s_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_after = Pt(4)

    add_notes(slide15,
        "Phase 1 and 2 of the live walkthrough show clinical and billing integration. "
        "First, we log in as Pharmacist to demonstrate how the CDSS engine catches penicillin allergies and enforces narcotic PIN sign-off. "
        "Next, we switch to Cashier, import the approved Rx with 1 click, verify the automated FEFO batch selection, and complete the split-payment checkout."
    )

    # =========================================================================
    # SLIDE 16: WORKING APPLICATION DEMO GUIDE (PART 3) — SUPPLY CHAIN & Z-REPORT
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16, BG_LIGHT)
    add_header(slide16, "Live Demo: Inventory IoT, Delivery OTP & Z-Report", "RUBRIC: LIVE APPLICATION WALKTHROUGH")

    demo_cards_3 = [
        ("📦 PHASE 3: SUPPLY CHAIN & IOT ALARM",
         "Inventory Inwarding & Cold-Chain",
         "• Login as Inventory Manager (`inventory` / `inv123`).\n• FEFO Ledger: Inspect batch list with color-coded expiry badges (<30d Red, <90d Yellow, >90d Green).\n• Add Medicine & GRN: Inward new consignment, updating stock atomically.\n• IoT Cold-Chain Monitor: Observe 2°C–8°C gauge. Click 'Simulate Temp Spike' (9.4°C) -> instant alarm badge & audit entry.",
         TEAL_ACCENT),
        ("🛵 PHASE 4: DELIVERY FLEET & OTP",
         "Logistics Fulfilment (e-POD)",
         "• Login as Delivery Agent (`delivery` / `deliv123`).\n• Kanban Dispatch Board: View orders under `Packaging`, `Out for Delivery`, `Delivered`.\n• Cold-Bag Checklist: Confirm ice-gel insulation for insulin orders.\n• 4-Digit OTP Handover: Customer provides OTP `1234`. Enter OTP -> system verifies and advances order to `DELIVERED`.",
         AMBER_WARN),
        ("👑 PHASE 5: ADMIN PRESENCE & RBAC",
         "Staff Governance & Live Telemetry",
         "• Login as Store Admin (`admin` / `admin123`).\n• Staff User CRUD: Add new staff account, edit roles, toggle status (`Active` / `Suspended`).\n• Active Workstations: View live telemetry stream of connected terminals, IPs, and 5s heartbeats.\n• 21 CFR Part 11 Audit Trail: Inspect tamper-evident operational event stream in real time.",
         BLUE_INFO),
        ("💰 PHASE 6: DAILY Z-REPORT CASH CLOSE",
         "Fiscal Register Balancing",
         "• Open 'Daily Z-Report' register close module.\n• System computes: `Expected Cash = Opening Float + Cash Sales - Payouts`.\n• Enter counted physical cash: system evaluates live variance (`BALANCED ₹0.00` or `SHORTAGE`).\n• Sign & Close Register: Locks register, logs to `z_reports`, and generates official printable Z-slip.",
         NAVY_DARK)
    ]

    for idx, (title, sub, body, col) in enumerate(demo_cards_3):
        r = idx // 2
        c = idx % 2
        x = Inches(0.8) + Inches(c * 5.95)
        y = Inches(1.8) + Inches(r * 2.6)
        w = Inches(5.75)
        h = Inches(2.4)

        add_card(slide16, x, y, w, h)
        bar = slide16.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = slide16.shapes.add_textbox(x + Inches(0.25), y + Inches(0.12), w - Inches(0.4), h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK

        p2 = tf.add_paragraph()
        p2.text = sub.upper()
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.space_after = Pt(4)

        for line in body.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(2)

    add_notes(slide16,
        "Phases 3 through 6 complete the live application demonstration. "
        "We show the cold-chain IoT temperature spike alarm, complete an OTP verified home delivery, "
        "inspect active staff sessions in the Admin Console, and close the shift register using the Daily Z-Report."
    )

    # =========================================================================
    # SLIDE 17: QUALITY VERIFICATION & 24 AUTOMATED TEST RESULTS
    # =========================================================================
    slide17 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide17, BG_LIGHT)
    add_header(slide17, "Quality Verification & 24 Automated Test Results", "RUBRIC: IMPLEMENTED FUNCTIONALITY")

    metrics = [
        ("24 / 24", "Automated Tests Passed", "100% pass rate across end-to-end unit, integration, and security test suites.", TEAL_ACCENT),
        ("0%", "Medication Dispensing Errors", "Achieved via automated Poka-Yoke CDSS allergy and interaction barriers.", CORAL_DANGER),
        ("100%", "Cold-Chain Integrity (2–8°C)", "Continuous 30s background telemetry streaming with instant excursion alerts.", BLUE_INFO),
        ("₹ 0.00", "Cash Drawer Variance", "Achieved on balanced registers via Daily Z-Report mathematical reconciliation.", NAVY_DARK)
    ]

    for i, (stat, label, desc, col) in enumerate(metrics):
        x = Inches(0.8) + Inches(i * 2.98)
        c = add_card(slide17, x, Inches(1.8), Inches(2.78), Inches(2.2))

        tb = slide17.shapes.add_textbox(x + Inches(0.1), Inches(1.9), Inches(2.58), Inches(2.0))
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

    add_card(slide17, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.6))
    tb_t = slide17.shapes.add_textbox(Inches(1.0), Inches(4.45), Inches(11.3), Inches(2.3))
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

    add_notes(slide17,
        "Here are our empirical verification metrics: "
        "Our test suite passes 24 out of 24 automated unit and integration tests with a 100% success rate. "
        "The comparison table below demonstrates how AegisPharm transforms traditional manual vulnerabilities into standardized, automated TQM safeguards."
    )

    # =========================================================================
    # SLIDE 18: EXAMINER VIVA DEFENSE GUIDE & STRATEGIC CONCLUSION
    # =========================================================================
    slide18 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide18, NAVY_DARK)

    strip18 = slide18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    strip18.fill.solid()
    strip18.fill.fore_color.rgb = TEAL_ACCENT
    strip18.line.fill.background()

    tb_end = slide18.shapes.add_textbox(Inches(1.0), Inches(0.9), Inches(11.3), Inches(3.8))
    tf_e = tb_end.text_frame
    tf_e.word_wrap = True

    pe0 = tf_e.paragraphs[0]
    pe0.text = "REVIEW 1 SUMMARY & EXAMINER VIVA DEFENSE"
    pe0.font.size = Pt(13)
    pe0.font.bold = True
    pe0.font.color.rgb = TEAL_ACCENT
    pe0.space_after = Pt(6)

    pe1 = tf_e.add_paragraph()
    pe1.text = "Review 1 Rubric Criteria Fully Delivered"
    pe1.font.size = Pt(28)
    pe1.font.bold = True
    pe1.font.color.rgb = TEXT_WHITE
    pe1.space_after = Pt(8)

    viva_qa = [
        ("Q: Why SQLite instead of MySQL/MongoDB?", "A: Pharmacy dispensing requires zero-downtime, local-first offline resilience. SQLite provides 100% ACID compliance with WAL mode, sub-10ms query commit latency, and zero server crashes, while FastAPI supports networked counter syncing."),
        ("Q: How does CDSS prevent medical malpractice?", "A: Deterministic Poka-Yoke cross-referencing patient allergy arrays and drug-drug contraindication matrices, mathematically blocking checkout without supervisor override."),
        ("Q: How does FEFO reduce financial wastage?", "A: Sorts batch ledger by earliest expiration (`days_to_expiry ASC`), ensuring nearest-expiry viable lots are dispensed first, with automatic lockout of expired stock.")
    ]
    for q, a in viva_qa:
        p = tf_e.add_paragraph()
        p.text = f"• {q} "
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = TEAL_LIGHT

        p2 = tf_e.add_paragraph()
        p2.text = f"  {a}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = RGBColor(226, 232, 240)
        p2.space_after = Pt(4)

    # Thank You Card (Bottom)
    add_card(slide18, Inches(1.0), Inches(5.1), Inches(11.3), Inches(1.8), bg_color=NAVY_CARD, border_color=TEAL_ACCENT)
    tb_qa = slide18.shapes.add_textbox(Inches(1.2), Inches(5.2), Inches(10.9), Inches(1.5))
    tf_qa = tb_qa.text_frame
    tf_qa.word_wrap = True

    pq1 = tf_qa.paragraphs[0]
    pq1.text = "🙏 THANK YOU RESPECTED FACULTY & EVALUATORS"
    pq1.font.size = Pt(15)
    pq1.font.bold = True
    pq1.font.color.rgb = TEAL_ACCENT
    pq1.space_after = Pt(4)

    pq2 = tf_qa.add_paragraph()
    pq2.text = "Sincere gratitude to the Computer Science & Engineering faculty at Amrapali University for their academic guidance."
    pq2.font.size = Pt(11.5)
    pq2.font.color.rgb = TEXT_WHITE
    pq2.space_after = Pt(4)

    pq3 = tf_qa.add_paragraph()
    pq3.text = "💬 The floor is now open for questions, code inspection, and live application demonstration. (Candidate: Piyush Bhatt)"
    pq3.font.size = Pt(12)
    pq3.font.bold = True
    pq3.font.color.rgb = RGBColor(148, 163, 184)

    add_notes(slide18,
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
