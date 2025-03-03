from django.shortcuts import render,redirect
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings


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

from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    if request.user.userprofile.user_type != 'admin':
        return redirect('login')  # Redirect if the user is not an admin
    users=UserProfile.object.all()
    return render(request, 'admin_dashboard.html',{'users':users})

@login_required
def teacher_dashboard(request):
    if request.user.userprofile.user_type != 'teacher':
        return redirect('login')  # Redirect if the user is not a teacher
    return render(request, 'teacher_dashboard.html')

@login_required
def student_dashboard(request):
    if request.user.userprofile.user_type != 'student':
        return redirect('login')  # Redirect if the user is not a student
    return render(request, 'student_dashboard.html')




def forgot_password(request):
    # Logic to handle forgot password (like showing a form to reset password)
    return render(request, 'forgot_password.html')









#SINUP USER

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        user_type = request.POST["user_type"]
        phone = request.POST["phone_number"]
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create the user profile and save it
        user_profile = UserProfile(user=user, user_type=user_type,phone=phone)
        user_profile.save()

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
                    messages.error(request, "User type mismatch. Please try again.")
                    return redirect('login')  # Redirect back to login if there's a mismatch
        else:
            # Handle invalid login attempt
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')



def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        try:
            user = User.objects.get(email=email)
            # Generate password reset link or token (implement your logic here)
            # For example, send a reset link to the email
            reset_link = "http://yourwebsite.com/reset_password/{token}"  # Replace with actual token

            # Send email (make sure you configure email settings in Django settings.py)
            send_mail(
                "Password Reset Request",
                f"Click the following link to reset your password: {reset_link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(request, "A password reset link has been sent to your email.")
            return redirect('login')  # Redirect to login after sending the link
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return redirect('forgot_password')  # Stay on the forgot password page if no account is found

    return render(request, "forgot_password.html")
