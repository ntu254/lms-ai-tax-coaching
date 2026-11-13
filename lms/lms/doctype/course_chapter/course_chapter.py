# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

from lms.lms.utils import get_lesson_count


class CourseChapter(Document):
	def on_update(self):
		self.update_lesson_count()

	def update_lesson_count(self):
		"""Update lesson count in the course"""
		frappe.db.set_value("LMS Course", self.course, "lessons", get_lesson_count(self.course))


def resolve_scorm_access(course: str, lesson: str | None) -> frappe._dict:
	return frappe._dict(can_access=False, locked=False)


def get_scorm_lesson(chapter: str) -> str | None:
	return None


@frappe.whitelist()
def get_scorm_playback(chapter: str) -> dict:
	return {"can_access": False, "locked": False}
