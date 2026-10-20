# 🎯 TQM Pharm Enterprise — Examiner Live Demonstration Guide
## University Project Review 1: Setup, SRS & Working Application Walkthrough
**Academic Institution:** Amrapali University, Haldwani / Nainital  
**Presenter:** Piyush Bhatt (B.Tech Computer Science & Engineering)  
**System Evaluated:** TQM Pharm Enterprise (Zero-Defect Pharmacy Operating System)  
**Evaluation Scope:** Review 1 – Setup & SRS / Working Application / Demo  

---

## 📋 Evaluation Rubric Alignment Matrix

| Rubric Criteria (Review 1) | Demonstrated Component in TQM Pharm | Verification Location |
| :--- | :--- | :--- |
| **1. Setup & Baseline Understanding** | Complete project architecture, virtualenv, dependencies installed, dual desktop/web runtime setup. | `main.py`, `web_app.py`, `requirements.txt` |
| **2. Modular Folder Architecture** | Strict 6-tier separation (`apps/`, `core/`, `ui/`, `server/`, `config/`, `tests/`). | Workspace Directory Tree |
| **3. Software Requirements Specification** | Formal IEEE Std 830-1998 compliant SRS document with complete functional & non-functional requirements. | `SRS_TQM Pharm_Enterprise.pdf / .docx / .md` |
| **4. Working Application & System Workflow** | Fully functional desktop GUI (CustomTkinter + Edge WebView2) and cloud web portal (FastAPI). | Live Demonstration |
| **5. Comprehensive CRUD Operations** | Full Create, Read, Update, Delete operations across staff, medicines, prescriptions, invoices, and suppliers. | Table CRUD Matrix in SRS Section 6.2 |
| **6. Core Modules Aligned with Quality Goals** | CDSS safety interception, automated FEFO batch dispensing, IoT cold-chain (2-8°C) monitoring, Z-Report balancing. | Slides 6–10 in PPTX & Live App Modals |
| **7. Database Integration** | 14-table relational SQLite schema with foreign keys, checks, default values, and ACID transactions. | `core/db.py` & SQLite Database |
| **8. Automated Verification & Testing** | 24/24 passing unit and integration tests asserting clinical rules, FEFO sorting, and financial integrity. | `tests/test_all_features.py` & `pytest` |

---

## 🚀 How to Launch the Application

### 1. Run Automated Test Suite (Examiner Quality Proof)
Open PowerShell in the project directory and run:
```powershell
pytest
```
*Expected Output:* `24 passed in ~7.8s` (Zero failures, zero errors).

### 2. Launch the Native Desktop Workstation Application
```powershell
python main.py
```
*(Alternatively, run `python desktop_app.py` for direct launch).*

### 3. Launch the Cloud-Ready Web Portal
In a second terminal window, run:
```powershell
python web_app.py
```
Open your browser and navigate to: **`http://127.0.0.1:8000`**

---

## 🔑 Workstation Personas & Default Credentials

| Workstation Role | Username | Password | Terminal Location | Focus Area for Demo |
| :--- | :--- | :--- | :--- | :--- |
| **👑 Store Admin** | `admin` | `admin123` | Store Admin HQ | Staff RBAC CRUD, Presence Telemetry, Daily Z-Report Cash Balancing, Audit Trail. |
| **🩺 Clinical Pharmacist** | `pharmacist` | `pharma123` | Dispensing Counter | eRx Queue, CDSS Drug-Drug/Allergy Safety Engine, Schedule X Double Sign-Off. |
| **💳 POS Cashier** | `cashier` | `cash123` | Front Counter A | 1-Click eRx Import, Barcode Scanning, FEFO Batch Selection, Split Payments, GST Receipt. |
| **📦 Inventory Manager** | `inventory` | `inv123` | Inwarding Bay | FEFO Batch Ledger, Add Medicine (CRUD), Goods Receipt Notes (GRN), Cold-Chain IoT (2-8°C). |
| **🚚 Delivery Agent** | `delivery` | `deliv123` | Delivery Dock | Active Route Kanban Board, Cold-Bag Checklist, 4-Digit OTP e-POD Verification. |

---

## 🎬 Step-by-Step Live Demonstration Script

Follow this sequential 6-step walkthrough during your presentation:

### Step 1: Workstation Login Portal & Clinical Dual Theming
1. **Show Default Light Mode:** Highlight the ultra-clean White/Light theme designed for hospital lighting and ergonomic clinical visibility.
2. **Toggle Dark Mode:** Click the `🌙 Dark Mode` button in the top navigation bar to demonstrate instant, flicker-free UI theming.
3. **Persona Selector Grid:** Click the persona badges (`Store Admin`, `Pharmacist`, `Cashier`, etc.) to demonstrate instant credential pre-filling.
4. **Terminal Selector:** Show assignment to physical counter terminals (`Front Counter A`, `Clinical Kiosk B`, `Inwarding Bay`).

---

### Step 2: Clinical Pharmacist Station & CDSS Safety Engine (TQM Zero-Defect)
1. **Login:** Select **Clinical Pharmacist** (`pharmacist` / `pharma123`).
2. **e-Prescription Intake Queue:**
   - View pending incoming doctor prescriptions.
   - Point out patient demographics, diagnosis, and prescribed medication lines.
3. **Demonstrate CDSS Safety Interception (Poka-Yoke):**
   - Click on an incoming prescription with **Amoxicillin** for a patient recorded with a **Penicillin allergy**, or **Aspirin + Warfarin**.
   - Show how the **CDSS Engine** instantly intercepts the contraindication with a high-visibility warning badge.
   - Explain to examiners: *"Under TQM Zero-Defect principles, the system prevents clinical malpractice at the source before the medication can ever reach the POS counter."*
4. **Schedule X / NDPS Narcotic Double Sign-Off:**
   - Select a controlled substance prescription (e.g. Zolpidem / Ketamine).
   - Click **Verify & Sign Off**.
   - Enter Doctor DMC Reg No: `DMC-2024-8891` and Pharmacist PIN: `9944`.
   - Show how the transaction is recorded in the statutory `narcotic_register` and exportable to CSV for drug inspectors.
5. **Sign Out:** Return to login screen.

---

### Step 3: POS Cashier Station & Express Billing
1. **Login:** Select **POS Cashier** (`cashier` / `cash123`).
2. **1-Click eRx Import:**
   - Click **Import Approved eRx**. The clinically validated prescription is pulled directly into the POS cart without manual re-typing.
3. **Automated FEFO Batch Selection:**
   - Show the cart items: the system automatically picked the batch with the earliest expiration date to eliminate dead stock wastage.
   - Note the real-time GST tax calculation (5%, 12%, 18%).
4. **Multi-Tender Split Settlement:**
   - Click **Checkout**.
   - **Cash:** Enter tendered amount (e.g., ₹1000 for a ₹740 bill) — show automated change return calculation (`Change: ₹260`).
   - **UPI QR:** Switch to UPI mode — dynamic QR code is displayed with interactive simulated bank confirmation.
5. **Print Official GST Thermal Receipt:**
   - Click **Generate Invoice / Print Receipt**.
   - Show the 80mm thermal receipt layout complete with Tax Breakdown, Batch Numbers, Expiry Dates, and QR code.
6. **Route to Delivery:**
   - Check the **"Dispatch for Home Delivery"** checkbox on checkout to route the order directly to the logistics fleet.

---

### Step 4: Supply Chain, FEFO Inventory & Cold-Chain IoT Monitor
1. **Login:** Select **Inventory Manager** (`inventory` / `inv123`).
2. **Multi-Batch FEFO Ledger (CRUD Read & Update):**
   - View stock sorted by nearest expiration.
   - Point out color-coded badges:
     - 🔴 `Critical (< 30 days)`
     - 🟡 `Attention (< 90 days)`
     - 🟢 `Healthy (> 90 days)`
   - Show that expired stock is locked from dispensing.
3. **Add Medicine Modal (CRUD Create):**
   - Click **Add Medicine**. Enter SKU, generic name, category, schedule, batch, expiry, rack coordinate, and cold-chain flag.
4. **Goods Receipt Notes (GRN) Inwarding:**
   - Click **Inward Consignment (GRN)**.
   - Select Supplier, enter PO number, received batch, and cost price.
   - Demonstrate atomic stock increment in the SQLite database.
5. **Cold-Chain IoT Monitor (2°C–8°C):**
   - Point out the real-time circular temperature gauge for Chamber A (Insulins & Vaccines).
   - Click **Simulate Temperature Spike** (e.g., to 9.4°C).
   - Observe immediate visual alarm banner, alert notification, and automated log entry in `temperature_logs`.

---

### Step 5: Fulfilment & Delivery Fleet Logistics
1. **Login:** Select **Delivery Agent** (`delivery` / `deliv123`).
2. **Active Route Kanban Board:**
   - View orders under `Packaging`, `Out for Delivery`, and `Delivered`.
3. **Cold-Bag Insulation Checklist:**
   - Click on an order containing insulin: show mandatory pre-dispatch checklist confirming ice-gel packs and insulated bag integrity.
4. **Customer 4-Digit OTP Electronic Proof-of-Delivery (e-POD):**
   - Select order `DEL-001`.
   - Click **Verify Delivery**.
   - Enter recipient OTP: `1234`.
   - Show order transition to `DELIVERED` with timestamp and courier geo-log.

---

### Step 6: Store Admin Command Center & End-of-Day Financial Z-Report
1. **Login:** Select **Store Admin** (`admin` / `admin123`).
2. **Staff User Management & RBAC (CRUD):**
   - View active staff directory.
   - Click **Add Staff User** to create a new user account with assigned role.
   - Edit an existing user or toggle status (`Active` / `Suspended`).
3. **Live Workstation Presence Stream:**
   - Point out the active sessions table showing connected terminals, IP addresses, and 5-second heartbeats.
4. **End-of-Day Financial Z-Report & Cash Drawer Reconciliation:**
   - Open the **Daily Z-Report** module.
   - Show shift financials: Opening Float (₹5,000), Cash Sales, UPI Sales, Card Sales, Petty Cash Payouts.
   - Enter **Actual Physical Cash Counted**.
   - Show automatic variance detection:
     - If count matches: `STATUS: BALANCED (₹0.00 Variance)`
     - If short: `STATUS: SHORTAGE (-₹200.00 Variance)`
   - Click **Sign & Lock Register (Z-Close)**.
   - View and print the official thermal/A4 Z-Report slip with manager signature line.
5. **Immutable 21 CFR Part 11 Audit Stream:**
   - Show the real-time event log recording every action performed during the demonstration.

---

## 💡 Examiner Q&A Defense Angles (Mastering the Viva)

### Q1: Why did you choose SQLite over MySQL or MongoDB?
> **Answer:** *"For retail pharmacy and hospital dispensing, local-first zero-downtime reliability is paramount. A network outage cannot be allowed to stop critical medication dispensing. SQLite runs embedded within the process with zero external server dependencies, provides full ACID compliance with Write-Ahead Logging (WAL), achieves sub-10ms query execution, and eliminates network latency. At the same time, our FastAPI backend and network sockets allow multi-terminal LAN synchronization across counter workstations."*

### Q2: How does your system implement Total Quality Management (TQM)?
> **Answer:** *"We incorporate four pillars of TQM:*
> 1. **Deming's PDCA Cycle:** *Plan (inventory reorder levels), Do (barcoded FEFO dispensing), Check (CDSS interaction checks and daily Z-Report variance), Act (automated supplier replenishment).*
> 2. **Crosby's Zero Defects:** *Clinical CDSS prevents contraindications; FEFO mathematically prevents expired drug dispensing.*
> 3. **Shigeo Shingo's Poka-Yoke (Mistake-Proofing):** *Disabling checkout buttons when clinical contraindications are present, and enforcing OTP verification before delivery sign-off.*
> 4. **Ishikawa Root-Cause Prevention:** *Cold-chain IoT sensors alert before temperature excursions ruin biologics."*

### Q3: What is the significance of the Daily Z-Report in pharmacy operations?
> **Answer:** *"A Z-Report is the statutory end-of-day register closure required for fiscal compliance. Unlike an intermediate X-Report, a Z-Report reconciles physical cash counted against system calculations (`Opening Float + Cash Sales - Payouts`), isolates cash discrepancies by cashier shift, records GST tax liabilities, and locks the register to prevent retrospective transaction tampering."*

---
*TQM Pharm Enterprise — Demonstration Guide Prepared for Review 1 Evaluation*
