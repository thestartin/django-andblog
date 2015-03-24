from django.views.generic import FormView
from django.views.generic.base import View
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, RegisterForm
from .mixins import MultiFormMixin, AjaxContextMixin
from .models import CustomUser


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

    success_url = '/'

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
        return HttpResponseRedirect(self.get_success_url())

    def login_user(self, form):
        user = authenticate(username=form.cleaned_data['log_user_name_email'], password=form.cleaned_data['log_password'])
        login(self.request, user)

    def register_user(self, form):
        data = form.cleaned_data
        user = CustomUser._default_manager.create_user(data['reg_user_name'], data['reg_user_email'], data['reg_password'])
        user = authenticate(username=user.username, password=user.password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)


class LogoutView(View):
    success_url = '/'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)


class AjaxLoginRegisterView(AjaxContextMixin, LoginRegisterView):
    template_name = 'includes/login_page.html'
