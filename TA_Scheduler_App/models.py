import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # username = models.CharField(max_length=20)
    # password = models.CharField(max_length=20)

    userEmail = models.EmailField()
    phoneNumber = models.IntegerField(null=True, blank=True)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    homeAddress = models.CharField(max_length=256)
    # optional office hours
    officeHours = models.CharField(max_length=256, null=True, blank=True)
    timeCreated = models.DateTimeField(auto_now_add=True)
    # have admin be 2 teacher 1 and TA 0
    accountType = models.IntegerField(default=2)


class Course(models.Model):
    objects = None
    courseName = models.CharField(max_length=256)
    semester = models.CharField(max_length=256, default='Spring 2025')

    def __str__(self):
        return self.courseName


class Section(models.Model):
    # not sure how to format the times
    # startTime, endTime, daysOfWeek?
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="section_set")
    sectionCode = models.CharField(max_length=20)  # must be exactly sectionCode #why would we need this? just use the PK
    instructor = models.CharField(max_length=256, blank=True)


# no longer in use
# class Lab(models.Model):
#     labTime = models.CharField(max_length=20)
#     courseForeignKey = models.ForeignKey(Course, on_delete=models.CASCADE)


class Assignment(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    sectionID = models.ForeignKey(Section, on_delete=models.CASCADE)
    # labID = models.ForeignKey(Lab, on_delete=models.CASCADE,blank=True,null=True)
    # set to 1 for grading
    graderStatus = models.IntegerField(default=0)


class skills(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.CharField(max_length=256)


class teacherToTA(models.Model):
    teacherIDF = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher")
    TAIDF = models.ForeignKey(User, on_delete=models.CASCADE, related_name="TA")
