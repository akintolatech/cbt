from django.db import models
from django.conf import settings

class Form(models.Model):
    name = models.CharField(max_length=33)
    form_img = models.ImageField(upload_to='form_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class ClassArm(models.Model):
    name = models.CharField(max_length=33)
    # class_form = models.ForeignKey(Form, on_delete=models.CASCADE)
    class_form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    photo = models.ImageField(
        upload_to='passport',
        blank=True,
        # default=""
    )

    class_arm = models.ForeignKey(
        ClassArm,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    phone_number = models.CharField(max_length=11, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


