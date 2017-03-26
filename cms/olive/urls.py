#-*-encoding:utf-8-*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'olive.views.home', name='home'),
    url(r'^weixin/', include('weixin.urls')),
    url(r'^backend/', include('backend.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
