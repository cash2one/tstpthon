from django.conf.urls import patterns, include, url
from subscribe import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='subscribe.index'),
    url(r'^add$', views.add, name='subscribe.add'),
    url(r'^edit/(\d+)/$', views.edit, name='subscribe.edit'),
	url(r'^save$', views.save, name='subscribe.save'),
	url(r'^match_project/(\d+)/$', views.match_project, name='subscribe.match_project'),
)
