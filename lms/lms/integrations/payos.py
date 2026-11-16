import hashlib
import hmac
import json
import re
import time
import frappe
from frappe import _
import requests

PAYOS_API_URL = "https://api-merchant.payos.vn/v2/payment-requests"


def get_payos_credentials():
	"""Lấy thông tin cấu hình PayOS từ PayOS Settings (Single DocType)."""
	if not frappe.db.exists("DocType", "PayOS Settings"):
		frappe.throw(_("PayOS Settings chưa được cài đặt trong hệ thống."))

	settings = frappe.get_single("PayOS Settings")
	if not settings.enabled:
		frappe.throw(_("Cổng thanh toán PayOS (VietQR) hiện đang tắt trong cài đặt."))

	client_id = settings.client_id
	api_key = settings.get_password("api_key")
	checksum_key = settings.get_password("checksum_key")

	if not (client_id and api_key and checksum_key):
		frappe.throw(_("Vui lòng cấu hình đầy đủ Client ID, API Key và Checksum Key trong PayOS Settings."))

	return client_id, api_key, checksum_key, settings


def generate_order_code() -> int:
	"""Sinh orderCode số nguyên duy nhất cho PayOS (giới hạn an toàn Javascript 9007199254740991)."""
	return int(time.time() * 1000) % 9007199254740991


def clean_description(text: str) -> str:
	"""Nội dung chuyển khoản PayOS tối đa 25 ký tự không dấu và không ký tự đặc biệt."""
	# Loại bỏ dấu tiếng Việt và ký tự lạ
	clean = re.sub(r"[^a-zA-Z0-9 ]", "", text or "")
	clean = clean.strip()[:25]
	return clean or "LMS Hoc Phi VietQR"


def create_signature(data: dict, checksum_key: str) -> str:
	"""
	Tạo chữ ký số HMAC-SHA256 chuẩn theo đặc tả của PayOS.
	Sắp xếp các key theo thứ tự a-z, nối thành chuỗi key1=val1&key2=val2...
	"""
	sorted_keys = sorted(data.keys())
	parts = []
	for k in sorted_keys:
		v = data[k]
		if v is None or v in ("null", "undefined"):
			v = ""
		elif isinstance(v, list):
			v = json.dumps(
				[dict(sorted(item.items())) if isinstance(item, dict) else item for item in v],
				ensure_ascii=False,
				separators=(",", ":"),
			)
		parts.append(f"{k}={v}")
	sign_str = "&".join(parts)

	return hmac.new(
		checksum_key.encode("utf-8"),
		sign_str.encode("utf-8"),
		hashlib.sha256,
	).hexdigest()


def verify_signature(data: dict, signature: str, checksum_key: str) -> bool:
	"""Xác thực chữ ký dữ liệu từ PayOS gửi qua Webhook."""
	if not data or not signature or not checksum_key:
		return False
	expected_sig = create_signature(data, checksum_key)
	return hmac.compare_digest(expected_sig, signature)


def get_payos_payment_url(payment_doc, amount: float, title: str, redirect_to: str) -> str:
	"""
	Tạo liên kết thanh toán PayOS (VietQR) và trả về URL trang thanh toán.
	Lưu lại orderCode vào LMS Payment để đối soát tự động khi webhook gọi đến.
	"""
	client_id, api_key, checksum_key, settings = get_payos_credentials()

	order_code = generate_order_code()
	amount_vnd = int(round(amount))
	description = clean_description(f"LMS {payment_doc.name}")

	# URLs điều hướng sau khi thanh toán hoặc hủy
	site_url = frappe.utils.get_url().rstrip("/")
	return_url = f"{site_url}/{redirect_to.lstrip('/')}"
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

	try:
		res = requests.post(PAYOS_API_URL, json=payload, headers=headers, timeout=15)
		res_data = res.json()
	except Exception as e:
		frappe.throw(_("Không thể kết nối đến máy chủ PayOS: {0}").format(str(e)))

	if res_data.get("code") != "00":
		err_desc = res_data.get("desc") or "Không thể tạo liên kết thanh toán VietQR với PayOS."
		frappe.throw(_(err_desc))

	checkout_url = res_data["data"]["checkoutUrl"]

	# Lưu order_code vào LMS Payment để webhook đối chiếu trong vòng 3-5s
	frappe.db.set_value(
		"LMS Payment",
		payment_doc.name,
		{"payment_id": str(order_code)},
	)

	return checkout_url


@frappe.whitelist(allow_guest=True, methods=["POST"])
def payos_webhook():
	"""
	Webhook nhận thông báo kết quả giao dịch chuyển khoản VietQR từ PayOS.
	Tự động xác nhận giao dịch trong vòng 3-5 giây và kích hoạt ghi danh học viên.
	"""
	raw_body = frappe.request.get_data(as_text=True)
	try:
		body = json.loads(raw_body)
	except Exception:
		frappe.response["http_status_code"] = 400
		return {"error": "Invalid JSON format"}

	data = body.get("data", {})
	signature = body.get("signature")

	if not data or not signature:
		frappe.response["http_status_code"] = 400
		return {"error": "Missing payload data or signature"}

	if not frappe.db.exists("DocType", "PayOS Settings"):
		frappe.response["http_status_code"] = 500
		return {"error": "PayOS Settings not found"}

	settings = frappe.get_single("PayOS Settings")
	checksum_key = settings.get_password("checksum_key")
	if not checksum_key:
		frappe.response["http_status_code"] = 500
		return {"error": "PayOS checksum_key not configured"}

	# 1. Xác thực tính toàn vẹn và chữ ký của Webhook
	if not verify_signature(data, signature, checksum_key):
		frappe.response["http_status_code"] = 403
		return {"error": "Invalid signature"}

	# 2. Xử lý khi giao dịch thành công (code "00")
	if data.get("code") == "00":
		order_code = str(data.get("orderCode"))
		payment_name = frappe.db.get_value("LMS Payment", {"payment_id": order_code}, "name")

		if payment_name:
			payment = frappe.get_doc("LMS Payment", payment_name)
			if not payment.payment_received:
				payment.payment_received = 1
				payment.save(ignore_permissions=True)

				# Báo cáo telemetry
				try:
					from lms.lms import telemetry
					telemetry.payment_received(payment.name)
				except Exception:
					pass

				# Tự động ghi danh học viên vào Khóa học / Lớp học (Batch)
				if settings.auto_enroll and payment.payment_for_document_type and payment.payment_for_document:
					from lms.lms.utils import complete_enrollment
					complete_enrollment(
						payment.name,
						payment.payment_for_document_type,
						payment.payment_for_document,
					)

				# Gửi thông báo realtime qua Socket.io để frontend cập nhật ngay lập tức (3-5s)
				if settings.notify_realtime:
					frappe.publish_realtime(
						"payos_payment_success",
						{
							"payment": payment.name,
							"order_code": order_code,
							"doctype": payment.payment_for_document_type,
							"docname": payment.payment_for_document,
						},
						user=payment.member if payment.member else None,
					)

				frappe.db.commit()

	return {"success": True, "message": "PayOS Webhook processed successfully"}


@frappe.whitelist(allow_guest=True)
def check_payos_payment(payment_id: str):
	"""
	Kiểm tra trạng thái thanh toán theo payment_id (orderCode) hoặc tên LMS Payment.
	Hỗ trợ frontend fallback polling định kỳ 2-3s nếu kết nối realtime gián đoạn.
	"""
	if not payment_id:
		return {"paid": False}

	# Tìm theo tên LMS Payment hoặc theo payment_id (orderCode)
	payment_data = frappe.db.get_value(
		"LMS Payment",
		{"name": payment_id},
		["name", "payment_received", "payment_for_document_type", "payment_for_document"],
		as_dict=True,
	) or frappe.db.get_value(
		"LMS Payment",
		{"payment_id": payment_id},
		["name", "payment_received", "payment_for_document_type", "payment_for_document"],
		as_dict=True,
	)

	if not payment_data:
		return {"paid": False}

	return {
		"paid": bool(payment_data.payment_received),
		"payment_name": payment_data.name,
		"doctype": payment_data.payment_for_document_type,
		"docname": payment_data.payment_for_document,
	}
