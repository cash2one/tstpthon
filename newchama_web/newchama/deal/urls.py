from django.conf.urls import patterns, include, url

from deal import views

urlpatterns = patterns('',

    url(r'^$', views.index,{'type': '0'}, name='deal.index'),
    url(r'^index/(\d+)/$', views.index,name='deal.index'),
    url(r'^rank_deal_type', views.rank_deal_type, name='deal.rank_deal_type'),
    url(r'^rank', views.rank, name='deal.rank'),
    url(r'^industry/(\d+)/$', views.industry, name='deal.industry'),
    url(r'^country/(\d+)/$', views.country, name='deal.country'),
    url(r'^ajax_get_list/(?P<industry_id>\d+)/(?P<country_id>\d+)/(?P<page>\d+)/(?P<pagesize>\d+)$', views.ajax_get_list, name='deal.ajax_get_list'),
)