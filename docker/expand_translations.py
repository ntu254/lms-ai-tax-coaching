import os
import json
import frappe

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init("lms.localhost")
frappe.connect()

print("--- 1. Cập nhật trực tiếp nội dung Workspace 'Learning' sang Tiếng Việt ---")
if frappe.db.exists("Workspace", "Learning"):
    ws = frappe.get_doc("Workspace", "Learning")
    ws.label = "Học tập"
    ws.title = "Học tập"
    
    # Cập nhật các blocks nội dung HTML trong Workspace
    content = json.loads(ws.content or "[]")
    for block in content:
        btype = block.get("type")
        data = block.get("data", {})
        
        if btype == "header":
            text = data.get("text", "")
            if "Get Started" in text:
                data["text"] = '<span class="h4"><b>Bắt đầu</b></span>'
            elif "Statistics" in text:
                data["text"] = '<span style="font-size:18px"><b>Thống kê</b></span>'
            elif "Master" in text:
                data["text"] = '<span class="h4"><b>Danh mục chính</b></span>'
                
        elif btype == "paragraph":
            text = data.get("text", "")
            if "Visit LMS Portal" in text:
                data["text"] = '<a href="/lms/courses" rel="noopener noreferrer">Truy cập Cổng học tập</a>'
            elif "Create a Course" in text:
                data["text"] = '<a href="/lms/courses/new/edit" rel="noopener noreferrer">Tạo khóa học mới</a>'
            elif "Setup a Home Page" in text:
                data["text"] = '<a href="/app/web-page/new-web-page-1" rel="noopener noreferrer">Thiết lập Trang chủ</a>'
            elif "LMS Settings" in text:
                data["text"] = '<a href="/app/lms-settings/LMS%20Settings" rel="noopener noreferrer">Cài đặt LMS</a>'
            elif "Documentation" in text:
                data["text"] = '<a href="https://docs.frappe.io/learning" rel="noopener noreferrer">Tài liệu hướng dẫn</a>'

        elif btype == "card":
            cname = data.get("card_name", "")
            if cname == "Course Data":
                data["card_name"] = "Dữ liệu khóa học"
            elif cname == "Course Stats":
                data["card_name"] = "Thống kê khóa học"
            elif cname == "Certification":
                data["card_name"] = "Chứng chỉ & Đánh giá"

        elif btype == "shortcut":
            sname = data.get("shortcut_name", "")
            if sname == "Course":
                data["shortcut_name"] = "Khóa học"
            elif sname == "Enrollments":
                data["shortcut_name"] = "Ghi danh"
            elif sname == "Course Completed":
                data["shortcut_name"] = "Khóa học hoàn thành"
            elif sname == "Certificate":
                data["shortcut_name"] = "Chứng chỉ"
            elif sname == "Evaluation":
                data["shortcut_name"] = "Đánh giá"
            elif sname == "Users":
                data["shortcut_name"] = "Người dùng"

    ws.content = json.dumps(content)
    
    # Cập nhật danh sách shortcuts
    for s in ws.shortcuts:
        if s.label == "Course":
            s.label = "Khóa học"
        elif s.label == "Enrollments":
            s.label = "Ghi danh"
        elif s.label == "Course Completed":
            s.label = "Khóa học hoàn thành"
        elif s.label == "Certificate":
            s.label = "Chứng chỉ"
        elif s.label == "Evaluation":
            s.label = "Đánh giá"
        elif s.label == "Users":
            s.label = "Người dùng"

    # Cập nhật danh sách links & card breaks
    for l in ws.links:
        if l.label == "Course Data":
            l.label = "Dữ liệu khóa học"
        elif l.label == "Course Stats":
            l.label = "Thống kê khóa học"
        elif l.label == "Certification":
            l.label = "Chứng chỉ & Đánh giá"
        elif l.label == "Course":
            l.label = "Khóa học"
        elif l.label == "Chapter":
            l.label = "Chương học"
        elif l.label == "Lesson":
            l.label = "Bài học"
        elif l.label == "Quiz":
            l.label = "Bài kiểm tra"
        elif l.label == "Quiz Submission":
            l.label = "Bài nộp kiểm tra"
        elif l.label == "Quiz Violation Log":
            l.label = "Nhật ký vi phạm bài thi"
        elif l.label == "Interest":
            l.label = "Quan tâm khóa học"
        elif l.label == "Review":
            l.label = "Đánh giá khóa học"
        elif l.label == "Evaluation Request":
            l.label = "Yêu cầu đánh giá"
        elif l.label == "Evaluation":
            l.label = "Đánh giá cấp chứng chỉ"

    ws.save(ignore_permissions=True)
    print("-> Đã cập nhật Workspace 'Học tập' hoàn toàn sang tiếng Việt!")

print("\n--- 2. Nạp thêm danh mục dịch thuật chi tiết cho Frontend & Backend ---")

translations = {
    # Khóa học & Bài học
    "All Courses": "Tất cả khóa học",
    "All Payments": "Tất cả giao dịch",
    "All Programs": "Tất cả lộ trình",
    "All members": "Tất cả thành viên",
    "About this course": "Giới thiệu khóa học",
    "Course Outline": "Đề cương khóa học",
    "Course Details": "Thông tin khóa học",
    "Course Description": "Mô tả khóa học",
    "Course Category": "Danh mục khóa học",
    "Course Instructor": "Giảng viên khóa học",
    "Course Progress": "Tiến độ khóa học",
    "Course Name": "Tên khóa học",
    "Course Title": "Tiêu đề khóa học",
    "Created Courses": "Khóa học đã tạo",
    "My Courses": "Khóa học của tôi",
    "Add Course": "Thêm khóa học",
    "New Course": "Khóa học mới",
    "Edit Course": "Chỉnh sửa khóa học",
    "Delete Course": "Xóa khóa học",
    "Publish Course": "Xuất bản khóa học",
    "Unpublish Course": "Hủy xuất bản khóa học",
    "Enroll in Course": "Ghi danh khóa học",
    "Enroll Now": "Ghi danh ngay",
    "Enrolled": "Đã ghi danh",
    "Start Learning": "Bắt đầu học",
    "Continue Learning": "Tiếp tục học",
    "Mark as Complete": "Đánh dấu đã hoàn thành",
    "Completed": "Đã hoàn thành",
    "In Progress": "Đang học",
    "Not Started": "Chưa bắt đầu",
    "Previous Lesson": "Bài trước",
    "Next Lesson": "Bài tiếp theo",
    "Complete & Next": "Hoàn thành & Tiếp tục",
    "Watch Video": "Xem video",
    "Video Link": "Đường dẫn video",
    "Lesson Content": "Nội dung bài học",
    "Add Lesson": "Thêm bài học",
    "Add a lesson": "Thêm bài học",
    "Add a Chapter": "Thêm chương học",
    "Add a chapter": "Thêm chương học",
    "Add Chapter": "Thêm chương học",
    "Add your first chapter": "Thêm chương học đầu tiên",
    "Add your first lesson": "Thêm bài học đầu tiên",
    "Short Introduction": "Mô tả ngắn",
    "Free": "Miễn phí",
    "Paid": "Có phí",

    # Đợt học (Batches)
    "Upcoming Batches": "Đợt học sắp diễn ra",
    "Ongoing Batches": "Đợt học đang diễn ra",
    "Completed Batches": "Đợt học đã kết thúc",
    "Batch Details": "Thông tin đợt học",
    "Batch Name": "Tên đợt học",
    "Batch Start Date": "Ngày bắt đầu",
    "Batch End Date": "Ngày kết thúc",
    "Start Date": "Ngày bắt đầu",
    "End Date": "Ngày kết thúc",
    "Start Time": "Giờ bắt đầu",
    "End Time": "Giờ kết thúc",
    "Seat Count": "Số lượng chỗ",
    "Seats Left": "Số chỗ còn lại",
    "Timetable": "Thời khóa biểu",
    "Enroll in Batch": "Tham gia đợt học",
    "Allow Self Enrollment": "Cho phép tự ghi danh",
    "Add students to your batch": "Thêm học viên vào đợt học",
    "Add courses to your batch": "Thêm khóa học vào đợt học",
    "Batch created successfully": "Tạo đợt học thành công",
    "Batch updated successfully": "Cập nhật đợt học thành công",
    "Batch deleted successfully": "Xóa đợt học thành công",

    # Lớp học trực tuyến (Live Class)
    "Join Class": "Vào lớp học",
    "Live Class Details": "Thông tin lớp trực tuyến",
    "Schedule Live Class": "Lên lịch lớp học",
    "Meeting Link": "Đường dẫn phòng học",
    "Zoom Meeting": "Phòng học Zoom",
    "Google Meet": "Phòng học Google Meet",
    "Upcoming Classes": "Lớp học sắp tới",
    "Past Classes": "Lớp học đã qua",

    # Bài kiểm tra (Quiz) & Câu hỏi
    "Start Quiz": "Bắt đầu làm bài",
    "Submit Quiz": "Nộp bài kiểm tra",
    "Your Score": "Điểm số của bạn",
    "Passing Score": "Điểm đạt yêu cầu",
    "Passing Percentage": "Tỷ lệ điểm đạt",
    "Total Marks": "Tổng điểm",
    "Marks": "Điểm",
    "Questions": "Câu hỏi",
    "Question": "Câu hỏi",
    "Choices": "Lựa chọn trắc nghiệm",
    "Single Choice": "Chọn 1 đáp án",
    "Multiple Choice": "Chọn nhiều đáp án",
    "Correct Answer": "Đáp án đúng",
    "Incorrect Answer": "Đáp án sai",
    "Explanation": "Giải thích đáp án",
    "Attempts Left": "Số lần làm lại còn lại",
    "Max Attempts": "Số lần thử tối đa",
    "Retake Quiz": "Làm lại bài kiểm tra",
    "Passed": "Đạt",
    "Failed": "Không đạt",
    "Time Remaining": "Thời gian còn lại",
    "Are you sure you want to submit the quiz?": "Bạn có chắc chắn muốn nộp bài?",
    "Add questions": "Thêm câu hỏi",
    "Add option": "Thêm đáp án",

    # Bài tập (Assignment) & Bài tập lập trình
    "Add Assessment": "Thêm bài đánh giá",
    "Submit Assignment": "Nộp bài tập",
    "Assignment Instructions": "Hướng dẫn làm bài",
    "Submission": "Bài nộp",
    "Submissions": "Danh sách bài nộp",
    "Your Submission": "Bài nộp của bạn",
    "Upload File": "Tải file lên",
    "Grade": "Chấm điểm",
    "Graded": "Đã chấm điểm",
    "Not Graded": "Chưa chấm điểm",
    "Evaluator Comments": "Nhận xét của người chấm",
    "Test Cases": "Bộ kiểm thử (Test Cases)",
    "Run Code": "Chạy thử code",
    "Submit Code": "Nộp code",
    "Expected Output": "Kết quả kỳ vọng",
    "Your Output": "Kết quả của bạn",

    # Chứng chỉ & Đánh giá
    "Claim Certificate": "Nhận chứng chỉ",
    "Download Certificate": "Tải chứng chỉ",
    "Verify Certificate": "Xác minh chứng chỉ",
    "Certificate ID": "Mã chứng chỉ",
    "Issued On": "Ngày cấp",
    "Valid Till": "Có hiệu lực đến",
    "Request Evaluation": "Yêu cầu đánh giá",
    "Evaluation Status": "Trạng thái đánh giá",
    "Certified Members": "Học viên có chứng chỉ",

    # Tương tác, Ghi chú, Thảo luận
    "Discussions": "Thảo luận",
    "Comments": "Bình luận",
    "Leave a comment": "Viết bình luận...",
    "Post Comment": "Gửi bình luận",
    "Notes": "Ghi chú",
    "Add a note": "Thêm ghi chú...",
    "Add to Notes": "Lưu vào ghi chú",
    "My Notes": "Ghi chú của tôi",
    "Reviews": "Đánh giá nhận xét",
    "Leave a Review": "Viết đánh giá",
    "Your rating": "Đánh giá của bạn",
    "Submit Review": "Gửi đánh giá",

    # Các thông báo & Hành động chung
    "Confirm": "Xác nhận",
    "Close": "Đóng",
    "Back": "Quay lại",
    "Back to courses": "Quay lại danh sách khóa học",
    "Back to topics": "Quay lại chủ đề",
    "Back to editing": "Quay lại chỉnh sửa",
    "Actions": "Hành động",
    "Options": "Tùy chọn",
    "Details": "Chi tiết",
    "Overview": "Tổng quan",
    "Description": "Mô tả",
    "Summary": "Tóm tắt",
    "Statistics": "Thống kê",
    "Analytics": "Phân tích số liệu",
    "Total Students": "Tổng số học viên",
    "Total Courses": "Tổng số khóa học",
    "Total Batches": "Tổng số đợt học",
    "Share": "Chia sẻ",
    "Copy Link": "Sao chép liên kết",
    "Link copied": "Đã sao chép liên kết",
    "Loading...": "Đang tải...",
    "Please wait...": "Vui lòng chờ...",
    "Success": "Thành công",
    "Error": "Lỗi",
    "Warning": "Cảnh báo",
    "Are you sure?": "Bạn có chắc chắn không?",
    "This action cannot be undone.": "Hành động này không thể hoàn tác.",
}

added_count = 0
updated_count = 0

for src, tr in translations.items():
    existing = frappe.db.get_value("Translation", {"source_text": src, "language": "vi"}, "name")
    if existing:
        doc = frappe.get_doc("Translation", existing)
        if doc.translated_text != tr:
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
print(f"-> Đã bổ sung {added_count} bản dịch mới và cập nhật {updated_count} bản dịch chuẩn tiếng Việt!")
