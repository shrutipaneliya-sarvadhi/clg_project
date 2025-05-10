# Copyright (c) 2025, shruti and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Announcements(Document):
	def before_save(self):
		self.created_by = self.owner
