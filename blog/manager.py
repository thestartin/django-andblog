from django.db import models


class UserArticleManager(models.Manager):
    def get_queryset(self):
        return super(UserArticleManager, self).get_queryset().filter()
