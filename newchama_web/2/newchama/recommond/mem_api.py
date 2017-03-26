#encoding:utf-8
from recommond.models import RECOMMONWEIGHT,RecommondItem,PROJECT_SCORE_LEVEL,TOTAL_SCORE,RECOMMONPROJECTWEIGHT,RecommondProjectItem
from project.models import Project,ProjectKeyword,ProjectKeywordAdmin
from member.models import CompanyInvestmentField,Company,CompanyInvestmentHistory
from member.views import convert_finance_type_to_num,convert_growth_type_to_num
from demand.models import Demand,DemandIndustry
import datetime


def is_company_score_industry_in_industry(project,company):
    _is_ok=False
    if project.company_industry:
        
        if company.industry == project.company_industry:
            _is_ok = True
    return _is_ok

def is_company_score_industry_invest_industry_one(project,company,database):
    _is_ok=False
    if project.company_industry:
        if project.company_industry.level==1:
            _industry_cv1=project.company_industry.id
        elif project.company_industry.level==2:
            _industry_cv1=project.company_industry.father.id
        elif project.company_industry.level==3:
            _industry_cv1=project.company_industry.father.father.id
        else:
            _industry_cv1=0
        _num=database['COMPANYINVESTMENTHISTORY'].filter(company=company,cv1=_industry_cv1).count()
        if _num>0:
            _is_ok = True
    return _is_ok

def is_company_score_industry_invest_industry_two(project,company,database):
    _is_ok=False
    if project.company_industry:
        if project.company_industry.level==1:
            _industry_cv2=0
        elif project.company_industry.level==2:
            _industry_cv2=project.company_industry.father.id
        elif project.company_industry.level==3:
            _industry_cv2=project.company_industry.father.id
        else:
            _industry_cv2=0
        _num=database['COMPANYINVESTMENTHISTORY'].filter(company=company,cv2=_industry_cv2).count()
        if _num>0:
            _is_ok = True
    return _is_ok

def is_company_score_industry_keyword(project,company_invest_field,database):
    _is_ok=False
    project_kv_list = database['PROJECTKEYWORD'].filter(project=project)
    project_admin_kv_list = database['PROJECTKEYWORDADMIN'].filter(project=project)
    
    for p_kv_item in project_kv_list+project_admin_kv_list:
        if company_invest_field.tags:
            if p_kv_item.keyword in company_invest_field.tags:
                _is_ok = True
    return _is_ok


def is_company_score_deal_type(project,company_invest_field):   
    _is_ok=False
    if company_invest_field.deal_type == 99:
        _is_ok = True
    
    if company_invest_field.deal_type == 1 and project.service_type == 4:
        _is_ok = True

    if company_invest_field.deal_type == 2 and project.service_type == 4:
        _is_ok = True

    if company_invest_field.deal_type == 4 and project.service_type == 1:
        _is_ok = True

    if company_invest_field.deal_type == 4 and project.service_type == 2:
        _is_ok = True

    if company_invest_field.deal_type == project.service_type:
        _is_ok = True

    return _is_ok


def is_company_score_deal_size(project,company_invest_field):
    _is_ok=False
    if project.deal_size:
        if project.deal_size>=company_invest_field.deal_size_min and project.deal_size <=company_invest_field.deal_size_max:
            _is_ok = True
    return _is_ok


def is_company_score_currency_sure(project,company_invest_field):
    _is_ok=False
    if project.currency_type_financial ==company_invest_field.deal_currency:
        _is_ok = True
    return _is_ok


def is_company_score_currency_not_sure(project,company_invest_field):
    _is_ok=False
    if company_invest_field.deal_currency==99:
        _is_ok = True
    return _is_ok

def is_company_score_finance_revenue(project,company_invest_field):
    num_min,num_max=convert_finance_type_to_num(company_invest_field.revenue)
    _is_ok=False
    if project.income:
        if project.income>=num_min and project.income <=num_max:
            _is_ok = True
    return _is_ok
#todo
def is_company_score_finance_growth(project,company_invest_field):
    num_min,num_max=convert_growth_type_to_num(company_invest_field.growth)
    _is_ok=False
    if project.growth_three_year:
        if project.growth_three_year>=num_min and project.growth_three_year <=num_max:
            _is_ok = True
    return _is_ok

def is_company_score_finance_net_income(project,company_invest_field):
    num_min,num_max=convert_finance_type_to_num(company_invest_field.net_income)
    _is_ok=False
    if project.profit:
        if project.profit>=num_min and project.profit <=num_max:
            _is_ok = True
    return _is_ok


def is_company_score_finance_ebitda(project,company_invest_field):
    num_min,num_max=convert_finance_type_to_num(company_invest_field.ebita)
    _is_ok=False
    if project.profit:
        if project.ebitda>=num_min and project.ebitda <=num_max:
            _is_ok = True
    return _is_ok

def is_company_score_local(project,company_invest_field):
    _is_ok=False
    if project.company_country:
        if project.company_country == company_invest_field.country:
            _is_ok=True
    return _is_ok



def is_project_score_industry_keyword(project,demand,database):
    _is_ok=False
    project_kv_list = database['PROJECTKEYWORD'].filter(project=project)
    for p_kv_item in project_kv_list:
        if p_kv_item.keyword in demand.name_cn:
            _is_ok = True
        if p_kv_item.keyword in demand.name_en:
            _is_ok = True

    return _is_ok

def is_project_score_industry_in_industry(project,demand,database):
    _is_ok=False
    if project.company_industry:

        demand_industry_list=database['DEMANDINDUSTRY'].filter(demand=demand)
        for _industry in demand_industry_list:
            if project.company_industry.level==1:
                _cv=project.company_industry.id
            elif project.company_industry.level==2:
                _cv=project.company_industry.father.id
            elif project.company_industry.level==3:
                _cv=project.company_industry.father.father.id
            else:
                _cv=0
            if _industry.cv1==_cv:
                _is_ok=True

    return _is_ok

    
def is_project_score_deal_type(project,demand):
    _is_ok=False
    if project.service_type:

        if demand.service_type ==0:
            _is_ok=True
       
        if demand.service_type == 1 and project.service_type == 4:
            _is_ok = True

        if demand.service_type == 2 and project.service_type == 4:
            _is_ok = True

        if demand.service_type == 4 and project.service_type == 1:
            _is_ok = True

        if demand.service_type == 4 and project.service_type == 2:
            _is_ok = True

        if project.service_type==demand.service_type:
            _is_ok=True


    return _is_ok


def is_project_score_deal_size(project,demand):
    num_min,num_max=convert_demand_finance_type_to_num(demand.deal_size)
    _is_ok=False
    if project.deal_size:
        if project.deal_size>=num_min and project.deal_size <=num_max:
            _is_ok=True
    return _is_ok

def is_project_score_currency_sure(project,demand):
    _is_ok=False
    if project.currency_type_financial:
        if project.currency_type_financial==demand.currency_type_financial:
            _is_ok=True
    return _is_ok

def is_project_score_currency_not_sure(project,demand):
    _is_ok=False
    if demand.currency_type_financial==0:
        _is_ok = True
    return _is_ok

def is_project_score_finance_revenue(project,demand):
    num_min,num_max=convert_demand_finance_type_to_num(demand.income)
    _is_ok=False
    if project.income:
        if project.income>=num_min and project.income <=num_max:
            _is_ok=True
    return _is_ok
    

def is_project_score_finance_growth(project,demand):
    
    _is_ok=False
    if project.growth_three_year and demand.growth_three_year:
        num_min=float(demand.growth_three_year)*0.5
        num_max=float(demand.growth_three_year)*1.5
        if project.growth_three_year>=num_min and project.growth_three_year <=num_max:
            _is_ok=True
    return _is_ok

def is_project_score_finance_net_income(project,demand):
    num_min,num_max=convert_demand_finance_type_to_num(demand.profit)
    _is_ok=False
    if project.profit:
        if project.profit>=num_min and project.profit <=num_max:
            _is_ok=True
    return _is_ok

#买方需求中没有ebitda
def is_project_score_finance_ebitda(project,demand):    
    _is_ok=False
    return _is_ok

def is_project_score_local(project,demand):
    _is_ok=False
    if project.company_country in demand.company_countries.all():
        _is_ok=True
    return _is_ok


def CheckDealTypeNotMatching(project,company,database):
    _is_ok=False
    company_demand_list=database['DEMAND'].exclude(status=5).filter(member__company=company,expire_date__gt=datetime.datetime.now())
    if company_demand_list.count()>0:
        _is_ok=True

        for _demand in company_demand_list:
            if is_project_score_deal_type(project,_demand)>0:
                _is_ok=False

    company_invest_field_list=database['COMPANYINVESTMENTFIELD'].filter(company=company)
    if company_invest_field_list.count()>0:
        _is_ok=True
        for _field in company_invest_field_list:
            if is_company_score_deal_type(project,_field)>0:
                _is_ok=False


    return _is_ok



#计算需求与项目的推荐分数
def GetProjectRecommondScoreItem(demand,project):
    total_score=TOTAL_SCORE
    _recommond_score_num=RecommondProjectItem.objects.filter(demand=demand,project=project).count()
    if _recommond_score_num>0:
        _recommond_score=RecommondProjectItem.objects.filter(demand=demand,project=project).first()
    else:
        _recommond_score = RecommondProjectItem()
        _recommond_score.project=project
        _recommond_score.demand=demand
    
    sum_project_score = 0
    score_industry_in_industry = 0
    score_deal_type = 0
    score_deal_size = 0
    score_currency = 0
    score_finance_revenue = 0
    score_finance_growth = 0
    score_finance_net_income = 0
    score_finance_ebitda = 0
    score_local = 0

    if is_project_score_industry_in_industry(project,demand,database):
        score_industry_in_industry=total_score*RECOMMONPROJECTWEIGHT['industry']

    
    if is_project_score_deal_type(project,demand):
        score_deal_type=total_score*RECOMMONPROJECTWEIGHT['deal_type']

    if is_project_score_deal_size(project,demand):
        score_deal_size=total_score*RECOMMONPROJECTWEIGHT['deal_size']

    if is_project_score_currency_sure(project,demand):
        score_currency=total_score*RECOMMONPROJECTWEIGHT['currency']*RECOMMONPROJECTWEIGHT['currency_sure']
    elif is_project_score_currency_not_sure(project,demand):
        score_currency=total_score*RECOMMONPROJECTWEIGHT['currency']*RECOMMONPROJECTWEIGHT['industry_not_sure']

    if is_project_score_finance_revenue(project,demand):
        score_finance_revenue=total_score*RECOMMONPROJECTWEIGHT['finance']*RECOMMONPROJECTWEIGHT['finance_revenue'] 

    if is_project_score_finance_growth(project,demand):
        score_finance_growth=total_score*RECOMMONPROJECTWEIGHT['finance']*RECOMMONPROJECTWEIGHT['finance_growth'] 

    if is_project_score_finance_net_income(project,demand):
        score_finance_net_income=total_score*RECOMMONPROJECTWEIGHT['finance']*RECOMMONPROJECTWEIGHT['finance_net_income'] 

    if is_project_score_finance_ebitda(project,demand):
        score_finance_ebitda=total_score*RECOMMONPROJECTWEIGHT['finance']*RECOMMONPROJECTWEIGHT['finance_ebitda'] 

    if is_project_score_local(project,demand):
        score_local=total_score*RECOMMONPROJECTWEIGHT['local']

    sum_project_score=score_industry_in_industry+score_deal_type+score_deal_size+score_currency+score_finance_revenue+score_finance_growth+score_finance_net_income+score_finance_ebitda+score_local
    
    _recommond_score.sum_project_score = sum_project_score

    _recommond_score.project_score_industry_in_industry = score_industry_in_industry
    _recommond_score.project_score_deal_type = score_deal_type
    _recommond_score.project_score_deal_size = score_deal_size
    _recommond_score.project_score_currency = score_currency
    _recommond_score.project_score_finance_growth = score_finance_growth
    _recommond_score.project_score_finance_net_income = score_finance_net_income
    _recommond_score.project_score_finance_ebitda = score_finance_ebitda
    _recommond_score.project_score_local = score_local


    return _recommond_score





#计算公司推荐分数
def GetRecommondScoreItem(project,company,database):

    _recommond_score_num=database['RECOMMONDITEM'].filter(company=company,project=project).count()
    if _recommond_score_num>0:
        _recommond_score=database['RECOMMONDITEM'].filter(company=company,project=project).first()
    else:
        _recommond_score = RecommondItem()
        _recommond_score.project=project
        _recommond_score.company=company
    ComputerProjectRecommondScore(project,company,_recommond_score,database)

    ComputerCompanyRecommondScore(project,company,_recommond_score,database)

    #设定一个阈值，减少不必要的计算
    if _recommond_score.sum_project_score>PROJECT_SCORE_LEVEL:
        _recommond_score.target_reason = 'relate buy-side mandate' #有相关需求

    _recommond_score.sum_score=_recommond_score.sum_project_score+_recommond_score.sum_company_score
    return _recommond_score



#计算公司下面的项目分数
def ComputerProjectRecommondScore(project,company,score_item,database):
    current_max_score=0
    total_score=TOTAL_SCORE

    company_demand_list=database['DEMAND'].exclude(status=5).filter(member__company=company,expire_date__gt=datetime.datetime.now())
    for _demand in company_demand_list:
        sum_project_score = 0
        score_industry_keyword = 0
        score_industry_in_industry = 0
        score_industry_invest_industry_one = 0
        score_industry_invest_industry_two = 0
        score_deal_type = 0
        score_deal_size = 0
        score_currency = 0
        score_finance_revenue = 0
        score_finance_growth = 0
        score_finance_net_income = 0
        score_finance_ebitda = 0
        score_local = 0

        
        if is_project_score_industry_keyword(project,_demand,database):
            score_industry_keyword=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_keyword']
        
        elif is_project_score_industry_in_industry(project,_demand,database):
            score_industry_in_industry=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_in_industry']

       
        if is_project_score_deal_type(project,_demand):
            score_deal_type=total_score*RECOMMONWEIGHT['deal_type']

        if is_project_score_deal_size(project,_demand):
            score_deal_size=total_score*RECOMMONWEIGHT['deal_size']

        if is_project_score_currency_sure(project,_demand):
            score_currency=total_score*RECOMMONWEIGHT['currency']*RECOMMONWEIGHT['currency_sure']
        elif is_project_score_currency_not_sure(project,_demand):
            score_currency=total_score*RECOMMONWEIGHT['currency']*RECOMMONWEIGHT['industry_not_sure']

        if is_project_score_finance_revenue(project,_demand):
            score_finance_revenue=total_score*RECOMMONWEIGHT['finance']*RECOMMONWEIGHT['finance_revenue'] 

        if is_project_score_finance_growth(project,_demand):
            score_finance_growth=total_score*RECOMMONWEIGHT['finance']*RECOMMONWEIGHT['finance_growth'] 

        if is_project_score_finance_net_income(project,_demand):
            score_finance_net_income=total_score*RECOMMONWEIGHT['finance']*RECOMMONWEIGHT['finance_net_income'] 

        if is_project_score_finance_ebitda(project,_demand):
            score_finance_ebitda=total_score*RECOMMONWEIGHT['finance']*RECOMMONWEIGHT['finance_ebitda'] 

        if is_project_score_local(project,_demand):
            company_score_local=total_score*RECOMMONWEIGHT['local']

        sum_project_score=score_industry_keyword+score_industry_in_industry+score_industry_invest_industry_one+score_industry_invest_industry_two+score_deal_type+score_deal_size+score_currency+score_finance_revenue+score_finance_growth+score_finance_net_income+score_finance_ebitda+score_local
        
        if sum_project_score>current_max_score:
            current_max_score=sum_project_score
            
            score_item.sum_project_score = sum_project_score
            score_item.project_score_industry_keyword = score_industry_keyword
            score_item.project_score_industry_in_industry = score_industry_in_industry
            score_item.project_score_deal_type = score_deal_type
            score_item.project_score_deal_size = score_deal_size
            score_item.project_score_currency = score_currency
            score_item.project_score_finance_revenue = score_finance_revenue
            score_item.project_score_finance_growth = score_finance_growth
            score_item.project_score_finance_net_income = score_finance_net_income
            score_item.project_score_finance_ebitda = score_finance_ebitda
            score_item.project_score_local = score_local

#计算公司分数
def ComputerCompanyRecommondScore(project,company,score_item,database):
    current_max_score=0
    total_score=TOTAL_SCORE

    score_industry_in_industry = 0
    score_industry_invest_industry_one = 0
    score_industry_invest_industry_two = 0

    if is_company_score_industry_in_industry(project,company):

        
        score_industry_in_industry=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_in_industry']
        score_item.target_reason = 'public company within the same industry' #行业战略投资人

    elif is_company_score_industry_invest_industry_one(project,company,database):
        score_industry_invest_industry_one=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_invest_industry_one']
        score_item.target_reason = 'invested in similar companies' #投资过类似行业

    elif is_company_score_industry_invest_industry_two(project,company,database):
        score_industry_invest_industry_two=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_invest_industry_two']
        
        score_item.target_reason = 'investor within the same industry' #投资过相同行业

    sum_company_score=score_industry_in_industry+score_industry_invest_industry_one+score_industry_invest_industry_two

    company_invest_field_list=database['COMPANYINVESTMENTFIELD'].filter(company=company)
    for _field in company_invest_field_list:
        sum_company_score = 0
        score_industry_keyword = 0
        
        score_deal_type = 0
        score_deal_size = 0
        score_currency = 0
        score_finance_revenue = 0
        score_finance_growth = 0
        score_finance_net_income = 0
        score_finance_ebitda = 0
        score_local = 0

        
        if is_company_score_industry_keyword(project,_field,database):
            score_industry_keyword=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_keyword']
            
            score_industry_in_industry = 0
            score_industry_invest_industry_one = 0
            score_industry_invest_industry_two = 0

            
            score_item.target_reason = 'investment orientation' #有投资方向
            

        
        if is_company_score_deal_type(project,_field):
            score_deal_type=total_score*RECOMMONWEIGHT['deal_type']

        if is_company_score_deal_size(project,_field):
            score_deal_size=total_score*RECOMMONWEIGHT['deal_size']

        if is_company_score_currency_sure(project,_field):
            score_currency=total_score*RECOMMONWEIGHT['currency']*RECOMMONWEIGHT['currency_sure']
        elif is_company_score_currency_not_sure(project,_field):
            score_currency=total_score*RECOMMONWEIGHT['currency']*RECOMMONWEIGHT['industry_not_sure']

        if is_company_score_finance_revenue(project,_field):
            score_finance_revenue=total_score*RECOMMONWEIGHT['finance']*RECOMMONWEIGHT['finance_revenue'] 

        if is_company_score_finance_growth(project,_field):
            score_finance_growth=total_score*RECOMMONWEIGHT['finance']*RECOMMONWEIGHT['finance_growth'] 

        if is_company_score_finance_net_income(project,_field):
            score_finance_net_income=total_score*RECOMMONWEIGHT['finance']*RECOMMONWEIGHT['finance_net_income'] 

        if is_company_score_finance_ebitda(project,_field):
            score_finance_ebitda=total_score*RECOMMONWEIGHT['finance']*RECOMMONWEIGHT['finance_ebitda'] 

        if is_company_score_local(project,_field):
            score_local=total_score*RECOMMONWEIGHT['local']

        sum_company_score=score_industry_keyword+score_industry_in_industry+score_industry_invest_industry_one+score_industry_invest_industry_two+score_deal_type+score_deal_size+score_currency+score_finance_revenue+score_finance_growth+score_finance_net_income+score_finance_ebitda+score_local
        
        if sum_company_score>current_max_score:
            current_max_score=sum_company_score
            
            
            score_item.company_score_industry_keyword = score_industry_keyword
            score_item.company_score_deal_type = score_deal_type
            score_item.company_score_deal_size = score_deal_size
            score_item.company_score_currency = score_currency
            score_item.company_score_finance_revenue = score_finance_revenue
            score_item.company_score_finance_growth = score_finance_growth
            score_item.company_score_finance_net_income = score_finance_net_income
            score_item.company_score_finance_ebitda = score_finance_ebitda
            score_item.company_score_local = score_local
    
    score_item.sum_company_score = sum_company_score
    score_item.company_score_industry_in_industry = score_industry_in_industry
    score_item.company_score_industry_invest_industry_one = score_industry_invest_industry_one
    score_item.company_score_industry_invest_industry_two = score_industry_invest_industry_two
    
    if company_invest_field_list.count()>0:
        score_item.company_score_has_invest_field=1
            



def convert_demand_finance_type_to_num(finance_type):
    
    if finance_type==0:
        num_min = 0
        num_max = 99999999999999
    elif finance_type==1:
        num_min = 0
        num_max = 10*10000000
    elif finance_type==2:
        num_min = 10*10000000
        num_max = 20*10000000
    elif finance_type==3:
        num_min = 20*10000000
        num_max = 50*10000000
    elif finance_type==4:
        num_min = 50*10000000
        num_max = 100*10000000
    elif finance_type==5:
        num_min = 100*10000000
        num_max = 200*10000000
    elif finance_type==6:
        num_min = 200*10000000
        num_max = 300*10000000
    elif finance_type==7:
        num_min = 300*10000000
        num_max = 500*10000000
    elif finance_type==8:
        num_min = 500*10000000
        num_max = 1000*10000000
    elif finance_type==9:
        num_min = 1000*10000000
        num_max = 2000*10000000
    elif finance_type==10:
        num_min = 2000*10000000
        num_max = 3000*10000000
    elif finance_type==11:
        num_min = 3000*10000000
        num_max = 99999999999999
    else:
        num_min=0
        num_max=0

    return num_min,num_max
