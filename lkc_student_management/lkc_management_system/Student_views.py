from django.shortcuts import redirect, render
from app.models import Student, StudentNotification
from django.contrib.auth.decorators import login_required



@login_required(login_url='/')
def home(request):
    return render(request, 'Student/home.html')

@login_required(login_url='/')
def messages(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id
        messages = StudentNotification.objects.filter(student_id = student_id)
        context = {
            'messages': messages,
        }
    return render(request, 'Student/messages.html', context)

@login_required(login_url='/')
def studentMessageMakeAsDone(request, status):
    messages = StudentNotification.objects.get(id = status)
    messages.status = 1
    messages.save()
    return redirect('student_messages')




