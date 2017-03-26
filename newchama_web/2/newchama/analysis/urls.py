#encoding:utf-8
from django.conf.urls import patterns, include, url
from analysis import views, export_user_detail

urlpatterns = patterns('',
    url(r'^project_recommond_view/(\d+)$', views.project_recommond_view, name='analysis.project_recommond_view'),
    url(r'^project_view/(\d+)$', views.project_view, name='analysis.project_view'),
    url(r'^project_fav/(\d+)$', views.project_fav, name='analysis.project_fav'),
    url(r'^project_message/(\d+)$', views.project_message, name='analysis.project_message'),
    url(r'^project_target/(\d+)$', views.project_target, name='analysis.project_target'),
    url(r'^project_finish$', views.project_finish, name='analysis.project_finish'),
    url(r'^project_detail', views.project_detail, name='analysis.project_detail'),

    url(r'^project', views.project, name='analysis.project'),

    url(r'^demand_view/(\d+)$', views.demand_view, name='analysis.demand_view'),
    url(r'^demand_fav/(\d+)$', views.demand_fav, name='analysis.demand_fav'),
    url(r'^demand_message/(\d+)$', views.demand_message, name='analysis.demand_message'),
    url(r'^demand_target/(\d+)$', views.demand_target, name='analysis.demand_target'),
    url(r'^demand_detail', views.demand_detail, name='analysis.demand_detail'),
    url(r'^demand_finish$', views.demand_finish, name='analysis.demand_finish'),
    url(r'^demand', views.demand, name='analysis.demand'),
    url(r'^action_message', views.action_message, name='analysis.action_message'),
    url(r'^action_login', views.action_login, name='analysis.action_login'),
    url(r'^action_publish', views.action_publish, name='analysis.action_publish'),

    url(r'^action', views.action, name='analysis.action'),


    url(r'^user_detail_login/(\d+)$', views.user_detail_login, name='analysis.user_detail_login'),
    url(r'^user_detail_view_project/(\d+)$', views.user_detail_view_project, name='analysis.user_detail_view_project'),
    url(r'^user_detail_view_demand/(\d+)$', views.user_detail_view_demand, name='analysis.user_detail_view_demand'),
    url(r'^user_detail_send_message/(\d+)$', views.user_detail_send_message, name='analysis.user_detail_send_message'),
    url(r'^user_detail_send_project/(\d+)$', views.user_detail_send_project, name='analysis.user_detail_send_project'),
    url(r'^user_detail_send_demand/(\d+)$', views.user_detail_send_demand, name='analysis.user_detail_send_demand'),
    url(r'^user_detail_fav_project/(\d+)$', views.user_detail_fav_project, name='analysis.user_detail_fav_project'),
    url(r'^user_detail_fav_demand/(\d+)$', views.user_detail_fav_demand, name='analysis.user_detail_fav_demand'),
    url(r'^visited_index_user/(\d+)$', views.visited_index_user, name='analysis.visited_index_user'),
    url(r'^message_list$', views.message_list, name='analysis.message_list'),
    

    url(r'^user_more_dim$', export_user_detail.index, name='export_user_detail.index'),
    url(r'^user_weekly_active$', export_user_detail.weekly_active, name='export_user_detail.weekly_active'),
    url(r'^user_weekly_active_detail$', export_user_detail.weekly_active_detail, name='export_user_detail.weekly_active_detail'),
    url(r'^user_detail$', views.user_detail, name='analysis.user_detail'),
    url(r'^user', views.user, name='analysis.user'),
    
    url(r'^send_mail_user/(\d+)$', views.send_mail_user, name='analysis.send_mail_user'),
    url(r'^send_message_noread_mail', views.send_message_noread_mail, name='analysis.send_message_noread_mail'),
    url(r'^send_message_nologin_mail', views.send_message_nologin_mail, name='analysis.send_message_nologin_mail'),
    url(r'^send_message_nopublish_mail', views.send_message_nopublish_mail, name='analysis.send_message_nopublish_mail'),
    
    url(r'^login_user/(\d+)$', views.login_user, name='analysis.login_user'),
    url(r'^active_user/(\d+)$', views.active_user, name='analysis.active_user'),
    url(r'^add_user/(\d+)$', views.add_user, name='analysis.add_user'),
    url(r'^creat_project_user/(\d+)$', views.creat_project_user, name='analysis.creat_project_user'),
    url(r'^creat_demand_user/(\d+)$', views.creat_demand_user, name='analysis.creat_demand_user'),
    url(r'^no_creat_user/(\d+)$', views.no_creat_user, name='analysis.no_creat_user'),
    
    url(r'^index', views.index, name='analysis.index'),
    url(r'^get_collected_number',views.get_collected_number,name='analysis.get_collected_number'),

)
