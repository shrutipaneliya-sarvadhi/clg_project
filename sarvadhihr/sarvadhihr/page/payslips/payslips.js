frappe.pages['payslips'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'employee  pay slip',
		single_column: true
	});
}