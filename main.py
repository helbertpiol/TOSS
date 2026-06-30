# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from screens.login import LoginScreen
from screens.dashboard import DashboardScreen
from screens.users import UsersScreen
from screens.profile import ProfileScreen
from screens.settings import SettingsScreen
from screens.register import RegisterScreen
from screens.technical_service_request import TechnicalServiceRequestScreen
from screens.repair_troubleshoot import RepairTroubleshootScreen
from database.db import get_user_by_remember_token
from utils.session import load_remember_token


class TOSSApp(App):

    def build(self):

        Builder.load_file("ui/login.kv")
        Builder.load_file("ui/dashboard.kv")
        Builder.load_file("ui/register.kv")
        Builder.load_file("ui/technical_service_request.kv")
        Builder.load_file("ui/repair_troubleshoot.kv")

        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(TechnicalServiceRequestScreen(name="technical_service_request"))
        sm.add_widget(RepairTroubleshootScreen(name="repair_troubleshoot"))
        # sm.add_widget(UsersScreen(name="users"))
        # sm.add_widget(ProfileScreen(name="profile"))
        # sm.add_widget(SettingsScreen(name="settings"))

        self.current_user = None
        Clock.schedule_once(self.try_auto_login, 0)

        return sm

    def try_auto_login(self, dt):
        token = load_remember_token()
        user = get_user_by_remember_token(token)

        if user:
            self.current_user = user
            self.root.current = "dashboard"


if __name__ == "__main__":
    TOSSApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
