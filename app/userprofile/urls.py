from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.userprofile.views',
    #url(r'^$', 'main', name='main_page'),

    url(r'^(?P<username>[-\.\w]+)/$', 'profile_detail', name='userprofile_detail'),
    url(r'^(?P<username>[-\.\w]+)/edit/$', 'edit', name='userprofile_edit'),
)
