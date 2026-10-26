"""
Centralized SQLite Database & Data Layer for Pharmacy Management System.
Stores persistent data for staff users, credentials, roles, active presence sessions,
audit logs, medicines catalog, prescriptions, sales invoices, delivery orders,
patients, suppliers, purchase orders, narcotic NDPS register, and cold chain logs.
"""

import sqlite3
import os
import json
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

try:
    from config.settings import get_settings
    _cfg_db = get_settings().system.db_path
    DB_PATH = os.path.abspath(os.path.expanduser(_cfg_db))
    DATA_DIR = os.path.dirname(DB_PATH)
except Exception:
    DATA_DIR = os.path.expanduser("~/.tqmpharm")
    DB_PATH = os.path.join(DATA_DIR, "pharmacy_system.db")

os.makedirs(DATA_DIR, exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Staff & Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL DEFAULT 'password123',
        email TEXT,
        phone TEXT,
        branch TEXT DEFAULT 'Apex Central - Branch #01',
        status TEXT DEFAULT 'Active'
    );
    """)
    
    # Check if password column exists in older schemas
    cursor.execute("PRAGMA table_info(staff)")
    columns = [row["name"] for row in cursor.fetchall()]
    if "password" not in columns:
        cursor.execute("ALTER TABLE staff ADD COLUMN password TEXT NOT NULL DEFAULT 'password123'")
    if "status" not in columns:
        cursor.execute("ALTER TABLE staff ADD COLUMN status TEXT DEFAULT 'Active'")
    
    # 2. Presence & Active Sessions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS active_sessions (
        session_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        terminal_name TEXT NOT NULL,
        ip_address TEXT DEFAULT '127.0.0.1',
        status TEXT DEFAULT 'Online',
        last_action TEXT DEFAULT 'Logged In',
        login_time TEXT NOT NULL,
        last_heartbeat TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES staff (id)
    );
    """)
    
    # 3. Live Audit / Event Log Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        user_name TEXT NOT NULL,
        role TEXT NOT NULL,
        action TEXT NOT NULL,
        details TEXT,
        level TEXT DEFAULT 'INFO'
    );
    """)
    
    # 4. Medicines Catalog Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        generic TEXT NOT NULL,
        category TEXT NOT NULL,
        schedule TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        batch TEXT NOT NULL,
        expiry TEXT NOT NULL,
        days_to_expiry INTEGER NOT NULL,
        stock INTEGER NOT NULL,
        unit TEXT NOT NULL,
        mrp REAL NOT NULL,
        cost_price REAL NOT NULL,
        gst_pct REAL NOT NULL,
        rack TEXT NOT NULL,
        cold_chain INTEGER DEFAULT 0,
        interactions TEXT DEFAULT '[]'
    );
    """)
    
    # 5. Prescriptions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        rx_id TEXT PRIMARY KEY,
        patient_name TEXT NOT NULL,
        patient_id TEXT NOT NULL,
        doctor_name TEXT NOT NULL,
        hospital TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        items TEXT NOT NULL,
        notes TEXT,
        verified_by TEXT,
        verified_at TEXT
    );
    """)
    
    # 6. Sales / Invoices Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        invoice_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        patient_name TEXT NOT NULL,
        cashier_name TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        subtotal REAL NOT NULL,
        gst_amount REAL NOT NULL,
        total_amount REAL NOT NULL,
        items_json TEXT NOT NULL
    );
    """)
    
    # 7. Delivery Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS delivery_orders (
        order_id TEXT PRIMARY KEY,
        patient_name TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        agent_name TEXT NOT NULL,
        status TEXT NOT NULL,
        time_slot TEXT NOT NULL,
        items_count INTEGER NOT NULL,
        cold_chain_pack INTEGER DEFAULT 0,
        amount REAL NOT NULL,
        payment_status TEXT NOT NULL,
        otp TEXT DEFAULT '1234'
    );
    """)

    # 8. Patients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        phone TEXT NOT NULL,
        allergies TEXT DEFAULT '[]',
        chronic_conditions TEXT DEFAULT '[]',
        loyalty_points INTEGER DEFAULT 0,
        recent_doctor TEXT
    );
    """)

    # 9. Schedule H1 / Schedule X Narcotic Dispensing Register
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS narcotic_register (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        rx_id TEXT NOT NULL,
        patient_name TEXT NOT NULL,
        patient_phone TEXT,
        doctor_name TEXT NOT NULL,
        doctor_reg_no TEXT,
        medicine_name TEXT NOT NULL,
        batch_no TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        pharmacist_name TEXT NOT NULL,
        pharmacist_reg_no TEXT NOT NULL,
        auth_pin_verified INTEGER DEFAULT 1
    );
    """)

    # 10. Purchase Orders / GRN Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase_orders (
        po_id TEXT PRIMARY KEY,
        date TEXT NOT NULL,
        supplier_name TEXT NOT NULL,
        status TEXT NOT NULL,
        items_json TEXT NOT NULL,
        total_amount REAL NOT NULL,
        received_date TEXT,
        created_by TEXT NOT NULL
    );
    """)

    # 11. Suppliers Directory
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        contact_person TEXT,
        phone TEXT,
        email TEXT,
        gstin TEXT,
        address TEXT,
        payment_terms TEXT DEFAULT '30 Days Net'
    );
    """)

    # 12. Cold Chain IoT Temperature Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS temperature_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        sensor_id TEXT NOT NULL,
        temperature REAL NOT NULL,
        status TEXT NOT NULL,
        alert_triggered INTEGER DEFAULT 0
    );
    """)

    # 13. Chronic Patient Refill Adherence
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS refill_schedules (
        id TEXT PRIMARY KEY,
        patient_name TEXT NOT NULL,
        patient_phone TEXT NOT NULL,
        medicine_name TEXT NOT NULL,
        last_dispensed TEXT NOT NULL,
        next_due_date TEXT NOT NULL,
        status TEXT DEFAULT 'Scheduled'
    );
    """)

    # 14. End-of-Day Financial Z-Reports & Cash Reconciliation
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS z_reports (
        z_report_id TEXT PRIMARY KEY,
        report_date TEXT NOT NULL,
        generated_at TEXT NOT NULL,
        generated_by TEXT NOT NULL,
        opening_float REAL NOT NULL,
        cash_sales REAL NOT NULL,
        cash_payouts REAL NOT NULL,
        expected_cash REAL NOT NULL,
        actual_cash REAL NOT NULL,
        variance REAL NOT NULL,
        upi_sales REAL NOT NULL,
        card_sales REAL NOT NULL,
        total_sales REAL NOT NULL,
        total_gst REAL NOT NULL,
        cgst REAL NOT NULL,
        sgst REAL NOT NULL,
        total_bills INTEGER NOT NULL,
        status TEXT DEFAULT 'CLOSED & SIGNED',
        notes TEXT
    );
    """)
    
    
    # 15. Consignment Batches (Pay-on-Sale / Sale-or-Return Stock)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consignment_batches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        po_id TEXT NOT NULL,
        supplier_name TEXT NOT NULL,
        medicine_id TEXT,
        medicine_name TEXT NOT NULL,
        batch_no TEXT NOT NULL,
        received_date TEXT NOT NULL,
        received_qty INTEGER NOT NULL,
        cost_price REAL NOT NULL,
        selling_price REAL NOT NULL,
        units_sold INTEGER NOT NULL DEFAULT 0,
        units_paid INTEGER NOT NULL DEFAULT 0,
        total_paid REAL NOT NULL DEFAULT 0.0,
        status TEXT DEFAULT 'Active',
        created_at TEXT NOT NULL
    );
    """)

    # 16. Supplier Settlement Payouts (Payments to Company for Sold Stock)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS supplier_payouts (
        payout_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        supplier_name TEXT NOT NULL,
        po_id TEXT,
        medicine_name TEXT,
        units_settled INTEGER NOT NULL DEFAULT 0,
        rate REAL NOT NULL DEFAULT 0.0,
        amount_paid REAL NOT NULL,
        payment_mode TEXT NOT NULL DEFAULT 'NEFT Bank Transfer',
        reference_no TEXT,
        notes TEXT,
        paid_by TEXT NOT NULL
    );
    """)

    # Seed initial default data
    seed_initial_data(cursor)
    
    conn.commit()
    conn.close()

def seed_initial_data(cursor):
    # 1. Staff default users
    cursor.execute("SELECT COUNT(*) as count FROM staff")
    if cursor.fetchone()["count"] == 0:
        sample_staff = [
            ("STF-01", "Dr. Rajesh Kulkarni", "Admin", "admin", "admin123", "admin@tqmpharm.com", "+91 98201 00001", "Apex Central - Branch #01", "Active"),
            ("STF-02", "Pooja Sharma, R.Ph", "Pharmacist", "pharmacist", "pharma123", "pooja.pharma@tqmpharm.com", "+91 98201 00002", "Apex Central - Branch #01", "Active"),
            ("STF-03", "Amit Deshmukh", "Cashier", "cashier", "cash123", "amit.pos@tqmpharm.com", "+91 98201 00003", "Apex Central - Branch #01", "Active"),
            ("STF-04", "Vikram Rathore", "Inventory Manager", "inventory", "inv123", "vikram.inv@tqmpharm.com", "+91 98201 00004", "Apex Central - Branch #01", "Active"),
            ("STF-05", "Ramesh Kumar", "Delivery Agent", "delivery", "deliv123", "ramesh.logistics@tqmpharm.com", "+91 98201 00005", "Apex Central - Branch #01", "Active"),
        ]
        cursor.executemany("INSERT INTO staff VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", sample_staff)

    # 2. Medicines Catalog
    cursor.execute("SELECT COUNT(*) as count FROM medicines")
    if cursor.fetchone()["count"] == 0:
        from data.mock_db import MEDICINES_CATALOG
        for m in MEDICINES_CATALOG:
            cursor.execute("""
            INSERT INTO medicines VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                m["id"], m["name"], m["generic"], m["category"], m["schedule"],
                m["manufacturer"], m["batch"], m["expiry"], m["days_to_expiry"],
                m["stock"], m["unit"], m["mrp"], m["cost_price"], m["gst_pct"],
                m["rack"], 1 if m.get("cold_chain") else 0, json.dumps(m.get("interactions", []))
            ))

    # 3. Prescriptions Queue
    cursor.execute("SELECT COUNT(*) as count FROM prescriptions")
    if cursor.fetchone()["count"] == 0:
        from data.mock_db import PRESCRIPTIONS_QUEUE
        for rx in PRESCRIPTIONS_QUEUE:
            cursor.execute("""
            INSERT INTO prescriptions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                rx["rx_id"], rx["patient"], rx["patient_id"], rx["doctor"],
                rx["hospital"], rx["date"], rx["status"], json.dumps(rx["items"]),
                rx["notes"], None, None
            ))

    # 4. Delivery Orders
    cursor.execute("SELECT COUNT(*) as count FROM delivery_orders")
    if cursor.fetchone()["count"] == 0:
        from data.mock_db import DELIVERY_DISPATCH
        for d in DELIVERY_DISPATCH:
            cursor.execute("""
            INSERT INTO delivery_orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                d["order_id"], d["patient"], d["address"], d["phone"],
                d["agent"], d["status"], d["time_slot"], d["items_count"],
                1 if d.get("cold_chain_pack") else 0, d["amount"], d["payment"], "4821"
            ))

    # 5. Patients
    cursor.execute("SELECT COUNT(*) as count FROM patients")
    if cursor.fetchone()["count"] == 0:
        from data.mock_db import PATIENTS
        for p in PATIENTS:
            cursor.execute("""
            INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["id"], p["name"], p["age"], p["gender"], p["phone"],
                json.dumps(p["allergies"]), json.dumps(p["chronic_conditions"]),
                p.get("loyalty_points", 100), p.get("recent_doctor", "")
            ))

    # 6. Suppliers
    cursor.execute("SELECT COUNT(*) as count FROM suppliers")
    if cursor.fetchone()["count"] == 0:
        sample_suppliers = [
            ("SUP-01", "MedLife Pharma Distributors", "Suresh Menon", "+91 98220 11223", "orders@medlife.com", "27AABCM1234F1Z5", "Plot 14, MIDC Industrial Area, Mumbai", "30 Days Net"),
            ("SUP-02", "Apex Healthcare Supply Co.", "Rajeev Khanna", "+91 98110 55443", "supply@apexhealth.in", "27AACCA9988G2Z1", "Unit 5, Pharma Logistics Park, Bhiwandi", "15 Days Net"),
            ("SUP-03", "ColdChain Vaccines India", "Dr. Arvind Nair", "+91 97690 44332", "logistics@coldchain.com", "27AABCC7744D1Z9", "Cold Hub 2, Vashi Cold Storage, Navi Mumbai", "Immediate (UPI/NEFT)")
        ]
        cursor.executemany("INSERT INTO suppliers VALUES (?, ?, ?, ?, ?, ?, ?, ?)", sample_suppliers)

    # 7. Initial Purchase Orders
    cursor.execute("SELECT COUNT(*) as count FROM purchase_orders")
    if cursor.fetchone()["count"] == 0:
        sample_pos = [
            ("PO-2026-881", "2026-10-05", "MedLife Pharma Distributors", "Goods Received", json.dumps([
                {"medicine": "Augmentin 625 Duo", "qty": 100, "rate": 148.00},
                {"medicine": "Pan-D Capsule", "qty": 150, "rate": 135.00}
            ]), 35050.00, "2026-10-07", "Vikram Rathore"),
            ("PO-2026-882", "2026-10-08", "ColdChain Vaccines India", "Pending Delivery", json.dumps([
                {"medicine": "Lantus Solostar Insulin Pen", "qty": 50, "rate": 540.00}
            ]), 27000.00, None, "Vikram Rathore")
        ]
        cursor.executemany("INSERT INTO purchase_orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)", sample_pos)

    # 8. Initial Narcotic Register entries
    cursor.execute("SELECT COUNT(*) as count FROM narcotic_register")
    if cursor.fetchone()["count"] == 0:
        now = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        INSERT INTO narcotic_register (timestamp, rx_id, patient_name, patient_phone, doctor_name, doctor_reg_no, medicine_name, batch_no, quantity, pharmacist_name, pharmacist_reg_no, auth_pin_verified)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (now, "RX-2026-077", "Suresh Mehta", "+91 98200 12345", "Dr. K. N. Joshi", "GMC-8823", "Alprax 0.5mg Tablet", "ALP-7703", 10, "Pooja Sharma, R.Ph", "PH-MH-44102"))

    # 9. Initial Cold Chain Logs
    cursor.execute("SELECT COUNT(*) as count FROM temperature_logs")
    if cursor.fetchone()["count"] == 0:
        base_time = datetime.now()
        for i in range(12):
            t_str = (base_time - timedelta(hours=i*2)).strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
            INSERT INTO temperature_logs (timestamp, sensor_id, temperature, status, alert_triggered)
            VALUES (?, ?, ?, ?, 0)
            """, (t_str, "SENSOR-FRIDGE-01", round(3.8 + (i % 4) * 0.3, 1), "Optimal (2-8°C)"))

    # 10. Initial Chronic Refills
    cursor.execute("SELECT COUNT(*) as count FROM refill_schedules")
    if cursor.fetchone()["count"] == 0:
        now_d = datetime.now()
        cursor.execute("""
        INSERT INTO refill_schedules VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("RF-101", "Rajesh Sharma", "+91 98765 43210", "Telma-H 40mg Tablet", (now_d - timedelta(days=25)).strftime("%Y-%m-%d"), (now_d + timedelta(days=5)).strftime("%Y-%m-%d"), "Due Soon"))
        cursor.execute("""
        INSERT INTO refill_schedules VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("RF-102", "Priya Verma", "+91 98112 34567", "Montair-LC Tablet", (now_d - timedelta(days=28)).strftime("%Y-%m-%d"), (now_d + timedelta(days=2)).strftime("%Y-%m-%d"), "Due Soon"))

    # 11. Initial Audit Logs
    cursor.execute("SELECT COUNT(*) as count FROM audit_logs")
    if cursor.fetchone()["count"] == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO audit_logs (timestamp, user_name, role, action, details, level) VALUES (?, ?, ?, ?, ?, ?)",
                       (now, "System", "System", "System Initialized", "All enterprise database tables verified and loaded.", "INFO"))

    # 12. Initial Consignment Batches (Pay-on-Sale Ledger)
    cursor.execute("SELECT COUNT(*) as count FROM consignment_batches")
    if cursor.fetchone()["count"] == 0:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_str = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        sample_consignments = [
            ("PO-2026-901", "MedLife Pharma Distributors", "MED-001", "Augmentin 625 Duo Tablet", "AUG-2025-09", date_str, 100, 10.0, 100.0, 50, 0, 0.0, "Active", now_str),
            ("PO-2026-881", "Apex Healthcare Supply Co.", "MED-002", "Pan-D Capsule", "PAND-883", date_str, 150, 135.0, 199.0, 40, 0, 0.0, "Active", now_str),
            ("PO-2026-882", "ColdChain Vaccines India", "MED-005", "Lantus Solostar Insulin Pen", "LAN-4401", date_str, 50, 540.0, 685.0, 15, 0, 0.0, "Active", now_str),
        ]
        cursor.executemany("""
        INSERT INTO consignment_batches (po_id, supplier_name, medicine_id, medicine_name, batch_no, received_date, received_qty, cost_price, selling_price, units_sold, units_paid, total_paid, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_consignments)



# --- USER AUTHENTICATION & STAFF CRUD FUNCTIONS ---

def authenticate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM staff WHERE (username = ? OR id = ?) AND status = 'Active'", (username.strip(), username.strip()))
    user = cur.fetchone()
    conn.close()
    if user and user["password"] == password.strip():
        return dict(user)
    return None

def get_all_staff():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, role, username, password, email, phone, branch, status FROM staff ORDER BY role ASC, name ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_staff_user(staff_id, name, role, username, password, email, phone, branch):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO staff (id, name, role, username, password, email, phone, branch, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Active')
        """, (staff_id.strip(), name.strip(), role.strip(), username.strip(), password.strip(), email.strip(), phone.strip(), branch.strip()))
        conn.commit()
        success, err = True, None
    except sqlite3.IntegrityError as e:
        success, err = False, f"Username or User ID already exists ({e})"
    except Exception as e:
        success, err = False, str(e)
    finally:
        conn.close()
    return success, err

def update_staff_user(staff_id, name, role, username, password, email, phone, branch, status="Active"):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        UPDATE staff 
        SET name = ?, role = ?, username = ?, password = ?, email = ?, phone = ?, branch = ?, status = ?
        WHERE id = ?
        """, (name.strip(), role.strip(), username.strip(), password.strip(), email.strip(), phone.strip(), branch.strip(), status.strip(), staff_id.strip()))
        conn.commit()
        success, err = True, None
    except Exception as e:
        success, err = False, str(e)
    finally:
        conn.close()
    return success, err

def delete_staff_user(staff_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM staff WHERE id = ?", (staff_id,))
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success


# --- MEDICINES & INVENTORY CRUD FUNCTIONS ---

def get_all_medicines():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM medicines ORDER BY name ASC")
    rows = cur.fetchall()
    conn.close()
    res = []
    for r in rows:
        d = dict(r)
        d["interactions"] = json.loads(d.get("interactions", "[]"))
        d["cold_chain"] = bool(d.get("cold_chain", 0))
        res.append(d)
    return res

def add_medicine(med_data):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO medicines (id, name, generic, category, schedule, manufacturer, batch, expiry, days_to_expiry, stock, unit, mrp, cost_price, gst_pct, rack, cold_chain, interactions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            med_data["id"], med_data["name"], med_data["generic"], med_data["category"],
            med_data["schedule"], med_data["manufacturer"], med_data["batch"],
            med_data["expiry"], med_data["days_to_expiry"], med_data["stock"],
            med_data["unit"], med_data["mrp"], med_data["cost_price"],
            med_data["gst_pct"], med_data["rack"],
            1 if med_data.get("cold_chain") else 0,
            json.dumps(med_data.get("interactions", []))
        ))
        conn.commit()
        success, err = True, None
    except Exception as e:
        success, err = False, str(e)
    finally:
        conn.close()
    return success, err

def update_medicine_stock(med_id, delta):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE medicines SET stock = MAX(0, stock + ?) WHERE id = ?", (delta, med_id))
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success

def delete_medicine(med_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM medicines WHERE id = ?", (med_id,))
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success


# --- PRESCRIPTIONS CRUD FUNCTIONS ---

def get_all_prescriptions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM prescriptions ORDER BY date DESC, rx_id DESC")
    rows = cur.fetchall()
    conn.close()
    res = []
    for r in rows:
        d = dict(r)
        try:
            raw_items = json.loads(d.get("items", "[]"))
        except Exception:
            raw_items = []
        norm_items = []
        for it in raw_items:
            if isinstance(it, dict):
                norm_items.append({
                    "medicine": it.get("medicine", "Medicine"),
                    "dosage": it.get("dosage", "1 tab daily"),
                    "qty": it.get("qty", 10),
                    "duration": it.get("duration", "As directed")
                })
            elif isinstance(it, str):
                norm_items.append({
                    "medicine": it,
                    "dosage": "1 tab daily",
                    "qty": 10,
                    "duration": "As directed"
                })
        d["items"] = norm_items
        res.append(d)
    return res

def add_prescription(rx_data):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO prescriptions (rx_id, patient_name, patient_id, doctor_name, hospital, date, status, items, notes, verified_by, verified_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rx_data["rx_id"], rx_data["patient_name"], rx_data["patient_id"],
            rx_data["doctor_name"], rx_data["hospital"], rx_data["date"],
            rx_data["status"], json.dumps(rx_data["items"]), rx_data.get("notes", ""),
            rx_data.get("verified_by"), rx_data.get("verified_at")
        ))
        conn.commit()
        success, err = True, None
    except Exception as e:
        success, err = False, str(e)
    finally:
        conn.close()
    return success, err

def update_prescription_status(rx_id, status, verified_by=None):
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if verified_by:
            cur.execute("UPDATE prescriptions SET status = ?, verified_by = ?, verified_at = ? WHERE rx_id = ?", (status, verified_by, now, rx_id))
        else:
            cur.execute("UPDATE prescriptions SET status = ? WHERE rx_id = ?", (status, rx_id))
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success


# --- INVOICES / BILLING CRUD FUNCTIONS ---

def create_invoice(invoice_data):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO invoices (invoice_id, timestamp, patient_name, cashier_name, payment_method, subtotal, gst_amount, total_amount, items_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            invoice_data["invoice_id"], invoice_data["timestamp"], invoice_data["patient_name"],
            invoice_data["cashier_name"], invoice_data["payment_method"], invoice_data["subtotal"],
            invoice_data["gst_amount"], invoice_data["total_amount"], json.dumps(invoice_data["items"])
        ))
        # Deduct stock for all items
        for it in invoice_data["items"]:
            med_id = it.get("med_id") or it.get("id")
            qty = it.get("qty", 1)
            if med_id:
                cur.execute("UPDATE medicines SET stock = MAX(0, stock - ?) WHERE id = ?", (qty, med_id))
                # Attribute sold units to active consignment batches for Pay-on-Sale tracking
        for it in invoice_data.get("items", []):
            med_id = it.get("med_id") or it.get("id")
            med_name = it.get("name") or it.get("medicine")
            qty = int(it.get("qty", 1))
            if not med_id and not med_name:
                continue
            cur.execute("""
            SELECT id, received_qty, units_sold 
            FROM consignment_batches 
            WHERE (medicine_id = ? OR medicine_name = ?) AND (received_qty > units_sold)
            ORDER BY received_date ASC, id ASC
            """, (med_id, med_name))
            c_batches = cur.fetchall()
            rem = qty
            for cb in c_batches:
                avail = cb["received_qty"] - cb["units_sold"]
                if avail > 0:
                    take = min(avail, rem)
                    cur.execute("UPDATE consignment_batches SET units_sold = units_sold + ? WHERE id = ?", (take, cb["id"]))
                    rem -= take
                    if rem <= 0:
                        break
        conn.commit()
        success, err = True, None
    except Exception as e:
        success, err = False, str(e)
    finally:
        conn.close()
    return success, err

def get_all_invoices(limit=100):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM invoices ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    res = []
    for r in rows:
        d = dict(r)
        try:
            raw_items = json.loads(d.get("items_json", "[]"))
        except Exception:
            raw_items = []
        norm_items = []
        for it in raw_items:
            if isinstance(it, dict):
                norm_items.append({
                    "med_id": it.get("med_id", "MED-000"),
                    "name": it.get("name", "Medicine Item"),
                    "batch": it.get("batch", "STD-01"),
                    "qty": it.get("qty", 1),
                    "rate": float(it.get("rate", 0.0)),
                    "amount": float(it.get("amount", it.get("rate", 0.0) * it.get("qty", 1)))
                })
            elif isinstance(it, str):
                tot = float(d.get("total_amount", 0.0))
                cnt = max(1, len(raw_items))
                norm_items.append({
                    "med_id": "MED-GEN",
                    "name": it,
                    "batch": "STD-01",
                    "qty": 1,
                    "rate": round(tot / cnt, 2),
                    "amount": round(tot / cnt, 2)
                })
        d["items"] = norm_items
        res.append(d)
    return res



# --- DELIVERY DISPATCH CRUD FUNCTIONS ---

def get_all_deliveries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM delivery_orders ORDER BY order_id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_delivery_order(deliv_data):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO delivery_orders (order_id, patient_name, address, phone, agent_name, status, time_slot, items_count, cold_chain_pack, amount, payment_status, otp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            deliv_data["order_id"], deliv_data["patient_name"], deliv_data["address"],
            deliv_data["phone"], deliv_data["agent_name"], deliv_data["status"],
            deliv_data["time_slot"], deliv_data["items_count"],
            1 if deliv_data.get("cold_chain_pack") else 0,
            deliv_data["amount"], deliv_data["payment_status"], deliv_data.get("otp", "1234")
        ))
        conn.commit()
        success, err = True, None
    except Exception as e:
        success, err = False, str(e)
    finally:
        conn.close()
    return success, err

def update_delivery_status(order_id, status):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE delivery_orders SET status = ? WHERE order_id = ?", (status, order_id))
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success


# --- NARCOTIC & PATIENTS & LOGS ---

def add_narcotic_record(rec_data):
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cur.execute("""
        INSERT INTO narcotic_register (timestamp, rx_id, patient_name, patient_phone, doctor_name, doctor_reg_no, medicine_name, batch_no, quantity, pharmacist_name, pharmacist_reg_no, auth_pin_verified)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            now, rec_data["rx_id"], rec_data["patient_name"], rec_data.get("patient_phone", ""),
            rec_data["doctor_name"], rec_data.get("doctor_reg_no", ""),
            rec_data["medicine_name"], rec_data["batch_no"], rec_data["quantity"],
            rec_data["pharmacist_name"], rec_data["pharmacist_reg_no"], 1
        ))
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success

def get_narcotic_records():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM narcotic_register ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_patients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients ORDER BY name ASC")
    rows = cur.fetchall()
    conn.close()
    res = []
    for r in rows:
        d = dict(r)
        d["allergies"] = json.loads(d.get("allergies", "[]"))
        d["chronic_conditions"] = json.loads(d.get("chronic_conditions", "[]"))
        res.append(d)
    return res

def add_patient(p_data):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO patients (id, name, age, gender, phone, allergies, chronic_conditions, loyalty_points, recent_doctor)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p_data["id"], p_data["name"], p_data["age"], p_data["gender"], p_data["phone"],
            json.dumps(p_data.get("allergies", [])), json.dumps(p_data.get("chronic_conditions", [])),
            p_data.get("loyalty_points", 0), p_data.get("recent_doctor", "")
        ))
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success

def get_all_suppliers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM suppliers ORDER BY name ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_purchase_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM purchase_orders ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    res = []
    for r in rows:
        d = dict(r)
        try:
            raw_items = json.loads(d.get("items_json", "[]"))
        except Exception:
            raw_items = []
        norm_items = []
        for it in raw_items:
            if isinstance(it, dict):
                norm_items.append({
                    "medicine": it.get("medicine", "Medicine"),
                    "qty": it.get("qty", 10),
                    "rate": float(it.get("rate", 0.0))
                })
            elif isinstance(it, str):
                norm_items.append({
                    "medicine": it,
                    "qty": 10,
                    "rate": 0.0
                })
        d["items"] = norm_items
        res.append(d)
    return res

def add_purchase_order(po_data):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO purchase_orders (po_id, date, supplier_name, status, items_json, total_amount, received_date, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            po_data["po_id"], po_data["date"], po_data["supplier_name"], po_data["status"],
            json.dumps(po_data["items"]), po_data["total_amount"],
            po_data.get("received_date"), po_data["created_by"]
        ))
        if po_data.get("status") in ("Received & Added to Stock", "Goods Received", "Delivered"):
            auto_inc = po_data.get("auto_increment_stock", False)
            _internal_inward_consignment(cur, po_data, auto_increment_stock=auto_inc)
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success

def get_temperature_logs(limit=20):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM temperature_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_temperature_log(sensor_id, temp, status="Optimal (2-8°C)"):
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert = 1 if (temp < 2.0 or temp > 8.0) else 0
    try:
        cur.execute("""
        INSERT INTO temperature_logs (timestamp, sensor_id, temperature, status, alert_triggered)
        VALUES (?, ?, ?, ?, ?)
        """, (now, sensor_id, temp, status, alert))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

def get_refill_schedules():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM refill_schedules ORDER BY next_due_date ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_refill_status(refill_id, status):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE refill_schedules SET status = ? WHERE id = ?", (status, refill_id))
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success

def get_patient_by_phone(phone):
    conn = get_connection()
    cur = conn.cursor()
    # Normalize comparison by stripping non-digit characters or checking suffix
    clean_p = "".join(ch for ch in phone if ch.isdigit())
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        db_p = "".join(ch for ch in r["phone"] if ch.isdigit())
        if clean_p and (clean_p in db_p or db_p in clean_p):
            d = dict(r)
            d["allergies"] = json.loads(d.get("allergies", "[]"))
            d["chronic_conditions"] = json.loads(d.get("chronic_conditions", "[]"))
            return d
    return None

def update_patient_loyalty(patient_id, points_delta):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE patients SET loyalty_points = MAX(0, loyalty_points + ?) WHERE id = ?", (points_delta, patient_id))
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success

def update_purchase_order_status(po_id, status, received_date=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        if received_date:
            cur.execute("UPDATE purchase_orders SET status = ?, received_date = ? WHERE po_id = ?", (status, received_date, po_id))
        else:
            cur.execute("UPDATE purchase_orders SET status = ? WHERE po_id = ?", (status, po_id))
        if status in ("Goods Received", "Received & Added to Stock", "Delivered"):
            cur.execute("SELECT * FROM purchase_orders WHERE po_id = ?", (po_id,))
            po_row = cur.fetchone()
            if po_row:
                p_dict = dict(po_row)
                try:
                    p_dict["items"] = json.loads(p_dict.get("items_json", "[]"))
                except Exception:
                    p_dict["items"] = []
                _internal_inward_consignment(cur, p_dict, auto_increment_stock=True)
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success

def get_dashboard_analytics():
    conn = get_connection()
    cur = conn.cursor()
    
    # Invoices stats
    cur.execute("SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as gross, COALESCE(SUM(gst_amount), 0) as total_gst FROM invoices")
    inv_row = cur.fetchone()
    total_sales_count = inv_row["count"] if inv_row else 0
    gross_sales = inv_row["gross"] if inv_row else 0.0
    total_gst = inv_row["total_gst"] if inv_row else 0.0
    
    # By payment method
    cur.execute("SELECT payment_method, COUNT(*) as cnt, COALESCE(SUM(total_amount), 0) as total FROM invoices GROUP BY payment_method")
    payment_breakdown = {r["payment_method"]: {"count": r["cnt"], "total": r["total"]} for r in cur.fetchall()}
    
    # Medicines count and stock alerts
    cur.execute("SELECT COUNT(*) as total_meds, SUM(CASE WHEN stock <= 20 THEN 1 ELSE 0 END) as low_stock, SUM(CASE WHEN days_to_expiry <= 90 THEN 1 ELSE 0 END) as exp_soon FROM medicines")
    med_row = cur.fetchone()
    total_meds = med_row["total_meds"] if med_row else 0
    low_stock_count = med_row["low_stock"] if med_row else 0
    exp_soon_count = med_row["exp_soon"] if med_row else 0
    
    # Prescriptions
    cur.execute("SELECT COUNT(*) as total_rx, SUM(CASE WHEN status LIKE '%Verification%' OR status LIKE '%Pending%' THEN 1 ELSE 0 END) as pending_rx, SUM(CASE WHEN status LIKE '%Verified%' OR status LIKE '%Approved%' THEN 1 ELSE 0 END) as approved_rx FROM prescriptions")
    rx_row = cur.fetchone()
    total_rx = rx_row["total_rx"] if rx_row else 0
    pending_rx = rx_row["pending_rx"] if rx_row else 0
    approved_rx = rx_row["approved_rx"] if rx_row else 0
    
    # Active sessions
    cur.execute("SELECT COUNT(*) as active_staff FROM active_sessions WHERE status = 'Online'")
    sess_row = cur.fetchone()
    active_staff = sess_row["active_staff"] if sess_row else 0
    
    # Deliveries
    cur.execute("SELECT COUNT(*) as total_deliv, SUM(CASE WHEN status LIKE '%Out for Delivery%' THEN 1 ELSE 0 END) as en_route, SUM(CASE WHEN status LIKE '%Delivered%' THEN 1 ELSE 0 END) as delivered FROM delivery_orders")
    deliv_row = cur.fetchone()
    total_deliv = deliv_row["total_deliv"] if deliv_row else 0
    en_route_deliv = deliv_row["en_route"] if deliv_row else 0
    delivered_deliv = deliv_row["delivered"] if deliv_row else 0
    
    conn.close()
    return {
        "gross_sales": gross_sales,
        "total_gst": total_gst,
        "total_sales_count": total_sales_count,
        "payment_breakdown": payment_breakdown,
        "total_meds": total_meds,
        "low_stock_count": low_stock_count,
        "exp_soon_count": exp_soon_count,
        "total_rx": total_rx,
        "pending_rx": pending_rx,
        "approved_rx": approved_rx,
        "active_staff": active_staff,
        "total_deliv": total_deliv,
        "en_route_deliv": en_route_deliv,
        "delivered_deliv": delivered_deliv
    }

def get_active_sessions() -> list:
    """Retrieve all active online staff sessions and terminals."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM active_sessions ORDER BY last_heartbeat DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_session_heartbeat(session_id: str, user_id: str, name: str, role: str, terminal_name: str, status: str = "Online", last_action: str = "Active"):
    """Update or register terminal presence heartbeat in SQLite."""
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cur.execute("""
        INSERT INTO active_sessions (session_id, user_id, name, role, terminal_name, status, last_action, login_time, last_heartbeat)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(session_id) DO UPDATE SET
            status = excluded.status,
            last_action = excluded.last_action,
            last_heartbeat = excluded.last_heartbeat,
            name = excluded.name,
            role = excluded.role
        """, (session_id, user_id, name, role, terminal_name, status, last_action, now, now))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

# --- 14. END-OF-DAY FINANCIAL Z-REPORT & CASH RECONCILIATION ---

def get_daily_z_report_data(target_date: Optional[str] = None) -> Dict[str, Any]:
    """Compile comprehensive End-of-Day Z-Report financial data and cash drawer reconciliation."""
    conn = get_connection()
    cur = conn.cursor()
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    date_query = target_date.strip() if target_date else today_str
    
    if date_query.lower() == "all":
        cur.execute("SELECT * FROM invoices ORDER BY timestamp DESC")
    else:
        cur.execute("SELECT * FROM invoices WHERE timestamp LIKE ? ORDER BY timestamp DESC", (f"{date_query}%",))
        
    rows = cur.fetchall()
    invoices = [dict(r) for r in rows]
    
    total_bills = len(invoices)
    gross_sales = sum(inv.get("total_amount", 0.0) for inv in invoices)
    total_gst = sum(inv.get("gst_amount", 0.0) for inv in invoices)
    net_sales = sum(inv.get("subtotal", 0.0) for inv in invoices)
    cgst = total_gst / 2.0
    sgst = total_gst / 2.0
    
    # Categorize payment types
    cash_bills = [inv for inv in invoices if "cash" in inv.get("payment_method", "").lower()]
    upi_bills = [inv for inv in invoices if "upi" in inv.get("payment_method", "").lower() or "qr" in inv.get("payment_method", "").lower()]
    card_bills = [inv for inv in invoices if "card" in inv.get("payment_method", "").lower()]
    other_bills = [inv for inv in invoices if inv not in cash_bills and inv not in upi_bills and inv not in card_bills]
    
    cash_total = sum(inv.get("total_amount", 0.0) for inv in cash_bills)
    upi_total = sum(inv.get("total_amount", 0.0) for inv in upi_bills)
    card_total = sum(inv.get("total_amount", 0.0) for inv in card_bills)
    other_total = sum(inv.get("total_amount", 0.0) for inv in other_bills)
    
    # Check if this date has already been formally closed
    closed_report = None
    if date_query.lower() != "all":
        cur.execute("SELECT * FROM z_reports WHERE report_date = ? ORDER BY generated_at DESC LIMIT 1", (date_query,))
        z_row = cur.fetchone()
        if z_row:
            closed_report = dict(z_row)
            
    conn.close()
    
    return {
        "report_date": date_query,
        "is_all_dates": (date_query.lower() == "all"),
        "total_bills": total_bills,
        "gross_sales": round(gross_sales, 2),
        "net_sales": round(net_sales, 2),
        "total_gst": round(total_gst, 2),
        "cgst": round(cgst, 2),
        "sgst": round(sgst, 2),
        "payment_breakdown": {
            "Cash": {"count": len(cash_bills), "total": round(cash_total, 2)},
            "UPI": {"count": len(upi_bills), "total": round(upi_total, 2)},
            "Card": {"count": len(card_bills), "total": round(card_total, 2)},
            "Other": {"count": len(other_bills), "total": round(other_total, 2)}
        },
        "cash_total": round(cash_total, 2),
        "upi_total": round(upi_total, 2),
        "card_total": round(card_total, 2),
        "digital_total": round(upi_total + card_total, 2),
        "invoices": invoices,
        "is_closed": bool(closed_report),
        "closed_report": closed_report
    }

def save_closed_z_report(z_data: Dict[str, Any]) -> Dict[str, Any]:
    """Persist an immutable signed End-of-Day Z-Report into the database."""
    conn = get_connection()
    cur = conn.cursor()
    
    z_id = z_data.get("z_report_id") or f"Z-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    report_date = z_data.get("report_date") or datetime.now().strftime("%Y-%m-%d")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    gen_by = z_data.get("generated_by", "Store Admin")
    
    op_float = float(z_data.get("opening_float", 2000.0))
    cash_s = float(z_data.get("cash_sales", 0.0))
    cash_p = float(z_data.get("cash_payouts", 0.0))
    exp_c = float(z_data.get("expected_cash", op_float + cash_s - cash_p))
    act_c = float(z_data.get("actual_cash", exp_c))
    var_c = float(z_data.get("variance", act_c - exp_c))
    
    upi_s = float(z_data.get("upi_sales", 0.0))
    card_s = float(z_data.get("card_sales", 0.0))
    tot_s = float(z_data.get("total_sales", 0.0))
    tot_gst = float(z_data.get("total_gst", 0.0))
    cgst = float(z_data.get("cgst", tot_gst / 2.0))
    sgst = float(z_data.get("sgst", tot_gst / 2.0))
    bills = int(z_data.get("total_bills", 0))
    notes = z_data.get("notes", "Clean End-of-Day Close")
    
    cur.execute("""
    INSERT INTO z_reports (
        z_report_id, report_date, generated_at, generated_by,
        opening_float, cash_sales, cash_payouts, expected_cash,
        actual_cash, variance, upi_sales, card_sales, total_sales,
        total_gst, cgst, sgst, total_bills, status, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'CLOSED & SIGNED', ?)
    ON CONFLICT(z_report_id) DO UPDATE SET
        actual_cash = excluded.actual_cash,
        variance = excluded.variance,
        notes = excluded.notes,
        generated_at = excluded.generated_at
    """, (
        z_id, report_date, now_str, gen_by,
        op_float, cash_s, cash_p, exp_c,
        act_c, var_c, upi_s, card_s, tot_s,
        tot_gst, cgst, sgst, bills, notes
    ))
    conn.commit()
    conn.close()
    
    return {"success": True, "z_report_id": z_id}

def get_all_z_reports(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve historical closed Z-Reports."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM z_reports ORDER BY generated_at DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Initialize database on import
init_db()



# --- SUPPLIER CONSIGNMENT & PAY-ON-SALE FUNCTIONS ---

def _internal_inward_consignment(cur, po_data, auto_increment_stock=True):
    po_id = po_data["po_id"]
    sup_name = po_data["supplier_name"]
    items = po_data.get("items", [])
    rec_date = po_data.get("received_date") or datetime.now().strftime("%Y-%m-%d")
    now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for it in items:
        if isinstance(it, str):
            med_name = it
            qty = 10
            rate = 0.0
        elif isinstance(it, dict):
            med_name = it.get("medicine") or it.get("name")
            qty = int(it.get("qty", 0))
            rate = float(it.get("rate", 0.0))
        else:
            continue
            
        if not med_name or qty <= 0:
            continue
            
        # Avoid duplicate batch entries for same po_id and medicine
        cur.execute("SELECT COUNT(*) as cnt FROM consignment_batches WHERE po_id = ? AND medicine_name = ?", (po_id, med_name))
        if cur.fetchone()["cnt"] > 0:
            continue
            
        cur.execute("SELECT id, name, mrp, cost_price, batch FROM medicines WHERE name = ? OR id = ?", (med_name, med_name))
        med_row = cur.fetchone()
        
        custom_mrp = float(it.get("selling_price") or it.get("mrp") or 0.0) if isinstance(it, dict) else 0.0
        if med_row:
            med_id = med_row["id"]
            mrp = custom_mrp if custom_mrp > 0 else float(med_row["mrp"])
            cp = rate if rate > 0 else float(med_row["cost_price"])
            batch_no = med_row["batch"]
            if auto_increment_stock:
                cur.execute("UPDATE medicines SET stock = stock + ? WHERE id = ?", (qty, med_id))
        else:
            med_id = f"MED-{secrets.token_hex(3).upper()}"
            cp = rate if rate > 0 else 10.0
            mrp = custom_mrp if custom_mrp > 0 else (round(cp * 1.5, 2) if cp > 0 else 100.0)
            batch_no = f"BAT-{datetime.now().strftime('%m%y')}"
            cur.execute("""
            INSERT INTO medicines (id, name, generic, category, schedule, manufacturer, batch, expiry, days_to_expiry, stock, unit, mrp, cost_price, gst_pct, rack, cold_chain, interactions)
            VALUES (?, ?, ?, 'General', 'OTC', ?, ?, ?, 365, ?, 'Strips', ?, ?, 12.0, 'Rack-A1', 0, '[]')
            """, (med_id, med_name, med_name, sup_name, batch_no, (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"), qty, mrp, cp))

        # Insert consignment batch: Inwarded stock on consignment, 0 upfront payment
        cur.execute("""
        INSERT INTO consignment_batches (po_id, supplier_name, medicine_id, medicine_name, batch_no, received_date, received_qty, cost_price, selling_price, units_sold, units_paid, total_paid, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0.0, 'Active', ?)
        """, (po_id, sup_name, med_id, med_name, batch_no, rec_date, qty, cp, mrp, now_ts))


def record_goods_receipt(po_id, received_date=None, auto_add_stock=True):
    """
    Mark an incoming purchase order as delivered/received.
    Increases inventory stock in medicines table and logs a new consignment batch
    with 0 upfront payment (pay-on-sale terms).
    """
    rec_d = received_date or datetime.now().strftime("%Y-%m-%d")
    return update_purchase_order_status(po_id, "Goods Received", rec_d)


def get_supplier_consignment_ledger(supplier_name=None):
    """
    Retrieve full pay-on-sale consignment ledger.
    Calculates:
    - Inwarded stock quantity (delivered from company)
    - Units sold so far at POS
    - Remaining unsold stock on hand (₹0 liability to pharmacy until sold)
    - Payable to company = Units Sold * Cost Price
    - Pharmacy Gross Profit = Units Sold * (Selling Price - Cost Price)
    - Total Paid and Net Balance Due
    """
    conn = get_connection()
    cur = conn.cursor()
    if supplier_name and supplier_name != "ALL":
        cur.execute("SELECT * FROM consignment_batches WHERE supplier_name = ? ORDER BY id DESC", (supplier_name,))
    else:
        cur.execute("SELECT * FROM consignment_batches ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    
    result = []
    for r in rows:
        d = dict(r)
        cost = float(d["cost_price"])
        mrp = float(d["selling_price"])
        sold = int(d["units_sold"])
        received = int(d["received_qty"])
        paid = float(d["total_paid"])
        
        unit_margin = round(mrp - cost, 2)
        unsold_stock = max(0, received - sold)
        accrued_payable = round(sold * cost, 2)            # Total owed to company for sold pieces
        pharmacy_profit = round(sold * unit_margin, 2)       # Total profit earned by pharmacy
        gross_sales_val = round(sold * mrp, 2)              # Total retail sales collected
        balance_due = round(max(0.0, accrued_payable - paid), 2)  # Remaining amount to pay company
        
        d["unit_margin"] = unit_margin
        d["unsold_stock"] = unsold_stock
        d["accrued_payable"] = accrued_payable
        d["pharmacy_profit"] = pharmacy_profit
        d["gross_sales_val"] = gross_sales_val
        d["balance_due"] = balance_due
        result.append(d)
    return result


def get_supplier_consignment_summary():
    """
    Retrieve overall high-level totals across all consignment batches.
    """
    ledger = get_supplier_consignment_ledger()
    total_inward_units = sum(x["received_qty"] for x in ledger)
    total_units_sold = sum(x["units_sold"] for x in ledger)
    total_unsold_units = sum(x["unsold_stock"] for x in ledger)
    total_accrued_payable = round(sum(x["accrued_payable"] for x in ledger), 2)
    total_profit_earned = round(sum(x["pharmacy_profit"] for x in ledger), 2)
    total_gross_sales = round(sum(x["gross_sales_val"] for x in ledger), 2)
    total_paid = round(sum(x["total_paid"] for x in ledger), 2)
    total_balance_due = round(sum(x["balance_due"] for x in ledger), 2)
    
    return {
        "total_inward_units": total_inward_units,
        "total_units_sold": total_units_sold,
        "total_unsold_units": total_unsold_units,
        "total_accrued_payable": total_accrued_payable,
        "total_profit_earned": total_profit_earned,
        "total_gross_sales": total_gross_sales,
        "total_paid": total_paid,
        "total_balance_due": total_balance_due,
        "total_batches_count": len(ledger)
    }


def settle_supplier_payment(payout_data):
    """
    Record payment to supplier/dealer for sold stock.
    payout_data: {
        'supplier_name': str,
        'batch_id': Optional[int],
        'po_id': Optional[str],
        'medicine_name': Optional[str],
        'units_settled': int,
        'amount_paid': float,
        'payment_mode': str,  # 'UPI', 'NEFT Bank Transfer', 'Cheque', 'Cash'
        'reference_no': str,
        'notes': str,
        'paid_by': str
    }
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        payout_id = f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        supplier_name = payout_data["supplier_name"]
        amount_paid = float(payout_data["amount_paid"])
        units_settled = int(payout_data.get("units_settled", 0))
        batch_id = payout_data.get("batch_id")
        
        cur.execute("""
        INSERT INTO supplier_payouts (payout_id, timestamp, supplier_name, po_id, medicine_name, units_settled, rate, amount_paid, payment_mode, reference_no, notes, paid_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            payout_id, ts, supplier_name,
            payout_data.get("po_id", ""),
            payout_data.get("medicine_name", ""),
            units_settled,
            float(payout_data.get("rate", 0.0)),
            amount_paid,
            payout_data.get("payment_mode", "NEFT Bank Transfer"),
            payout_data.get("reference_no", ""),
            payout_data.get("notes", ""),
            payout_data.get("paid_by", "Admin")
        ))
        
        # Update consignment batch if specified, or distribute across supplier batches
        if batch_id:
            cur.execute("""
            UPDATE consignment_batches 
            SET total_paid = total_paid + ?,
                units_paid = units_paid + ?,
                status = CASE WHEN (units_paid + ?) >= units_sold AND units_sold >= received_qty THEN 'Settled' ELSE status END
            WHERE id = ?
            """, (amount_paid, units_settled, units_settled, batch_id))
        else:
            # Distribute payment to active batches for this supplier
            cur.execute("""
            SELECT id, (units_sold * cost_price - total_paid) as due
            FROM consignment_batches
            WHERE supplier_name = ? AND (units_sold * cost_price) > total_paid
            ORDER BY id ASC
            """, (supplier_name,))
            unpaid_batches = cur.fetchall()
            rem = amount_paid
            for ub in unpaid_batches:
                if rem <= 0:
                    break
                due_val = max(0.0, float(ub["due"]))
                pay_val = min(rem, due_val)
                cur.execute("UPDATE consignment_batches SET total_paid = total_paid + ? WHERE id = ?", (pay_val, ub["id"]))
                rem -= pay_val
                
        conn.commit()
        success, err = True, None
    except Exception as e:
        success, err = False, str(e)
    finally:
        conn.close()
    return success, err or payout_id


def get_supplier_payouts(supplier_name=None, limit=100):
    """
    Retrieve historical settlement payouts made to suppliers.
    """
    conn = get_connection()
    cur = conn.cursor()
    if supplier_name and supplier_name != "ALL":
        cur.execute("SELECT * FROM supplier_payouts WHERE supplier_name = ? ORDER BY timestamp DESC LIMIT ?", (supplier_name, limit))
    else:
        cur.execute("SELECT * FROM supplier_payouts ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
