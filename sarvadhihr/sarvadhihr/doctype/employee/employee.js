// Copyright (c) 2025, sarvadhi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Employee", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        // Apply the filter to the Leave Type child table
        frm.fields_dict['leave_type'].grid.get_field('employee').get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    'employee': frm.doc.name
                }
            };
        };

        // Optionally, you can set read-only for fields like Total Paid Leave, etc. for the current employee
        frm.fields_dict['leave_type'].grid.get_field('total_paid_leave').read_only = 1;
        frm.fields_dict['leave_type'].grid.get_field('remaining_paid_leave').read_only = 1;
        frm.fields_dict['leave_type'].grid.get_field('taken_casual_leave').read_only = 1;
        frm.fields_dict['leave_type'].grid.get_field('taken_sick_leave').read_only = 1;
    }
});
// frappe.ui.form.on('Employee', {
//     after_save: function(frm) {
//         if (frm.doc.__islocal) return;  // Prevent sending email on creation

//         frappe.call({
//             method: "ourhrms.ourhrms.doctype.employee.employee.send_credentials",
//             args: {
//                 employee: frm.doc.name
//             },
//             callback: function(response) {
//                 if (!response.exc) {
//                     frappe.msgprint(__('Credentials have been sent to the employee.'));
//                 }
//             }
//         });
//     }
// });
