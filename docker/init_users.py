import os
import frappe
from frappe.utils.password import update_password

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init("lms.localhost")
frappe.connect()

print("--- Thiết lập tài khoản và mật khẩu cho các Actor trong Frappe Learning ---")

# 1. Administrator (Toàn quyền)
update_password("Administrator", "admin")

# 2. Moderator (Jannat Patel)
if frappe.db.exists("User", "jannat@example.com"):
    update_password("jannat@example.com", "123456")

# 3. Course Creator / Giảng viên (teacher@example.com)
if not frappe.db.exists("User", "teacher@example.com"):
    user = frappe.new_doc("User")
    user.email = "teacher@example.com"
    user.first_name = "Nguyễn Văn"
    user.last_name = "Giảng Viên"
    user.full_name = "Nguyễn Văn Giảng Viên"
    user.send_welcome_email = False
    user.language = "vi"
    user.time_zone = "Asia/Ho_Chi_Minh"
    user.append("roles", {"role": "Course Creator"})
    user.append("roles", {"role": "LMS Student"})
    user.insert(ignore_permissions=True)
update_password("teacher@example.com", "123456")

# 4. Batch Evaluator / Người đánh giá (Ashley Ippolito)
if frappe.db.exists("User", "ash@ipp.com"):
    update_password("ash@ipp.com", "123456")

# 5. LMS Student / Học viên (John Doe & Jane Smith)
if frappe.db.exists("User", "john.doe@example.com"):
    update_password("john.doe@example.com", "123456")

if frappe.db.exists("User", "jane.smith@example.com"):
    update_password("jane.smith@example.com", "123456")

frappe.db.commit()
print("Đã thiết lập tài khoản & mật khẩu các Actor thành công!")
