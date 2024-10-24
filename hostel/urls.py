from django.urls import path
from . import views
from .views import rector_logout  # Import the rector_logout view

urlpatterns = [
    path('signup/', views.student_signup, name='student_signup'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),  # Add this line
    path('faculty_login/', views.faculty_login, name='faculty_login'),
    path('rector_view/', views.rector_view, name='rector_view'),
    path('student_view/', views.student_view, name='student_view'),
    path('', views.home, name='home'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('rector_login/', views.rector_login, name='rector_login'),
    path('rector_logout/', rector_logout, name='rector_logout'),
    path('allot_rooms/', views.allot_rooms, name='allot_rooms'),
]
