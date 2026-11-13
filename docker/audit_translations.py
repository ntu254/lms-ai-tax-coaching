import os

po_path = "/home/frappe/frappe-bench/apps/lms/lms/locale/vi.po"
with open(po_path, "r", encoding="utf-8") as f:
    content = f.read()

entries = content.split("\n\n")
untranslated = []
for entry in entries:
    lines = [l.strip() for l in entry.split("\n") if l.strip()]
    msgid = None
    msgstr = None
    for l in lines:
        if l.startswith('msgid "'):
            msgid = l[7:-1]
        elif l.startswith('msgstr "'):
            msgstr = l[8:-1]
    if msgid and msgstr == "" and len(msgid) > 1 and not msgid.startswith("{"):
        untranslated.append(msgid)

print(f"Total untranslated in LMS: {len(untranslated)}")
print("\n--- Top common untranslated strings in LMS ---")
for s in untranslated[:60]:
    print(" -", s)
