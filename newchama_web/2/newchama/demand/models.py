from django.db import models
from member.models import Member, Company
from area.models import Country, Province, City
from project.models import Project
from industry.models import Industry
from adminuser.models import AdminUser
from django.utils.translation import ugettext as _
import datetime
# Create your models here.
class Demand(models.Model):
    STATUS_TYPES = (
        (0, _('Pending')),
        (1, _('Not approved')),
        (2, _('Approved')),
        (3, _('Offline')),
        (4, _('Draft')),
        (5, _('Deleted')),
    )
    SERVICE_TYPES = (
        (0, _('All')),
        (1, _('Buyout')),
        (2, _('Growth Capital/Financing')),
        (3, _('Old stock transfer(not buyout)')),
        (4, _('Buyout or Financing')),
        (5, _('Asset sale')),
        (6, _('Additonal issue')),
        (7, _('Debt')),
        (9, _('IPO')),
    )
    SERVICE_TYPES_2 = (
        (1, _('Buyout')),
        (2, _('Growth Capital/Financing')),
        (3, _('Old stock transfer(not buyout)')),
        (4, _('Buyout or Financing')),
        (5, _('Asset sale')),
        (6, _('Additonal issue')),
        (7, _('Debt')),
        (9, _('IPO')),
    )
    CURRENCY_TYPES = (
        (1, _('CNY')),
        (2, _('USD')),
        (3, _('EUR')),
    )
    EMPLOYEES_COUNT_TYPES = (
        (0, _('All')),
        (1, _('Less than 10')),
        (2, _('10-20')),
        (3, _('20-50')),
        (4, _('50-100')),
        (5, _('100-200')),
        (6, _('200-300')),
        (7, _('300-500')),
        (8, _('500-1000')),
        (9, _('1000-2000')),
        (10, _('2000-3000')),
        (11, _('More than 3000')),
    )
    FINANCIAL_TYPES = (
        (0, _('All')),
        (1, _('Less than 5 M')),
        (2, _('5-10 M')),
        (3, _('10-20 M')),
        (4, _('20-50 M')),
        (5, _('50-100 M')),
        (7, _('100-300 M')),
        (8, _('300-500 M')),
        (9, _('500-1000 M')),
        (10, _('More than 1000 M')),
    )
    FINANCIAL_TYPES_2 = (
        (1, _('Less than 5 M')),
        (2, _('5-10 M')),
        (3, _('10-20 M')),
        (4, _('20-50 M')),
        (5, _('50-100 M')),
        (7, _('100-300 M')),
        (8, _('300-500 M')),
        (9, _('500-1000 M')),
        (10, _('More than 1000 M')),
    )
    STOCK_STRUCTURE_PERCENTAGE_TYPES = (
        (0, _('All')),
        (1, _('Less than 10%')),
        (2, '10-20%'),
        (3, '20-30%'),
        (4, '30-40%'),
        (5, '50-60%'),
        (6, '60-70%'),
        (7, '70-80%'),
        (8, _('More than 90%')),
    )
    INVESTMENT_STAGE = (
        (5, _('Angel Investment')),
        (1, _('series A')),
        (2, _('series B')),
        (3, _('series C')),
        (4, _('series D')),
    )
    PAY_WAY = (
        (1, _('cash')),
        (2, _('stock')),
        (3, _('other')),
    )
    PAY_CURRENCY = (
        (1, _('CNY')),
        (2, _('USD')),
        (3, _('EUR')),
    )
    RELATE_DEMAND = (
        (1, _('buyer agent')),
        (2, _('direct buyer')),
        (4, _('other')),
    )
    VALID_DAY = (
        (30, _('30 days')),
        (60, _('60 days')),
        (90, _('90 days')),
        (180, _('180 days')),
    )
    PROCESS = (
        (0, _('UnPublished')),
        (1, _('Published')),
        (2, _('In Negotiation')),
        (3, _('NDA Signed')),
        (4, _('TS Signed')),
        (5, _('Settlement')),
    )
    AUDIT_STATUS = (
        (0, _('No audited')),
        (1, _('Big four')),
        (2, _('Not big four')),
    )
    name_cn = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    member = models.ForeignKey(Member, related_name='member_demand_publisher')
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(default=datetime.datetime.now(), auto_now=True)
    status = models.IntegerField(choices=STATUS_TYPES, default=0)
    pv = models.IntegerField(default=0)
    service_type = models.IntegerField(choices=SERVICE_TYPES, null=True, blank=True)
    intro_cn = models.TextField(null=True)
    intro_en = models.TextField(null=True)
    business_cn = models.TextField(null=True)
    business_en = models.TextField(null=True)
    company_symbol = models.CharField(null=True, max_length=50)
    company_name = models.CharField(null=True, max_length=255)
    company_countries = models.ManyToManyField(Country, null=True, blank=True)
    company_provinces = models.ManyToManyField(Province, null=True, blank=True)
    company_cities = models.ManyToManyField(City, null=True, blank=True)
    company_industries = models.ManyToManyField(Industry, null=True, blank=True, related_name='demand_target_company_industries')
    company_stock_symbol = models.CharField(null=True, max_length=20)
    financial_is_must_audit = models.BooleanField(default=0)
    financial_audit_company_is_must_default = models.BooleanField(default=0)
    currency_type_financial = models.IntegerField(choices=CURRENCY_TYPES, null=True, blank=True)
    financial_year = models.IntegerField(default=datetime.datetime.today().year)
    income = models.IntegerField(null=True, blank=True, choices=FINANCIAL_TYPES)
    profit = models.IntegerField(null=True, blank=True, choices=FINANCIAL_TYPES)
    growth_three_year = models.DecimalField(null=True, max_digits=16, decimal_places=2)
    net_assets = models.IntegerField(null=True, blank=True, choices=FINANCIAL_TYPES)
    employees_count_type = models.IntegerField(choices=EMPLOYEES_COUNT_TYPES, null=True, blank=True)
    registered_capital = models.IntegerField(choices=FINANCIAL_TYPES, null=True, blank=True)
    total_assets_last_phase = models.IntegerField(choices=FINANCIAL_TYPES, null=True, blank=True)
    income_last_phase = models.IntegerField(choices=FINANCIAL_TYPES, null=True, blank=True)
    profit_last_phase = models.IntegerField(choices=FINANCIAL_TYPES, null=True, blank=True)
    remark_cn = models.TextField(null=True)
    remark_en = models.TextField(null=True)
    expire_date = models.DateField(null=True)
    target_members = models.ManyToManyField(Member, related_name='demand_push_target_members')
    target_companies = models.ManyToManyField(Company, related_name='project_target_companies')
    target_industries = models.ManyToManyField(Industry, related_name='demand_push_target_industries')
    is_anonymous = models.BooleanField(default=0)
    stock_structure_percentage_type_management = models.IntegerField(null=True, blank=True, choices=STOCK_STRUCTURE_PERCENTAGE_TYPES)
    stock_structure_percentage_type_institutional = models.IntegerField(null=True, blank=True, choices=STOCK_STRUCTURE_PERCENTAGE_TYPES)
    stock_structure_percentage_type_private = models.IntegerField(null=True, blank=True, choices=STOCK_STRUCTURE_PERCENTAGE_TYPES)
    name_project_cn = models.CharField(max_length=255)
    name_project_en = models.CharField(max_length=255)
    expected_enterprice_value =models.IntegerField(choices=FINANCIAL_TYPES, null=True, blank=True)
    financial_audit_company_name = models.CharField(null=True, default=None, max_length=255)
    deal_size = models.IntegerField(null=True, blank=True, choices=FINANCIAL_TYPES)
    has_attach = models.BooleanField(default=0)
    # other_target_companies = models.TextField(null=True)
    is_suitor = models.BooleanField(default=0)

    is_list_company = models.BooleanField(default=0)
    project_relation = models.IntegerField(choices=RELATE_DEMAND, null=True, blank=True)
    project_stage = models.IntegerField(choices=INVESTMENT_STAGE, null=True, blank=True)
    pay_way = models.IntegerField(choices=PAY_WAY, null=True, blank=True)
    pay_currency = models.IntegerField(choices=PAY_CURRENCY, null=True, blank=True)
    valid_day = models.IntegerField(choices=VALID_DAY, null=True, blank=True)
    income_enter = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    profit_enter = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    total_assets = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    total_profit = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    process = models.IntegerField(choices=PROCESS, null=True, blank=True)
    integrity = models.IntegerField(null=True, blank=True)
    integrity_en = models.IntegerField(null=True, blank=True)
    is_recommend = models.BooleanField(default=0)
    is_top = models.BooleanField(default=0)
    audit_status = models.IntegerField(choices=AUDIT_STATUS, null=True, blank=True)
    stock_percent = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    ebitda = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    deal_size_enter = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    income_last_phase_enter = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    profit_last_phase_enter = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    expected_enterprice_value_enter = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'demand_demand'


class DemandKeyword(models.Model):
    demand = models.ForeignKey(Demand, related_name='demand_keyword')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'demand_keyword'


class DemandKeywordEn(models.Model):
    demand = models.ForeignKey(Demand, related_name='demand_keyword_en')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'demand_keyword_en'


class DemandKeywordAdmin(models.Model):
    demand = models.ForeignKey(Demand, related_name='demand_keyword_admin')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'demand_keyword_Admin'


class DemandOtherTargetCompany(models.Model):
    TYPES = (
        (1, _('repository_investmentcompany')),
        (2, _('repository_listedcompany')),
    )
    demand = models.ForeignKey(Demand, related_name='demand_other_company')
    name_cn = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    short_name_cn = models.CharField(max_length=20, blank=True)
    short_name_en = models.CharField(max_length=20, blank=True)
    table_name = models.IntegerField(choices=TYPES, default=1)
    company_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'demand_other_target_company'


class DemandTargetProjectDetail(models.Model):
    TYPES = (
        (1, _('Admin')),
        (2, _('Self')),
        (3, _('Submit')),
    )
    demand = models.ForeignKey(Demand, related_name='demand_detail')
    project = models.ForeignKey(Project, related_name='demand_detail_project')
    member = models.ForeignKey(Member, related_name='demand_detail_member')
    recommend_type = models.IntegerField(choices=TYPES, default=1)
    add_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=0)
    update_member = models.ForeignKey(Member, related_name='demand_detail_update_member', null=True, blank=True)
    update_time = models.DateTimeField(default=datetime.datetime.now(), auto_now=True)

    class Meta:
        db_table = 'demand_target_project_detail'


class DemandIndustry(models.Model):
    demand = models.ForeignKey(Demand, related_name='demand_industries')
    cv1 = models.IntegerField(blank=True, null=True)
    cv2 = models.IntegerField(blank=True, null=True)
    cv3 = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'demand_demandindustry'


class DemandAttach(models.Model):
    demand = models.ForeignKey(Demand, related_name='demand_attach')
    file_type = models.CharField(max_length=50)
    file_type_name = models.CharField(null=True, max_length=100)
    file_name = models.CharField(max_length=100)
    new_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.file_name

    class Meta:
        db_table = 'demand_demandAttach'


class StatusDemand(object):
    pending = 0
    not_approved = 1
    approved = 2
    offline = 3
    draft = 4
    deleted = 5


class DemandViewLog(models.Model):
    member = models.ForeignKey(Member, related_name='demand_view_log_member')
    demand = models.ForeignKey(Demand, related_name='demand_view_log_demand')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demand_view_log'


class DemandCheckLog(models.Model):
    Results_Check = (
        (1, 'Approve'),
        (2, 'Disapprove'),
    )
    adminuser = models.ForeignKey(AdminUser, related_name='demand_check_log_adminuser')
    demand = models.ForeignKey(Demand, related_name='demand_check_log_demand')
    reason = models.TextField(null=True)
    result = models.IntegerField(default=1, choices=Results_Check)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demand_check_log'


class ResultsDemandCheck(object):
    approve = 1
    disapprove = 2


class DemandPrintLog(models.Model):
    member = models.ForeignKey(Member, related_name='demand_print_log_member')
    demand = models.ForeignKey(Demand, related_name='demand_print_log_demand')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demand_print_log'


class DemandDownloadLog(models.Model):
    member = models.ForeignKey(Member, related_name='demand_download_log_member')
    demand = models.ForeignKey(Demand, related_name='demand_download_log_demand')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demand_download_log'



class DemandTargetProjectDetail(models.Model):
    TYPES = (
        (1, _('Admin')),
        (2, _('Self')),
        (3, _('Submit')),
    )
    demand = models.ForeignKey(Demand, related_name='demand_detail')
    project = models.ForeignKey(Project, related_name='demand_detail_project')
    member = models.ForeignKey(Member, related_name='demand_detail_member')
    recommend_type = models.IntegerField(choices=TYPES, default=1)
    add_time = models.DateTimeField(default=datetime.datetime.now())
    is_delete = models.BooleanField(default=0)
    update_member = models.ForeignKey(Member, related_name='demand_detail_update_member', null=True, blank=True)
    update_time = models.DateTimeField(default=datetime.datetime.now(), auto_now=True)

    class Meta:
        db_table = 'demand_target_project_detail'


class DemandRecommendLog(models.Model):
    TYPES = (
        (1, 'recommend'),
        (2, 'top'),
    )
    demand = models.ForeignKey(Demand, related_name='demand_recommend_log_demand')
    add_time = models.DateTimeField(auto_now=True)
    type = models.IntegerField(choices=TYPES, default=1)

    class Meta:
        db_table = 'demand_recommend_log'


class DemandRecommondReasonAdmin(models.Model):
    project = models.ForeignKey(Demand, related_name='demand_recommond_reason_admin')
    reason = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'demand_admin_recommond_reason'


class TypeDemandRecommend(object):
    recommend = 1
    top = 2