#encoding:utf-8
import os,sys,datetime
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/adminnewchama/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

from project.models import Project
from demand.models import Demand,DemandIndustry
from recommond.mem_api import GetRecommondScoreItem,CheckDealTypeNotMatching
from recommond.models import RecommondItem,PROJECT_SCORE_LEVEL
from member.models import Company,CompanyInvestmentField,CompanyInvestmentHistory,Member
from project.models import Project,ProjectKeyword,ProjectKeywordAdmin

import logging

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='recommond_error.log',
                filemode='a')

database={}
database['RECOMMONDITEM']=list(RecommondItem.objects.all())
database['COMPANYINVESTMENTHISTORY']=list(CompanyInvestmentHistory.objects.all())
'''


database['DEMAND']=list(Demand.objects.all())
database['COMPANY']=list(Company.objects.all())
database['MEMBER']=list(Member.objects.all())
database['PROJECTKEYWORD']=list(ProjectKeyword.objects.all())
database['PROJECTKEYWORDADMIN']=list(ProjectKeywordAdmin.objects.all())
database['DEMANDINDUSTRY']=list(DemandIndustry.objects.all())
database['COMPANYINVESTMENTFIELD']=list(CompanyInvestmentField.objects.all())
'''



def update_recommond_list(project):

    RecommondItem.objects.exclude(is_man=True).filter(project=project).delete()

    company_list_by_field=[company['company'] for company in database['COMPANYINVESTMENTHISTORY'].values('company').distinct()]
    
    company_list_by_listed=[company.id for company in database['COMPANY'].filter(industry=project.company_industry,type=1)]
    
    if project.company_industry.level==1:
        _industry_cv1=project.company_industry.id
    elif project.company_industry.level==2:
        _industry_cv1=project.company_industry.father.id
    elif project.company_industry.level==3:
        _industry_cv1=project.company_industry.father.father.id
    else:
        _industry_cv1=0
    
    company_list_by_invested=[company['company'] for company in database['COMPANYINVESTMENTHISTORY'].filter(cv1=_industry_cv1).values('company').distinct()]
    
    company_list_have_demand=[member['member__company'] for member in database['DEMAND'].exclude(status=5).filter(expire_date__gt=datetime.datetime.now()).values('member__company').distinct()]
    
    _company_list_id=set(company_list_by_field+company_list_by_listed+company_list_by_invested+company_list_have_demand)

    #排除大米资本
    _company_list_id2=[item for item in _company_list_id if item!=27]

    _company_list=database['COMPANY'].filter(id__in=_company_list_id2,status__lt=2)
    
    for company in _company_list:
        #print '[*]',CheckDealTypeNotMatching(project,company)

        if not CheckDealTypeNotMatching(project,company,database):
            _recommond_score=GetRecommondScoreItem(project,company,database)        
            #print company.name_cn
            #print _recommond_score.sum_project_score
            #print _recommond_score.sum_company_score

            if _recommond_score.sum_project_score >0 or _recommond_score.sum_company_score >0 :
                member_count=database['MEMBER'].filter(company=company).count()
                if member_count>0:
                    _recommond_score.has_user=True

                _recommond_score.save()
   


  

if __name__=="__main__":

    try:
        print database['RECOMMONDITEM']
        print database['COMPANYINVESTMENTHISTORY']
        
        
        '''
        project_list=Project.objects.all().order_by('-id')[:100]
        #print project_list

        for project in project_list:
            #print project.name_cn
            update_recommond_list(project)
        '''
    except Exception,e:
        print e
        logging.error(e)

