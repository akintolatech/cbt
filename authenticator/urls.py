from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "authenticator"

urlpatterns = [
    path('', views.user_login, name="login"),
    # path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name="register"),
    path('edit_account/', views.edit_account, name="edit_account"),
]
