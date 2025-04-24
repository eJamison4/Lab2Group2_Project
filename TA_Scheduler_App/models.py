import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    #username = models.CharField(max_length=20)
    #password = models.CharField(max_length=20)

    userEmail = models.EmailField()
    phoneNumber = models.IntegerField(null = True, blank = True)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    homeAddress = models.CharField(max_length=20)
    #optional office hours
    officeHours = models.CharField(max_length=20, null=True, blank=True)
    timeCreated = models.DateTimeField(auto_now_add=True)
    #have admin be 2 teacher 1 and TA 0
    accountType = models.IntegerField(default=0)


class Course(models.Model):
    courseName = models.CharField(max_length=20)


class Section(models.Model):
    #not sure how to format the times
    # startTime, endTime, daysOfWeek?
    sectionTime = models.CharField(max_length=20)
    courseForeignKey = models.ForeignKey(Course, on_delete=models.CASCADE)

class Lab(models.Model):
    labTime = models.CharField(max_length=20)
    courseForeignKey = models.ForeignKey(Course, on_delete=models.CASCADE)

class Assignment(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    sectionID = models.ForeignKey(Section, on_delete=models.CASCADE)
    labID = models.ForeignKey(Lab, on_delete=models.CASCADE,blank=True,null=True)
    #set to 1 for grading
    graderStatus = models.IntegerField(default=0)