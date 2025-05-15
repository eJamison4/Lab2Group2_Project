from TA_Scheduler_App.models import Section, Course


class CourseFeatures:
    """
    Model snapshot (May 01 2025)
    @Zach Fornero: Put this here so I didn't have to switch files all the time figured it would be helpful
        class Course(models.Model):
            courseName = models.CharField(max_length=256)
            semester   = models.CharField(max_length=256)

        class Section(models.Model):
            course       = models.ForeignKey(Course, on_delete=models.CASCADE,
                                             related_name="section_set")
            sectionCode  = models.CharField(max_length=20)
            instructor   = models.CharField(max_length=256, blank=True)
    """
    @staticmethod
    def create_course(courseName: str, semester: str):
        if not courseName:
            raise Exception("no course name provided")
        if not semester:
            raise Exception("no semester provided")

        a: Course = None
        try:
            a = Course.objects.get(courseName=courseName, semester=semester)
        except Course.MultipleObjectsReturned:
            raise Exception("something is really wrong")
        except Course.DoesNotExist:
            pass

        if a is not None:
            return False

        course = Course.objects.create(courseName=courseName, semester=semester)
        course.save()
        return course

    @staticmethod
    def create_section(courseForeignKey: Course, sectionCode="newSection", instructor=""):
        if not (courseForeignKey and sectionCode):
            return False
        if not isinstance(courseForeignKey, Course):
            raise Exception("not a course")

        section = Section.objects.create(course=courseForeignKey, sectionCode=sectionCode, instructor=instructor)
        section.save()

        return section

    @staticmethod
    def delete_course(courseKey: int):
        try:
            course = Course.objects.get(pk=courseKey)
            course.delete()
            return True
        except Course.DoesNotExist:
            return False

    @staticmethod
    def delete_section(sectionKey: int):
        if not isinstance(sectionKey, int):
            return False
        try:
            section = Section.objects.get(pk=sectionKey)
            section.delete()
            return True
        except Section.DoesNotExist:
            return False

    @staticmethod
    def edit_course(courseKey: int, newCourseName="", newSemester=""):
        if (
            not isinstance(courseKey, int)
            or not isinstance(newCourseName, str)
            or not isinstance(newSemester, str)
        ):
            return False
        try:
            course = Course.objects.get(pk=courseKey)
        except Course.DoesNotExist:
            return False
        if newCourseName.strip():
            course.courseName = newCourseName.strip()
            course.save()
        if newSemester.strip():
            course.semester = newSemester.strip()
            course.save()

        return course

    @staticmethod
    def edit_section(sectionKey: int, newSectionCode="", newInstructor=""):
        if not isinstance(sectionKey, int):
            return False
        try:
            section = Section.objects.get(pk=sectionKey)
        except Section.DoesNotExist:
            return False

        if newSectionCode.strip():
            section.sectionCode = newSectionCode.strip()
            section.save()
        if newInstructor.strip():  # allow blank strings
            section.instructor = newInstructor
            section.save()
        return section
