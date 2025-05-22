

import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import save_file
from frappe.utils.pdf import get_pdf

class JobApplicant(Document):
    def before_save(self):
        print(f"JobApplicant {self.applicant_name} status: {self.status}")  # Debugging line
        self.send_offer_email()

    def send_offer_email(self):
        print(f"Checking if status is 'Hired' and offer_sent is {self.offer_sent}")  # Debugging line
        
           
        # Check if status is "Hired" and offer has not been sent
        if self.status == "Hired" and not self.offer_sent:
            print("Status is 'Hired', sending offer email...")  # Debugging line
            
            
            file_doc = generate_offer_report_pdf(self) 
            print('file_doc:',file_doc)
            file_path = file_doc.file_url
            print('file_path:',file_path)
            file_path = frappe.get_site_path(file_doc.file_url.strip('/'))
            print('path:',file_path)

            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            print('file_content:',file_content)
            # Compose the email content
            subject = "Congratulations on Your Job Offer"
            message = f"""
            Dear {self.applicant_name},

            Congratulations! We are pleased to offer you the position of {self.applied_for}.

            Here is your offer letter

            Best Regards,  
            HR Team
            """
            try:
                print(f"Sending email to {self.email}")  # Debugging line
                # Send the email directly (without enqueue)
                frappe.sendmail(
                    recipients=[self.email],
                    subject=subject,
                    message=message,
                    attachments=[{
                            "fname": file_doc.file_name,
                            "fcontent": file_content
                        }]
                )
                # Set the flag to avoid duplicate emails
                self.offer_sent = True
                frappe.db.commit()  # Ensure the flag gets updated
                frappe.msgprint(f"Payment Report Sent to {self.email}!")

                print(f"Email sent to {self.email}")  # Debugging line
                frappe.enqueue("frappe.email.queue.flush")
            except Exception as e:
                print(f"Error sending email to {self.email}: {str(e)}")  # Debugging line
                raise e

    def get_offer_reply_link(self):
        # Generate the offer reply link dynamically
        return "http://ourhrms.local:8047/offer-letter-reply/new"





def generate_offer_report_pdf(doc):
    print("generate_offer_report_pdf calling:")
    frappe.logger().info(f"Generating offer report for: {doc.name}")

    # ✅ Fix PDF file name
    file_name = f"offer_{doc.name}.pdf"

    # ✅ Ensure template path is correct
    template_path = "sarvadhihr/print_format/format/offer_format.html"
    html_template = frappe.get_template(template_path).render({
        "applicant_name": doc.applicant_name,
        'applied_for':doc.applied_for
    })

    # ✅ Generate PDF
    pdf_content = get_pdf(html_template)
    print('pdf_content',pdf_content)
    # ✅ Save PDF using save_file
    file_doc = save_file(file_name, pdf_content, doc.doctype, doc.name, is_private=1)
    print("file_doc:", file_doc)

    if not file_doc:
        frappe.throw("PDF generation failed. Please check the template or data.")

    return file_doc
