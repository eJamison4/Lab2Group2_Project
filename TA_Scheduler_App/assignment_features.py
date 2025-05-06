from TA_Scheduler_App.models import Section, User, Assignment

class assignment_features:

    @staticmethod
    def create_assignment(self,inSection:Section,inUser:User):
        newAssignment = Assignment.objects.create(userID=inUser,sectionID=inSection)
        newAssignment.save()

        return newAssignment

    @staticmethod
    def delete_assignment(self,assignmentID:int):
        try:
            assignment = Assignment.objects.get(pk=assignmentID)
            assignment.delete()
            return True
        except Assignment.DoesNotExist:
            return False

    # def add_lab(self,inAssignment:Assignment):
    #     userID = inAssignment.userID
    #     sectionID = inAssignment.sectionID
    #
    #     newAssignment = Assignment.objects.create(userID=userID,sectionID=sectionID)
    #
    #     inAssignment.delete()
    #
    #     return newAssignment
