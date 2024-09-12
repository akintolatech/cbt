from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django import forms


# Create your models here.


class Form(models.Model):
    name = models.CharField(max_length=33)
    form_img = models.ImageField(upload_to='form_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class ClassGroup(models.Model):
    name = models.CharField(max_length=33)
    class_form = models.ForeignKey(Form, on_delete=models.CASCADE)


class StudentUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class StudentUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    passport = models.ImageField(upload_to="passports", blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)

    classes = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    form = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)

    total_score = models.IntegerField(default=2)
    position = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = StudentUserManager()

    def __str__(self):
        return self.username
