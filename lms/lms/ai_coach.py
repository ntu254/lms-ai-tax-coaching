import json
import os
import re
import frappe
from frappe import _
from frappe.rate_limiter import rate_limit
import requests

from lms.lms.utils import guest_access_allowed


SYSTEM_PROMPT = """Bạn là trợ lý tư vấn khóa học của Ai Coaching Vietnam.
Chỉ hỗ trợ khách tìm hiểu khóa học, lớp học, học phí, lịch học và cách đăng ký.
Chỉ sử dụng dữ liệu khóa học và lớp học được cung cấp; nếu không có thông tin, hãy nói rõ và hướng dẫn khách xem danh mục hoặc chi tiết khóa học.
Không tự tạo thông tin về khóa học, giá, lịch học, phương thức thanh toán hoặc cam kết.
Nếu khách hỏi kiến thức chuyên môn, tư vấn thuế, tài chính, pháp lý hoặc chủ đề ngoài đào tạo, hãy lịch sự nói bạn chỉ hỗ trợ tìm khóa học và mời khách cho biết nhu cầu học tập.
Trả lời ngắn gọn bằng tiếng Việt."""


def get_live_lms_context() -> str:
	"""Lấy thông tin các Khóa học và Lớp học (Batch) đang mở để đưa vào ngữ cảnh AI."""
	context_parts = []
	if not guest_access_allowed():
		return ""

	# 1. Khóa học đang phát hành
	try:
		courses = frappe.get_all(
			"LMS Course",
			filters={"published": 1},
			fields=["name", "title", "short_introduction", "paid_course", "course_price", "currency"],
			limit=10,
		)
		if courses:
			course_lines = ["\nDANH SÁCH KHÓA HỌC HIỆN CÓ:"]
			for c in courses:
				price_str = (
					f"{c.course_price} {c.currency or 'VND'}"
					if c.paid_course and c.course_price
					else ("Xem chi tiết khóa học" if c.paid_course else "Miễn phí")
				)
				intro = f" - {c.short_introduction}" if c.short_introduction else ""
				course_lines.append(f"• Khóa '{c.title}': {price_str}{intro} (Mã: {c.name})")
			context_parts.append("\n".join(course_lines))
	except Exception:
		pass

	# 2. Lớp học (Batch) đang tuyển sinh
	try:
		batches = frappe.get_all(
			"LMS Batch",
			filters={"published": 1},
			fields=["name", "title", "start_date", "end_date", "amount", "currency"],
			limit=5,
		)
		if batches:
			batch_lines = ["\nLỚP HỌC (BATCH) SẮP KHAI GIẢNG:"]
			for b in batches:
				fee_str = f"{b.amount} {b.currency or 'VND'}" if b.amount else "Xem chi tiết lớp học"
				time_str = f"Khai giảng: {b.start_date}" if b.start_date else ""
				batch_lines.append(f"• Lớp '{b.title}': Học phí {fee_str}. {time_str} (Mã lớp: {b.name})")
			context_parts.append("\n".join(batch_lines))
	except Exception:
		pass


	return "\n".join(context_parts)


def call_gemini_api(prompt: str, user_message: str, api_key: str) -> str | None:
	"""Gọi Google Gemini API nếu có cấu hình API Key."""
	url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
	headers = {"Content-Type": "application/json"}
	payload = {
		"contents": [
			{
				"role": "user",
				"parts": [{"text": f"{prompt}\n\nKhách hỏi: {user_message}"}],
			}
		],
		"generationConfig": {
			"temperature": 0.4,
			"maxOutputTokens": 1000,
		},
	}
	try:
		res = requests.post(url, json=payload, headers=headers, timeout=12)
		if res.status_code == 200:
			data = res.json()
			candidates = data.get("candidates", [])
			if candidates:
				parts = candidates[0].get("content", {}).get("parts", [])
				if parts and "text" in parts[0]:
					return parts[0]["text"]
	except Exception:
		pass
	return None


UNAVAILABLE_MESSAGE = _(
	"Trợ lý tư vấn hiện tạm thời không khả dụng. Bạn có thể xem danh sách khóa học trong lúc chờ."
)


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=30, seconds=60)
def guest_ai_chat(message: str, history: list | None = None) -> dict:
	"""
	API tư vấn tự động cho khách (Guest) truy cập trang chủ / landing page.
	Đảm bảo kiểm soát quyền (không rò rỉ dữ liệu nhạy cảm) và áp dụng rate limit.
	"""
	if not message or not message.strip():
		return {"response": "Vui lòng nhập câu hỏi để tôi có thể hỗ trợ bạn tốt nhất."}

	clean_msg = message.strip()[:1000]

	# Chỉ tải thông tin khóa học khi có dịch vụ AI để xử lý câu hỏi.
	# Thử gọi Gemini AI nếu có key.
	conf = getattr(frappe, "conf", {}) or {}
	db = getattr(frappe, "db", None)
	gemini_key = (
		conf.get("gemini_api_key")
		or os.environ.get("GEMINI_API_KEY")
		or (db.get_single_value("LMS Settings", "gemini_api_key") if db and frappe.get_meta("LMS Settings").has_field("gemini_api_key") else None)
	)

	response_text = None
	if gemini_key:
		context = get_live_lms_context()
		response_text = call_gemini_api(f"{SYSTEM_PROMPT}\n\n{context}", clean_msg, gemini_key)

	if not response_text:
		return {"response": UNAVAILABLE_MESSAGE, "status": "unavailable"}

	return {"response": response_text, "status": "success"}
