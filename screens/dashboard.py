from kivy.app import App
from kivy.properties import ListProperty, StringProperty
from kivy.uix.screenmanager import Screen

from database.db import clear_remember_token
from utils.session import clear_remember_token as clear_saved_remember_token


class DashboardScreen(Screen):
    display_name = StringProperty("User")
    current_year = StringProperty("")
    total_services = StringProperty("0")
    services = ListProperty([])

    def on_enter(self):
        app = App.get_running_app()
        user = getattr(app, "current_user", None)

        if user:
            self.display_name = user.get("userFullname") or user.get("userName") or "User"

        from datetime import datetime

        self.current_year = str(datetime.now().year)
        self.services = [
            {"name": "Technical Repair with SRF", "total": "0", "accent": (0.10, 0.36, 0.72, 1)},
            {"name": "Technical Repair", "total": "0", "accent": (0.06, 0.55, 0.45, 1)},
            {"name": "Preventive Maintenance", "total": "0", "accent": (0.56, 0.36, 0.74, 1)},
            {"name": "Network Troubleshooting", "total": "0", "accent": (0.90, 0.42, 0.15, 1)},
            {"name": "Network Maintenance", "total": "0", "accent": (0.18, 0.50, 0.64, 1)},
            {"name": "Telephone & CCTV Repairs", "total": "0", "accent": (0.72, 0.22, 0.32, 1)},
            {"name": "ICT Inspection & Installation", "total": "0", "accent": (0.42, 0.50, 0.24, 1)},
            {"name": "Other Services", "total": "0", "accent": (0.44, 0.44, 0.50, 1)},
            {"name": "Software Installation", "total": "0", "accent": (0.18, 0.58, 0.82, 1)},
        ]
        self.total_services = str(sum(int(service["total"]) for service in self.services))

    def logout(self):
        app = App.get_running_app()

        if getattr(app, "current_user", None):
            clear_remember_token(app.current_user["userID"])

        clear_saved_remember_token()
        app.current_user = None
        app.root.current = "login"

