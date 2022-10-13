from email import message
from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    USER = (
        (1, 'HOD'),
        (2, 'OFFICER'),
        (3, 'TEACHER'),
        (4, 'STUDENT'),
    )
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')

class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    department_name = models.ForeignKey(Department, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'media/schedule_class')
    session_year = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_year


class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    studentID = models.TextField(max_length = 30, null = True, unique=True)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    department_id = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    session_year = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username

class Teacher(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teacherID = models.TextField(max_length = 30, null = True, unique=True)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username

class Officer(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    officerID = models.TextField(max_length = 30, null = True, unique=True)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username


# Notifications sytem
class OfficerNotification(models.Model):
    officer_id = models.ForeignKey(Officer, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    status = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.officer_id.admin.first_name

class StudentNotification(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    status = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.student_id.admin.first_name





