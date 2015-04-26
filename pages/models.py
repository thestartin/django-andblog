from django.db import models
from django.conf import settings


class Page(models.Model):
    title = models.CharField(max_length=100)  # Heading of the page
    menu_name = models.CharField(max_length=10, unique=True)  # Menu display name
    menu_display_name = models.CharField(max_length=10, unique=True)  # Menu name
    content = models.TextField()  # Content of the page
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='page_created_by')
    create_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='page_updated_by')
    updated_date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.menu_display_name