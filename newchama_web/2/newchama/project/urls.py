from django.conf.urls import patterns, include, url
from project import views

urlpatterns = patterns('',
                    url(r'^$', views.index, name='project.index'),
                    url(r'^list_oneclick$', views.list_oneclick, name='project.list_oneclick'),
                    url(r'^add$', views.add, name='project.add'),
                    url(r'^save', views.save, name='project.save'),
                    url(r'^edit/(\d+)', views.edit, name='project.edit'),
                    url(r'^removeFile$', views.remove_file, name='project.removeFile'),
                    url(r'^check/(\d+)$', views.check, name='project.check'),
                    url(r'^detail/(\d+)$', views.detail, name='project.detail'),
                    url(r'^approve$', views.approve, name='project.approve'),
                    url(r'^ban$', views.ban, name='project.ban'),
                    url(r'^get_members/(\w+)', views.get_members, name='project.get_members'),
                    url(r'^get_companies/(\w+)', views.get_companies, name='project.get_companies'),
                    url(r'^get_company/(\d+)/(\d+)', views.get_company, name='project.get_company'),

                    url(r'^recommend_members/(\d+)$', views.recommend_members, name='project.recommend_members'),
                    url(r'^recommend_member_add/(\d+)$', views.recommend_member_add, name='project.recommend_member_add'),
                    url(r'^recommend_member_detail/(\d+)$', views.recommend_member_detail, name='project.recommend_member_detail'),
                    url(r'^recommend_member_delete/(\d+)$', views.recommend_member_delete, name='project.recommend_member_delete'),
                    url(r'^recommend_member_remove/(\d+)$', views.recommend_member_remove, name='project.recommend_member_remove'),
                    url(r'^recommend_member_star/(\d+)$', views.recommend_member_star, name='project.recommend_member_star'),
                    url(r'^recommend_member_unstar/(\d+)$', views.recommend_member_unstar, name='project.recommend_member_unstar'),
                    url(r'^recommend_member_toprank/(\d+)$', views.recommend_member_toprank, name='project.recommend_member_toprank'),
                    url(r'^recommend_member_uprank/(\d+)$', views.recommend_member_uprank, name='project.recommend_member_uprank'),
                    url(r'^recommend_member_downrank/(\d+)$', views.recommend_member_downrank, name='project.recommend_member_downrank'),

                    url(r'^recommend/(\d+)$', views.recommendCampany, name='project.recommend'),
                    url(r'^recommend_add/(\d+)$', views.recommendCampanyAdd, name='project.recommend_add'),
                    url(r'^recommend_detail/(\d+)$', views.recommendCampanyDetail, name='project.recommend_detail'),
                    url(r'^recommend_delete/(\d+)$', views.recommendCampanyDelete, name='project.recommend_delete'),
                    url(r'^recommend_remove/(\d+)$', views.recommendCampanyRemove, name='project.recommend_remove'),
                    url(r'^recommend_star/(\d+)$', views.recommendCampanyStar, name='project.recommend_star'),
                    url(r'^recommend_unstar/(\d+)$', views.recommendCampanyUnStar, name='project.recommend_unstar'),
                    url(r'^recommend_toprank/(\d+)$', views.recommendCampanyTopRank, name='project.recommend_toprank'),
                    url(r'^recommend_uprank/(\d+)$', views.recommendCampanyUpRank, name='project.recommend_uprank'),
                    url(r'^recommend_downrank/(\d+)$', views.recommendCampanyDownRank, name='project.recommend_downrank'),

                    url(r'^setRecommend$', views.setRecommend, name='project.setRecommend'),
                    url(r'^setTop$', views.setTop, name='project.setTop'),
                    url(r'^cancelRecommend$', views.cancelRecommend, name='project.cancelRecommend'),
                    url(r'^cancelTop$', views.cancelTop, name='project.cancelTop'),
                    url(r'^sync_recommend/(\d+)$', views.sync_recommend, name='project.sync_recommend'),
                    url(r'^genuissave$', views.bankingGenuisSave, name='project.genuissave'),
                    url(r'^genuissavenew$', views.bankingGenuisSaveNew, name='project.genuissavenew'),


                    
)
