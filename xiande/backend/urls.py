#-*-encoding:utf-8-*-
from django.conf.urls import patterns, include, url
from backend import views

urlpatterns = patterns('',

    url(r'^event/bbb$', views.bbb, name='backend.bbb'),
    
    url(r'^event/money_apply_approved/(\d+)$', views.money_apply_approved, name='backend.money_apply_approved'),
    url(r'^event/money_apply_disapproved$', views.money_apply_disapproved, name='backend.money_apply_disapproved'),
    url(r'^event/money_apply_remove$', views.money_apply_remove, name='backend.money_apply_remove'),
    url(r'^event/money_user_remove$', views.money_user_remove, name='backend.money_user_remove'),
    url(r'^event/money_user_list', views.money_user_list, name='backend.money_user_list'),
    url(r'^event/money_user_edit/(\d+)', views.money_user_edit, name='backend.money_user_edit'),
    url(r'^event/money_apply_list', views.money_apply_list, name='backend.money_apply_list'),
    
    url(r'^event/apply_approved$', views.event_apply_approved, name='backend.event_apply_approved'),
    url(r'^event/apply_disapproved$', views.event_apply_disapproved, name='backend.event_apply_disapproved'),
    url(r'^event/apply_remove$', views.event_apply_remove, name='backend.event_apply_remove'),
    url(r'^event/user_remove$', views.event_user_remove, name='backend.event_user_remove'),
    url(r'^event/user_list', views.event_user_list, name='backend.event_user_list'),
    url(r'^event/event_user_edit/(\d+)', views.event_user_edit, name='backend.event_user_edit'),
    
    url(r'^event/apply_list', views.event_apply_list, name='backend.event_apply_list'),

    url(r'^user/apply_approved$', views.apply_approved, name='backend.apply_approved'),
    url(r'^user/apply_disapproved$', views.apply_disapproved, name='backend.apply_disapproved'),
    url(r'^user/apply_remove$', views.apply_remove, name='backend.apply_remove'),
    url(r'^user/income_remove$', views.income_remove, name='backend.income_remove'),
    
    url(r'^user/income_add', views.income_add, name='backend.income_add'),
    url(r'^user/income_edit/(\d+)', views.income_edit, name='backend.income_edit'),
    url(r'^user/income_list', views.income_list, name='backend.income_list'),
    url(r'^user/apply_list', views.apply_list, name='backend.apply_list'),

    url(r'^user/list', views.user_list, name='backend.user_list'),
    url(r'^user/add', views.user_add, name='backend.user_add'),
    
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
