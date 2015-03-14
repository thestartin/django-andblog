from django.shortcuts import render
from django.views.generic import FormView
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, RegisterForm, EMAIL_REGEX
from .mixins import MultiFormMixin


class LoginRegisterView(MultiFormMixin, FormView):
    template_name = "login.html"
    form_classes = {
        'loginform': LoginForm,
        'registerform': RegisterForm
    }
    valid_routes = {
        'loginform': 'login_user',
        'registerform': 'register_user'
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

    def form_valid(self, form):
        route = self.valid_routes.get(str(form))

        getattr(self, route)(form)

    def login_user(self, form):
        user = authenticate(username=form.cleaned_data['log_username'], password=form.cleaned_data['log_password'])

    def register_user(self, form):
        pass
