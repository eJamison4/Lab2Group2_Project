import models

class CourseFeatures:

    @staticmethod
    def create_course(self, courseName):
        course = models.Course.objects.create(name=courseName)
        return course

    @staticmethod
    def create_section(self, courseForeignKey, sectionData):
        section = models.Section.objects.create(courseForeignKey=courseForeignKey, sectionTime=sectionData)
        return section

    @staticmethod
    def create_lab(self, courseForeignKey, labData):
        lab = models.Lab.objects.create(courseForeignKey=courseForeignKey, labTime=labData)
        pass

    @staticmethod
    def delete_course(self, courseKey):
        try:
            course = models.Course.objects.get(key=courseKey)
            course.delete()
            return True
        except models.Course.DoesNotExist:
            return False


    @staticmethod
    def delete_section(self, sectionKey):
        pass

    @staticmethod
    def delete_lab(self, labKey):
        pass

    @staticmethod
    def edit_course(self, courseKey):
        pass

    @staticmethod
    def edit_section(self, sectionKey):
        pass

    @staticmethod
    def edit_lab(self, labKey):
        pass

