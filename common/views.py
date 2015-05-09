from django.views.generic import FormView
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response

from .forms import LoginForm, RegisterForm, ProfileForm, ContactUsForm
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
            self.template_name = "login.html"
            return self.form_invalid(form)

    def form_valid(self, form):
        route = self.valid_routes.get(str(form))

        return getattr(self, route)(form)

    def login_user(self, form):
        user = authenticate(username=form.cleaned_data['log_user_name_email'], password=form.cleaned_data['log_password'])
        if not user:
            form._errors['log_user_name_email'] = 'User Name & password does not match'
            self.template_name = 'login.html'
            return self.form_invalid(form)

        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def register_user(self, form):
        data = form.cleaned_data
        user = CustomUser._default_manager.create_user(data['reg_user_name'], data['reg_user_email'], data['reg_password'])
        user = authenticate(username=user.username, password=data['reg_password'])
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


class ProfileView(FormView):
    form_class = ProfileForm
    self_template_name = 'profile.html'
    view_template_name = 'view_profile.html'

    def get(self, request, *args, **kwargs):
        user = self.kwargs.get('username')
        if (user and self.request.user.username == user) or (not user and self.request.user.is_authenticated):
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            return self.render_to_response(self.get_context_data(form=form))
        else:
            user = CustomUser._default_manager.filter(username=user).get()
            return self.render_to_response(context={'viewuser': user})

    def form_valid(self, form):
        data = form.cleaned_data
        cleaned = form.changed_data
        user = self.request.user
        if cleaned:
            if self.request.POST.get('username') != user.username:
                return HttpResponseBadRequest()

            user._default_manager.update_user(data, cleaned, user)

        return HttpResponseRedirect(self.request.path)

    def get_template_names(self):
        user = self.kwargs.get('username')
        if (user and self.request.user.username == user) or (not user and self.request.user.is_authenticated):
            return [self.self_template_name]
        else:
            return [self.view_template_name]

    def get_initial(self):
        initial = dict()
        initial['name'] = self.request.user.get_full_name()
        initial['subscription'] = self.request.user.subscription
        initial['avatar'] = self.request.user.avatar
        initial['username'] = self.request.user.username
        initial['about'] = self.request.user.about
        initial['location'] = self.request.user.location
        return initial.copy()


class ContactUsView(CreateView):
    form_class = ContactUsForm
    template_name = "contact.html"
    success_url = '/'

    def get_initial(self):
        if self.request.user.is_authenticated():
            self.initial['contacted_by'] = self.request.user
            self.initial['email'] = self.request.user.email
        else:
            self.initial['contacted_by'] = ''
            self.initial['email'] = ''

        return self.initial.copy()

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)
