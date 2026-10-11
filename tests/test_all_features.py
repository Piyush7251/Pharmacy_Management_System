"""
AegisPharm Enterprise — Comprehensive Automated Test Suite.
Validates all core features, database integrity, business logic, calculations,
and security workflows across all 5 roles.
"""

import os
import sys
import unittest
from datetime import datetime

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.db import (
    init_db, get_connection, authenticate_user, get_all_staff,
    create_staff_user, update_staff_user, delete_staff_user,
    get_all_medicines, add_medicine, update_medicine_stock, delete_medicine,
    get_all_prescriptions, add_prescription, update_prescription_status,
    create_invoice, get_all_invoices,
    get_all_deliveries, create_delivery_order, update_delivery_status,
    get_all_patients, add_patient, get_patient_by_phone, update_patient_loyalty,
    get_narcotic_records, add_narcotic_record,
    get_all_suppliers, get_all_purchase_orders, add_purchase_order, update_purchase_order_status,
    get_temperature_logs, add_temperature_log,
    get_refill_schedules, update_refill_status,
    get_dashboard_analytics
)

class TestAegisPharmFeatures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    # --- 1. AUTHENTICATION & STAFF RBAC ---
    def test_01_authentication_all_roles(self):
        roles_creds = [
            ("admin", "admin123", "Admin"),
            ("pharmacist", "pharma123", "Pharmacist"),
            ("cashier", "cash123", "Cashier"),
            ("inventory", "inv123", "Inventory Manager"),
            ("delivery", "deliv123", "Delivery Agent"),
        ]
        for uname, pwd, expected_role in roles_creds:
            user = authenticate_user(uname, pwd)
            self.assertIsNotNone(user, f"Authentication failed for {uname}")
            self.assertEqual(user["role"], expected_role)
            self.assertEqual(user["status"], "Active")

    def test_02_authentication_invalid(self):
        user = authenticate_user("admin", "wrongpassword")
        self.assertIsNone(user)
        user = authenticate_user("nonexistent_user", "pass")
        self.assertIsNone(user)

    def test_03_staff_crud_lifecycle(self):
        test_id = "STF-TEST-99"
        # 1. Create
        success, err = create_staff_user(test_id, "Test User", "Cashier", "test.user99", "testpass", "test@pharma.com", "+91 99999 88888", "Branch #01")
        self.assertTrue(success, f"Create user failed: {err}")
        
        # 2. Authenticate newly created user
        user = authenticate_user("test.user99", "testpass")
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "Test User")
        
        # 3. Update
        success, err = update_staff_user(test_id, "Test User Updated", "Pharmacist", "test.user99", "newpass", "test@pharma.com", "+91 99999 88888", "Branch #01", "Active")
        self.assertTrue(success, f"Update user failed: {err}")
        user = authenticate_user("test.user99", "newpass")
        self.assertIsNotNone(user)
        self.assertEqual(user["role"], "Pharmacist")
        
        # 4. Delete
        del_success = delete_staff_user(test_id)
        self.assertTrue(del_success)
        user = authenticate_user("test.user99", "newpass")
        self.assertIsNone(user)

    # --- 2. MEDICINES & INVENTORY ---
    def test_04_medicines_catalog_and_stock(self):
        meds = get_all_medicines()
        self.assertGreaterEqual(len(meds), 1)
        
        # Pick first medicine and check stock adjustment
        med = meds[0]
        initial_stock = med["stock"]
        
        # Add 10 stock
        update_medicine_stock(med["id"], 10)
        updated_med = next(m for m in get_all_medicines() if m["id"] == med["id"])
        self.assertEqual(updated_med["stock"], initial_stock + 10)
        
        # Revert
        update_medicine_stock(med["id"], -10)
        reverted_med = next(m for m in get_all_medicines() if m["id"] == med["id"])
        self.assertEqual(reverted_med["stock"], initial_stock)

    def test_05_medicine_crud(self):
        test_med_id = "MED-TEST-999"
        med_data = {
            "id": test_med_id,
            "name": "Test Medicine 500mg",
            "generic": "Test Salt Molecule",
            "category": "Pain / General",
            "schedule": "Schedule H",
            "manufacturer": "Test Pharma Labs",
            "batch": "TEST-BAT-01",
            "expiry": "2027-12-31",
            "days_to_expiry": 450,
            "stock": 50,
            "unit": "Strip (10 tabs)",
            "mrp": 99.00,
            "cost_price": 60.00,
            "gst_pct": 12,
            "rack": "TEST-RACK-01",
            "cold_chain": False,
            "interactions": ["Warfarin"]
        }
        success, err = add_medicine(med_data)
        self.assertTrue(success, f"Add medicine failed: {err}")
        
        # Verify in catalog
        all_meds = get_all_medicines()
        found = next((m for m in all_meds if m["id"] == test_med_id), None)
        self.assertIsNotNone(found)
        self.assertEqual(found["stock"], 50)
        self.assertEqual(found["interactions"], ["Warfarin"])
        
        # Delete
        del_success = delete_medicine(test_med_id)
        self.assertTrue(del_success)
        found_after = next((m for m in get_all_medicines() if m["id"] == test_med_id), None)
        self.assertIsNone(found_after)

    # --- 3. PATIENTS & LOYALTY ---
    def test_06_patient_phone_lookup(self):
        # Look up existing seed patient Rajesh Sharma (+91 98765 43210)
        p1 = get_patient_by_phone("9876543210")
        self.assertIsNotNone(p1)
        self.assertEqual(p1["name"], "Rajesh Sharma")
        self.assertIn("Penicillin", p1["allergies"])
        
        # Phone with country code and spaces
        p2 = get_patient_by_phone("+91 98765 43210")
        self.assertIsNotNone(p2)
        self.assertEqual(p2["id"], p1["id"])

    def test_07_patient_loyalty_update(self):
        p = get_patient_by_phone("9876543210")
        initial_points = p["loyalty_points"]
        
        # Deduct 100 points
        update_patient_loyalty(p["id"], -100)
        p_updated = get_patient_by_phone("9876543210")
        self.assertEqual(p_updated["loyalty_points"], max(0, initial_points - 100))
        
        # Restore points
        update_patient_loyalty(p["id"], 100)
        p_restored = get_patient_by_phone("9876543210")
        self.assertEqual(p_restored["loyalty_points"], initial_points)

    # --- 4. PRESCRIPTIONS & CLINICAL APPROVAL ---
    def test_08_prescription_lifecycle(self):
        test_rx_id = f"RX-TEST-{int(datetime.now().timestamp())}"
        rx_data = {
            "rx_id": test_rx_id,
            "patient_name": "Test Patient",
            "patient_id": "PAT-TEST-01",
            "doctor_name": "Dr. Joshi",
            "hospital": "City Care Hospital",
            "date": "2026-10-11",
            "status": "Verification Required",
            "items": [{"medicine": "Augmentin 625 Duo Tablet", "dosage": "1 tab daily", "qty": 10}],
            "notes": "Test notes",
            "verified_by": None,
            "verified_at": None
        }
        success, err = add_prescription(rx_data)
        self.assertTrue(success, f"Add prescription failed: {err}")
        
        # Approve
        appr_success = update_prescription_status(test_rx_id, "Verified & Approved", "Pharmacist Pooja")
        self.assertTrue(appr_success)
        
        rx_list = get_all_prescriptions()
        found = next(r for r in rx_list if r["rx_id"] == test_rx_id)
        self.assertEqual(found["status"], "Verified & Approved")
        self.assertEqual(found["verified_by"], "Pharmacist Pooja")

    # --- 5. INVOICES & AUTOMATIC STOCK DEDUCTION ---
    def test_09_invoice_creation_and_stock_deduction(self):
        meds = get_all_medicines()
        med = meds[0]
        initial_stock = med["stock"]
        
        test_inv_id = f"INV-TEST-{int(datetime.now().timestamp())}"
        inv_data = {
            "invoice_id": test_inv_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "patient_name": "Walk-in Test Customer",
            "cashier_name": "Amit Deshmukh",
            "payment_method": "Cash",
            "subtotal": med["mrp"] * 2,
            "gst_amount": (med["mrp"] * 2) * 0.12,
            "total_amount": (med["mrp"] * 2),
            "items": [
                {
                    "med_id": med["id"],
                    "name": med["name"],
                    "batch": med["batch"],
                    "qty": 2,
                    "rate": med["mrp"],
                    "amount": med["mrp"] * 2
                }
            ]
        }
        success, err = create_invoice(inv_data)
        self.assertTrue(success, f"Invoice creation failed: {err}")
        
        # Verify stock was decremented by 2
        updated_med = next(m for m in get_all_medicines() if m["id"] == med["id"])
        self.assertEqual(updated_med["stock"], max(0, initial_stock - 2))
        
        # Restore stock
        update_medicine_stock(med["id"], 2)

    # --- 6. DELIVERY DISPATCH & OTP VERIFICATION ---
    def test_10_delivery_dispatch_and_otp(self):
        test_order_id = f"ORD-TEST-{int(datetime.now().timestamp())}"
        deliv_data = {
            "order_id": test_order_id,
            "patient_name": "Test Home Patient",
            "address": "101, Test Road, Mumbai",
            "phone": "+91 98200 11111",
            "agent_name": "Ramesh Kumar",
            "status": "Packaging & Verification",
            "time_slot": "14:00 - 16:00",
            "items_count": 1,
            "cold_chain_pack": 0,
            "amount": 250.00,
            "payment_status": "Paid (UPI)",
            "otp": "4821"
        }
        success, err = create_delivery_order(deliv_data)
        self.assertTrue(success, f"Create delivery failed: {err}")
        
        # Transition 1: Out for Delivery
        st1 = update_delivery_status(test_order_id, "Out for Delivery")
        self.assertTrue(st1)
        found = next(d for d in get_all_deliveries() if d["order_id"] == test_order_id)
        self.assertEqual(found["status"], "Out for Delivery")
        
        # Transition 2: Delivered (OTP Verified)
        st2 = update_delivery_status(test_order_id, "Delivered (OTP Verified)")
        self.assertTrue(st2)
        found_deliv = next(d for d in get_all_deliveries() if d["order_id"] == test_order_id)
        self.assertEqual(found_deliv["status"], "Delivered (OTP Verified)")

    # --- 7. NARCOTIC REGISTER ---
    def test_11_narcotic_record(self):
        rec_data = {
            "rx_id": "RX-NARCO-01",
            "patient_name": "Test Narcotic Patient",
            "patient_phone": "+91 98200 99999",
            "doctor_name": "Dr. K. Joshi",
            "doctor_reg_no": "DMC-8821",
            "medicine_name": "Alprax 0.5mg Tablet",
            "batch_no": "ALP-9912",
            "quantity": 10,
            "pharmacist_name": "Pooja Sharma, R.Ph",
            "pharmacist_reg_no": "PH-MH-44102"
        }
        success = add_narcotic_record(rec_data)
        self.assertTrue(success)
        
        records = get_narcotic_records()
        self.assertTrue(any(r["rx_id"] == "RX-NARCO-01" for r in records))

    # --- 8. COLD CHAIN TELEMETRY & ALERTS ---
    def test_12_cold_chain_telemetry(self):
        initial_logs = get_temperature_logs(5)
        
        # Add normal temperature
        add_temperature_log("SENSOR-TEST-01", 4.5, "Optimal (2-8°C)")
        logs_after_norm = get_temperature_logs(5)
        self.assertEqual(logs_after_norm[0]["temperature"], 4.5)
        self.assertEqual(logs_after_norm[0]["alert_triggered"], 0)
        
        # Add spike temperature (>8°C)
        add_temperature_log("SENSOR-TEST-01", 9.8, "BREACH ALERT (>8°C)")
        logs_after_spike = get_temperature_logs(5)
        self.assertEqual(logs_after_spike[0]["temperature"], 9.8)
        self.assertEqual(logs_after_spike[0]["alert_triggered"], 1)

    # --- 9. REFILL ADHERENCE ---
    def test_13_refill_schedule_status(self):
        refills = get_refill_schedules()
        self.assertGreaterEqual(len(refills), 1)
        target = refills[0]
        
        success = update_refill_status(target["id"], "Reminder Sent (WhatsApp)")
        self.assertTrue(success)
        
        updated = next(r for r in get_refill_schedules() if r["id"] == target["id"])
        self.assertEqual(updated["status"], "Reminder Sent (WhatsApp)")

    # --- 10. OVERALL STORE ANALYTICS ---
    def test_14_dashboard_analytics_aggregation(self):
        analytics = get_dashboard_analytics()
        self.assertIn("gross_sales", analytics)
        self.assertIn("total_gst", analytics)
        self.assertIn("total_sales_count", analytics)
        self.assertIn("total_meds", analytics)
        self.assertIn("low_stock_count", analytics)
        self.assertIn("total_rx", analytics)
        self.assertIn("total_deliv", analytics)
        self.assertGreater(analytics["total_meds"], 0)
        self.assertGreaterEqual(analytics["gross_sales"], 0.0)

if __name__ == "__main__":
    unittest.main()
