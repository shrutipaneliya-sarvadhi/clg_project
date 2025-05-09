

import frappe

def get_context(context):
    print("🔹 get_context is being called!")  # Debugging
    frappe.logger().info("🔹 get_context is running!")  # Debugging

    user_email = frappe.session.user  
    print(f"Logged-in user email: {user_email}")  # Debugging
    frappe.logger().info(f"Logged-in user email: {user_email}")

    # Fetch employee(s) linked to the user
    employees = frappe.get_all("Employee", filters={"email": user_email}, pluck="name")

    if not employees:
        print(" No employee found")
        frappe.logger().warning(" No employee found")
        context.timesheets = []
        return context

    print(f"Employee Names: {employees}")  # Debugging
    frappe.logger().info(f"Employee Names: {employees}")

    # ✅ Check if employees list is empty before applying the filter
    if not employees:
        context.timesheets = []
        return context

    # Fetch all timesheets linked to any of the retrieved employees
    timesheets = frappe.get_all(
        "Timesheet",
        filters=[["employee", "in", employees]],  # ✅ Corrected filter format
        fields=["name", "date", "total_hours"]
    )

    print(f"Fetched Timesheets: {timesheets}")  # Debugging
    frappe.logger().info(f"Fetched Timesheets: {timesheets}")

    if not timesheets:
        print(" No timesheets found")
        frappe.logger().warning("No timesheets found")
        context.timesheets = []
        return context

    # Fetch tasks
    timesheet_ids = [ts["name"] for ts in timesheets]
    tasks = frappe.get_all(
        "Timesheet Details",
        filters=[["parent", "in", timesheet_ids]],  # ✅ Corrected filter format
        fields=["parent", "task_name"]
    )
    
    print(f"Tasks fetched: {tasks}")  # Debugging
    frappe.logger().info(f"Tasks fetched: {tasks}")

    # Map tasks to timesheets
    task_map = {}
    for task in tasks:
        task_map.setdefault(task["parent"], []).append(task["task_name"])

    for ts in timesheets:
        ts["tasks"] = ", ".join(task_map.get(ts["name"], ["No tasks"]))

    context.timesheets = timesheets
    return context
