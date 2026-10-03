"""
API Client and Presence Connector for Pharmacy Management System Apps.
Handles communication with the Central Gateway Server, sends periodic heartbeats,
and logs real-time operational events.
"""

import threading
import time
import uuid
import socket
from datetime import datetime
import requests
from core.db import get_connection

SERVER_URL = "http://127.0.0.1:8000"

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
        self.register_session()
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()
        self.log_event("Session Connected", f"User logged into {self.app_name} on terminal {self.hostname}")

    def stop(self):
        """Unregister session on window close."""
        self.is_running = False
        self.unregister_session()
        self.log_event("Session Disconnected", f"User closed {self.app_name}")

    def register_session(self):
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
            # Try REST API first
            res = requests.post(f"{SERVER_URL}/api/presence/register", json=payload, timeout=1.5)
            if res.status_code == 200:
                return
        except Exception:
            pass
            
        # Fallback to direct DB write
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
            print(f"[Presence Error]: {e}")

    def _heartbeat_loop(self):
        while self.is_running:
            time.sleep(4)
            if not self.is_running:
                break
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            try:
                requests.post(f"{SERVER_URL}/api/presence/heartbeat", json={
                    "session_id": self.session_id,
                    "last_action": self.last_action,
                    "status": self.current_status
                }, timeout=1.5)
            except Exception:
                # Direct DB fallback
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

    def unregister_session(self):
        try:
            requests.post(f"{SERVER_URL}/api/presence/unregister", json={"session_id": self.session_id}, timeout=1.5)
        except Exception:
            pass
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM active_sessions WHERE session_id = ?", (self.session_id,))
            conn.commit()
            conn.close()
        except Exception:
            pass

    def log_event(self, action, details, level="INFO"):
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
        except Exception as e:
            print(f"[Log Error]: {e}")
