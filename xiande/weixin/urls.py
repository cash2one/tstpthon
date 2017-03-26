#-*-encoding:utf-8-*-
from django.conf.urls import patterns, include, url
from weixin import views

urlpatterns = patterns('',
    
    url(r'^testjs', views.testjs, name='weixin.testjs'),
    url(r'^$', views.index, name='weixin.index'),

)
