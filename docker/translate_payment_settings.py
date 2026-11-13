import os
import frappe

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init("lms.localhost")
frappe.connect()

print("--- Nạp bản dịch cho Cài đặt Thanh toán (Payment Settings) & Cấu hình ---")

translations = {
    # 1. Menu & Tiêu đề nhóm Cài đặt
    "Payment": "Thanh toán",
    "Configuration": "Cấu hình",
    "Gateways": "Cổng thanh toán",
    "Transactions": "Giao dịch",
    "Coupons": "Mã giảm giá",
    "System Configuration": "Cấu hình hệ thống",
    "Course Configuration": "Cấu hình khóa học",
    "Communication": "Giao tiếp & Liên hệ",
    "User Management": "Quản lý người dùng",
    "Customization": "Tùy chỉnh giao diện",

    # 2. Trang Cấu hình Thanh toán (Settings > Payment > Configuration)
    "Default Currency": "Tiền tệ mặc định",
    "Default currency used for course and batch pricing.": "Tiền tệ mặc định dùng cho định giá khóa học và đợt học.",
    "Show USD equivalent amount": "Hiển thị số tiền tương đương USD",
    "Show USD Equivalent": "Hiển thị số tiền tương đương USD",
    "If enabled, it shows the USD equivalent amount for all transactions based on the current exchange rate.": "Nếu bật, hệ thống sẽ hiển thị số tiền tương đương bằng USD cho tất cả giao dịch dựa trên tỷ giá hiện tại.",
    "Apply rounding on equivalent": "Làm tròn số tiền tương đương",
    "Apply Rounding on Equivalent": "Làm tròn số tiền tương đương",
    "If enabled, it applies rounding on the USD equivalent amount.": "Nếu bật, hệ thống sẽ làm tròn số tiền tương đương quy đổi sang USD.",
    "Payment Gateway": "Cổng thanh toán",
    "Payment gateway used to process course and batch purchases.": "Cổng thanh toán dùng để xử lý các giao dịch mua khóa học và đợt học.",
    "Apply GST for India": "Áp dụng thuế GST cho Ấn Độ",
    "If enabled, GST will be applied to the price for students from India.": "Nếu bật, thuế GST sẽ được áp dụng vào giá cho học viên đến từ Ấn Độ.",
    "Payment Reminders": "Nhắc nhở thanh toán",
    "Send payment reminders for batch": "Gửi nhắc nhở thanh toán cho đợt học",
    "Send Payment Reminders for Batch": "Gửi nhắc nhở thanh toán cho đợt học",
    "If enabled, it sends payment reminders to students who left the payment incomplete for a batch.": "Nếu bật, hệ thống sẽ gửi email nhắc nhở thanh toán đến các học viên chưa hoàn tất thanh toán đợt học.",
    "Send payment reminders for course": "Gửi nhắc nhở thanh toán cho khóa học",
    "Send Payment Reminders for Course": "Gửi nhắc nhở thanh toán cho khóa học",
    "If enabled, it sends payment reminders to students who left the payment incomplete for a course.": "Nếu bật, hệ thống sẽ gửi email nhắc nhở thanh toán đến các học viên chưa hoàn tất thanh toán khóa học.",
    "Payment Settings": "Cài đặt thanh toán",
    "Payment Reminder Template": "Mẫu nhắc nhở thanh toán",
    "Payments app is not installed": "Ứng dụng thanh toán chưa được cài đặt",

    # 3. Cổng thanh toán (Payment Gateways)
    "Payment Gateways": "Cổng thanh toán",
    "New Payment Gateway": "Cổng thanh toán mới",
    "Provider": "Nhà cung cấp",
    "Choose a provider to configure its credentials.": "Chọn một nhà cung cấp dịch vụ để cấu hình thông tin đăng nhập.",
    "Select a provider": "Chọn một nhà cung cấp",
    "No file attached": "Chưa đính kèm tệp",
    "Saved, leave blank to keep it": "Đã lưu, để trống để giữ nguyên",
    "Delete {0}?": "Xóa {0}?",
    "This stops {0} being offered at checkout. Its credentials remain in {1}.": "Thao tác này sẽ ngừng hiển thị {0} khi thanh toán. Thông tin kết nối vẫn được lưu trong {1}.",
    "Payment gateway deleted successfully": "Đã xóa cổng thanh toán thành công",
    "Error deleting payment gateway": "Lỗi khi xóa cổng thanh toán",
    "Error loading payment gateway": "Lỗi khi tải cổng thanh toán",
    "Error loading payment providers": "Lỗi khi tải danh sách nhà cung cấp thanh toán",
    "Error loading provider fields": "Lỗi khi tải các trường cấu hình nhà cung cấp",
    "Payment gateway created successfully": "Đã tạo cổng thanh toán thành công",
    "Payment gateway updated successfully": "Đã cập nhật cổng thanh toán thành công",
    "Error saving payment gateway": "Lỗi khi lưu cổng thanh toán",

    # 4. Giao dịch (Transactions)
    "Billing Name": "Tên thanh toán",
    "Amount": "Số tiền",
    "Amount with GST": "Số tiền gồm thuế GST",
    "Paid For": "Thanh toán cho",
    "Payment ID": "Mã thanh toán",
    "Order ID": "Mã đơn hàng",
    "Payment for Certificate": "Thanh toán cấp chứng chỉ",
    "Member Consent": "Sự đồng ý của thành viên",
    "The user this payment is recorded against.": "Học viên được ghi nhận cho khoản thanh toán này.",
    "What this payment paid for.": "Nội dung thanh toán cho khóa học hoặc đợt học này.",
    "The currency the amount above is in.": "Loại tiền tệ của số tiền thanh toán ở trên.",
    "The address this payment is billed to.": "Địa chỉ xuất hóa đơn cho khoản thanh toán này.",
    "The coupon this payment was discounted by.": "Mã giảm giá được áp dụng cho khoản thanh toán này.",
    "Read from the coupon above every time this is saved.": "Tự động đọc từ mã giảm giá ở trên mỗi khi lưu.",
    "Original Amount": "Số tiền gốc",
    "Discount Amount": "Số tiền giảm giá",
    "GSTIN": "Mã số thuế GSTIN",
    "PAN": "Mã định danh PAN",
    "All Payments": "Tất cả thanh toán",
    "Paid": "Đã thanh toán",
    "Unpaid": "Chưa thanh toán",
    "For Certificate": "Cấp chứng chỉ",
    "For Course": "Khóa học",
    "Filter by payment status": "Lọc theo trạng thái thanh toán",
    "Open the Course": "Mở khóa học",
    "Open the Batch": "Mở đợt học",
    "Delete this transaction?": "Xóa giao dịch này?",
    "This will permanently delete this payment record, including its billing details. This cannot be undone.": "Thao tác này sẽ xóa vĩnh viễn bản ghi thanh toán này cùng chi tiết hóa đơn. Không thể hoàn tác.",
    "Transaction deleted successfully": "Đã xóa giao dịch thành công",
    "Unable to delete transaction": "Không thể xóa giao dịch",
    "Received": "Đã nhận thanh toán",
    "Actions for {0}": "Thao tác cho {0}",

    # 5. Mã giảm giá (Coupons)
    "Discount": "Giảm giá",
    "Discount Type": "Loại giảm giá",
    "Percentage": "Phần trăm (%)",
    "Fixed Amount": "Số tiền cố định",
    "Discount Percentage": "Phần trăm giảm giá",
    "Expires On": "Hết hạn vào ngày",
    "Usage Limit": "Giới hạn số lần dùng",
    "Unlimited": "Không giới hạn",
    "Redeemed": "Đã sử dụng",
    "Enabled": "Kích hoạt",
    "Enable {0}": "Kích hoạt {0}",
    "This will permanently delete the coupon and the code will no longer be valid.": "Thao tác này sẽ xóa vĩnh viễn mã giảm giá và mã sẽ không còn hiệu lực.",
    "Coupon deleted successfully": "Đã xóa mã giảm giá thành công",
    "Error deleting coupon": "Lỗi khi xóa mã giảm giá",
    "Error updating coupon": "Lỗi khi cập nhật mã giảm giá",

    # 6. Thương hiệu & Giao diện (Branding & Preferences)
    "Branding": "Thương hiệu",
    "Brand Settings": "Cài đặt thương hiệu",
    "Brand Name": "Tên thương hiệu",
    "Set the name of your brand. Appears in the left sidebar.": "Đặt tên cho thương hiệu của bạn. Tên này xuất hiện ở thanh bên trái.",
    "Enter Brand Name": "Nhập tên thương hiệu",
    "Brand Logo": "Logo thương hiệu",
    "Appears in the left sidebar. Recommended size is 32x32 px in PNG or SVG": "Xuất hiện ở thanh bên trái. Kích thước khuyến nghị là 32x32 px định dạng PNG hoặc SVG",
    "Favicon": "Biểu tượng trang (Favicon)",
    "Appears next to the title in your browser tab. Recommended size is 32x32 px in PNG or ICO": "Xuất hiện bên cạnh tiêu đề trên tab trình duyệt. Kích thước khuyến nghị là 32x32 px định dạng PNG hoặc ICO",
    "Preferences": "Tùy chọn chung",
    "System Language": "Ngôn ngữ hệ thống",
    "The language this site falls back to.": "Ngôn ngữ mặc định hệ thống sử dụng.",
    "System Timezone": "Múi giờ hệ thống",
    "The timezone new batches and courses start from.": "Múi giờ mặc định cho các khóa học và đợt học mới.",
    "Search timezone": "Tìm kiếm múi giờ",
    "Text Direction": "Hướng văn bản",
    "Auto follows the language of the site.": "Tự động điều chỉnh theo ngôn ngữ của trang web.",
    "Access & Availability": "Quyền truy cập & Tính khả dụng",
    "Allow Guest Access": "Cho phép khách truy cập",
    "If enabled, users can access the course and batch lists without logging in.": "Nếu bật, người dùng có thể xem danh sách khóa học và đợt học mà không cần đăng nhập.",
    "Disable PWA": "Tắt PWA (Ứng dụng web cài đặt)",
    "If checked, users will not be able to install the application as a Progressive Web App.": "Nếu chọn, người dùng sẽ không thể cài đặt ứng dụng dưới dạng Progressive Web App (PWA).",
    "Allow Job Posting": "Cho phép đăng tin tuyển dụng",
    "If enabled, users can post job openings on the job board. Else only admins can post jobs.": "Nếu bật, thành viên có thể đăng tin tuyển dụng lên trang việc làm. Nếu tắt, chỉ quản trị viên mới được đăng.",
    "Send calendar invite for evaluations": "Gửi thư mời lịch cho buổi đánh giá",
    "If enabled, it sends google calendar invite to the student for evaluations.": "Nếu bật, hệ thống sẽ gửi thư mời Google Calendar cho học viên khi có lịch đánh giá.",
    "Notifications": "Thông báo",
    "Send Notification for Published Courses": "Gửi thông báo khi xuất bản khóa học",
    "Notify members when a new course is published.": "Thông báo cho học viên khi có khóa học mới được xuất bản.",
    "Send Notification for Published Batches": "Gửi thông báo khi xuất bản đợt học",
    "Notify members when a new batch is published.": "Thông báo cho học viên khi có đợt học mới được xuất bản.",

    # 7. Tiến độ khóa học (Course Progress)
    "Progress": "Tiến độ học tập",
    "Lesson Completion": "Hoàn thành bài học",
    "Lesson Completion Time (seconds)": "Thời gian hoàn thành bài học (giây)",
    "Seconds a learner must stay on a lesson before it is marked complete.": "Số giây học viên phải lưu lại bài học trước khi được đánh dấu hoàn thành.",
    "Enforce completion": "Bắt buộc hoàn thành",
    "A lesson is marked complete only once the selected items are done.": "Bài học chỉ được đánh dấu hoàn thành sau khi hoàn tất các mục được chọn.",
    "Enforce passing": "Bắt buộc đạt điểm",
    "The selected items must be passed, not just attempted.": "Các mục được chọn phải đạt điểm yêu cầu, không chỉ làm thử.",
    "Prevent Skipping Videos": "Chặn tua nhanh video",
    "Learners can't jump ahead of the furthest point they've watched. Turn on with Videos above to require watching the whole video.": "Học viên không thể tua qua đoạn chưa xem. Bật cùng mục Video ở trên để yêu cầu xem toàn bộ video.",
    "This is not enforced for videos from Cloudflare Stream, Google Drive, Aparat or other embedded links.": "Không áp dụng cho video từ Cloudflare Stream, Google Drive, Aparat hoặc liên kết nhúng khác.",
    "Videos": "Video",
    "Open-ended quizzes": "Bài tập tự luận",
    "Programming exercises": "Bài tập lập trình",
    "The lesson completes only after an instructor grades it.": "Bài học chỉ hoàn thành sau khi giảng viên chấm điểm.",
    "A video that fails to load, or comes from Cloudflare Stream, Google Drive, Aparat or another embedded link, cannot be tracked, so its lesson completes on the completion time instead.": "Video bị lỗi tải hoặc nhúng từ link ngoài sẽ không theo dõi được, bài học sẽ hoàn thành theo thời gian quy định.",

    # 8. Liên hệ & Mẫu Email (Communication & Email Templates)
    "Contact Information": "Thông tin liên hệ",
    "Email Templates": "Mẫu email",
    "Batch Confirmation Template": "Mẫu xác nhận đợt học",
    "Certificate Email Template": "Mẫu email gửi chứng chỉ",
    "Replaces the wording of the batch enrollment notification.": "Thay thế nội dung thông báo ghi danh đợt học.",
    "Replaces the wording of the certification notification.": "Thay thế nội dung thông báo cấp chứng chỉ.",
    "Email Accounts": "Tài khoản email",
    "Email Template": "Mẫu email",
    "Services": "Dịch vụ tích hợp",
    "Google Calendar": "Google Calendar",
    "Google Meet": "Google Meet",
    "Zoom": "Zoom",
    "Raven": "Trò chuyện (Raven)",
    "SEO": "Tối ưu tìm kiếm (SEO)",
    "Meta Description": "Mô tả Meta (SEO)",
    "This description will be shown on lists and pages that don't have meta description": "Mô tả này sẽ hiển thị trên các trang và danh sách chưa có mô tả riêng.",
    "Meta Keywords": "Từ khóa Meta (SEO)",
    "Comma separated keywords for search engines to find your website.": "Các từ khóa phân cách bằng dấu phẩy để công cụ tìm kiếm tìm thấy trang web của bạn.",
    "Meta Image": "Hình ảnh đại diện Meta (SEO)",
    "Default social-share image used when pages lack their own meta image.": "Hình ảnh chia sẻ mạng xã hội mặc định khi trang chưa có ảnh đại diện riêng.",
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
print(f"Đã thêm {added_count} và cập nhật {updated_count} bản dịch cho Cài đặt Thanh toán & Cấu hình!")
