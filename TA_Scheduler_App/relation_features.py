from TA_Scheduler_App.models import User, teacherToTA


class teacher_to_TA_features:
    @staticmethod
    def create_relation(inTeacher: User, inTA: User):
        if inTeacher is None or inTA is None:
            raise Exception("problem with parameters")

        if inTeacher.accountType < 1 or inTA.accountType > 0:
            raise Exception("TA and/or teacher in wrong spots")

        newRelation = teacherToTA.objects.create(teacherIDF=inTeacher, TAIDF=inTA)
        newRelation.save()
        return newRelation

    @staticmethod
    def delete_relation(inRelationID: int):
        try:
            relation = teacherToTA.objects.get(pk=inRelationID)
            relation.delete()
            return True
        except teacherToTA.DoesNotExist:
            return False
