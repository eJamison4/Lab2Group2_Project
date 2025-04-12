from django.test import TestCase
from django.db import models

#Takes all functions from AccountFeatures to test
from TA_Scheduler_App.account_features import AccountFeatures
#Imports the User model from the models file.
#This allows manual creation of users without using account_features
from TA_Scheduler_App.models import User



class TestAccountFeatures(TestCase):
    #sets up the service field to AccountFeatures
    def setUp(self):
        self.service = AccountFeatures()

    #tests creation of one account
    def test_account_creation(self):
        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe'}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'], data['lastName'])

        #All data sent is checked if it can be retrieved as intended
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Teach')
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 0)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, 'Doe')

    #tests account creation with the optional phone number provided
    def test_account_creation_with_phone_number(self):
        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe'}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'],
                                        data['lastName'], phone_number= data['phoneNumber'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Teach')
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 1114449999) #This is what is checked
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, 'Doe')

    #tests account creation with the optional account type provided
    def test_account_creation_with_account_type(self):
        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe', 'accountType': 2}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'],
                                        data['lastName'], account_type=data['accountType'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Teach')
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 0)
        self.assertEqual(user.accountType, 2) #This is what is checked
        self.assertEqual(user.lastName, 'Doe')

    #tests account deletion
    def test_account_deletion(self):
        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe'}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'],
                                        data['lastName'], phone_number=data['phoneNumber'])

        self.assertEqual(User.objects.count(), 1) #Should be one
        self.assertEqual(user.username, 'Teach')
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 1114449999)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, 'Doe')

        user.delete()
        self.assertEqual(User.objects.count(), 0) #Should be zero after the user is deleted

    #tests the edit function
    def test_account_edit(self):
        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe'}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'],
                                        data['lastName'], phone_number=data['phoneNumber'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Teach')
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 1114449999)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, 'Doe')

        #Primary key for the user
        user_id = user.pk

        #Primary key is passed to find the account to edit
        user = self.service.edit_account(user_id, username="Edited", phone_number=2223337777)

        #Checks every field again to confirm the right fields are changed
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Edited') #Changed
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 2223337777) #Changed
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, 'Doe')

    #Features two accounts made that tests the count.  Create, delete, and edit functions are also tested.
    def test_with_two_accounts(self):

        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe'}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'],
                                        data['lastName'], phone_number=data['phoneNumber'])
        data2 = {'username': 'Coach', 'password': '123word', 'userEmail': 'example@hotmail.com', 'phoneNumber': 3335550000,
                'firstName': 'Jack', 'lastName': 'Someone'}
        user2 = self.service.create_user(data2['username'], data2['password'], data2['userEmail'], data2['firstName'],
                                        data2['lastName'], phone_number=data2['phoneNumber'], account_type=2)
        #Count should be 2 accounts at this point
        self.assertEqual(User.objects.count(), 2)

        #Field checks for both accounts
        self.assertEqual(user.username, 'Teach')
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 1114449999)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, 'Doe')


        self.assertEqual(user2.username, 'Coach')
        self.assertEqual(user2.password, '123word')
        self.assertEqual(user2.phoneNumber, 3335550000)
        self.assertEqual(user2.accountType, 2)
        self.assertEqual(user2.lastName, 'Someone')

        user_id1 = user.pk

        user = self.service.edit_account(user_id1, username="Edited", phone_number=2223337777)
        self.assertEqual(User.objects.count(), 2) #Count should remain the same
        #fields below should change
        self.assertEqual(user.username, 'Edited')
        self.assertEqual(user.phoneNumber, 2223337777)

        self.service.delete_account(user_id1)

        self.assertEqual(User.objects.count(), 1) #Count should tick down to 1

        user_id2 = user2.pk

        self.service.delete_account(user_id2)

        self.assertEqual(User.objects.count(), 0) #Count should tick down to 0 as we deleted all accounts