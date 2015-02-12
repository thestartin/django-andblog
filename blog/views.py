from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import JsonResponse
from ckeditor.widgets import CKEditorWidget

from .forms import BlogEntryForm
from .services import get_custom_fields
from .models import Article, ArticleSection


class BlogEntry(FormView):
    """"
    View to create and edit blog posts.
    """
    template_name = 'entry.html'
    form_class = BlogEntryForm
    request_custom_fields = []
    # Custom fields used by the form form the Client
    # The format is dict with <field_name>:[<field_type>, <list of args as in form>, <dict of kwargs as in form>]
    custom_fields = {
        'title': (forms.CharField, (), {'max_length': 150}),
        'content': (forms.CharField, (), {'widget': CKEditorWidget()})
    }

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        Redefining post to process custom sections by Client. Not doing this is init as that would spoil get requests.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.request_custom_fields = get_custom_fields(self.custom_fields, request)
        self.add_custom_fields(form, request)
        if form.is_valid():
            return self.form_valid(form)
        else:
            # We use Ajax forms so return the errors
            return JsonResponse(form.errors)

    def add_custom_fields(self, form, request):
        for field in self.request_custom_fields:
            field_type, args, kwargs = field[1]
            form.fields[field[0]] = field_type(*args, **kwargs)

    def form_valid(self, form):
        article = Article()
        article.add_article(form.cleaned_data, self.request.user)
