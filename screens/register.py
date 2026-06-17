from kivy.app import App
from kivy.uix.screenmanager import Screen

from database.db import register_user, username_exists
from datetime import datetime


class RegisterScreen(Screen):
    def register(self):
        username = self.ids.txt_username.text.strip()
        position = self.ids.txt_position.text.strip()
        role = self.ids.spn_role.text.strip()
        password = self.ids.txt_password.text
        confirm_password = self.ids.txt_confirm_password.text

        if not username or not position or not password or not confirm_password:
            self.ids.lbl_message.text = "Please complete all fields."
            self.ids.lbl_message.color = 1, 0.1, 0.1, 1
            return

        if role == "Select Role":
            self.ids.lbl_message.text = "Please select a user role."
            self.ids.lbl_message.color = 1, 0.1, 0.1, 1
            return

        if password != confirm_password:
            self.ids.lbl_message.text = "Passwords do not match."
            self.ids.lbl_message.color = 1, 0.1, 0.1, 1
            return

        if len(password) < 6:
            self.ids.lbl_message.text = "Password must be at least 6 characters."
            self.ids.lbl_message.color = 1, 0.1, 0.1, 1
            return

        if username_exists(username):
            self.ids.lbl_message.text = "Username already exists."
            self.ids.lbl_message.color = 1, 0.1, 0.1, 1
            return

        created_at = datetime.now().isoformat(timespec="seconds")
        success = register_user(
            username=username,
            password=password,
            role=role,
            position=position,
            rememberToken="",
            createdAt=created_at,
        )

        if success:
            self.clear_form()
            self.ids.lbl_message.text = "User registered successfully."
            self.ids.lbl_message.color = 0.1, 0.55, 0.1, 1
        else:
            self.ids.lbl_message.text = "Registration failed."
            self.ids.lbl_message.color = 1, 0.1, 0.1, 1

    def clear_form(self):
        self.ids.txt_username.text = ""
        self.ids.txt_position.text = ""
        self.ids.spn_role.text = "Select Role"
        self.ids.txt_password.text = ""
        self.ids.txt_confirm_password.text = ""

    def go_back(self):
        app = App.get_running_app()
        if getattr(app, "current_user", None):
            app.root.current = "dashboard"
        else:
            app.root.current = "login"
