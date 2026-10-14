"""
AegisPharm Enterprise — Native Desktop RPC Bridge.
Exposes secure, thread-safe Python methods directly to the Edge Chromium WebView2 frontend.
Allows instantaneous, zero-latency desktop interaction without HTTP overhead.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from core.db import (
    authenticate_user, get_all_staff, create_staff_user, update_staff_user, delete_staff_user,
    get_all_medicines, add_medicine, update_medicine_stock, delete_medicine,
    get_all_prescriptions, add_prescription, update_prescription_status,
    create_invoice, get_all_invoices,
    get_all_deliveries, create_delivery_order, update_delivery_status,
    get_all_patients, add_patient, get_patient_by_phone, update_patient_loyalty,
    get_narcotic_records, add_narcotic_record,
    get_all_suppliers, get_all_purchase_orders, add_purchase_order, update_purchase_order_status,
    get_temperature_logs, add_temperature_log,
    get_refill_schedules, update_refill_status,
    get_dashboard_analytics, get_active_sessions, update_session_heartbeat
)
from config.settings import get_settings, save_settings, reset_to_defaults
from core.logger import (
    log_activity, get_activity_logs,
    export_activity_logs_to_csv, backup_sqlite_database
)
from core.api_client import AppConnector

class PharmacyBridge:
    """
    Python RPC Bridge registered with pywebview.
    Methods on this class can be called directly in JavaScript via:
        const res = await window.pywebview.api.<method_name>(...args);
    """
    def __init__(self, window=None):
        self._window = window
        self._current_user = None
        self._connector = None

    def set_window(self, window):
        self._window = window

    # --- 1. AUTHENTICATION & SESSION MANAGEMENT ---

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user against database credentials."""
        user = authenticate_user(username, password)
        if user:
            self._current_user = user
            if self._connector:
                self._connector.stop()
            self._connector = AppConnector(
                user_id=user["id"],
                user_name=user["name"],
                role=user["role"],
                app_name=f"{user['role']} Workstation"
            )
            self._connector.start()
            
            log_activity(
                action="User Login",
                details=f"{user['name']} signed in to {user['role']} session.",
                user_name=user["name"],
                role=user["role"],
                level="INFO"
            )
            return {"success": True, "user": user}
        return {"success": False, "error": "Invalid username or password. Please verify credentials."}

    def logout(self) -> Dict[str, Any]:
        """Sign out current user and terminate presence heartbeat."""
        if self._current_user:
            user_name = self._current_user.get("name", "User")
            role = self._current_user.get("role", "Staff")
            log_activity(
                action="User Sign Out",
                details=f"{user_name} signed out cleanly.",
                user_name=user_name,
                role=role,
                level="INFO"
            )
        if self._connector:
            self._connector.stop()
            self._connector = None
        self._current_user = None
        return {"success": True}

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Return currently signed in staff profile."""
        return self._current_user

    def switch_role(self, role_name: str) -> Dict[str, Any]:
        """Switch active role persona for supervisor inspection (Restricted to Store Admin)."""
        if not self._current_user:
            return {"success": False, "error": "Authentication required. Please sign in to a workstation first."}

        # Regulatory & Security Compliance: In production, non-admin staff cannot switch identity without logging out
        if self._current_user.get("role") != "Admin":
            log_activity(
                action="Unauthorized Role Switch Attempt",
                details=f"{self._current_user.get('name')} ({self._current_user.get('role')}) attempted to switch to {role_name}.",
                user_name=self._current_user.get("name", "Unknown"),
                role=self._current_user.get("role", "Staff"),
                level="WARN"
            )
            return {
                "success": False,
                "error": f"Access Denied: Station identity is locked to {self._current_user.get('name')} ({self._current_user.get('role')}). Please Lock / Sign Out to log in as another user."
            }

        role_map = {
            "Admin": ("Admin", "Dr. Rajesh Kulkarni", "STF-01"),
            "Store Admin": ("Admin", "Dr. Rajesh Kulkarni", "STF-01"),
            "Pharmacist": ("Pharmacist", "Pooja Sharma, R.Ph", "STF-02"),
            "Cashier": ("Cashier", "Amit Deshmukh", "STF-03"),
            "Inventory Manager": ("Inventory Manager", "Vikram Rathore", "STF-04"),
            "Delivery Agent": ("Delivery Agent", "Ramesh Kumar", "STF-05"),
        }
        target = role_map.get(role_name)
        if target:
            self._current_user["role"] = target[0]
            self._current_user["name"] = target[1]
            self._current_user["id"] = target[2]

            if self._connector:
                self._connector.role = target[0]
                self._connector.user_name = target[1]
                self._connector.user_id = target[2]
                self._connector.update_action(f"Supervisor inspected {target[0]}")

            log_activity(
                action="Supervisor View Switched",
                details=f"Admin switched workstation view to {target[0]} for supervisor inspection.",
                user_name=target[1],
                role=target[0],
                level="INFO"
            )
            return {"success": True, "user": self._current_user}
        return {"success": False, "error": f"Unknown role persona: {role_name}"}

    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Fetch all active online terminal presence heartbeats."""
        return get_active_sessions()

    # --- 2. MEDICINES & INVENTORY ---

    def get_all_medicines(self) -> List[Dict[str, Any]]:
        """Retrieve complete pharmacy inventory catalog."""
        return get_all_medicines()

    def add_medicine(self, med_data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert new medicine SKU into catalog."""
        success, err = add_medicine(med_data)
        if success:
            log_activity(
                action="Medicine Added",
                details=f"Added {med_data.get('name')} (Batch: {med_data.get('batch')}, Stock: {med_data.get('stock')})",
                user_name=self._current_user.get("name", "Staff") if self._current_user else "Staff",
                role=self._current_user.get("role", "Inventory") if self._current_user else "Inventory",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": err}

    def update_medicine_stock(self, med_id: str, delta: int) -> Dict[str, Any]:
        """Adjust medicine stock level by delta."""
        success = update_medicine_stock(med_id, delta)
        if success:
            log_activity(
                action="Stock Adjusted",
                details=f"Adjusted medicine {med_id} by {delta:+d} units.",
                user_name=self._current_user.get("name", "Staff") if self._current_user else "Staff",
                role=self._current_user.get("role", "Inventory") if self._current_user else "Inventory",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": "Failed to adjust stock."}

    def delete_medicine(self, med_id: str) -> Dict[str, Any]:
        """Remove medicine item from inventory (Inventory Manager or Admin Only)."""
        if self._current_user and self._current_user.get("role") not in ("Admin", "Inventory Manager"):
            return {"success": False, "error": "Access Denied: Only Inventory Managers and Administrators can delete items from catalog."}
        success = delete_medicine(med_id)
        if success:
            log_activity(
                action="Medicine Deleted",
                details=f"Removed medicine ID {med_id} from catalog.",
                user_name=self._current_user.get("name", "Staff") if self._current_user else "Staff",
                role=self._current_user.get("role", "Inventory") if self._current_user else "Inventory",
                level="WARN"
            )
            return {"success": True}
        return {"success": False, "error": "Failed to delete medicine."}

    # --- 3. PRESCRIPTIONS & CLINICAL CDSS ---

    def get_all_prescriptions(self) -> List[Dict[str, Any]]:
        """Retrieve all prescriptions in clinical queue."""
        return get_all_prescriptions()

    def add_prescription(self, rx_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new digital prescription."""
        success, err = add_prescription(rx_data)
        if success:
            log_activity(
                action="Prescription Created",
                details=f"New prescription {rx_data.get('rx_id')} for {rx_data.get('patient_name')}.",
                user_name=self._current_user.get("name", "Staff") if self._current_user else "Staff",
                role=self._current_user.get("role", "Clinical") if self._current_user else "Clinical",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": err}

    def update_prescription_status(self, rx_id: str, status: str, verified_by: Optional[str] = None) -> Dict[str, Any]:
        """Update e-Prescription status (e.g. Verified & Approved, Dispensed)."""
        v_by = verified_by or (self._current_user.get("name") if self._current_user else "Pharmacist")
        success = update_prescription_status(rx_id, status, v_by)
        if success:
            log_activity(
                action="Prescription Status Updated",
                details=f"{rx_id} transitioned to '{status}' by {v_by}.",
                user_name=v_by,
                role="Pharmacist",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": "Failed to update prescription status."}

    def get_all_patients(self) -> List[Dict[str, Any]]:
        """Retrieve patient EHR directory."""
        return get_all_patients()

    def add_patient(self, p_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add new patient profile with allergies & conditions."""
        success = add_patient(p_data)
        if success:
            log_activity(
                action="Patient Registered",
                details=f"Added patient {p_data.get('name')} (Phone: {p_data.get('phone')}).",
                user_name=self._current_user.get("name", "Staff") if self._current_user else "Staff",
                role="Clinical",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": "Failed to register patient."}

    def get_patient_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        """Lookup patient profile by phone number for quick POS counter fill."""
        return get_patient_by_phone(phone)

    def get_narcotic_records(self) -> List[Dict[str, Any]]:
        """Retrieve Schedule X NDPS controlled drug register."""
        return get_narcotic_records()

    def add_narcotic_record(self, rec_data: Dict[str, Any]) -> Dict[str, Any]:
        """Record Schedule X double sign-off into official register (Pharmacist or Admin Only)."""
        if self._current_user and self._current_user.get("role") not in ("Admin", "Pharmacist"):
            return {"success": False, "error": "Access Denied: Schedule X NDPS dispensation requires a Registered Pharmacist."}
        success = add_narcotic_record(rec_data)
        if success:
            log_activity(
                action="Narcotic Dispensed (Schedule X)",
                details=f"Dispensed {rec_data.get('medicine_name')} (Qty: {rec_data.get('quantity')}) for {rec_data.get('patient_name')} by {rec_data.get('pharmacist_name')}.",
                user_name=rec_data.get("pharmacist_name", "Pharmacist"),
                role="Pharmacist",
                level="CRITICAL"
            )
            return {"success": True}
        return {"success": False, "error": "Failed to record narcotic entry."}

    # --- 4. POS BILLING & INVOICING ---

    def create_invoice(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final sales invoice and automatically decrement stock."""
        success, err = create_invoice(invoice_data)
        if success:
            # Award loyalty points if enabled
            cfg = get_settings()
            if cfg.receipt.enable_loyalty_points and invoice_data.get("patient_phone"):
                pts = int((invoice_data.get("total_amount", 0.0) / 100.0) * cfg.receipt.loyalty_rate)
                if pts > 0:
                    update_patient_loyalty(invoice_data.get("patient_phone"), pts)

            log_activity(
                action="Invoice Generated",
                details=f"Bill {invoice_data.get('invoice_id')} (₹ {invoice_data.get('total_amount'):.2f}, Method: {invoice_data.get('payment_method')}) by {invoice_data.get('cashier_name')}.",
                user_name=invoice_data.get("cashier_name", "Cashier"),
                role="Cashier",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": err}

    def get_all_invoices(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve recent sales invoices history."""
        return get_all_invoices(limit)

    # --- 5. DELIVERIES & FLEET ---

    def get_all_deliveries(self) -> List[Dict[str, Any]]:
        """Retrieve active delivery dispatch orders."""
        return get_all_deliveries()

    def create_delivery_order(self, deliv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new delivery fulfillment task."""
        success, err = create_delivery_order(deliv_data)
        if success:
            log_activity(
                action="Delivery Created",
                details=f"Order {deliv_data.get('order_id')} for {deliv_data.get('patient_name')} (Agent: {deliv_data.get('agent_name')}).",
                user_name=self._current_user.get("name", "Staff") if self._current_user else "Staff",
                role="Delivery",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": err}

    def update_delivery_status(self, order_id: str, status: str) -> Dict[str, Any]:
        """Update delivery order lifecycle status."""
        success = update_delivery_status(order_id, status)
        if success:
            log_activity(
                action="Delivery Status Updated",
                details=f"Order {order_id} marked as '{status}'.",
                user_name=self._current_user.get("name", "Agent") if self._current_user else "Agent",
                role="Delivery",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": "Failed to update delivery status."}

    # --- 6. SUPPLIERS & PURCHASE ORDERS (GRN) ---

    def get_all_suppliers(self) -> List[Dict[str, Any]]:
        """Retrieve suppliers directory."""
        return get_all_suppliers()

    def get_all_purchase_orders(self) -> List[Dict[str, Any]]:
        """Retrieve purchase orders and inwarding GRNs."""
        return get_all_purchase_orders()

    def add_purchase_order(self, po_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add new purchase order."""
        success = add_purchase_order(po_data)
        if success:
            log_activity(
                action="PO Created",
                details=f"Created {po_data.get('po_id')} for supplier {po_data.get('supplier_name')} (₹ {po_data.get('total_amount'):.2f}).",
                user_name=self._current_user.get("name", "Staff") if self._current_user else "Staff",
                role="Inventory",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": "Failed to add purchase order."}

    def update_purchase_order_status(self, po_id: str, status: str) -> Dict[str, Any]:
        """Update status of purchase order."""
        success = update_purchase_order_status(po_id, status)
        return {"success": success}

    # --- 7. COLD CHAIN TELEMETRY & REFILL ADHERENCE ---

    def get_temperature_logs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieve recent IoT fridge telemetry."""
        return get_temperature_logs(limit)

    def add_temperature_log(self, sensor_id: str, temp: float, status: str = "Optimal (2-8°C)") -> Dict[str, Any]:
        """Record temperature measurement from IoT probe."""
        add_temperature_log(sensor_id, temp, status)
        if temp < 2.0 or temp > 8.0:
            log_activity(
                action="Cold-Chain Breach Alert",
                details=f"Sensor {sensor_id} registered {temp:.1f}°C (Threshold: 2.0-8.0°C).",
                user_name="IoT Sensor",
                role="System",
                level="CRITICAL"
            )
        return {"success": True}

    def get_refill_schedules(self) -> List[Dict[str, Any]]:
        """Retrieve chronic refill schedules."""
        return get_refill_schedules()

    def update_refill_status(self, refill_id: str, status: str) -> Dict[str, Any]:
        """Update chronic refill schedule status."""
        success = update_refill_status(refill_id, status)
        return {"success": success}

    # --- 8. DASHBOARD ANALYTICS & STAFF RBAC ---

    def get_dashboard_analytics(self) -> Dict[str, Any]:
        """Fetch overall business KPIs, financials, and inventory counts."""
        return get_dashboard_analytics()

    def get_all_staff(self) -> List[Dict[str, Any]]:
        """Retrieve staff list for admin."""
        return get_all_staff()

    def create_staff_user(self, staff_id: str, name: str, role: str, username: str, password: str, email: str, phone: str, branch: str) -> Dict[str, Any]:
        """Create new staff account (Admin Only)."""
        if self._current_user and self._current_user.get("role") != "Admin":
            return {"success": False, "error": "Access Denied: Only Store Administrators can manage staff accounts."}
        success, err = create_staff_user(staff_id, name, role, username, password, email, phone, branch)
        if success:
            log_activity(
                action="Staff User Created",
                details=f"Created staff account {username} ({name}, Role: {role}).",
                user_name=self._current_user.get("name", "Admin") if self._current_user else "Admin",
                role="Admin",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": err}

    def update_staff_user(self, staff_id: str, name: str, role: str, username: str, password: str, email: str, phone: str, branch: str, status: str = "Active") -> Dict[str, Any]:
        """Update existing staff account (Admin Only)."""
        if self._current_user and self._current_user.get("role") != "Admin":
            return {"success": False, "error": "Access Denied: Only Store Administrators can manage staff accounts."}
        success, err = update_staff_user(staff_id, name, role, username, password, email, phone, branch, status)
        if success:
            log_activity(
                action="Staff User Updated",
                details=f"Updated staff account {username} (Status: {status}).",
                user_name=self._current_user.get("name", "Admin") if self._current_user else "Admin",
                role="Admin",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": err}

    def delete_staff_user(self, staff_id: str) -> Dict[str, Any]:
        """Delete staff account (Admin Only)."""
        if self._current_user and self._current_user.get("role") != "Admin":
            return {"success": False, "error": "Access Denied: Only Store Administrators can delete staff accounts."}
        success = delete_staff_user(staff_id)
        if success:
            log_activity(
                action="Staff User Deleted",
                details=f"Deleted staff user ID {staff_id}.",
                user_name=self._current_user.get("name", "Admin") if self._current_user else "Admin",
                role="Admin",
                level="WARN"
            )
            return {"success": True}
        return {"success": False, "error": "Failed to delete user."}

    # --- 9. CONFIGURATION & SYSTEM SETTINGS ---

    def get_settings(self) -> Dict[str, Any]:
        """Retrieve centralized system configuration as dictionary."""
        return get_settings().to_dict()

    def save_settings(self, settings_data: Dict[str, Any]) -> Dict[str, Any]:
        """Persist updated system configuration (Admin Only)."""
        if self._current_user and self._current_user.get("role") != "Admin":
            return {"success": False, "error": "Access Denied: Only Store Administrators can modify system configuration."}
        success = save_settings(settings_data)
        if success:
            log_activity(
                action="Settings Updated",
                details="Updated store configuration and parameters.",
                user_name=self._current_user.get("name", "Admin") if self._current_user else "Admin",
                role="Admin",
                level="INFO"
            )
            return {"success": True}
        return {"success": False, "error": "Failed to save settings."}

    def reset_settings(self) -> Dict[str, Any]:
        """Reset system configuration back to factory defaults (Admin Only)."""
        if self._current_user and self._current_user.get("role") != "Admin":
            return {"success": False, "error": "Access Denied: Only Store Administrators can reset system configuration."}
        cfg = reset_to_defaults()
        log_activity(
            action="Settings Reset",
            details="Restored system configuration to out-of-the-box defaults.",
            user_name=self._current_user.get("name", "Admin") if self._current_user else "Admin",
            role="Admin",
            level="WARN"
        )
        return {"success": True, "settings": cfg.to_dict()}

    # --- 10. ACTIVITY LOGGING & DATABASE BACKUP ---

    def get_activity_logs(self, limit: int = 50, level: str = "ALL", search: str = "") -> List[Dict[str, Any]]:
        """Query activity audit logs from SQLite."""
        return get_activity_logs(limit, level, search)

    def export_activity_logs(self, target_path: Optional[str] = None) -> Dict[str, Any]:
        """Export activity logs to CSV."""
        if not target_path:
            os.makedirs("backups", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            target_path = os.path.abspath(f"backups/audit_export_{timestamp}.csv")
        success, msg = export_activity_logs_to_csv(target_path)
        return {"success": success, "message": msg, "path": target_path}

    def backup_database(self) -> Dict[str, Any]:
        """Create timestamped snapshot of central database (Admin Only)."""
        if self._current_user and self._current_user.get("role") != "Admin":
            return {"success": False, "error": "Access Denied: Only Store Administrators can perform database backups."}
        success, result_path = backup_sqlite_database()
        return {"success": success, "path": result_path if success else "", "error": "" if success else result_path}

    def log_event(self, action: str, details: str, level: str = "INFO") -> None:
        """Generic client-side action logger."""
        u_name = self._current_user.get("name", "User") if self._current_user else "User"
        role = self._current_user.get("role", "Staff") if self._current_user else "Staff"
        log_activity(action, details, u_name, role, level)
