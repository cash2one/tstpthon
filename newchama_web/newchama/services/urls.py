from django.conf.urls import patterns, include, url
from services import views


urlpatterns = patterns('',
    url(r'^get_industrys/(\d+)$', views.get_industrys, name='services.get_industrys'),
    url(r'^get_provinces/(\d+)', views.get_provinces, name='services.get_provinces'),
    url(r'^get_cities/(\d+)', views.get_cities, name='services.get_cities'),
    url(r'^get_audit_companies/(\w+)', views.get_audit_companies, name='services.get_audit_companies'),
    url(r'^get_listed_companies/(\w+)', views.get_listed_companies, name='services.get_listed_companies'),
    url(r'^get_listed_company/(\d+)', views.get_listed_company, name='services.get_listed_company'),
    url(r'^get_industry/(\d+)$', views.get_industry, name='services.get_industry'),
    


    
    url(r'^upload_message_file$', views.upload_message_file, name='services.upload_message_file'),
    url(r'^upload_file$', views.upload_file, name='services.upload_file'),
    url(r'^getKeywords$', views.getKeywords, name='services.getKeywords'),
    url(r'^get_companies/(\w+)', views.get_companies, name='services.get_companies'),
    url(r'^get_active_companies/(\w+)', views.get_active_companies, name='services.get_active_companies'),
    url(r'^get_active_member/(\w+)', views.get_active_member, name='services.get_active_member'),
    url(r'^get_investment_companies/(\w+)', views.get_investment_companies, name='services.get_investment_companies'),

)
