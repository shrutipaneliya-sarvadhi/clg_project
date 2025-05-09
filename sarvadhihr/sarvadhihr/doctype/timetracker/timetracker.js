// Copyright (c) 2025, sarvadhi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Timetracker", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Timetracker', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            // Check if there is an active task (task without clock_out)
            const active_task = frm.doc.tasks_worked_on?.find(detail => !detail.clock_out);

            // If no active task, show Start Time button, else show Stop Time button
            let button_label = active_task ? "Stop Time" : "Start Time";
            let button_color = active_task ? "danger" : "primary";  // Red if active, blue otherwise

            // Remove any previously added custom buttons to avoid duplicates
            frm.clear_custom_buttons();

            // Add or update the button based on the task's status
            frm.add_custom_button(__(button_label), function() {
                if (!active_task) {
                    // No active task, so we start a new one
                    frappe.prompt([
                        {
                            label: 'Task Name',
                            fieldname: 'task_name',
                            fieldtype: 'Data',
                            reqd: 1
                        }
                    ], (values) => {
                        // Get task name and start time
                        let task_name = values.task_name;
                        let start_time = frappe.datetime.now_datetime();

                        // Add the task to the child table
                        let child = frm.add_child('tasks_worked_on', {
                            task_name: task_name,
                            clock_in: start_time
                        });

                        // Refresh the child table field to reflect the updated data
                        frm.refresh_field('tasks_worked_on');

                        // // Show message
                        // frappe.msgprint(`Started task: ${task_name} at ${start_time}`);

                        console.log(`task added to the child table with clock_in time: ${start_time} `);

                        // Save the parent document to ensure the child table is saved
                        frm.save();

                        // Reload to update button state
                        frm.reload_doc();
                    });

                } else {
                    // There is an active task, so we stop it
                    let stop_time = frappe.datetime.now_datetime();
                    let clock_in = active_task.clock_in;

                    // Calculate total hours
                    const start_time_obj = moment(clock_in);
                    const end_time_obj = moment(stop_time);
                    const duration = moment.duration(end_time_obj.diff(start_time_obj));
                    const total_hours = duration.asHours();

                    // Update the task details with clock_out and total_hours
                    frappe.model.set_value('Timetracker Details', active_task.name, 'clock_out', stop_time);
                    frappe.model.set_value('Timetracker Details', active_task.name, 'total_hours', total_hours);

                    // Calculate total hours for all tasks worked on
                    const parent_total_hours = frm.doc.tasks_worked_on.reduce((sum, task) => {
                        return sum + (task.total_hours || 0);
                    }, 0);
                    frappe.model.set_value(frm.doctype, frm.docname, 'total_hours', parent_total_hours);

                    // Refresh the child table and total hours fields
                    frm.refresh_field('tasks_worked_on');
                    frm.refresh_field('total_hours');

                    // // Show message
                    // frappe.msgprint(`Stopped task: ${active_task.task_name} at ${stop_time}. Total hours worked: ${total_hours}`);
                    console.log(`clock_out time and total hours are added to child table:${stop_time}`)

                    // Save the parent form so the changes in the child table are stored
                    frm.save();

                    // Reload to update button state
                    frm.reload_doc();
                }
            }).addClass(`btn-${button_color}`); // Apply the appropriate button color
        }
    }
});



// frappe.ui.form.on('Timetracker', {
//     // Add Start Time button
//     refresh: function(frm) {
//         if (!frm.is_new()) {
//             // Add Start Time button
//             frm.add_custom_button(__('Start Time'), function() {
//                 // Check if there is an active task (one without clock_out)
//                 const active_task = frm.doc.tasks_worked_on.find(detail => !detail.clock_out);
//                 if (active_task) {
//                     // If there's an active task, show an error message
//                     frappe.msgprint('Please stop the active task before starting a new one.');
//                     return; // Prevent starting a new task
//                 }

//                 // Prompt the user to enter the task name
//                 frappe.prompt([
//                     {
//                         label: 'Task Name',
//                         fieldname: 'task_name',
//                         fieldtype: 'Data',
//                         reqd: 1
//                     }
//                 ], (values) => {
//                     // Get the task name and start time
//                     const task_name = values.task_name;
//                     const start_time = frappe.datetime.now_datetime();

//                     // Add a new entry to the child table Timetracker Details
//                     let child = frm.add_child('tasks_worked_on', {
//                         task_name: task_name,
//                         clock_in: start_time
//                     });

//                     // Refresh the Timetracker Details field to show the updated data
//                     frm.refresh_field('tasks_worked_on');

//                     // Show a message indicating that the task has started
//                     frappe.msgprint(`Started task: ${task_name} at ${clock_in}`);
//                 });
//             });


//                         // Add Stop Time button
//                 frm.add_custom_button(__('Stop Time'), function() {
//                     // Find the active task (one that doesn't have an end time)
//                     const active_task = frm.doc.tasks_worked_on.find(detail => !detail.clock_out);

//                     if (active_task) {
//                         // Capture the current stop time
//                         const stop_time = frappe.datetime.now_datetime();

//                         // Calculate the total hours by finding the difference between stop_time and clock_in
//                         const clock_in = active_task.clock_in;
//                         const start_time_obj = moment(clock_in); // Use Moment.js to parse the start time
//                         const end_time_obj = moment(stop_time); // Use Moment.js to parse the stop time
                        
//                         // Calculate the difference in hours
//                         const duration = moment.duration(end_time_obj.diff(start_time_obj));
//                         const total_hours = duration.asHours(); // Get total hours as a floating point number

//                         // Update the child table with the stop time and total_hours
//                         frappe.model.set_value('Timetracker Details', active_task.name, 'clock_out', stop_time);
//                         frappe.model.set_value('Timetracker Details', active_task.name, 'total_hours', total_hours);

//                         // Calculate the total_hours for all tasks worked on
//                         const parent_total_hours = frm.doc.tasks_worked_on.reduce((sum, task) => {
//                             return sum + (task.total_hours || 0);
//                         }, 0);
//                         frappe.msgprint(`total_hoursssss: ${parent_total_hours}`);

//                         // Update the parent total_hours field with the sum of total hours from all tasks
//                         frappe.model.set_value(frm.doctype, frm.docname, 'total_hours', parent_total_hours);

//                         // Refresh the Timetracker Details field to show the updated data
//                         frm.refresh_field('tasks_worked_on');
//                         frm.refresh_field('total_hours'); // Refresh the parent total_hours field

//                         // Show a message indicating that the task has stopped, clock-out time, and total hours worked
//                         frappe.msgprint(`Stopped task: ${active_task.task_name} at ${stop_time}. Total hours worked: ${total_hours}`);
//                     } else {
//                         // If there are no active tasks, show an error message
//                         frappe.msgprint('No active task to stop.');
//                     }
//                 });
//         }
//     }
// });

frappe.ui.form.on('Timetracker', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {  // If document is submitted
            frm.set_df_property('clock_out_time', 'hidden', 0);  // Show field
        } else {
            frm.set_df_property('clock_out_time', 'hidden', 1);  // Hide field before submission
        }
    }
});
