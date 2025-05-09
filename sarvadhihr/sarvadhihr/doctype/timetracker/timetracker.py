from datetime import datetime
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils.data import now_datetime
import pytz

class Timetracker(WebsiteGenerator):
    def before_insert(self):
        print("before_insert callingggggggggggggggggggggggg")
        if not self.clock_out_time:
            self.clock_out_time = "00:00:00"


    def on_submit(self):
        print("on_submit is being called")

        # Capture the current UTC time when the submit button is clicked using now_datetime
        utc_time = now_datetime()

        print("utc yimeeeeeeeeeeeee:",utc_time)

        # Convert the UTC time to your local timezone (e.g., 'Asia/Kolkata')
        local_tz = pytz.timezone('Asia/Kolkata')  # Replace with your local timezone
        local_time = utc_time.astimezone(local_tz)

        # Assign the converted time to clock_out_time
        self.clock_out_time = local_time.strftime('%H:%M:%S')

        # Log the captured and converted time (optional for debugging)
        print("Captured and converted clock_out_time:", self.clock_out_time)
    
   
    def create_timelog(date, total_hours, tasks):
        new_entry = frappe.get_doc({
            "doctype": "Timetracker",
            "date": date,
            "total_hours": total_hours,
            "tasks": tasks
        })
        new_entry.insert()
        frappe.db.commit()
        return new_entry

   

def calculate_total_hours(clock_in, clock_out):
    """Calculate total hours between clock-in and clock-out times."""
    if not clock_in or not clock_out:
        return 0  # Return 0 if any field is missing

    # Convert string to datetime
    clock_in_dt = datetime.strptime(clock_in, "%H:%M:%S")
    clock_out_dt = datetime.strptime(clock_out, "%H:%M:%S")

    total_hours = (clock_out_dt - clock_in_dt).total_seconds() / 3600  # Convert to hours
    return round(total_hours, 2)


