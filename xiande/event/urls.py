#-*-encoding:utf-8-*-
from django.conf.urls import patterns, include, url
from event import views

urlpatterns = patterns('',
    
    url(r'^bbb_first', views.bbb_first, name='event.bbb_first'),
    url(r'^bbb_success', views.bbb_success, name='event.bbb_success'),
    url(r'^bbb_wait', views.bbb_wait, name='event.bbb_wait'),
    url(r'^bbb_end', views.bbb_end, name='event.bbb_end'),
    url(r'^bbb_join', views.bbb_join, name='event.bbb_join'),
    url(r'^bbb', views.bbb, name='event.bbb'),
    url(r'^cash_join', views.cash_join, name='event.cash_join'),
    url(r'^cash', views.cash, name='event.cash'),
    url(r'^join', views.join, name='event.join'),

)
