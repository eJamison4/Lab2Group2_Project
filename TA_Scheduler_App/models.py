from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    userEmail = models.EmailField()
    phoneNumber = models.IntegerField()
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)

    timeCreated = models.DateTimeField(auto_now_add=True)
    accountType = models.IntegerField(default=0)


class Course(models.Model):
    courseName = models.CharField(max_length=20)


class Section(models.Model):
    sectionTime = models.CharField(max_length=20)
    courseForeignKey = models.ForeignKey(Course, on_delete=models.CASCADE)

class lab(models.Model):
    labTime = models.CharField(max_length=20)
    courseForeignKey = models.ForeignKey(Course, on_delete=models.CASCADE)

class assignment(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    sectionID = models.ForeignKey(Section, on_delete=models.CASCADE)
    labID = models.ForeignKey(lab, on_delete=models.CASCADE,blank=True,null=True)
    graderStatus = models.IntegerField(default=0)