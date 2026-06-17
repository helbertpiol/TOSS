from kivy.app import App
from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):

    def login(self):

        username = self.ids.txt_username.text
        password = self.ids.txt_password.text

        # Temporary authentication
        if username == "admin" and password == "1234":

            app = App.get_running_app()

            # Save current user
            app.current_user = username

            # Navigate to Dashboard
            app.root.current = "dashboard"

        else:

            print("Invalid Username or Password")