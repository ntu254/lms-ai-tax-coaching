import os
import frappe

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init("lms.localhost")
frappe.connect()

# 1. Clean up corrupted translations
frappe.db.sql("DELETE FROM `tabTranslation` WHERE language = 'vi'")

# 2. Comprehensive, accurately accented Vietnamese dictionary
translations = {
    # Core navigation & modules
    "Learning": "Học tập",
    "Courses": "Khóa học",
    "Course": "Khóa học",
    "Batches": "Đợt học",
    "Batch": "Đợt học",
    "Chapters": "Chương học",
    "Chapter": "Chương học",
    "Lessons": "Bài học",
    "Lesson": "Bài học",
    "Quizzes": "Bài kiểm tra",
    "Quiz": "Bài kiểm tra",
    "Questions": "Câu hỏi",
    "Question": "Câu hỏi",
    "Assignments": "Bài tập",
    "Assignment": "Bài tập",
    "Programming Exercises": "Bài tập lập trình",
    "Programming Exercise": "Bài tập lập trình",
    "Certificates": "Chứng chỉ",
    "Certificate": "Chứng chỉ",
    "Certification": "Chứng chỉ",
    "Programs": "Lộ trình học tập",
    "Program": "Lộ trình học",
    "Enrollments": "Ghi danh",
    "Enrollment": "Ghi danh",
    "Course Completed": "Khóa học hoàn thành",
    "Live Classes": "Lớp học trực tuyến",
    "Live Class": "Lớp học trực tuyến",
    "Coupons": "Mã giảm giá",
    "Coupon": "Mã giảm giá",
    "Reviews": "Đánh giá",
    "Review": "Đánh giá",
    "Evaluation": "Đánh giá",
    "Evaluations": "Đánh giá",
    "Evaluation Request": "Yêu cầu đánh giá",
    "Badges": "Huy hiệu",
    "Badge": "Huy hiệu",
    "Signups": "Đăng ký",
    
    # DocType Labels
    "LMS Course": "Khóa học",
    "Course Chapter": "Chương học",
    "Course Lesson": "Bài học",
    "LMS Batch": "Đợt học / Lớp học",
    "LMS Enrollment": "Ghi danh khóa học",
    "LMS Quiz": "Bài kiểm tra (Quiz)",
    "LMS Question": "Câu hỏi kiểm tra",
    "LMS Assignment": "Bài tập nộp",
    "LMS Assignment Submission": "Bài nộp bài tập",
    "LMS Quiz Submission": "Bài nộp kiểm tra",
    "LMS Quiz Violation Log": "Nhật ký vi phạm bài thi",
    "Quiz Submission": "Bài nộp kiểm tra",
    "Quiz Violation Log": "Nhật ký vi phạm bài thi",
    "LMS Programming Exercise": "Bài tập lập trình",
    "LMS Programming Exercise Submission": "Bài nộp lập trình",
    "LMS Certificate": "Chứng chỉ",
    "LMS Certificate Request": "Yêu cầu cấp chứng chỉ",
    "LMS Certificate Evaluation": "Đánh giá cấp chứng chỉ",
    "LMS Program": "Lộ trình học tập",
    "LMS Payment": "Giao dịch thanh toán",
    "LMS Coupon": "Mã giảm giá",
    "LMS Live Class": "Lớp học trực tuyến",
    "LMS Course Review": "Đánh giá khóa học",
    "LMS Course Interest": "Quan tâm khóa học",
    "Interest": "Quan tâm",
    "LMS Settings": "Cài đặt LMS",
    "LMS Zoom Settings": "Cài đặt Zoom",
    "LMS Google Meet Settings": "Cài đặt Google Meet",
    "LMS Batch Timetable": "Thời khóa biểu lớp học",
    "Course Data": "Dữ liệu khóa học",
    "Course Stats": "Thống kê khóa học",
    
    # Workspace & Cards
    "Get Started": "Bắt đầu",
    "Visit LMS Portal": "Truy cập Cổng học tập",
    "Create a Course": "Tạo khóa học mới",
    "Setup a Home Page": "Thiết lập trang chủ",
    "Documentation": "Tài liệu hướng dẫn",
    "Statistics": "Thống kê",
    "Master": "Danh mục chính",
    
    # Roles
    "Moderator": "Quản trị viên LMS",
    "Course Creator": "Giảng viên tạo khóa học",
    "Batch Evaluator": "Người đánh giá lớp học",
    "LMS Student": "Học viên LMS",
    "Instructor": "Giảng viên",
    "Instructors": "Giảng viên",
    "Student": "Học viên",
    "Students": "Học viên",
    "Evaluator": "Người chấm bài",
    "Learner": "Người học",
    "Learners": "Người học",
    "Member": "Thành viên",
    "Members": "Thành viên",
    
    # UI actions & Common headers
    "Switch to Desk": "Chuyển sang Trang Quản trị",
    "Clear Demo Data": "Xóa dữ liệu mẫu",
    "Search or type a command (Ctrl + K)": "Tìm kiếm hoặc gõ lệnh (Ctrl + K)",
    "Workspace": "Không gian làm việc",
    "Workspaces": "Không gian làm việc",
    "Settings": "Cài đặt",
    "Integrations": "Tích hợp",
    "Users": "Người dùng",
    "User": "Người dùng",
    "Roles": "Vai trò",
    "Role": "Vai trò",
    "Build": "Xây dựng",
    "Customization": "Tùy biến",
    "Dashboard": "Bảng điều khiển",
    "Reports": "Báo cáo",
    "Tools": "Công cụ",
    "Help": "Trợ giúp",
    "My Settings": "Cài đặt của tôi",
    "Log out": "Đăng xuất",
    "Session": "Phiên làm việc",
    "Profile": "Hồ sơ cá nhân",
    "General": "Chung",
    "Save": "Lưu",
    "Cancel": "Hủy",
    "Submit": "Gửi đi",
    "Delete": "Xóa",
    "Edit": "Sửa",
    "New": "Thêm mới",
    "Filter": "Bộ lọc",
    "Sort By": "Sắp xếp theo",
    "Status": "Trạng thái",
    "Published": "Đã xuất bản",
    "Unpublished": "Chưa xuất bản",
    "Active": "Hoạt động",
    "Enabled": "Đã bật",
    "Disabled": "Đã tắt",
}

for src, tr in translations.items():
    doc = frappe.new_doc("Translation")
    doc.language = "vi"
    doc.source_text = src
    doc.translated_text = tr
    doc.insert()

frappe.db.commit()
frappe.clear_cache()
print(f"Successfully inserted {len(translations)} clean UTF-8 Vietnamese translations!")
