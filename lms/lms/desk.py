"""LMS-specific changes to the Frappe Desk navigation."""

import frappe
from werkzeug.exceptions import NotFound


def remove_studio_navigation(bootinfo):
	"""Hide Frappe Studio's launcher and dock entry without changing its data."""
	for app in bootinfo.get("app_data") or []:
		if app.get("app_name") != "frappe":
			continue
		app["module_icons"] = [
			icon for icon in app.get("module_icons") or [] if icon.get("route") != "/studio"
		]
		app["dock"] = [entry for entry in app.get("dock") or [] if not is_studio_sidebar(entry)]

	dock = bootinfo.get("dock") or {}
	if "frappe" in dock:
		dock["frappe"] = [entry for entry in dock["frappe"] if not is_studio_sidebar(entry)]

	(bootinfo.get("module_sidebars") or {}).pop("Studio", None)
	if "studio_apps" in bootinfo:
		bootinfo["studio_apps"] = []


def is_studio_sidebar(entry):
	return entry.get("link_type") == "Sidebar" and entry.get("link_to") == "Studio"


def disable_studio_requests():
	"""Retire Studio's editor and API without removing framework-owned files."""
	path = frappe.local.request.path.rstrip("/")
	command = frappe.form_dict.get("cmd") or ""
	if (
		path == "/studio"
		or path.startswith("/studio/")
		or path.startswith("/api/method/frappe.studio.")
		or path.startswith("/api/v2/method/frappe.studio.")
		or command.startswith("frappe.studio.")
	):
		raise NotFound()
