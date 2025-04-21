from django.test import TestCase, Client
from django.urls import reverse
from TA_Scheduler_App.models import User

#no real login logic yet since authentication isn't ready
class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="testuser",
            password="testpass",  # Not hashed yet
          
            userEmail="test@example.com",
            phoneNumber=1234567890,
            firstName="Test",
            lastName="User",
            homeAddress="123 Test St"
        )

    def test_login_success(self):
        response = self.client.post("/", {
            "username": "testuser",
            "password": "testpass"
          
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Either username or password is incorrect!")

    def test_login_blank_username(self):
        response = self.client.post("/", {
            "username": "",
            "password": "testpass"
          
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_blank_password(self):
        response = self.client.post("/", {
            "username": "testuser",
            "password": ""
          
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_blank_both(self):
        response = self.client.post("/", {
            "username": "",
            "password": ""
          
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_incorrect_credentials(self):
        response = self.client.post("/", {
            "username": "wronguser",
            "password": "wrongpass"
          
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Either username or password is incorrect!")
