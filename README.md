# 💊 TQM Pharm Enterprise — Pharmacy Management System

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![UI-CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-brightgreen.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Backend-FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Database-SQLite](https://img.shields.io/badge/Database-SQLite-07405e.svg)](https://www.sqlite.org/)
[![License-MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, high-performance desktop pharmacy operating system engineered for retail pharmacy chains, hospital dispensaries, and clinical networks. 

Features a **clean White/Light theme by default** with a **1-click instant Dark Mode toggle**, zero-lag non-blocking asynchronous architecture, real-time staff presence heartbeats, and comprehensive enterprise functionality across **all 5 operational roles**.

---

## 🎨 Clean Dual Theming (Default: White / Light Mode)

TQM Pharm features an intuitive, modern clinical UI:
- **Default Appearance**: **White / Light Mode** with clean slate borders, crisp typography, and high-readability clinical status badges.
- **Dynamic Theme Switcher**: Instant toggle button (`🌙 Dark Mode` / `☀️ Light Mode`) in both the login screen and the global top navigation bar across all dashboards.
- **Zero-Lag Architecture**: Database operations and presence telemetry run on asynchronous background threads, ensuring the UI never stutters or freezes.

---

## 🔐 Workstation Login Dashboard Portal & Default Credentials

The application boots directly to a high-performance **Workstation Login Dashboard Portal**:
- **Interactive Station Persona Grid**: Visual station tiles (👑 Store Admin, 🩺 Clinical Pharmacist, 💳 Cashier POS, 📦 Inventory Manager, 🛵 Delivery Rider) that instantly pre-fill credentials and display workstation responsibilities.
- **Terminal Location Selector**: Assign sessions to physical terminals (Front Counter A, Clinical Kiosk B, Inwarding Bay, Store Admin HQ, Delivery Bay).
- **Security & Telemetry Header**: Displays real-time database connection status, live digital clock, instant Light/Dark mode switcher, and Station Guide modal.
- **Show/Hide Password & 1-Click Fast Login**: Seamless developer/user testing with 1-click login and 256-bit AES encrypted local sessions.

| Role | Username | Password | Assigned Dashboard & Responsibilities |
| :--- | :--- | :--- | :--- |
| **👑 Store Admin** | `admin` | `admin123` | **Admin Command Center**: Create/manage user IDs & passwords, assign roles, monitor live online staff/terminals, view daily Z-Report cash reconciliation & live audit stream. |
| **🩺 Pharmacist** | `pharmacist` | `pharma123` | **Clinical & Dispensing Station**: e-Prescription intake queue, CDSS drug interaction & patient allergy contraindication engine, Schedule X NDPS double sign-off, refill adherence, allergy EHR. |
| **💳 Cashier** | `cashier` | `cash123` | **POS & Express Billing Terminal**: 1-click import of approved prescriptions, barcode search, FEFO batch selection, split payments (Cash / Dynamic UPI QR / Card), GST invoice generator & thermal receipt printing. |
| **📦 Inventory Manager** | `inventory` | `inv123` | **Supply Chain & Inventory Hub**: Multi-batch FEFO stock ledger, low stock/expiry alerts, Goods Receipt Notes (GRN) inwarding, Cold-Chain IoT (2–8°C) telemetry & alarms, supplier directory. |
| **🚚 Delivery Agent** | `delivery` | `deliv123` | **Delivery & Logistics App**: Active dispatch Kanban board, cold-bag packaging checks, manual route dispatch, and customer 4-digit OTP digital proof-of-delivery (e-POD). |

---

## 🏗️ System Architecture & Dynamic Dashboard Routing

```mermaid
graph TD
    Login["🔐 Unified Login Screen (app.py / main.py)<br/>Default Light/White Theme • Instant Theme Toggle"]
    
    Login -->|Role: Admin| AD["👑 Admin Command Center<br/>• Staff RBAC Management (Add/Edit Users)<br/>• Live Presence & Heartbeats<br/>• Daily Z-Report Cash/UPI Financials<br/>• Dead Stock Risk Analysis<br/>• System Security Audit Trail"]
    Login -->|Role: Pharmacist| PD["🩺 Pharmacist Clinical Dashboard<br/>• eRx Queue & CDSS Safety Engine<br/>• Patient Allergy Contraindications<br/>• Schedule X / NDPS Narcotic Sign-Off<br/>• Chronic Patient Refill Adherence<br/>• Patient EHR Allergy Profiles"]
    Login -->|Role: Cashier| CD["💳 Cashier POS & Express Billing<br/>• 1-Click Approved eRx Import<br/>• Barcode Scanner & FEFO Selection<br/>• Dynamic UPI QR & Cash Change Calculator<br/>• GST Tax Thermal Receipt Generator<br/>• Delivery Routing Dispatch"]
    Login -->|Role: Inventory Manager| ID["📦 Supply Chain & Inventory Hub<br/>• FEFO Batch Ledger with Expiry Badges<br/>• Add Medicine & Stock Adjustment Modals<br/>• Cold-Chain IoT Sensor Monitor (2-8°C)<br/>• Goods Receipt Notes (GRN) Inwarding<br/>• Supplier & Vendor Directory"]
    Login -->|Role: Delivery Agent| DD["🚚 Delivery & Fulfilment Dashboard<br/>• Active Route Kanban Board<br/>• Customer 4-Digit OTP e-POD Verification<br/>• Manual Delivery Dispatch Creator<br/>• Cold-Bag Packaging Checklist"]
    
    AD -->|Sign Out| Login
    PD -->|Sign Out| Login
    CD -->|Sign Out| Login
    ID -->|Sign Out| Login
    DD -->|Sign Out| Login
```

---

## 🗄️ Database Architecture & Entity-Relationship (ER) Diagram

TQM Pharm Enterprise is architected upon a normalized **Third Normal Form (3NF)** relational database engine implemented in SQLite 3 with **Write-Ahead Logging (WAL)** for high-throughput non-blocking multi-threaded concurrency, strict foreign key constraints, and multi-table ACID transactions.

> 📖 **Complete Data Dictionary**: See [docs/DATABASE_ERD.md](docs/DATABASE_ERD.md) for field-by-field definitions, constraints, indexes, and concurrency specifications.

### 📐 Visual Relational ER Diagram

![TQM Pharm Relational ER Diagram](assets/er_diagram.svg)

*(Scalable vector SVG with live schema badges. A high-definition 300 DPI raster preview is also available at [`assets/er_diagram.png`](assets/er_diagram.png))*

### 📊 Interactive Mermaid Entity-Relationship Diagram

GitHub natively renders the interactive diagram below:

```mermaid
erDiagram
    %% CLUSTER 1: IDENTITY, SESSION & AUDIT GOVERNANCE
    STAFF ||--o{ ACTIVE_SESSIONS : "maintains"
    STAFF ||--o{ AUDIT_LOGS : "records"
    STAFF ||--o{ PRESCRIPTIONS : "verifies"
    STAFF ||--o{ INVOICES : "bills"
    STAFF ||--o{ DELIVERY_ORDERS : "dispatches"
    STAFF ||--o{ PURCHASE_ORDERS : "authorizes"
    STAFF ||--o{ NARCOTIC_REGISTER : "countersigns"
    STAFF ||--o{ Z_REPORTS : "closes_till"

    %% CLUSTER 2: CLINICAL EHR & CONTROLLED DRUGS
    PATIENTS ||--o{ PRESCRIPTIONS : "presents"
    PATIENTS ||--o{ INVOICES : "billed_to"
    PATIENTS ||--o{ DELIVERY_ORDERS : "receives"
    PATIENTS ||--o{ REFILL_SCHEDULES : "enrolled_in"

    PRESCRIPTIONS ||--o{ NARCOTIC_REGISTER : "mandates_audit"
    MEDICINES ||--o{ NARCOTIC_REGISTER : "controlled_stock"
    MEDICINES ||--o{ REFILL_SCHEDULES : "refill_item"

    %% CLUSTER 3: PHARMACEUTICALS, IOT & SUPPLY CHAIN
    SUPPLIERS ||--o{ PURCHASE_ORDERS : "fulfills"
    SUPPLIERS ||--o{ CONSIGNMENT_BATCHES : "inwards"
    CONSIGNMENT_BATCHES ||--o{ SUPPLIER_PAYOUTS : "settles"
    MEDICINES ||--o{ TEMPERATURE_LOGS : "monitored_by_iot"
    MEDICINES ||--o{ CONSIGNMENT_BATCHES : "consigned_stock"
    PURCHASE_ORDERS }o--o{ MEDICINES : "restocks"

    %% CLUSTER 4: POS BILLING & FINANCIAL RECONCILIATION
    INVOICES ||--o{ Z_REPORTS : "settles_into"
    INVOICES ||--o{ DELIVERY_ORDERS : "routes_fulfillment"

    STAFF {
        string id PK "Staff ID (e.g. STF-01)"
        string name "Full Name"
        string role "Admin, Pharmacist, Cashier, Inventory, Delivery"
        string username UK "Unique system handle"
        string password "Salted password"
        string email "Official staff email"
        string phone "Contact number"
        string branch "Assigned branch store"
        string status "Active or Suspended"
    }

    ACTIVE_SESSIONS {
        string session_id PK "UUID session token"
        string user_id FK "References staff(id)"
        string name "Operator Name"
        string role "Active persona role"
        string terminal_name "Assigned workstation"
        string ip_address "Client IP address"
        string status "Online or Away"
        string last_action "Last action performed"
        datetime login_time "Session initiation"
        datetime last_heartbeat "Live telemetry ping"
    }

    AUDIT_LOGS {
        int id PK "Autoincrement ID"
        datetime timestamp "Event timestamp"
        string user_name "Operator username"
        string role "Operator role"
        string action "Event classification"
        string details "Context and payload"
        string level "INFO, WARN, CRITICAL"
    }

    PATIENTS {
        string id PK "Patient ID (e.g. PAT-001)"
        string name "Patient full name"
        int age "Age in years"
        string gender "Gender identifier"
        string phone "Primary contact phone"
        json allergies "List of known drug allergies"
        json chronic_conditions "Hypertension, Diabetes, etc."
        int loyalty_points "Store reward credits"
        string recent_doctor "Last consulting physician"
    }

    MEDICINES {
        string id PK "Medicine SKU (e.g. MED-001)"
        string name "Brand trade name"
        string generic "Active pharmaceutical ingredient"
        string category "Antibiotic, Analgesic, etc."
        string schedule "OTC, Schedule H, H1, or X"
        string manufacturer "Pharma manufacturer"
        string batch "Batch / Lot identifier"
        date expiry "Expiration date (YYYY-MM-DD)"
        int days_to_expiry "Calculated shelf life remaining"
        int stock "Current sellable inventory count"
        string unit "Strips, Bottles, Vials"
        float mrp "Maximum retail price"
        float cost_price "Purchase procurement cost"
        float gst_pct "Applicable GST rate (e.g. 12%)"
        string rack "Warehouse physical rack location"
        int cold_chain "1 if 2-8 deg C storage required"
        json interactions "Interacting drug molecules list"
    }

    PRESCRIPTIONS {
        string rx_id PK "Prescription ID (e.g. RX-2026-001)"
        string patient_name "Patient name"
        string patient_id FK "References patients(id)"
        string doctor_name "Prescribing doctor"
        string hospital "Originating clinic or hospital"
        date date "Prescription issue date"
        string status "Pending, Verified, Dispensed, Rejected"
        json items "Prescribed drugs, dosage, duration"
        string notes "Clinical pharmacist notes"
        string verified_by FK "References staff(name)"
        datetime verified_at "Timestamp of pharmacist sign-off"
    }

    INVOICES {
        string invoice_id PK "Tax Invoice ID (e.g. INV-2026-1001)"
        datetime timestamp "Billing transaction timestamp"
        string patient_name "Customer or patient name"
        string cashier_name FK "References staff(name)"
        string payment_method "Cash, Dynamic UPI QR, Card"
        float subtotal "Pre-tax merchandise subtotal"
        float gst_amount "Calculated CGST + SGST total"
        float total_amount "Final payable invoice total"
        json items_json "Itemized sold items with batch and tax"
    }

    DELIVERY_ORDERS {
        string order_id PK "Shipment ID (e.g. DEL-501)"
        string patient_name "Recipient patient name"
        string address "Delivery physical address"
        string phone "Recipient phone number"
        string agent_name FK "References staff(name)"
        string status "Packaging, Out for Delivery, Delivered"
        string time_slot "Delivery window"
        int items_count "Total packages in shipment"
        int cold_chain_pack "1 if insulated thermal icepack required"
        float amount "Cash on Delivery or prepaid amount"
        string payment_status "Paid or Collect On Delivery"
        string otp "4-digit electronic POD verification PIN"
    }

    NARCOTIC_REGISTER {
        int id PK "Autoincrement entry ID"
        datetime timestamp "Sign-off timestamp"
        string rx_id FK "References prescriptions(rx_id)"
        string patient_name "Patient name"
        string patient_phone "Contact number"
        string doctor_name "Prescribing doctor"
        string doctor_reg_no "Doctor state medical council reg number"
        string medicine_name FK "References medicines(name)"
        string batch_no "Controlled batch number"
        int quantity "Dispensed unit quantity"
        string pharmacist_name FK "Dispensing licensed pharmacist"
        string pharmacist_reg_no "Pharmacist statutory license reg number"
        int auth_pin_verified "1 if PIN authenticated"
    }

    SUPPLIERS {
        string id PK "Supplier ID (e.g. SUP-01)"
        string name "Distributor / vendor business name"
        string contact_person "Representative name"
        string phone "Vendor hotline"
        string email "Purchase order email"
        string gstin "15-digit GST identification number"
        string address "Warehouse logistics address"
        string payment_terms "e.g. 30 Days Net, Immediate UPI"
    }

    PURCHASE_ORDERS {
        string po_id PK "Purchase Order ID (e.g. PO-2026-881)"
        date date "Purchase order issue date"
        string supplier_name FK "References suppliers(name)"
        string status "Pending Delivery or Goods Received"
        json items_json "Procurement line items and rates"
        float total_amount "Total invoice payable amount"
        date received_date "Warehouse receipt date (GRN)"
        string created_by FK "References staff(name)"
    }

    TEMPERATURE_LOGS {
        int id PK "Autoincrement reading ID"
        datetime timestamp "Reading timestamp"
        string sensor_id "IoT probe identifier"
        float temperature "Temperature in deg Celsius"
        string status "Optimal 2-8 deg C or Critical Alert"
        int alert_triggered "1 if excursion alarm fired"
    }

    REFILL_SCHEDULES {
        string id PK "Refill ID (e.g. RF-101)"
        string patient_name "Patient name"
        string patient_phone "Contact phone"
        string medicine_name FK "References medicines(name)"
        date last_dispensed "Date of last fulfillment"
        date next_due_date "Calculated next cycle due date"
        string status "Scheduled, Due Soon, Overdue"
    }

    Z_REPORTS {
        string z_report_id PK "Closure ID (e.g. ZREP-2026-10-20)"
        date report_date "Financial trading date"
        datetime generated_at "Till closure timestamp"
        string generated_by FK "References staff(name)"
        float opening_float "Starting cash drawer float"
        float cash_sales "Total cash tender collected"
        float cash_payouts "Petty expense payouts"
        float expected_cash "opening_float + cash_sales - cash_payouts"
        float actual_cash "Physical drawer cash counted"
        float variance "Discrepancy (Over / Short / Balanced)"
        float upi_sales "Settled dynamic UPI volume"
        float card_sales "Settled POS card terminal volume"
        float total_sales "Gross revenue across all tenders"
        float total_gst "Combined statutory tax collected"
        float cgst "Central GST component"
        float sgst "State GST component"
        int total_bills "Total tax invoices processed"
        string status "CLOSED & SIGNED or AUDIT REVIEW"
        string notes "Cashier shift remarks"
    }

    CONSIGNMENT_BATCHES {
        int id PK "Autoincrement consignment ID"
        string po_id FK "References purchase_orders(po_id)"
        string supplier_name FK "References suppliers(name)"
        string medicine_name FK "References medicines(name)"
        string batch_no "Supplier batch identifier"
        int received_qty "Delivered consignment quantity"
        float cost_price "Procurement rate owed upon sale"
        float selling_price "Retail MRP at counter"
        int units_sold "Quantity sold to patients"
        float accrued_payable "units_sold * cost_price"
        float total_paid "Total payouts settled to supplier"
        datetime created_at "Goods receipt timestamp"
    }

    SUPPLIER_PAYOUTS {
        int id PK "Autoincrement payout ID"
        int consignment_id FK "References consignment_batches(id)"
        string supplier_name FK "References suppliers(name)"
        float amount_paid "Settled payout amount"
        string payment_method "Bank Transfer, UPI, Cheque, Cash"
        string reference_no "Transaction UTR or Cheque number"
        string notes "Settlement remarks"
        string settled_by FK "References staff(name)"
        datetime settled_at "Settlement timestamp"
    }
```

### 📋 16-Table Relational Schema Architecture

| Domain Cluster | Table Name | Primary Key | Key Relationships & Foreign Keys | Role / Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **🛡️ Identity & Access** | `staff` | `id` | Root Identity entity (1:N to Sessions, Audits, POS) | User accounts, credentials, RBAC roles, branches |
| **🛡️ Identity & Access** | `active_sessions` | `session_id` | `user_id -> staff.id` | Live operator heartbeat and terminal telemetry |
| **🛡️ Identity & Access** | `audit_logs` | `id` | `user_name -> staff.name` | Tamper-evident operational event stream |
| **🩺 Clinical & EHR** | `patients` | `id` | 1:N to Prescriptions, Invoices, Refills | Patient demographics, drug allergies, chronic EHR |
| **🩺 Clinical & EHR** | `prescriptions` | `rx_id` | `patient_id -> patients.id`, `verified_by -> staff.name` | Clinical orders, CDSS validation, review queue |
| **🩺 Clinical & EHR** | `narcotic_register` | `id` | `rx_id -> prescriptions.rx_id`, `pharmacist -> staff.name` | Mandatory NDPS Schedule X double-sign register |
| **🩺 Clinical & EHR** | `refill_schedules` | `id` | `medicine_name -> medicines.name` | Chronic medication cycle refill tracking |
| **💊 Catalog & Supply** | `medicines` | `id` | 1:N to Register, Refills, IoT sensors | Formulations, FEFO batches, pricing, rack coordinates |
| **💊 Catalog & Supply** | `temperature_logs` | `id` | Monitored biologicals (`cold_chain = 1`) | IoT refrigerator 2–8°C telemetry and alarm log |
| **💊 Catalog & Supply** | `suppliers` | `id` | 1:N to Purchase Orders | Vendor master directory, GSTINs, commercial terms |
| **💊 Catalog & Supply** | `purchase_orders` | `po_id` | `supplier_name -> suppliers.name` | Procurement orders, stock inwarding (GRN) |
| **💳 Sales & POS** | `invoices` | `invoice_id` | `cashier_name -> staff.name` | Retail GST bills, multi-tender transactions |
| **💳 Sales & POS** | `delivery_orders` | `order_id` | `agent_name -> staff.name` | Dispatch routing, Kanban stages, 4-digit OTP e-POD |
| **💳 Sales & POS** | `z_reports` | `z_report_id` | `generated_by -> staff.name` | Shift cash drawer reconciliation and till closure |
| **📦 Consignment & Pay-on-Sale** | `consignment_batches` | `id` | `supplier_name -> suppliers.name`, `po_id -> purchase_orders.po_id` | Pay-on-sale consignment inventory, cost rate, sold count, accrued liability |
| **📦 Consignment & Pay-on-Sale** | `supplier_payouts` | `id` | `consignment_id -> consignment_batches.id`, `settled_by -> staff.name` | Supplier disbursement vouchers, payment references (UTR/Cheque), settlement history |


---

## 🌟 Comprehensive Features by Module

### 1. 🩺 Pharmacist Clinical Station
- **e-Prescription Intake Queue**: Review incoming doctor prescriptions, patient details, and medication dosages.
- **CDSS Safety Engine**: Real-time automated cross-checks against patient allergy records (e.g., Penicillin flags) and drug-drug interactions.
- **Schedule X / NDPS Narcotic Register**: Mandatory double-sign compliance modal with Pharmacist PIN authentication and Doctor DMC registration number logging, plus CSV export for regulatory drug inspectors.
- **Chronic Patient Refill Adherence**: Track patient refill schedules, overdue flags, and 1-click WhatsApp/SMS refill reminder simulations.
- **Patient EHR Profiles**: Comprehensive allergy records, chronic conditions, and patient registration intake modal.

### 2. 💳 Cashier POS & Billing Terminal
- **1-Click eRx Import**: Instantly pull approved prescriptions from the pharmacist queue into the POS cart without manual re-entry.
- **FEFO Batch Auto-Selection**: First-Expiry, First-Out batch picking guarantees dispensing nearest-expiry batches first.
- **Multi-Tender Payments**:
  - **Cash**: Automated cash tendered and change return calculation.
  - **Dynamic UPI QR**: Interactive modal with dynamic UPI payment string and simulation timer.
  - **Card**: Credit/Debit terminal authorization simulation.
- **GST Tax Invoice & Thermal Receipt**: Instant 80mm thermal receipt generator modal with print and export capabilities.
- **Home Delivery Dispatch Routing**: Checkbox to route orders directly to the Delivery Fleet dispatch board upon checkout.
- **End-of-Day Till Close (Z-Report)**: Quick-action button directly accessible from the POS counter for cashier cash counting and shift reconciliation.

### 3. 📦 Inventory & Supply Chain Hub
- **Multi-Batch FEFO Ledger**: Real-time batch inventory tracking with color-coded expiry badges (`Expired`, `Critical < 30d`, `Attention < 90d`, `Good`) and stock adjustments.
- **Add Medicine Modal**: SKU, generic name, category, Schedule classification (H1/X/OTC), manufacturer, rack location, and cold-chain flags.
- **Goods Receipt Notes (GRN)**: Inward supplier shipments with PO number, supplier selection, received quantity, batch number, expiry date, and unit cost.
- **Cold-Chain IoT Monitor**: Live circular temperature gauge, 24-hour telemetry log stream, and simulated temperature spike alarms (`ALERT: Exceeded 8.0°C`).
- **Suppliers Directory**: Manage distributors, contact persons, phone numbers, and payment terms.
- **Pharmaceutical Consignment & Pay-on-Sale Ledger**: Zero-upfront procurement workflow. When stock arrives, it enters sellable inventory immediately while supplier payable remains ₹0 until dispensing. When items sell at POS, the system automatically calculates supplier payables (`units_sold * cost_price`) and pharmacy gross margin (`units_sold * (selling_price - cost_price)`).
- **Supplier Settlement Payouts**: Real-time batch-level or supplier-level payout settlements (Cash, Bank Transfer, Cheque, UPI) with balance tracking, payment reference logging, and complete settlement audit trail.

### 4. 🚚 Delivery Fleet & Logistics
- **Active Route Board**: Kanban columns for `Packaging`, `Out for Delivery`, and `Delivered`.
- **Electronic Proof of Delivery (e-POD)**: 4-digit customer OTP verification modal ensuring secure handoff of medicines.
- **Manual Task Dispatch**: Create ad-hoc delivery tasks with customer address, phone number, and special delivery notes.
- **Cold-Bag Telemetry**: Tagging cold-chain packages to ensure thermal transport compliance.

### 5. 👑 Enterprise Admin Command Center
- **Staff User Management & RBAC**: Create new staff accounts, assign roles, edit passwords, or toggle account status (`Active` / `Suspended`).
- **Live Online Presence**: Non-blocking heartbeat monitor tracking currently active terminals, login timestamps, and active user tasks.
- **Daily Financial Z-Report & Cash Drawer Reconciliation**: Complete register closing workflow with opening cash float, total cash sales, petty payouts, expected drawer cash, physical cash counted, and live variance detection (Shortage/Overage/Balanced). Includes tender settlement table (Cash, UPI QR, Cards), shift sales audit stream, printable official thermal/A4 Z-slip with signature blocks, and CSV export.
- **Dead Stock & Movement Analytics**: Fast-moving inventory analysis vs stagnant capital risks.
- **System Audit Trail**: Complete immutable event stream recording every prescription approval, POS transaction, stock adjustment, and user authentication.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher.

### 2. Clone Repository & Install Dependencies
```bash
git clone https://github.com/Piyush7251/Pharmacy_Management_System.git
cd Pharmacy_Management_System

# Install dependencies
pip install customtkinter pillow requests
```

---

## 🖥️ Running the Application

### Option A: Next-Gen Hardware-Accelerated Desktop UI (Recommended)
Launches the silky-smooth, zero-lag Edge Chromium WebView2 desktop app with modern aesthetics, animations, and instant role switching:
```bash
python main.py
# or
python desktop_app.py
```

### Option B: Legacy CustomTkinter Mode
If you prefer the original Tkinter canvas interface:
```bash
python main.py --legacy
# or
python app.py
```

### Option C: Dedicated Standalone Terminals
Each station can also be launched directly as a standalone kiosk:
```bash
# Pharmacist Station
python apps/pharmacist_app.py

# Cashier POS Billing Terminal
python apps/cashier_app.py

# Inventory & Supply Chain Hub
python apps/inventory_app.py

# Delivery Logistics Fleet
python apps/delivery_app.py

# Admin Command Center
python apps/admin_app.py
```

### Option D: Automated Full-Feature Test Suite
Run the comprehensive 25-point automated integration test suite covering all security, clinical, pos, inventory, config, logging, UI rendering, and desktop bridge functions:
```bash
python tests/test_all_features.py
```

---

## ⚙️ Configuration & System Settings

TQM Pharm includes a centralized configuration subsystem with file-based persistence:
- **`config.json`**: Active JSON configuration file controlling store profile, licensing, inventory alert thresholds, receipt templates, and paths.
- **`config.example.json`**: Template configuration file for onboarding new store locations or branches.
- **`config/settings.py`**: Thread-safe `SettingsManager` with strongly typed data classes (`StoreConfig`, `InventoryConfig`, `ReceiptConfig`, `SystemConfig`).
- **Admin Settings View**: Admins can interactively edit store name, DL number, GSTIN, cold chain min/max bounds, reorder thresholds, and trigger manual database backups directly from the UI.

---

## 📡 Activity & Audit Logging Subsystem

Every event across the system is recorded to both disk and database:
- **Disk File**: `logs/activity.log` captures standard formatted log entries with timestamps, user credentials, roles, and action details.
- **SQLite Database**: Table `audit_logs` maintains queryable history.
- **Search & Filter**: Admin UI supports instant full-text filtering by action, user name, role, or log level (`ALL`, `INFO`, `WARN`, `CRITICAL`).
- **CSV Export**: 1-click export of the complete audit log to CSV for compliance audits.
- **Database Backup**: 1-click timestamped snapshot backup to `backups/pharmacy_backup_YYYYMMDD_HHMMSS.db`.

---

## 📂 Project Structure

```
Pharmacy_Management_System/
├── README.md                      # Comprehensive System Documentation
├── main.py                        # Primary Unified Entry Point (Auto-detects WebView2/Legacy)
├── desktop_app.py                 # Next-Gen Hardware-Accelerated WebView2 Desktop Runner
├── app.py                         # Legacy CustomTkinter Desktop Application
├── config.json                    # Active Centralized Configuration
├── config.example.json            # Configuration Template
├── config/                        # Configuration Module
│   ├── __init__.py                # Package exports
│   └── settings.py                # Typed Configuration Models & SettingsManager
├── assets/                        # High-Resolution Architectural & ER Diagrams
│   ├── er_diagram.svg             # Scalable Vector Graphics ER Diagram
│   └── er_diagram.png             # 300 DPI High-Definition Master ER Diagram
├── docs/                          # Comprehensive Technical Documentation
│   └── DATABASE_ERD.md            # Complete Database Schema, ERD & Data Dictionary
├── backups/                       # Timestamped SQLite Database Snapshots
├── logs/                          # Physical File-based Activity Logs
├── apps/                          # Dedicated Standalone Terminal Launchers
│   ├── admin_app.py               # Standalone Admin Command Center
│   ├── cashier_app.py             # Standalone Cashier POS Terminal
│   ├── delivery_app.py            # Standalone Delivery Fleet Terminal
│   ├── inventory_app.py           # Standalone Inventory Hub Terminal
│   └── pharmacist_app.py          # Standalone Pharmacist Clinical Station
├── core/                          # Data, Security & Network Layer
│   ├── bridge.py                  # Python Native RPC Bridge for Desktop Frontend
│   ├── api_client.py              # Asynchronous Presence Heartbeat & Event Logger
│   ├── db.py                      # SQLite Central State Engine & Relational CRUD Layer
│   └── logger.py                  # Dual File/DB Activity Logger, CSV Export & Backup
├── tests/                         # Automated Verification Test Suite
│   └── test_all_features.py       # 18 Automated Integration & Unit Tests
├── ui/                            # Desktop & CustomTkinter UI
│   ├── desktop/                   # Next-Gen Hardware-Accelerated UI
│   │   └── index.html             # Responsive Single-Page Desktop Application
│   ├── theme.py                   # Light (Default White) & Dark Color Tokens
│   ├── components/                # Reusable Widgets (Toasts, Badges, etc.)
│   └── views/                     # CustomTkinter Role Dashboard Views
│       ├── login_view.py          # Unified Authentication Screen
│       ├── admin_dashboard_view.py      # Admin Command Center, Staff, Settings & Logs
│       ├── pharmacist_dashboard_view.py # Pharmacist Clinical & CDSS Station
│       ├── cashier_dashboard_view.py    # Cashier POS & Billing Terminal
│       ├── inventory_dashboard_view.py  # Inventory & FEFO Batch Ledger
│       └── delivery_dashboard_view.py   # Delivery Dispatch & e-POD App
├── server/                        # Optional Central Cloud/Network Gateway
│   └── gateway_server.py          # FastAPI Gateway Server & REST Endpoints
└── data/                          # Seed Datasets
    └── mock_db.py                 # Initial medicines, patients, and batch data
```

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
