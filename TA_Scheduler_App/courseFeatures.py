from TA_Scheduler_App.models import Lab,Section,Course

class CourseFeatures:

    @staticmethod
    def create_course(self, courseName:str):
        course = Course.objects.create(courseName=courseName)
        course.save()
        return course

    @staticmethod
    def create_section(self, courseForeignKey:Course, sectionData:str):
        section = Section.objects.create(courseForeignKey=courseForeignKey, sectionTime=sectionData)
        section.save()
        return section

    @staticmethod
    def create_lab(self, courseForeignKey:Course, labData:str):
        lab = Lab.objects.create(courseForeignKey=courseForeignKey, labTime=labData)
        lab.save()
        return lab

    @staticmethod
    def delete_course(self, courseKey:int):
        try:
            course = Course.objects.get(pk=courseKey)
            course.delete()
            return True
        except Course.DoesNotExist:
            return False


    @staticmethod
    def delete_section(self, sectionKey:int):
        try:
            section = Section.objects.get(pk=sectionKey)
            section.delete()
            return True
        except Section.DoesNotExist:
            return False

    @staticmethod
    def delete_lab(self, labKey:int):
        try:
            lab = Lab.objects.get(pk=labKey)
            lab.delete()
            return True

        except Lab.DoesNotExist:
            return False

    @staticmethod
    def edit_course(self, courseKey:int, newCourseName:str=""):
        try:
            course = Course.objects.get(pk=courseKey)
        except Course.DoesNotExist:
            return False


        if newCourseName is not '' and newCourseName is not None:
            course.courseName = newCourseName
            course.save()

        return course

    @staticmethod
    def edit_section(self, sectionKey:int, newSectionTime:str=None):
        try:
            section = Section.objects.get(pk=sectionKey)
        except Section.DoesNotExist:
            return False

        if newSectionTime is not None and newSectionTime is not '':
            section.sectionTime = newSectionTime
            section.save()

        return section


    @staticmethod
    def edit_lab(self, labKey:int, newLabTime:str=None):
        try:
            lab = Lab.objects.get(pk=labKey)
        except Lab.DoesNotExist:
            return False

        if newLabTime is not None and newLabTime is not '' :
            lab.labTime = newLabTime
            lab.save()

        return lab

