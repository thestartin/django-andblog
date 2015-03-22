from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def get_by_user_or_email(self, username, email):
        return self.filter(username=username) | self.filter(email=email)
