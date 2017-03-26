from django.conf.urls import patterns, include, url
from news import views

urlpatterns = patterns('',
                    url(r'^$', views.index, name='news.index'),
                    url(r'^add$', views.add, name='news.add'),
                    url(r'^edit/(\d+)$', views.edit, name='news.edit'),
)