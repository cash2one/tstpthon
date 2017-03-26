from django.conf.urls import patterns, include, url

from cvsource import views

urlpatterns = patterns('',
    
    url(r'^rank', views.rank, name='cvsource.rank'),
    url(r'^contact', views.contact, name='cvsource.contact'),
    url(r'^data', views.data, name='cvsource.data'),
    url(r'^news', views.news, name='cvsource.news'),
)