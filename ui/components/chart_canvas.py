"""
TQM Pharm Enterprise — Dynamic Cold-Chain IoT Telemetry Chart.
Visualizes live 24-hour sensor temperatures against critical clinical thresholds (2-8°C).
"""

import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from ui.theme import COLORS, FONTS

class ColdChainChartCanvas(ctk.CTkFrame):
    def __init__(self, master, logs=None, width=650, height=220):
        super().__init__(master, fg_color="transparent")
        self.width = width
        self.height = height
        self.logs = logs or []
        
        self.setup_ui()
        self.render_chart()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        
        # Header strip with current status
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=4, pady=(2, 6))
        
        self.lbl_title = ctk.CTkLabel(
            top,
            text="❄️ Live Cold-Chain IoT Telemetry (Sensor: SENSOR-FRIDGE-01)",
            font=FONTS["body_bold"],
            text_color=COLORS["text_main"]
        )
        self.lbl_title.pack(side="left")
        
        self.badge_status = ctk.CTkLabel(
            top,
            text=" Optimal (4.2°C) ",
            font=FONTS["small_bold"],
            fg_color=COLORS["success_bg"],
            text_color=COLORS["clinical"],
            corner_radius=6
        )
        self.badge_status.pack(side="right")
        
        # Canvas
        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#E2E8F0"
        )
        self.canvas.pack(fill="both", expand=True, padx=4, pady=2)
        self.canvas.bind("<Configure>", lambda e: self.render_chart())

    def update_logs(self, new_logs):
        self.logs = new_logs
        self.render_chart()

    def render_chart(self):
        self.canvas.delete("all")
        
        w = self.canvas.winfo_width()
        if w < 100:
            w = self.width
        h = self.canvas.winfo_height()
        if h < 100:
            h = self.height
            
        pad_l = 45
        pad_r = 25
        pad_t = 20
        pad_b = 30
        
        plot_w = w - pad_l - pad_r
        plot_h = h - pad_t - pad_b
        
        min_temp = 0.0
        max_temp = 12.0
        
        def y_for_temp(t):
            ratio = (t - min_temp) / (max_temp - min_temp)
            return pad_t + plot_h - (ratio * plot_h)
            
        # 1. Shaded Optimal Band (2°C to 8°C)
        y_8 = y_for_temp(8.0)
        y_2 = y_for_temp(2.0)
        self.canvas.create_rectangle(pad_l, y_8, pad_l + plot_w, y_2, fill="#ECFDF5", outline="")
        self.canvas.create_text(pad_l + 10, (y_8 + y_2) / 2, text="OPTIMAL STORAGE BAND (2°C - 8°C)", fill="#059669", font=("Segoe UI", 9, "bold"), anchor="w")
        
        # 2. Grid lines & Axis labels
        for t in [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]:
            y = y_for_temp(t)
            is_thresh = t in (2.0, 8.0)
            line_col = "#EF4444" if t == 8.0 else ("#3B82F6" if t == 2.0 else "#E2E8F0")
            dash = (4, 2) if is_thresh else ()
            self.canvas.create_line(pad_l, y, pad_l + plot_w, y, fill=line_col, width=1.5 if is_thresh else 1, dash=dash)
            self.canvas.create_text(pad_l - 6, y, text=f"{int(t)}°C", fill="#64748B", font=("Segoe UI", 9), anchor="e")
            
        # 3. Y-Axis and X-Axis lines
        self.canvas.create_line(pad_l, pad_t, pad_l, pad_t + plot_h, fill="#94A3B8", width=1)
        self.canvas.create_line(pad_l, pad_t + plot_h, pad_l + plot_w, pad_t + plot_h, fill="#94A3B8", width=1)
        
        # 4. Plot points
        if not self.logs:
            self.canvas.create_text(w/2, h/2, text="No sensor readings logged yet.", fill="#94A3B8", font=("Segoe UI", 11))
            return
            
        # Logs usually in desc order, reverse for timeline
        readings = list(reversed(self.logs[-14:]))
        if len(readings) == 1:
            readings = readings * 2  # duplicate to draw line
            
        n = len(readings)
        x_step = plot_w / max(1, n - 1)
        
        points = []
        for i, item in enumerate(readings):
            temp_val = float(item["temperature"])
            px = pad_l + i * x_step
            py = y_for_temp(temp_val)
            points.append((px, py, temp_val, item.get("timestamp", "")))
            
        # Draw curve line
        for i in range(len(points) - 1):
            x1, y1, t1, _ = points[i]
            x2, y2, t2, _ = points[i+1]
            seg_col = "#DC2626" if (t1 > 8.0 or t2 > 8.0 or t1 < 2.0 or t2 < 2.0) else "#0D9488"
            self.canvas.create_line(x1, y1, x2, y2, fill=seg_col, width=2.5)
            
        # Draw points
        for i, (px, py, t, ts) in enumerate(points):
            pt_col = "#DC2626" if (t > 8.0 or t < 2.0) else "#0D9488"
            r = 4 if i < len(points)-1 else 6
            self.canvas.create_oval(px - r, py - r, px + r, py + r, fill=pt_col, outline="#FFFFFF", width=1.5)
            
            # X-axis timestamp label every 3rd point or endpoints
            if i % 3 == 0 or i == len(points) - 1:
                t_label = ts.split()[-1][:5] if " " in ts else ts[:5]
                self.canvas.create_text(px, pad_t + plot_h + 12, text=t_label, fill="#64748B", font=("Segoe UI", 8))
                
        # Latest reading callout on rightmost point
        last_px, last_py, last_t, _ = points[-1]
        callout_text = f" {last_t:.1f}°C "
        is_alert = last_t > 8.0 or last_t < 2.0
        bg_col = "#FEE2E2" if is_alert else "#CCFBF1"
        fg_col = "#DC2626" if is_alert else "#0D9488"
        
        self.canvas.create_rectangle(last_px - 22, last_py - 24, last_px + 22, last_py - 6, fill=bg_col, outline=fg_col, width=1)
        self.canvas.create_text(last_px, last_py - 15, text=callout_text, fill=fg_col, font=("Segoe UI", 9, "bold"))
        
        # Update badge status
        if is_alert:
            self.badge_status.configure(
                text=f" 🚨 ALARM: {last_t:.1f}°C EXCEEDED SAFE RANGE! ",
                fg_color=COLORS["danger_bg"],
                text_color=COLORS["danger"]
            )
        else:
            self.badge_status.configure(
                text=f" Optimal: {last_t:.1f}°C (Compliant) ",
                fg_color=COLORS["success_bg"],
                text_color=COLORS["clinical"]
            )
