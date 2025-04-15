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

        section = self.service.create_section(self,course,'time to duel')

        self.assertEqual(section.sectionTime, 'time to duel')
        self.assertEqual(section.courseForeignKey.courseName, 'yugioh class')
        self.assertEqual(Section.objects.count(), 1)

    def testLabCreation(self):
        course = self.service.create_course(self,courseName="yugioh class")

        lab = self.service.create_lab(self,course,'time to duel')

        self.assertEqual(lab.labTime, 'time to duel')
        self.assertEqual(lab.courseForeignKey.courseName, 'yugioh class')
        self.assertEqual(Lab.objects.count(), 1)


    def testCourseDelete(self):
        course = self.service.create_course(self,courseName="yugioh class")

        self.assertEqual(Course.objects.count(), 1)

        self.service.delete_course(self,courseKey=course.pk)

        self.assertEqual(Course.objects.count(), 0)

    def testSectionDelete(self):
        course = self.service.create_course(self,courseName="yugioh class")

        section = self.service.create_section(self,course,'time to duel')

        self.assertEqual(Section.objects.count(), 1)

        self.service.delete_section(self,sectionKey=section.pk)

        self.assertEqual(Section.objects.count(), 0)


    def testLabDelete(self):
        course = self.service.create_course(self,courseName="yugioh class")

        lab = self.service.create_lab(self,course,'time to duel')

        self.assertEqual(Lab.objects.count(), 1)

        self.service.delete_lab(self,labKey=lab.pk)

        self.assertEqual(Lab.objects.count(), 0)

    def testCourseUpdateNoArgument(self):
        course = self.service.create_course(self,courseName="yugioh class")

        self.assertIsNone(self.service.edit_course(self,courseKey=course.pk))

    def testCourseUpdate(self):
        course = self.service.create_course(self,courseName="yugioh class")

        course = self.service.edit_course(self,courseKey=course.pk, newCourseName='MTG class')

        self.assertEqual(course.courseName, 'MTG class')

    def testSectionUpdate(self):
        pass

    def testLabUpdate(self):
        pass

    pass