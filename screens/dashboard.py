from kivy.app import App
from kivy.uix.screenmanager import Screen

from database.db import clear_remember_token
from utils.session import clear_remember_token as clear_saved_remember_token


class DashboardScreen(Screen):
    def on_enter(self):
        print("Dashboard Loaded")

    def logout(self):
        app = App.get_running_app()

        if getattr(app, "current_user", None):
            clear_remember_token(app.current_user["userID"])

        clear_saved_remember_token()
        app.current_user = None
        app.root.current = "login"

