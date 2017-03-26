from django.conf.urls import patterns, include, url

from account import views, other_login

urlpatterns = patterns('',

    url(r'^get_check_code_image',views.get_check_code_image, name='account.get_check_code_image'),
    # url(r'^email_log/(\w+)/(\w+)/(\w+)/(\w+)/$', views.email_log, name='account.email_log'),
    url(r'^email_log/(\w+)/(\w+)/(\w+)/$', views.email_log, name='account.email_log'),
    url(r'^login', views.login, name='account.login'),
	url(r'^logout', views.logout, name='account.logout'),
    
    url(r'^must_change_password', views.must_change_password, name='account.must_change_password'),
    url(r'^active_error', views.active_error, name='account.active_error'),
    url(r'^active', views.active, name='account.active'),
    url(r'^send_active', views.send_active, name='account.send_active'),
    
    url(r'^signup_success_company', views.signup_success_company, name='account.signup_success_company'),
    url(r'^signup_success', views.signup_success, name='account.signup_success'),
    
	url(r'^signup', views.signup, name='account.signup'),
	url(r'^forgot_sendmail_success', views.forgot_sendmail_success, name='account.forgot_sendmail_success'),
    url(r'^forgot_change_success', views.forgot_change_success, name='account.forgot_change_success'),
    url(r'^forgot', views.forgot, name='account.forgot'),
    
	url(r'^profile/(\d+)/$', views.profile, name='account.profile'),
	url(r'^company/(\d+)/$', views.company, name='account.company'),
	url(r'^o_company/(\d+)/(\d+)/$', views.o_company, name='account.o_company'),
	url(r'^invitation', views.invitation, name='account.invitation'),
    url(r'^preference_project_first', views.preference, {'type': 'project', 'isfirst': True}, name='account.preference_project_first'),
    url(r'^preference_project', views.preference, {'type': 'project'}, name='account.preference_project'),
    url(r'^preference_demand_first', views.preference, {'type': 'demand', 'isfirst': True}, name='account.preference_demand_first'),
    url(r'^preference_demand', views.preference, {'type': 'demand'}, name='account.preference_demand'),
    url(r'^preference_news_first', views.preference, {'type': 'news', 'isfirst': True}, name='account.preference_news_first'),
    url(r'^preference_news', views.preference, {'type': 'news'}, name='account.preference_news'),
    url(r'^ajax_preference$', views.ajax_preference, name='account.ajax_preference'),
    url(r'^ajax_preference_remove', views.ajax_preference_remove, name='account.ajax_preference_remove'),
    url(r'^ajax_preference_news', views.ajax_preference_news, name='account.ajax_preference_news'),
    url(r'^setting_first', views.setting,{ 'isfirst': True}, name='account.setting_first'),
	url(r'^setting', views.setting, name='account.setting'),
    url(r'^focus_first', views.focus, {'isfirst': True}, name='account.focus_first'),
    url(r'^changepassword', views.changepassword, name='account.changepassword'),

	url(r'^notifications_read', views.notifications,{'message_type':'read'} ,name='account.notifications_read'),
	url(r'^notifications_send', views.notifications,{'message_type':'send'} ,name='account.notifications_send'),
	url(r'^notifications$', views.notifications,{'message_type':'unread'} ,name='account.notifications'),
	url(r'^notification/(\w+)/(\d+)/(\d+)/$', views.notifications, name='account.notification'),
    
    url(r'^messages_project', views.message_center,{'sort_type':'project'} ,name='account.messages_project'),
    url(r'^messages_person', views.message_center,{'sort_type':'person'} ,name='account.messages_person'),
    url(r'^messages$', views.message_center,{'sort_type':'project'} ,name='account.messages'),
    url(r'^ajax_message_center_person_more/(\d+)/(\d+)/$', views.ajax_message_center_person_more, name='account.ajax_message_center_person_more'),
    url(r'^search_keyword_message$', views.search_keyword_message, name='account.search_keyword_message'),

    url(r'^ajax_search_message_more/(\d+)/(\d+)/$', views.ajax_search_message_more, name='account.ajax_search_message_more'),




	url(r'^ajax_notifications', views.ajax_notifications, name='account.ajax_notifications'),
	url(r'^send_invitecode', views.send_invitecode,name='account.send_invitecode'),

	url(r'^get_new_message_num', views.get_new_message_num, name='account.get_new_message_num'),
	url(r'^get_new_message_html', views.get_new_message_html, name='account.get_new_message_html'),
    
	url(r'^get_new_message_by_id', views.get_new_message_by_id, name='account.get_new_message_by_id'),
    url(r'^get_new_message', views.get_new_message, name='account.get_new_message'),
	url(r'^send_message', views.send_message, name='account.send_message'),
	url(r'^read_message', views.read_message, name='account.read_message'),
    
    url(r'^remove_message_person_all', views.remove_message_person_all, name='account.remove_message_person_all'), 
    url(r'^remove_message_person', views.remove_message_person, name='account.remove_message_person'),

    
    url(r'^remove_message_project_all', views.remove_message_project_all, name='account.remove_message_project_all'),
    url(r'^remove_message_project', views.remove_message_project, name='account.remove_message_project'),
    url(r'^remove_message_demand$', views.remove_message_demand, name='account.remove_message_demand'),
	url(r'^remove_message$', views.remove_message, name='account.remove_message'),
    url(r'^reset_password/(.+)/(.+)', views.reset_password, name='account.reset_password'),
    url(r'^avatar/(?P<width>\d+)/(?P<height>\d+)/(?P<file_name>.+)$', views.get_logo,{'type':'avatar'}, name='account.avatar'),
    url(r'^logo/(?P<width>\d+)/(?P<height>\d+)/(?P<file_name>.+)$', views.get_logo,{'type':'logo'}, name='account.logo'),

    url(r'^$', views.index, name='account.index'),
    url(r'^ajax_project', views.ajax_project, name='account.ajax_project'),
    url(r'^myfavorite_member', views.myfavorite, {'type': 'member'}, name='account.myfavorite_member'),
    url(r'^myfavorite_data', views.myfavorite, {'type': 'data'}, name='account.myfavorite_data'),
    url(r'^myfavorite_company', views.myfavorite, {'type': 'company'}, name='account.myfavorite_company'),
    url(r'^myfavorite_demand', views.myfavorite, {'type': 'demand'}, name='account.myfavorite_demand'),
    url(r'^myfavorite_news', views.myfavorite, {'type': 'news'}, name='account.myfavorite_news'),
    url(r'^myfavorite', views.myfavorite, {'type': 'project'}, name='account.myfavorite'),
    url(r'^add_member_to_favorite', views.addfavorite, {'type': 'member'}, name='account.add_member_to_favorite'),
    url(r'^add_data_to_favorite', views.addfavorite, {'type': 'data'}, name='account.add_data_to_favorite'),
    url(r'^add_company_to_favorite', views.addfavorite, {'type': 'company'}, name='account.add_company_to_favorite'),
    url(r'^add_demand_to_favorite', views.addfavorite, {'type': 'demand'}, name='account.add_demand_to_favorite'),
    url(r'^add_news_to_favorite', views.addfavorite, {'type': 'news'}, name='account.add_news_to_favorite'),
    url(r'^add_project_to_favorite', views.addfavorite, {'type': 'project'}, name='account.add_project_to_favorite'),
    url(r'^remove_member_from_favorite', views.removefavorite, {'type': 'member'}, name='account.remove_member_from_favorite'),
    url(r'^remove_data_from_favorite', views.removefavorite, {'type': 'data'}, name='account.remove_data_from_favorite'),
    url(r'^remove_company_from_favorite', views.removefavorite, {'type': 'company'}, name='account.remove_company_from_favorite'),
    url(r'^remove_demand_from_favorite', views.removefavorite, {'type': 'demand'}, name='account.remove_demand_from_favorite'),
    url(r'^remove_news_from_favorite', views.removefavorite, {'type': 'news'}, name='account.remove_news_from_favorite'),
    url(r'^remove_project_from_favorite', views.removefavorite, {'type': 'project'}, name='account.remove_project_from_favorite'),
    #url(r'^search_keyword_company/(\w+)', views.search_keyword_company, name='account.search_keyword_company'),
    #url(r'^search_keyword_member/(\w+)', views.search_keyword_member, name='account.search_keyword_member'),
    #url(r'^search_company', views.search_company, name='account.search_company'),
    #url(r'^search_member', views.search_member, name='account.search_member'),
    url(r'^first_step1', views.first_confirm, name='account.first_step1'),
    url(r'^privacy', views.privacy, name='account.privacy'),
    url(r'^user', views.user, name='account.user'),
    url(r'^ajax_more_favorite', views.ajax_more_favorite, name='account.ajax_more_favorite'),
    url(r'^gohome', views.gohome, name='account.gohome'),
    url(r'^json_dynamic', views.json_dynamic, name='account.json_dynamic'),

    url(r'^weibo', other_login.weibo, name='other_login.weibo'),
    url(r'^signin', other_login.signin, name='other_login.signin'),
    url(r'^other_first', other_login.first, name='other_login.first'),

)

