from django.conf.urls import patterns, url
from industry import views

urlpatterns = patterns('',
    url(r'^json/(\d+)$', views.json, name='industry.json'),
    url(r'^get/(\d+)$', views.get_industry, name='industry.get'),
)
