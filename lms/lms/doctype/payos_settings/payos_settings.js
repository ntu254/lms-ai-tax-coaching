frappe.ui.form.on("PayOS Settings", {
	refresh: function(frm) {
		if (frm.doc.enabled && frm.doc.client_id) {
			frm.add_custom_button(__("Xác thực Webhook với PayOS"), function() {
				frappe.call({
					doc: frm.doc,
					method: "confirm_webhook_with_payos",
					freeze: true,
					freeze_message: __("Đang gửi yêu cầu đăng ký Webhook lên PayOS..."),
					callback: function(r) {
						if (r.message && r.message.success) {
							frappe.msgprint({
								title: __("Thành công"),
								indicator: "green",
								message: r.message.message
							});
							frm.reload_doc();
						}
					}
				});
			}).addClass("btn-primary");
		}
	}
});
