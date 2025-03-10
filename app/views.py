
from django.shortcuts import render, redirect
from .models import UserProfile,AttendanceStudent, Department, Semester, Attendance
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date
from django.contrib.auth.decorators import login_required

# Home View
def home(request):
    return render(request, 'home.html')

# Login View
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


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        user_type = request.POST["user_type"]
        phone = request.POST["phone"]  # Updated here to match the form field name

        # Ensure passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        # Validate that email and username are not already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect("signup")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already in use.")
            return redirect("signup")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create the user profile and save it
        user_profile = UserProfile(user=user, user_type=user_type, phone=phone)
        user_profile.save()

        messages.success(request, "Signup successful!")
        return redirect("login")

    return render(request, "signup.html")


# Admin Dashboard View
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# Admin Dashboard View
@login_required
def admin_dashboard(request):
    if request.user.userprofile.user_type != 'admin':
        return redirect('login')  # Redirect if the user is not an admin
    
    # Get all users for the admin to manage
    users = UserProfile.objects.all()
    
    # Render the admin dashboard with user data
    return render(request, 'admin_dashboard.html', {'users': users})


# Teacher Dashboard View
@login_required
def teacher_dashboard(request):
    if request.user.userprofile.user_type != 'teacher':
        return redirect('login')  # Redirect if the user is not a teacher
    
    # Render the teacher dashboard
    return render(request, 'teacher_dashboard.html')


# Student Dashboard View
@login_required
def student_dashboard(request):
    if request.user.userprofile.user_type != 'student':
        return redirect('login')  # Redirect if the user is not a student
    
    # Render the student dashboard
    return render(request, 'student_dashboard.html')






# Forgot Password View
def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        try:
            user = User.objects.get(email=email)
            # Generate password reset link or token (implement your logic here)
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


# About, Contact, Terms, Privacy Views (no changes needed)
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')




def mark_attendance(request):
    departments = Department.objects.all()  # Get all departments
    semesters = Semester.objects.all()      # Get all semesters
    students = AttendanceStudent.objects.all()        # Get all students
    
    if request.method == "POST":
        # Handle form submission
        attendance_data = request.POST
        
        # Ensure that the required fields are selected
        student_id = attendance_data.get('student')
        semester_id = attendance_data.get('semester')
        
        # Make sure student and semester are valid
        if student_id and semester_id:
            student = AttendanceStudent.objects.get(id=student_id)
            semester = Semester.objects.get(id=semester_id)
            
            # Check if attendance for today has already been marked
            existing_attendance = Attendance.objects.filter(
                student=student, semester=semester, date=date.today()
            )
            
            if not existing_attendance.exists():  # Only create a new attendance record if one doesn't exist
                attendance = Attendance.objects.create(
                    student=student,
                    semester=semester,
                    date=date.today(),
                )

                # Loop through each hour (1-8) and mark attendance
                for hour in range(1, 9):  # Assuming 8 hours a day
                    # Check if the hour checkbox was checked (should be 'on' if checked)
                    is_present = attendance_data.get(f'hour_{hour}') == 'on'
                    setattr(attendance, f'hour_{hour}', is_present)

                attendance.save()
            else:
                # Handle case where attendance for the day is already recorded
                return render(request, 'mark_attendance.html', {
                    'students': students, 'semesters': semesters, 
                    'departments': departments, 'error': 'Attendance already marked for today.'
                })

        else:
            return render(request, 'mark_attendance.html', {
                'students': students, 'semesters': semesters, 
                'departments': departments, 'error': 'Please select both student and semester.'
            })

    return render(request, 'mark_attendance.html', {'students': students, 'semesters': semesters, 'departments': departments})

from django.shortcuts import render, redirect
from .models import AttendanceStudent, Semester, Attendance
from .forms import AttendanceForm
from django.utils import timezone

def mark_attendance(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    students = AttendanceStudent.objects.filter(department=semester.department)  # Get students for this semester

    if request.method == 'POST':
        for student in students:
            attendance_data = request.POST.get(f'attendance_{student.id}')  # Collect the attendance data for each student
            attendance_instance = Attendance.objects.get_or_create(student=student, semester=semester, date=timezone.now().date())[0]
            # Update attendance for the hours (for example)
            attendance_instance.hour_1 = 'hour_1' in attendance_data
            attendance_instance.hour_2 = 'hour_2' in attendance_data
            attendance_instance.hour_3 = 'hour_3' in attendance_data
            attendance_instance.hour_4 = 'hour_4' in attendance_data
            attendance_instance.hour_5 = 'hour_5' in attendance_data
            attendance_instance.hour_6 = 'hour_6' in attendance_data
            attendance_instance.save()

        return redirect('attendance_list', semester_id=semester.id)  # Redirect to a page showing all attendance

    return render(request, 'mark_attendance.html', {
        'semester': semester,
        'students': students
    })


from django.http import JsonResponse
from .models import Department, Semester,AttendanceStudent

def get_students(request, department_id, semester_id):
    try:
        # Get the department and semester based on the provided IDs
        department = Department.objects.get(id=department_id)
        semester = Semester.objects.get(id=semester_id)

        # Get all students in this department and semester (you may need a relationship model to link these)
        students = Student.objects.filter(department=department)

        # Prepare the response data
        student_data = [{"id": student.id, "name": student.name} for student in students]

        # Return the data as JSON
        return JsonResponse({"students": student_data})

    except Department.DoesNotExist or Semester.DoesNotExist:
        return JsonResponse({"error": "Invalid department or semester"}, status=400)

# views.py
from django.shortcuts import render

def admin_dashboard(request):
    # Your logic for admin dashboard
    return render(request, 'admin_dashboard.html')

def teacher_dashboard(request):
    # Your logic for teacher dashboard
    return render(request, 'teacher_dashboard.html')

def student_dashboard(request):
    # Your logic for student dashboard
    return render(request, 'student_dashboard.html')
