from django.test import TestCase
from TA_Scheduler_App.relation_features import teacher_to_TA_features as relationFeatures
from TA_Scheduler_App.models import User, teacherToTA


class MyTestCase(TestCase):

    def test_create(self):
        self.service = relationFeatures()
        teacher = User(userEmail='a',firstName='a',last_name='a',homeAddress='a',accountType=1,username='a')
        teacher.save()
        TA = User(userEmail='b',firstName='b',last_name='b',homeAddress='b',accountType=0,username='b')
        TA.save()
        relation = self.service.create_relation(teacher,TA)
        self.assertEqual(relation.teacherIDF,teacher)
        self.assertEqual(relation.TAIDF,TA)



    def test_multiple(self):
        self.service = relationFeatures()
        teacher = User(userEmail='a',firstName='a',last_name='a',homeAddress='a',accountType=1,username='a')
        teacher.save()
        TA1 = User(userEmail='b',firstName='b',last_name='b',homeAddress='b',accountType=0,username='b')
        TA1.save()
        TA2 = User(userEmail='b',firstName='b',last_name='b',homeAddress='b',accountType=0,username='c')
        TA2.save()
        relation1 = self.service.create_relation(teacher,TA1)
        relation2 = self.service.create_relation(teacher,TA2)

        self.assertEqual(relation1.teacherIDF,teacher)
        self.assertEqual(relation1.TAIDF,TA1)
        self.assertEqual(relation2.teacherIDF, teacher)
        self.assertEqual(relation2.TAIDF, TA2)


    def test_delete(self):
        self.service = relationFeatures()
        teacher = User(userEmail='a',firstName='a',last_name='a',homeAddress='a',accountType=1,username='a')
        teacher.save()
        TA1 = User(userEmail='b',firstName='b',last_name='b',homeAddress='b',accountType=0,username='b')
        TA1.save()
        TA2 = User(userEmail='b',firstName='b',last_name='b',homeAddress='b',accountType=0,username='c')
        TA2.save()
        relation1 = self.service.create_relation(teacher,TA1)
        relation2 = self.service.create_relation(teacher,TA2)
        self.assertEqual(teacherToTA.objects.count(),2)
        self.service.delete_relation(relation1.pk)
        self.assertEqual(teacherToTA.objects.count(),1)
        self.service.delete_relation(relation2.pk)
        self.assertEqual(teacherToTA.objects.count(),0)
        self.assertEqual(self.service.delete_relation(TA1.pk),False)
