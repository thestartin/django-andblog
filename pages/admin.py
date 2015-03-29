from django.contrib import admin
from django.db import models
from ckeditor.widgets import CKEditorWidget

from .models import Page


class PageAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': CKEditorWidget()}}
    exclude = ['created_by', 'updated_by']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


admin.site.register(Page, PageAdmin)
