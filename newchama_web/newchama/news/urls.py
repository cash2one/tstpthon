from django.conf.urls import patterns, include, url

from news import views

urlpatterns = patterns('',
    url(r'^$', views.index,name='news.index'),
    url(r'^tag/(?P<tag>\w+)/$', views.tag, name='news.tag'),
    url(r'^detail/(\d+)/$', views.detail, name='news.detail'),
    url(r'^ajax_search_keyword$', views.ajax_search_keyword, name='news.ajax_search_keyword'),
    url(r'^search_keyword$', views.search_keyword, name='news.search_keyword'),
    url(r'^search', views.search, name='news.search'),
)