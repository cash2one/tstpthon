from django.conf.urls import patterns, include, url
from repository import views

urlpatterns = patterns('',
                    url(r'^get_listed_companies/(\w+)', views.get_listed_companies, name='repository.get_listed_companies'),
                    url(r'^get_audit_companies/(\w+)', views.get_audit_companies, name='repository.get_audit_companies'),
                    url(r'^get_listed_company/(\d+)', views.get_listed_company, name='repository.get_listed_company'),
                    url(r'^keywords$', views.keywords, name='repository.keywords'),
                    url(r'^addKeyword$', views.addKeyword, name='repository.addKeyword'),
                    url(r'^editKeyword/(\d+)', views.editKeyword, name='repository.editKeyword'),
                    url(r'^getKeywords$', views.getKeywords, name='repository.getKeywords'),
                    url(r'^get_investment_companies/(\w+)', views.get_investment_companies, name='repository.get_investment_companies'),
                    url(r'^get_investment_company/(\d+)', views.get_investment_company, name='repository.get_investment_company'),
                    url(r'^get_active_companies/(\w+)', views.get_active_companies, name='repository.get_active_companies'),
                    url(r'^get_active_member/(\w+)', views.get_active_member, name='services.get_active_member'),
)

