import unittest
from unittest.mock import patch

from lms.lms import api
from lms.lms.doctype.course_lesson import course_lesson
from lms.lms.retired_features import has_permission, query_conditions


class TestRetiredFeatures(unittest.TestCase):
	def test_retired_documents_are_not_available_through_permissions(self):
		self.assertFalse(has_permission(None, "read", "student@example.com"))
		self.assertEqual(query_conditions("student@example.com"), "1=0")

	def test_retired_endpoints_are_not_whitelisted(self):
		import frappe

		for name in (
			"get_job_details",
			"get_job_opportunities",
			"send_job_application_email",
			"get_programming_exercise",
			"evaluate_programming_exercise",
			"create_programming_exercise_submission",
		):
			with self.subTest(name=name):
				self.assertNotIn(getattr(api, name), frappe.whitelisted)

	def test_legacy_exercise_does_not_block_lesson_completion(self):
		rules = {"quiz": None, "open_ended_quiz": None, "assignment": None, "programming_exercise": "Passed"}
		with (
			patch.object(course_lesson, "get_quiz_progress", return_value=True),
			patch.object(course_lesson, "get_assignment_progress", return_value=True),
			patch.object(course_lesson, "get_programming_exercise_progress", return_value=False) as exercise,
		):
			self.assertTrue(course_lesson.lesson_requirements_met("lesson", "learner", rules))
			exercise.assert_not_called()
