from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import TemplateView

from common.views import LoginRegisterView, LogoutView, AjaxLoginRegisterView
from common.decorators import login_redirect

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_andblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^blog/', include("blog.urls", namespace='blog')),
    (r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('^logout/$', login_required(LogoutView.as_view()), name='logout'),
    url('^login/$', login_redirect(LoginRegisterView.as_view()), name='regular_login'),
    url('^login/js/$', login_redirect(AjaxLoginRegisterView.as_view()), name='popup_login'),
    url('^/', include("social.apps.django_app.urls", namespace="social")),

)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
