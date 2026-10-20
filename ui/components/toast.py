"""
TQM Pharm Enterprise — Dynamic Floating Toast Notification System.
Provides non-blocking, elegant animated alerts (Success, Warning, Danger, Info)
overlayed at the top-right corner of the desktop application.
"""

import customtkinter as ctk
from ui.theme import COLORS, FONTS

class ToastNotification(ctk.CTkFrame):
    def __init__(self, master, title, message, toast_type="success", duration_ms=3500):
        # Choose colors based on toast type
        type_colors = {
            "success": (COLORS["clinical"], COLORS["success_bg"], "✅"),
            "warning": (COLORS["warning"], COLORS["warning_bg"], "⚠️"),
            "danger": (COLORS["danger"], COLORS["danger_bg"], "🚨"),
            "info": (COLORS["commerce"], COLORS["info_bg"], "ℹ️")
        }
        
        accent_color, bg_color, icon = type_colors.get(toast_type, type_colors["info"])
        
        super().__init__(
            master,
            fg_color=COLORS["bg_surface"],
            corner_radius=10,
            border_width=2,
            border_color=accent_color,
            width=360,
            height=70
        )
        self.master = master
        self.duration_ms = duration_ms
        
        self.grid_propagate(False)
        self.grid_columnconfigure(1, weight=1)
        
        # Left Accent Pill / Icon
        lbl_icon = ctk.CTkLabel(self, text=icon, font=("Segoe UI", 20))
        lbl_icon.grid(row=0, column=0, rowspan=2, padx=(12, 8), pady=10)
        
        # Title
        lbl_title = ctk.CTkLabel(
            self,
            text=title,
            font=FONTS["body_bold"],
            text_color=accent_color,
            anchor="w"
        )
        lbl_title.grid(row=0, column=1, sticky="w", padx=(0, 8), pady=(8, 0))
        
        # Message
        lbl_msg = ctk.CTkLabel(
            self,
            text=message,
            font=FONTS["small"],
            text_color=COLORS["text_main"],
            anchor="w",
            wraplength=250,
            justify="left"
        )
        lbl_msg.grid(row=1, column=1, sticky="w", padx=(0, 8), pady=(0, 8))
        
        # Close '✕' Button
        btn_close = ctk.CTkButton(
            self,
            text="✕",
            width=20,
            height=20,
            font=FONTS["small_bold"],
            fg_color="transparent",
            hover_color=COLORS["btn_secondary"],
            text_color=COLORS["text_dim"],
            command=self.dismiss
        )
        btn_close.grid(row=0, column=2, sticky="ne", padx=6, pady=6)
        
        # Show on master window
        self.place(relx=0.985, rely=0.08, anchor="ne")
        self.lift()
        
        # Auto-dismiss timer
        self._dismiss_job = self.after(self.duration_ms, self.dismiss)

    def dismiss(self):
        try:
            if hasattr(self, "_dismiss_job") and self._dismiss_job:
                self.after_cancel(self._dismiss_job)
                self._dismiss_job = None
            self.destroy()
        except Exception:
            pass


def show_toast(master, title, message, toast_type="success", duration_ms=3500):
    """Helper to display a toast notification on any window or widget."""
    try:
        toplevel = master.winfo_toplevel()
        # Dismiss any existing toast first
        for child in toplevel.winfo_children():
            if isinstance(child, ToastNotification):
                child.dismiss()
        return ToastNotification(toplevel, title, message, toast_type, duration_ms)
    except Exception:
        return None
