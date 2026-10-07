"""
AegisPharm Enterprise — Application Entry Point.
Executes the unified Pharmacy desktop application with Login & Role-based Dashboard.
"""

from app import PharmacyApplication

if __name__ == "__main__":
    app = PharmacyApplication()
    app.mainloop()
