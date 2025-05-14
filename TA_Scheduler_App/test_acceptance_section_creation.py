from django.test import TestCase, Client
from django.urls import reverse
from TA_Scheduler_App.models import User, Course, Section
from datetime import datetime

class LabSectionAcceptanceTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create users
        self.admin = User.objects.create_user(
            userEmail="admin@example.com",
            password="adminpass",
            accountType=2,
            firstName="Admin", lastName="User"
        )

        self.ta = User.objects.create_user(
            userEmail="ta@example.com",
            password="tapass",
            accountType=0,
            firstName="TA", lastName="User"
        )

        self.instructor = User.objects.create_user(
            userEmail="instructor@example.com",
            password="instructorpass",
            accountType=1,
            firstName="Instructor", lastName="User"
        )

        # Create course
        self.course = Course.objects.create(
            courseName="CS101",
            semester="Fall",
            year="2024"
        )

    def test_admin_can_create_section(self):
        self.client.login(userEmail="admin@example.com", password="adminpass")

        response = self.client.post(f"/courses/{self.course.id}/add-section/", {
            "sectionCode": "301",
            "instructor": f"{self.ta.firstName} {self.ta.lastName}"
        })

        self.assertEqual(response.status_code, 302)  # redirect on success
        self.assertTrue(Section.objects.filter(course=self.course, sectionCode="301").exists())

    def test_ta_cannot_access_add_section_page(self):
        self.client.login(userEmail="ta@example.com", password="tapass")

        response = self.client.get(f"/courses/{self.course.id}/add-section/")
        self.assertNotEqual(response.status_code, 200)
        self.assertIn(response.status_code, [302, 403])

    def test_instructor_cannot_access_add_section_page(self):
        self.client.login(userEmail="instructor@example.com", password="instructorpass")

        response = self.client.get(f"/courses/{self.course.id}/add-section/")
        self.assertNotEqual(response.status_code, 200)
        self.assertIn(response.status_code, [302, 403])

    def test_ta_cannot_create_section(self):
        self.client.login(userEmail="ta@example.com", password="tapass")

        response = self.client.post(f"/courses/{self.course.id}/add-section/", {
            "sectionCode": "302",
            "instructor": f"{self.ta.firstName} {self.ta.lastName}"
        })

        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(Section.objects.filter(course=self.course, sectionCode="302").exists())

    def test_instructor_cannot_create_section(self):
        self.client.login(userEmail="instructor@example.com", password="instructorpass")

        response = self.client.post(f"/courses/{self.course.id}/add-section/", {
            "sectionCode": "303",
            "instructor": f"{self.ta.firstName} {self.ta.lastName}"
        })

        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(Section.objects.filter(course=self.course, sectionCode="303").exists())
