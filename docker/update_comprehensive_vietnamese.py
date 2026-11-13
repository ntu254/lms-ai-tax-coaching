import os
import frappe

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init("lms.localhost")
frappe.connect()

print("--- Nạp bộ bản dịch toàn diện cho các trang, thông báo, Empty State của LMS ---")

full_dict = {
    # 1. Việc làm (Jobs)
    "Post a job": "Đăng tin tuyển dụng",
    "Share openings with the people who learn on your site, from internships to full-time roles.": "Chia sẻ cơ hội việc làm tới học viên trên hệ thống của bạn, từ thực tập đến vị trí chính thức.",
    "No closed jobs": "Chưa có tin tuyển dụng nào đóng",
    "Jobs you close move here, so you keep a record of past openings.": "Các tin tuyển dụng bạn đã đóng sẽ chuyển về đây để lưu trữ lịch sử.",
    "Job Openings": "Vị trí tuyển dụng",
    "New Job": "Tin tuyển dụng mới",
    "Search jobs": "Tìm kiếm việc làm",
    "Work Mode": "Hình thức làm việc",
    "Type": "Loại hình công việc",
    "Open": "Đang tuyển",
    "Closed": "Đã đóng",
    "Jobs": "Việc làm",
    "{0} {1} Jobs": "{0} việc làm {1}",
    "No applications yet": "Chưa có hồ sơ ứng tuyển nào",
    "People who apply to this job show up here. Share the job link to reach more applicants.": "Học viên ứng tuyển vào vị trí này sẽ xuất hiện tại đây. Hãy chia sẻ liên kết để tiếp cận nhiều ứng viên hơn.",
    "Job Details": "Chi tiết việc làm",
    "Job Title": "Chức danh công việc",
    "Job Description": "Mô tả công việc",
    "Apply for Job": "Ứng tuyển công việc",

    # 2. Khóa học (Courses)
    "Publish your first course": "Xuất bản khóa học đầu tiên của bạn",
    "Turn what you know into lessons, quizzes and a certificate people can take at their own pace.": "Biến kiến thức của bạn thành các bài học, bài kiểm tra và chứng chỉ để học viên tự học theo lộ trình.",
    "No upcoming courses": "Chưa có khóa học sắp diễn ra",
    "Courses marked as upcoming show up here, so learners can see what is coming next.": "Các khóa học được đánh dấu sắp ra mắt sẽ hiển thị tại đây để học viên tiện theo dõi.",
    "No courses created by you": "Bạn chưa tạo khóa học nào",
    "Courses you create or teach show up here, for your team, students or customers.": "Các khóa học do bạn tạo hoặc giảng dạy sẽ hiển thị ở đây dành cho đội ngũ, học viên hoặc khách hàng của bạn.",
    "No unpublished courses": "Không có khóa học nào chưa xuất bản",
    "New courses wait here while you build them. Publish one when it is ready.": "Khóa học mới đang biên soạn sẽ nằm ở đây. Bạn có thể xuất bản khi nội dung đã sẵn sàng.",
    "Start building your course": "Bắt đầu xây dựng khóa học của bạn",
    "A course is chapters with lessons inside. Create the first chapter, then add lessons to it.": "Khóa học gồm các chương và bài học bên trong. Hãy tạo chương đầu tiên, sau đó thêm các bài học vào.",
    "Add your first lesson": "Thêm bài học đầu tiên của bạn",
    "Lessons hold your videos, text, quizzes and files. Add one to {0} to get going.": "Bài học có thể chứa video, bài viết, bài kiểm tra và tài liệu. Hãy thêm bài học vào {0} để bắt đầu.",
    "Pick a lesson to edit": "Chọn một bài học để chỉnh sửa",
    "Buy this course": "Mua khóa học này",
    "Continue your course": "Tiếp tục khóa học của bạn",
    "Checkout Courses": "Khám phá các khóa học",
    "Course content coming soon!": "Nội dung khóa học sẽ sớm ra mắt!",
    "Course creator": "Người tạo khóa học",
    "Course created successfully": "Tạo khóa học thành công",
    "Course updated successfully": "Cập nhật khóa học thành công",
    "Course deleted successfully": "Xóa khóa học thành công",
    "Course published": "Đã xuất bản khóa học",
    "Course unpublished": "Đã hủy xuất bản khóa học",
    "Course options": "Tùy chọn khóa học",
    "Course overview": "Tổng quan khóa học",
    "Course description": "Mô tả khóa học",
    "Course details": "Chi tiết khóa học",
    "Course editor": "Trình soạn thảo khóa học",
    "Course thumbnail": "Ảnh đại diện khóa học",
    "Course price": "Giá khóa học",
    "Course progress": "Tiến độ khóa học",
    "Course Completion": "Hoàn thành khóa học",
    "Course Completions": "Khóa học đã hoàn thành",
    "Course Enrollment": "Ghi danh khóa học",
    "Course Enrollments": "Danh sách ghi danh khóa học",
    "Course added to batch successfully": "Đã thêm khóa học vào đợt học thành công",
    "Course added to program successfully": "Đã thêm khóa học vào lộ trình thành công",
    "Charge learners to enroll in this course.": "Thu phí học viên khi ghi danh vào khóa học này.",
    "Complete the previous lessons to unlock this one": "Hoàn thành các bài học trước để mở khóa bài học này.",
    "Contact the Administrator to enroll for this course.": "Vui lòng liên hệ Quản trị viên để ghi danh khóa học này.",
    "Delete this lesson?": "Bạn có chắc muốn xóa bài học này?",
    "Delete this chapter?": "Bạn có chắc muốn xóa chương học này?",
    "Delete Course": "Xóa khóa học",

    # 3. Đợt học (Batches)
    "Teach people together in a batch": "Giảng dạy học viên theo đợt học",
    "Take a group through your courses on a schedule, with live classes and a certificate at the end.": "Dẫn dắt một nhóm học viên theo lịch trình cụ thể, kết hợp lớp học trực tuyến và cấp chứng chỉ khi hoàn thành.",
    "No upcoming batches": "Chưa có đợt học sắp diễn ra",
    "Published batches that start later show up here, so you can open sign-ups early.": "Các đợt học đã xuất bản và khai giảng trong tương lai sẽ xuất hiện ở đây để bạn mở đăng ký sớm.",
    "No archived batches": "Chưa có đợt học nào lưu trữ",
    "Batches move here once they start, so you can look back at each group.": "Các đợt học đã bắt đầu hoặc hoàn thành sẽ chuyển về đây để bạn xem lại lịch sử.",
    "No unpublished batches": "Không có đợt học nào chưa xuất bản",
    "New batches wait here until you publish them, so learners never see a half-ready batch.": "Các đợt học mới đang soạn thảo sẽ lưu tạm ở đây cho đến khi bạn sẵn sàng xuất bản.",
    "Charge a fee for batch enrollment.": "Thu phí ghi danh tham gia đợt học này.",
    "Bring your learners into a batch.": "Tập hợp học viên của bạn vào một đợt học.",
    "Contact the Administrator to enroll for this batch": "Vui lòng liên hệ Quản trị viên để ghi danh đợt học này.",
    "Batch overview": "Tổng quan đợt học",
    "Batch options": "Tùy chọn đợt học",
    "Batch published": "Đã xuất bản đợt học",
    "Batch unpublished": "Đã hủy xuất bản đợt học",
    "Confirm your action to delete": "Xác nhận hành động xóa",

    # 4. Lớp học trực tuyến (Live Classes)
    "Set up live classes": "Thiết lập lớp học trực tuyến",
    "Pick Zoom or Google Meet for this batch in Settings, then schedule classes your students join from here.": "Chọn Zoom hoặc Google Meet trong phần Cài đặt, sau đó lên lịch lớp để học viên tham gia trực tiếp từ đây.",
    "No live classes yet": "Chưa có lớp học trực tuyến nào",
    "Schedule a class on Zoom or Google Meet. Students get a reminder and join from here.": "Lên lịch lớp học trên Zoom hoặc Google Meet. Học viên sẽ nhận được thông báo nhắc nhở và vào học từ đây.",
    "Classes your instructors schedule show up here, with a link to join.": "Các buổi học trực tuyến do giảng viên lên lịch sẽ hiển thị tại đây kèm đường dẫn tham gia.",

    # 5. Bài kiểm tra (Quizzes) & Ngân hàng câu hỏi
    "Create your first quiz": "Tạo bài kiểm tra đầu tiên",
    "Check what learners understood with multiple choice, short answer or open ended questions.": "Kiểm tra mức độ tiếp thu của học viên bằng câu hỏi trắc nghiệm, điền từ hoặc câu hỏi mở.",
    "Build your question bank": "Xây dựng ngân hàng câu hỏi",
    "Write a question once and reuse it in any quiz you build.": "Soạn câu hỏi một lần và tái sử dụng cho bất kỳ bài kiểm tra nào bạn tạo.",
    "No quiz attempts yet": "Chưa có lượt làm bài thi nào",
    "Each time a learner takes a quiz, their answers and score show up here.": "Mỗi khi học viên hoàn thành bài kiểm tra, đáp án và điểm số của họ sẽ hiển thị tại đây.",
    "Delete this quiz?": "Bạn có chắc muốn xóa bài kiểm tra này?",
    "Leave without saving?": "Bạn có muốn rời đi mà không lưu thay đổi?",
    "Face must be visible": "Khuôn mặt phải luôn hiển thị trước camera",
    "One person only": "Chỉ được phép có một người trước camera",
    "Stay on this tab": "Vui lòng ở lại tab làm bài thi",
    "Keep camera connected": "Vui lòng duy trì kết nối camera",

    # 6. Bài tập (Assignments) & Lập trình (Programming Exercises)
    "Create your first assignment": "Tạo bài tập đầu tiên",
    "Ask learners to upload a file, write an answer or share a link, then grade their work.": "Yêu cầu học viên nộp file tài liệu, viết câu trả lời hoặc gửi liên kết, sau đó bạn có thể chấm điểm và nhận xét.",
    "Create your first programming exercise": "Tạo bài tập lập trình đầu tiên",
    "Learners write and run code in the browser, and test cases check their answers.": "Học viên viết và thực thi mã nguồn trực tiếp trên trình duyệt, hệ thống sẽ tự động chấm điểm qua các test case.",
    "Start again?": "Bạn có muốn làm lại từ đầu?",

    # 7. Lộ trình học (Programs) & Chứng chỉ
    "Group courses into a program": "Gom nhóm các khóa học thành lộ trình",
    "A program puts courses in order, like a path for new hires or a full certification track.": "Lộ trình giúp sắp xếp các khóa học theo thứ tự, phù hợp cho đào tạo nội bộ hoặc cấp chứng chỉ chuyên môn.",
    "No unpublished programs": "Không có lộ trình nào chưa xuất bản",
    "New programs wait here until you publish them, so learners only see finished paths.": "Các lộ trình mới sẽ lưu tạm ở đây cho đến khi bạn xuất bản để học viên theo học.",
    "Delete Program": "Xóa lộ trình",
    "No one is certified yet": "Chưa có học viên nào được cấp chứng chỉ",
    "Learners who finish a course with a certificate show up here. Add one to a course to begin.": "Học viên hoàn thành khóa học có cấp chứng chỉ sẽ xuất hiện tại đây.",
    "No imports yet": "Chưa có dữ liệu nào được nhập",
    "Bring in courses, batches or categories from a spreadsheet instead of adding them one by one.": "Nhập nhanh danh sách khóa học, đợt học hoặc danh mục từ file Excel/CSV thay vì thêm thủ công từng mục.",

    # 8. Onboarding & Sidebar
    "Create your first course": "Tạo khóa học đầu tiên",
    "Add your first chapter": "Thêm chương học đầu tiên",
    "Create your first quiz": "Tạo bài kiểm tra đầu tiên",
    "Invite your team and students": "Mời đội ngũ và học viên",
    "Create your first batch": "Tạo đợt học đầu tiên",
    "Add students to your batch": "Thêm học viên vào đợt học",
    "Add courses to your batch": "Thêm khóa học vào đợt học",
    "Create a course": "Tạo khóa học",
    "Add a chapter": "Thêm chương học",
    "Add a lesson": "Thêm bài học",
    "Creating a batch": "Tạo đợt học",
    "Create a batch": "Tạo đợt học",
    "Create a live class": "Tạo lớp học trực tuyến",
    "Learning Paths": "Lộ trình học tập",
    "Add a program": "Thêm lộ trình",
    "Issue a Certificate": "Cấp chứng chỉ",
    "Custom Certificate Templates": "Tùy biến mẫu chứng chỉ",
    "Setting up payment gateway": "Cài đặt cổng thanh toán",
    "Setting up": "Thiết lập",
    "Introduction": "Giới thiệu",
    "Confirm clearing demo data?": "Bạn có chắc muốn xóa dữ liệu mẫu không?",
    "Delete this category?": "Bạn có chắc muốn xóa danh mục này?",
    "Page not found": "Không tìm thấy trang",
    "Not Permitted": "Không có quyền truy cập",
}

added = 0
updated = 0
for src, tr in full_dict.items():
    existing = frappe.db.get_value("Translation", {"source_text": src, "language": "vi"}, "name")
    if existing:
        doc = frappe.get_doc("Translation", existing)
        if doc.translated_text != tr:
            doc.translated_text = tr
            doc.save(ignore_permissions=True)
            updated += 1
    else:
        doc = frappe.new_doc("Translation")
        doc.language = "vi"
        doc.source_text = src
        doc.translated_text = tr
        doc.insert(ignore_permissions=True)
        added += 1

frappe.db.commit()
frappe.clear_cache()
print(f"Đã bổ sung thành công {added} bản dịch mới và cập nhật {updated} bản dịch!")
