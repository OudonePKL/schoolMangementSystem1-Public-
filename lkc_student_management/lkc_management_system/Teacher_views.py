from django.shortcuts import redirect, render
from app.models import Teacher
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def home(request):
    return render(request, 'Teacher/home.html')

# @login_required(login_url='/')
# def notifications(request):
#     officer = Teacher.objects.filter(admin = request.user.id)
#     for i in officer:
#         officer_id = i.id
#         notification = TeacherNotification.objects.filter(officer_id = officer_id)
#         context = {
#             'notification': notification,
#         }
#     return render(request, 'Officer/notification.html', context)

# @login_required(login_url='/')
# def officerNotificationsMakeAsDone(request, status):
#     notification = OfficerNotification.objects.get(id = status)
#     notification.status = 1
#     notification.save()
#     return redirect('Officer_notifications')