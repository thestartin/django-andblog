from django.contrib import admin
from django.db import models
from django.template.defaultfilters import slugify
from ckeditor.widgets import CKEditorWidget

from .models import Page
from common.funcs import set_menu_cache


class PageAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': CKEditorWidget()}}
    exclude = ['created_by', 'updated_by']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.updated_by = request.user
        obj.menu_name = slugify(obj.menu_name)
        obj.save()
        set_menu_cache()


admin.site.register(Page, PageAdmin)
