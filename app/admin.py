from django.contrib import admin
from .models import Teacher, AttendanceStudent, Admin

# Register your models here.

admin.site.register(Teacher)
admin.site.register( AttendanceStudent)
admin.site.register(Admin)
