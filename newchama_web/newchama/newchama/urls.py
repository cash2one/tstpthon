#-*-encoding:utf-8-*-
from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
   
    url(r'^$', 'home.views.index', name='home'),
    
    url(r'^baidu_verify_hDP2Pd8fky.html$',  'home.views.baidu_verify_hDP2Pd8fky', name='baidu_verify_hDP2Pd8fky'),
    url(r'^home/', include('home.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^sales/', include('sales.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^deal/', include('deal.urls')),
    url(r'^services/', include('services.urls')),
    url(r'^purchase/', include('purchase.urls')),
    url(r'^subscribe/', include('subscribe.urls')),
    
    url(r'^buyer/', 'account.views.home', {'role_type':'buyer'},name='account.buyer'),
    url(r'^seller/', 'account.views.home',{'role_type':'seller'}, name='account.seller'),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    url(r'^api/', include('api.urls')),
    #url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)
