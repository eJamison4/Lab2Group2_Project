from django.test import TestCase
from django.db import models

from TA_Scheduler_App.account_features import AccountFeatures
from TA_Scheduler_App.models import User



# Create your tests here.
class TestAccountFeatures(TestCase):
    def setUp(self):
        self.service = AccountFeatures()

    def test_account_creation(self):
        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe'}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'], data['lastName'])

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Teach')
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 0)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, 'Doe')

    def test_account_creation_with_phone_number(self):
        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe'}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'],
                                        data['lastName'], phoneNumber= data['phoneNumber'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Teach')
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 1114449999)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, 'Doe')
    def test_account_creation_with_email(self):
        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe', 'accountType': 2}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'],
                                        data['lastName'], accountType=data['accountType'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Teach')
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 0)
        self.assertEqual(user.accountType, 2)
        self.assertEqual(user.lastName, 'Doe')

    def test_account_deletion(self):
        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe'}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'],
                                        data['lastName'], phoneNumber=data['phoneNumber'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Teach')
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 1114449999)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, 'Doe')

        user.delete()
        self.assertEqual(User.objects.count(), 0)

    def test_account_edit(self):
        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe'}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'],
                                        data['lastName'], phoneNumber=data['phoneNumber'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Teach')
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 1114449999)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, 'Doe')

        userID = user.pk

        user = self.service.edit_account(userID, username="Edited", phoneNumber=2223337777)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Edited') #Changed
        self.assertEqual(user.password, 'pass123')
        self.assertEqual(user.phoneNumber, 2223337777) #Changed
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, 'Doe')

    def test_with_two_accounts(self):
        data = {'username': 'Teach', 'password': 'pass123', 'userEmail': 'example@email.com', 'phoneNumber': 1114449999,
                'firstName': 'John', 'lastName': 'Doe'}
        user = self.service.create_user(data['username'], data['password'], data['userEmail'], data['firstName'],
                                        data['lastName'], phoneNumber=data['phoneNumber'])
        data2 = {'username': 'Coach', 'password': '123word', 'userEmail': 'example@hotmail.com', 'phoneNumber': 3335550000,
                'firstName': 'Jack', 'lastName': 'Someone'}
        user2 = self.service.create_user(data2['username'], data2['password'], data2['userEmail'], data2['firstName'],
                                        data2['lastName'], phoneNumber=data2['phoneNumber'], accountType=2)

        self.assertEqual(User.objects.count(), 2)
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

        user.delete()

        self.assertEqual(User.objects.count(), 1)

        user2.delete()

        self.assertEqual(User.objects.count(), 0)