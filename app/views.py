from django.shortcuts import render,redirect
from .models import UserProfile
from django.contrib import messages
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
