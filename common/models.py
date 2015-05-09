from django.contrib.auth.models import AbstractUser
from django.db import models
from sorl.thumbnail.fields import ImageField
from django.conf import settings

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    avatar = ImageField(upload_to=settings.PROFILE_UPLOAD_PATH, blank=True, null=True)
    subscription = models.CharField(max_length=1, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    about = models.TextField(max_length=1000, blank=True, null=True)
    USEREMAIL_FIELD = 'email'

    objects = CustomUserManager()


class ContactUs(models.Model):
    subject = models.CharField(max_length=250)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    contacted_date_time = models.DateTimeField(auto_now_add=True)
    contacted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
