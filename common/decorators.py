from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template.response import TemplateResponse


def login_redirect(func):
    def redirect_if_logged_in(request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            return func(request, *args, **kwargs)

    return redirect_if_logged_in


def staff_or_not_allowed(func):
    def disallow_if_not_staff(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        else:
            return func(request, *args, **kwargs)

    return disallow_if_not_staff
