from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django import forms


# Create your models here.
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
    passport = models.ImageField(upload_to="passports", blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=11, blank=True, null=True)

    classes = models.CharField(max_length=50)
    total_score = models.IntegerField(default=2)
    position = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = StudentUserManager()

    def __str__(self):
        return self.username


class Form(models.Model):
    name = models.CharField(max_length=50)
    rnk = models.ImageField(upload_to='rnk/', null=True, blank=True)

    def __str__(self):
        return self.name
