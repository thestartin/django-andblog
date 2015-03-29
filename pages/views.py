from django.views.generic import DetailView
from django.http import Http404
from django.utils.translation import ugettext as _

from .models import Page


class PageView(DetailView):
    template_name = "page.html"
    model = Page

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(menu_name=self.kwargs['menu_name'])

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj
