frappe.ui.form.on('Leave Application', {
    // from_date: function(frm) {
    //     update_leave_details(frm);
    // },
    // to_date: function(frm) {
    //     update_leave_details(frm);
    // }
});

// function update_leave_details(frm) {
//     if (frm.doc.from_date && frm.doc.to_date) {
//         // **1️⃣ Ensure Table is Fully Cleared Before New Data**
//         frm.clear_table("leave_details");
//         frm.set_value("total_days", 0); // Reset total days before calculation
//         frm.refresh_field("leave_details");
//         frm.refresh_field("total_days");

//         frappe.call({
//             method: "ourhrms.ourhrms.doctype.leave_application.leave_application.get_leave_days",
//             args: {
//                 from_date: frm.doc.from_date,
//                 to_date: frm.doc.to_date
//             },
//             callback: function(response) {
//                 if (response.message) {
//                     let leave_days = response.message.leave_days;
//                     show_leave_details_dialog(frm, leave_days);
//                 }
//             }
//         });
//     }
// }

// function show_leave_details_dialog(frm, leave_days) {
//     let table_html = `
//         <table class="table table-bordered" id="leave-days-table">
//             <thead>
//                 <tr>
//                     <th>Date</th>
//                     <th>Type</th>
//                     <th>Leave Type</th>
//                 </tr>
//             </thead>
//             <tbody>
//     `;

//     leave_days.forEach(day => {
//         let leave_type_options = `
//             <select class="leave-type" data-date="${day.date}">
//                 <option value="Full Day" selected>Full Day</option>
//                 <option value="Half Day - First Half">Half Day - First Half</option>
//                 <option value="Half Day - Second Half">Half Day - Second Half</option>
//             </select>
//         `;
//         table_html += `
//             <tr>
//                 <td>${day.date}</td>
//                 <td>${day.holiday_type || "Working Day"}</td>
//                 <td>${leave_type_options}</td>
//             </tr>
//         `;
//     });

//     table_html += `</tbody></table>`;

//     let d = new frappe.ui.Dialog({
//         title: 'Leave Details',
//         fields: [{ fieldtype: 'HTML', options: table_html }],
//         size: 'large',
//         primary_action_label: 'Save',
//         primary_action: function() {
//             let selected_leaves = [];
//             let total_leave_days = 0;

//             $("#leave-days-table tbody tr").each(function() {
//                 let date = $(this).find("td:first").text();
//                 let holiday_type = $(this).find("td:nth-child(2)").text();
//                 let leave_type = $(this).find(".leave-type").val();

//                 if (holiday_type !== "Weekend" && holiday_type !== "Public Holiday") {
//                     if (leave_type === "Full Day") {
//                         total_leave_days += 1;
//                     } else if (leave_type.includes("Half Day")) {
//                         total_leave_days += 0.5;
//                     }
//                 }

//                 selected_leaves.push({ date, holiday_type, leave_type });
//             });

//             // **2️⃣ Clear Table Again to Prevent Duplication**
//             frm.clear_table("leave_details");

//             // **3️⃣ Insert New Data Properly**
//             selected_leaves.forEach(day => {
//                 let row = frm.add_child("leave_details");
//                 row.leave_date = day.date;
//                 row.holiday_type = day.holiday_type;
//                 row.leave_type = day.leave_type;
//             });

//             // **4️⃣ Correctly Update Total Days**
//             frm.set_value("total_days", total_leave_days);

//             // **5️⃣ Ensure UI Updates Immediately**
//             frm.refresh_field("leave_details");
//             frm.refresh_field("total_days");

//             // **6️⃣ Small Delay to Ensure UI Refreshes Properly**
//             setTimeout(() => {
//                 frm.refresh();
//             }, 200);

//             d.hide();
//         }
//     });

//     d.show();
// }
