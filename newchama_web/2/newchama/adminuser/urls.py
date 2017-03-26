from django.conf.urls import patterns, include, url
from adminuser import views

urlpatterns = patterns('',
    url(r'^index', views.index, name='adminuser.index'),
    url(r'^login', views.login, name='adminuser.login'),
    url(r'^logout', views.logout, name='adminuser.logout'),
    url(r'^profile', views.profile, name='adminuser.profile'),
    url(r'^nopermission', views.nopermission, name='adminuser.nopermission'),
    url(r'^changepassword', views.changepassword, name='adminuser.changepassword'),
    url(r'^users/add', views.add_adminuser, name='adminuser.add'),
    url(r'^users/edit/(\d+)', views.edit_adminuser, name='adminuser.edit'),
    url(r'^users/reset_password/(\d+)', views.reset_adminuser_password, name='adminuser.reset_password'),
    url(r'^users/remove', views.remove_adminuser, name='adminuser.remove'),
    url(r'^users', views.adminuser_list, name='adminuser.list'),
    url(r'^roles/add', views.add_role, name='role.add'),
    url(r'^roles/edit/(\d+)', views.edit_role, name='role.edit'),
    url(r'^roles', views.role_list, name='role.list'),
    url(r'^removerole', views.remove_role, name='role.remove'),
    url(r'^newchamasay/add', views.add_newchamasay, name='newchamasay.add'),
    url(r'^newchamasay/edit/(\d+)', views.edit_newchamasay, name='newchamasay.edit'),
    url(r'^newchamasay/remove', views.remove_newchamasay, name='newchamasay.remove'),
    url(r'^newchamasay', views.newchamasay, name='newchamasay.list'),

)
