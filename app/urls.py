from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),  
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.terms, name='privacy'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    
        path('get_students/<int:department_id>/<int:semester_id>/', views.get_students, name='get_students'),
        # Dashboard paths
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    
]
