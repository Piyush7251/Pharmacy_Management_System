"""
AegisPharm Enterprise — Automated Web Application & REST API Test Suite.
Validates FastAPI web server, session authentication, universal RPC bridge,
and standalone web browser parity with the desktop application.
"""

import os
import sys
import unittest

# Ensure application root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from web_app import app
from core.db import init_db

class TestAegisPharmWebApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

    def test_01_health_and_system_info(self):
        """Verify health check endpoint returns 200 and online status."""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "online")
        self.assertEqual(data["system"], "AegisPharm Enterprise")
        self.assertEqual(data["version"], "2.5")

    def test_02_web_frontend_served(self):
        """Verify root URL serves the complete web application HTML."""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/html", resp.headers.get("content-type", ""))
        self.assertIn("AegisPharm Enterprise", resp.text)
        self.assertIn("callBridge", resp.text)
        self.assertIn("login-view", resp.text)
        self.assertIn("pharma-nav-cdss", resp.text)
        self.assertIn("pharma-nav-narcotics", resp.text)

    def test_03_web_authentication_lifecycle(self):
        """Test login with session token generation, authenticated state, and logout."""
        # 1. Invalid credentials
        bad_login = self.client.post("/api/login", json={"args": ["admin", "wrongpass"]})
        self.assertEqual(bad_login.status_code, 200)
        self.assertFalse(bad_login.json()["success"])

        # 2. Valid Admin credentials
        login_resp = self.client.post("/api/login", json={"args": ["admin", "admin123"]})
        self.assertEqual(login_resp.status_code, 200)
        login_data = login_resp.json()
        self.assertTrue(login_data["success"])
        self.assertIn("token", login_data)
        token = login_data["token"]
        self.assertEqual(login_data["user"]["role"], "Admin")

        # 3. Check current user with session token
        user_resp = self.client.post("/api/get_current_user", json={"args": []}, headers={"X-Session-Token": token})
        self.assertEqual(user_resp.status_code, 200)
        user_data = user_resp.json()
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data["username"], "admin")

        # 4. Check unauthenticated client has no user
        unauth_resp = self.client.post("/api/get_current_user", json={"args": []})
        self.assertEqual(unauth_resp.status_code, 200)
        self.assertIsNone(unauth_resp.json())

        # 5. Logout
        logout_resp = self.client.post("/api/logout", json={"args": []}, headers={"X-Session-Token": token})
        self.assertEqual(logout_resp.status_code, 200)
        self.assertTrue(logout_resp.json()["success"])

        # 6. Verify session invalidated
        after_logout = self.client.post("/api/get_current_user", json={"args": []}, headers={"X-Session-Token": token})
        self.assertEqual(after_logout.status_code, 200)
        self.assertIsNone(after_logout.json())

    def test_04_universal_rpc_endpoints(self):
        """Test universal RPC dispatcher calls across all operational domains."""
        # Test get_all_medicines
        meds_resp = self.client.post("/api/get_all_medicines", json={"args": []})
        self.assertEqual(meds_resp.status_code, 200)
        meds = meds_resp.json()
        self.assertIsInstance(meds, list)
        self.assertGreaterEqual(len(meds), 1)

        # Test get_all_prescriptions
        rx_resp = self.client.post("/api/get_all_prescriptions", json={"args": []})
        self.assertEqual(rx_resp.status_code, 200)
        rxs = rx_resp.json()
        self.assertIsInstance(rxs, list)

        # Test get_dashboard_analytics
        kpi_resp = self.client.post("/api/get_dashboard_analytics", json={"args": []})
        self.assertEqual(kpi_resp.status_code, 200)
        kpi = kpi_resp.json()
        self.assertIn("gross_sales", kpi)
        self.assertIn("total_meds", kpi)

        # Test get_narcotic_records
        narc_resp = self.client.post("/api/get_narcotic_records", json={"args": []})
        self.assertEqual(narc_resp.status_code, 200)
        narcs = narc_resp.json()
        self.assertIsInstance(narcs, list)

        # Test get_all_deliveries
        deliv_resp = self.client.post("/api/get_all_deliveries", json={"args": []})
        self.assertEqual(deliv_resp.status_code, 200)
        delivs = deliv_resp.json()
        self.assertIsInstance(delivs, list)

        # Test get_daily_z_report RPC
        z_resp = self.client.post("/api/get_daily_z_report", json={"args": ["all"]})
        self.assertEqual(z_resp.status_code, 200)
        z_data = z_resp.json()
        self.assertIn("gross_sales", z_data)
        self.assertIn("payment_breakdown", z_data)
        self.assertIn("cash_total", z_data)

    def test_05_direct_rest_endpoints(self):
        """Verify dedicated OpenAPI REST endpoints return valid responses."""
        endpoints = [
            "/api/medicines",
            "/api/prescriptions",
            "/api/deliveries",
            "/api/analytics",
            "/api/settings",
            "/api/zreport",
            "/api/zreports/history"
        ]
        for ep in endpoints:
            resp = self.client.get(ep)
            self.assertEqual(resp.status_code, 200, f"Endpoint {ep} failed")
            self.assertIsNotNone(resp.json())

if __name__ == "__main__":
    unittest.main()
