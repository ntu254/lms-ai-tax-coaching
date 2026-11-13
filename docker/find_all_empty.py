import os
import re

frontend_dir = "/home/frappe/frappe-bench/apps/lms/frontend/src"
all_empty = []

for root, _, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith(".vue"):
            with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
                # find emptyState computed or objects
                matches = re.findall(r"title:\s*__\(['\"]([^'\"]+)['\"]\)", content)
                for m in matches:
                    all_empty.append((f, "title", m))
                desc_matches = re.findall(r"description:\s*__\(['\"]([^'\"]+)['\"]\)", content)
                for m in desc_matches:
                    all_empty.append((f, "desc", m))

print(f"Total empty state strings found: {len(all_empty)}")
for f, kind, s in all_empty:
    print(f"[{f}] {kind}: {s}")
