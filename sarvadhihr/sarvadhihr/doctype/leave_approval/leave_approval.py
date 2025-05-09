# Copyright (c) 2025, sarvadhi and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class LeaveApproval(Document):
# 	pass

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class LeaveApproval(Document):
    def validate(self):
        self.update_leave_application_status_and_balance()

    def update_leave_application_status_and_balance(self):
        if self.leave_application:
            # Fetch the linked Leave Application
            leave_app_doc = frappe.get_doc("Leave Application", self.leave_application)

            # Update status based on this document's status
            if self.status == "Approved":
                leave_app_doc.status = "Approved"
                leave_app_doc.approved_by = self.approved_by
                leave_app_doc.approval_date = nowdate()

                # Adjust leave balances
                self.adjust_leave_balances(leave_app_doc)

                # Send email to employee on approval
                self.send_email_to_employee(leave_app_doc.employee, "Leave Application Approved", leave_app_doc)

            elif self.status == "Rejected":
                leave_app_doc.status = "Rejected"
                leave_app_doc.approved_by = self.approved_by
                leave_app_doc.approval_date = nowdate()

                # Send email to employee on rejection
                self.send_email_to_employee(leave_app_doc.employee, "Leave Application Rejected", leave_app_doc)

            # Save the Leave Application changes
            leave_app_doc.save()
            frappe.db.commit()

    def adjust_leave_balances(self, leave_app_doc):
        total_days = (leave_app_doc.to_date - leave_app_doc.from_date).days + 1
        leave_type = leave_app_doc.leave_type

        # Fetch the Employee document
        employee_doc = frappe.get_doc("Employee", leave_app_doc.employee)

        # Update the corresponding leave balances in the child table
        for row in employee_doc.leave_type:
            if leave_type == "Paid Leave":
                if row.remaining_paid_leave >= total_days:
                    row.remaining_paid_leave -= total_days
                else:
                    frappe.throw("Insufficient Paid Leave balance.")
            elif leave_type == "Sick Leave":
                row.taken_sick_leave += total_days
            elif leave_type == "Casual Leave":
                row.taken_casual_leave += total_days

        # Save the employee document to persist the changes
        employee_doc.save()
        frappe.db.commit()

    def send_email_to_employee(self, employee, subject, leave_app_doc):
        employee_doc = frappe.get_doc("Employee", employee)

        # Construct the full name
        employee_name = f"{employee_doc.first_name} {employee_doc.last_name}"

        # Send an email to the employee using frappe.sendmail
        frappe.sendmail(
            recipients=[employee_doc.email],
            subject=subject,
            message=f"Dear {employee_name},\n\nYour leave application for {leave_app_doc.leave_type} from {leave_app_doc.from_date} to {leave_app_doc.to_date} has been {leave_app_doc.status}.\n\nBest Regards,\nHR Team"
        )
        frappe.enqueue("frappe.email.queue.flush")
        frappe.msgprint(f"Email sent to {employee_name} ({employee_doc.email})")
