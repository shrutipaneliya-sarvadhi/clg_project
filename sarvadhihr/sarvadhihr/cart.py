import frappe

@frappe.whitelist()
def get_cart_items(user):
    # Fetch cart items from the 'Booking' doctype (or replace with your own cart-related logic)
    cart_items = frappe.get_all('Payslip', fields=['employee', 'net_salary'])
    return cart_items
