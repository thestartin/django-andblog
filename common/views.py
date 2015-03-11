from django.shortcuts import render

from django.views.generic import FormView

from .forms import LoginForm, RegisterForm
from .mixins import MultiFormMixin


class LoginRegisterView(MultiFormMixin, FormView):
    template_name = "login.html"
    form_classes = {
        'loginform': LoginForm,
        'registerform': RegisterForm
    }

