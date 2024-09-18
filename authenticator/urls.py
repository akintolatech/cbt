from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "authenticator"

urlpatterns = [
    path('', views.user_login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name="register"),
    path('student_dashboard/', views.student_dashboard, name="student_dashboard"),
    path('edit_account/', views.edit_account, name="edit_account"),
]
