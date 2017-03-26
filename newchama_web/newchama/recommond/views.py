#encoding:utf-8
import os,sys,datetime
from django.shortcuts import render

from services.models import Project
from services.models import Demand
from recommond.api import GetRecommondScoreItem,CheckDealTypeNotMatching,is_project_score_industry_in_industry,GetProjectRecommondScoreItem
from recommond.models import RecommondItem,PROJECT_SCORE_LEVEL,RecommondProjectItem
from services.models import Company,CompanyInvestmentField,CompanyInvestmentHistory,Member


import logging

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='recommond_error.log',
                filemode='a')



def update_recommond_list(project):

    RecommondItem.objects.exclude(is_in_control_panel=True).filter(is_man=False, project=project).delete()

    company_list_by_field=[company['company'] for company in CompanyInvestmentField.objects.values('company').distinct()]


    company_list_by_listed=[]
    company_list_by_listed=[company.id for company in Company.objects.filter(industry=project.company_industry,type=1)]

    _industry_cv1=0
    if project.company_industry:
        if project.company_industry.level==1:
            _industry_cv1=project.company_industry.id
        elif project.company_industry.level==2:
            _industry_cv1=project.company_industry.father.id
        elif project.company_industry.level==3:
            _industry_cv1=project.company_industry.father.father.id


    company_list_by_invested=[company['company'] for company in CompanyInvestmentHistory.objects.filter(cv1=_industry_cv1).values('company').distinct()]

    company_list_have_demand=[member['member__company'] for member in Demand.objects.exclude(status=5).filter(expire_date__gt=datetime.datetime.now()).values('member__company').distinct()]

    _company_list_id=set(company_list_by_field+company_list_by_listed+company_list_by_invested+company_list_have_demand)

    #排除大米资本
    _company_list_id2=[item for item in _company_list_id if item!=27]

    _company_list=Company.objects.filter(id__in=_company_list_id2,status__lt=2)

    for company in _company_list:
        #print '[*]',CheckDealTypeNotMatching(project,company)

        if not CheckDealTypeNotMatching(project,company):
            _recommond_score=GetRecommondScoreItem(project,company)
            #print company.name_cn
            #print _recommond_score.sum_project_score
            #print _recommond_score.sum_company_score

            if _recommond_score.sum_project_score >0 or _recommond_score.sum_company_score >0 :

                #if _recommond_score.company_score_industry_in_industry>0 or _recommond_score.project_score_industry_in_industry>0:
                member_count=Member.objects.filter(company=company).count()
                if member_count>0:
                    _recommond_score.has_user=True

                #融资项目排除上市公司
                if project.service_type!=2:
                    _recommond_score.save()
                else:
                    company_invest_field_num=CompanyInvestmentField.objects.filter(company=company).count()
                    company_demand_num=Demand.objects.exclude(status=5).filter(member__company=company,expire_date__gt=datetime.datetime.now()).count()
                    if company_invest_field_num>0 or company_demand_num>0:
                        _recommond_score.save()


            del _recommond_score
   


def update_project_recommond_list(demand,project_list):

    RecommondProjectItem.objects.exclude(is_man=True).filter(demand=demand).delete()
    #排除大米资本
    project_list=[project for project in project_list if project.member.company.id !=27]
  
    for project in project_list:

        if is_project_score_industry_in_industry(project,demand):

            _recommond_score=GetProjectRecommondScoreItem(demand,project)

            if _recommond_score.sum_project_score >0:
                #print _recommond_score
                _recommond_score.save()
