from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


from django.contrib.auth.models import User
from quiz.models import Teacher,Student,Test
# Create your views here.

def login_page(request):
    return render(request, "accounts/login.html")

def register_page(request):
    return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect('login_handle')


def login_handle(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # check is user is student or teacher
            try:
                student = Student.objects.get(user=user)
                return redirect('student_dashboard',id=student.id)
            except Student.DoesNotExist:
                teacher = Teacher.objects.get(user=user)
                return redirect('teacher_dashboard',id=teacher.id)
            # return redirect('home')  # replace 'home' with the name of your homepage URL
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')


def register_handle(request):
    # print("Inside the register handle",request.POST.get('email'))
    if request.method == 'POST':
        # Get the post parameters
        email = request.POST.get('email')
        fname =request.POST.get('name')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        type  = request.POST.get('type')
        username = email
        # check for errorneous input
        # username should be under 10 characters
        # if len(username) > 10:
        #     messages.error(request, "Username must be under 10 characters")
        #     return redirect('register')

        # username should be alphanumeric
        # if not username.isalnum():
        #     messages.error(request, "Username should only contain letters and numbers")
        #     return redirect('register')
        # password should match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.save()
        if type == "student":
            student = Student(user=myuser,name=fname)
            student.save()
            user = authenticate(request,username=email,password=pass1)
            if user is not None:
                login(request,user)
                # redirect('')
                return redirect('student_dashboard',id=student.id)
        if type == "teacher":
            teacher = Teacher(user=myuser,name=fname)
            teacher.save()
            user = authenticate(request,username=email,password=pass1)
            if user is not None:
                login(request,user)
                # redirect('')
                return redirect('teacher_dashboard',id=teacher.id)
        # messages.success(request, "You are successfully register ")
        # return redirect('/')

    else:
        return HttpResponse("404 - Not found")
    

@login_required
def student_dashboard(request,id):
    student = Student.objects.get(id=id)
    test    = Test.objects.all()

    context = {
        'student':student,
        'test':test
    }
    return render(request,"quiz/student_dashboard.html",context)

@login_required
def teacher_dashboard(request,id):
    teacher = Teacher.objects.get(id=id)
    test    = Test.objects.all()
    context = {
        'teacher':teacher,
        'tests':test
    }
    return render(request,"quiz/teacher_dashboard.html",context)

