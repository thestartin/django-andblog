from django.conf import settings
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.base import TemplateView
from django import forms
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy
from ckeditor.widgets import CKEditorWidget

from .forms import BlogEntryForm, BlogEntryUpdateForm, BlogVoteForm
from .services import get_custom_fields, BlogPaginator
from .models import Article, ArticleSection
from .mixins import JSONResponseMixin
from .decorators import get_ip_hashed


class BlogEntry(FormView):
    """"
    View to create and edit blog posts.
    """
    template_name = 'entry.html'
    form_class = BlogEntryForm
    success_url = '/'
    request_custom_fields = []
    # Custom fields used by the form form the Client
    # The format is dict with <field_name>:[<field_type>, <list of args as in form>, <dict of kwargs as in form>]
    custom_fields = {
        'title': (forms.CharField, (), {'max_length': 150}),
        'content': (forms.CharField, (), {'widget': CKEditorWidget()}),
        'score': (forms.DecimalField, (), {'max_digits': settings.RATING_MAX_DIGITS,
                                           'max_value': settings.RATING_SCALE})
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
        return HttpResponseRedirect(self.get_success_url())


class BlogList(ListView):
    route = 'all'
    model = Article
    template_name = 'blog_list.html'
    paginate_by = 2
    context_object_name = 'articles'
    paginator_class = BlogPaginator

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.request.user.is_staff:
            queryset = self.model.objects.get_posts(self.route, **self.kwargs)
        else:
            queryset = self.model.pub.get_posts(self.route, **self.kwargs)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data()
        return context


class BlogDetail(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'blog_detail.html'

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        queryset = super(BlogDetail, self).get_queryset().prefetch_related('articlesection_set').select_related('author')
        return queryset


class BlogUpdate(FormView):
    template_name = 'blog_update.html'
    form_class = BlogEntryUpdateForm
    pk_url_kwarg = 'pk'
    slug_url_kwarg = 'slug'

    def get_initial(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        self.pk = self.kwargs.get(self.pk_url_kwarg, None)
        self.slug = self.kwargs.get(self.slug_url_kwarg, None)

        if self.pk:
            data = Article._default_manager.filter(pk=self.pk).prefetch_related('articlesection_set').\
                select_related('author')
        else:
            data = Article._default_manager.filter(slug=self.slug).prefetch_related('articlesection_set').\
                select_related('author')

        try:
            initial = data.get()
        except ObjectDoesNotExist:
            raise Http404("OOps! Article does not exist")

        return initial

    def form_valid(self, form):
        try:
            article = Article._default_manager.get(pk=form.cleaned_data['article'])
            article.update_article(form.cleaned_data, form.changed_data, self.request.user)
            return HttpResponseRedirect(self.get_success_url())
        except ObjectDoesNotExist:
            raise Http404

    def form_invalid(self, form):
        return JsonResponse(form.errors)

    def get_success_url(self):
        kwargs = {}
        if self.pk:
            kwargs['pk'] = self.pk
        if self.slug:
            kwargs['slug'] = self.slug

        return reverse_lazy('blog:blog_update', kwargs=kwargs)


class BlogVote(JSONResponseMixin, FormView):
    http_method_names = ['post']
    hashed_ip = ''
    form_class = BlogVoteForm

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    @get_ip_hashed
    def post(self, request, hashed_ip, *args, **kwargs):
        self.failure_message['message'] = 'Unable to cast your vote at this point'
        self.success_message['message'] = 'Successfully casted the vote'

        if not hashed_ip:
            return self.render_to_response(self.failure_message, **kwargs)

        self.hashed_ip = hashed_ip
        return super(BlogVote, self).post(self, request, *args, **kwargs)

    def form_invalid(self, form):
        return self.render_to_response(self.failure_message)

    def form_valid(self, form):
        if ArticleSection._default_manager.vote(form.cleaned_data, self.hashed_ip, self.request.user):
            return self.render_to_response(self.success_message)
        else:
            self.failure_message['message'] = "You have already voted"
            return self.render_to_response(self.failure_message)
