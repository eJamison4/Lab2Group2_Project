from django.test import TestCase, Client
from TA_Scheduler_App.models import User, Course, Section, Assignment

class AssignmentAcceptanceTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_user(
            username="admin", password="adminpass", userEmail="admin@example.com",
            firstName="Admin", lastName="User", accountType=2
        )
        self.instructor = User.objects.create_user(
            username="instructor", password="instrpass", userEmail="instr@example.com",
            firstName="Inst", lastName="User", accountType=1
        )
        self.ta = User.objects.create_user(
            username="ta", password="tapass", userEmail="ta@example.com",
            firstName="TA", lastName="User", accountType=0
        )

        self.course = Course.objects.create(courseName="CS101", semester="Fall2025")
        self.section = Section.objects.create(course=self.course, sectionCode="001", instructor="Inst User")

    def test_admin_can_assign_ta_to_section(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.post("/assignments/create/", {
            "user_id": self.ta.pk,
            "section_id": self.section.pk
        })
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(Assignment.objects.filter(userID=self.ta, sectionID=self.section).exists())

    def test_instructor_can_assign_ta(self):
        self.client.login(username="instructor", password="instrpass")
        response = self.client.post("/assignments/create/", {
            "user_id": self.ta.pk,
            "section_id": self.section.pk
        })
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(Assignment.objects.filter(userID=self.ta, sectionID=self.section).exists())
