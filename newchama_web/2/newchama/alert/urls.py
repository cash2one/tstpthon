#encoding:utf-8
from django.conf.urls import patterns, include, url
from alert import views

urlpatterns = patterns('',
    url(r'^index', views.index, name='alert.index'),
)
