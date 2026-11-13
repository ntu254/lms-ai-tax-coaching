import os
import re

frontend_dir = "/home/frappe/frappe-bench/apps/lms/frontend/src"
keys = set()
pattern = re.compile(r"__\(\s*['\"]([^'\"]+)['\"]")

for root, _, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith((".vue", ".js", ".ts")):
            with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fp:
                for match in pattern.finditer(fp.read()):
                    keys.add(match.group(1))

print(f"Total __() translation keys found in frontend: {len(keys)}")

os.chdir("/home/frappe/frappe-bench/sites")
import frappe
frappe.init("lms.localhost")
frappe.connect()

from frappe.translate import get_all_translations
current_vi = get_all_translations("vi")

missing = [k for k in keys if k not in current_vi]
print(f"Missing in vi translations: {len(missing)}")
print("\n--- Missing translation keys in Frontend ---")
for m in sorted(missing)[:100]:
    print(f"  {repr(m)}:")
