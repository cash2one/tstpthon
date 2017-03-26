#encoding:utf-8
from django.db import models
import datetime
from django.utils.translation import ugettext as _
from services.models import Project, Company, Demand, Member

PROJECT_SCORE_LEVEL=50
TOTAL_SCORE=100
RECOMMONWEIGHT={
    'industry':0.5,
    'deal_type':0.2,
    'deal_size':0.1,
    'currency':0.05,
    'finance':0.1,
    'local':0.05,
    'industry_keyword':0.6,
    'industry_in_industry':0.3,
    'industry_invest_industry_one':0.5,
    'industry_invest_industry_two':0.5,
    'currency_sure':1,
    'industry_not_sure':0.5,
    'finance_revenue':0.2,
    'finance_growth':0.1,
    'finance_net_income':0.5,
    'finance_ebitda':0.2,

}

class RecommondItem(models.Model):
    project = models.ForeignKey(Project)
    company = models.ForeignKey(Company)

    is_man = models.BooleanField(default=0)
    is_star = models.BooleanField(default=0)
    has_user = models.BooleanField(default=0)
    is_delete = models.BooleanField(default=0)
    rank = models.IntegerField(default=0)
    target_reason=models.CharField(max_length=255, blank=True,null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    man_add_time = models.DateTimeField(default=datetime.datetime.now())
    
    sum_score = models.IntegerField(default=0)
    sum_project_score = models.IntegerField(default=0)
    sum_company_score = models.IntegerField(default=0)
    company_score_industry_keyword = models.IntegerField(default=0)
    company_score_industry_in_industry = models.IntegerField(default=0)
    company_score_industry_invest_industry_one = models.IntegerField(default=0)
    company_score_industry_invest_industry_two = models.IntegerField(default=0)
    company_score_deal_type = models.IntegerField(default=0)
    company_score_deal_size = models.IntegerField(default=0)
    company_score_currency = models.IntegerField(default=0)
    company_score_finance_revenue = models.IntegerField(default=0)
    company_score_finance_growth = models.IntegerField(default=0)
    company_score_finance_net_income = models.IntegerField(default=0)
    company_score_finance_ebitda = models.IntegerField(default=0)
    company_score_local = models.IntegerField(default=0)
    company_score_has_invest_field = models.IntegerField(default=0)
    
    project_score_industry_keyword = models.IntegerField(default=0)
    project_score_industry_in_industry = models.IntegerField(default=0)
    project_score_industry_invest_industry_one = models.IntegerField(default=0)
    project_score_industry_invest_industry_two = models.IntegerField(default=0)
    project_score_deal_type = models.IntegerField(default=0)
    project_score_deal_size = models.IntegerField(default=0)
    project_score_currency = models.IntegerField(default=0)
    project_score_finance_revenue = models.IntegerField(default=0)
    project_score_finance_growth = models.IntegerField(default=0)
    project_score_finance_net_income = models.IntegerField(default=0)
    project_score_finance_ebitda = models.IntegerField(default=0)
    project_score_local = models.IntegerField(default=0)
    is_in_control_panel = models.BooleanField(default=0)
    
    updated = models.DateTimeField(auto_now=True, default=datetime.datetime.now())
    
    class Meta:
        db_table = 'recommond_score'


    def target_reason_cn(self):
        if self.target_reason=='Active Deal Alert':
            return '订阅相关交易机会'
        elif self.target_reason=='Strategic Industry Investor':
            return '行业战略投资人'
        elif self.target_reason=='Active Buy-Side Mandates':
            return '正在寻找相关标的'   #'有活跃的买方需求'
        elif self.target_reason=='Company Investment Criteria':
            return '持续关注此投资领域'  #'有相关投资需求'
        elif self.target_reason=='Relevant Portfolio Company':
            return '投资过相关的行业'
    def has_user_cn(self):
        if self.has_user:
            return 'Y'
        else:
            return 'N'

    def is_star_cn(self):
        if self.is_star:
            return '★'
        else:
            return ''


RECOMMEND_PROCESS = (
    (0, _('UnPublished')),
    (1, _('Published')),
    (2, _('Remove')),
    (3, _('NDA Signed')),
    (4, _('TS Signed')),
    (5, _('Settlement')),
)

class ProjectTargetCompanyDetail(models.Model):
    TYPES = (
        (1, _('Admin')),
        (2, _('Self')),
        (3, _('Submit')),
    )
    project = models.ForeignKey(Project, related_name='project_detail')
    company = models.ForeignKey(Company, related_name='project_detail_company')
    recommondItem = models.ForeignKey(RecommondItem, related_name='project_recommond_item', blank=True, null=True)
    member = models.ForeignKey(Member, related_name='project_detail_member')
    recommend_type = models.IntegerField(choices=TYPES, default=1)
    status = models.IntegerField(choices=RECOMMEND_PROCESS, default=0)
    add_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=0)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_target_company_detail'


class TargetCompanyDetailHistory(models.Model):
    target_company_detail = models.ForeignKey(ProjectTargetCompanyDetail, related_name='target_company_detail')
    operate_status = models.IntegerField(choices=RECOMMEND_PROCESS, default=0)
    add_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'project_target_company_detail_history'


RECOMMONPROJECTWEIGHT={
    'industry':0.5,
    'deal_type':0.2,
    'deal_size':0.1,
    'currency':0.05,
    'finance':0.1,
    'local':0.05,
    'currency_sure':1,
    'industry_not_sure':0.5,
    'finance_revenue':0.2,
    'finance_growth':0.1,
    'finance_net_income':0.5,
    'finance_ebitda':0.2,
}


class RecommondProjectItem(models.Model):  
    demand = models.ForeignKey(Demand)
    project = models.ForeignKey(Project)

    is_man = models.BooleanField(default=0)
    is_star = models.BooleanField(default=0)
    has_user = models.BooleanField(default=0)
    is_delete = models.BooleanField(default=0)
    rank = models.IntegerField(default=0)
    target_reason=models.CharField(max_length=255, blank=True,null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    man_add_time = models.DateTimeField(default=datetime.datetime.now())
    
    sum_project_score = models.IntegerField(default=0)
    project_score_industry_in_industry = models.IntegerField(default=0)
    project_score_deal_type = models.IntegerField(default=0)
    project_score_deal_size = models.IntegerField(default=0)
    project_score_currency = models.IntegerField(default=0)
    project_score_finance_revenue = models.IntegerField(default=0)
    project_score_finance_growth = models.IntegerField(default=0)
    project_score_finance_net_income = models.IntegerField(default=0)
    project_score_finance_ebitda = models.IntegerField(default=0)
    project_score_local = models.IntegerField(default=0)
    
    updated = models.DateTimeField(auto_now=True, default=datetime.datetime.now())
    
    class Meta:
        db_table = 'recommond_project_score'
    
    def is_star_cn(self):
        if self.is_star:
            return '★'
        else:
            return ''


class MatchingWord(models.Model):  
    word1=models.CharField(max_length=255)
    word2=models.CharField(max_length=255)
    rank = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recommond_matching_word'

    