import os
import frappe

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init("lms.localhost")
frappe.connect()

from frappe.translate import get_all_translations
tr = get_all_translations("vi")

tests = [
    "Post a job",
    "Share openings with the people who learn on your site, from internships to full-time roles.",
    "No closed jobs",
    "Jobs you close move here, so you keep a record of past openings.",
    "Publish your first course",
    "Teach people together in a batch",
    "Create your first quiz"
]

for t in tests:
    print(f"[{t}] -> [{tr.get(t)}]")
