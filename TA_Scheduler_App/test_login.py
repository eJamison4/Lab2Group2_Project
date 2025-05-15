from django.test import TestCase, Client
from TA_Scheduler_App.models import User


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = "/"  # root URL based on urls.py
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            userEmail="test@example.com",
            firstName="Test",
            lastName="User",
            homeAddress="123 Main St",
            accountType=1,  # Example: 1 = Teacher
        )

    def test_login_page_loads_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.login_url, {"username": "testuser", "password": "testpass"})
        self.assertNotContains(response, "Either username or password is incorrect!")

    def test_login_with_empty_fields(self):
        response = self.client.post(self.login_url, {"username": "", "password": ""})
        self.assertEqual(response.status_code, 200)

    def test_login_with_invalid_username(self):
        response = self.client.post(self.login_url, {"username": "wronguser", "password": "testpass"})
        self.assertContains(response, "Either username or password is incorrect!")

    def test_login_with_invalid_password(self):
        response = self.client.post(self.login_url, {"username": "testuser", "password": "wrongpass"})
        self.assertContains(response, "Either username or password is incorrect!")

    def test_login_success_behavior_placeholder(self):
        response = self.client.post(self.login_url, {"username": "admin", "password": "admin123"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Either username or password is incorrect!")
