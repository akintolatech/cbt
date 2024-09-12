from django.contrib import admin
from .models import StudentUser, ClassGroup, Form

# Register your models here.
admin.site.register(Form)
admin.site.register(ClassGroup)
admin.site.register(StudentUser)
