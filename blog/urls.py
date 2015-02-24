from django.conf.urls import patterns, url

from .views import BlogEntry, BlogList, BlogDetail, BlogUpdate


urlpatterns = patterns('',
                       url('^create/$', BlogEntry.as_view(), name='create'),
                       url('^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', BlogList.as_view(route='ymd'), name='blog_list_ymd'),
                       url('^(?P<year>\d{4})/(?P<month>\d{2})/$', BlogList.as_view(route='year_month'), name='blog_list_year_month'),
                       url('^(?P<year>\d{4})/$', BlogList.as_view(route='year'), name='blog_list_year'),
                       url('^tags/(?P<tag>\w+)/$', BlogList.as_view(route='tag'), name='blog_list_tag'),
                       url('^view/(?P<slug>[\w-]+)/edit', BlogUpdate.as_view(), name='blog_update'),
                       url('^view/(?P<slug>[\w-]+)', BlogDetail.as_view(), name='blog_detail'),
                       url('^$', BlogList.as_view(), name='blog_list'),
                       #url('^update/(?P<blog_id>\d+)/$', name='update'),
)