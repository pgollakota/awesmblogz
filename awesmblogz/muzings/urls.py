from django.conf.urls import patterns, url

urlpatterns = patterns('awesmblogz.muzings.views',
   url(r'^$', 'entries_list'),
   url(r'^(?P<id>\d+)/$', 'entries_detail'),
)
