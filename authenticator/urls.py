from django.urls import path
from . import views

app_name = "authenticator"

urlpatterns = [
    path('', views.login_to_cbt, name="login"),
]
