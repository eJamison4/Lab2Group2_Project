from django.test import TestCase, Client
from TA_Scheduler_App.models import Course, User

class TestCourseViewAcceptance(TestCase):
    def setUp(self):
        self.client = Client()

        # Admin user
        self.admin_user = User.objects.create(
            username="admin1",
            password="adminpass",
            userEmail="admin@email.com",
            phoneNumber=1234567890,
            firstName="Alice",
            lastName="Admin",
            homeAddress="1 Admin Rd",
            accountType=2
        )

    def test_all_course_features_as_admin(self):
        # Simulate admin login
        session = self.client.session
        session['_auth_user_id'] = self.admin_user.id
        session.save()

        # CREATE course
        self.client.post('/courses/', {
            "action": "create",
            "courseName": "CS 101"
        })
        self.assertEqual(Course.objects.count(), 1, msg="Course should be created")

        course = Course.objects.get(courseName="CS 101")

        # EDIT course
        self.client.post('/courses/', {
            "action": "edit",
            "courseId": course.id,
            "newCourseName": "CS 102"
        })
        course.refresh_from_db()
        self.assertEqual(course.courseName, "CS 102", msg="Course name should be updated")

        # DELETE course
        self.client.post('/courses/', {
            "action": "delete",
            "courseId": course.id,
        })
        self.assertEqual(Course.objects.count(), 0, msg="Course should be deleted")

    def test_course_creation_rejected_for_non_admin(self):
        ta_user = User.objects.create(
            username="ta1",
            password="tapass",
            userEmail="ta@email.com",
            phoneNumber=9876543210,
            firstName="Tim",
            lastName="Assistant",
            homeAddress="2 TA Blvd",
            accountType=0  # TA
        )
        session = self.client.session
        session['_auth_user_id'] = ta_user.id
        session.save()

        response = self.client.post('/courses/', {
            "action": "create",
            "courseName": "CS 202"
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Course.objects.count(), 0, msg="TA should not be able to create a course")

    def test_course_edit_rejected_for_non_admin(self):
        course = Course.objects.create(courseName="CS Unchanged")

        ta_user = User.objects.create(
            username="ta1",
            password="tapass",
            userEmail="ta@email.com",
            phoneNumber=9876543210,
            firstName="Tim",
            lastName="Assistant",
            homeAddress="2 TA Blvd",
            accountType=0
        )
        session = self.client.session
        session['_auth_user_id'] = ta_user.id
        session.save()

        response = self.client.post('/courses/', {
            "action": "edit",
            "courseId": course.id,
            "newCourseName": "Hacked Name"
        })
        self.assertEqual(response.status_code, 403)
        course.refresh_from_db()
        self.assertEqual(course.courseName, "CS Unchanged", msg="Course name should not change")

    def test_edit_course_with_blanks_does_nothing(self):
        # Log in as admin and create course
        session = self.client.session
        session['_auth_user_id'] = self.admin_user.id
        session.save()

        self.client.post('/courses/', {
            "action": "create",
            "courseName": "Original Course"
        })
        course = Course.objects.get(courseName="Original Course")

        # edit with blank name
        self.client.post('/courses/', {
            "action": "edit",
            "courseId": course.id,
            "newCourseName": ""
        })
        course.refresh_from_db()
        self.assertEqual(course.courseName, "Original Course", msg="Blank edit should not change course name")

    def test_prevent_duplicate_course_names(self):
        session = self.client.session
        session['_auth_user_id'] = self.admin_user.id
        session.save()
    
        self.client.post('/courses/', {"action": "create", "courseName": "CS 101"})
        response = self.client.post('/courses/', {"action": "create", "courseName": "CS 101"})

        self.assertEqual(Course.objects.filter(courseName="CS 101").count(), 1)
        self.assertIn(response.status_code, [400, 409])  # depends on your handling

    def test_course_creation_missing_name(self):
        session = self.client.session
        session['_auth_user_id'] = self.admin_user.id
        session.save()

        response = self.client.post('/courses/', {
            "action": "create",
            "courseName": ""
        })
        self.assertEqual(Course.objects.count(), 0)
        self.assertEqual(response.status_code, 400)


