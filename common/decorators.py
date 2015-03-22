from django.http import HttpResponseRedirect


def login_redirect(func):
    def redirect_if_logged_in(request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            return func(request, *args, **kwargs)

    return redirect_if_logged_in