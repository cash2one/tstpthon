#-*-encoding:utf-8-*-
from django.conf.urls import patterns, include, url
from oauth import views

urlpatterns = patterns('',
    
    url(r'^$', views.index, name='oauth.index'),
    

)