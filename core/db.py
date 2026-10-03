"""
Centralized SQLite Database & Data Layer for Pharmacy Management System.
Stores persistent data for medicines, batches, prescriptions, orders, staff, audit logs, and presence.
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
    
    # 1. Staff & Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT,
        phone TEXT,
        branch TEXT DEFAULT 'Apex Central - Branch #01'
    );
    """)
    
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
    
    # Seed initial data if tables are empty
    seed_initial_data(cursor)
    
    conn.commit()
    conn.close()

def seed_initial_data(cursor):
    # Check if staff exists
    cursor.execute("SELECT COUNT(*) as count FROM staff")
    if cursor.fetchone()["count"] == 0:
        sample_staff = [
            ("STF-01", "Dr. Rajesh Kulkarni", "Admin", "admin.rajesh", "admin@aegispharm.com", "+91 98201 00001", "Apex Central - Branch #01"),
            ("STF-02", "Pooja Sharma, R.Ph", "Pharmacist", "pharm.pooja", "pooja.pharma@aegispharm.com", "+91 98201 00002", "Apex Central - Branch #01"),
            ("STF-03", "Amit Deshmukh", "Cashier", "pos.amit", "amit.pos@aegispharm.com", "+91 98201 00003", "Apex Central - Branch #01"),
            ("STF-04", "Vikram Rathore", "Inventory Manager", "inv.vikram", "vikram.inv@aegispharm.com", "+91 98201 00004", "Apex Central - Branch #01"),
            ("STF-05", "Ramesh Kumar", "Delivery Agent", "deliv.ramesh", "ramesh.logistics@aegispharm.com", "+91 98201 00005", "Apex Central - Branch #01"),
        ]
        cursor.executemany("INSERT INTO staff VALUES (?, ?, ?, ?, ?, ?, ?)", sample_staff)

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

    # Add initial audit logs
    cursor.execute("SELECT COUNT(*) as count FROM audit_logs")
    if cursor.fetchone()["count"] == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO audit_logs (timestamp, user_name, role, action, details, level) VALUES (?, ?, ?, ?, ?, ?)",
                       (now, "System", "System", "Gateway Initialized", "Database tables verified and baseline synced.", "INFO"))

# Initialize on import
init_db()
