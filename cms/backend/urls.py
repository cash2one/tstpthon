#-*-encoding:utf-8-*-
from django.conf.urls import patterns, include, url
from backend import views

urlpatterns = patterns('',

    url(r'^user/list', views.user_list, name='backend.user_list'),
    url(r'^user/add', views.user_add, name='backend.user_add'),
    url(r'^user/detail/(\d+)', views.user_detail, name='backend.user_detail'),
    url(r'^user/edit/(\d+)', views.user_edit, name='backend.user_edit'),
    url(r'^user/reset_password/(\d+)', views.user_reset_password, name='backend.user_reset_password'),
    url(r'^user/remove', views.user_remove, name='backend.user_remove'),

    url(r'^admin/list', views.admin_list, name='backend.admin_list'),
    url(r'^admin/add', views.admin_add, name='backend.admin_add'),
    url(r'^admin/detail/(\d+)', views.admin_detail, name='backend.admin_detail'),
    url(r'^admin/edit/(\d+)', views.admin_edit, name='backend.admin_edit'),
    url(r'^admin/reset_password/(\d+)', views.admin_reset_password, name='backend.admin_reset_password'),
    url(r'^admin/remove', views.admin_remove, name='backend.admin_remove'),

    url(r'^profile', views.profile, name='backend.profile'),
    url(r'^change_password', views.change_password, name='backend.change_password'),
    url(r'^signin', views.signin, name='backend.signin'),
    url(r'^signout', views.signout, name='backend.signout'),
    url(r'^index', views.index, name='backend.index'),
    url(r'^$', views.index, name='backend.index'),

)
