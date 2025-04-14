import models

class CourseFeatures:

    @staticmethod
    def create_course(self, courseName):
        course = models.Course.objects.create(name=courseName)
        course.save()
        return course

    @staticmethod
    def create_section(self, courseForeignKey, sectionData):
        section = models.Section.objects.create(courseForeignKey=courseForeignKey, sectionTime=sectionData)
        section.save()
        return section

    @staticmethod
    def create_lab(self, courseForeignKey, labData):
        lab = models.Lab.objects.create(courseForeignKey=courseForeignKey, labTime=labData)
        lab.save()
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
        try:
            section = models.Section.objects.get(key=sectionKey)
            section.delete()
            return True
        except models.Section.DoesNotExist:
            return False

    @staticmethod
    def delete_lab(self, labKey):
        try:
            lab = models.Lab.objects.get(key=labKey)
            lab.delete()
            return True

        except models.Lab.DoesNotExist:
            return False

    @staticmethod
    def edit_course(self, courseKey):
        pass

    @staticmethod
    def edit_section(self, sectionKey):
        pass

    @staticmethod
    def edit_lab(self, labKey):
        pass

