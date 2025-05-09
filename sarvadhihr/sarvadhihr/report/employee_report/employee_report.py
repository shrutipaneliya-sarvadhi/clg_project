# import frappe
# from frappe.utils import flt, nowdate
 
# def execute(filters=None):
#     # Check if filters are provided (like date range, employee, etc.)
#     filters = filters or {}
 
#     # Get the list of payslips within the given filters (e.g., period_start_date and period_end_date)
#     payslips = frappe.get_all('Payslip', filters=filters, fields=[
#         'name','employee', 'period_start_date', 'period_end_date', 'total_salary', 'total_deductions', 'net_salary','payslip_status'
#     ])
 
#     # Prepare data for the report
#     report_data = []
#     for payslip in payslips:
#         employee = frappe.get_doc('Employee', payslip.employee)
#         report_data.append({
#             'payslip_name': payslip.name,
#             'employee_name': employee.name1,
#             'period_start_date': payslip.period_start_date,
#             'period_end_date': payslip.period_end_date,
#             'total_salary': payslip.total_salary,
#             'total_deductions': payslip.total_deductions,
#             'net_salary': payslip.net_salary
#         })
 
#     # Define columns to be shown in the report
#     columns = [
#         {"label": "Payslip Name", "fieldname": "payslip_name", "fieldtype": "Data"},
#         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data"},
#         {"label": "Period Start Date", "fieldname": "period_start_date", "fieldtype": "Date"},
#         {"label": "Period End Date", "fieldname": "period_end_date", "fieldtype": "Date"},
#         {"label": "Total Salary", "fieldname": "total_salary", "fieldtype": "Currency"},
#         {"label": "Total Deductions", "fieldname": "total_deductions", "fieldtype": "Currency"},
#         {"label": "Net Salary", "fieldname": "net_salary", "fieldtype": "Currency"}
#     ]
 
#     # Return the columns and data for the report
#     return columns, report_data
 
 
 
# import frappe
# from frappe.utils import flt, nowdate
 
# def execute(filters=None):
#     # Check if filters are provided (like date range, employee, etc.)
#     filters = filters or {}
 
#     # Log the filters to ensure they're being passed correctly
#     frappe.log_error(filters, "Payslip Report Filters")
 
#     # Get the list of payslips within the given filters (e.g., period_start_date and period_end_date)
#     payslips = frappe.get_all('Payslip', filters=filters, fields=[
#         'name', 'employee', 'period_start_date', 'period_end_date', 'total_salary', 'total_deductions', 'net_salary', 'payslip_status'
#     ])
 
#     # Log the fetched payslips to ensure data is being retrieved
#     frappe.log_error(payslips, "Fetched Payslips")
 
#     # Prepare data for the report
#     report_data = []
#     for payslip in payslips:
#         # Check if employee exists
#         employee = frappe.get_doc('Employee', payslip.employee)
 
#         # Log employee data
#         frappe.log_error(employee, f"Employee Data for Payslip {payslip.name}")
 
#         report_data.append({
#             'payslip_name': payslip.name,
#             'employee_name': employee.employee_name,  # Corrected to employee.employee_name
#             'period_start_date': payslip.period_start_date,
#             'period_end_date': payslip.period_end_date,
#             'total_salary': payslip.total_salary,
#             'total_deductions': payslip.total_deductions,
#             'net_salary': payslip.net_salary
#         })
 
#     # Check if report data was populated
#     if not report_data:
#         frappe.msgprint("No data found for the specified filters.")
    
#     # Define columns to be shown in the report
#     columns = [
#         {"label": "Payslip Name", "fieldname": "payslip_name", "fieldtype": "Data"},
#         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data"},
#         {"label": "Period Start Date", "fieldname": "period_start_date", "fieldtype": "Date"},
#         {"label": "Period End Date", "fieldname": "period_end_date", "fieldtype": "Date"},
#         {"label": "Total Salary", "fieldname": "total_salary", "fieldtype": "Currency"},
#         {"label": "Total Deductions", "fieldname": "total_deductions", "fieldtype": "Currency"},
#         {"label": "Net Salary", "fieldname": "net_salary", "fieldtype": "Currency"}
#     ]
 
#     # Return the columns and data for the report
#     return columns, report_data
 
 
 
import frappe
 
def execute(filters=None):
    # Define columns to be displayed in the report
    columns = [
        {"fieldname": "payslip_name", "label": "Payslip Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "period_start_date", "label": "Period Start Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "period_end_date", "label": "Period End Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "total_salary", "label": "Total Salary", "fieldtype": "Currency", "width": 120},
        {"fieldname": "total_deductions", "label": "Total Deductions", "fieldtype": "Currency", "width": 120},
        {"fieldname": "net_salary", "label": "Net Salary", "fieldtype": "Currency", "width": 120}
    ]
    
    # Fetch payslip data from the Payslip doctype based on the filters
    data = frappe.db.get_all(
        "Payslip",
        fields=["name", "employee", "period_start_date", "period_end_date", "total_salary", "total_deductions", "net_salary", "payslip_status"],
        filters=filters,  # Apply any provided filters like date range, employee, etc.
        order_by="period_start_date desc"  # Sort by period start date in descending order
    )
    print("Payslips fetched:", data)
    
    # Prepare the final data to show in the report
    report_data = []
    for payslip in data:
        employee = frappe.get_doc("Employee", payslip.employee)
        report_data.append({
            "payslip_name": payslip.name,
            "employee_name": employee.first_name,
            "period_start_date": payslip.period_start_date,
            "period_end_date": payslip.period_end_date,
            "total_salary": payslip.total_salary,
            "total_deductions": payslip.total_deductions,
            "net_salary": payslip.net_salary
        })
    print("Report Data:", report_data)
 
    # Return the columns and the report data
    return columns, report_data