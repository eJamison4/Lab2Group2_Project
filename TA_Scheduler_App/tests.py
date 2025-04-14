from django.test import TestCase
from django.db import models
from courseFeatures import CourseFeatures
from models import Section, Course, Lab

# Create your tests here.

class testCourseFeatures(TestCase):

    def setUp(self):
        self.service = CourseFeatures()

    def testCourseCreation(self):

        pass

    def testSectionCreation(self):
        pass

    def testLabCreation(self):
        pass

    def testCourseDelete(self):
        pass

    def testSectionDelete(self):
        pass

    def testLabDelete(self):
        pass

    def testCourseUpdate(self):
        pass

    def testSectionUpdate(self):
        pass

    def testLabUpdate(self):
        pass

    pass