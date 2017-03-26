#encoding:utf-8
import os,sys,datetime
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

from project.models import Project,ProjectCustomerTargetCompany
from demand.models import Demand
from recommond.api import GetRecommondScoreItem
from recommond.models import RecommondItem,PROJECT_SCORE_LEVEL
from member.models import Company,CompanyInvestmentField,CompanyInvestmentHistory,Member


old_list=ProjectCustomerTargetCompany.objects.filter(is_man=1,is_delete=0)

print old_list

for item in old_list:
    print item.project.id
    print item.company_name_cn

    rec_num=RecommondItem.objects.filter(project=item.project,company__name_cn=item.company_name_cn).count()
    if rec_num>0:
        rec=RecommondItem.objects.filter(project=item.project,company__name_cn=item.company_name_cn).first()
        
    else:
        rec=RecommondItem()
        rec.project=item.project
        rec.company=Company.objects.filter(name_cn=item.company_name_cn).first()
    rec.is_man=1
    rec.is_star=item.is_star
    rec.rank=item.rank
    rec.target_reason=item.target_reason
    rec.save()




    