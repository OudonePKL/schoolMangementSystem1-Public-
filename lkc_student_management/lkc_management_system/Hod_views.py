from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from app.models import Department ,CustomUser, Officer, Student, OfficerNotification, StudentNotification, Subject, Teacher
from django.contrib import auth, messages


@login_required(login_url='/')
def home(request):
    student_count = Student.objects.all().count()
    teacher_count = Teacher.objects.all().count()
    officer_count = Officer.objects.all().count()
    department_count = Department.objects.all().count()

    student_gender_male = Student.objects.filter(gender = 'Male').count()
    student_gender_female = Student.objects.filter(gender = 'Female').count()

    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'officer_count': officer_count,
        'department_count': department_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,
    }

    return render(request, 'Hod/home.html', context)

# --------- For Student -----------
@login_required(login_url='/')
def addStudent(request):
    department = Department.objects.all()

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        studentID = request.POST.get('studentID')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')
        session_year = request.POST.get('session_year')
    
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'This email is already exist!')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'This username is already exist!')
            return redirect('add_student')

        if gender == 'Select Gender':
            messages.error(request, 'Choice The Gender Please!')
            return redirect('add_student')
        if department_id == 'Select Department':
            messages.error(request, 'Choice The Department Please!')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 4
            )
            user.set_password(password)
            user.save()
            department = Department.objects.get(id=department_id)
            student = Student(
                admin = user,
                studentID = studentID,
                address = address,
                department_id = department,
                gender = gender,
                session_year = session_year,
            )
            student.save()
            messages.success(request, user.first_name + " " + user.last_name + ' Are Successfully Added!')
            return redirect('add_student')
    context = {
        'department': department,
    }

    return render(request, 'Hod/addStudent.html', context)

@login_required(login_url='/')
def viewStudent(request):
    students = Student.objects.all()
    context = {
        'students': students
    }
    return render(request, 'Hod/viewStudent.html', context)

@login_required(login_url='/')
def editStudent(request, id):
    student = Student.objects.filter(id = id)
    department = Department.objects.all()

    context = {
        'student':student,
        'department':department,
    }
    return render(request,'Hod/editStudent.html',context)

@login_required(login_url='/')
def updateStudent(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        studentID = request.POST.get('studentID')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')
        session_year = request.POST.get('year')

        if gender == "Select Gender":
            messages.error(request,'Please Choose The Gender!')
        if department_id == "Select Department":
            messages.error(request,'Please Choose The Department!')

        else:
            user = CustomUser.objects.get(id = student_id)

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            

            if password != None and password != "":
                user.set_password(password)
            if profile_pic != None and profile_pic != "":
                user.profile_pic = profile_pic
            user.save()

            student = Student.objects.get(admin = student_id)
            student.studentID = studentID
            student.address = address
            student.gender = gender
            student.session_year = session_year

            department = Department.objects.get(id = department_id)
            student.department_id = department

            student.save()
            messages.success(request,'Record Are Successfully Updated !')
            return redirect('view_student')

    return render(request,'Hod/editStudent.html')

@login_required(login_url='/')
def deleteStudent(request, admin):
    student = CustomUser.objects.get(id = admin)
    student.delete()
    messages.success(request, 'Record Are Successfully Deleted!')
    return redirect('view_student')

# --------- For Teacher ---------
@login_required(login_url='/')
def addTeacher(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        teacherID = request.POST.get('teacherID')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'This email is already exist!')
            return redirect('add_teacher')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'This username is already exist!')
            return redirect('add_teacher')

        if gender == 'Select Gender':
            messages.error(request, 'Choice The Gender Please!')
            return redirect('add_teacher')

        user = CustomUser(
            first_name = first_name, 
            last_name = last_name, 
            email = email, 
            username = username,
            profile_pic = profile_pic,
            user_type = 3,
        )
        user.set_password(password)
        user.save()

        teacher = Teacher(
            teacherID = teacherID,
            admin = user,
            address = address,
            gender = gender,
        )
        teacher.save()
        messages.success(request, 'Teacher Are Successfully Added!')
        return redirect('add_teacher')


    return render(request, 'Hod/addTeacher.html')

@login_required(login_url='/')
def viewTeacher(request):
    teacher = Teacher.objects.all()
    context = {
        'teacher': teacher
    }
    return render(request, 'Hod/viewTeacher.html', context)

@login_required(login_url='/')
def editTeacher(request, id):
    teacher = Teacher.objects.get(id = id)
    context = {
        'teacher':teacher,
    }
    return render(request,'Hod/editTeacher.html',context)

@login_required(login_url='/')
def updateTeacher(request):
    if request.method == "POST":
        teacher_id = request.POST.get('teacher_id')
        profile_pic = request.FILES.get('profile_pic')
        teacherID = request.POST.get('teacherID')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id = teacher_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic   
        
        user.save()

        teacher = Teacher.objects.get(admin = teacher_id)
        teacher.teacherID = teacherID
        teacher.address = address
        teacher.gender = gender

        teacher.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_teacher')

    return render(request,'Hod/editTeacher.html')

@login_required(login_url='/')
def deleteTeacher(request, admin):
    teacher = CustomUser.objects.get(id = admin)
    teacher.delete()
    messages.success(request, 'Record Are Successfully Deleted!')
    return redirect('view_teacher')

# --------- For Officer -----------
@login_required(login_url='/')
def addOfficer(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        officerID = request.POST.get('officerID')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
    
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'This email is already exist!')
            return redirect('add_officer')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'This username is already exist!')
            return redirect('add_officer')

        if gender == 'Select Gender':
            messages.error(request, 'Choice The Gender Please!')
            return redirect('add_officer')

        user = CustomUser(
            first_name = first_name, 
            last_name = last_name, 
            email = email, 
            username = username,
            profile_pic = profile_pic,
            user_type = 2,
        )
        user.set_password(password)
        user.save()

        officer = Officer(
            officerID = officerID,
            admin = user,
            address = address,
            gender = gender,
        )
        officer.save()
        messages.success(request, 'Officer Are Successfully Added!')
        return redirect('add_officer')

    return render(request, 'Hod/addOfficer.html')

@login_required(login_url='/')
def viewOfficer(request):
    officer = Officer.objects.all()
    context = {
        'officer': officer,
    }
    return render(request, 'Hod/viewOfficer.html', context)

@login_required(login_url='/')
def editOfficer(request, id):
    officer = Officer.objects.get(id = id)
    context = {
        'officer': officer
    }
    return render(request, 'Hod/editOfficer.html', context )

@login_required(login_url='/')
def updateOfficer(request):
    if request.method == "POST":
        officer_id = request.POST.get('officer_id')
        profile_pic = request.FILES.get('profile_pic')
        officerID = request.POST.get('officerID')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id = officer_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic   
        
        user.save()

        officer = Officer.objects.get(admin = officer_id)
        officer.officerID = officerID
        officer.address = address
        officer.gender = gender

        officer.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_officer')

    return render(request,'Hod/editOfficer.html')

@login_required(login_url='/')
def deleteOfficer(request, admin):
    officer = CustomUser.objects.get(id = admin)
    officer.delete()
    messages.success(request, 'Record Are Successfully Deleted!')
    return redirect('view_officer')


# --------- For Department or Department -----------
@login_required(login_url='/')
def addDepartment(request):
    if request.method == 'POST':
        department_name = request.POST.get('department_name')

        department = Department(
            name = department_name
        )
        department.save()
        messages.success(request, 'Department Is Successfully Created!')
        return redirect('add_department')
        
    return render(request, 'Hod/addDepartment.html')

@login_required(login_url='/')
def viewDepartment(request):
    department = Department.objects.all()
    context = {
        'department': department,
    }
    return render(request, 'Hod/viewDepartment.html', context)

@login_required(login_url='/')
def editDepartment(request, id):
    department = Department.objects.get(id = id)

    context = {
        'department': department,
    }

    return render(request, 'Hod/editDepartment.html', context)

@login_required(login_url='/')
def updateDepartment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department_id = request.POST.get('department_id')

        department = Department.objects.get(id = department_id)
        department.name = name
        department.save()
        messages.success(request, 'Department Are Successfully Updated!')
        return redirect('view_department')

    return render(request, 'Hod/editDepartment.html')

@login_required(login_url='/')
def deleteDepartment(request, id):
    department = Department.objects.get(id = id)
    department.delete()
    messages.success(request, 'Department are Successfully Deleted!')

    return redirect('view_department')


# For Subjects
@login_required(login_url='/')
def addSubject(request):
    department = Department.objects.all()

    if request.method == 'POST':
        department_name = request.POST.get('department_name')
        session_year = request.POST.get('session_year')
        image = request.FILES.get('subject_pic')

        if department_name == 'Select Department':
            messages.error(request, 'Choice The Department Please!')
            return redirect('add_subject')
        else:
            department = Department.objects.get(id=department_name)
            subject = Subject(
                department_name= department,
                session_year = session_year,
                image = image,
            )
            subject.save()
            messages.success(request, 'Subject Is Successfully Created!')
            return redirect('add_subject')

    context = {
        'department': department,
    }
    return render(request, 'Hod/addSubject.html', context)

@login_required(login_url='/')
def viewSubject(request):
    subject = Subject.objects.all()
    context = {
        'subject': subject,
    }
    return render(request, 'Hod/viewSubject.html', context)

def editSubject(request, id):
    subject = Subject.objects.filter(id = id)
    department = Department.objects.all()

    context = {
        'subject':subject,
        'department':department,
    }
    
    return render(request, 'Hod/editSubject.html', context )

@login_required(login_url='/')
def updateSubject(request):
    # if request.method == 'POST':
    #     department_id = request.POST.get('department_id')
    #     department_name = request.POST.get('department_name')
    #     session_year = request.POST.get('session_year')
    #     subject_pic = request.POST.get('subject_pic')

    #     subject = Subject.objects.get(id = department_id)
    #     subject.department_name = department_name
    #     subject.session_year = session_year
    #     subject.subject_pic = subject_pic
    #     subject.save()
    #     messages.success(request, 'Subject Are Successfully Updated!')
    #     return redirect('view_subject')

    return render(request, 'Hod/editSubject.html')

@login_required(login_url='/')
def deleteSubject(request, id):
    subject = Subject.objects.get(id = id)
    subject.delete()
    messages.success(request, 'Subject Are Successfully Deleted!')

    return redirect('view_subject')

# For Officer Message 
@login_required(login_url='/')
def officerSendMessage(request):
    officer = Officer.objects.all()
    see_notification = OfficerNotification.objects.all().order_by('-id')
    context = {
        'officer': officer,
        'see_notification': see_notification,
    }
    return render(request, 'Hod/officerSendMessage.html', context)

@login_required(login_url='/')
def saveOfficerMessage(request):
    if request.method == 'POST':
        officer_id = request.POST.get('officer_id')
        message = request.POST.get('message')

        officer = Officer.objects.get(admin = officer_id)
        notification = OfficerNotification(
            officer_id = officer,
            message = message,
        )
        notification.save()
        messages.success(request, 'Notification Are Successfully Sent')
        return redirect('officer_send_message')


# For Student Message 
@login_required(login_url='/')
def studentSendMessage(request):
    student = Student.objects.all()
    see_notification = StudentNotification.objects.all().order_by('-id')
    context = {
        'student': student,
        'see_notification': see_notification,
    }
    return render(request, 'Hod/studentSentNotification.html', context)

@login_required(login_url='/')
def saveStudentMessage(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')

        student = Student.objects.get(admin = student_id)
        notification = StudentNotification(
            student_id = student,
            message = message,
        )
        notification.save()
        messages.success(request, 'Notification Are Successfully Sent')
        return redirect('student_send_message')


