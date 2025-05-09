# Copyright (c) 2025, hr and contributors
# For license information, please see license.txt
 
# import frappe
import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import save_file
from frappe.utils.pdf import get_pdf
from datetime import datetime

 
class Payslip(Document):
    def on_submit(self):
        print("email sending...")
        print("send_payslip_report calling...")
        try:
            print("try blockkkkkkkkkkkkkkk")
            # Get the employee record linked to this payslip
            employee = frappe.get_doc("Employee", self.employee)  # 'employee' field in Payslip
            print("employeee payslip      --------:",employee)
            if employee and employee.email:
                # Get the employee email address from the Employee doctype
                employee_email = employee.email
                print("email of employeee-------",employee_email)
                # Prepare the email content
                subject = f"Your Payslip for {self.period_start_date} - {self.period_end_date}"
                message = f"Dear {employee.first_name},<br><br>"
                message += f"Your payslip for the period from {self.period_start_date} to {self.period_end_date} has been finalized.<br>"
                message += "Regards,<br>Your HR Team Megha Sharma"
 

                # file_name = f"Payslip_{self.name}.pdf"
                # html_content = frappe.get_print("Payslip", self.name, as_pdf=True)
                print("html_content:")
                # file_doc = save_file(file_name, html_content, self.doctype, self.name, is_private=1)
                file_doc = generate_payment_report_pdf(self) 

                print("after this pdf generatinggggggggggg")
                # file_name = f"payslip{self.name}.pdf"
                print("pdf  nameeeeeeeeee:",file_doc)

                # Get the file content properly
                file_path = file_doc.file_url
                print("file_path:", file_path)

                file_path = frappe.get_site_path(file_doc.file_url.strip('/'))
                print("file_path:", file_path)

                try:
                    # Read file content
                    with open(file_path, 'rb') as f:
                        file_content = f.read()

                    # Send email with attachment
                    frappe.sendmail(
                        recipients=[employee_email],
                        subject=subject,
                        message=message,
                        attachments=[{
                            "fname": file_doc.file_name,
                            "fcontent": file_content
                        }]
                    )
                    frappe.msgprint(f"Payment Report Sent to {employee_email}!")
                except Exception as e:
                    print("Error reading file content:", e)


                frappe.msgprint(f"Payment Report Sent to {employee_email}!")

                frappe.enqueue("frappe.email.queue.flush")
                print("Payslip email sent to:", employee_email)
            else:
                frappe.throw(frappe._("Employee record not found or email is missing."))
        
        except Exception as e:
            # Log error and notify user in case of failure
            frappe.log_error(message=str(e), title="Payslip Email Sending Error")
            frappe.msgprint(frappe._("An error occurred while sending the email. Please try again later."))
        
        print("email sending complete")
 

    def before_submit(self):
        # Set the payslip status to 'Finalized' before submission
        if self.payslip_status == "Draft":  # Ensure it is in Draft state before changing
            self.payslip_status = "Finalized"
            print(f"Payslip {self.name} has been finalized.")

        # Fetch salary structure details
        salary_structure = frappe.get_doc("Salary_Structure", self.salary_structure)

        # Log salary structure details to debug
        print(f"Salary Structure: {salary_structure.name}, Basic Pay: {salary_structure.basic_pay}, Overtime Pay: {salary_structure.overtime_pay}")
        
        # Check if basic_pay is None and handle accordingly
        
        overtime_pay = salary_structure.overtime_pay if salary_structure.overtime_pay is not None else 0.0
            
        # Fetch allowances and deductions
        allowances = frappe.get_all(
            "allowances",
            filters={"parent": self.salary_structure},
            fields=["allowance_type", "amount"]
        )
        deductions = frappe.get_all(
            "deductions",
            filters={"parent": self.salary_structure},
            fields=["deduction_type", "amount"]
        )
        
        # Calculate total allowances (ensure float)
        total_allowances = sum([float(allowance['amount']) for allowance in allowances])
        
        # Calculate total deductions (ensure float)
        total_deductions = sum([float(deduction['amount']) for deduction in deductions])
        basic_pay = float(salary_structure.basic_pay) if salary_structure.basic_pay else 0.0
        hourly_rate = basic_pay / 30  # Assuming 160 hours a month for salary calculation

        print("basiccccccccccccccccc",basic_pay)
        

        # Now handle the calculation of net salary based on total hours worked
        if self.employee and self.period_start_date and self.period_end_date:
            # Fetch total worked hours for the given period
            total_hours = self.get_total_hours_worked_in_period(self.employee, self.period_start_date, self.period_end_date)
            self.total_hours = total_hours  # Save total hours in Payslip
            
            # Gross Salary Calculation = Basic Pay + Allowances + Overtime
            gross_salary = float(total_hours * hourly_rate) + float(total_allowances) + float(overtime_pay)



            if self.total_hours >=150:
                # Calculate net salary = Gross Salary + (Total Worked Hours * Hourly Rate) - Total Deductions
                net_salary = gross_salary - total_deductions
            else:
                net_salary=gross_salary
            # tax_deduction = net_salary * 0.30  # 10% tax deduction
            # net_salary_after_tax = net_salary - tax_deduction  # Subtracting the tax from the net salary


            # Set the calculated values to the Payslip document
            self.net_salary = net_salary
            self.total_salary = gross_salary
            self.total_deductions = total_deductions

            # Notify the user about the calculated net salary
            frappe.msgprint(f"Payslip Calculated: Net Salary = {self.net_salary}")
            print(f"Employee: {self.employee}, Total Hours Worked: {total_hours}, Net Salary: {self.net_salary}")


    def get_total_hours_worked_in_period(self, employee, period_start_date, period_end_date):
        """Fetch and sum up total hours worked by the employee for the given period."""
        
        # Convert string dates to datetime objects
        period_start_date = datetime.strptime(period_start_date, '%Y-%m-%d')
        period_end_date = datetime.strptime(period_end_date, '%Y-%m-%d')
        
        # Query the timesheets based on the given period and employee
        timesheets = frappe.get_all(
            'Timesheet',
            filters={
                'employee': employee,
                'date': ['between', [period_start_date, period_end_date]]
            },
            fields=['total_hours']
        )
        
        # Sum up the total hours worked from the timesheet entries
        total_hours = 0
        for ts in timesheets:
            try:
                # Ensure the total_hours is treated as a float for addition
                total_hours += float(ts['total_hours'])
            except ValueError:
                # Handle the case where total_hours is not a valid number (e.g., invalid or empty value)
                frappe.log_error(f"Invalid total_hours value in Timesheet: {ts['total_hours']}")
        
        return total_hours


   



def generate_payment_report_pdf(doc):
    print("generate_payment_report_pdf calling:")
    frappe.logger().info(f"Generating payment report for: {doc.employee}")

    # ✅ Fix PDF file name
    file_name = f"Payslip_{doc.employee}.pdf"

    # ✅ Ensure template path is correct
    template_path = "ourhrms/print_format/format/format.html"
    html_template = frappe.get_template(template_path).render({
        "employee": doc.employee,
        "salary_structure": doc.salary_structure,
        "total_salary": doc.total_salary,
        "net_salary": doc.net_salary,
    })

    # ✅ Generate PDF
    pdf_content = get_pdf(html_template)

    # ✅ Save PDF using save_file
    file_doc = save_file(file_name, pdf_content, doc.doctype, doc.name, is_private=1)
    print("file_doc:", file_doc)

    if not file_doc:
        frappe.throw("PDF generation failed. Please check the template or data.")

    return file_doc
