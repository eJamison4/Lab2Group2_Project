# tests_acceptance.py
from django.test import TestCase, Client
from django.urls import reverse
from TA_Scheduler_App.models import User

class TestAccountView(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='Admin', email='', password='Admin')


    def test_all_features(self):
        #Create
        self.client.login(username='Admin', password='Admin')
        response = self.client.post(reverse('accounts'), {"action": "create",
            "username": "bob",
            "password": "pw",
            "userEmail": "bob@example.com",
            "firstName": "Bob",
            "lastName": "B",
            "homeAddress": "1 Oak",})

        self.assertEqual(User.objects.count(), 2, msg="Number of users should be 2")
        self.assertRedirects(response, reverse('accounts'))

        bob = User.objects.get(username="bob", userEmail="bob@example.com")
        #Edit
        response = self.client.post(reverse('accounts'),{
            "action": "edit",
            "pk": bob.pk,
            "username": "bobby",
        })
        bob = User.objects.get(pk=bob.pk)
        self.assertEqual(bob.username, "bobby", msg="User name not updated")

        #Delete
        self.client.post(reverse('accounts'), {
            "action": "delete",
            "pk": bob.pk,
        })
        self.assertEqual(User.objects.count(), 1 , msg="Account was not deleted")

    #Leaving blanks for editing should not alter the respective fields
    def test_edit_blanks(self):
        # Create
        self.client.post(reverse('accounts'), {
            "action": "create",
            "username": "bob",
            "password": "pw",
            "userEmail": "bob@example.com",
            "firstName": "Bob",
            "lastName": "B",
            "homeAddress": "1 Oak",
            "phoneNumber": "1113337777",
        })
        self.assertEqual(User.objects.count(), 2, msg="Should be 2")

        bob = User.objects.get(username="bob")
        # Edit
        self.client.post(reverse('accounts'), {
            "action": "edit",
            "pk": bob.pk,
            "username": "",
            "userEmail": "",
            "phoneNumber": "",
            "homeAddress": "",
        })
        bob.refresh_from_db()
        #Everything should remain the same as before
        self.assertEqual(bob.username, "bob", msg="Username was changed")
        self.assertEqual(bob.phoneNumber, 1113337777, msg="Phone number was changed")
        self.assertEqual(bob.homeAddress, "1 Oak", msg="Home Address was changed")
        self.assertEqual(bob.userEmail, "bob@example.com", msg="Email was changed")

    #Account creation should be rejected if the necessary fields are not provided
    #First name, last name, email, home address, username, and password are needed
    def test_create_blanks(self):
        self.client.post(reverse('accounts'), {
            "action": "create",
            "username": "bob",
            "password": "",
            "userEmail": "",
            "homeAddress": "",
            "firstName": "",
            "lastName": "",
        })

        self.assertEqual(User.objects.count(), 1, msg="Account was created when it should be rejected")

