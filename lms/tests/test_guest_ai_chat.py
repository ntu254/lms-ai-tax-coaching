import unittest
from unittest.mock import MagicMock, patch
import sys
import importlib.machinery
import types

# Mock frappe if not in bench environment
if "frappe" not in sys.modules:
	frappe_mod = types.ModuleType("frappe")
	frappe_mod.__spec__ = importlib.machinery.ModuleSpec("frappe", None)
	frappe_mod.__path__ = []
	frappe_mod._ = lambda x: x
	frappe_mod.whitelist = lambda **kw: (lambda f: f)
	frappe_mod.rate_limit = lambda **kw: (lambda f: f)
	frappe_mod.conf = {}
	frappe_mod.get_all = MagicMock(return_value=[])
	sys.modules["frappe"] = frappe_mod

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
	mock_utils.format_number_into_currency = lambda n, c: f"{n:,.0f} {c}"
	mock_utils.guest_access_allowed = lambda: True
	sys.modules["lms.lms.utils"] = mock_utils

from lms.lms.ai_coach import SYSTEM_PROMPT, get_live_lms_context, guest_ai_chat


class TestGuestAiChat(unittest.TestCase):
	def test_empty_message(self):
		res = guest_ai_chat("")
		self.assertIn("Vui lòng nhập câu hỏi", res.get("response", ""))

	@patch.dict("os.environ", {}, clear=True)
	@patch("lms.lms.ai_coach.get_live_lms_context")
	@patch("lms.lms.ai_coach.frappe.conf", {})
	def test_unconfigured_ai_returns_unavailable_without_loading_catalog(self, context):
		result = guest_ai_chat("Tìm khóa học thuế")
		self.assertEqual(result["status"], "unavailable")
		self.assertIn("tạm thời không khả dụng", result["response"])
		self.assertNotIn("DANH SÁCH", result["response"])
		context.assert_not_called()

	@patch("lms.lms.ai_coach.frappe.conf", {"gemini_api_key": "test-key"})
	@patch("lms.lms.ai_coach.get_live_lms_context", return_value="catalog")
	@patch("lms.lms.ai_coach.call_gemini_api", return_value=None)
	def test_failed_ai_returns_unavailable(self, call_ai, context):
		result = guest_ai_chat("Tìm khóa học")
		self.assertEqual(result["status"], "unavailable")
		self.assertIn("tạm thời không khả dụng", result["response"])

	@patch("lms.lms.ai_coach.frappe.conf", {"gemini_api_key": "test-key"})
	@patch("lms.lms.ai_coach.get_live_lms_context", return_value="catalog")
	@patch("lms.lms.ai_coach.call_gemini_api", return_value="Khóa học phù hợp")
	def test_available_ai_returns_answer(self, call_ai, context):
		self.assertEqual(guest_ai_chat("Tìm khóa học"), {"response": "Khóa học phù hợp", "status": "success"})

	def test_model_is_instructed_to_limit_scope_and_use_catalog(self):
		self.assertIn("Chỉ hỗ trợ khách tìm hiểu khóa học", SYSTEM_PROMPT)
		self.assertIn("Không tự tạo thông tin", SYSTEM_PROMPT)
		self.assertIn("ngoài đào tạo", SYSTEM_PROMPT)

	@patch("lms.lms.ai_coach.guest_access_allowed", return_value=False)
	@patch("lms.lms.ai_coach.frappe.get_all")
	def test_guest_access_disabled_does_not_read_catalog(self, get_all, access):
		self.assertEqual(get_live_lms_context(), "")
		get_all.assert_not_called()


if __name__ == "__main__":
	unittest.main()
