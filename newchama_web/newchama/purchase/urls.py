from django.conf.urls import patterns, include, url

from purchase import views

urlpatterns = patterns('',
    url(r'^mydetail/(\d+)/$', views.mydetail, name='purchase.mydetail'),
	url(r'^detail/(\d+)/$', views.detail, name='purchase.detail'),
    url(r'^pdf/(\d+)/$', views.pdf, name='purchase.pdf'),
    url(r'^download_attach/(\d+)/$', views.download_attach, name='purchase.download_attach'),
	url(r'^mylists', views.mylist, {'type': 'release'}, name='purchase.mylist'),
	url(r'^save', views.save, name='purchase.save'),
    #url(r'^mylist/(?P<type>\w+)/(?P<id>\d+)/$', views.mylist, name='purchase.mylist'),
	#url(r'^mylist/(?P<id>\d+)/$', views.mylist, {'type': 'all'}, name='purchase.mylist'),
    #url(r'^mylist_public', views.mylist, {'type': 'public'}, name='purchase.mylist_public'),
	#url(r'^mylist_public/(?P<id>\d+)/$', views.mylist, {'type': 'public'}, name='purchase.mylist_public'),
    #url(r'^mylist_private', views.mylist, {'type': 'private'}, name='purchase.mylist_private'),
    #url(r'^mylist_private/(?P<id>\d+)/$', views.mylist, {'type': 'private'}, name='purchase.mylist_private'),
    url(r'^mylist_release', views.mylist,{'type': 'release'}, name='purchase.mylist_release'),
    url(r'^mylist_pending', views.mylist,{'type': 'pending'}, name='purchase.mylist_pending'),
    url(r'^mylist_expired', views.mylist,{'type': 'expired'},name='purchase.mylist_expired'),
    url(r'^mylist_draft', views.mylist,{'type': 'draft'},name='purchase.mylist_draft'),
    url(r'^mylist_offline', views.mylist,{'type': 'offline'},name='purchase.mylist_offline'),
    url(r'^mylist_not_approved', views.mylist,{'type': 'not_approved'},name='purchase.mylist_not_approved'),
	url(r'^new', views.new, name='purchase.new'),
    url(r'^search_keyword$', views.search_keyword, name='purchase.search_keyword'),
	url(r'^search', views.search, name='purchase.search'),
    url(r'^addsuccess', views.addsuccess, name='purchase.addsuccess'),
    url(r'^add', views.add, name='purchase.add'),
    url(r'^edit/(\d+)/$', views.edit, name='purchase.edit'),
    url(r'^json_index$', views.json_index, name='purchase.json_index'),
    url(r'^delete', views.delete, name='purchase.delete'),
    url(r'^offline', views.offline, name='purchase.offline'),
    url(r'^get_list_for_home', views.get_list_for_home, name='purchase.get_list_for_home'),
    url(r'^ajax_more$', views.ajax_more, name='purchase.ajax_more'),
    url(r'^banking_genius/(\d+)/$', views.banking_genius, name='purchase.banking_genius'),
    url(r'^sync_recommond$', views.sync_recommond, name='purchase.sync_recommond'),
    url(r'^json_recommend$', views.json_recommend, name='purchase.json_recommend'),
    url(r'^json_recommend_count$', views.json_recommend_count, name='purchase.json_recommend_count'),
	#url(r'^$', views.index,name='purchase.index'),
)
