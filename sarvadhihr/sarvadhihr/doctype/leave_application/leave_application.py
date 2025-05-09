import frappe
from frappe.model.document import Document
from datetime import datetime, date, timedelta

class LeaveApplication(Document):
    def before_insert(self):
        self.status = self.status or "Pending"

    def validate(self):
        self.calculate_total_days()

    def calculate_total_days(self):
        print("callll")
        if self.from_date and self.to_date:
            from_date = self.from_date if isinstance(self.from_date, date) else datetime.strptime(self.from_date, "%Y-%m-%d").date()
            to_date = self.to_date if isinstance(self.to_date, date) else datetime.strptime(self.to_date, "%Y-%m-%d").date()

            # Call get_leave_days to filter weekends and holidays
            leave_data = get_leave_days(from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
            self.total_days = leave_data["total_days"]  # Only count working days
            print(leave_data["total_days"])
            # Ensure child table is updated
            # self.set("leave_details", [])
            # for day in leave_data["leave_days"]:
            #     new_row = self.append("leave_details", {})
            #     new_row.leave_date = day["date"]
            #     new_row.holiday_type = day["holiday_type"]

@frappe.whitelist()
def get_leave_days(from_date, to_date):
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%Y-%m-%d")

    # leave_days = []
    total_days = 0
    current_date = from_date

    while current_date <= to_date:
        holiday_info = frappe.db.get_value(
            "Weekend and Holiday List", 
            {"date": current_date.strftime("%Y-%m-%d")}, 
            ["holiday_name", "is_weekend", "is_public_holiday"], 
            as_dict=True
        )

        # Determine holiday type
        holiday_type = ""
        if holiday_info:
            if holiday_info.get("is_weekend"):
                holiday_type = "Weekend"
            elif holiday_info.get("is_public_holiday"):
                holiday_type = "Public Holiday"

        # Only count working days in total_days
        if not holiday_type:
            total_days += 1

        # leave_days.append({
        #     "date": current_date.strftime("%Y-%m-%d"),
        #     "holiday_type": holiday_type
        # })

        current_date += timedelta(days=1)

    return {
        # "leave_days": leave_days,
        "total_days": total_days
    }
