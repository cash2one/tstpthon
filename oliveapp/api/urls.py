from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from api import views

urlpatterns = patterns('',
    url(r'^ip/ip2city', views.ip2city, name='ip2city'),
    url(r'^$', views.index, name='index'),
)

