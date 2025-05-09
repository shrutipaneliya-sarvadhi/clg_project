import frappe
from datetime import datetime

def get_context(context):
    today = datetime.today().strftime('%Y-%m-%d')

    # Fetch all holidays (after today)
    all_holidays = frappe.get_all("Weekend and Holiday List",
        filters=[["date", ">", today]],
        fields=["holiday_name", "date"],
        order_by="date asc"
    )

    context.holiday_list = all_holidays  # Pass all holidays

    return context
