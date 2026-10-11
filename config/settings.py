"""
Centralized Configuration Manager for Pharmacy Management System.
Handles application settings, store metadata, regulatory compliance bounds,
inventory alert thresholds, receipt formatting, and file persistence via config.json.
"""

import os
import json
import threading
from dataclasses import dataclass, field, asdict
from typing import Dict, Any

# Root directory of the application
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config.json")
BACKUP_DIR_DEFAULT = os.path.join(BASE_DIR, "backups")
LOGS_DIR_DEFAULT = os.path.join(BASE_DIR, "logs")

@dataclass
class StoreConfig:
    """Store profile, physical location, and regulatory drug license details."""
    name: str = "Apex Central Pharmacy"
    branch: str = "Branch #01, Navi Mumbai"
    address: str = "Shop 4-5, Commercial Complex, Sector 15, Navi Mumbai, MH 400614"
    phone: str = "+91 98200 12345"
    email: str = "support@apexpharmacy.com"
    gstin: str = "27AABCS1429B1Z2"
    dl_number: str = "MH-TZ2-441902"
    currency_symbol: str = "₹"

@dataclass
class InventoryConfig:
    """Stock management parameters, reorder thresholds, and temperature limits."""
    low_stock_threshold: int = 20
    expiring_days_threshold: int = 180
    cold_chain_min_temp: float = 2.0
    cold_chain_max_temp: float = 8.0
    default_gst_percent: float = 12.0

@dataclass
class ReceiptConfig:
    """Customer sales invoice print formatting, header, footer, and loyalty policy."""
    header_message: str = "Thank you for choosing Apex Central Pharmacy!"
    footer_message: str = "Prescription medicines cannot be returned without original batch receipt."
    enable_loyalty_points: bool = True
    loyalty_rate: float = 1.0  # 1 point per 100 spent

@dataclass
class SystemConfig:
    """System runtime flags, server endpoints, and storage path locations."""
    db_path: str = os.path.expanduser("~/.aegispharm/pharmacy_system.db")
    log_dir: str = LOGS_DIR_DEFAULT
    backup_dir: str = BACKUP_DIR_DEFAULT
    server_url: str = "http://127.0.0.1:8000"
    auto_refresh_interval_ms: int = 4000
    default_theme: str = "light"
    session_timeout_minutes: int = 60

@dataclass
class AppConfig:
    """Top-level composite configuration container."""
    store: StoreConfig = field(default_factory=StoreConfig)
    inventory: InventoryConfig = field(default_factory=InventoryConfig)
    receipt: ReceiptConfig = field(default_factory=ReceiptConfig)
    system: SystemConfig = field(default_factory=SystemConfig)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration hierarchy to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppConfig":
        """Instantiate configuration from dictionary with safe key fallbacks."""
        return cls(
            store=StoreConfig(**data.get("store", {})),
            inventory=InventoryConfig(**data.get("inventory", {})),
            receipt=ReceiptConfig(**data.get("receipt", {})),
            system=SystemConfig(**data.get("system", {}))
        )

class SettingsManager:
    """
    Thread-safe Singleton manager for loading, persisting, and caching application settings.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SettingsManager, cls).__new__(cls)
                cls._instance._config = None
                cls._instance._file_path = CONFIG_FILE_PATH
                cls._instance._load_or_initialize()
            return cls._instance

    def _load_or_initialize(self):
        """Loads config.json from disk, creating a default one if it doesn't exist."""
        if os.path.exists(self._file_path):
            try:
                with open(self._file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._config = AppConfig.from_dict(data)
                return
            except Exception as e:
                # If corrupted, fallback to clean defaults
                print(f"[SettingsManager] Warning: failed to parse config.json ({e}). Using defaults.")
        
        # Initialize default config and write to file
        self._config = AppConfig()
        self.save()

    def get_config(self) -> AppConfig:
        """Returns the current cached configuration."""
        if self._config is None:
            self._load_or_initialize()
        return self._config

    def save(self) -> bool:
        """Serializes current configuration to config.json."""
        try:
            os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump(self._config.to_dict(), f, indent=4)
            return True
        except Exception as e:
            print(f"[SettingsManager] Error saving config file: {e}")
            return False

    def update_from_dict(self, updates: Dict[str, Any]) -> bool:
        """
        Merges dictionary updates into the configuration model and persists to disk.
        """
        with self._lock:
            current = self._config.to_dict()
            for section, values in updates.items():
                if section in current and isinstance(values, dict):
                    current[section].update(values)
                else:
                    current[section] = values
            try:
                self._config = AppConfig.from_dict(current)
                return self.save()
            except Exception as e:
                print(f"[SettingsManager] Error updating settings: {e}")
                return False

    def reset_defaults(self) -> AppConfig:
        """Resets configuration back to out-of-the-box defaults and writes to disk."""
        with self._lock:
            self._config = AppConfig()
            self.save()
            return self._config

# Global convenience helper accessors
def get_settings() -> AppConfig:
    """Retrieve global cached AppConfig instance."""
    return SettingsManager().get_config()

def save_settings(data: Dict[str, Any]) -> bool:
    """Update and persist settings using a section dictionary."""
    return SettingsManager().update_from_dict(data)

def reload_settings() -> AppConfig:
    """Force reload settings from disk."""
    manager = SettingsManager()
    manager._load_or_initialize()
    return manager.get_config()

def reset_to_defaults() -> AppConfig:
    """Restore all settings to original defaults."""
    return SettingsManager().reset_defaults()
