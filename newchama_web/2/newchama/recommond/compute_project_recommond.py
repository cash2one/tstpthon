#encoding:utf-8
import os,sys,datetime
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/adminnewchama/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

from project.models import Project
from demand.models import Demand
from recommond.api import GetRecommondScoreItem,CheckDealTypeNotMatching,is_project_score_industry_in_industry,GetProjectRecommondScoreItem
from recommond.models import RecommondItem,PROJECT_SCORE_LEVEL,RecommondProjectItem
from member.models import Company,CompanyInvestmentField,CompanyInvestmentHistory,Member

import logging

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='recommond_error.log',
                filemode='a')



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

  

if __name__=="__main__":
    try:
        demand_list=Demand.objects.exclude(status=5).filter(expire_date__gt=datetime.datetime.now()).order_by('-id')

        project_list=Project.objects.exclude(status=5).filter(expire_date__gt=datetime.datetime.now()).order_by('-id')

        for demand in demand_list:
            update_project_recommond_list(demand,project_list)
            
            
    except Exception,e:
        
        logging.error(e)
        print e

