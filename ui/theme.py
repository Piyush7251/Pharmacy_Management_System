"""
UI Theme and Color System for Pharmacy Management System Desktop Application.
Supports dual-theme (Clean White Light Mode by default, and Sleek Dark Mode).
All color tokens are defined as (LightMode, DarkMode) tuples for instantaneous CustomTkinter theme switching.
"""

COLORS = {
    # Base backgrounds: (Light, Dark)
    "bg_base": ("#F8FAFC", "#0B111A"),
    "bg_sidebar": ("#FFFFFF", "#080D14"),
    "bg_surface": ("#FFFFFF", "#101924"),
    "bg_surface_alt": ("#F1F5F9", "#162232"),
    "bg_card": ("#FFFFFF", "#15202E"),
    "bg_card_alt": ("#F8FAFC", "#1A283B"),
    "bg_input": ("#F8FAFC", "#1C2B3E"),
    
    # Borders: (Light, Dark)
    "border": ("#E2E8F0", "#24374E"),
    "border_light": ("#CBD5E1", "#334A68"),
    
    # Text colors: (Light, Dark)
    "text_main": ("#0F172A", "#FFFFFF"),
    "text_muted": ("#475569", "#CBD5E1"),
    "text_dim": ("#64748B", "#8A9BA8"),
    "text_inverse": ("#FFFFFF", "#0F172A"),
    
    # Domain Accent Colors: (Light, Dark)
    "clinical": ("#0D9488", "#10B981"),         # Emerald / Teal
    "clinical_hover": ("#0F766E", "#059669"),
    "inventory": ("#D97706", "#F59E0B"),        # Warm Amber
    "inventory_hover": ("#B45309", "#D97706"),
    "commerce": ("#0284C7", "#06B6D4"),         # Cyan / Sky
    "commerce_hover": ("#0369A1", "#0891B2"),
    "operations": ("#7C3AED", "#8B5CF6"),       # Purple
    "operations_hover": ("#6D28D9", "#7C3AED"),
    "admin": ("#D97706", "#FBBF24"),            # Gold / Amber
    
    # Alert / Status colors: (Light, Dark)
    "danger": ("#DC2626", "#EF4444"),           # Red
    "danger_bg": ("#FEE2E2", "#3B1219"),
    "warning": ("#D97706", "#F59E0B"),          # Amber
    "warning_bg": ("#FEF3C7", "#3D270B"),
    "success": ("#0D9488", "#10B981"),          # Green
    "success_bg": ("#CCFBF1", "#0F291E"),
    "info": ("#0284C7", "#38BDF8"),             # Sky Blue
    "info_bg": ("#E0F2FE", "#0C2740"),
    "schedule_x": ("#DB2777", "#EC4899"),       # Pink/Magenta
    "schedule_x_bg": ("#FCE7F3", "#3B1028"),
    
    # UI Buttons & Interactive Badges: (Light, Dark)
    "btn_primary": ("#0284C7", "#06B6D4"),
    "btn_primary_hover": ("#0369A1", "#0891B2"),
    "btn_secondary": ("#E2E8F0", "#1E2E42"),
    "btn_secondary_hover": ("#CBD5E1", "#2B405B"),
    "btn_secondary_text": ("#1E293B", "#F1F5F9"),
    "btn_danger": ("#DC2626", "#DC2626"),
    "btn_danger_hover": ("#B91C1C", "#B91C1C"),
    "badge_bg": ("#F1F5F9", "#1E293B"),
    "badge_text": ("#334155", "#E2E8F0")
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
