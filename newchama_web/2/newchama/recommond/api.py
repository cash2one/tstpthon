#encoding:utf-8
from recommond.models import RECOMMONWEIGHT,RecommondItem,PROJECT_SCORE_LEVEL,TOTAL_SCORE,RECOMMONPROJECTWEIGHT,RecommondProjectItem,MatchingWord
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

def is_company_score_industry_invest_industry_one(project,company):
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
        _num=CompanyInvestmentHistory.objects.filter(company=company,cv1=_industry_cv1).count()
        if _num>0:
            _is_ok = True
    return _is_ok

def is_company_score_industry_invest_industry_two(project,company):
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
        _num=CompanyInvestmentHistory.objects.filter(company=company,cv2=_industry_cv2).count()
        if _num>0:
            _is_ok = True
    return _is_ok

notkey=['互联网','移动互联网','制造行业及其他']


def is_company_score_industry_keyword(project,company_invest_field):
    _is_ok=False
    project_kv_list =[item.keyword for item in ProjectKeyword.objects.filter(project=project)]

    _another_word=[]

    for kv in project_kv_list:
        _words=[item.word2 for item in MatchingWord.objects.filter(word1=kv, rank__gt=5) ]

        _another_word+=_words
    project_kv_list+=list(set(_another_word))    


    project_admin_kv_list = [item.keyword for item in ProjectKeywordAdmin.objects.filter(project=project)]
    

    _another_word2=[]
    for kv in project_admin_kv_list:
        _words=[item.word2 for item in MatchingWord.objects.filter(word1=kv, rank__gt=5) ]

        _another_word2+=_words
    project_admin_kv_list+=list(set(_another_word2)) 

    for p_kv_item in project_kv_list+project_admin_kv_list:
        if company_invest_field.tags:
            if p_kv_item not in notkey:
                if p_kv_item in company_invest_field.tags.split(','):
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
    #num_min,num_max=convert_demand_finance_type_to_num(company_invest_field.deal_size)
    _is_ok=False
    if project.deal_size:
        if project.deal_size>=company_invest_field.deal_size_min and project.deal_size <=company_invest_field.deal_size_max:
        #if project.deal_size>=num_min and project.deal_size <=num_max:
            _is_ok = True
        if company_invest_field.deal_size == 99:
            _is_ok = True
    else:
        _is_ok=True
    return _is_ok

def is_company_score_currency_sure(project,company_invest_field):
    _is_ok=False
    if project.pay_currency ==company_invest_field.deal_currency:
        _is_ok = True
    if company_invest_field.deal_currency == 99:
        _is_ok = True
    return _is_ok


def is_company_score_currency_not_sure(company_invest_field):
    _is_ok=False
    if company_invest_field.deal_currency==0:
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
    else:
        _is_ok=True
    return _is_ok



def is_project_score_industry_keyword(project,demand):
    _is_ok=False
    project_kv_list = ProjectKeyword.objects.filter(project=project)
    for p_kv_item in project_kv_list:
        if p_kv_item.keyword in demand.name_cn:
            _is_ok = True
        if p_kv_item.keyword in demand.name_en:
            _is_ok = True

    return _is_ok

def is_project_score_industry_in_industry(project,demand):
    _is_ok=False
    if project.company_industry:

        demand_industry_list=DemandIndustry.objects.filter(demand=demand)
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
    else:
        _is_ok=True
    return _is_ok

def is_project_score_above_deal_size(project,demand):
    num_min,num_max=convert_demand_finance_type_to_num(demand.deal_size)
    _is_ok=False
    if project.deal_size:
        if project.deal_size>num_max:
            _is_ok=True
    return _is_ok


def is_project_score_currency_sure(project,demand):
    _is_ok=False
    if project.pay_currency:
        if project.pay_currency==demand.pay_currency:
            _is_ok=True
    return _is_ok

def is_project_score_currency_not_sure(demand):
    _is_ok=False
    if demand.pay_currency==0:
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
    if project.company_country:
        if project.company_country in demand.company_countries.all():
            _is_ok=True
    else:
        _is_ok=True
    return _is_ok

def CheckDealCurrencyNotMatching(project,company):
    _is_ok=False
    company_demand_list=Demand.objects.exclude(status=5).filter(member__company=company,expire_date__gt=datetime.datetime.now())
    if company_demand_list.count()>0:
        _is_ok=True

        for _demand in company_demand_list:
            if is_project_score_currency_sure(project, _demand)>0 or \
               is_project_score_currency_not_sure(_demand):
                _is_ok=False

    company_invest_field_list=CompanyInvestmentField.objects.filter(company=company)
    if company_invest_field_list.count( )> 0:
        _is_ok=True
        for _field in company_invest_field_list:
            if is_company_score_currency_sure(project, _field) > 0 or \
               is_company_score_currency_not_sure(_field):
                _is_ok=False
    return _is_ok

def CheckDealSizeNotMatching(project,company):
    _is_ok=False
    company_demand_list=Demand.objects.exclude(status=5).filter(member__company=company,expire_date__gt=datetime.datetime.now())
    if company_demand_list.count()>0:
        _is_ok=True

        for _demand in company_demand_list:
            if is_project_score_deal_size(project, _demand)>0:
                _is_ok=False

    company_invest_field_list=CompanyInvestmentField.objects.filter(company=company)
    if company_invest_field_list.count( )> 0:
        _is_ok=True
        for _field in company_invest_field_list:
            if is_company_score_deal_size(project, _field) > 0:
                _is_ok=False
    return _is_ok

def CheckDealTypeNotMatching(project,company):
    _is_ok=False
    company_demand_list=Demand.objects.exclude(status=5).filter(member__company=company,expire_date__gt=datetime.datetime.now())
    if company_demand_list.count()>0:
        _is_ok=True

        for _demand in company_demand_list:
            if is_project_score_deal_type(project,_demand)>0:
                _is_ok=False

    company_invest_field_list=CompanyInvestmentField.objects.filter(company=company)
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

    if is_project_score_industry_in_industry(project,demand):
        score_industry_in_industry=total_score*RECOMMONPROJECTWEIGHT['industry']

    
    if is_project_score_deal_type(project,demand):
        score_deal_type=total_score*RECOMMONPROJECTWEIGHT['deal_type']

    if is_project_score_deal_size(project,demand):
        score_deal_size=total_score*RECOMMONPROJECTWEIGHT['deal_size']

    if is_project_score_currency_sure(project,demand):
        score_currency=total_score*RECOMMONPROJECTWEIGHT['currency']*RECOMMONPROJECTWEIGHT['currency_sure']
    elif is_project_score_currency_not_sure(demand):
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
def GetRecommondScoreItem(project,company):

    _recommond_score_num=RecommondItem.objects.filter(company=company,project=project).count()
    if _recommond_score_num>0:
        _recommond_score=RecommondItem.objects.filter(company=company,project=project).first()
    else:
        _recommond_score = RecommondItem()
        _recommond_score.project=project
        _recommond_score.company=company
    ComputerProjectRecommondScore(project,company,_recommond_score)

    ComputerCompanyRecommondScore(project,company,_recommond_score)

    if _recommond_score.company_score_industry_in_industry>0:
        _recommond_score.target_reason = 'Strategic Industry Investor' #行业战略投资人
    
    if _recommond_score.company_score_industry_invest_industry_one >0 or _recommond_score.company_score_industry_invest_industry_two>0:
        _recommond_score.target_reason = 'Relevant Portfolio Company' #投资过相关的行业

    if _recommond_score.company_score_industry_keyword >0:
        _recommond_score.target_reason = 'Company Investment Criteria' #有相关投资需求

    if _recommond_score.sum_project_score >=PROJECT_SCORE_LEVEL:
        _recommond_score.target_reason = 'Active Buy-Side Mandates' #有活跃的买方需求

    _recommond_score.sum_score=_recommond_score.sum_project_score+_recommond_score.sum_company_score
    return _recommond_score

def get_financial_type_of_demand(deal_size):
    financial_type = 0
    if deal_size <= 5000000:
        financial_type = 1
    elif 5000000 < deal_size <= 10000000:
        financial_type = 2
    elif 10000000 < deal_size <= 20000000:
        financial_type = 3
    elif 20000000 < deal_size <= 50000000:
        financial_type = 4
    elif 50000000 < deal_size <= 100000000:
        financial_type = 5
    elif 100000000 < deal_size <= 300000000:
        financial_type = 7
    elif 300000000 < deal_size <= 500000000:
        financial_type = 8
    elif 500000000 < deal_size <= 1000000000:
        financial_type = 9
    elif deal_size > 1000000000:
        financial_type =10
    return financial_type

def get_financial_type_of_matching_table(deal_size):
    financial_type = [0, 1]
    if deal_size <= 10000000:
        financial_type = [1, 0]
    elif 10000000 < deal_size <= 20000000:
        financial_type = [2, 3]
    elif 20000000 < deal_size <= 50000000:
        financial_type = [3, 4]
    elif 50000000 < deal_size <= 100000000:
        financial_type = [4, 5]
    elif 100000000 < deal_size <= 200000000:
        financial_type = [5, 6]
    elif 200000000 < deal_size <= 300000000:
        financial_type = [6, 7]
    elif 300000000 < deal_size <= 500000000:
        financial_type = [7, 8]
    elif 500000000 < deal_size <= 1000000000:
        financial_type = [8, 9]
    elif 1000000000 < deal_size <= 2000000000:
        financial_type = [9, 10]
    elif 2000000000 < deal_size <= 3000000000:
        financial_type = [10, 11]
    elif deal_size > 3000000000:
        financial_type = [11]
    return financial_type

#def get_financial_type_of_matching_table(deal_size):
#    financial_type = 0
#    if deal_size <= 10000000:
#        financial_type = 1
#    elif 10000000 < deal_size <= 20000000:
#        financial_type = 2
#    elif 20000000 < deal_size <= 50000000:
#        financial_type = 3
#    elif 50000000 < deal_size <= 100000000:
#        financial_type = 4
#    elif 100000000 < deal_size <= 200000000:
#        financial_type = 5
#    elif 200000000 < deal_size <= 300000000:
#        financial_type = 6
#    elif 300000000 < deal_size <= 500000000:
#        financial_type = 7
#    elif 500000000 < deal_size <= 1000000000:
#        financial_type = 8
#    elif 1000000000 < deal_size <= 2000000000:
#        financial_type = 9
#    elif 2000000000 < deal_size <= 3000000000:
#        financial_type = 10
#    elif deal_size > 3000000000:
#        financial_type = 11
#    return financial_type

#计算公司下面的项目分数
def ComputerProjectRecommondScore(project,company,score_item):
    current_max_score=0
    total_score=TOTAL_SCORE

    # company_demand_list=Demand.objects.exclude(status=5).filter(member__company=company,expire_date__gt=datetime.datetime.now())
    # ensure the deal size is in the same range (enum value 0 mapping to "All")
    financial_type = get_financial_type_of_demand(project.deal_size)
    company_demand_list=Demand.objects.exclude(status=5).filter(member__company=company,
                                                                pay_currency=project.pay_currency,
                                                                deal_size__in=(0, financial_type),
                                                                expire_date__gt=datetime.datetime.now())
    for _demand in company_demand_list:

        #if not is_project_score_above_deal_size:
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

        
        if is_project_score_industry_keyword(project,_demand):
            score_industry_keyword=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_keyword']
        
        elif is_project_score_industry_in_industry(project,_demand):
            score_industry_in_industry=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_in_industry']

        sum_industry_score = score_industry_in_industry + score_industry_keyword

        if sum_industry_score > 0:
            if is_project_score_deal_type(project,_demand):
                score_deal_type=total_score*RECOMMONWEIGHT['deal_type']

            if is_project_score_deal_size(project,_demand):
                score_deal_size=total_score*RECOMMONWEIGHT['deal_size']

            if is_project_score_currency_sure(project,_demand):
                score_currency=total_score*RECOMMONWEIGHT['currency']*RECOMMONWEIGHT['currency_sure']
            elif is_project_score_currency_not_sure(_demand):
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
        else:
            sum_project_score = 0
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
def ComputerCompanyRecommondScore(project,company,score_item):
    current_max_score=0
    total_score=TOTAL_SCORE

    score_industry_in_industry = 0
    score_industry_invest_industry_one = 0
    score_industry_invest_industry_two = 0

    if is_company_score_industry_in_industry(project,company):

        
        score_industry_in_industry=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_in_industry']
        

    elif is_company_score_industry_invest_industry_one(project,company):
        score_industry_invest_industry_one=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_invest_industry_one']
        

    elif is_company_score_industry_invest_industry_two(project,company):
        score_industry_invest_industry_two=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_invest_industry_two']
        
        

    sum_company_score=score_industry_in_industry+score_industry_invest_industry_one+score_industry_invest_industry_two

    #company_invest_field_list=CompanyInvestmentField.objects.filter(company=company)

    financial_type = get_financial_type_of_matching_table(project.deal_size)
    financial_type.append(0)
    financial_type.append(99)
    company_invest_field_list=CompanyInvestmentField.objects.filter(company=company,
                                                                    deal_currency__in=(0, 99, project.pay_currency),
                                                                    deal_size__in=financial_type)
    company_invest_field_list = company_invest_field_list.exclude(hot=0)
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

        
        if is_company_score_industry_keyword(project,_field):
            score_industry_keyword=total_score*RECOMMONWEIGHT['industry']*RECOMMONWEIGHT['industry_keyword']
            
            score_industry_in_industry = 0
            score_industry_invest_industry_one = 0
            score_industry_invest_industry_two = 0

        
        if is_company_score_deal_type(project,_field):
            score_deal_type=total_score*RECOMMONWEIGHT['deal_type']

        if is_company_score_deal_size(project,_field):
            score_deal_size=total_score*RECOMMONWEIGHT['deal_size']

        if is_company_score_currency_sure(project,_field):
            score_currency=total_score*RECOMMONWEIGHT['currency']*RECOMMONWEIGHT['currency_sure']
        elif is_company_score_currency_not_sure(_field):
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
    
    #score_item.sum_company_score = sum_company_score
    if score_item.company_score_industry_keyword == 0:
        score_item.company_score_industry_in_industry = score_industry_in_industry
        score_item.company_score_industry_invest_industry_one = score_industry_invest_industry_one
        score_item.company_score_industry_invest_industry_two = score_industry_invest_industry_two
    else:
        score_item.company_score_industry_in_industry = 0
        score_item.company_score_industry_invest_industry_one = 0
        score_item.company_score_industry_invest_industry_two = 0

    score_item.sum_company_score = score_item.company_score_industry_keyword + \
                                   score_item.company_score_industry_in_industry + \
                                   score_item.company_score_industry_invest_industry_one + \
                                   score_item.company_score_industry_invest_industry_two + \
                                   score_item.company_score_deal_type + \
                                   score_item.company_score_deal_size + \
                                   score_item.company_score_currency + \
                                   score_item.company_score_finance_revenue + \
                                   score_item.company_score_finance_growth + \
                                   score_item.company_score_finance_net_income + \
                                   score_item.company_score_finance_ebitda + \
                                   score_item.company_score_local
    
    if company_invest_field_list.count()>0:
        score_item.company_score_has_invest_field=1
            



def convert_demand_finance_type_to_num(finance_type):
    base = 1000000 
    if finance_type==99:
        num_min = 0
        num_max = 99999999999999
    elif finance_type==1:
        num_min = 0
        num_max = 10*base
    elif finance_type==2:
        num_min = 10*base
        num_max = 20*base
    elif finance_type==3:
        num_min = 20*base
        num_max = 50*base
    elif finance_type==4:
        num_min = 50*base
        num_max = 100*base
    elif finance_type==5:
        num_min = 100*base
        num_max = 200*base
    elif finance_type==6:
        num_min = 200*base
        num_max = 300*base
    elif finance_type==7:
        num_min = 300*base
        num_max = 500*base
    elif finance_type==8:
        num_min = 500*base
        num_max = 1000*base
    elif finance_type==9:
        num_min = 1000*base
        num_max = 2000*base
    elif finance_type==10:
        num_min = 2000*base
        num_max = 3000*base
    elif finance_type==11:
        num_min = 3000*base
        num_max = 99999999999999
    else:
        num_min=0
        num_max=0

    return num_min,num_max
