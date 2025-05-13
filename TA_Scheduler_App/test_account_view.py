# tests_acceptance.py
from django.test import TestCase, Client
from django.urls import reverse
from TA_Scheduler_App.models import User


class TestAccountView(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="Admin", email="", password="Admin")

    def _login(self, usr, pwd):
        ok = self.client.login(username=usr, password=pwd)
        self.assertTrue(ok, f"Login failed for {usr!r}")

    def test_all_features(self):
        # Create
        self._login("Admin", "Admin")
        response = self.client.post(
            reverse("accounts"),
            {
                "action": "create",
                "username": "bob",
                "password": "pw",
                "userEmail": "bob@example.com",
                "firstName": "Bob",
                "lastName": "B",
                "homeAddress": "1 Oak",
            },
        )

        self.assertEqual(User.objects.count(), 2, msg="Number of users should be 2")
        self.assertRedirects(response, reverse("accounts"))

        bob = User.objects.get(username="bob", userEmail="bob@example.com")
        # Edit
        response = self.client.post(
            reverse("accounts"),
            {
                "action": "edit",
                "pk": bob.pk,
                "username": "bobby",
                "password": "new password",
            },
        )
        bob = User.objects.get(pk=bob.pk)
        self.assertEqual(bob.username, "bobby", msg="User name not updated")
        self.assertEqual(bob.check_password("new password"), True, msg="Password not updated")

        # Delete
        self.client.post(
            reverse("accounts"),
            {
                "action": "delete",
                "pk": bob.pk,
            },
        )
        self.assertEqual(User.objects.count(), 1, msg="Account was not deleted")

    # Leaving blanks for editing should not alter the respective fields
    def test_edit_blanks(self):
        # Create
        self._login("Admin", "Admin")
        self.client.post(
            reverse("accounts"),
            {
                "action": "create",
                "username": "bob",
                "password": "pw",
                "userEmail": "bob@example.com",
                "firstName": "Bob",
                "lastName": "B",
                "homeAddress": "1 Oak",
                "phoneNumber": "1113337777",
            },
        )
        self.assertEqual(User.objects.count(), 2, msg="Should be 2")

        bob = User.objects.get(username="bob")
        # Edit
        self.client.post(
            reverse("accounts"),
            {
                "action": "edit",
                "pk": bob.pk,
                "username": "",
                "userEmail": "",
                "phoneNumber": "",
                "homeAddress": "",
            },
        )
        bob.refresh_from_db()
        # Everything should remain the same as before
        self.assertEqual(bob.username, "bob", msg="Username was changed")
        self.assertEqual(bob.phoneNumber, 1113337777, msg="Phone number was changed")
        self.assertEqual(bob.homeAddress, "1 Oak", msg="Home Address was changed")
        self.assertEqual(bob.userEmail, "bob@example.com", msg="Email was changed")

    def test_create_blanks(self):
        """
        Account creation should be rejected if the necessary fields are not provided
        First name, last name, email, username, and password are needed
        """
        self._login("Admin", "Admin")
        self.client.post(
            reverse("accounts"),
            {
                "action": "create",
                "username": "bob",
                "password": "",
                "userEmail": "",
                "homeAddress": "",
                "firstName": "",
                "lastName": "",
            },
        )
        self.assertEqual(User.objects.count(), 1, msg="Account was created when it should be rejected")


class SecurityAcceptanceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="Admin",
            password="Admin",
            userEmail="a@uwm.edu",
            firstName="Admin",
            lastName="Admin",
            homeAddress="1 Main",
            accountType=2,
        )
        self.ta = User.objects.create_user(
            username="TA",
            password="TA",
            userEmail="t@uwm.edu",
            firstName="Tim",
            lastName="Assistant",
            homeAddress="2 Main",
            accountType=0,
        )

    def _login(self, usr, pwd):
        ok = self.client.login(username=usr, password=pwd)
        self.assertTrue(ok, f"Login failed for {usr!r}")

    def test_non_admin_sees_no_admin_controls(self):
        """Checks if admin feature buttons are not rendered"""
        self._login("TA", "TA")
        resp = self.client.get(reverse("accounts"))

        self.assertEqual(resp.status_code, 200)  # Successful traversal to accounts page

        self.assertNotContains(resp, "�? Add User")
        self.assertNotContains(resp, "✏�? Edit")
        self.assertNotContains(resp, "Delete")

    def test_non_admin_cannot_create_via_post(self):
        """tests forced post from non_admin"""
        self._login("TA", "TA")
        resp = self.client.post(
            reverse("accounts"),
            {
                "action": "create",
                "username": "hax",
                "password": "pw",
                "userEmail": "h@uwm.edu",
                "firstName": "Hax",
                "lastName": "User",
                "homeAddress": "3 Main",
                "accountType": 0,
            },
        )
        self.assertEqual(resp.status_code, 403)  # Rejected request
        self.assertFalse(User.objects.filter(username="hax").exists())

    def test_admin_can_create_user(self):
        """Ideal route, admin creates user"""
        self._login("Admin", "Admin")
        self.client.post(
            reverse("accounts"),
            {
                "action": "create",
                "username": "newbie",
                "password": "pw",
                "userEmail": "n@uwm.edu",
                "firstName": "New",
                "lastName": "User",
                "homeAddress": "4 Main",
                "accountType": 0,
            },
            follow=True,
        )
        self.assertTrue(User.objects.filter(username="newbie").exists())

    def test_deleting_self_logs_out(self):
        """Deleting own account should force logout"""
        self._login("Admin", "Admin")
        self.client.post(reverse("accounts"), {"action": "delete", "pk": self.admin.pk}, follow=True)

        resp = self.client.get(reverse("accounts"))
        self.assertEqual(resp.status_code, 302)  # Redirect to different page

        # removes part of the url that indicates which page it redirects back to after logging in.
        # in other words, we get the important part of the url
        redirected_to = resp.url.split("?", 1)[0]
        self.assertEqual(redirected_to, reverse("login"))
