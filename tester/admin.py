from django.contrib import admin
from .models import Test, TestResult, Question

# Register your models here.
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(Question)
