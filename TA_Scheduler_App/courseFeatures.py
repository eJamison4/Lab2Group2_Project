from TA_Scheduler_App.models import Lab,Section,Course

class CourseFeatures:

    @staticmethod
    def create_course(self, courseName):
        course = Course.objects.create(name=courseName)
        course.save()
        return course

    @staticmethod
    def create_section(self, courseForeignKey, sectionData):
        section = Section.objects.create(courseForeignKey=courseForeignKey, sectionTime=sectionData)
        section.save()
        return section

    @staticmethod
    def create_lab(self, courseForeignKey, labData):
        lab = Lab.objects.create(courseForeignKey=courseForeignKey, labTime=labData)
        lab.save()
        pass

    @staticmethod
    def delete_course(self, courseKey):
        try:
            course = Course.objects.get(key=courseKey)
            course.delete()
            return True
        except Course.DoesNotExist:
            return False


    @staticmethod
    def delete_section(self, sectionKey):
        try:
            section = Section.objects.get(key=sectionKey)
            section.delete()
            return True
        except Section.DoesNotExist:
            return False

    @staticmethod
    def delete_lab(self, labKey):
        try:
            lab = Lab.objects.get(key=labKey)
            lab.delete()
            return True

        except Lab.DoesNotExist:
            return False

    @staticmethod
    def edit_course(self, courseKey, newCourseName=None):
        try:
            course = Course.objects.get(key=courseKey)
        except Course.DoesNotExist:
            return False

        if newCourseName is not None:
            course.courseName = newCourseName
            course.save()
            return True
        return False

    @staticmethod
    def edit_section(self, sectionKey, newSectionTime=None):
        try:
            section = Section.objects.get(key=sectionKey)
        except Section.DoesNotExist:
            return False

        if newSectionTime is not None:
            section.sectionTime = newSectionTime
            section.save()
            return True

        return False


    @staticmethod
    def edit_lab(self, labKey, newLabTime=None):
        try:
            lab = Lab.objects.get(key=labKey)
        except Lab.DoesNotExist:
            return False

        if newLabTime is not None:
            lab.labTime = newLabTime
            lab.save()
            return True

        return False

