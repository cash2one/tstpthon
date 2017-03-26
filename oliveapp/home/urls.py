from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from home import views

import os
css_media = os.path.join(
    os.path.dirname(__file__),'templates/css/'
)
images_media = os.path.join(
    os.path.dirname(__file__),'templates/images/'
)
js_media = os.path.join(
    os.path.dirname(__file__),'templates/js/'
)

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^images/(?P<path>.*)$','django.views.static.serve',{'document_root': images_media }),
    url(r'^css/(?P<path>.*)$','django.views.static.serve',{'document_root': css_media }),
    url(r'^js/(?P<path>.*)$','django.views.static.serve',{'document_root': js_media }),
)
