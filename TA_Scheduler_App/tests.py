from django.test import TestCase
from TA_Scheduler_App.models import Section, Course, Lab
from TA_Scheduler_App.courseFeatures import CourseFeatures

# Create your tests here.

class testCourseFeatures(TestCase):

    def setUp(self):
        self.service = CourseFeatures()

    def testCourseCreation(self):
        course = self.service.create_course(self,courseName="yugioh class")

        self.assertEqual(course.courseName, 'yugioh class')
        self.assertEqual(Course.objects.count(), 1)


    def testSectionCreation(self):
        course = self.service.create_course(self,courseName="yugioh class")

        section = self.service.create_section(self,course.pk,'time to duel')
        self.assertEqual(section.sectionTime, 'time to duel')
        self.assertEqual(Section.objects.count(), 1)

    def testLabCreation(self):
        lab = self.service.create_lab('time to duel')
        self.assertEqual(lab.labTime, 'time to duel')
        self.assertEqual(Lab.objects.count(), 1)
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