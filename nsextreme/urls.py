from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings

from registration.backends.default.views import (
    ActivationView,
    RegistrationView,
)

from nsextreme.forms import EmailRegistrationForm

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nsextreme.views.home', name='home'),
    # url(r'^nsextreme/', include('nsextreme.foo.urls')),

    url(r'^api/', include('nsextreme.api.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'nsextreme.views.home'),
    url(r'^upload/$', TemplateView.as_view(template_name="fileupload.html")),
    url(r'^support/$', 'nsextreme.views.support', name='support'),
    url(r'^contact/$', 'nsextreme.views.contact', name='contact'),
    url(r'^features/$', 'nsextreme.views.features', name='features'),
    url(r'^testimonials/$', 'nsextreme.views.testimonials', name='testimonials'),
    url(r'^terms_conditions/$', 'nsextreme.views.terms_conditions', name='terms_conditions'),

    #url(r'^profile/$', 'nsextreme.views.profile'),
    url(r'^explore/(?P<categoryid>\d+)/page/(?P<pagenum>\d+)$', 'nsextreme.views.explore_c_p', name='explore_c_p'),
    url(r'^explore/(?P<categoryid>\d+)/$', 'nsextreme.views.explore_c', name='explore_c'),
    url(r'^explore/page/(?P<pagenum>\d+)$', 'nsextreme.views.explore_p', name='explore_p'),
    url(r'^explore/$', 'nsextreme.views.explore', name='explore'),
    url(r'^activity/(?P<categoryid>\d+)/page/(?P<pagenum>\d+)$', 'nsextreme.views.activity_c_p', name='activity_c_p'),
    url(r'^activity/(?P<categoryid>\d+)/$', 'nsextreme.views.activity_c', name='activity_c'),
    url(r'^activity/page/(?P<pagenum>\d+)$', 'nsextreme.views.activity_p', name='activity_p'),
    url(r'^activity/$', 'nsextreme.views.activity', name='activity'),

    url(r'^favorites/page/(?P<pagenum>\d+)$', 'nsextreme.views.favorites_p', name='favorites_p'),
    url(r'^favorites/$', 'nsextreme.views.favorites', name='favorites'),
    url(r'^popular/page/(?P<pagenum>\d+)$', 'nsextreme.views.popular_p', name='popular_p'),
    url(r'^popular/$', 'nsextreme.views.popular', name='popular'),
    url(r'^toppicks/page/(?P<pagenum>\d+)$', 'nsextreme.views.toppicks_p', name='toppicks_p'),
    url(r'^toppicks/$', 'nsextreme.views.toppicks', name='toppicks'),
    url(r'^recommended/page/(?P<pagenum>\d+)$', 'nsextreme.views.recommended_p', name='recommended_p'),
    url(r'^recommended/$', 'nsextreme.views.recommended', name='recommended'),

    url(r'^favorites/add/(?P<videoid>[-\.\w]+)$', 'nsextreme.views.favorites_add', name='favorites_add'),
    url(r'^favorites/remove/(?P<videoid>[-\.\w]+)$', 'nsextreme.views.favorites_remove', name='favorites_delete'),

    url(r'^comment/list/(?P<videoid>[-\.\w]+)/$', 'nsextreme.views.comment_list', name='comment_list'),
    url(r'^comment/create/(?P<videoid>[-\.\w]+)/$', 'nsextreme.views.comment_create', name='comment_create'),
    url(r'^comment/vote/(?P<commentid>[-\.\w]+)/$', 'nsextreme.views.comment_vote', name='comment_vote'),
    url(r'^comment/update/(?P<commentid>[-\.\w]+)/$', 'nsextreme.views.comment_update', name='comment_update'),

    url(r'^video/(?P<pk>\d+)/detail$', 'nsextreme.views.details'),
    url(r'^video/(?P<pk>\d+)$', 'nsextreme.views.details', name='video_details'),
    url(r'^video/(?P<pk>\d+)/video_data$', 'nsextreme.views.video_data', name='video_data'),
    url(r'^video/(?P<pk>\d+)/sensor_data$', 'nsextreme.views.sensor_data'),
    url(r'^video/(?P<pk>\d+)/share_via_email$', 'nsextreme.views.share_via_email'),
    url(r'^video/scanner$', 'nsextreme.views.scanner'),
    url(r'^video/(?P<videoid>\d+)/like$', 'nsextreme.views.video_like', name='video_like'),
    url(r'^video/(?P<videoid>\d+)/unlike$', 'nsextreme.views.video_unlike', name='video_unlike'),
    url(r'^video/(?P<videoid>\d+)/fav$', 'nsextreme.views.video_fav', name='video_fav'),
    url(r'^user/video/(?P<videoid>\d+)$', 'nsextreme.views.private_video', name='private_video'),
    url(r'^user/video/(?P<videoid>\d+)/edit$', 'nsextreme.views.video_edit', name='video_edit'),
    url(r'^user/video/(?P<videoid>\d+)/delete$', 'nsextreme.views.video_delete', name='video_delete'),
    url(r'^user/video/(?P<videoid>\d+)/share$', 'nsextreme.views.video_share', name='video_share'),

    # url(r'^beta/', include('hunger.urls')),
    url(r'^facebook', include('django_facebook.urls')),
    #url(r'^accounts2/', include('django_facebook.auth_urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    #url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login/'}),
    url(r'^accounts/', include('nsextreme.reg.urls')),
    url(r'^accounts/', include('registration_email.backends.default.urls')),
    url(r'^profile/', include('app.userprofile.urls')),

)

# ... the rest of your URLconf goes here ...

# if settings.DEBUG:
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
