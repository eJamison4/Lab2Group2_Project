from logging import exception

from TA_Scheduler_App.models import User, skills

class SkillsFeatures:
    @staticmethod
    def create_skill(inUser:User,inSkill:str):
        if inUser is None:
            raise exception("null user")
        if not isinstance(inUser, User):
            raise exception("invalid user")

        if inSkill is None or inSkill == '':
            raise exception("null skill")
        if not isinstance(inSkill, str):
            raise exception("invalid skill")

        newSkill = skills.objects.create(userID = inUser, skill = inSkill)
        newSkill.save()
        return newSkill


    @staticmethod
    def delete_skill(inSkill: skills):
        if inSkill is None:
            return False
        if not isinstance(inSkill, skills):
            raise exception("invalid inSkill")
        inSkill.delete()
        return True

    @staticmethod
    def edit_skill(editSkill:skills,inSkill:str):
        if editSkill is None:
            raise exception("no skill")
        if not isinstance(editSkill, skills):
            raise exception("invalid editSkill")

        if inSkill is None or inSkill == '':
            return False
        if not isinstance(inSkill, str):
            raise exception("invalid skill")

        editSkill.skill = inSkill
        editSkill.save()
        return editSkill
