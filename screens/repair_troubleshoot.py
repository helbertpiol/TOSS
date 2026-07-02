from kivy.app import App
from kivy.uix.screenmanager import Screen

from database.db import (
    get_equipment_services,
    get_statuses,
    save_repair_troubleshoot_record,
)


REPAIR_SERVICE_TYPE_ID = 1


class RepairTroubleshootScreen(Screen):
    def on_enter(self):
        self.equipment_options = {}
        self.status_options = {}

        self.load_equipment_services()
        self.load_statuses()

    def load_equipment_services(self):
        self.equipment_options = {
            service["esName"]: service for service in get_equipment_services(REPAIR_SERVICE_TYPE_ID)
        }
        self.ids.spn_equipment.values = list(self.equipment_options.keys())

    def load_statuses(self):
        self.status_options = {
            status["statusName"]: status["statusID"]
            for status in get_statuses(REPAIR_SERVICE_TYPE_ID)
        }
        self.ids.spn_status.values = list(self.status_options.keys())

    def save_repair_record(self):
        app = App.get_running_app()
        user = getattr(app, "current_user", None)
        selected_equipment = self.ids.spn_equipment.text
        common_screen = self.manager.get_screen("technical_service_request")
        common_data = common_screen.get_common_service_data()

        if not user:
            self.show_error("Please login again before saving.")
            return

        if common_data is None:
            self.show_error("Please complete the service details on the previous screen.")
            return

        if selected_equipment not in self.equipment_options:
            self.show_error("Please select equipment / service item.")
            return

        unit_qty_text = self.ids.txt_unit_qty.text.strip()
        if not unit_qty_text.isdigit() or int(unit_qty_text) < 1:
            self.show_error("Unit quantity must be a positive number.")
            return

        equipment = self.equipment_options[selected_equipment]
        srf_id = self.ids.txt_srf_id.text.strip()

        if self.ids.chk_with_srf.active and not srf_id:
            self.show_error("Please enter the SRF ID.")
            return

        accomplishment = {
            "deptID": common_data["deptID"],
            "userID": user["userID"],
            "strRequester": common_data["strRequester"],
            "serviceID": equipment["serviceID"],
            "serviceTypeID": equipment["serviceTypeID"],
            "esID": equipment["esID"],
            "strConstructed": common_data["strConstructed"],
            "dtDate": common_data["dtDate"],
            "unitQty": int(unit_qty_text),
            "unitUom": self.ids.spn_unit_uom.text,
            "requestDetails": self.ids.txt_problem.text.strip(),
        }
        repair = {
            "strFindings": self.ids.txt_findings.text.strip(),
            "strSolution": self.ids.txt_solution.text.strip(),
            "strRemarks": self.ids.txt_remarks.text.strip(),
            "srfID": int(srf_id) if srf_id.isdigit() else None,
        }

        try:
            acc_id = save_repair_troubleshoot_record(accomplishment, repair)
        except Exception as error:
            self.show_error(f"Save failed: {error}")
            return

        self.clear_form()
        self.ids.lbl_message.color = 0.1, 0.55, 0.1, 1
        self.ids.lbl_message.text = f"Repair record saved. Accomplishment ID: {acc_id}"

    def clear_form(self):
        self.ids.spn_equipment.text = "Select equipment / service"
        self.ids.spn_status.text = "Select result"
        self.ids.txt_unit_qty.text = "1"
        self.ids.spn_unit_uom.text = "unit"
        self.ids.chk_with_srf.active = False
        self.ids.txt_srf_id.text = ""
        self.ids.txt_problem.text = ""
        self.ids.txt_findings.text = ""
        self.ids.txt_solution.text = ""
        self.ids.txt_remarks.text = ""

    def show_error(self, message):
        self.ids.lbl_message.color = 1, 0.1, 0.1, 1
        self.ids.lbl_message.text = message
