# import frappe

# def get_context(context):
#     if frappe.session.user == "Administrator":
#         frappe.throw("You need to log in to access this page.", frappe.PermissionError)

#     employee = frappe.get_value("Employee", {"user_id": frappe.session.user}, "name")

#     if employee:
#         context.payslips = frappe.get_all("Payslip",
#             fields=["name", "total_salary", "total_deductions", "net_salary"]
#         )
#     else:
#         context.payslips = []

#     context.no_cache = 1
# import frappe

# def get_context(context):
    
#     employee = frappe.get_value("Employee",  "name")

#     if employee:
#         context.payslips = frappe.get_all("Payslip", fields=["name", "total_salary", "total_deductions", "net_salary"], filters={"employee": employee})
#     else:
#         context.payslips = []

#     context.no_cache = 1



# import frappe

# def get_context(context):
#     if frappe.session.user == "Administrator":
#         frappe.throw("You need to log in to access this page.", frappe.PermissionError)

#     employee = frappe.get_value("Employee", {"user": frappe.session.user}, "name")
#     frappe.logger().info(f"Fetched Employee: {employee}")  # Debug log

#     if employee:
#         context.payslips = frappe.get_all("Payslip", 
#             fields=["name", "total_salary", "total_deductions", "net_salary"],
#             filters={"employee": employee}  # Filtering by employee
#         )
#         frappe.logger().info(f"Payslips: {context.payslips}")  # Debug log
#     else:
#         context.payslips = []
#         frappe.logger().info("No Employee found for this user.")

#     context.no_cache = 1



# import frappe

# def get_context(context):
#     if frappe.session.user == "Administrator":
#         frappe.throw("You need to log in to access this page.", frappe.PermissionError)

#     # Fetch employee using email instead of 'user'
#     employee = frappe.get_value("Employee", {"email": frappe.session.user}, "name")
#     frappe.logger().info(f"Fetched Employee: {employee}")  # Debugging

#     if employee:
#         context.payslips = frappe.get_all(
#             "Payslip", 
#             fields=["name", "total_salary", "total_deductions", "net_salary"],
#             filters={"employee": employee}  # Corrected filter
#         )
#         frappe.logger().info(f"Payslips: {context.payslips}")  # Debug log
#     else:
#         context.payslips = []
#         frappe.logger().info("No Employee found for this user.")

#     context.no_cache = 1



import frappe

def get_context(context):
    user_email = frappe.session.user  # Get logged-in user's email

    # Fetch the Employee record associated with the logged-in user
    employee = frappe.get_value("Employee", {"email": user_email}, "name")

    if employee:
        # Fetch all payslips for the identified employee
        payslips = frappe.get_all("Payslip", 
            filters={"employee": employee}, 
            fields=["name", "total_salary", "total_deductions", "net_salary", "total_hours","period_start_date","period_end_date"]
        )
        context.payslips = payslips  # Assign payslips to context
    else:
        context.payslips = []  # No payslips if no matching employee is found

    return context
