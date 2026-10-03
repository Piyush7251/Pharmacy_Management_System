"""
UI Theme and Color System for Pharmacy Management System Desktop Application.
Matches the 6-layer architecture dark aesthetic with clinical & commerce accents.
"""

COLORS = {
    # Base backgrounds
    "bg_base": "#0B111A",
    "bg_sidebar": "#080D14",
    "bg_surface": "#101924",
    "bg_surface_alt": "#162232",
    "bg_card": "#15202E",
    "bg_input": "#1C2B3E",
    "border": "#24374E",
    "border_light": "#334A68",
    
    # Text
    "text_main": "#FFFFFF",
    "text_muted": "#CBD5E1",
    "text_dim": "#8A9BA8",
    
    # Domain Accent Colors from Architecture
    "clinical": "#10B981",       # Emerald Green
    "clinical_hover": "#059669",
    "inventory": "#F59E0B",      # Amber/Gold
    "inventory_hover": "#D97706",
    "commerce": "#06B6D4",       # Cyan
    "commerce_hover": "#0891B2",
    "operations": "#8B5CF6",     # Purple
    "operations_hover": "#7C3AED",
    
    # Alert / Status colors
    "danger": "#EF4444",         # Red (Allergy / Interaction / Critical alert)
    "warning": "#F59E0B",        # Amber (Expiring soon / low stock)
    "success": "#10B981",        # Green (In stock / Verified)
    "info": "#38BDF8",           # Sky blue
    "schedule_x": "#EC4899",     # Pink/Magenta for Narcotic / Schedule X
    
    # UI Elements
    "btn_primary": "#06B6D4",
    "btn_primary_hover": "#0891B2",
    "btn_secondary": "#1E2E42",
    "btn_secondary_hover": "#2B405B",
    "btn_danger": "#DC2626",
    "btn_danger_hover": "#B91C1C",
    "badge_bg": "#1E293B"
}

FONTS = {
    "h1": ("Segoe UI", 20, "bold"),
    "h2": ("Segoe UI", 16, "bold"),
    "h3": ("Segoe UI", 14, "bold"),
    "body_bold": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 12),
    "small": ("Segoe UI", 10),
    "small_bold": ("Segoe UI", 10, "bold"),
    "mono": ("Consolas", 11),
    "mono_bold": ("Consolas", 12, "bold"),
    "price_large": ("Segoe UI", 22, "bold"),
}
