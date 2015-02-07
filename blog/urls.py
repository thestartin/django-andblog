from django.conf.urls import patterns, url

from .views import BlogEntry


urlpatterns = patterns('',
                       url('^create/$', BlogEntry.as_view(), name='create'),
                       #url('^update/(?P<blog_id>\d+)/$', name='update'),
)