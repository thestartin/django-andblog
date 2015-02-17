from django.conf.urls import patterns, url

from .views import BlogEntry, BlogList


urlpatterns = patterns('',
                       url('^create/$', BlogEntry.as_view(), name='create'),
                       url('^$', BlogList.as_view(), name='blog_list'),
                       #url('^update/(?P<blog_id>\d+)/$', name='update'),
)