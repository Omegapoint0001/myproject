from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import datetime


# Phone number validation regex
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


# UserProfile Model (for User Type and Phone)
class UserProfile(models.Model):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Make user nullable
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    additional_info = models.TextField(blank=True)  # Can be used to store additional info specific to the user
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # Add phone number field with validation

    class Meta:
        permissions = [
            ("can_mark_attendance", "Can mark attendance"),
            ("can_view_attendance", "Can view attendance"),
        ]
    
    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # Add phone number field with validation

    def __str__(self):
        return f"{self.user.username} - {self.subject} ({self.department})"


# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=100)
    major = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.major}"


# Admin Model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)  # Specify admin's specific role or permissions

    def __str__(self):
        return f"{self.user.username} - Admin"


# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Semester Model
class Semester(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, related_name="semesters", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.department.name}"


# Student Model (for Attendance System)
class Student(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, related_name="students", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey(Student, related_name="attendances", on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, related_name="attendances", on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    
    # Attendance for each hour (let's say 8 hours a day)
    hour_1 = models.BooleanField(default=False)
    hour_2 = models.BooleanField(default=False)
    hour_3 = models.BooleanField(default=False)
    hour_4 = models.BooleanField(default=False)
    hour_5 = models.BooleanField(default=False)
    hour_6 = models.BooleanField(default=False)
   
    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.semester.name}"

