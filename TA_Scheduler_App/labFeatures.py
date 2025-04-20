from TA_Scheduler_App.models import Lab

class LabFeatures:

    @staticmethod
    def create_lab(self, course_id: int, lab_time: str):
        new_lab = Lab.objects.create(courseForeignKey_id=course_id,labTime=lab_time)
        return new_lab

    @staticmethod
    def delete_lab(self, lab_id: int) -> bool:
        try:
            Lab.objects.get(pk=lab_id).delete()
            return True
        except Lab.DoesNotExist:
            return False

    @staticmethod
    def update_lab(self, lab_id: int, lab_time: str = None, course_id: int = None):
        lab = Lab.objects.get(pk=lab_id)
        if lab_time is not None:
            lab.labTime = lab_time
        if course_id is not None:
            lab.courseForeignKey_id = course_id
        lab.save()
        return lab
