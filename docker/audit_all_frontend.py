import os
import re

frontend_dir = "/home/frappe/frappe-bench/apps/lms/frontend/src"
all_strings = set()

# Pattern for __('...')
p_trans = re.compile(r"__\(\s*['\"]([^'\"]+)['\"]")
# Pattern for empty-title="..." or empty-description="..." or title: '...'
p_empty = re.compile(r"empty-(?:title|description|name)=['\"]([^'\"]+)['\"]")

for root, _, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith((".vue", ".js", ".ts")):
            with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fp:
                text = fp.read()
                for m in p_trans.finditer(text):
                    all_strings.add(m.group(1).strip())
                for m in p_empty.finditer(text):
                    all_strings.add(m.group(1).strip())

os.chdir("/home/frappe/frappe-bench/sites")
import frappe
frappe.init("lms.localhost")
frappe.connect()

from frappe.translate import get_all_translations
current = get_all_translations("vi")

missing = [s for s in all_strings if s and s not in current]
print(f"Total missing strings: {len(missing)}")

# Find strings related to jobs, empty states, courses, batches, etc.
keywords = ["job", "post", "share", "open", "close", "course", "batch", "lesson", "empty", "no ", "create", "welcome", "learn"]
priority_missing = {}
for s in missing:
    sl = s.lower()
    if any(k in sl for k in keywords) and len(s) < 150:
        priority_missing[s] = True

print(f"Priority missing count: {len(priority_missing)}")
for s in sorted(priority_missing.keys())[:100]:
    print(" -", repr(s))
