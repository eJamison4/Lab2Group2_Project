# tests_acceptance.py
from django.test import TestCase, Client
from TA_Scheduler_App.models import User

class TestAccountView(TestCase):

    def setUp(self):
        self.client = Client()


    def test_all_features(self):
        #Create
        self.client.post('accounts/',{
            "action": "create",
            "username": "bob",
            "password": "pw",
            "userEmail": "bob@example.com",
            "firstName": "Bob",
            "lastName": "B",
            "homeAddress": "1 Oak",
        })
        self.assertEqual(User.objects.count(), 1, msg="Number of users should be 1")

        bob = User.objects.get(username="bob")
        #Edit
        self.client.post('accounts/',{
            "action": "edit",
            "user_id": bob.id,
            "username": "bobby",
        })
        bob.refresh_from_db()
        self.assertEqual(bob.username, "bobby", msg="User name not updated")

        #Delete
        self.client.post('accounts/',{
            "action": "delete",
            "user_id": bob.id,
        })
        self.assertEqual(User.objects.count(), 0 , msg="Account was not deleted")

    #Leaving blanks for editing should not alter the respective fields
    def test_edit_blanks(self):
        # Create
        self.client.post('accounts/', {
            "action": "create",
            "username": "bob",
            "password": "pw",
            "userEmail": "bob@example.com",
            "firstName": "Bob",
            "lastName": "B",
            "homeAddress": "1 Oak",
            "phoneNumber": 1113337777,
        })
        self.assertEqual(User.objects.count(), 1, msg="Should be 1")

        bob = User.objects.get(username="bob")
        # Edit
        self.client.post('accounts/', {
            "action": "edit",
            "user_id": bob.id,
            "username": "",
            "userEmail": "",
            "phoneNumber": None,
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
        self.client.post('accounts/', {
            "action": "create",
            "username": "bob",
            "password": "",
            "userEmail": "",
            "homeAddress": "",
            "firstName": "",
            "lastName": "",
        })

        self.assertEqual(User.objects.count(), 0, msg="Account was created when it should be rejected")

