import json
import re
import frappe
from frappe import _
import requests

GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


FALLBACK_MODELS = [
	"gemini-3.1-flash-lite-preview",
	"gemini-3.8-flash",
	"gemini-2.5-pro",
	"gemini-flash-latest",
]


def get_gemini_config():
	settings = frappe.get_single("LMS Settings")
	api_key = settings.get_password("gemini_api_key")
	if not api_key:
		if frappe.db.exists("Flow Provider", "gemini"):
			prov = frappe.get_doc("Flow Provider", "gemini")
			api_key = prov.get_password("api_key")

	if not api_key:
		frappe.throw(_("Chưa cấu hình Google Gemini API Key trong LMS Settings."))
	model = settings.gemini_model or "gemini-3.1-flash-lite-preview"
	return api_key, model


def call_gemini(system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
	api_key, preferred_model = get_gemini_config()
	models_to_try = [preferred_model] + [m for m in FALLBACK_MODELS if m != preferred_model]
	last_error = None

	for model in models_to_try:
		url = f"{GEMINI_API_BASE.format(model=model)}?key={api_key}"
		generation_config = {}
		if json_mode:
			generation_config["responseMimeType"] = "application/json"

		payload = {
			"contents": [{"parts": [{"text": user_prompt}]}],
			"systemInstruction": {"parts": [{"text": system_prompt}]},
			"generationConfig": generation_config,
		}

		try:
			res = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=20)
			if res.status_code == 200:
				data = res.json()
				candidates = data.get("candidates", [])
				if candidates:
					return candidates[0]["content"]["parts"][0]["text"].strip()
			else:
				last_error = res.text
		except Exception as e:
			last_error = str(e)

	frappe.log_error("Gemini API Error", last_error or "All models failed")
	frappe.throw(_("Lỗi khi kết nối với Google Gemini AI. Vui lòng thử lại sau."))


@frappe.whitelist()
def ask_lesson_tutor(lesson_title: str, lesson_content: str, question: str) -> dict:
	"""AI Tutor: Answers learner questions about current lesson content in Vietnamese."""
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw(_("Vui lòng đăng nhập để hỏi trợ lý AI."), frappe.PermissionError)

	if not question or not question.strip():
		frappe.throw(_("Vui lòng nhập câu hỏi."))

	system_prompt = (
		"Bạn là trợ lý giảng dạy AI (AI Tutor) thông thái và nhiệt tình của khóa học trực tuyến. "
		"Nhiệm vụ: Giải đáp thắc mắc của học viên dựa trên bài học hiện tại. "
		"Phong cách: Tận tình, giải thích rõ ràng, bằng tiếng Việt chuẩn xác, ngắn gọn, có ví dụ minh họa nếu cần. "
		"Nếu câu hỏi nằm ngoài phạm vi bài học, hãy trả lời ngắn gọn và lịch sự gợi ý học viên tập trung vào bài học."
	)

	user_prompt = f"""
	=== BÀI HỌC: {lesson_title} ===
	Nội dung bài học:
	{lesson_content[:4000]}
	
	=== CÂU HỎI CỦA HỌC VIÊN ===
	{question}
	"""

	answer = call_gemini(system_prompt, user_prompt, json_mode=False)
	return {"answer": answer}


@frappe.whitelist()
def summarize_lesson(lesson_title: str, lesson_content: str) -> dict:
	"""Summarizes lesson into 3-5 key takeaways."""
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw(_("Vui lòng đăng nhập."), frappe.PermissionError)

	system_prompt = (
		"Bạn là chuyên gia sư phạm. Hãy tóm tắt bài học thành 3 đến 5 gạch đầu dòng cô đọng nhất "
		"những kiến thức cốt lõi cần nhớ, hoàn toàn bằng tiếng Việt."
	)

	user_prompt = f"""
	Bài học: {lesson_title}
	Nội dung:
	{lesson_content[:5000]}
	"""

	summary = call_gemini(system_prompt, user_prompt, json_mode=False)
	return {"summary": summary}


@frappe.whitelist()
def generate_quiz_from_lesson(lesson_title: str, lesson_content: str, num_questions: int = 5) -> list:
	"""Generates multiple choice quiz questions from lesson content for instructors."""
	frappe.only_for(["Moderator", "Course Creator", "Batch Evaluator"])

	num_questions = min(max(int(num_questions or 5), 1), 10)

	system_prompt = (
		"Bạn là chuyên gia khảo thí và ra đề bài giảng. Dựa vào nội dung bài học, hãy tạo ra các câu hỏi trắc nghiệm khách quan. "
		"Mỗi câu hỏi có 4 lựa chọn A, B, C, D và chỉ có 1 đáp án đúng. "
		"Trả về kết quả dưới định dạng JSON list các object có schema: "
		'[{"question": "Nội dung câu hỏi", "options": [{"text": "Phương án 1", "is_correct": 1}, {"text": "Phương án 2", "is_correct": 0}, {"text": "Phương án 3", "is_correct": 0}, {"text": "Phương án 4", "is_correct": 0}], "explanation": "Giải thích vì sao đúng"}]'
	)

	user_prompt = f"""
	Bài học: {lesson_title}
	Số lượng câu hỏi cần tạo: {num_questions}
	Nội dung bài học:
	{lesson_content[:5000]}
	"""

	raw_json = call_gemini(system_prompt, user_prompt, json_mode=True)
	try:
		# Strip potential markdown formatting if returned
		cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_json.strip())
		questions = json.loads(cleaned)
		if not isinstance(questions, list):
			questions = questions.get("questions", [])
		return questions
	except Exception as e:
		frappe.log_error("JSON Parse Error from Gemini Quiz Generator", str(e))
		frappe.throw(_("Không thể xử lý định dạng câu hỏi do AI tạo. Vui lòng thử lại."))


@frappe.whitelist(allow_guest=True)
def advise_courses(message: str, history: str | list = None) -> dict:
	"""AI Course Advisor Chatbot: Recommends courses based on user goals, background, or budget."""
	if not message or not message.strip():
		frappe.throw(_("Vui lòng nhập nội dung cần tư vấn."))

	if isinstance(history, str):
		try:
			history = json.loads(history)
		except Exception:
			history = []
	history = history or []

	# 1. Fetch all published courses from database
	courses = frappe.get_all(
		"LMS Course",
		filters={"published": 1, "upcoming": 0},
		fields=["name", "title", "short_introduction", "category", "course_price", "currency", "lessons"],
		order_by="creation desc",
	)

	course_catalog = []
	for c in courses:
		price_str = f"{c.course_price:,.0f} VNĐ" if c.course_price else "Miễn phí"
		course_catalog.append(
			f"- Tên khóa học: {c.title}\n"
			f"  Mã khóa học (Slug): {c.name}\n"
			f"  Danh mục: {c.category or 'Tổng hợp'}\n"
			f"  Học phí: {price_str}\n"
			f"  Số bài học: {c.lessons or 0}\n"
			f"  Mô tả: {c.short_introduction or 'Khóa học chất lượng cao'}\n"
			f"  Link: /courses/{c.name}"
		)

	catalog_text = "\n\n".join(course_catalog) if course_catalog else "Hiện chưa có khóa học công khai."

	system_prompt = (
		"Bạn là Chuyên viên tư vấn tuyển sinh AI tận tâm, chuyên nghiệp và thân thiện của học viện trực tuyến.\n"
		"Nhiệm vụ: Lắng nghe mục tiêu, nhu cầu, trình độ hoặc ngân sách của người học và tư vấn 1-2 khóa học phù hợp nhất từ danh mục dưới đây.\n\n"
		f"=== DANH MỤC KHÓA HỌC HIỆN CÓ CỦA HỌC VIỆN ===\n{catalog_text}\n============================================\n\n"
		"QUY TẮC TƯ VẤN QUAN TRỌNG:\n"
		"1. Luôn trả lời bằng tiếng Việt tự nhiên, nhiệt tình, xưng hô 'mình - bạn' hoặc 'em - anh/chị'.\n"
		"2. Chỉ tư vấn các khóa học có trong danh mục trên. Nếu người học hỏi về lĩnh vực học viện chưa có, hãy lịch sự thông báo và gợi ý khóa gần nhất nếu có.\n"
		"3. Với mỗi khóa học được gợi ý, BẮT BUỘC cung cấp: Tên khóa học, lý do phù hợp, học phí và kèm liên kết dạng markdown: [👉 Xem chi tiết khóa học](/courses/<mã-khóa-học>).\n"
		"4. Trả lời súc tích, định dạng gạch đầu dòng rõ ràng, có điểm nhấn icon emoji."
	)

	# Format conversation history
	formatted_history = []
	for item in history[-6:]:  # Keep last 3 turns
		role = "Người học" if item.get("role") == "user" else "Tư vấn viên AI"
		formatted_history.append(f"{role}: {item.get('text', '')}")

	history_text = "\n".join(formatted_history)
	user_prompt = f"""Lịch sử trò chuyện trước đó:
{history_text}

Người học hỏi:
{message}
"""
	try:
		reply = call_gemini(system_prompt, user_prompt, json_mode=False)
	except Exception as e:
		frappe.clear_messages()
		if "gemini_api_key" in str(e) or "Chưa cấu hình" in str(e) or "Password" in str(e) or "mật khẩu" in str(e):
			reply = "Hiện tại hệ thống tư vấn AI đang chờ cấu hình Google Gemini API Key trong trang Quản trị (Desk > LMS Settings). Bạn có thể xem ngay các khóa học chất lượng trên trang chủ nhé! 😊"
		else:
			raise e
	return {"reply": reply}
