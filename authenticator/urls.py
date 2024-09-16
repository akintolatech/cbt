from django.urls import path
from . import views

app_name = "authenticator"

urlpatterns = [
    path('', views.log_in, name="login"),
    path('register/', views.register, name="register"),
]
