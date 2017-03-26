#-*-encoding:utf-8-*-
from django.conf.urls import patterns, include, url
from member import views

urlpatterns = patterns('',
    url(r'^first', views.first, name='member.first'),
    url(r'^money', views.money, name='member.money'),
    url(r'^assets', views.assets, name='member.assets'),
    url(r'^join', views.join, name='member.join'),
    url(r'^logout', views.logout, name='member.logout'),
    url(r'^$', views.index, name='member.index'),
    

)
