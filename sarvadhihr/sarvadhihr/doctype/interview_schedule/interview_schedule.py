# Copyright (c) 2025, sarvadhi and contributors
# For license information, please see license.txt

# import frappe
#from frappe.model.document import Document


#class InterviewSchedule(Document):
#	pass
# Copyright (c) 2025, Shruti and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InterviewSchedule(Document):
    def on_submit(self):
        send_interview_schedule_email(self)


# Function to send the interview schedule email without PDF attachment
def send_interview_schedule_email(doc):
    
    if doc.email:  # Ensure the document has an 'applicant' and email field
        # Retrieve the linked applicant document
        applicant_doc = frappe.get_doc("Job Applicant", doc.applicant)
        
        # Access the field from the linked document
        applicant_name = applicant_doc.applicant_name  # Assuming the field is 'applicant_name'
        
        subject = f"Interview Scheduled for {applicant_name}"
        message = f"""
<html>
    <body>
        <p>Hello {applicant_name},</p>

        <p>We are pleased to inform you that your interview has been scheduled on {doc.interview_date}.</p>

        <p>Please find the interview details below:</p>        
        
        <p><strong>Interview Date:</strong> {doc.interview_date}</p>
        <p><strong>Interview Panel:</strong> {doc.interview_panel}</p>
        
        <p>We look forward to meeting you!</p>

        <p>Regards,<br>HR Team</p>
    </body>
</html>
"""


        try:
            # Send the email without the PDF attachment
            frappe.sendmail(
                recipients=doc.email,  # Send to the applicant's email
                subject=subject,
                message=message
            )
            frappe.enqueue("frappe.email.queue.flush")
            frappe.msgprint(
                f"Interview schedule email sent successfully to {doc.email}.",
                alert=True
            )
        except Exception as e:
            frappe.log_error(f"Email Sending Error: {str(e)}", "Interview Schedule Email")
            frappe.msgprint("Failed to send email. Please check the logs.", alert=True)
