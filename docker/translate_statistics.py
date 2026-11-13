import os
import frappe

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init("lms.localhost")
frappe.connect()

print("--- Nạp bản dịch cho trang Thống kê (Statistics) & Biểu đồ ---")

translations = {
    # 1. Các mục người dùng vừa báo
    "Signups per day": "Số lượng đăng ký theo ngày",
    "New accounts on your site show up here, day by day, as people join.": "Tài khoản mới trên trang của bạn sẽ hiển thị ở đây theo từng ngày khi có người đăng ký tham gia.",
    "Enrollments per day": "Lượt ghi danh theo ngày",
    "Each time a learner joins one of your courses, it shows up here.": "Mỗi khi có học viên tham gia một khóa học của bạn, thông tin sẽ hiển thị ở đây.",
    "Certifications per day": "Số chứng chỉ cấp theo ngày",
    "Certificates your learners earn show up here, day by day.": "Chứng chỉ học viên của bạn đạt được sẽ hiển thị ở đây theo từng ngày.",

    # 2. Thẻ số liệu & Biểu đồ trang Statistics
    "Statistics": "Thống kê",
    "Signups": "Đăng ký",
    "Enrollments": "Ghi danh",
    "Certifications": "Chứng chỉ",
    "Completions": "Hoàn thành",
    "Course Completion": "Hoàn thành khóa học",
    "Course Completions": "Khóa học đã hoàn thành",
    "When learners finish a course, you will see how many completed out of everyone enrolled.": "Khi học viên hoàn thành khóa học, bạn sẽ thấy tỷ lệ hoàn thành trên tổng số học viên đã ghi danh.",
    "Published Courses": "Khóa học đã xuất bản",
    "Active Members": "Thành viên tích cực",
    "Course Enrollments": "Lượt ghi danh khóa học",
    "Certified Members": "Học viên được cấp chứng chỉ",
    "Courses": "Khóa học",
    "Completed": "Đã hoàn thành",
}

added_count = 0
updated_count = 0

for src, tr in translations.items():
    existing = frappe.db.sql("SELECT name, translated_text FROM `tabTranslation` WHERE BINARY source_text = %s AND language = 'vi'", (src,))
    if existing:
        doc_name, current_tr = existing[0]
        if current_tr != tr:
            doc = frappe.get_doc("Translation", doc_name)
            doc.translated_text = tr
            doc.save(ignore_permissions=True)
            updated_count += 1
    else:
        doc = frappe.new_doc("Translation")
        doc.language = "vi"
        doc.source_text = src
        doc.translated_text = tr
        doc.insert(ignore_permissions=True)
        added_count += 1

frappe.db.commit()
frappe.clear_cache()
print(f"Đã thêm {added_count} và cập nhật {updated_count} bản dịch cho Statistics!")
