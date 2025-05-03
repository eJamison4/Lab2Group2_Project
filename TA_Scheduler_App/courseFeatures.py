from TA_Scheduler_App.models import Section,Course

class CourseFeatures:

    @staticmethod
    def create_course(courseName:str):
        if courseName is None or courseName is '':
            raise Exception('no')

        a = None
        try:
            a = Course.objects.get(courseName=courseName)
        except Course.MultipleObjectsReturned:
            raise Exception("something is really wrong")
        except Course.DoesNotExist:
            pass

        if a is not None:
            return False

        course = Course.objects.create(courseName=courseName)
        course.save()
        return course

    @staticmethod
    def create_section(courseForeignKey:Course, sectionData:str=None):
        if courseForeignKey is None:
            return False

        if sectionData is None:
            return False

        if not isinstance(courseForeignKey,Course):
            raise Exception('not a course')

        section = Section.objects.create(course=courseForeignKey, sectionCode=sectionData)
        section.save()
        return section

    # @staticmethod
    # def create_lab(courseForeignKey:Course, labData:str):
    #     lab = Lab.objects.create(courseForeignKey=courseForeignKey, labTime=labData)
    #     lab.save()
    #     return lab

    @staticmethod
    def delete_course(courseKey:int):
        try:
            course = Course.objects.get(pk=courseKey)
            course.delete()
            return True
        except Course.DoesNotExist:
            return False


    @staticmethod
    def delete_section(sectionKey:int):
        if not isinstance(sectionKey,int):
            return False
        try:
            section = Section.objects.get(pk=sectionKey)
            section.delete()
            return True
        except Section.DoesNotExist:
            return False
    #
    # @staticmethod
    # def delete_lab(labKey:int):
    #     try:
    #         lab = Lab.objects.get(pk=labKey)
    #         lab.delete()
    #         return True
    #
    #     except Lab.DoesNotExist:
    #         return False

    @staticmethod
    def edit_course(courseKey:int, newCourseName:str=""):
        if not isinstance(courseKey,int) or not isinstance(newCourseName,str):
            return False

        try:
            course = Course.objects.get(pk=courseKey)
        except Course.DoesNotExist:
            return False


        if newCourseName is not '' and newCourseName is not None:
            course.courseName = newCourseName
            course.save()

        return course

    @staticmethod
    def edit_section(sectionKey:int, newSectionTime:str=None):
        if not isinstance(sectionKey,int):
            return False

        try:
            section = Section.objects.get(pk=sectionKey)
        except Section.DoesNotExist:
            return False

        if newSectionTime is not None and newSectionTime is not '':
            section.sectionTime = newSectionTime
            section.save()

        return section

    #
    # @staticmethod
    # def edit_lab(labKey:int, newLabTime:str=None):
    #     try:
    #         lab = Lab.objects.get(pk=labKey)
    #     except Lab.DoesNotExist:
    #         return False
    #
    #     if newLabTime is not None and newLabTime is not '' :
    #         lab.labTime = newLabTime
    #         lab.save()
    #
    #     return lab

