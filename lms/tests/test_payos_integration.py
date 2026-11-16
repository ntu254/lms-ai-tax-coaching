import hashlib
import hmac
import json
import unittest
from unittest.mock import MagicMock, patch
import sys

import importlib.machinery
import types

# Mock frappe and requests if not in bench environment
if "frappe" not in sys.modules:
	frappe_mod = types.ModuleType("frappe")
	frappe_mod.__spec__ = importlib.machinery.ModuleSpec("frappe", None)
	frappe_mod.__path__ = []
	frappe_mod._ = lambda x: x
	frappe_mod.whitelist = lambda **kw: (lambda f: f)
	frappe_mod.rate_limit = lambda **kw: (lambda f: f)
	sys.modules["frappe"] = frappe_mod

	utils_mod = types.ModuleType("frappe.utils")
	utils_mod.__spec__ = importlib.machinery.ModuleSpec("frappe.utils", None)
	utils_mod.get_url = lambda *a, **k: "http://localhost:8000"
	sys.modules["frappe.utils"] = utils_mod

	telemetry_mod = types.ModuleType("frappe.utils.telemetry")
	telemetry_mod.__spec__ = importlib.machinery.ModuleSpec("frappe.utils.telemetry", None)
	telemetry_mod.capture = lambda *a, **k: None
	sys.modules["frappe.utils.telemetry"] = telemetry_mod

	rate_limiter_mod = types.ModuleType("frappe.rate_limiter")
	rate_limiter_mod.__spec__ = importlib.machinery.ModuleSpec("frappe.rate_limiter", None)
	rate_limiter_mod.rate_limit = lambda **kw: (lambda f: f)
	sys.modules["frappe.rate_limiter"] = rate_limiter_mod

if "requests" not in sys.modules:
	req_mod = types.ModuleType("requests")
	req_mod.__spec__ = importlib.machinery.ModuleSpec("requests", None)
	sys.modules["requests"] = req_mod

if "lms.lms.utils" not in sys.modules:
	mock_utils = types.ModuleType("lms.lms.utils")
	mock_utils.__spec__ = importlib.machinery.ModuleSpec("lms.lms.utils", None)
	mock_utils.complete_enrollment = MagicMock()
	mock_utils.get_lms_route = lambda: "lms"
	mock_utils.format_number_into_currency = lambda n, c: f"{n:,.0f} {c}"
	sys.modules["lms.lms.utils"] = mock_utils



from lms.lms.integrations.payos import (
	clean_description,
	create_signature,
	generate_order_code,
	verify_signature,
)


class TestPayOSIntegration(unittest.TestCase):
	def test_clean_description(self):
		# Must strip special characters and limit to 25 chars
		desc = clean_description("Học phí Khóa Thuế & BCTC @2026!")
		self.assertTrue(len(desc) <= 25)
		self.assertNotIn("@", desc)
		self.assertNotIn("!", desc)
		self.assertNotIn("&", desc)

	def test_create_and_verify_signature(self):
		checksum_key = "test_checksum_key_123456"
		data = {
			"orderCode": 123456,
			"amount": 2500000,
			"description": "LMS PAY001",
			"cancelUrl": "https://example.com/cancel",
			"returnUrl": "https://example.com/return",
		}

		signature = create_signature(data, checksum_key)
		self.assertIsInstance(signature, str)
		self.assertEqual(len(signature), 64)  # SHA256 hex string

		# Verify signature passes
		self.assertTrue(verify_signature(data, signature, checksum_key))

		# Tampered data must fail
		tampered_data = dict(data, amount=1000)
		self.assertFalse(verify_signature(tampered_data, signature, checksum_key))

		# Wrong key must fail
		self.assertFalse(verify_signature(data, signature, "wrong_key"))

	def test_signature_matches_payos_documented_webhook(self):
		data = {
			"orderCode": 123, "amount": 3000, "description": "VQRIO123",
			"accountNumber": "12345678", "reference": "TF230204212323",
			"transactionDateTime": "2023-02-04 18:25:00", "currency": "VND",
			"paymentLinkId": "124c33293c43417ab7879e14c8d9eb18",
			"code": "00", "desc": "Thành công", "counterAccountBankId": "",
			"counterAccountBankName": "", "counterAccountName": "",
			"counterAccountNumber": "", "virtualAccountName": "", "virtualAccountNumber": "",
		}
		key = "1a54716c8f0efb2744fb28b6e38b25da7f67a925d98bc1c18bd8faaecadd7675"
		self.assertEqual(create_signature(data, key), "412e915d2871504ed31be63c8f62a149a4410d34c4c42affc9006ef9917eaa03")

	def test_order_code_range(self):
		code = generate_order_code()
		self.assertIsInstance(code, int)
		self.assertGreater(code, 0)
		self.assertLess(code, 9007199254740991)

	@patch("lms.lms.integrations.payos.frappe")
	def test_payos_webhook_success_enrolls_student(self, mock_frappe_env):
		from lms.lms.integrations.payos import payos_webhook

		checksum_key = "test_checksum_key_secret"
		webhook_data = {
			"orderCode": 998877,
			"amount": 3500000,
			"description": "LMS PAY001",
			"code": "00",
		}
		signature = create_signature(webhook_data, checksum_key)
		payload = json.dumps({"data": webhook_data, "signature": signature})

		mock_frappe_env.request.get_data.return_value = payload
		mock_frappe_env.db.exists.return_value = True

		mock_settings = MagicMock()
		mock_settings.get_password.return_value = checksum_key
		mock_settings.auto_enroll = 1
		mock_settings.notify_realtime = 1
		mock_frappe_env.get_single.return_value = mock_settings

		mock_frappe_env.db.get_value.return_value = "PAY-001"

		mock_payment = MagicMock()
		mock_payment.name = "PAY-001"
		mock_payment.payment_received = 0
		mock_payment.payment_for_document_type = "LMS Course"
		mock_payment.payment_for_document = "thue-chuyen-sau-2026"
		mock_payment.member = "student@example.com"
		mock_frappe_env.get_doc.return_value = mock_payment

		with patch("lms.lms.utils.complete_enrollment") as mock_complete:
			res = payos_webhook()

			self.assertTrue(res.get("success"))
			self.assertEqual(mock_payment.payment_received, 1)
			mock_payment.save.assert_called_once_with(ignore_permissions=True)
			mock_complete.assert_called_once_with("PAY-001", "LMS Course", "thue-chuyen-sau-2026")
			mock_frappe_env.publish_realtime.assert_called_once()


if __name__ == "__main__":
	unittest.main()
