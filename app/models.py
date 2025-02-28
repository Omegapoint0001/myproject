from django.db import models

# Create your models here.
from django.db import models

class UserProfile(models.Model):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Note: Use password hashing in real apps
    user_type = models.CharField(max_length=10, choices=USER_TYPES)  # Store user role

    def __str__(self):
        return f"{self.username} ({self.user_type})"
