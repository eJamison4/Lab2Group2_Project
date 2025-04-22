from django.test import TestCase
from TA_Scheduler_App.course_features import CourseFeatures
from TA_Scheduler_App.models import Course


class CourseAcceptanceTests(TestCase):

    def test_create_course_success(self):
        # Basic course creation
        course = CourseFeatures.create_course(
            course_id="MATH101", course_title="Calculus I", course_description="Limits, derivatives, integrals"
        )
        self.assertIsNotNone(course)
        self.assertEqual(course.courseID, "MATH101")
        self.assertEqual(course.courseTitle, "Calculus I")
        self.assertEqual(course.courseDescription, "Limits, derivatives, integrals")

    def test_create_course_duplicate_id(self):
        # Try creating a duplicate course with the same ID
        CourseFeatures.create_course("PHYS101", "Physics I", "Mechanics")
        with self.assertRaises(Exception):  # Django will raise an IntegrityError unless handled
            CourseFeatures.create_course("PHYS101", "Duplicate", "Should fail")
    
    def test_edit_existing_course_fields(self):
        #TODO
