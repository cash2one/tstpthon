#encoding:utf-8
import os,sys,datetime
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/adminnewchama/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
import traceback
from project.models import Project
from demand.models import Demand
from recommond.api import GetRecommondScoreItem, CheckDealTypeNotMatching, CheckDealSizeNotMatching, CheckDealCurrencyNotMatching
from recommond.models import RecommondItem,PROJECT_SCORE_LEVEL
from member.models import Company,CompanyInvestmentField,CompanyInvestmentHistory,Member

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

        if not CheckDealTypeNotMatching(project,company) and \
           not CheckDealSizeNotMatching(project, company) and \
           not CheckDealCurrencyNotMatching(project, company):
            _recommond_score=GetRecommondScoreItem(project, company)
            #print company.name_cn
            #print _recommond_score.sum_project_score
            #print _recommond_score.sum_company_score

            #if _recommond_score.company_score_industry_in_industry>0 or _recommond_score.project_score_industry_in_industry>0:
            if _recommond_score.sum_project_score >0 or _recommond_score.sum_company_score >0 :
                if _recommond_score.company_score_industry_in_industry == 0 and \
                   _recommond_score.company_score_industry_keyword == 0 and \
                   _recommond_score.company_score_industry_invest_industry_one == 0 and \
                   _recommond_score.company_score_industry_invest_industry_two == 0:
                    pass
                else:
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



  

if __name__=="__main__":

    try:
         
        project_list=Project.objects.exclude(status=5).order_by('-id')[:20]
        #print project_list

        for project in project_list:
            #print project.name_cn
            update_recommond_list(project)

    except Exception,e:
        traceback.print_exc()
        logging.error(e)

