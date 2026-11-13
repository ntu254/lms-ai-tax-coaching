import os
import re

os.chdir("/home/frappe/frappe-bench/sites")
import frappe
frappe.init("lms.localhost")
frappe.connect()

from frappe.translate import get_all_translations
current_vi = get_all_translations("vi")

frontend_dir = "/home/frappe/frappe-bench/apps/lms/frontend/src"
keys = set()
pattern = re.compile(r"__\(\s*['\"]([^'\"]+)['\"]")

for root, _, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith((".vue", ".js", ".ts")):
            with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fp:
                for match in pattern.finditer(fp.read()):
                    keys.add(match.group(1))

missing = [k for k in keys if k not in current_vi and len(k) <= 60 and not k.startswith("<")]
print(f"Total short UI keys missing: {len(missing)}")

# Print categorized
print("\n--- Short missing keys ---")
for k in sorted(missing)[:150]:
    print(k)
