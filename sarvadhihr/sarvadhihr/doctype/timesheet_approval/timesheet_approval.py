# Copyright (c) 2025, sarvadhi and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class Timesheet_approval(Document):
	@frappe.whitelist()
	def get_pending_timesheets():
		return frappe.db.get_list(
			"Timesheet",  
			filters={"status": "Pending"},  
			fields=["name"]
		)
	def on_update(self):
		if self.employee_timesheet and self.status in ["Confirmed", "Reject"]:
			frappe.db.set_value("Timesheet", self.employee_timesheet, "status", self.status)
			frappe.db.commit()  # Save changes in the database
