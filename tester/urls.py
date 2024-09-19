from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "tester"

urlpatterns = [
    path('test_questions/<int:test_id>', views.test_questions, name="test_questions"),
    path('<int:test_id>/results/', views.mark_test, name='mark'),
    path('test_results/', views.test_results, name='test_results'),
]
