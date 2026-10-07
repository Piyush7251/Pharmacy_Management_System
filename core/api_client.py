"""
API Client and Presence Connector for Pharmacy Management System Apps.
Runs completely in the background via non-blocking asynchronous threads to ensure 0ms UI latency.
"""

import threading
import time
import uuid
import socket
from datetime import datetime
from core.db import get_connection

class AppConnector:
    def __init__(self, user_id, user_name, role, app_name):
        self.user_id = user_id
        self.user_name = user_name
        self.role = role
        self.app_name = app_name
        self.session_id = str(uuid.uuid4())[:8]
        self.hostname = socket.gethostname()
        self.is_running = False
        self.heartbeat_thread = None
        self.current_status = "Online"
        self.last_action = f"Launched {app_name}"

    def start(self):
        """Register session and start background heartbeat loop."""
        self.is_running = True
        threading.Thread(target=self._async_register, daemon=True).start()
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()

    def stop(self):
        """Unregister session on window close."""
        self.is_running = False
        threading.Thread(target=self._async_unregister, daemon=True).start()

    def _async_register(self):
        payload = {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "name": self.user_name,
            "role": self.role,
            "terminal_name": self.hostname,
            "ip_address": "127.0.0.1",
            "status": self.current_status,
            "last_action": self.last_action,
            "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_heartbeat": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
            INSERT OR REPLACE INTO active_sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                payload["session_id"], payload["user_id"], payload["name"], payload["role"],
                payload["terminal_name"], payload["ip_address"], payload["status"],
                payload["last_action"], payload["login_time"], payload["last_heartbeat"]
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            pass
            
        self.log_event("Session Connected", f"User logged into {self.app_name} on terminal {self.hostname}")

    def _heartbeat_loop(self):
        while self.is_running:
            time.sleep(5)
            if not self.is_running:
                break
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                UPDATE active_sessions 
                SET last_heartbeat = ?, last_action = ?, status = ?
                WHERE session_id = ?
                """, (now, self.last_action, self.current_status, self.session_id))
                conn.commit()
                conn.close()
            except Exception:
                pass

    def update_action(self, action_text, status="Active"):
        self.last_action = action_text
        self.current_status = status
        threading.Thread(target=self._async_update_action, args=(action_text, status), daemon=True).start()

    def _async_update_action(self, action_text, status):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
            UPDATE active_sessions 
            SET last_heartbeat = ?, last_action = ?, status = ?
            WHERE session_id = ?
            """, (now, action_text, status, self.session_id))
            conn.commit()
            conn.close()
        except Exception:
            pass

    def _async_unregister(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM active_sessions WHERE session_id = ?", (self.session_id,))
            conn.commit()
            conn.close()
        except Exception:
            pass
        self.log_event("Session Disconnected", f"User logged out of {self.app_name}")

    def log_event(self, action, details, level="INFO"):
        threading.Thread(target=self._async_log_event, args=(action, details, level), daemon=True).start()

    def _async_log_event(self, action, details, level):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO audit_logs (timestamp, user_name, role, action, details, level)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (now, self.user_name, self.role, action, details, level))
            conn.commit()
            conn.close()
        except Exception:
            pass
