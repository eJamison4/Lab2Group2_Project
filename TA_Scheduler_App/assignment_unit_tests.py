from django.test import TestCase
from TA_Scheduler_App.models import User, Course, Section, Assignment
from TA_Scheduler_App.assignment_features import assignment_features

class AssignmentUnitTests(TestCase):
    def setUp(self):
        # Create users
        self.admin = User.objects.create_user(
            username='admin1',
            password='pass123',
            userEmail='admin1@example.com',
            phoneNumber=1234567890,
            firstName='Admin',
            lastName='User',
            homeAddress='Admin Address',
            accountType=2
        )

        self.instructor = User.objects.create_user(
            username='instructor1',
            password='pass123',
            userEmail='instructor1@example.com',
            phoneNumber=1234567891,
            firstName='Instructor',
            lastName='User',
            homeAddress='Instructor Address',
            accountType=1
        )

        self.ta = User.objects.create_user(
            username='ta1',
            password='pass123',
            userEmail='ta1@example.com',
            phoneNumber=1234567892,
            firstName='TA',
            lastName='User',
            homeAddress='TA Address',
            accountType=0
        )

        # Create course and section
        self.course = Course.objects.create(courseName='CS101', semester='Fall 2025')
        self.section = Section.objects.create(course=self.course, sectionCode='001', instructor='Instructor Name')

    def test_create_assignment(self):
        # Call feature method
        assignment = assignment_features.create_assignment(self=None, inSection=self.section, inUser=self.ta)

        # Assertions
        self.assertEqual(assignment.userID, self.ta)
        self.assertEqual(assignment.sectionID, self.section)
        self.assertEqual(assignment.graderStatus, 0)
        self.assertEqual(Assignment.objects.count(), 1)

    def test_delete_existing_assignment(self):
        # Create and save assignment
        assignment = Assignment.objects.create(userID=self.ta, sectionID=self.section)

        # Delete it via feature method
        result = assignment_features.delete_assignment(self=None, assignmentID=assignment.id)

        # Assertions
        self.assertTrue(result)
        self.assertEqual(Assignment.objects.count(), 0)

    def test_delete_nonexistent_assignment(self):
        # Try deleting an assignment ID that doesn’t exist
        result = assignment_features.delete_assignment(self=None, assignmentID=9999)

        # Assertions
        self.assertFalse(result)
        self.assertEqual(Assignment.objects.count(), 0)
