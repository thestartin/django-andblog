from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from common.forms import EMAIL_REGEX


class EmailModelBackend(ModelBackend):
    def authenticate(self, user_name_email=None, password=None, **kwargs):
        if EMAIL_REGEX.match(user_name_email):
            UserModel = get_user_model()
            if user_name_email is None:
                username = kwargs.get(UserModel.USERNAME_FIELD)
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
                if user.check_password(password):
                    return user
            except UserModel.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a non-existing user (#20760).
                UserModel().set_password(password)
        else:
            super(EmailModelBackend, self).authenticate(username=user_name_email, password=password, **kwargs)
