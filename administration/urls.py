from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = "administration"

urlpatterns = [
    # Add patterns here
    path('', views.administration_dashboard, name='administration'),
    path('test_mgmt/', views.test_mgmt, name="test_mgmt"),
    path('create_test/', views.create_test, name="create_test"),
    path('edit_test/<int:test_id>/', views.edit_test, name="edit_test")
]