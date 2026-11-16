import frappe


def execute():
	"""Remove retired built-in links, leaving custom links and learning records alone."""
	frappe.db.delete(
		"LMS Sidebar Item",
		{
			"parent": "LMS Settings",
			"parenttype": "LMS Settings",
			"parentfield": "sidebar_items",
			"item_type": "Built-in",
			"name1": ("in", ["jobs", "programming_exercises"]),
		},
	)
	if frappe.db.exists("Web Form", "job-opportunity"):
		frappe.db.set_value("Web Form", "job-opportunity", "published", 0)
	frappe.clear_cache()
