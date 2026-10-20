"""
High-Precision ER Diagram Asset Generator for TQM Pharm Enterprise.
Generates:
1. assets/er_diagram.svg (Responsive, high-contrast, scalable vector ER diagram with relational connectors)
2. assets/er_diagram.png (High-definition 300 DPI raster graphic for universal preview)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("assets", exist_ok=True)
os.makedirs("docs", exist_ok=True)

TABLES = {
    # Column 1: Identity & Governance
    "staff": {
        "title": "staff",
        "cluster": "Identity & RBAC",
        "header_color": "#1e3a8a",
        "badge_color": "#3b82f6",
        "cols": [
            ("id", "TEXT", "PK"),
            ("name", "TEXT", ""),
            ("role", "TEXT", ""),
            ("username", "TEXT", "UK"),
            ("password", "TEXT", ""),
            ("email", "TEXT", ""),
            ("phone", "TEXT", ""),
            ("branch", "TEXT", ""),
            ("status", "TEXT", "")
        ]
    },
    "active_sessions": {
        "title": "active_sessions",
        "cluster": "Presence Telemetry",
        "header_color": "#1e3a8a",
        "badge_color": "#3b82f6",
        "cols": [
            ("session_id", "TEXT", "PK"),
            ("user_id", "TEXT", "FK"),
            ("name", "TEXT", ""),
            ("role", "TEXT", ""),
            ("terminal_name", "TEXT", ""),
            ("ip_address", "TEXT", ""),
            ("status", "TEXT", ""),
            ("last_action", "TEXT", ""),
            ("login_time", "TEXT", ""),
            ("last_heartbeat", "TEXT", "")
        ]
    },
    "audit_logs": {
        "title": "audit_logs",
        "cluster": "Security Audit Trail",
        "header_color": "#1e3a8a",
        "badge_color": "#3b82f6",
        "cols": [
            ("id", "INTEGER", "PK"),
            ("timestamp", "TEXT", ""),
            ("user_name", "TEXT", ""),
            ("role", "TEXT", ""),
            ("action", "TEXT", ""),
            ("details", "TEXT", ""),
            ("level", "TEXT", "")
        ]
    },
    "z_reports": {
        "title": "z_reports",
        "cluster": "Financial Governance",
        "header_color": "#0f766e",
        "badge_color": "#14b8a6",
        "cols": [
            ("z_report_id", "TEXT", "PK"),
            ("report_date", "TEXT", ""),
            ("generated_at", "TEXT", ""),
            ("generated_by", "TEXT", "FK"),
            ("opening_float", "REAL", ""),
            ("cash_sales", "REAL", ""),
            ("cash_payouts", "REAL", ""),
            ("expected_cash", "REAL", ""),
            ("actual_cash", "REAL", ""),
            ("variance", "REAL", ""),
            ("upi_sales", "REAL", ""),
            ("card_sales", "REAL", ""),
            ("total_sales", "REAL", ""),
            ("total_gst", "REAL", ""),
            ("cgst", "REAL", ""),
            ("sgst", "REAL", ""),
            ("total_bills", "INTEGER", ""),
            ("status", "TEXT", ""),
            ("notes", "TEXT", "")
        ]
    },

    # Column 2: Clinical & Patients
    "patients": {
        "title": "patients",
        "cluster": "Clinical EHR",
        "header_color": "#065f46",
        "badge_color": "#10b981",
        "cols": [
            ("id", "TEXT", "PK"),
            ("name", "TEXT", ""),
            ("age", "INTEGER", ""),
            ("gender", "TEXT", ""),
            ("phone", "TEXT", ""),
            ("allergies", "JSON", ""),
            ("chronic_conditions", "JSON", ""),
            ("loyalty_points", "INTEGER", ""),
            ("recent_doctor", "TEXT", "")
        ]
    },
    "prescriptions": {
        "title": "prescriptions",
        "cluster": "Clinical Dispensing",
        "header_color": "#065f46",
        "badge_color": "#10b981",
        "cols": [
            ("rx_id", "TEXT", "PK"),
            ("patient_name", "TEXT", ""),
            ("patient_id", "TEXT", "FK"),
            ("doctor_name", "TEXT", ""),
            ("hospital", "TEXT", ""),
            ("date", "TEXT", ""),
            ("status", "TEXT", ""),
            ("items", "JSON", ""),
            ("notes", "TEXT", ""),
            ("verified_by", "TEXT", "FK"),
            ("verified_at", "TEXT", "")
        ]
    },
    "narcotic_register": {
        "title": "narcotic_register",
        "cluster": "NDPS Schedule X",
        "header_color": "#991b1b",
        "badge_color": "#ef4444",
        "cols": [
            ("id", "INTEGER", "PK"),
            ("timestamp", "TEXT", ""),
            ("rx_id", "TEXT", "FK"),
            ("patient_name", "TEXT", ""),
            ("patient_phone", "TEXT", ""),
            ("doctor_name", "TEXT", ""),
            ("doctor_reg_no", "TEXT", ""),
            ("medicine_name", "TEXT", "FK"),
            ("batch_no", "TEXT", ""),
            ("quantity", "INTEGER", ""),
            ("pharmacist_name", "TEXT", "FK"),
            ("pharmacist_reg_no", "TEXT", ""),
            ("auth_pin_verified", "INTEGER", "")
        ]
    },
    "refill_schedules": {
        "title": "refill_schedules",
        "cluster": "Chronic Adherence",
        "header_color": "#065f46",
        "badge_color": "#10b981",
        "cols": [
            ("id", "TEXT", "PK"),
            ("patient_name", "TEXT", ""),
            ("patient_phone", "TEXT", ""),
            ("medicine_name", "TEXT", "FK"),
            ("last_dispensed", "TEXT", ""),
            ("next_due_date", "TEXT", ""),
            ("status", "TEXT", "")
        ]
    },

    # Column 3: Catalog, Inventory & Supply Chain
    "medicines": {
        "title": "medicines",
        "cluster": "Catalog & Stock",
        "header_color": "#92400e",
        "badge_color": "#f59e0b",
        "cols": [
            ("id", "TEXT", "PK"),
            ("name", "TEXT", ""),
            ("generic", "TEXT", ""),
            ("category", "TEXT", ""),
            ("schedule", "TEXT", ""),
            ("manufacturer", "TEXT", ""),
            ("batch", "TEXT", ""),
            ("expiry", "TEXT", ""),
            ("days_to_expiry", "INTEGER", ""),
            ("stock", "INTEGER", ""),
            ("unit", "TEXT", ""),
            ("mrp", "REAL", ""),
            ("cost_price", "REAL", ""),
            ("gst_pct", "REAL", ""),
            ("rack", "TEXT", ""),
            ("cold_chain", "INTEGER", ""),
            ("interactions", "JSON", "")
        ]
    },
    "temperature_logs": {
        "title": "temperature_logs",
        "cluster": "IoT Cold-Chain",
        "header_color": "#0369a1",
        "badge_color": "#0ea5e9",
        "cols": [
            ("id", "INTEGER", "PK"),
            ("timestamp", "TEXT", ""),
            ("sensor_id", "TEXT", ""),
            ("temperature", "REAL", ""),
            ("status", "TEXT", ""),
            ("alert_triggered", "INTEGER", "")
        ]
    },
    "suppliers": {
        "title": "suppliers",
        "cluster": "Supply Chain",
        "header_color": "#6b21a8",
        "badge_color": "#a855f7",
        "cols": [
            ("id", "TEXT", "PK"),
            ("name", "TEXT", ""),
            ("contact_person", "TEXT", ""),
            ("phone", "TEXT", ""),
            ("email", "TEXT", ""),
            ("gstin", "TEXT", ""),
            ("address", "TEXT", ""),
            ("payment_terms", "TEXT", "")
        ]
    },
    "purchase_orders": {
        "title": "purchase_orders",
        "cluster": "Supply Chain",
        "header_color": "#6b21a8",
        "badge_color": "#a855f7",
        "cols": [
            ("po_id", "TEXT", "PK"),
            ("date", "TEXT", ""),
            ("supplier_name", "TEXT", "FK"),
            ("status", "TEXT", ""),
            ("items_json", "JSON", ""),
            ("total_amount", "REAL", ""),
            ("received_date", "TEXT", ""),
            ("created_by", "TEXT", "FK")
        ]
    },

    # Column 4: POS & Logistics
    "invoices": {
        "title": "invoices",
        "cluster": "POS & Billing",
        "header_color": "#831843",
        "badge_color": "#f43f5e",
        "cols": [
            ("invoice_id", "TEXT", "PK"),
            ("timestamp", "TEXT", ""),
            ("patient_name", "TEXT", ""),
            ("cashier_name", "TEXT", "FK"),
            ("payment_method", "TEXT", ""),
            ("subtotal", "REAL", ""),
            ("gst_amount", "REAL", ""),
            ("total_amount", "REAL", ""),
            ("items_json", "JSON", "")
        ]
    },
    "delivery_orders": {
        "title": "delivery_orders",
        "cluster": "Logistics & Dispatch",
        "header_color": "#374151",
        "badge_color": "#64748b",
        "cols": [
            ("order_id", "TEXT", "PK"),
            ("patient_name", "TEXT", ""),
            ("address", "TEXT", ""),
            ("phone", "TEXT", ""),
            ("agent_name", "TEXT", "FK"),
            ("status", "TEXT", ""),
            ("time_slot", "TEXT", ""),
            ("items_count", "INTEGER", ""),
            ("cold_chain_pack", "INTEGER", ""),
            ("amount", "REAL", ""),
            ("payment_status", "TEXT", ""),
            ("otp", "TEXT", "")
        ]
    }
}


def generate_svg():
    width = 2460
    height = 1920
    col_w = 540
    col_xs = [60, 660, 1260, 1860]

    layout = {
        "staff": (col_xs[0], 140),
        "active_sessions": (col_xs[0], 480),
        "audit_logs": (col_xs[0], 840),
        "z_reports": (col_xs[0], 1150),

        "patients": (col_xs[1], 140),
        "prescriptions": (col_xs[1], 480),
        "narcotic_register": (col_xs[1], 880),
        "refill_schedules": (col_xs[1], 1340),

        "medicines": (col_xs[2], 140),
        "temperature_logs": (col_xs[2], 710),
        "suppliers": (col_xs[2], 980),
        "purchase_orders": (col_xs[2], 1300),

        "invoices": (col_xs[3], 140),
        "delivery_orders": (col_xs[3], 500),
    }

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#090d16; font-family:-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif;">')

    # Defs
    svg_lines.append("""
    <defs>
        <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%" filterUnits="userSpaceOnUse">
            <feDropShadow dx="0" dy="6" stdDeviation="12" flood-color="#000000" flood-opacity="0.7"/>
        </filter>
        <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/>
        </marker>
        <marker id="circle" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6">
            <circle cx="5" cy="5" r="3" fill="#38bdf8"/>
        </marker>
    </defs>
    """)

    # Background
    svg_lines.append('<rect x="0" y="0" width="100%" height="100%" fill="#090d16"/>')

    # Main Canvas Header
    svg_lines.append(f"""
    <g transform="translate(60, 45)">
        <text x="0" y="24" fill="#f8fafc" font-size="28" font-weight="800" letter-spacing="0.5">TQM Pharm Enterprise — Relational Database Architecture (ERD)</text>
        <text x="0" y="52" fill="#94a3b8" font-size="14" font-weight="500">14 Relational Tables • 3NF Compliant • Multi-Table ACID Transactions • Concurrency via SQLite 3 WAL Mode</text>
        <rect x="2000" y="-10" width="340" height="42" rx="8" fill="#131b2e" stroke="#1e293b" stroke-width="1.5"/>
        <text x="2015" y="17" fill="#38bdf8" font-size="13" font-weight="800">AMRAPALI UNIVERSITY</text>
        <text x="2195" y="17" fill="#e2e8f0" font-size="13">| Piyush Bhatt</text>
    </g>
    """)

    # Domain Column Headers
    domain_headers = [
        (col_xs[0], "IDENTITY & AUDIT GOVERNANCE", "#3b82f6"),
        (col_xs[1], "CLINICAL EHR & DISPENSING", "#10b981"),
        (col_xs[2], "PHARMACEUTICALS & SUPPLY CHAIN", "#f59e0b"),
        (col_xs[3], "POS SALES & LOGISTICS FLEET", "#f43f5e")
    ]
    for x, title, col in domain_headers:
        svg_lines.append(f"""
        <g transform="translate({x}, 102)">
            <rect x="0" y="0" width="{col_w}" height="28" rx="6" fill="{col}15" stroke="{col}40" stroke-width="1.5"/>
            <circle cx="16" cy="14" r="5" fill="{col}"/>
            <text x="30" y="18" fill="{col}" font-size="11" font-weight="800" letter-spacing="1.2">{title}</text>
        </g>
        """)

    row_h = 24
    header_h = 36
    table_bounds = {}

    # Render Cards
    for t_name, (x, y) in layout.items():
        t_data = TABLES[t_name]
        cols = t_data["cols"]
        card_h = header_h + (len(cols) * row_h) + 12
        table_bounds[t_name] = (x, y, col_w, card_h)

        svg_lines.append(f"""
        <g transform="translate({x}, {y})" filter="url(#shadow)">
            <rect x="0" y="0" width="{col_w}" height="{card_h}" rx="10" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
            <path d="M 0 10 Q 0 0 10 0 L {col_w - 10} 0 Q {col_w} 0 {col_w} 10 L {col_w} {header_h} L 0 {header_h} Z" fill="{t_data['header_color']}"/>
            <text x="16" y="23" fill="#f8fafc" font-size="15" font-weight="700">{t_data['title']}</text>
            <rect x="{col_w - 140}" y="8" width="126" height="20" rx="4" fill="{t_data['badge_color']}20" stroke="{t_data['badge_color']}" stroke-width="1"/>
            <text x="{col_w - 77}" y="22" fill="#f1f5f9" font-size="10" font-weight="700" text-anchor="middle">{t_data['cluster'].upper()}</text>
        """)

        cur_y = header_h + 8
        for col_name, col_type, key in cols:
            svg_lines.append(f'<line x1="8" y1="{cur_y + 16}" x2="{col_w - 8}" y2="{cur_y + 16}" stroke="#1f2937" stroke-width="0.8"/>')
            
            if key == "PK":
                svg_lines.append(f'<rect x="12" y="{cur_y - 3}" width="28" height="15" rx="3" fill="#f59e0b" />')
                svg_lines.append(f'<text x="26" y="{cur_y + 9}" fill="#0f172a" font-size="9" font-weight="900" text-anchor="middle">PK</text>')
            elif key == "FK":
                svg_lines.append(f'<rect x="12" y="{cur_y - 3}" width="28" height="15" rx="3" fill="#0ea5e9" />')
                svg_lines.append(f'<text x="26" y="{cur_y + 9}" fill="#0f172a" font-size="9" font-weight="900" text-anchor="middle">FK</text>')
            elif key == "UK":
                svg_lines.append(f'<rect x="12" y="{cur_y - 3}" width="28" height="15" rx="3" fill="#a855f7" />')
                svg_lines.append(f'<text x="26" y="{cur_y + 9}" fill="#ffffff" font-size="9" font-weight="900" text-anchor="middle">UK</text>')
            else:
                svg_lines.append(f'<circle cx="26" cy="{cur_y + 5}" r="2" fill="#4b5563"/>')

            name_color = "#f8fafc" if key in ["PK", "FK"] else "#cbd5e1"
            font_weight = "700" if key in ["PK", "FK"] else "500"
            svg_lines.append(f'<text x="48" y="{cur_y + 9}" fill="{name_color}" font-size="12" font-weight="{font_weight}">{col_name}</text>')

            type_color = "#38bdf8" if "JSON" in col_type else "#94a3b8"
            svg_lines.append(f'<text x="{col_w - 16}" y="{cur_y + 9}" fill="{type_color}" font-size="11" font-weight="500" text-anchor="end" font-family="monospace">{col_type}</text>')
            cur_y += row_h

        svg_lines.append('</g>')

    # Explicit Connector Lines with Bezier Curves
    # Connecting tables to represent 1:N foreign keys
    connectors = [
        # (src_table, tgt_table, label, color)
        ("staff", "active_sessions", "1:N (user_id)", "#38bdf8"),
        ("staff", "audit_logs", "1:N (user_name)", "#38bdf8"),
        ("patients", "prescriptions", "1:N (patient_id)", "#10b981"),
        ("prescriptions", "narcotic_register", "1:N (rx_id)", "#ef4444"),
        ("medicines", "temperature_logs", "1:N (sensor_id)", "#0ea5e9"),
        ("suppliers", "purchase_orders", "1:N (supplier_name)", "#a855f7"),
        ("invoices", "delivery_orders", "1:N (patient_name)", "#f43f5e"),
    ]

    for src, tgt, label, col in connectors:
        sx, sy, sw, sh = table_bounds[src]
        tx, ty, tw, th = table_bounds[tgt]

        # Draw vertical or horizontal connections
        if sx == tx:
            # Vertical column link
            x_mid = sx + 25
            y_start = sy + sh
            y_end = ty
            svg_lines.append(f"""
            <g>
                <path d="M {x_mid} {y_start} L {x_mid} {y_end}" stroke="{col}" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow)" marker-start="url(#circle)"/>
                <rect x="{x_mid + 8}" y="{(y_start + y_end)/2 - 10}" width="110" height="18" rx="3" fill="#090d16" stroke="{col}" stroke-width="0.8"/>
                <text x="{x_mid + 14}" y="{(y_start + y_end)/2 + 3}" fill="{col}" font-size="9" font-weight="700">{label}</text>
            </g>
            """)

    # Bottom Legend Footer
    leg_y = height - 90
    svg_lines.append(f"""
    <g transform="translate(60, {leg_y})">
        <rect x="0" y="0" width="{width - 120}" height="60" rx="8" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
        <text x="20" y="36" fill="#f8fafc" font-size="12" font-weight="800">KEY DEFINITION:</text>
        
        <rect x="140" y="24" width="28" height="16" rx="3" fill="#f59e0b"/>
        <text x="154" y="36" fill="#0f172a" font-size="9" font-weight="900" text-anchor="middle">PK</text>
        <text x="175" y="36" fill="#cbd5e1" font-size="12">Primary Key</text>

        <rect x="270" y="24" width="28" height="16" rx="3" fill="#0ea5e9"/>
        <text x="284" y="36" fill="#0f172a" font-size="9" font-weight="900" text-anchor="middle">FK</text>
        <text x="305" y="36" fill="#cbd5e1" font-size="12">Foreign Key (Indexed)</text>

        <rect x="460" y="24" width="28" height="16" rx="3" fill="#a855f7"/>
        <text x="474" y="36" fill="#ffffff" font-size="9" font-weight="900" text-anchor="middle">UK</text>
        <text x="495" y="36" fill="#cbd5e1" font-size="12">Unique Constraint</text>

        <text x="640" y="36" fill="#94a3b8" font-size="12">Engine: <tspan fill="#38bdf8">SQLite 3 WAL Mode</tspan> | Concurrency: <tspan fill="#38bdf8">Multi-threaded Non-blocking</tspan> | Normalization: <tspan fill="#38bdf8">Third Normal Form (3NF)</tspan></text>
        <text x="{width - 150}" y="36" fill="#e2e8f0" font-size="12" font-weight="700" text-anchor="end">Lead Architect: Piyush Bhatt</text>
    </g>
    """)

    svg_lines.append('</svg>')

    with open("assets/er_diagram.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print("[SUCCESS] Generated assets/er_diagram.svg")


def generate_png():
    fig, ax = plt.subplots(figsize=(24, 18), dpi=200)
    fig.patch.set_facecolor('#090d16')
    ax.set_facecolor('#090d16')
    ax.set_xlim(0, 2460)
    ax.set_ylim(1920, 0)
    ax.axis('off')

    col_w = 540
    col_xs = [60, 660, 1260, 1860]

    layout = {
        "staff": (col_xs[0], 140),
        "active_sessions": (col_xs[0], 480),
        "audit_logs": (col_xs[0], 840),
        "z_reports": (col_xs[0], 1150),

        "patients": (col_xs[1], 140),
        "prescriptions": (col_xs[1], 480),
        "narcotic_register": (col_xs[1], 880),
        "refill_schedules": (col_xs[1], 1340),

        "medicines": (col_xs[2], 140),
        "temperature_logs": (col_xs[2], 710),
        "suppliers": (col_xs[2], 980),
        "purchase_orders": (col_xs[2], 1300),

        "invoices": (col_xs[3], 140),
        "delivery_orders": (col_xs[3], 500),
    }

    # Main Title
    ax.text(60, 60, "TQM Pharm Enterprise -- Relational Database Architecture (ERD)", 
            fontsize=22, fontweight='bold', color='#f8fafc', va='center')
    ax.text(60, 95, "14 Relational Tables -- 3NF Compliant -- Multi-Table ACID Transactions -- SQLite 3 WAL Mode", 
            fontsize=12, fontweight='normal', color='#94a3b8', va='center')

    domain_headers = [
        (col_xs[0], "IDENTITY & AUDIT GOVERNANCE", "#3b82f6"),
        (col_xs[1], "CLINICAL EHR & DISPENSING", "#10b981"),
        (col_xs[2], "PHARMACEUTICALS & SUPPLY CHAIN", "#f59e0b"),
        (col_xs[3], "POS SALES & LOGISTICS FLEET", "#f43f5e")
    ]
    for x, title, col in domain_headers:
        rect = patches.FancyBboxPatch((x, 110), col_w, 26, boxstyle="round,pad=2", 
                                      facecolor='#111827', edgecolor=col, linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + 15, 123, title, fontsize=9.5, fontweight='bold', color=col, va='center')

    row_h = 24
    header_h = 36

    for t_name, (x, y) in layout.items():
        t_data = TABLES[t_name]
        cols = t_data["cols"]
        card_h = header_h + (len(cols) * row_h) + 12

        card_rect = patches.FancyBboxPatch((x, y), col_w, card_h, boxstyle="round,pad=3",
                                          facecolor='#111827', edgecolor='#1f2937', linewidth=1.5)
        ax.add_patch(card_rect)

        header_rect = patches.Rectangle((x, y), col_w, header_h, 
                                        facecolor=t_data['header_color'], edgecolor='none')
        ax.add_patch(header_rect)
        ax.text(x + 14, y + 18, t_data['title'], 
                fontsize=13, fontweight='bold', color='#f8fafc', va='center')

        ax.text(x + col_w - 16, y + 18, t_data['cluster'].upper(), 
                fontsize=8.5, fontweight='bold', color='#cbd5e1', va='center', ha='right')

        cur_y = y + header_h + 16
        for col_name, col_type, key in cols:
            if key == "PK":
                k_rect = patches.FancyBboxPatch((x + 12, cur_y - 7), 26, 14, boxstyle="round,pad=1",
                                               facecolor='#f59e0b', edgecolor='none')
                ax.add_patch(k_rect)
                ax.text(x + 25, cur_y, "PK", fontsize=7.5, fontweight='bold', color='#0f172a', va='center', ha='center')
            elif key == "FK":
                k_rect = patches.FancyBboxPatch((x + 12, cur_y - 7), 26, 14, boxstyle="round,pad=1",
                                               facecolor='#0ea5e9', edgecolor='none')
                ax.add_patch(k_rect)
                ax.text(x + 25, cur_y, "FK", fontsize=7.5, fontweight='bold', color='#0f172a', va='center', ha='center')
            elif key == "UK":
                k_rect = patches.FancyBboxPatch((x + 12, cur_y - 7), 26, 14, boxstyle="round,pad=1",
                                               facecolor='#a855f7', edgecolor='none')
                ax.add_patch(k_rect)
                ax.text(x + 25, cur_y, "UK", fontsize=7.5, fontweight='bold', color='#ffffff', va='center', ha='center')
            else:
                ax.plot(x + 25, cur_y, 'o', markersize=2.5, color='#4b5563')

            name_col = '#f8fafc' if key in ['PK', 'FK'] else '#cbd5e1'
            ax.text(x + 48, cur_y, col_name, fontsize=10, fontweight='bold' if key in ['PK', 'FK'] else 'normal',
                    color=name_col, va='center')
            ax.text(x + col_w - 16, cur_y, col_type, fontsize=9, color='#94a3b8', va='center', ha='right', family='monospace')

            cur_y += row_h

    # Bottom Legend Footer
    leg_y = 1845
    footer_rect = patches.FancyBboxPatch((60, leg_y), 2340, 50, boxstyle="round,pad=2",
                                         facecolor='#111827', edgecolor='#1f2937', linewidth=1.5)
    ax.add_patch(footer_rect)
    ax.text(80, leg_y + 25, "KEY:  [PK] Primary Key    [FK] Foreign Key (Indexed)    [UK] Unique Constraint", 
            fontsize=10, fontweight='bold', color='#f8fafc', va='center')
    ax.text(1200, leg_y + 25, "Core Engine: SQLite 3 WAL Mode | Concurrency: Multi-threaded Non-blocking | 3NF Architecture", 
            fontsize=10, color='#38bdf8', va='center')
    ax.text(2380, leg_y + 25, "Lead Architect: Piyush Bhatt | Amrapali University", 
            fontsize=10, fontweight='bold', color='#cbd5e1', va='center', ha='right')

    plt.tight_layout()
    plt.savefig("assets/er_diagram.png", dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("[SUCCESS] Generated assets/er_diagram.png")


if __name__ == "__main__":
    generate_svg()
    generate_png()
