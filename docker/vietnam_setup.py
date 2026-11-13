import os
import frappe

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init("lms.localhost")
frappe.connect()

print("--- Áp dụng thiết lập tối ưu hóa riêng cho thị trường Việt Nam ---")

# 1. Cài đặt Hệ thống (System Settings)
sys = frappe.get_doc("System Settings")
sys.country = "Vietnam"
sys.time_zone = "Asia/Ho_Chi_Minh"
sys.language = "vi"
sys.currency = "VND"
sys.currency_symbol = "₫"
sys.date_format = "dd-mm-yyyy"
sys.time_format = "HH:mm:ss"
sys.number_format = "#,###"
sys.save(ignore_permissions=True)
print("1. Đã cấu hình System Settings chuẩn Việt Nam: Múi giờ Asia/Ho_Chi_Minh, Tiền tệ VND (₫), Ngày dd-mm-yyyy")

# 2. Cài đặt LMS (LMS Settings)
lms = frappe.get_doc("LMS Settings")
lms.default_currency = "VND"
lms.apply_gst = 0
lms.show_usd_equivalent = 0
lms.save(ignore_permissions=True)
print("2. Đã cấu hình LMS Settings: Tiền tệ khóa học VND, tắt thuế ngoại GST và tắt quy đổi USD")

# 3. Giới hạn danh sách ngôn ngữ: Chỉ giữ lại Tiếng Việt và Tiếng Anh
frappe.db.sql("UPDATE `tabLanguage` SET enabled = 0 WHERE name NOT IN ('vi', 'en')")
frappe.db.sql("UPDATE `tabLanguage` SET enabled = 1 WHERE name IN ('vi', 'en')")
print("3. Đã giới hạn ngôn ngữ: Chỉ cho phép Tiếng Việt (vi) và Tiếng Anh (en)")

# 4. Cập nhật tiền tệ VND trong bảng Currency
if frappe.db.exists("Currency", "VND"):
    cur = frappe.get_doc("Currency", "VND")
    cur.symbol = "₫"
    cur.enabled = 1
    cur.fraction = ""
    cur.fraction_units = 0
    cur.smallest_currency_fraction_value = 1
    cur.save(ignore_permissions=True)
    print("4. Đã tối ưu định dạng tiền tệ VND: Ký hiệu ₫, không dùng số thập phân lẻ")

# 5. Gán ngôn ngữ tiếng Việt cho các tài khoản hiện tại
users = frappe.get_all("User", filters={"user_type": "System User", "name": ["not in", ["Guest"]]}, pluck="name")
for u in users:
    usr = frappe.get_doc("User", u)
    if not usr.language or usr.language != "en":
        usr.language = "vi"
        usr.time_zone = "Asia/Ho_Chi_Minh"
        usr.save(ignore_permissions=True)
print(f"5. Đã đặt ngôn ngữ mặc định Tiếng Việt & múi giờ VN cho {len(users)} người dùng hệ thống")

# 6. Cập nhật các batch hiện có sang múi giờ Asia/Ho_Chi_Minh
batches = frappe.get_all("LMS Batch", pluck="name")
for b in batches:
    batch = frappe.get_doc("LMS Batch", b)
    if batch.timezone != "Asia/Ho_Chi_Minh":
        batch.timezone = "Asia/Ho_Chi_Minh"
        batch.save(ignore_permissions=True)
print(f"6. Đã kiểm tra và cập nhật múi giờ cho {len(batches)} đợt học (batch)")

frappe.db.commit()
frappe.clear_cache()
print("--> Hoàn tất tối ưu hóa toàn bộ hệ thống cho Việt Nam thành công!")
