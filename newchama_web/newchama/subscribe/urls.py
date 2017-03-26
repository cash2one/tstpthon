from django.conf.urls import patterns, include, url

from subscribe import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='subscribe.index'),
	url(r'^json$', views.json, name='subscribe.json'),
    url(r'^add$', views.add, name='subscribe.add'),
    url(r'^edit/(\d+)/$', views.edit, name='subscribe.edit'),
    url(r'^delete/(\d+)/$', views.delete, name='subscribe.delete'),
	url(r'^save$', views.save, name='subscribe.save'),
	url(r'^interval/(\d+)/(\d+)/$', views.interval, name='subscribe.interval'),
)
