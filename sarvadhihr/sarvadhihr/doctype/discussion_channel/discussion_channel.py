# Copyright (c) 2025, shruti and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class DiscussionChannel(Document):
	pass


@frappe.whitelist()
def get_users_by_role(roles):
    if isinstance(roles, str):
        roles = frappe.parse_json(roles)
 
    try:
        user_links = frappe.get_all(
            "Has Role",
            filters={"role": ["in", roles]},
            fields=["parent"]
        )
 
        user_ids = list({u["parent"] for u in user_links})
 
        return frappe.get_all(
            "User",
            filters={"name": ["in", user_ids]},
            fields=["name", "username"]
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Error in get_users_by_role")
        return {"error": "Failed to fetch users by role."}