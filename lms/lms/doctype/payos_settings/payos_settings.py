import frappe
from frappe import _
from frappe.model.document import Document
import requests


class PayOSSettings(Document):
	def validate(self):
		if self.enabled:
			if not self.client_id:
				frappe.throw(_("Vui lòng nhập Client ID của PayOS."))
			if not (self.api_key or self.get_password("api_key")):
				frappe.throw(_("Vui lòng nhập API Key của PayOS."))
			if not (self.checksum_key or self.get_password("checksum_key")):
				frappe.throw(_("Vui lòng nhập Checksum Key của PayOS."))

		# Tự động cập nhật Webhook URL
		base_url = frappe.utils.get_url().rstrip("/")
		self.webhook_url = f"{base_url}/api/method/lms.lms.integrations.payos.payos_webhook"

	@frappe.whitelist()
	def confirm_webhook_with_payos(self):
		"""Gửi yêu cầu đăng ký/xác thực Webhook URL tự động lên hệ thống PayOS."""
		client_id = self.client_id
		api_key = self.get_password("api_key")
		if not (client_id and api_key):
			frappe.throw(_("Chưa cấu hình Client ID và API Key để xác thực."))

		base_url = frappe.utils.get_url().rstrip("/")
		webhook_url = f"{base_url}/api/method/lms.lms.integrations.payos.payos_webhook"

		headers = {
			"x-client-id": client_id,
			"x-api-key": api_key,
			"Content-Type": "application/json",
		}
		payload = {"webhookUrl": webhook_url}

		try:
			res = requests.post(
				"https://api-merchant.payos.vn/v2/payment-requests/confirm-webhook",
				json=payload,
				headers=headers,
				timeout=15,
			)
			res_data = res.json()
			if res_data.get("code") == "00":
				self.webhook_status = "Đã xác thực thành công (Active)"
				self.save(ignore_permissions=True)
				return {
					"success": True,
					"message": _("Xác thực Webhook PayOS thành công! Hệ thống sẵn sàng nhận thông báo giao dịch VietQR."),
				}
			else:
				desc = res_data.get("desc") or res.text
				frappe.throw(_("PayOS từ chối xác thực Webhook: {0}").format(desc))
		except Exception as e:
			frappe.throw(_("Lỗi khi kết nối đến PayOS: {0}").format(str(e)))
