from TA_Scheduler_App.models import Section, User, Lab, Assignment

class assignment_features:

    @staticmethod
    def create_assignment(self,inSection,inUser,inLab=None):
        newAssignment = Assignment.objects.create(userID=inUser,sectionID=inSection,labID=inLab)
        newAssignment.save()

        return newAssignment

    @staticmethod
    def delete_assignment(self,assignmentID):
        try:
            assignment = Assignment.objects.get(pk=assignmentID)
            assignment.delete()
            return True
        except Assignment.DoesNotExist:
            return False

    def add_lab(self,inAssignment:Assignment,inLab:Lab):
        userID = inAssignment.userID
        sectionID = inAssignment.sectionID

        newAssignment = Assignment.objects.create(userID=userID,sectionID=sectionID,labID=inLab)

        inAssignment.delete()

        return newAssignment
