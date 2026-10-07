"""
Centralized SQLite Database & Data Layer for Pharmacy Management System.
Stores persistent data for staff users, credentials, roles, active presence sessions,
audit logs, medicines catalog, prescriptions, sales invoices, and delivery orders.
"""

import sqlite3
import os
import json
from datetime import datetime

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
    
    # 1. Staff & Users Table (with Username, Password, Role, Status)
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
    
    # Check if password column exists in older schemas and add if missing
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
    
    # Seed initial default data
    seed_initial_data(cursor)
    
    conn.commit()
    conn.close()

def seed_initial_data(cursor):
    # Check if staff exists
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
    else:
        # Ensure default passwords exist for sample users
        defaults = [
            ("admin", "admin123", "Admin"),
            ("pharmacist", "pharma123", "Pharmacist"),
            ("cashier", "cash123", "Cashier"),
            ("inventory", "inv123", "Inventory Manager"),
            ("delivery", "deliv123", "Delivery Agent")
        ]
        for uname, pwd, role in defaults:
            cursor.execute("SELECT id FROM staff WHERE username = ?", (uname,))
            if not cursor.fetchone():
                new_id = f"STF-{uname[:3].upper()}"
                cursor.execute("""
                INSERT OR IGNORE INTO staff (id, name, role, username, password, email, phone, branch, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (new_id, f"Demo {role}", role, uname, pwd, f"{uname}@aegispharm.com", "+91 98201 00000", "Apex Central - Branch #01", "Active"))
            else:
                cursor.execute("UPDATE staff SET password = ? WHERE username = ?", (pwd, uname))

    # Check if medicines exist
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

    # Check if prescriptions exist
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

    # Check if delivery orders exist
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

    # Add initial audit log
    cursor.execute("SELECT COUNT(*) as count FROM audit_logs")
    if cursor.fetchone()["count"] == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO audit_logs (timestamp, user_name, role, action, details, level) VALUES (?, ?, ?, ?, ?, ?)",
                       (now, "System", "System", "System Initialized", "Database tables & default credentials verified.", "INFO"))

# --- USER AUTHENTICATION & STAFF CRUD FUNCTIONS ---

def authenticate_user(username, password):
    """Check credentials and return user dict if valid and active."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM staff WHERE (username = ? OR id = ?) AND status = 'Active'", (username.strip(), username.strip()))
    user = cur.fetchone()
    conn.close()
    
    if user and user["password"] == password.strip():
        return dict(user)
    return None

def get_all_staff():
    """Retrieve all staff members for the Admin Dashboard."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, role, username, password, email, phone, branch, status FROM staff ORDER BY role ASC, name ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_staff_user(staff_id, name, role, username, password, email, phone, branch):
    """Create a new staff user account (by Admin)."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO staff (id, name, role, username, password, email, phone, branch, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Active')
        """, (staff_id.strip(), name.strip(), role.strip(), username.strip(), password.strip(), email.strip(), phone.strip(), branch.strip()))
        conn.commit()
        success = True
        err = None
    except sqlite3.IntegrityError as e:
        success = False
        err = f"Username or User ID already exists ({e})"
    except Exception as e:
        success = False
        err = str(e)
    finally:
        conn.close()
    return success, err

def update_staff_user(staff_id, name, role, username, password, email, phone, branch, status="Active"):
    """Update an existing staff user's credentials, role, or status."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        UPDATE staff 
        SET name = ?, role = ?, username = ?, password = ?, email = ?, phone = ?, branch = ?, status = ?
        WHERE id = ?
        """, (name.strip(), role.strip(), username.strip(), password.strip(), email.strip(), phone.strip(), branch.strip(), status.strip(), staff_id.strip()))
        conn.commit()
        success = True
        err = None
    except Exception as e:
        success = False
        err = str(e)
    finally:
        conn.close()
    return success, err

def delete_staff_user(staff_id):
    """Delete a staff user account."""
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

# Initialize database on import
init_db()
