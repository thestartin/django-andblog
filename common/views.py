from django.shortcuts import render
from django.views.generic import FormView
from django.http import HttpResponseBadRequest

from .forms import LoginForm, RegisterForm
from .mixins import MultiFormMixin


class LoginRegisterView(MultiFormMixin, FormView):
    template_name = "login.html"
    form_classes = {
        'loginform': LoginForm,
        'registerform': RegisterForm
    }

    success_url = '/login'

    def post(self, request, *args, **kwargs):
        formname = request.POST.get('formname')
        if not formname:
            return HttpResponseBadRequest()

        form_class = self.get_form_class(form_name=formname)
        form = self.get_form(form_class, formname)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=self.get_all_other_forms(form)))

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