from django.conf.urls import patterns, include, url

from home import views

import os
css_media = os.path.join(
    os.path.dirname(__file__),'templates/css/'
)
images_media = os.path.join(
    os.path.dirname(__file__),'templates/images/'
)
js_media = os.path.join(
    os.path.dirname(__file__),'templates/js/'
)
fonts_media = os.path.join(
    os.path.dirname(__file__),'templates/fonts/'
)

urlpatterns = patterns('',
    url(r'^$', views.index,name='home.index'),

    url(r'^products', views.products, name='home.products'),
    url(r'^us', views.us, name='home.us'),
    url(r'^bd', views.bd, name='home.bd'),
    url(r'^contact', views.contact, name='home.contact'),
    
    url(r'^images/(?P<path>.*)$','django.views.static.serve',{'document_root': images_media }),
    url(r'^css/(?P<path>.*)$','django.views.static.serve',{'document_root': css_media }),
    url(r'^js/(?P<path>.*)$','django.views.static.serve',{'document_root': js_media }),
    url(r'^fonts/(?P<path>.*)$','django.views.static.serve',{'document_root': fonts_media }),

    url(r'^m/step1', views.m_step1, name='home.m_step1'),
    url(r'^m/step2', views.m_step2, name='home.m_step2'),
    url(r'^m/step3', views.m_step3, name='home.m_step3'),
    
    url(r'^m/privacy', views.m_privacy, name='home.m_privacy'),
    url(r'^m/user', views.m_user, name='home.m_user'),

    url(r'^m/tag/index', views.m_tag_index, name='home.m_tag_index'),
    url(r'^m/tag/list/(\d+)/$', views.m_tag_list, name='home.m_tag_list'),

    # url(r'^aboutus', views.aboutus, name='home.aboutus'),
    # url(r'^join', views.join, name='home.join'),
    # url(r'^contact', views.contact, name='home.contact'),
)
