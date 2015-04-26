from django.conf.urls import url, patterns

from .views import PageView


urlpatterns = patterns('',
                       url(r'^(?P<menu_name>[\w-]+)/$', PageView.as_view(), name='view')
                       )
