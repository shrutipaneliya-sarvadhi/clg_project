from datetime import datetime
import traceback
import frappe
from frappe import whitelist
import frappe.sessions

@frappe.whitelist(allow_guest=True)
def timelog():
    print("timelog callingggggggggg")
    print(f"Form data received: {frappe.form_dict}")

    # Fetch data from form_dict
    project = frappe.form_dict.get("project")
    job = frappe.form_dict.get("job")
    todo = frappe.form_dict.get("todo")
    company_name = frappe.form_dict.get("company_name")
    status = frappe.form_dict.get("status")
    time = frappe.form_dict.get("time")
    date=frappe.form_dict.get("date")
    formattedtotaltime=frappe.form_dict.get("formattedtotaltime")


    print(f"project: {project}, job: {job}, todo: {todo}, company_name: {company_name}, status: {status},time:{time},date:{date},formattedtotaltime:{formattedtotaltime}")

    # Check if any of the required fields are missing
    if not project or not job or not todo or not company_name or not status:
        return {"message": "All fields are required. Please fill out the form completely.", "status": "error"}

    try:
        # Let ERPNext handle name generation automatically (skip manual assignment)
        timelog_application = frappe.get_doc({
            "doctype": "Timelogs",
            "project": project,
            "job": job,
            "todo": todo,
            "company_name": company_name,
            "status": status,
            "time":time,
            "date":date,
            "formattedtotaltime":formattedtotaltime,
            "owner": frappe.session.user,

        })

        print("timeloggggg:", timelog_application)

        # Insert and commit, let ERPNext handle name uniqueness
        timelog_application.insert(ignore_permissions=True)
        frappe.db.commit()

        print("timelog saved:", timelog_application.name)
        return {"message": "Timelog application submitted successfully", "redirect": "/timetracker", "status": "success"}

    except Exception as e:
        # Log the full traceback
        print(f"Error saving timelog: {e}")
        print(traceback.format_exc())  # Log the full traceback to identify the issue
        frappe.log_error(f"Error saving timelog: {traceback.format_exc()}", "Timelog Creation")
        return {"message": f"Error submitting timelog application: {str(e)}", "status": "error"}

    

@frappe.whitelist(allow_guest=True)
def timesheet():
    print("timesheet callingggggggggg")
    print(f"Form data received: {frappe.form_dict}")

    # Fetch data from form_dict
    employee = frappe.form_dict.get("employee")
    date = frappe.form_dict.get("date")
    clock_in_time = frappe.form_dict.get("clock_in_time")
    clock_out_time = frappe.form_dict.get("clock_out_time")
    total_hours = frappe.form_dict.get("total_hours")
    status = frappe.form_dict.get("status")

    # Convert total_hours to decimal float
    total_hours_decimal = float(convert_to_decimal_hours(total_hours))
    print(f"DEBUG - Converted total_hours to decimal (float): {total_hours_decimal}")  # Debugging


    print(f"employee: {employee}, date: {date}, clock_in: {clock_in_time}, clock_out: {clock_out_time}, total_hours: {total_hours_decimal}, status: {status}")

    # Check if any of the required fields are missing
    if not employee or not date or not clock_in_time or not clock_out_time or not total_hours or not status:
        return {"message": "All fields are required. Please fill out the form completely.", "status": "error"}

    try:

        # Let ERPNext handle name generation automatically (skip manual assignment)
        timesheet_entry = frappe.get_doc({
            "doctype": "Timesheet",
            "employee": employee,
            "date": date,
            "clock_in_time": clock_in_time,
            "clock_out_time": clock_out_time,
            "total_hours": total_hours_decimal,
            "status": status,
        })
        print("timesheetgggg:", timesheet_entry)

        # Insert and commit, let ERPNext handle name uniqueness
        timesheet_entry.insert(ignore_permissions=True)
        frappe.db.commit()

        print("timesheet saved:", timesheet_entry.name)
        return {"message": "Timesheet entry submitted successfully", "redirect": "/timetracker/timesheet/index.html", "status": "success"}

    except Exception as e:
        # Log the full traceback
        print(f"Error saving timesheet: {e}")
        print(traceback.format_exc())  # Log the full traceback to identify the issue
        frappe.log_error(f"Error saving timesheet: {traceback.format_exc()}", "Timesheet Creation")
        return {"message": f"Error submitting timesheet entry: {str(e)}", "status": "error"}
    


@frappe.whitelist(allow_guest=True)
def jobs():
    print("jobs callingggggggggg")
    print(f"Form data received: {frappe.form_dict}")

    # Fetch data from form_dict
    job_name = frappe.form_dict.get("job_name")
    start_date = frappe.form_dict.get("start_date")
    end_date = frappe.form_dict.get("end_date")
    project = frappe.form_dict.get("project")
    user = frappe.form_dict.get("user")
    department = frappe.form_dict.get("department")

    print(f"job_name: {job_name}, start_date: {start_date}, end_date: {end_date}, project: {project}, user: {user}, department: {department}")

    # Check if any of the required fields are missing
    if not job_name or not start_date or not end_date or not project or not user or not department:
        return {"message": "All fields are required. Please fill out the form completely.", "status": "error"}

    try:
        # Let ERPNext handle name generation automatically (skip manual assignment)
        job_entry = frappe.get_doc({
            "doctype": "Jobs",
            "job_name": job_name,
            "start_date": start_date,
            "end_date": end_date,
            "project": project,
            "user": user,
            "department": department,
        })

        print("logssssssssss:", job_entry)

        # Insert and commit, let ERPNext handle name uniqueness
        job_entry.insert(ignore_permissions=True)
        frappe.db.commit()

        print("jobs saved:", job_entry.name)
        return {"message": "log entry submitted successfully", "redirect": "/timetracker/jobs/index.html", "status": "success"}

    except Exception as e:
        # Log the full traceback
        print(f"Error saving job: {e}")
        print(traceback.format_exc())  # Log the full traceback to identify the issue
        frappe.log_error(f"Error saving job: {traceback.format_exc()}", "job Creation")
        return {"message": f"Error submitting job entry: {str(e)}", "status": "error"}
    



@frappe.whitelist(allow_guest=True)
def projects():
    print("project callingggggggggg")
    print(f"Form data received: {frappe.form_dict}")

    # Fetch data from form_dict
    project_name = frappe.form_dict.get("project_name")
    client_name = frappe.form_dict.get("client_name")
    project_cost = frappe.form_dict.get("project_cost")
    project_manager = frappe.form_dict.get("project_manager")
    status = frappe.form_dict.get("status")

    print(f"project_name: {project_name}, client_name: {client_name}, project_cost: {project_cost}, project_manager: {project_manager}, status: {status}")

    # Check if any of the required fields are missing
    if not project_name or not client_name or not project_cost or not project_manager or not status:
        return {"message": "All fields are required. Please fill out the form completely.", "status": "error"}

    try:
        # Let ERPNext handle name generation automatically (skip manual assignment)
        project_entry = frappe.get_doc({
            "doctype": "Projects",
            "project_name": project_name,
            "client_name": client_name,
            "project_cost": project_cost,
            "project_manager": project_manager,
            "status": status,
        })

        print("projectsssssssssss:", project_entry)

        # Insert and commit, let ERPNext handle name uniqueness
        project_entry.insert(ignore_permissions=True)
        frappe.db.commit()

        print("project saved:", project_entry.name)
        return {"message": "project entry submitted successfully", "redirect": "/timetracker/project/index.html", "status": "success"}

    except Exception as e:
        # Log the full traceback
        print(f"Error saving project: {e}")
        print(traceback.format_exc())  # Log the full traceback to identify the issue
        frappe.log_error(f"Error saving project: {traceback.format_exc()}", "project Creation")
        return {"message": f"Error submitting project entry: {str(e)}", "status": "error"}
    




@frappe.whitelist(allow_guest=True)
def get_timelogs():
    print("data frtched callig")
    """Fetch all Timelogs records."""
    user=frappe.session.user
    try:
        timelogs = frappe.get_all(
            "Timelogs",
            filters={"owner":user},
            fields=["name", "project", "job", "todo", "company_name", "status","time","date","formattedtotaltime"]
        )
        return {"status": "success", "data": timelogs}
    except Exception as e:
        frappe.log_error(f"Error fetching timelogs: {str(e)}")
        return {"status": "error", "message": str(e)}
    


@frappe.whitelist(allow_guest=True)
def get_timesheet():
    print("data frtched callig")
    """Fetch all Timesheet records."""
    user=frappe.session.user
    try:
        timesheet = frappe.get_all(
            "Timesheet",
            filters={"owner":user},
            fields=["name", "employee", "date", "clock_in_time", "clock_out_time", "total_hours","status"]
        )
        return {"status": "success", "data": timesheet}
    except Exception as e:
        frappe.log_error(f"Error fetching timetimesheetlogs: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_project():
    print("data frtched callig")
    """Fetch all project records."""
    try:
        print("try block")
        projects = frappe.get_all(
            "Projects",
            fields=["project_name","client_name", "project_cost", "project_manager", "status" ]
        )
        print("fetchd data::::",projects)
        return {"status": "success", "data": projects}
    except Exception as e:
        frappe.log_error(f"Error fetching projects: {str(e)}")
        return {"status": "error", "message": str(e)}
    



@frappe.whitelist()
def get_job():
    print("data frtched callig")
    """Fetch all job records."""
    try:
        job = frappe.get_all(
            "Jobs",
            fields=["job_name","start_date", "end_date", "project", "user","department" ]
        )
        return {"status": "success", "data": job}
    except Exception as e:
        frappe.log_error(f"Error fetching jobs: {str(e)}")
        return {"status": "error", "message": str(e)}
    





@frappe.whitelist()
def update_formatted_total_time(date, formattedtotaltime):
    try:
        # Find existing timelog entry for the date
        existing_log = frappe.get_all("Timelogs", filters={"date": date}, fields=["name"])

        if existing_log:
            for log in existing_log:
                doc = frappe.get_doc("Timelogs", log.name)
                doc.formattedtotaltime = formattedtotaltime
                doc.save()
        print("formattedtotaltime:",formattedtotaltime)
        frappe.db.commit()
        return {"message": "Success"}
    except Exception as e:
        return {"error": str(e)}

    




def convert_to_decimal_hours(time_str):
    """Convert HH:MM:SS or HH:MM format to decimal hours."""
    try:
        parts = time_str.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2]) if len(parts) == 3 else 0  # Handle HH:MM and HH:MM:SS

        decimal_hours = hours + (minutes / 60) + (seconds / 3600)
        return round(decimal_hours, 2)  # Return as float with 2 decimal places
    except Exception as e:
        print(f"Error converting time: {e}")
        return 0.0  # Return 0.0 instead of 0





@frappe.whitelist()
def get_users():
    print("het_user calling")
    users = frappe.get_all("User", filters={"enabled": 1}, fields=["name"])
    print("userrrrrr:",users)
    return {"status": "success", "data": users}




@frappe.whitelist()
def get_department():
    print("get_department calling")
    department = frappe.get_all("Department",fields=["department_name"])
    print("departmentt:",department)
    return {"status": "success", "data": department}





@frappe.whitelist(allow_guest=True)
def get_pending_timesheets():
    timesheets = frappe.db.get_list(
        "Timesheet",
        filters={"status": "Pending"},
        fields=["name"]
    )
    return {"message": timesheets}  # Ensure response has a 'message' key



@frappe.whitelist()
def timesheet_approval(timesheet, status):
    try:
        print("approve timesheet callling")
        # Timesheet document fetch karein
        doc = frappe.get_doc("Timesheet", timesheet)
        
        # Status update karein
        doc.status = status
        # Document ko submit karein (agar "Confirmed" hai to)
        if status == "Confirmed":
            doc.submit()
        else:
            doc.save()  # Agar reject hai to sirf save karein        frappe.db.commit()  # Database update karein
        print("status updated")

        return {"status": "success", "message": f"Timesheet {timesheet} updated to {status}."}
    
    except Exception as e:
        frappe.log_error(f"Error in Timesheet Approval: {str(e)}")
        return {"status": "error", "message": str(e)}



