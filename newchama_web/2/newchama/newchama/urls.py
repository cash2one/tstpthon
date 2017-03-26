from django.conf.urls import patterns, include, url

from django.contrib import admin

from newchama import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'adminuser.views.index', name='home'),
     url(r'^Dashboard$', 'adminuser.views.index', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^adminuser/', include('adminuser.urls')),
    url(r'^member/', include('member.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^demand/', include('demand.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^repository/', include('repository.urls')),
    url(r'^area/', include('area.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^industry/', include('industry.urls')),
    url(r'^analysis/', include('analysis.urls')),
    url(r'^alert/', include('alert.urls')),
    url(r'^monitor/', include('monitor.urls')),
    url(r'^subscribe/', include('subscribe.urls')),
)
if settings.DEBUG:
   urlpatterns += patterns('',
        url(r'^upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
 )
