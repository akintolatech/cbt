from django.db import models

# Create your models here.
class AppInfo (models.Model):
    logo = models.ImageField(upload_to="webcms", blank=True, null=True)
    email = models.CharField(max_length=33)
    name = models.CharField(max_length=33)
    phone = models.CharField(max_length=11, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phrase = models.CharField(max_length=500)


    def __str__(self):
        return self.name