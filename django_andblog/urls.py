from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

import blog
from common.views import LoginRegisterView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_andblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^blog/', include("blog.urls", namespace='blog')),
    (r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('^login/$', LoginRegisterView.as_view(), name='regular_login'),
    url('^login/js/$', TemplateView.as_view(template_name='includes/../common/templates/includes/login_page.html'), name='js_login'),
    url('^/', include("social.apps.django_app.urls", namespace="social")),

)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))