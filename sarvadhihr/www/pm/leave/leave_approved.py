import frappe

def get_context(context):
    leave_approved=frappe.get_all(
       "Leave Approval",
        fields=['leave_application','status','approved_by','approval_date']
    )
    context.leave_approved_list=leave_approved
    return context