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
