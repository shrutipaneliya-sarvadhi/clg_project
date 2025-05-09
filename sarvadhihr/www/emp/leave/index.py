import frappe
from datetime import datetime

def get_context(context):
    user_email = frappe.session.user  # Get logged-in user's email

    # Fetch employee details for the logged-in user
    employee = frappe.get_all("Employee",
        filters={"email": user_email},
        fields=["name"]  # Fetch only the employee's unique ID (name)
    )

    if employee:
        employee_name = employee[0]["name"]
        
        # Fetch leave type details
        leave_types = frappe.get_all("Leave Type",
            filters={"parent": employee_name},
            fields=["total_paid_leave", "remaining_paid_leave", "taken_casual_leave", "taken_sick_leave"]
        )

        context.leave_types = leave_types  # Assign the leave type data to context
    else:
        context.leave_types = []  # No employee record found

    # Get current date
    today = datetime.today().strftime('%Y-%m-%d')

    # Fetch upcoming holidays (only holidays after today)
    all_holidays = frappe.get_all("Weekend and Holiday List",
        filters=[["date", ">", today]],
        fields=["holiday_name", "date"],
        order_by="date asc"
    )

    context.holiday_list = all_holidays  # Pass all holidays

    return context
