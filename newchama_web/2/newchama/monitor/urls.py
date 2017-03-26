from django.conf.urls import patterns, url
from monitor import views

urlpatterns = patterns("",
        url(r'^shsz-notice/content/(\d+)$', views.notice_content, name='notice_content'),
        url(r'^hknotice/content/(\d+)$', views.hk_notice_content, name='hk_notice_content'),
        url(r'^daily_notices/$', views.daily_notices, name='monitor.daily_notices'),
        url(r'^daily_notices/deals_query/export_to_xls$', views.export_to_xls, name='export_to_xls'),
        url(r'^daily_notices/deals_query/$', views.deals_query, name='deals_query'),
        url(r'^daily_notices/submit_deals_to_database', views.submit_deals_to_database, name='submit_deals_to_database'),
        url(r'^daily_notices/notices_query/$', views.notices_query, name='notices_query'),)
