import os
import re

frontend_dir = "/home/frappe/frappe-bench/apps/lms/frontend/src"
all_empty_cases = []

# Regex that matches title and description with possible whitespace/newlines
pattern = re.compile(
    r"title:\s*__\(\s*['\"]([^'\"]+)['\"]\s*\).*?"
    r"description:\s*__\(\s*['\"]([^'\"]+)['\"]\s*\)",
    re.DOTALL
)

for root, _, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith(".vue"):
            with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
                for m in pattern.finditer(content):
                    all_empty_cases.append((f, m.group(1).strip(), m.group(2).strip()))

print(f"Found {len(all_empty_cases)} title-description pairs:")
for f, t, d in all_empty_cases:
    print(f"\n[{f}]")
    print(f"  title: {t}")
    print(f"  desc:  {d}")
