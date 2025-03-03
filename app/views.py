from django.shortcuts import render,redirect
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.
def home(request):
    return render(request,'home.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

from django.shortcuts import render

# Admin Dashboard
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Teacher Dashboard
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

# Student Dashboard
def student_dashboard(request):
    return render(request, 'student_dashboard.html')










#SINUP USER

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        user_type = request.POST["user_type"]  # Get user type from form

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        # Save data to MySQL table
        user = UserProfile(username=username, email=email, password=password, user_type=user_type)
        user.save()

        messages.success(request, "Signup successful!")
        return redirect("login")

    return render(request, "signup.html")



#login

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if user_type matches the one in the form
            if user.userprofile.user_type == user_type:  # Validate the selected user type
                # Redirect based on user type
                if user_type == "admin":
                    return redirect('admin_dashboard')
                elif user_type == "teacher":
                    return redirect('teacher_dashboard')
                elif user_type == "student":
                    return redirect('student_dashboard')
            else:
                return redirect('login')  # Redirect back to login if there's a mismatch
        else:
            # Handle invalid login attempt
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')
