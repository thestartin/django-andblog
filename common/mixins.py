from django.http import HttpResponseBadRequest


class MultiFormMixin(object):
    """
    Mixin to use/process multiple forms in a view
    """
    def get_form_class(self, form_name=None):
        if not self.form_classes:
            # If there are no form classes return bad request.
            return HttpResponseBadRequest()

        if form_name:
            form = self.form_classes.get(form_name)
            if not form:
                return HttpResponseBadRequest()

            return form

        return tuple(self.form_classes.itervalues())

    def get_form(self, form_classes, exclude=None):
        if isinstance(form_classes, tuple):
            forms = []
            for form_class in form_classes:
                forms.append(form_class(**self.get_form_kwargs()))

            return forms
        else:
            return form_classes(**self.get_form_kwargs())

    def get_all_other_forms(self, form):
        forms = [form]
        for form_name, form_class in self.form_classes.iteritems():
            if form_name != str(form):
                forms.append(form_class(**self.get_form_kwargs(others=True)))

        return forms

    def get_form_kwargs(self, others=False):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT') and not others:
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=self.get_all_other_forms(form)))


class AjaxContextMixin(object):
    """
    Mixin to add Ajax specific context data
    """

    def get_context_data(self, **kwargs):
        context = super(AjaxContextMixin, self).get_context_data(**kwargs)
        context['ajax'] = True
        next_page = self.request.GET.get('next')
        if next_page:
            context['next_page'] = next_page
        return context
