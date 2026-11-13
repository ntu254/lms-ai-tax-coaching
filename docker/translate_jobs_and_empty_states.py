import os
import frappe

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init("lms.localhost")
frappe.connect()

print("--- Nạp bản dịch cho Việc làm (Jobs), Trạng thái rỗng (Empty States) & Danh sách ---")

translations = {
    # 1. Trạng thái rỗng mặc định (EmptyStateLayout)
    "There are no {0} currently. Keep an eye out, fresh learning experiences are on the way!": "Hiện tại chưa có {0} nào. Hãy quay lại sau, các cơ hội học tập mới sắp ra mắt!",
    "There are no job openings currently. Keep an eye out, fresh learning experiences are on the way!": "Hiện tại chưa có vị trí tuyển dụng nào. Hãy quay lại sau, các cơ hội học tập mới sắp ra mắt!",
    "No {0} Found": "Không tìm thấy {0}",
    "No Job Openings Found": "Không tìm thấy vị trí tuyển dụng",
    "No job openings Found": "Không tìm thấy vị trí tuyển dụng",
    "No job openings found": "Không tìm thấy vị trí tuyển dụng",
    "No Courses Found": "Không tìm thấy khóa học",
    "No Batches Found": "Không tìm thấy đợt học",
    "No Programs Found": "Không tìm thấy chương trình đào tạo",
    "No Quizzes Found": "Không tìm thấy bài kiểm tra",
    "No Questions Found": "Không tìm thấy câu hỏi",
    "No Assignments Found": "Không tìm thấy bài tập",
    "No Job Applications Found": "Không tìm thấy đơn ứng tuyển",
    "No Certified Members Found": "Không tìm thấy học viên có chứng chỉ",
    "No Categories Found": "Không tìm thấy danh mục",
    "No Coupons Found": "Không tìm thấy mã giảm giá",
    "No Users Found": "Không tìm thấy người dùng",
    "No Transactions Found": "Không tìm thấy giao dịch",

    # 2. Bộ lọc & tìm kiếm trong ListPage / Settings
    "No {0} match {1}": "Không có {0} nào khớp với {1}",
    "No {0} match this filter": "Không có {0} nào khớp với bộ lọc này",
    'Nothing matches "{0}". Try another search or clear the filters.': 'Không có kết quả nào khớp với "{0}". Hãy thử tìm kiếm khác hoặc xóa bộ lọc.',
    "Nothing matches the filters applied. Try changing or clearing them.": "Không có kết quả nào khớp với bộ lọc đã chọn. Hãy thử thay đổi hoặc xóa bộ lọc.",
    "Clear filters": "Xóa bộ lọc",
    "Add one to get started": "Thêm mới để bắt đầu",
    "No results": "Không có kết quả",
    "1 result loaded": "Đã tải 1 kết quả",
    "{0} results loaded": "Đã tải {0} kết quả",

    # 3. Tên đối tượng (Hoa và Thường)
    "Job Openings": "Vị trí tuyển dụng",
    "job openings": "vị trí tuyển dụng",
    "Job Opening": "Vị trí tuyển dụng",
    "job opening": "vị trí tuyển dụng",
    "Job Applications": "Đơn ứng tuyển",
    "job applications": "đơn ứng tuyển",
    "Job Application": "Đơn ứng tuyển",
    "job application": "đơn ứng tuyển",
    "Certified Members": "Học viên có chứng chỉ",
    "certified members": "học viên có chứng chỉ",
    "Assignment Submissions": "Bài nộp bài tập",
    "assignment submissions": "bài nộp bài tập",
    "Quiz Submissions": "Bài nộp trắc nghiệm",
    "quiz submissions": "bài nộp trắc nghiệm",
    "Programming Exercises": "Bài tập lập trình",
    "programming exercises": "bài tập lập trình",
    "Programming Exercise Submissions": "Bài nộp bài tập lập trình",
    "programming exercise submissions": "bài nộp bài tập lập trình",
    "Imports": "Dữ liệu nhập",
    "imports": "dữ liệu nhập",
    "Coupons": "Mã giảm giá",
    "coupons": "mã giảm giá",
    "Categories": "Danh mục",
    "categories": "danh mục",
    "Users": "Người dùng",
    "users": "người dùng",
    "Transactions": "Giao dịch",
    "transactions": "giao dịch",
    "Workspaces": "Không gian làm việc",
    "workspaces": "không gian làm việc",
    "Courses": "Khóa học",
    "courses": "khóa học",
    "Batches": "Đợt học",
    "batches": "đợt học",
    "Programs": "Chương trình đào tạo",
    "programs": "chương trình đào tạo",
    "Quizzes": "Bài kiểm tra",
    "quizzes": "bài kiểm tra",
    "Questions": "Câu hỏi",
    "questions": "câu hỏi",
    "Assignments": "Bài tập",
    "assignments": "bài tập",

    # 4. Loại công việc, hình thức làm việc, trạng thái
    "Full Time": "Toàn thời gian",
    "Part Time": "Bán thời gian",
    "Contract": "Hợp đồng",
    "Freelance": "Tự do",
    "On-site": "Tại văn phòng",
    "On site": "Tại văn phòng",
    "Hybrid": "Linh hoạt (Hybrid)",
    "Remote": "Từ xa",
    "Open": "Đang mở",
    "Closed": "Đã đóng",

    # 5. Chi tiết, Đơn ứng tuyển & Form tuyển dụng
    "Job Details": "Chi tiết việc làm",
    "View Applications": "Xem đơn ứng tuyển",
    "Visit Website": "Truy cập trang web",
    "Apply": "Ứng tuyển",
    "Apply for this job": "Ứng tuyển vị trí này",
    "You have applied": "Bạn đã ứng tuyển",
    "Login to apply": "Đăng nhập để ứng tuyển",
    "applicant": "ứng viên",
    "applicants": "ứng viên",
    "Upload your resume": "Tải lên CV của bạn",
    "Uploading {0}%": "Đang tải lên {0}%",
    "Submit your resume to proceed with your application for this position. Upon submission, it will be shared with the job poster.": "Nộp CV của bạn để hoàn tất hồ sơ ứng tuyển vị trí này. Sau khi nộp, hồ sơ sẽ được gửi đến nhà tuyển dụng.",
    "Please upload your resume": "Vui lòng tải lên CV của bạn",
    "Your application has been submitted successfully": "Đơn ứng tuyển của bạn đã được gửi thành công",
    "Only PDF file is allowed": "Chỉ chấp nhận tệp định dạng PDF",
    "Send Email": "Gửi email",
    "No applications yet": "Chưa có đơn ứng tuyển nào",
    "Application": "Đơn ứng tuyển",
    "Applications": "Đơn ứng tuyển",
    "Applied On": "Ngày ứng tuyển",
    "Search applications": "Tìm kiếm đơn ứng tuyển",
    "Not Saved": "Chưa lưu",
    "Work Mode": "Chế độ làm việc",
    "Company Details": "Thông tin công ty",
    "Company Name": "Tên công ty",
    "Company Website": "Trang web công ty",
    "Company Email Address": "Email công ty",
    "Company Logo": "Logo công ty",
    "City": "Thành phố",
    "Country": "Quốc gia",
    "More actions": "Thao tác khác",
}

added_count = 0
updated_count = 0

for src, tr in translations.items():
    existing = frappe.db.sql(
        "SELECT name, translated_text FROM `tabTranslation` WHERE BINARY source_text = %s AND language = 'vi'",
        (src,),
    )
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
print(f"Đã thêm {added_count} và cập nhật {updated_count} bản dịch cho Jobs & Empty States!")
