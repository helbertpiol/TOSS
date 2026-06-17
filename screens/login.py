from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):

    def login(self):

        username = self.ids.txt_username.text
        password = self.ids.txt_password.text

        print(username)
        print(password)