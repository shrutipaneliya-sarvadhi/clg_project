$(".form-signup").on("submit", function(event) {
    event.preventDefault();
    var args = {};
    args.cmd = "frappe.core.doctype.user.user.sign_up";
    args.email = ($("#signup_email").val() || "").trim();
    args.mobile_no = ($("#mobile_no").val() || "").trim()
    args.redirect_to = get_url_arg("redirect-to") || '';
    args.full_name = ($("#signup_fullname").val() || "").trim();
    if(!args.email || !valid_email(args.email) || !args.full_name) {
        
        return false;
    }
    login.call(args);
    return false;
});