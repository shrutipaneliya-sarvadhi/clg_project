import frappe

def get_context(context):
    leave_requests=frappe.get_all(
       "Leave Application",
        fields=['leave_type','from_date','to_date','total_days','leave_reason']
    )
    context.leave_request_list=leave_requests
    return context