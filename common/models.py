from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    USEREMAIL_FIELD = 'email'

    objects = CustomUserManager()
