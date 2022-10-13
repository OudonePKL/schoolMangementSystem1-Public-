from django.contrib import admin
from .models import CustomUser, Department, Student, Officer, OfficerNotification, StudentNotification, Subject, Teacher
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserModle(UserAdmin):
    list_display = ['username', 'user_type']

admin.site.register(CustomUser, UserModle)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Officer)
admin.site.register(OfficerNotification)
admin.site.register(StudentNotification)
admin.site.register(Subject)