from kivy.app import App
from kivy.uix.screenmanager import Screen

from database.db import validate_user


class LoginScreen(Screen):

    def login(self):

        username = self.ids.txt_username.text.strip()
        password = self.ids.txt_password.text

        if not username or not password:
            self.ids.lbl_error.text = "Please enter username and password."
            return

        user = validate_user(username, password)

        if user:
            app = App.get_running_app()

            # Save current user
            app.current_user = user

            # Navigate to Dashboard
            app.root.current = "dashboard"
            self.ids.txt_password.text = ""
            self.ids.lbl_error.text = ""
        else:
            self.ids.lbl_error.text = "Invalid username or password."
