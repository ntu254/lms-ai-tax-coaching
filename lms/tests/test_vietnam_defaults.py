import unittest
from unittest.mock import patch

from lms.install import set_default_currency_for_new_install


class TestVietnamDefaults(unittest.TestCase):
	@patch("lms.install.frappe")
	def test_new_install_defaults_to_vnd(self, frappe):
		frappe.db.get_single_value.return_value = None
		frappe.db.exists.return_value = "VND"
		set_default_currency_for_new_install()
		frappe.db.set_single_value.assert_called_once_with("LMS Settings", "default_currency", "VND")

	@patch("lms.install.frappe")
	def test_existing_currency_is_preserved(self, frappe):
		frappe.db.get_single_value.return_value = "USD"
		set_default_currency_for_new_install()
		frappe.db.set_single_value.assert_not_called()

	@patch("lms.install.frappe")
	def test_missing_vnd_does_not_break_install(self, frappe):
		frappe.db.get_single_value.return_value = None
		frappe.db.exists.return_value = False
		set_default_currency_for_new_install()
		frappe.db.set_single_value.assert_not_called()
