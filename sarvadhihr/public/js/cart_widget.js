frappe.ui.form.on('Dashboard', {
    refresh: function(frm) {
        // Add custom Cart button to the dashboard
        frm.add_custom_button(__('Cart'), function() {
            // Trigger AJAX call to fetch cart items
            frappe.call({
                method: 'ourhrms.ourhrms.cart.get_cart_items',
                args: {
                    user: frappe.session.user  // Fetch cart for the logged-in user
                },
                callback: function(response) {
                    let cartItems = response.message;
                    let cartTable = '<table><thead><tr><th>Item</th><th>Quantity</th></tr></thead><tbody>';
                    cartItems.forEach(item => {
                        cartTable += `<tr><td>${item.employee}</td><td>${item.net_salary}</td><td>`;
                    });
                    cartTable += '</tbody></table>';
                    // Show cart table in a message box
                    frappe.msgprint(cartTable);
                }
            });
        });
    }
});
