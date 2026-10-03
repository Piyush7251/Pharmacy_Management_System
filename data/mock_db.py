"""
Mock Database and In-Memory Data Store for Pharmacy Management System.
Contains comprehensive datasets matching the 6-layer architecture specifications.
"""

MEDICINES_CATALOG = [
    {
        "id": "MED-001",
        "name": "Augmentin 625 Duo Tablet",
        "generic": "Amoxicillin (500mg) + Clavulanic Acid (125mg)",
        "category": "Antibiotic",
        "schedule": "Schedule H",
        "manufacturer": "GSK Healthcare",
        "batch": "AUG-2025-09",
        "expiry": "2026-11-30",
        "days_to_expiry": 420,
        "stock": 145,
        "unit": "Strip (10 tabs)",
        "mrp": 204.50,
        "cost_price": 148.00,
        "gst_pct": 12,
        "rack": "A-12-B",
        "cold_chain": False,
        "interactions": ["Methotrexate", "Warfarin"]
    },
    {
        "id": "MED-002",
        "name": "Pan-D Capsule",
        "generic": "Pantoprazole (40mg) + Domperidone (30mg)",
        "category": "Gastrointestinal",
        "schedule": "Schedule H",
        "manufacturer": "Alkem Laboratories",
        "batch": "PAND-883",
        "expiry": "2027-04-15",
        "days_to_expiry": 560,
        "stock": 280,
        "unit": "Strip (15 caps)",
        "mrp": 199.00,
        "cost_price": 135.00,
        "gst_pct": 12,
        "rack": "B-04-A",
        "cold_chain": False,
        "interactions": ["Ketoconazole", "Atazanavir"]
    },
    {
        "id": "MED-003",
        "name": "Glycomet-GP 2 Forte Tablet",
        "generic": "Metformin (1000mg) + Glimepiride (2mg)",
        "category": "Antidiabetic",
        "schedule": "Schedule H",
        "manufacturer": "USV Pharma",
        "batch": "GLY-4102",
        "expiry": "2026-03-20",
        "days_to_expiry": 170,
        "stock": 18,  # Low stock
        "unit": "Strip (15 tabs)",
        "mrp": 142.50,
        "cost_price": 98.00,
        "gst_pct": 12,
        "rack": "C-01-D",
        "cold_chain": False,
        "interactions": ["Furosemide", "Nifedipine", "Alcohol"]
    },
    {
        "id": "MED-004",
        "name": "Telma-H 40mg Tablet",
        "generic": "Telmisartan (40mg) + Hydrochlorothiazide (12.5mg)",
        "category": "Cardiovascular / BP",
        "schedule": "Schedule H",
        "manufacturer": "Glenmark Pharma",
        "batch": "TLM-9912",
        "expiry": "2026-01-10",
        "days_to_expiry": 100,  # Expiring soon
        "stock": 95,
        "unit": "Strip (15 tabs)",
        "mrp": 268.00,
        "cost_price": 185.00,
        "gst_pct": 12,
        "rack": "C-08-A",
        "cold_chain": False,
        "interactions": ["Lithium", "Potassium Supplements", "NSAIDs"]
    },
    {
        "id": "MED-005",
        "name": "Lantus Solostar Insulin Pen (100IU/ml)",
        "generic": "Insulin Glargine (rDNA origin)",
        "category": "Endocrine / Insulin",
        "schedule": "Schedule G",
        "manufacturer": "Sanofi India",
        "batch": "LAN-5521",
        "expiry": "2026-08-15",
        "days_to_expiry": 315,
        "stock": 32,
        "unit": "Pen (3ml)",
        "mrp": 725.00,
        "cost_price": 540.00,
        "gst_pct": 5,
        "rack": "FRIDGE-01 (2-8°C)",
        "cold_chain": True,
        "interactions": ["Beta Blockers", "Corticosteroids"]
    },
    {
        "id": "MED-006",
        "name": "Alprax 0.5mg Tablet",
        "generic": "Alprazolam (0.5mg)",
        "category": "Psychotropic / Sedative",
        "schedule": "Schedule X / Narcotic",
        "manufacturer": "Torrent Pharma",
        "batch": "ALP-7703",
        "expiry": "2027-01-30",
        "days_to_expiry": 485,
        "stock": 60,
        "unit": "Strip (15 tabs)",
        "mrp": 78.00,
        "cost_price": 45.00,
        "gst_pct": 12,
        "rack": "LOCKER-SECURE-A",
        "cold_chain": False,
        "interactions": ["Opioids", "Alcohol", "Fluconazole", "Cimetidine"]
    },
    {
        "id": "MED-007",
        "name": "Dolo 650 Tablet",
        "generic": "Paracetamol (650mg)",
        "category": "Analgesic / Antipyretic",
        "schedule": "OTC",
        "manufacturer": "Micro Labs",
        "batch": "DOLO-1299",
        "expiry": "2027-09-10",
        "days_to_expiry": 710,
        "stock": 450,
        "unit": "Strip (15 tabs)",
        "mrp": 34.00,
        "cost_price": 22.00,
        "gst_pct": 12,
        "rack": "A-01-A",
        "cold_chain": False,
        "interactions": ["Warfarin (high dose)", "Isoniazid"]
    },
    {
        "id": "MED-008",
        "name": "Montair-LC Tablet",
        "generic": "Montelukast (10mg) + Levocetirizine (5mg)",
        "category": "Antiallergic / Respiratory",
        "schedule": "Schedule H",
        "manufacturer": "Cipla Ltd",
        "batch": "MLC-6610",
        "expiry": "2026-05-30",
        "days_to_expiry": 240,
        "stock": 120,
        "unit": "Strip (10 tabs)",
        "mrp": 215.00,
        "cost_price": 140.00,
        "gst_pct": 12,
        "rack": "B-15-C",
        "cold_chain": False,
        "interactions": ["Phenobarbital", "Rifampicin"]
    }
]

PATIENTS = [
    {
        "id": "PAT-1001",
        "name": "Rajesh Sharma",
        "age": 52,
        "gender": "Male",
        "phone": "+91 98765 43210",
        "allergies": ["Penicillin", "Sulfa drugs"],
        "chronic_conditions": ["Type 2 Diabetes", "Hypertension"],
        "loyalty_points": 450,
        "recent_doctor": "Dr. Vivek Mehra (MD Cardiology)"
    },
    {
        "id": "PAT-1002",
        "name": "Priya Verma",
        "age": 34,
        "gender": "Female",
        "phone": "+91 98112 34567",
        "allergies": ["Aspirin / NSAIDs"],
        "chronic_conditions": ["Asthma", "GERD"],
        "loyalty_points": 180,
        "recent_doctor": "Dr. Sunita Rao (Pulmonologist)"
    },
    {
        "id": "PAT-1003",
        "name": "Harish Patel",
        "age": 68,
        "gender": "Male",
        "phone": "+91 97234 56789",
        "allergies": [],
        "chronic_conditions": ["Chronic Kidney Disease", "Hypertension"],
        "loyalty_points": 820,
        "recent_doctor": "Dr. K. N. Joshi (Nephrologist)"
    }
]

PRESCRIPTIONS_QUEUE = [
    {
        "rx_id": "RX-2026-089",
        "patient": "Rajesh Sharma",
        "patient_id": "PAT-1001",
        "doctor": "Dr. Vivek Mehra (Reg #DMC-44910)",
        "hospital": "Apex Heart & Multispeciality Clinic",
        "date": "2026-10-02",
        "status": "Verification Required",
        "items": [
            {"medicine": "Telma-H 40mg Tablet", "dosage": "1 tab daily morning", "qty": 30, "duration": "30 Days"},
            {"medicine": "Glycomet-GP 2 Forte Tablet", "dosage": "1 tab with breakfast", "qty": 30, "duration": "30 Days"},
            {"medicine": "Augmentin 625 Duo Tablet", "dosage": "1 tab twice daily", "qty": 10, "duration": "5 Days"}
        ],
        "notes": "Patient allergic to Penicillin. WARNING: Augmentin contains Amoxicillin (Penicillin group)!"
    },
    {
        "rx_id": "RX-2026-090",
        "patient": "Priya Verma",
        "patient_id": "PAT-1002",
        "doctor": "Dr. Sunita Rao (Reg #KMC-11029)",
        "hospital": "City Chest Care Hospital",
        "date": "2026-10-02",
        "status": "Ready for Dispensing",
        "items": [
            {"medicine": "Montair-LC Tablet", "dosage": "1 tab at bedtime", "qty": 20, "duration": "20 Days"},
            {"medicine": "Pan-D Capsule", "dosage": "1 cap before food in morning", "qty": 15, "duration": "15 Days"}
        ],
        "notes": "Standard seasonal allergy prescription."
    },
    {
        "rx_id": "RX-2026-091",
        "patient": "Harish Patel",
        "patient_id": "PAT-1003",
        "doctor": "Dr. K. N. Joshi (Reg #GMC-8823)",
        "hospital": "Kidney Care & Dialysis Institute",
        "date": "2026-10-01",
        "status": "Schedule X Approval Pending",
        "items": [
            {"medicine": "Alprax 0.5mg Tablet", "dosage": "0.5 tab SOS for anxiety/insomnia", "qty": 15, "duration": "15 Days"},
            {"medicine": "Dolo 650 Tablet", "dosage": "1 tab SOS for body ache/fever", "qty": 15, "duration": "As needed"}
        ],
        "notes": "Requires Pharmacist Double-Signature & ID proof verification."
    }
]

DELIVERY_DISPATCH = [
    {
        "order_id": "ORD-9901",
        "patient": "Mrs. Anita Deshmukh",
        "address": "Flat 402, Green Glen Heights, Sector 14, Navi Mumbai",
        "phone": "+91 99881 22334",
        "agent": "Ramesh Kumar (ID #DL-104)",
        "status": "Out for Delivery",
        "time_slot": "14:00 - 15:30",
        "items_count": 4,
        "cold_chain_pack": True,
        "amount": 1420.00,
        "payment": "Prepaid (UPI)"
    },
    {
        "order_id": "ORD-9902",
        "patient": "Sanjay Gupta",
        "address": "B-12, Palm Springs Residency, Vashi",
        "phone": "+91 98200 44556",
        "agent": "Vikas Shinde (ID #DL-108)",
        "status": "Packaging & Verification",
        "time_slot": "15:00 - 16:30",
        "items_count": 2,
        "cold_chain_pack": False,
        "amount": 485.00,
        "payment": "Cash on Delivery"
    },
    {
        "order_id": "ORD-9903",
        "patient": "Kavita Nair",
        "address": "Villa 9, Sea View Enclave, Nerul",
        "phone": "+91 97690 11223",
        "agent": "Auto-Assigning...",
        "status": "Pending Dispatch",
        "time_slot": "16:30 - 18:00",
        "items_count": 5,
        "cold_chain_pack": True,
        "amount": 2340.00,
        "payment": "Prepaid (Card)"
    }
]

DAILY_STATS = {
    "today_sales": "₹ 48,920.50",
    "prescriptions_dispensed": 38,
    "pending_rx_checks": 3,
    "low_stock_alerts": 4,
    "cold_chain_temp": "4.2 °C (Optimal: 2-8°C)",
    "active_deliveries": 6,
    "cash_in_drawer": "₹ 12,450.00",
    "digital_upi_pos": "₹ 36,470.50"
}
