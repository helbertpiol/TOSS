from kivy.app import App
from kivy.uix.screenmanager import Screen

from database.db import create_remember_token, validate_user
from utils.session import save_remember_token


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

            if self.ids.chk_remember.active:
                token = create_remember_token(user["userID"])
                save_remember_token(token)

            # Navigate to Dashboard
            app.root.current = "dashboard"
            self.ids.txt_username.text = ""
            self.ids.txt_password.text = ""
            self.ids.lbl_error.text = ""
            self.ids.chk_remember.active = False
        else:
            self.ids.lbl_error.text = "Invalid username or password."
