from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USEREMAIL_FIELD = 'email'

