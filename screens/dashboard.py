from kivy.uix.screenmanager import Screen


class DashboardScreen(Screen):
    def on_enter(self):
        print("Dashboard Loaded")

