from django.db import models
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def get_by_user_or_email(self, username, email):
        user = self.filter(username=username) | self.filter(email=email)
        return user.first()

    def update_user(self, data, changed, user):
        for field in changed:
            if field == 'name':
                names = data[field].split(' ')
                if len(names) > 1:
                    first_name = names[0]
                    last_name = ' '.join(names[1:])
                    setattr(user, 'first_name', first_name)
                    setattr(user, 'last_name', last_name)
                else:
                    first_name = names[0]
                    setattr(user, 'first_name', first_name)
            else:
                if hasattr(user, field):
                    setattr(user, field, data[field])

        user.save()
