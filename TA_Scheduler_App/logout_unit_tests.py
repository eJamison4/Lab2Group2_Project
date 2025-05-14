from django.test import TestCase, Client
from TA_Scheduler_App.models import User


class TestLogoutAcceptance(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a user (TA for this example)
        self.user = User.objects.create(
            username="ta1",
            password="tapass",
            userEmail="ta@email.com",
            phoneNumber=9876543210,
            firstName="Tim",
            lastName="Assistant",
            homeAddress="2 TA Blvd",
            accountType=0,  # TA
        )

    def test_logout_redirects_to_login(self):
        # Simulate login by setting session manually
        session = self.client.session
        session["_auth_user_id"] = self.user.id
        session.save()

        # Log out
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertEqual(response["Location"], "/login/")  #target

    def test_access_after_logout_redirects_to_login(self):
        # Simulate login
        session = self.client.session
        session["_auth_user_id"] = self.user.id
        session.save()

        self.client.get("/logout/")

        # Try to access protected page
        response = self.client.get("/accounts/")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["Location"].startswith("/login/"))
