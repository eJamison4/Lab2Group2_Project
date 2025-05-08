from django.test import TestCase
from TA_Scheduler_App.models import User, Section, Assignment
from TA_Scheduler_App.assignment_features import AssignmentFeatures


class AssignmentUnitTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin1',
            password='adminpass',
            user_type='admin',
            email='admin1@example.com'
        )
      
        self.instructor = User.objects.create_user(
            username='instructor1',
            password='instructorpass',
            user_type='instructor',
            email='instructor1@example.com'
        )
      
        self.ta = User.objects.create_user(
            username='ta1',
            password='tapass',
            user_type='ta',
            email='ta1@example.com'
        )

        self.section = Section.objects.create(
            name='CS351-Lab1',
            course_name='CS351',
            section_type='lab'
        )
      #Create
    def test_create_assignment_success_admin(self):
        success, message = AssignmentFeatures.create_assignment(self.admin.username, self.ta.username, self.section.id)
        self.assertTrue(success)
        self.assertEqual(message, "Assignment created successfully.")
        self.assertEqual(Assignment.objects.count(), 1)

    def test_create_assignment_permission_denied(self):
        # Instructor tries to create an assignment
        success, message = AssignmentFeatures.create_assignment(self.instructor.username, self.ta.username, self.section.id)
        self.assertFalse(success)
        self.assertEqual(message, "Only admins or TAs can create assignments.")

    def test_create_assignment_success_ta(self):
        # allow ta's to assign themselves
        success, message = AssignmentFeatures.create_assignment(self.ta.username, self.ta.username, self.section.id)
        self.assertTrue(success)
        self.assertEqual(Assignment.objects.count(), 1)

    def test_create_assignment_user_not_found(self):
        success, message = AssignmentFeatures.create_assignment(self.admin.username, "nonexistentuser", self.section.id)
        self.assertFalse(success)
        self.assertEqual(message, "Assigned user does not exist.")
        self.assertEqual(Assignment.objects.count(), 0)

    def test_create_assignment_section_not_found(self):
        success, message = AssignmentFeatures.create_assignment(self.admin.username, self.ta.username, 9999)
        self.assertFalse(success)
        self.assertEqual(message, "Section does not exist.")
        self.assertEqual(Assignment.objects.count(), 0)

    def test_create_assignment_duplicate(self):
        AssignmentFeatures.create_assignment(self.admin.username, self.ta.username, self.section.id)
        success, message = AssignmentFeatures.create_assignment(self.admin.username, self.ta.username, self.section.id)
        self.assertFalse(success)
        self.assertEqual(message, "Assignment already exists.")
        self.assertEqual(Assignment.objects.count(), 1)

  #delete########################

    def test_delete_assignment_success(self):
        AssignmentFeatures.create_assignment(self.admin.username, self.ta.username, self.section.id)
        success, message = AssignmentFeatures.delete_assignment(self.admin.username, self.ta.username, self.section.id)
        self.assertTrue(success)
        self.assertEqual(message, "Assignment deleted successfully.")
        self.assertEqual(Assignment.objects.count(), 0)

    def test_delete_assignment_not_found(self):
        success, message = AssignmentFeatures.delete_assignment(self.admin.username, self.ta.username, self.section.id)
        self.assertFalse(success)
        self.assertEqual(message, "Assignment does not exist.")

    def test_delete_assignment_user_not_found(self):
        success, message = AssignmentFeatures.delete_assignment(self.admin.username, "fakeuser", self.section.id)
        self.assertFalse(success)
        self.assertEqual(message, "Assigned user does not exist.")

    def test_delete_assignment_section_not_found(self):
        success, message = AssignmentFeatures.delete_assignment(self.admin.username, self.ta.username, 9999)
        self.assertFalse(success)
        self.assertEqual(message, "Section does not exist.")

    def test_delete_assignment_permission_denied(self):
        # Instructor tries to delete an assignment
        AssignmentFeatures.create_assignment(self.admin.username, self.ta.username, self.section.id)
        success, message = AssignmentFeatures.delete_assignment(self.instructor.username, self.ta.username, self.section.id)
        self.assertFalse(success)
        self.assertEqual(message, "Only admins or TAs can delete assignments.")
        self.assertEqual(Assignment.objects.count(), 1)
