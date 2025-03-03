
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Make user nullable
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    additional_info = models.TextField(blank=True)  # Can be used to store additional info specific to the user
    phone = models.CharField(max_length=15, blank=True)  # Add phone number field here

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


# teacher

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"


# students

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=100)
    major = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.major}"

# Admin

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)  # Specify admin's specific role or permissions

    def __str__(self):
        return f"{self.user.username} - Admin"
