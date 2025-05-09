# # import frappe

# # def get_context(context):
# #     context.employees = frappe.get_all("Employee", 
# #         fields=["first_name", "last_name", "email", "date_of_joining", "department", "designation", "contact_number"]
# #     )
# #     return context
# import frappe

# def get_context(context):
#     if frappe.session.user == "Guest":
#         frappe.local.flags.redirect_location = "/emplyee"
#         raise frappe.Redirect
#     context.user = frappe.session.user

#     user_email = frappe.session.user  # Get logged-in user's email

#     # Fetch employee details for the logged-in user
#     employee = frappe.get_all("Employee", 
#         filters={"email": user_email}, 
#         fields=["first_name", "last_name", "email", "date_of_joining", "department", "designation", "contact_number"]
#     )

#     if employee:
#         context.employee = employee[0]  # Assign the first (and only) record to context
#     else:
#         context.employee = None  # If no employee found, return None

#     return context


import frappe

def get_context(context):
    # If user is not logged in, redirect to login page
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"  # Redirect to login page
        raise frappe.Redirect

    context.user = frappe.session.user
# import frappe

# def get_context(context):
#     context.employees = frappe.get_all("Employee", 
#         fields=["first_name", "last_name", "email", "date_of_joining", "department", "designation", "contact_number"]
#     )
#     return context
import frappe

def get_context(context):
    user_email = frappe.session.user  # Get logged-in user's email

    # Fetch employee details for the logged-in user
    employee = frappe.get_all("Employee", 
        filters={"email": user_email}, 
        fields=["first_name", "last_name", "email", "date_of_joining", "department", "designation", "contact_number"],
        limit_page_length=1
    )

    if employee:
        context.employee = employee[0]  # Assign employee data to context
        fields=["first_name", "last_name", "email", "date_of_joining", "department", "designation", "contact_number"]
    

    if employee:
        context.employee = employee[0]  # Assign the first (and only) record to context
    else:
        context.employee = None  # If no employee found, return None

    return context
