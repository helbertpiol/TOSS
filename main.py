# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from screens.login import LoginScreen
from screens.dashboard import DashboardScreen
from screens.users import UsersScreen
from screens.profile import ProfileScreen
from screens.settings import SettingsScreen


class TOSSApp(App):

    def build(self):

        Builder.load_file("ui/login.kv")
        Builder.load_file("ui/dashboard.kv")

        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        # sm.add_widget(UsersScreen(name="users"))
        # sm.add_widget(ProfileScreen(name="profile"))
        # sm.add_widget(SettingsScreen(name="settings"))

        return sm


if __name__ == "__main__":
    TOSSApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
