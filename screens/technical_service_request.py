import calendar
from datetime import date

from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
#from kivymd.uix.card import MDCard

from database.db import get_departments, get_service_types


class ServiceTypeCard(ButtonBehavior, BoxLayout):
    service_id = NumericProperty(0)
    service_name = StringProperty("")
    service_description = StringProperty("")
    accent_color = ListProperty([0.10, 0.36, 0.72, 1])
    image_source = StringProperty("assets/images/default.png")


class TechnicalServiceRequestScreen(Screen):
    service_type_accents = [
        [0.10, 0.36, 0.72, 1],
        [0.06, 0.55, 0.45, 1],
        [0.90, 0.42, 0.15, 1],
        [0.56, 0.36, 0.74, 1],
        [0.18, 0.50, 0.64, 1],
        [0.42, 0.50, 0.24, 1],
        [0.72, 0.22, 0.32, 1],
    ]

    def on_enter(self):
        if not hasattr(self, "selected_date"):
            self.selected_date = date.today()
            self.ids.btn_service_date.text = self.selected_date.isoformat()

        self.load_departments()
        self.load_service_types()

    def load_departments(self):
        self.department_options = {
            f"{dept['deptCode']} - {dept['deptName']}": dept["deptID"]
            for dept in get_departments()
        }
        self.ids.spn_department.values = list(self.department_options.keys())

    def load_service_types(self):
        container = self.ids.service_type_container
        container.clear_widgets()

        for index, service_type in enumerate(get_service_types()):
            name = service_type["serviceTypeName"]
            card = ServiceTypeCard(
                service_id=service_type["serviceTypeID"],
                service_name=name,
                service_description=self.get_service_description(name),
                image_source=self.get_service_image(name),
                accent_color=self.service_type_accents[
                    index % len(self.service_type_accents)
                ],
            )
            card.bind(on_release=self.open_service_type)
            container.add_widget(card)

    def open_service_type(self, card):
        common_data = self.get_common_service_data()
        if common_data is None:
            return

        if card.service_name.lower().startswith("repair/troubleshoot"):
            self.manager.current = "repair_troubleshoot"
            return

        self.ids.lbl_message.text = f"{card.service_name} module will be added next."

    def get_common_service_data(self):
        selected_department = self.ids.spn_department.text
        requester = self.ids.txt_requester.text.strip()

        if selected_department not in self.department_options:
            self.show_error("Please select a department / agency first.")
            return None

        # if not requester:
        #     self.show_error("Please enter the requester first.")
        #     return None

        self.ids.lbl_message.text = ""
        return {
            #"dtDate": self.ids.btn_service_date.text,
            #"deptID": self.department_options[selected_department],
            "departmentDisplay": selected_department,
            #"strRequester": requester,
            #"strConstructed": self.ids.txt_constructed.text.strip(),
        }

    def open_date_picker(self):
        self.date_year = self.selected_date.year
        self.date_month = self.selected_date.month

        content = GridLayout(cols=1, spacing=8, padding=12)
        self.date_title = Label(size_hint_y=None, height=34, color=(0.1, 0.16, 0.24, 1))

        nav = GridLayout(cols=3, size_hint_y=None, height=42, spacing=8)
        nav.add_widget(Button(text="<", on_release=lambda _button: self.change_month(-1)))
        nav.add_widget(self.date_title)
        nav.add_widget(Button(text=">", on_release=lambda _button: self.change_month(1)))

        self.days_grid = GridLayout(cols=7, spacing=4)
        content.add_widget(nav)
        content.add_widget(self.days_grid)

        self.date_popup = Popup(
            title="Select Date of Service",
            content=content,
            size_hint=(None, None),
            size=(min(420, Window.width * 0.92), 430),
        )
        self.refresh_calendar()
        self.date_popup.open()

    def change_month(self, direction):
        self.date_month += direction
        if self.date_month < 1:
            self.date_month = 12
            self.date_year -= 1
        elif self.date_month > 12:
            self.date_month = 1
            self.date_year += 1

        self.refresh_calendar()

    def refresh_calendar(self):
        self.date_title.text = f"{calendar.month_name[self.date_month]} {self.date_year}"
        self.days_grid.clear_widgets()

        for day_name in ["M", "T", "W", "T", "F", "S", "S"]:
            self.days_grid.add_widget(Label(text=day_name, color=(0.25, 0.3, 0.36, 1)))

        for week in calendar.monthcalendar(self.date_year, self.date_month):
            for day_number in week:
                if day_number == 0:
                    self.days_grid.add_widget(Label(text=""))
                    continue

                button = Button(text=str(day_number))
                button.bind(
                    on_release=lambda _button, selected_day=day_number: self.select_date(selected_day)
                )
                self.days_grid.add_widget(button)

    def select_date(self, selected_day):
        self.selected_date = date(self.date_year, self.date_month, selected_day)
        self.ids.btn_service_date.text = self.selected_date.isoformat()
        self.date_popup.dismiss()

    def show_error(self, message):
        self.ids.lbl_message.color = 1, 0.1, 0.1, 1
        self.ids.lbl_message.text = message

    def get_service_description(self, service_name):
        descriptions = {
            "Repair/Troubleshoot ICT Equipment": "Record ICT equipment repair, troubleshooting, findings, solutions, and SRF status.",
            "Preventive Maintenance": "Schedule and record annual maintenance for computers and ICT equipment.",
            "Network Maintenance": "Track network-wide maintenance, outages, and escalation activities.",
            "ICT Inspection / Installation": "Inspect newly purchased ICT equipment and record installation details.",
            "ICT Equipment Setup for Events": "Record ICT setup support for events, meetings, trainings, and programs.",
            "Software / System Installation": "Track software, system, drivers, and application installation requests.",
            "Printer Sharing": "Record printer sharing setup and troubleshooting services.",
        }

        return descriptions.get(service_name, "Record and track this technical service request.")

    def get_service_image(self, service_name):
        images = {
            "Repair/Troubleshoot ICT Equipment": "assets/images/Repair.png",
            "Preventive Maintenance": "assets/images/Preventive maintenance.png",
            "Network Maintenance": "assets/images/Network maintenance.png",
            #"ICT Inspection / Installation": "",
            #"ICT Equipment Setup for Events": "Record ICT setup support for events, meetings, trainings, and programs.",
            #"Software / System Installation": "Track software, system, drivers, and application installation requests.",
            #"Printer Sharing": "Record printer sharing setup and troubleshooting services.",

        }

        return images.get(service_name,"assets/images/default.png")