from django.conf.urls import patterns, include, url
from demand import views

urlpatterns = patterns('',
                    url(r'^$', views.index, name='demand.index'),
                    url(r'^add$', views.add, name='demand.add'),
                    url(r'^edit/(\d+)$', views.edit, name='demand.edit'),
                    url(r'^detail/(\d+)$', views.detail, name='demand.detail'),
                    url(r'^check/(\d+)$', views.check, name='demand.check'),
                    url(r'^approve$', views.approve, name='demand.approve'),
                    url(r'^ban$', views.ban, name='demand.ban'),
                    url(r'^save$', views.save, name='demand.save'),

                    url(r'^recommend/(\d+)$', views.recommendProject, name='demand.recommend'),
                    url(r'^recommend_add/(\d+)$', views.recommendProjectAdd, name='demand.recommend_add'),
                    url(r'^recommend_delete/(\d+)$', views.recommendProjectDelete, name='demand.recommend_delete'),
                    url(r'^recommend_remove/(\d+)$', views.recommendProjectRemove, name='demand.recommend_remove'),
                    url(r'^recommend_star/(\d+)$', views.recommendProjectStar, name='demand.recommend_star'),
                    url(r'^recommend_unstar/(\d+)$', views.recommendProjectUnStar, name='demand.recommend_unstar'),
                    url(r'^recommend_toprank/(\d+)$', views.recommendProjectTopRank, name='demand.recommend_toprank'),
                    url(r'^recommend_uprank/(\d+)$', views.recommendProjectUpRank, name='demand.recommend_uprank'),
                    url(r'^recommend_downrank/(\d+)$', views.recommendProjectDownRank, name='demand.recommend_downrank'),
                    url(r'^recommend_detail/(\d+)$', views.recommendProjectDetail, name='demand.recommend_detail'),

                    url(r'^setRecommend$', views.setRecommend, name='demand.setRecommend'),
                    url(r'^setTop$', views.setTop, name='demand.setTop'),
                    url(r'^cancelRecommend$', views.cancelRecommend, name='demand.cancelRecommend'),
                    url(r'^cancelTop$', views.cancelTop, name='demand.cancelTop'),
                    url(r'^sync_recommend/(\d+)$', views.sync_recommend, name='demand.sync_recommend'),
                    
)

