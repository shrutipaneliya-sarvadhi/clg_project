import frappe


@frappe.whitelist()
def save_timelog(data):
    # Create a new Timelog record
    timelog = frappe.get_doc({
        'doctype': 'Timetracker',
        'project': data.get('project'),
        'job': data.get('job'),
        'todo': data.get('todo'),
        'company_name': data.get('company_name'),
        'status': data.get('status')
    })
    timelog.insert()  # Save the timelog to the database
    return {'status': 'success'}
