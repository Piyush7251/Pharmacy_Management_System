"""
Centralized SQLite Database & Data Layer for Pharmacy Management System.
Stores persistent data for staff users, credentials, roles, active presence sessions,
audit logs, medicines catalog, prescriptions, sales invoices, delivery orders,
patients, suppliers, purchase orders, narcotic NDPS register, and cold chain logs.
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta

DATA_DIR = os.path.expanduser("~/.aegispharm")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "pharmacy_system.db")

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
    
    # Seed initial default data
    seed_initial_data(cursor)
    
    conn.commit()
    conn.close()

def seed_initial_data(cursor):
    # 1. Staff default users
    cursor.execute("SELECT COUNT(*) as count FROM staff")
    if cursor.fetchone()["count"] == 0:
        sample_staff = [
            ("STF-01", "Dr. Rajesh Kulkarni", "Admin", "admin", "admin123", "admin@aegispharm.com", "+91 98201 00001", "Apex Central - Branch #01", "Active"),
            ("STF-02", "Pooja Sharma, R.Ph", "Pharmacist", "pharmacist", "pharma123", "pooja.pharma@aegispharm.com", "+91 98201 00002", "Apex Central - Branch #01", "Active"),
            ("STF-03", "Amit Deshmukh", "Cashier", "cashier", "cash123", "amit.pos@aegispharm.com", "+91 98201 00003", "Apex Central - Branch #01", "Active"),
            ("STF-04", "Vikram Rathore", "Inventory Manager", "inventory", "inv123", "vikram.inv@aegispharm.com", "+91 98201 00004", "Apex Central - Branch #01", "Active"),
            ("STF-05", "Ramesh Kumar", "Delivery Agent", "delivery", "deliv123", "ramesh.logistics@aegispharm.com", "+91 98201 00005", "Apex Central - Branch #01", "Active"),
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
        d["items"] = json.loads(d.get("items", "[]"))
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
        d["items"] = json.loads(d.get("items_json", "[]"))
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
        d["items"] = json.loads(d.get("items_json", "[]"))
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

# Initialize database on import
init_db()
