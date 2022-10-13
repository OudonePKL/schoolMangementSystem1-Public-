from django.shortcuts import redirect, render
from app.models import Officer, OfficerNotification
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def home(request):
    return render(request, 'Officer/home.html')

@login_required(login_url='/')
def messages(request):
    officer = Officer.objects.filter(admin = request.user.id)
    for i in officer:
        officer_id = i.id
        messages = OfficerNotification.objects.filter(officer_id = officer_id)
        context = {
            'messages': messages,
        }
    return render(request, 'Officer/message.html', context)

@login_required(login_url='/')
def officerMessageMakeAsDone(request, status):
    messages = OfficerNotification.objects.get(id = status)
    messages.status = 1
    messages.save()
    return redirect('officer_messages')






