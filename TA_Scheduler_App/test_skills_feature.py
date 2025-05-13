# import unittest
from django.test import TestCase
from TA_Scheduler_App.models import User, skills
from TA_Scheduler_App.skills_features import SkillsFeatures


class MyTestCase(TestCase):
    def setUp(self):
        self.service = SkillsFeatures()

    def testSkillCreate(self):
        self.service = SkillsFeatures()
        user = User(userEmail="", firstName="", last_name="", homeAddress="", accountType=0)
        user.save()
        skill = self.service.create_skill(inUser=user, inSkill="can play yugioh")
        self.assertEqual(user, skill.userID)
        self.assertEqual(skill.skill, "can play yugioh")

    def testSkillUpdate(self):
        self.service = SkillsFeatures()
        user = User(userEmail="", firstName="", last_name="", homeAddress="", accountType=0)
        user.save()
        skill = self.service.create_skill(inUser=user, inSkill="can play yugioh")
        skill = self.service.edit_skill(skill, "can play magic")
        self.assertEqual(skill.skill, "can play magic")

    def testSkillDelete(self):
        self.service = SkillsFeatures()
        user = User(userEmail="", firstName="", last_name="", homeAddress="", accountType=0)
        user.save()
        skill = self.service.create_skill(inUser=user, inSkill="can play yugioh")
        self.assertEqual(skills.objects.count(), 1)
        skill = self.service.delete_skill(skill)
        self.assertEqual(skills.objects.count(), 0)
