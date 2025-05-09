import random
import re
import string
import frappe
from frappe.model.document import Document

class Employee(Document):
    def on_submit(self):
        if not self.email:
            frappe.throw("Employee must have an email address.")
  		# Generate a random password
        password = self.generate_random_password()
        
        print("password:",password)
        user = frappe.get_doc({
            "doctype": "User",
            "email": self.email,
            "first_name": self.first_name,
            "send_welcome_email": 0,  # Prevent Frappe from sending a default email
            "new_password": password,  # Set initial password
            "roles": [{"role": "Employee"}]  # Assign the appropriate role
        })
        user.insert(ignore_permissions=True)

        self.validate_email()

        # Send a simple email immediately
        try:
            frappe.sendmail(
            	recipients=[self.email],
                subject="Welcome to the Company - Your Login Credentials",
                message=f"""
                <p>Dear {self.first_name},</p>
                <p>Welcome to the company! We are excited to have you on board.</p>
                <p>Your login credentials are:</p>
                <ul>
                    <li><b>Username:</b> {self.email}</li>
                    <li><b>Password:</b> {password}</li>
                </ul>
                <p>Please log in and change your password immediately.</p>
                <p>Best Regards,<br>HR Team</p>
                """,
            )
            # Immediately process the email queue
            frappe.email.queue.flush()

            frappe.msgprint(f"Email sent to {self.email}.")
        except Exception as e:
            frappe.log_error(f"Error sending email to {self.email}: {str(e)}", "Employee Email Error")
            frappe.throw("Failed to send email. Please check email configuration.")
    def generate_random_password(self, length=10):
        """Generate a secure random password"""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))
    
    def validate_email(self):
        """
        Validate the email address format.
        """
        if not self.email:
            return
 
        self.email = self.email.strip()
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, self.email):
            frappe.throw("Invalid email format. Please enter a valid email address.")