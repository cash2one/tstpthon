#-*-encoding:utf-8-*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^qa/$', 'home.views.qa', name='home.qa'),
    url(r'^about/$', 'home.views.about', name='home.about'),
    url(r'^thinking/$', 'home.views.thinking', name='home.thinking'),
    url(r'^project/$', 'home.views.project', name='home.project'),
    url(r'^backend/', include('backend.urls')),
    url(r'^member/', include('member.urls')),
    url(r'^event/', include('event.urls')),

    url(r'^oauth/', include('oauth.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^weixin/$', 'home.views.weixin', name='home.weixin'),
    
    url(r'^$', 'backend.views.index', name='home'),
    
)
