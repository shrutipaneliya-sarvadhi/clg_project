# Copyright (c) 2025, sarvadhi and contributors
# For license information, please see license.txt

# import frappe
#from frappe.model.document import Document


#class JobApplicant(Document):
#	pass


# Copyright (c) 2025, sarvadhi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JobApplicant(Document):
    def before_save(self):
        print(f"JobApplicant {self.applicant_name} status: {self.status}")  # Debugging line
        self.send_offer_email()

    def send_offer_email(self):
        print(f"Checking if status is 'Hired' and offer_sent is {self.offer_sent}")  # Debugging line
        
        # Check if status is "Hired" and offer has not been sent
        if self.status == "Hired" and not self.offer_sent:
            print("Status is 'Hired', sending offer email...")  # Debugging line
            
            # Compose the email content
            subject = "Congratulations on Your Job Offer"
            message = f"""
            Dear {self.applicant_name},

            Congratulations! We are pleased to offer you the position of {self.applied_for}.
            
            Please let us know your acceptance at your earliest convenience by clicking the link below:

            {self.get_offer_reply_link()}

            Best Regards,  
            HR Team
            """
            try:
                print(f"Sending email to {self.email}")  # Debugging line
                # Send the email directly (without enqueue)
                frappe.sendmail(
                    recipients=[self.email],
                    subject=subject,
                    message=message
                )
                # Set the flag to avoid duplicate emails
                self.offer_sent = True
                frappe.db.commit()  # Ensure the flag gets updated
                print(f"Email sent to {self.email}")  # Debugging line
                frappe.enqueue("frappe.email.queue.flush")
            except Exception as e:
                print(f"Error sending email to {self.email}: {str(e)}")  # Debugging line
                raise e

    def get_offer_reply_link(self):
        # Generate the offer reply link dynamically
        return "http://ourhrms.local:8047/offer-letter-reply/new"
