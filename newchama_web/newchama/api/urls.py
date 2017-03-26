from django.conf.urls import patterns, include, url
from django.conf import settings
from rest_framework import routers
from api import views

router = routers.DefaultRouter()#trailing_slash=False)
#router.register(r'country',views.CountryViewSet)
#router.register(r'login',views.LoginViewSet)
#router.register(r'reg',views.regViewSet)


urlpatterns = patterns('',
   url(r'^', include(router.urls)),
   url(r'login', views.login),
   url(r'other_way_login',views.other_way_login),
   url(r'register',views.register),
   url(r'get_valid_code',views.get_valid_code),
   url(r'user_identify',views.user_identify),
   url(r'get_dynamic_msg_list',views.get_dynamic_msg_list),
   url(r'get_user_detail',views.get_user_detail),
   url(r'focus_user',views.focus_user),
   url(r'get_user_publish_pro_list',views.get_user_publish_pro_list),
   url(r'get_user_care_pro_list',views.get_user_care_pro_list),
   url(r'get_user_care_mem_list',views.get_user_care_mem_list),
   url(r'get_pro_detail',views.get_pro_detail),
   url(r'send_msg_to_publisher',views.send_msg_to_publisher),
   url(r'define_pro_not_proper',views.define_pro_not_proper),
   url(r'get_pro_and_demand_list',views.get_pro_and_demand_list),
   url(r'get_target_pro_list',views.get_target_pro_list),
   url(r'get_target_demand_list',views.get_target_demand_list),
   url(r'get_keyword_search_pro_list',views.get_keyword_search_pro_list),
   url(r'pro_share',views.pro_share),
   url(r'get_pro_msg_list',views.get_pro_msg_list),
   url(r'get_friends_list',views.get_friends_list),
   url(r'get_pro_teaser_list',views.get_pro_teaser_list),
   url(r'get_upload_file_list',views.get_upload_file_list),
   url(r'get_personal_detail',views.get_personal_detail),
   url(r'get_personal_publish_pro_list',views.get_personal_publish_pro_list),
   url(r'get_personal_care_pro_list',views.get_personal_care_pro_list),
   url(r'get_personal_company_detail',views.get_personal_company_detail),
   url(r'genius_company_list',views.genius_company_list),
   url(r'genius_get_filter_buyer_list',views.genius_get_filter_buyer_list),
   url(r'genius_company_operation',views.genius_company_operation),
   url(r'get_controlboard_list',views.get_controlboard_list),
   url(r'get_controlboard_recent_view_pro_list',views.get_controlboard_recent_view_pro_list),
   url(r'focus_pro',views.focus_pro),
   url(r'get_controlboard_recent_focuspro_list',views.get_controlboard_recent_focuspro_list),
   url(r'controlboard_company_operation',views.controlboard_company_operation),
   url(r'get_newbuyer_list',views.get_newbuyer_list),
   url(r'send_pro_to_inneruser',views.send_pro_to_inneruser),
   url(r'send_pro_to_outerser',views.send_pro_to_outerser),
   url(r'focus_aspect_setting',views.focus_aspect_setting),
   url(r'get_focus_aspect_list',views.get_focus_aspect_list),
   url(r'get_hot_tag_list',views.get_hot_tag_list),
   # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

