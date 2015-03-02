from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

import blog

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_andblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^blog/', include("blog.urls", namespace='blog')),
    (r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))