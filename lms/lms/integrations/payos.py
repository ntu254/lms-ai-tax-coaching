import hashlib
import hmac
import json
import re
import time
import frappe
from frappe import _
import requests

from lms.lms.utils import complete_enrollment, get_lms_route

PAYOS_API_URL = "https://api-merchant.payos.vn/v2/payment-requests"


def get_payos_credentials():
	settings = frappe.get_single("PayOS Settings")
	if not settings.enabled:
		frappe.throw(_("PayOS hiện đang tắt trong cài đặt."))
	client_id = settings.client_id
	api_key = settings.get_password("api_key")
	checksum_key = settings.get_password("checksum_key")
	if not (client_id and api_key and checksum_key):
		frappe.throw(_("Vui lòng cấu hình đầy đủ Client ID, API Key và Checksum Key trong PayOS Settings."))
	return client_id, api_key, checksum_key


def generate_order_code() -> int:
	"""Generate a unique integer orderCode for PayOS (max 9007199254740991)."""
	return int(time.time() * 1000) % 9007199254740991


def clean_description(text: str) -> str:
	"""PayOS description must be max 25 chars without special symbols."""
	clean = re.sub(r"[^a-zA-Z0-9 ]", "", text or "")
	clean = clean.strip()[:25]
	return clean or "Hoc phi LMS"


def create_signature(data: dict, checksum_key: str) -> str:
	"""Create HMAC-SHA256 signature for PayOS by sorting keys alphabetically."""
	sorted_keys = sorted(data.keys())
	sign_str = "&".join(f"{k}={data[k]}" for k in sorted_keys if data[k] is not None)
	return hmac.new(
		checksum_key.encode("utf-8"),
		sign_str.encode("utf-8"),
		hashlib.sha256,
	).hexdigest()


def get_payos_payment_url(payment_doc, amount: float, title: str, redirect_to: str) -> str:
	"""Create a PayOS payment request and return the checkout URL."""
	client_id, api_key, checksum_key = get_payos_credentials()

	order_code = generate_order_code()
	amount_vnd = int(round(amount))
	description = clean_description(f"LMS {payment_doc.name}")

	# Return and cancel URLs
	site_url = frappe.utils.get_url()
	return_url = f"{site_url}/{get_lms_route()}/{redirect_to.lstrip('/')}"
	cancel_url = return_url

	payload = {
		"orderCode": order_code,
		"amount": amount_vnd,
		"description": description,
		"cancelUrl": cancel_url,
		"returnUrl": return_url,
	}

	payload["signature"] = create_signature(payload, checksum_key)

	headers = {
		"x-client-id": client_id,
		"x-api-key": api_key,
		"Content-Type": "application/json",
	}

	res = requests.post(PAYOS_API_URL, json=payload, headers=headers, timeout=15)
	res_data = res.json()

	if res_data.get("code") != "00":
		err_desc = res_data.get("desc") or "Không thể tạo liên kết thanh toán PayOS."
		frappe.throw(_(err_desc))

	checkout_url = res_data["data"]["checkoutUrl"]

	# Save order_code as payment_id on the LMS Payment record
	frappe.db.set_value(
		"LMS Payment",
		payment_doc.name,
		{"payment_id": str(order_code)},
	)

	return checkout_url


@frappe.whitelist(allow_guest=True, methods=["POST"])
def payos_webhook():
	"""Webhook endpoint to receive payment notifications from PayOS."""
	raw_body = frappe.request.get_data(as_text=True)
	try:
		body = json.loads(raw_body)
	except Exception:
		frappe.response["http_status_code"] = 400
		return {"error": "Invalid JSON"}

	data = body.get("data", {})
	signature = body.get("signature")

	if not data or not signature:
		frappe.response["http_status_code"] = 400
		return {"error": "Missing data or signature"}

	settings = frappe.get_single("PayOS Settings")
	checksum_key = settings.get_password("checksum_key")
	if not checksum_key:
		frappe.response["http_status_code"] = 500
		return {"error": "PayOS not configured"}

	# Verify webhook signature
	expected_sig = create_signature(data, checksum_key)
	if not hmac.compare_digest(expected_sig, signature):
		frappe.response["http_status_code"] = 403
		return {"error": "Invalid signature"}

	# Check payment success
	if data.get("code") == "00":
		order_code = str(data.get("orderCode"))
		payment_name = frappe.db.get_value("LMS Payment", {"payment_id": order_code}, "name")

		if payment_name:
			payment = frappe.get_doc("LMS Payment", payment_name)
			if not payment.payment_received:
				payment.payment_received = 1
				payment.save(ignore_permissions=True)

				# Enroll student automatically
				if payment.payment_for_document_type and payment.payment_for_document:
					complete_enrollment(
						payment.name,
						payment.payment_for_document_type,
						payment.payment_for_document,
					)

	return {"success": True}
