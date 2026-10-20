"""
Centralized Activity & Audit Logging Service for Pharmacy Management System.
Maintains persistent audit logs both in SQLite database (audit_logs table) and
in physical disk files (logs/activity.log). Records all user interactions,
security events, financial transactions, clinical approvals, and stock changes.
"""

import os
import csv
import logging
import threading
import shutil
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from config.settings import get_settings
from core.db import get_connection, DB_PATH

# Initialize logs directory
_cfg = get_settings()
LOG_DIR = os.path.abspath(_cfg.system.log_dir)
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "activity.log")

# Setup Python logging facility
_file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
_file_formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
_file_handler.setFormatter(_file_formatter)

_logger = logging.getLogger("TQM Pharm")
_logger.setLevel(logging.INFO)
if not _logger.handlers:
    _logger.addHandler(_file_handler)

def log_activity(
    action: str,
    details: str,
    user_name: str = "System",
    role: str = "System",
    level: str = "INFO"
) -> None:
    """
    Records an activity event to both the disk file and the SQLite database.
    Runs asynchronously in a background thread to prevent UI micro-stutters.
    
    Args:
        action (str): Short summary of the action (e.g. 'Invoice Created', 'Stock Adjusted').
        details (str): Detailed metadata or contextual information.
        user_name (str): The name of the user performing the action.
        role (str): The user's role (e.g. 'Store Admin', 'Pharmacist', 'Cashier').
        level (str): Log level: 'INFO', 'WARN', or 'CRITICAL'.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Write to standard logger immediately
    log_msg = f"[{user_name} ({role})] {action} — {details}"
    if level.upper() == "CRITICAL":
        _logger.critical(log_msg)
    elif level.upper() == "WARN" or level.upper() == "WARNING":
        _logger.warning(log_msg)
    else:
        _logger.info(log_msg)

    # 2. Write to SQLite audit_logs in daemon background thread
    def _db_insert():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO audit_logs (timestamp, user_name, role, action, details, level)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, user_name, role, action, details, level.upper()))
            conn.commit()
            conn.close()
        except Exception as e:
            _logger.error(f"Failed to record audit log to SQLite: {e}")

    threading.Thread(target=_db_insert, daemon=True).start()

def get_activity_logs(
    limit: int = 50,
    level: str = "ALL",
    search: str = ""
) -> List[Dict[str, Any]]:
    """
    Fetches historical activity logs from SQLite with optional filtering.
    
    Args:
        limit (int): Maximum number of rows to retrieve.
        level (str): Level filter ('ALL', 'INFO', 'WARN', 'CRITICAL').
        search (str): Optional search query for user, role, action, or details.
        
    Returns:
        List[Dict[str, Any]]: List of audit log records ordered from newest to oldest.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        query = "SELECT * FROM audit_logs"
        params = []
        conditions = []
        
        if level != "ALL":
            conditions.append("level = ?")
            params.append(level.upper())
            
        if search:
            s_param = f"%{search.strip().lower()}%"
            conditions.append("(LOWER(user_name) LIKE ? OR LOWER(action) LIKE ? OR LOWER(details) LIKE ? OR LOWER(role) LIKE ?)")
            params.extend([s_param, s_param, s_param, s_param])
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        
        cur.execute(query, tuple(params))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        _logger.error(f"Error reading activity logs from DB: {e}")
        return []

def export_activity_logs_to_csv(target_path: str) -> Tuple[bool, str]:
    """
    Exports all activity logs to a clean CSV report.
    
    Args:
        target_path (str): File system path to write the CSV to.
        
    Returns:
        Tuple[bool, str]: Success boolean and status message.
    """
    try:
        logs = get_activity_logs(limit=5000, level="ALL")
        if not logs:
            return False, "No activity logs available to export."
            
        fields = ["id", "timestamp", "user_name", "role", "action", "details", "level"]
        with open(target_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(logs)
            
        return True, f"Successfully exported {len(logs)} activity records to {target_path}"
    except Exception as e:
        return False, f"Failed to export activity logs: {str(e)}"

def backup_sqlite_database(custom_backup_dir: Optional[str] = None) -> Tuple[bool, str]:
    """
    Creates a timestamped snapshot of the central SQLite database.
    
    Args:
        custom_backup_dir (Optional[str]): Target directory to place the backup.
        
    Returns:
        Tuple[bool, str]: Success status and file path or error message.
    """
    try:
        cfg = get_settings()
        backup_folder = custom_backup_dir or os.path.abspath(cfg.system.backup_dir)
        os.makedirs(backup_folder, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"pharmacy_backup_{timestamp}.db"
        dest_path = os.path.join(backup_folder, backup_filename)
        
        # Copy active database file
        shutil.copy2(DB_PATH, dest_path)
        
        # Log this administrative action
        log_activity(
            action="Database Backup Created",
            details=f"Backup snapshot created at {dest_path}",
            user_name="Store Admin",
            role="Store Admin",
            level="INFO"
        )
        return True, dest_path
    except Exception as e:
        return False, f"Database backup failed: {str(e)}"
