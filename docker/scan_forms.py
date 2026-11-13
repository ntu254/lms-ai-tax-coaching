import os
import re

forms_dir = "/home/frappe/frappe-bench/apps/lms/frontend/src/pages/Forms"
form_keys = set()
pattern = re.compile(r"__\(\s*['\"]([^'\"]+)['\"]\s*\)")

for root, _, files in os.walk(forms_dir):
    for f in files:
        if f.endswith((".vue", ".js", ".ts")):
            with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fp:
                for match in pattern.finditer(fp.read()):
                    form_keys.add(match.group(1).strip())

os.chdir("/home/frappe/frappe-bench/sites")
import frappe
frappe.init("lms.localhost")
frappe.connect()

from frappe.translate import get_all_translations
current = get_all_translations("vi")

missing = [k for k in form_keys if k not in current]
print(f"Total keys in Forms: {len(form_keys)}")
print(f"Missing keys in Forms: {len(missing)}")
for k in sorted(missing):
    print(" -", repr(k))
