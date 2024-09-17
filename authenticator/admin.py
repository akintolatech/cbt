from django.contrib import admin
from .models import (
    Profile,
    Form,
    ClassGroup
)

# Register your models here.
admin.site.register(Form)
admin.site.register(ClassGroup)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']
