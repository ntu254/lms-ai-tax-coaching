import unittest
from types import SimpleNamespace
from unittest.mock import patch

from werkzeug.exceptions import NotFound

from lms.lms.desk import disable_studio_requests, remove_studio_navigation


class TestDeskNavigation(unittest.TestCase):
	def test_removes_only_frappe_studio_entries(self):
		studio = {"link_type": "Sidebar", "link_to": "Studio"}
		flow = {"link_type": "Sidebar", "link_to": "Flow"}
		bootinfo = {
			"app_data": [
				{
					"app_name": "frappe",
					"module_icons": [{"route": "/studio"}, {"route": "/flow"}],
					"dock": [studio, flow],
				},
				{"app_name": "lms", "module_icons": [{"route": "/studio"}], "dock": [studio]},
			],
			"dock": {"frappe": [studio, flow], "lms": [studio]},
			"module_sidebars": {"Studio": {}, "Flow": {"name": "Flow"}},
			"studio_apps": [{"route": "/example"}],
		}

		remove_studio_navigation(bootinfo)

		self.assertEqual(bootinfo["app_data"][0]["module_icons"], [{"route": "/flow"}])
		self.assertEqual(bootinfo["app_data"][0]["dock"], [flow])
		self.assertEqual(bootinfo["dock"]["frappe"], [flow])
		self.assertEqual(bootinfo["module_sidebars"], {"Flow": {"name": "Flow"}})
		self.assertEqual(bootinfo["app_data"][1]["dock"], [studio])
		self.assertEqual(bootinfo["dock"]["lms"], [studio])
		self.assertEqual(bootinfo["studio_apps"], [])

	def test_accepts_missing_desk_data(self):
		remove_studio_navigation({})

	def test_studio_editor_and_api_are_unavailable(self):
		for path in ("/studio", "/studio/example", "/api/method/frappe.studio.api.example"):
			with self.subTest(path=path), patch("lms.lms.desk.frappe") as frappe:
				frappe.local.request = SimpleNamespace(path=path)
				frappe.form_dict = {}
				with self.assertRaises(NotFound):
					disable_studio_requests()

	def test_other_requests_are_unaffected(self):
		with patch("lms.lms.desk.frappe") as frappe:
			frappe.local.request = SimpleNamespace(path="/lms/courses")
			frappe.form_dict = {}
			disable_studio_requests()
