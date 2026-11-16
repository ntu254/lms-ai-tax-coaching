import unittest
from unittest.mock import patch

import frappe
from frappe.website.path_resolver import resolve_redirect

from lms.hooks import get_lms_path, website_redirects


class TestGuestHomeRedirect(unittest.TestCase):
	def test_root_redirects_to_configured_lms_path(self):
		with (
			patch.object(frappe, "get_hooks", return_value=website_redirects),
			patch.object(frappe, "get_website_settings", return_value={}),
			patch.object(frappe.cache, "hget", return_value=None),
			patch.object(frappe.cache, "hset"),
			self.assertRaises(frappe.Redirect) as caught,
		):
			resolve_redirect("", b"campaign=spring")

		self.assertEqual(caught.exception.http_status_code, 302)
		self.assertEqual(frappe.flags.redirect_location, f"/{get_lms_path()}?campaign=spring")

	def test_lms_path_is_not_redirected_back_to_itself(self):
		with (
			patch.object(frappe, "get_hooks", return_value=website_redirects),
			patch.object(frappe, "get_website_settings", return_value={}),
			patch.object(frappe.cache, "hget", return_value=None),
			patch.object(frappe.cache, "hset"),
		):
			resolve_redirect(get_lms_path())
