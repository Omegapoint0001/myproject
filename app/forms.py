# forms.py
from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'semester', 'date', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6']



class UploadStudentFileForm(forms.Form):
    file = forms.FileField()
