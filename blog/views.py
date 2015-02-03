from django.shortcuts import render
from django.views.generic.edit import BaseFormView
from django.contrib.auth.decorators import login_required

from .forms import BlogEntryForm

@login_required('/')
class BlogEntry(BaseFormView):
    """"
    View to create and edit blog posts.
    """
    template_name = 'entry.html'
    form_class = BlogEntryForm

    def form_valid(self, form):
        pass
