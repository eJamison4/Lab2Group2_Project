# Imports the TestCase framework.  Allows each test case to act isolated from each other.
from django.test import TestCase
from TA_Scheduler_App.models import Section, Course, User
from TA_Scheduler_App.courseFeatures import CourseFeatures
from TA_Scheduler_App.account_features import AccountFeatures

# Create your tests here.


class testCourseFeatures(TestCase):

    def setUp(self):
        self.service = CourseFeatures()

    def testCourseCreation(self):
        course = self.service.create_course(courseName="yugioh class")
        self.assertEqual(course.courseName, "yugioh class")
        self.assertEqual(Course.objects.count(), 1)

    def testSectionCreation(self):
        course = self.service.create_course(courseName="yugioh class")

        section = self.service.create_section(course, "time to duel")

        self.assertEqual(section.sectionCode, "time to duel")
        self.assertEqual(section.course.courseName, "yugioh class")
        self.assertEqual(Section.objects.count(), 1)

    # def testLabCreation(self):
    #     course = self.service.create_course(self, courseName="yugioh class")
    #
    #     lab = self.service.create_lab(self, course, "time to duel")
    #
    #     self.assertEqual(lab.labTime, "time to duel")
    #     self.assertEqual(lab.courseForeignKey.courseName, "yugioh class")
    #     self.assertEqual(Lab.objects.count(), 1)

    def testCourseDelete(self):
        course = self.service.create_course(courseName="yugioh class")

        self.assertEqual(Course.objects.count(), 1)

        self.service.delete_course(courseKey=course.pk)

        self.assertEqual(Course.objects.count(), 0)

    def testSectionDelete(self):
        course = self.service.create_course(courseName="yugioh class")

        section = self.service.create_section(course, "time to duel")

        self.assertEqual(Section.objects.count(), 1)

        self.service.delete_section(sectionKey=section.pk)

        self.assertEqual(Section.objects.count(), 0)

    # def testLabDelete(self):
    #     course = self.service.create_course(self, courseName="yugioh class")
    #
    #     lab = self.service.create_lab(self, course, "time to duel")
    #
    #     self.assertEqual(Lab.objects.count(), 1)
    #
    #     self.service.delete_lab(self, labKey=lab.pk)
    #
    #     self.assertEqual(Lab.objects.count(), 0)

    def testCourseUpdateNoArgument(self):
        course = self.service.create_course(courseName="yugioh class")
        course = self.service.edit_course(courseKey=course.pk)

        self.assertNotEqual(course.courseName, "")

    def testCourseUpdate(self):
        course = self.service.create_course(courseName="yugioh class")

        course = self.service.edit_course(courseKey=course.pk, newCourseName="MTG class")

        self.assertEqual(course.courseName, "MTG class")

    def testSectionUpdate(self):
        course = self.service.create_course(courseName="yugioh class")
        section = self.service.create_section(course, "time to duel")

        section = self.service.edit_section(sectionKey=section.pk, newSectionTime="time to MTG")

        self.assertEqual(section.sectionTime, "time to MTG")

    def testSectionUpdateNoArgument(self):
        course = self.service.create_course(courseName="yugioh class")
        section = self.service.create_section(course, "time to duel")

        section = self.service.edit_section(sectionKey=section.pk)

        self.assertNotEqual(section.sectionCode, "")

    # def testLabUpdate(self):
    #     course = self.service.create_course(self, courseName="yugioh class")
    #     lab = self.service.create_lab(self, course, "time to duel")
    #     lab = self.service.edit_lab(self, labKey=lab.pk, newLabTime="time to MTG")
    #     self.assertEqual(lab.labTime, "time to MTG")
    #
    # def testLabUpdateNoArgument(self):
    #     course = self.service.create_course(self, courseName="yugioh class")
    #     lab = self.service.create_lab(self, course, "time to duel")
    #
    #     lab = self.service.edit_lab(self, labKey=lab.pk)
    #
    #     self.assertNotEqual(lab.labTime, "")


class TestAccountFeatures(TestCase):
    # sets up the service field to AccountFeatures

    def setUp(self):
        self.service = AccountFeatures()

    # tests creation of one account
    def test_account_creation(self):
        data = {
            "username": "Teach",
            "password": "pass123",
            "userEmail": "example@email.com",
            "phoneNumber": 1114449999,
            "firstName": "John",
            "lastName": "Doe",
            "homeAddress": "123 Main St",
        }
        user = self.service.create_user(
            data["username"],
            data["password"],
            data["userEmail"],
            data["firstName"],
            data["lastName"],
            data["homeAddress"],
        )

        # All data sent is checked if it can be retrieved as intended
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, "Teach")
        self.assertEqual(user.check_password("pass123"), True)
        self.assertEqual(user.phoneNumber, 0)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, "Doe")
        self.assertEqual(user.homeAddress, "123 Main St")

    # tests account creation with the optional phone number provided
    def test_account_creation_with_phone_number(self):
        data = {
            "username": "Teach",
            "password": "pass123",
            "userEmail": "example@email.com",
            "phoneNumber": 1114449999,
            "firstName": "John",
            "lastName": "Doe",
            "homeAddress": "123 Main St",
        }
        user = self.service.create_user(
            data["username"],
            data["password"],
            data["userEmail"],
            data["firstName"],
            data["lastName"],
            data["homeAddress"],
            phone_number=data["phoneNumber"],
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, "Teach")
        self.assertEqual(user.check_password("pass123"), True)
        self.assertEqual(user.phoneNumber, 1114449999)  # This is what is checked
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, "Doe")
        self.assertEqual(user.homeAddress, "123 Main St")

    # tests account creation with the optional account type provided
    def test_account_creation_with_account_type(self):
        data = {
            "username": "Teach",
            "password": "pass123",
            "userEmail": "example@email.com",
            "phoneNumber": 1114449999,
            "firstName": "John",
            "lastName": "Doe",
            "accountType": 2,
            "homeAddress": "123 Main St",
        }
        user = self.service.create_user(
            data["username"],
            data["password"],
            data["userEmail"],
            data["firstName"],
            data["lastName"],
            data["homeAddress"],
            account_type=data["accountType"],
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, "Teach")
        self.assertEqual(user.check_password("pass123"), True)
        self.assertEqual(user.phoneNumber, 0)
        self.assertEqual(user.accountType, 2)  # This is what is checked
        self.assertEqual(user.lastName, "Doe")
        self.assertEqual(user.homeAddress, "123 Main St")

    # tests account deletion
    def test_account_deletion(self):
        data = {
            "username": "Teach",
            "password": "pass123",
            "userEmail": "example@email.com",
            "phoneNumber": 1114449999,
            "firstName": "John",
            "lastName": "Doe",
            "homeAddress": "123 Main St",
        }
        user = self.service.create_user(
            data["username"],
            data["password"],
            data["userEmail"],
            data["firstName"],
            data["lastName"],
            data["homeAddress"],
            phone_number=data["phoneNumber"],
        )

        self.assertEqual(User.objects.count(), 1)  # Should be one
        self.assertEqual(user.username, "Teach")
        self.assertEqual(user.check_password("pass123"), True)
        self.assertEqual(user.phoneNumber, 1114449999)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, "Doe")
        self.assertEqual(user.homeAddress, "123 Main St")

        user.delete()
        self.assertEqual(User.objects.count(), 0)  # Should be zero after the user is deleted

    # tests the edit function
    def test_account_edit(self):
        data = {
            "username": "Teach",
            "password": "pass123",
            "userEmail": "example@email.com",
            "phoneNumber": 1114449999,
            "firstName": "John",
            "lastName": "Doe",
            "homeAddress": "123 Main St",
        }
        user = self.service.create_user(
            data["username"],
            data["password"],
            data["userEmail"],
            data["firstName"],
            data["lastName"],
            data["homeAddress"],
            phone_number=data["phoneNumber"],
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, "Teach")
        self.assertEqual(user.check_password("pass123"), True)
        self.assertEqual(user.phoneNumber, 1114449999)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, "Doe")
        self.assertEqual(user.homeAddress, "123 Main St")

        # Primary key for the user
        user_id = user.pk

        # Primary key is passed to find the account to edit
        user_id = self.service.edit_account(
            user_id, username="Edited", phone_number=2223337777, home_address="fake address"
        )

        user = User.objects.get(pk=user_id)

        # Checks every field again to confirm the right fields are changed
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, "Edited")  # Changed
        self.assertEqual(user.check_password("pass123"), True)
        self.assertEqual(user.phoneNumber, 2223337777)  # Changed
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, "Doe")
        self.assertEqual(user.homeAddress, "fake address")  # Changed

    # Features two accounts made that tests the count.  Create, delete, and edit functions are also tested.
    def test_with_two_accounts(self):

        data = {
            "username": "Teach",
            "password": "pass123",
            "userEmail": "example@email.com",
            "phoneNumber": 1114449999,
            "firstName": "John",
            "lastName": "Doe",
            "homeAddress": "123 Main St",
        }
        user = self.service.create_user(
            data["username"],
            data["password"],
            data["userEmail"],
            data["firstName"],
            data["lastName"],
            data["homeAddress"],
            phone_number=data["phoneNumber"],
        )
        data2 = {
            "username": "Coach",
            "password": "123word",
            "userEmail": "example@hotmail.com",
            "phoneNumber": 3335550000,
            "firstName": "Jack",
            "lastName": "Someone",
            "homeAddress": "789 Test Dr",
        }
        user2 = self.service.create_user(
            data2["username"],
            data2["password"],
            data2["userEmail"],
            data2["firstName"],
            data2["lastName"],
            data2["homeAddress"],
            phone_number=data2["phoneNumber"],
            account_type=2,
        )
        # Count should be 2 accounts at this point
        self.assertEqual(User.objects.count(), 2)

        # Field checks for both accounts
        self.assertEqual(user.username, "Teach")
        self.assertEqual(user.check_password("pass123"), True)
        self.assertEqual(user.phoneNumber, 1114449999)
        self.assertEqual(user.accountType, 0)
        self.assertEqual(user.lastName, "Doe")
        self.assertEqual(user.homeAddress, "123 Main St")

        self.assertEqual(user2.username, "Coach")
        self.assertEqual(user2.check_password("123word"), True)
        self.assertEqual(user2.phoneNumber, 3335550000)
        self.assertEqual(user2.accountType, 2)
        self.assertEqual(user2.lastName, "Someone")
        self.assertEqual(user2.homeAddress, "789 Test Dr")

        user_id1 = user.pk

        user_id1 = self.service.edit_account(user_id1, username="Edited", phone_number=2223337777)

        user = User.objects.get(pk=user_id1)

        self.assertEqual(User.objects.count(), 2)  # Count should remain the same
        # fields below should change
        self.assertEqual(user.username, "Edited")
        self.assertEqual(user.phoneNumber, 2223337777)

        self.service.delete_account(user_id1)

        self.assertEqual(User.objects.count(), 1)  # Count should tick down to 1

        # Primary key for the second user
        user_id2 = user2.pk

        self.service.delete_account(user_id2)

        self.assertEqual(User.objects.count(), 0)  # Count should tick down to 0 as we deleted all accounts
