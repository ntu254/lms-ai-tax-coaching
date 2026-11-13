import os
import frappe

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init("lms.localhost")
frappe.connect()

print("--- Nạp bản dịch cho tất cả các Form, Section Empty State và thông báo lỗi ---")

form_translations = {
    # ProgramForm & BatchForm SectionEmptyStates
    "Add the courses learners take in this program, in the order they should take them.": "Thêm các khóa học trong lộ trình này theo đúng thứ tự học viên cần hoàn thành.",
    "Add the people who should take this program. They get every course in it.": "Thêm học viên cần tham gia lộ trình này. Họ sẽ được ghi danh vào tất cả khóa học trong lộ trình.",
    "Add the courses this batch works through. Students get access to each one when they enroll.": "Thêm các khóa học cho đợt học này. Học viên sẽ được truy cập vào tất cả các khóa học khi ghi danh.",
    "Courses for this batch show up here once your instructors add them.": "Các khóa học của đợt học này sẽ hiển thị ở đây khi giảng viên thêm vào.",
    "Add quizzes, assignments or programming exercises for students to complete during this batch.": "Thêm các bài kiểm tra, bài tập hoặc bài tập lập trình để học viên hoàn thành trong đợt học này.",
    "Add Course to Program": "Thêm khóa học vào lộ trình",
    "Enroll Member to Program": "Ghi danh học viên vào lộ trình",
    "Program Member": "Thành viên lộ trình",
    "Progress Summary": "Tổng quan tiến độ",
    "Enforce Course Order": "Bắt buộc học các khóa theo đúng thứ tự",
    "Members": "Thành viên",
    "Delete program": "Xóa lộ trình",
    "Delete Program": "Xóa lộ trình",
    "Program created successfully": "Đã tạo lộ trình thành công",
    "Program updated successfully": "Đã cập nhật lộ trình thành công",
    "Program deleted successfully": "Đã xóa lộ trình thành công",
    "Are you sure you want to delete this program? This action cannot be undone.": "Bạn có chắc muốn xóa lộ trình này? Hành động này không thể hoàn tác.",
    "Course already added to program": "Khóa học này đã có trong lộ trình",
    "Member added to program successfully": "Đã thêm thành viên vào lộ trình thành công",
    "Member already added to program": "Thành viên này đã có trong lộ trình",

    # QuizForm & Question Editor
    "Add your first question and edit it right here. Choices, correct answers and explanations all in one card.": "Thêm câu hỏi đầu tiên và chỉnh sửa trực tiếp tại đây. Các lựa chọn, đáp án đúng và giải thích đều nằm trong một thẻ.",
    "Name the quiz first": "Hãy đặt tên cho bài kiểm tra trước",
    "Fill in the title on the right. The quiz is created then, and questions can go in.": "Điền tiêu đề ở cột bên phải để tạo bài kiểm tra, sau đó bạn có thể thêm câu hỏi vào.",
    "New question": "Câu hỏi mới",
    "No questions yet": "Chưa có câu hỏi nào",
    "Allow users to view their past quiz attempts.": "Cho phép học viên xem lại lịch sử các lần làm bài kiểm tra trước đó.",
    "Enable Proctoring": "Bật tính năng giám sát thi (Proctoring)",
    "Require camera access and monitor for violations during the quiz.": "Yêu cầu quyền truy cập camera và giám sát các vi phạm trong suốt bài thi.",
    "Max Violations": "Số lần vi phạm tối đa",
    "Quiz auto-submits when this many violations are recorded.": "Bài thi sẽ tự động nộp khi số lần vi phạm đạt mức này.",
    "Enable Negative Marking": "Bật tính năng trừ điểm khi trả lời sai",
    "Deduct marks for incorrect answers.": "Trừ điểm khi trả lời sai.",
    "Marks to Deduct": "Số điểm bị trừ",
    "Maximum Attempts": "Số lần làm bài tối đa",
    "Limit Questions To": "Giới hạn số câu hỏi",
    "Randomize the order of questions for each attempt.": "Đảo thứ tự câu hỏi ngẫu nhiên trong mỗi lần làm bài.",
    "Shuffle Questions": "Trộn ngẫu nhiên câu hỏi",
    "Display correct answers after each question is attempted.": "Hiển thị đáp án đúng sau khi học viên trả lời mỗi câu hỏi.",
    "Show Answers": "Hiển thị đáp án",
    "Show Submission History": "Hiển thị lịch sử nộp bài",
    "Restrict when learners can start and submit this quiz.": "Giới hạn khoảng thời gian học viên được phép bắt đầu và nộp bài thi.",
    "Optional. Leave empty to keep the quiz open after it starts.": "Tùy chọn. Để trống nếu muốn mở bài kiểm tra không giới hạn hạn chót.",
    "The questions you have added, removed or reordered are not saved yet. Leaving this page discards them.": "Các câu hỏi bạn đã thêm, xóa hoặc sắp xếp lại chưa được lưu. Nếu rời khỏi trang này, các thay đổi sẽ bị mất.",
    "Deleting this quiz permanently removes it and its submissions. This action cannot be undone. Are you sure you want to continue?": "Xóa bài kiểm tra này sẽ xóa vĩnh viễn cả các bài nộp của học viên. Hành động này không thể hoàn tác. Bạn có chắc muốn tiếp tục?",
    "Could not delete the quiz": "Không thể xóa bài kiểm tra",
    "Quiz updated successfully": "Đã cập nhật bài kiểm tra thành công",
    "Quiz deleted successfully": "Đã xóa bài kiểm tra thành công",
    "Search questions": "Tìm kiếm câu hỏi",
    "Total Questions": "Tổng số câu hỏi",
    "Question bank": "Ngân hàng câu hỏi",

    # AssignmentForm
    "Edit Assignment": "Chỉnh sửa bài tập",
    "New Assignment": "Bài tập mới",
    "Submission Type": "Hình thức nộp bài",
    "Grade submissions": "Chấm điểm bài nộp",
    "Manual grading": "Chấm điểm thủ công",
    "Students answer in a rich-text editor (image embeds allowed).": "Học viên trả lời trực tiếp trong trình soạn thảo (hỗ trợ chèn ảnh).",
    "Restrict when learners can submit this assignment.": "Giới hạn khoảng thời gian học viên được phép nộp bài tập.",
    "Optional. Leave empty to keep the assignment open after it starts.": "Tùy chọn. Để trống nếu muốn mở bài tập không giới hạn hạn chót.",
    "Only the authors of this assignment can edit it.": "Chỉ tác giả của bài tập này mới có quyền chỉnh sửa.",
    "Assignment created successfully": "Đã tạo bài tập thành công",
    "Assignment updated successfully": "Đã cập nhật bài tập thành công",

    # ProgrammingExerciseForm
    "New Programming Exercise": "Bài tập lập trình mới",
    "Problem Statement": "Đề bài",
    "Starter Code": "Đoạn mã khởi đầu (Starter Code)",
    "Prefills the learner’s editor. Leave empty for the language default.": "Đoạn code gợi ý sẵn cho học viên. Để trống để dùng mặc định.",
    "Only the authors of this programming exercise can edit it.": "Chỉ tác giả của bài tập lập trình này mới có quyền chỉnh sửa.",
    "Programming Exercise deleted successfully": "Đã xóa bài tập lập trình thành công",

    # CourseForm & SCORM & Import
    "Course description": "Mô tả khóa học",
    "A 750×422 .jpg, .gif or .png, shown on the course card.": "Ảnh kích thước 750×422 dạng .jpg, .gif hoặc .png hiển thị trên thẻ khóa học.",
    "Select instructors": "Chọn giảng viên",
    "Enable this only if you want to upload a SCORM package as a chapter.": "Chỉ bật mục này nếu bạn muốn tải lên gói bài giảng chuẩn SCORM.",
    "SCORM Package": "Gói bài giảng SCORM",
    "Please upload a SCORM package": "Vui lòng tải lên gói SCORM",
    "Import Course from ZIP": "Nhập khóa học từ file ZIP",
    "Drag and drop a ZIP file, or upload from your": "Kéo thả file ZIP vào đây, hoặc tải lên từ",
    "Upload a ZIP file": "Tải lên file ZIP",
    "Uploading {0}%": "Đang tải lên {0}%",
    "Only zip files are allowed": "Chỉ chấp nhận file định dạng .zip",
    "Error importing course": "Lỗi khi nhập dữ liệu khóa học",
    "Chapter added successfully": "Đã thêm chương học thành công",
    "Chapter updated successfully": "Đã cập nhật chương học thành công",
    "Edit Chapter": "Chỉnh sửa chương học",

    # BatchForm & LiveClassForm
    "New Batch": "Đợt học mới",
    "Error creating batch": "Lỗi khi tạo đợt học",
    "No students in this batch": "Chưa có học viên nào trong đợt học này",
    "New Live Class": "Lớp học trực tuyến mới",
    "Auto Recording": "Tự động ghi hình",
    "Duration (in minutes)": "Thời lượng (phút)",
    "Time must be in 24 hour format (HH:mm). Example 11:30 or 22:00": "Thời gian phải theo định dạng 24 giờ (HH:mm). Ví dụ 11:30 hoặc 22:00",
    "Please enter a valid time in the format HH:mm.": "Vui lòng nhập giờ hợp lệ theo định dạng HH:mm (ví dụ 14:30).",
    "Please select a future date and time.": "Vui lòng chọn thời gian trong tương lai.",
    "Please select a duration.": "Vui lòng chọn thời lượng.",
    "Please select a conferencing provider and add an account to the batch to create live classes.": "Vui lòng chọn nhà cung cấp phòng học (Zoom/Google Meet) và thêm tài khoản vào đợt học để tạo lớp trực tuyến.",
    "Ask your site administrator to set up your Google Calendar to schedule Zoom classes.": "Vui lòng liên hệ quản trị viên để cài đặt Google Calendar cho việc lên lịch lớp học Zoom.",
    "Ask your site administrator to add a Google Calendar to this Google Meet account.": "Vui lòng liên hệ quản trị viên để thêm Google Calendar vào tài khoản Google Meet này.",

    # MemberForm & BulkCertificatesForm
    "New Member": "Thành viên mới",
    "Edit Member": "Chỉnh sửa thành viên",
    "Member added successfully": "Đã thêm thành viên thành công",
    "Member updated": "Đã cập nhật thành viên",
    "Unable to add member": "Không thể thêm thành viên",
    "Unable to update member": "Không thể cập nhật thành viên",
    "Generate": "Tạo chứng chỉ",
    "Generate Certificates": "Cấp chứng chỉ hàng loạt",
    "Certificates generated successfully": "Đã tạo chứng chỉ thành công",
    "This batch has no students to certify.": "Đợt học này chưa có học viên nào đủ điều kiện cấp chứng chỉ.",
    "Enabling this will publish the certificate on the certified participants page.": "Bật mục này sẽ công khai chứng chỉ trên trang danh sách học viên có chứng nhận.",
    "Unable to generate certificate": "Không thể tạo chứng chỉ",

    # AnnouncementForm & EmailTemplateForm
    "New Announcement": "Thông báo mới",
    "Announcement": "Thông báo",
    "Announcement has been sent successfully": "Đã gửi thông báo thành công",
    "Announcement is required": "Vui lòng nhập nội dung thông báo",
    "Add students to the batch to make an announcement": "Thêm học viên vào đợt học để có thể gửi thông báo",
    "New Email Template": "Mẫu email mới",
    "Email Template created successfully": "Đã tạo mẫu email thành công",
    "Error creating email template": "Lỗi khi tạo mẫu email",
    "Subject is required": "Vui lòng nhập tiêu đề email",
    "Reply To": "Email phản hồi",
    "Reply To is required": "Vui lòng nhập email phản hồi",
    "Use HTML content for the email response": "Sử dụng nội dung định dạng HTML cho email",

    # Validation & Permissions
    "Title is required": "Vui lòng nhập tiêu đề",
    "Please enter a title.": "Vui lòng nhập tiêu đề.",
    "Email is required": "Vui lòng nhập địa chỉ email",
    "Please select a course": "Vui lòng chọn một khóa học",
    "Please select a member": "Vui lòng chọn một thành viên",
    "Please select a time.": "Vui lòng chọn thời gian.",
    "Please select a timezone.": "Vui lòng chọn múi giờ.",
    "Schedule Start is required when scheduling is enabled.": "Vui lòng chọn thời gian bắt đầu khi bật giới hạn thời gian.",
    "Schedule End must be after Schedule Start.": "Thời gian kết thúc phải diễn ra sau thời gian bắt đầu.",
    "File upload failed. Please try again.": "Tải file thất bại. Vui lòng thử lại.",
    "Please fill the mandatory fields: {0}": "Vui lòng điền các trường bắt buộc: {0}",
    "This site is in read-only mode.": "Hệ thống hiện đang ở chế độ chỉ đọc.",
    "Not saved": "Chưa lưu thay đổi",
    "{0} Your changes are not saved.": "{0} Các thay đổi của bạn chưa được lưu.",
    "You are not permitted to create a course.": "Bạn không có quyền tạo khóa học mới.",
    "You are not permitted to create a batch.": "Bạn không có quyền tạo đợt học mới.",
    "You are not permitted to manage programs.": "Bạn không có quyền quản lý lộ trình học.",
    "You are not permitted to manage assignments.": "Bạn không có quyền quản lý bài tập.",
    "You are not permitted to manage chapters.": "Bạn không có quyền quản lý chương học.",
    "You are not permitted to manage members.": "Bạn không có quyền quản lý thành viên.",
    "You are not permitted to manage programming exercises.": "Bạn không có quyền quản lý bài tập lập trình.",
    "You are not permitted to generate certificates for this batch.": "Bạn không có quyền cấp chứng chỉ cho đợt học này.",
    "You are not permitted to make an announcement for this batch.": "Bạn không có quyền gửi thông báo cho đợt học này.",
    "You do not have permission to add assessments to this batch.": "Bạn không có quyền thêm bài đánh giá vào đợt học này.",
    "You do not have permission to add courses to this batch.": "Bạn không có quyền thêm khóa học vào đợt học này.",
    "You do not have permission to create email templates.": "Bạn không có quyền tạo mẫu email.",
    "You do not have permission to enroll students in this batch.": "Bạn không có quyền ghi danh học viên vào đợt học này.",
    "You do not have permission to enroll students in this course.": "Bạn không có quyền ghi danh học viên vào khóa học này.",
    "You can only edit your own profile.": "Bạn chỉ có thể chỉnh sửa hồ sơ của chính mình.",
}

added_count = 0
updated_count = 0

for src, tr in form_translations.items():
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
print(f"Đã bổ sung thành công {added_count} bản dịch mới và cập nhật {updated_count} bản dịch cho Forms & Modals!")
