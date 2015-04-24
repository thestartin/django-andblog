from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from common.forms import EMAIL_REGEX


class EmailModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        if EMAIL_REGEX.match(username):
            UserModel = get_user_model()
            try:
                user = UserModel._default_manager.get_by_user_or_email(None, username)
                if user.check_password(password):
                    return user
            except UserModel.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a non-existing user (#20760).
                UserModel().set_password(password)
        else:
            super(EmailModelBackend, self).authenticate(username=username, password=password, **kwargs)
