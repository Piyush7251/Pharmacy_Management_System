"""
TQM Pharm Enterprise — Modern Web Application Server.
Powered by FastAPI & High-Performance Uvicorn Asynchronous Engine.
Provides complete multi-role web access (Store Admin, Clinical Pharmacist, Cashier POS,
Inventory & FEFO Manager, Delivery Rider) identical to the desktop application experience.
"""

import os
import sys
import secrets
from datetime import datetime
from typing import Dict, Any, List, Optional
import webbrowser

# Ensure application root directory is on Python path
if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, Request, HTTPException, Header, Response, status
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.db import init_db
from core.bridge import PharmacyBridge
from config.settings import get_settings
from core.logger import log_activity

# Initialize SQLite database on server startup
init_db()

# Load central configuration
cfg = get_settings()

app = FastAPI(
    title=f"{cfg.store.name} — TQM Pharm Enterprise Web",
    description="Next-Generation Enterprise Pharmacy Management Web System & CDSS API.",
    version="2.5",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for local network and mobile terminal access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory Active Web Sessions Store: token -> {"user": user, "bridge": PharmacyBridge, "last_active": datetime}
ACTIVE_SESSIONS: Dict[str, Dict[str, Any]] = {}
DEFAULT_BRIDGE = PharmacyBridge()


class RPCRequest(BaseModel):
    args: Optional[List[Any]] = []


def resolve_bridge_and_user(session_token: Optional[str]):
    """Resolve the active PharmacyBridge instance and user profile for an incoming web request."""
    if session_token and session_token in ACTIVE_SESSIONS:
        session = ACTIVE_SESSIONS[session_token]
        session["last_active"] = datetime.now()
        return session["bridge"], session["user"]
    return DEFAULT_BRIDGE, None


# =========================================================================
# WEB FRONTEND ROUTES
# =========================================================================

@app.get("/", response_class=FileResponse, tags=["Web Application"])
async def serve_web_app():
    """Serve the complete, reactive TQM Pharm web application interface."""
    web_file = os.path.join(BASE_DIR, "ui", "web", "index.html")
    if not os.path.exists(web_file):
        web_file = os.path.join(BASE_DIR, "ui", "desktop", "index.html")
    if not os.path.exists(web_file):
        raise HTTPException(status_code=404, detail="Web application interface file not found.")
    return FileResponse(web_file, media_type="text/html")


@app.get("/health", tags=["System Health"])
async def health_check():
    """Uptime health check and system diagnostic status."""
    return {
        "status": "online",
        "system": "TQM Pharm Enterprise",
        "edition": "Web & Cloud Platform",
        "version": "2.5",
        "store": cfg.store.name,
        "branch": cfg.store.branch,
        "active_web_sessions": len(ACTIVE_SESSIONS),
        "timestamp": datetime.now().isoformat()
    }


# =========================================================================
# UNIVERSAL RPC DISPATCHER (100% PARITY WITH DESKTOP BRIDGE)
# =========================================================================

@app.post("/api/{method}", tags=["Universal RPC Bridge"])
async def dispatch_rpc_method(
    method: str,
    rpc_body: RPCRequest,
    x_session_token: Optional[str] = Header(None)
):
    """
    Universal REST RPC dispatcher matching all 38 methods exposed by the Python desktop bridge.
    Allows the browser interface to run with zero lag, identical to the desktop app.
    """
    args = rpc_body.args or []
    bridge, user = resolve_bridge_and_user(x_session_token)

    # 1. Specialized handling for authentication & session tokens
    if method == "login":
        if len(args) < 2:
            return {"success": False, "error": "Username and password required."}
        username, password = str(args[0]), str(args[1])
        
        # Instantiate dedicated bridge for new session
        new_bridge = PharmacyBridge()
        login_res = new_bridge.login(username, password)
        if login_res.get("success") and "user" in login_res:
            token = secrets.token_hex(24)
            ACTIVE_SESSIONS[token] = {
                "user": login_res["user"],
                "bridge": new_bridge,
                "created_at": datetime.now(),
                "last_active": datetime.now()
            }
            login_res["token"] = token
            log_activity(
                action="Web Session Started",
                details=f"User {login_res['user']['name']} ({login_res['user']['role']}) opened web session.",
                user_name=login_res["user"]["name"],
                role=login_res["user"]["role"],
                level="INFO"
            )
        return login_res

    elif method == "logout":
        if x_session_token and x_session_token in ACTIVE_SESSIONS:
            sess = ACTIVE_SESSIONS.pop(x_session_token)
            sess["bridge"].logout()
        return {"success": True}

    elif method == "get_current_user":
        return user

    # 2. Universal method invocation on active bridge
    if not hasattr(bridge, method):
        raise HTTPException(
            status_code=404,
            detail=f"Requested bridge method '{method}' does not exist on TQM Pharm backend."
        )

    target_func = getattr(bridge, method)
    if not callable(target_func) or method.startswith("_"):
        raise HTTPException(
            status_code=403,
            detail=f"Access to private method '{method}' is forbidden."
        )

    try:
        # Execute backend bridge method
        result = target_func(*args)
        return result
    except Exception as exc:
        log_activity(
            action="RPC Error",
            details=f"Exception during /api/{method}: {str(exc)}",
            user_name=user.get("name", "Web Client") if user else "Web Client",
            role=user.get("role", "Guest") if user else "Guest",
            level="WARN"
        )
        return {"success": False, "error": str(exc)}


# =========================================================================
# DEDICATED REST DOCUMENTATION ENDPOINTS
# =========================================================================

@app.get("/api/medicines", tags=["Medicines & Catalog"])
async def list_medicines():
    """Retrieve full medicine catalog with real-time stock levels and batch expiry."""
    return DEFAULT_BRIDGE.get_all_medicines()


@app.get("/api/prescriptions", tags=["Clinical Prescriptions"])
async def list_prescriptions():
    """Retrieve all digital e-prescriptions and clinical review status."""
    return DEFAULT_BRIDGE.get_all_prescriptions()


@app.get("/api/deliveries", tags=["Logistics & Fleet"])
async def list_deliveries():
    """Retrieve active home delivery dispatch orders and e-POD tracking."""
    return DEFAULT_BRIDGE.get_all_deliveries()


@app.get("/api/analytics", tags=["Executive Analytics"])
async def get_analytics():
    """Retrieve gross sales, GST liability, catalog metrics, and financial breakdown."""
    return DEFAULT_BRIDGE.get_dashboard_analytics()


@app.get("/api/settings", tags=["System Configuration"])
async def get_system_settings():
    """Retrieve current pharmacy settings, branch details, and tax parameters."""
    return DEFAULT_BRIDGE.get_settings()


@app.get("/api/zreport", tags=["Financial Z-Report"])
async def get_z_report(target_date: Optional[str] = None):
    """Compile End-of-Day Z-Report financial reconciliation and payment breakdown."""
    return DEFAULT_BRIDGE.get_daily_z_report(target_date)


@app.get("/api/zreports/history", tags=["Financial Z-Report"])
async def get_z_reports_history(limit: int = 50):
    """Retrieve history of closed end-of-day Z-Reports."""
    return DEFAULT_BRIDGE.get_z_reports_history(limit)


# =========================================================================
# APPLICATION SERVER LAUNCHER
# =========================================================================

def run_web_server(host: str = "127.0.0.1", port: int = 8000, auto_open: bool = True):
    """Launch the modern TQM Pharm web application server with Uvicorn."""
    import uvicorn
    import sys

    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    server_url = f"http://{host}:{port}"
    print("\n" + "=" * 68)
    print("  [TQM Pharm Enterprise] Web Application Server Online")
    print(f"  Web Browser Access:   {server_url}")
    print(f"  API Documentation:    {server_url}/docs")
    print(f"  Store Location:       {cfg.store.name} ({cfg.store.branch})")
    print("=" * 68 + "\n")

    if auto_open:
        try:
            webbrowser.open(server_url)
        except Exception:
            pass

    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    auto_open = "--no-browser" not in sys.argv
    run_web_server(auto_open=auto_open)
