#-*-encoding:utf-8-*-
from django.db import models
from member.models import Member, Company, DetailDealType, SubDetailDealType
from repository.models import StockExchange
from area.models import Country, Province, City, RegionLevelOne, RegionLevelTwo, RegionLevelThree
from industry.models import Industry
from adminuser.models import AdminUser
import datetime
from django.utils.translation import ugettext as _
# Create your models here.


class Project(models.Model):
    STATUS_TYPES = (
        (0, _('Pending')),
        (1, _('Not approved')),
        (2, _('Approved')),
        (3, _('Offline')),
        (4, _('Draft')),
        (5, _('Deleted')),
    )
    STATUS_CHECK_TYPES = (
        (-1, _('Return')),
        (0, _('Normal')),
        (1, _('Pass')),
    )
    SERVICE_TYPES = (
        (1, _('Buyout')),
        (2, _('Growth Capital/Financing')),
        (3, _('Old stock transfer(not buyout)')),
        (4, _('Buyour or Financing')),
        (5, _('Asset sale')),
        (6, _('Additonal issue')),
        (7, _('Debt')),
        (8, _('Convertible bond')),
        (9, _('IPO'))
    )
    CURRENCY_TYPES = (
        (1, _('CNY')),
        (2, _('USD')),
        (3, _('EUR')),
    )
    PAY_CURRENCY = (
        (1, _('CNY')),
        (2, _('USD')),
        (3, _('EUR')),
    )
    EMPLOYEES_COUNT_TYPES = (
        (1, _('Less than 10')),
        (2, '10-20'),
        (3, '20-50'),
        (4, '50-100'),
        (5, '100-200'),
        (6, '200-300'),
        (7, '300-500'),
        (8, '500-1000'),
        (9, '1000-2000'),
        (10, '2000-3000'),
        (11, _('More than 3000')),
    )
    FINANCIAL_TYPES = (
        (1, _('Less than 2')),
        (2, '2-5'),
        (3, '5-10'),
        (4, '10-20'),
        (5, '20-50'),
        (6, '50-100'),
        (7, '100-300'),
        (8, '300-500'),
        (9, '500-1000'),
        (10, _('More than 1000')),
    )
    INVESTMENT_STAGE = (
        (5, _('Angel Investment')),
        (1, _('series A')),
        (2, _('series B')),
        (3, _('series C')),
        (4, _('series D')),
    )
    RELATE_PROJECT = (
        (1, _('exclusive agent')),
        (2, _('not exclusive agent')),
        (3, _('management of seller')),
        (4, _('shareholder of seller')),
        (5, _('other')),
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
    CREATE_SOURCE = (
        (0, _('Web Create')),
        (1, _('App Create')),
        (2, _('CMS Create')),
    )
    TARGET_PLATFORM = (
        (0, _('Display in Web')),
        (1, _('Display in App')),
        (2, _('Display in Both')),
    )
    name_cn = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    member = models.ForeignKey(Member, related_name='member_publisher')
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(default=datetime.datetime.now(), auto_now=True)
    status = models.IntegerField(choices=STATUS_TYPES, default=0)
    # status_check = models.IntegerField(choices=STATUS_CHECK_TYPES, default=0)
    pv = models.IntegerField(default=0)
    service_type = models.IntegerField(choices=SERVICE_TYPES, null=True, blank=True)
    price_min = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    price_max = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    lock_date = models.DateField(null=True)
    intro_cn = models.TextField(null=True)
    intro_en = models.TextField(null=True)
    currency_type_service = models.IntegerField(choices=CURRENCY_TYPES, null=True, blank=True)
    company_symbol_en = models.CharField(null=True, max_length=50)
    company_name_en = models.CharField(null=True, max_length=255)
    company_symbol_cn = models.CharField(null=True, max_length=50)
    company_name_cn = models.CharField(null=True, max_length=255)
    is_list_company = models.BooleanField(default=0)
    company_country = models.ForeignKey(Country, null=True, blank=True)
    company_province = models.ForeignKey(Province, null=True, blank=True)
    company_cities = models.ForeignKey(City, null=True, blank=True)
    regionlevelone = models.ForeignKey(RegionLevelOne, null=True, blank=True)
    regionleveltwo = models.ForeignKey(RegionLevelTwo, null=True, blank=True)
    regionlevelthree = models.ForeignKey(RegionLevelThree, null=True, blank=True)
    company_stock_exchange = models.ForeignKey(StockExchange, null=True, blank=True)
    company_industry = models.ForeignKey(Industry, null=True, blank=True, related_name='project_company_industry')
    company_stock_symbol = models.CharField(null=True, max_length=20)

    company_intro_cn = models.TextField(blank=True,null=True)
    company_intro_en = models.TextField(blank=True,null=True)
    company_industry_intro_cn = models.TextField(blank=True,null=True)
    company_industry_intro_en = models.TextField(blank=True,null=True)

    financial_is_audit = models.BooleanField(default=0)
    financial_audit_company_name = models.CharField(null=True, max_length=255)
    financial_audit_company_is_default = models.BooleanField(default=0)
    currency_type_financial = models.IntegerField(choices=CURRENCY_TYPES, default=1)
    financial_year = models.IntegerField(null=True, blank=True)
    income = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    profit = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    growth_three_year = models.DecimalField(null=True, max_digits=16, decimal_places=2)
    employees_count_type = models.IntegerField(choices=EMPLOYEES_COUNT_TYPES, null=True, blank=True)
    registered_capital = models.BigIntegerField(choices=FINANCIAL_TYPES, null=True, blank=True)
    total_assets_last_phase = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    income_last_phase = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    profit_last_phase = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    expected_enterprice_value = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    features_cn = models.TextField(null=True)
    features_en = models.TextField(null=True)
    expire_date = models.DateField(null=True)
    target_members = models.ManyToManyField(Member)
    target_companies = models.ManyToManyField(Company)
    target_industries = models.ManyToManyField(Industry)


    is_anonymous = models.BooleanField(default=0)
    is_public = models.BooleanField(default=0)
    is_suitor = models.BooleanField(default=0)
    is_follow = models.BooleanField(default=0)
    upload_file = models.FileField(upload_to='project/', blank=True, default='')
    cv1 = models.IntegerField(blank=True, null=True)
    cv2 = models.IntegerField(blank=True, null=True)
    cv3 = models.IntegerField(blank=True, null=True)
    deal_size = models.BigIntegerField(blank=True, null=True)
    stock_percent = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    ebitda = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    has_attach = models.BooleanField(default=0)
    is_agent_project = models.BooleanField(default=0)

    project_relation = models.IntegerField(choices=RELATE_PROJECT, null=True, blank=True)
    project_stage = models.IntegerField(null=True, blank=True)
    valid_day = models.IntegerField(choices=VALID_DAY, null=True, blank=True)
    income_last_phase_2 = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    profit_last_phase_2 = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    income_last_phase_3 = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    profit_last_phase_3 = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    total_assets_last_phase_2 = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    total_assets_last_phase_3 = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    total_profit_last_phase = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    total_profit_last_phase_2 = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    total_profit_last_phase_3 = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    ebitda_2 = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    ebitda_3 = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    audit_status = models.IntegerField(choices=AUDIT_STATUS, null=True, blank=True)
    audit_status_2 = models.IntegerField(choices=AUDIT_STATUS, null=True, blank=True)
    audit_status_3 = models.IntegerField(choices=AUDIT_STATUS, null=True, blank=True)
    income_type = models.IntegerField(choices=FINANCIAL_TYPES, null=True, blank=True)
    profit_type = models.IntegerField(choices=FINANCIAL_TYPES, null=True, blank=True)
    process = models.IntegerField(choices=PROCESS, null=True, blank=True)
    integrity = models.IntegerField(null=True, blank=True)
    integrity_en = models.IntegerField(null=True, blank=True)
    pay_currency = models.IntegerField(choices=PAY_CURRENCY, null=True, blank=True)
    # other_target_companies = models.TextField(null=True)
    is_recommend = models.BooleanField(default=0)
    is_top = models.BooleanField(default=0)
    deal_type = models.ManyToManyField(DetailDealType)
    create_source = models.IntegerField(choices=CREATE_SOURCE,  default=0)
    multi_currency = models.CharField(max_length=10, blank=True, null=True)
    target_platform = models.IntegerField(choices=TARGET_PLATFORM,  default=0)

    def __unicode__(self):
        return self.name_en

    def project_stage_name(self):
        reVal = u"未公布"
        if self.project_stage:
            reVal = SubDetailDealType.objects.get(pk=self.project_stage).name_cn
        return reVal

    def project_multi_currency(self):
        currencies = (
            (1, u'人民币'),
            (2, u'美元'),
            (3, u'欧元'),
        )
        if self.multi_currency:
            currency_array = [int(cur) for cur in self.multi_currency.split(",")]
            currencies_str_lst = [text for val, text in currencies if val in currency_array]
            return ",".join(currencies_str_lst)
        return ""

    class Meta:
        db_table = 'project_project'


class ProjectOtherTargetCompany(models.Model):
    TYPES = (
        (1, _('repository_investmentcompany')),
        (2, _('repository_listedcompany')),
    )
    project = models.ForeignKey(Project, related_name='project_other_company')
    company_id = models.IntegerField(blank=True, null=True)
    name_cn = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    short_name_cn = models.CharField(max_length=20, blank=True)
    short_name_en = models.CharField(max_length=20, blank=True)
    table_name = models.IntegerField(choices=TYPES, default=1)

    class Meta:
        db_table = 'project_other_target_company'



class ProjectCustomerTargetCompany(models.Model):
    TYPES = (
        (0, _('newchama company')),
        (1, _('investment company')),
        (2, _('listed company')),
    )
    project = models.ForeignKey(Project, related_name='project_customer_target_company')
    company_id = models.IntegerField( blank=True,null=True)
    company_name_cn = models.CharField(max_length=255, blank=True,null=True)
    company_name_en = models.CharField(max_length=255, blank=True,null=True)
    company_short_name_cn = models.CharField(max_length=20, blank=True,null=True)
    company_short_name_en = models.CharField(max_length=20, blank=True,null=True)
    company_logo=models.CharField(max_length=255, blank=True,null=True)
    is_man = models.BooleanField(default=0)
    is_star = models.BooleanField(default=0)
    has_user = models.BooleanField(default=0)
    is_delete = models.BooleanField(default=0)
    rank = models.IntegerField(default=0)
    company_field = models.CharField(max_length=200, blank=True,null=True)
    company_type = models.IntegerField(choices=TYPES, default=0)
    target_reason=models.CharField(max_length=255, blank=True,null=True)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_customer_target_company'

    def company_type_name(self):
        if self.company_type==0:
             return 'Newchama用户'
        elif self.company_type==1:
            return '投资机构'
        else:
            return '上市公司'
    def target_reason_cn(self):
        if self.target_reason=='invested in similar companies':
            return '投资过类似公司'
        elif self.target_reason=='public company within the same industry':
            return '同行业'
        elif self.target_reason=='investment orientation':
            return '有投资方向'
        elif self.target_reason=='relate buy-side mandate':
            return '有相关需求'
        elif self.target_reason=='investor within the same industry':
            return '投资过相同行业'
    def has_user_cn(self):
        if self.has_user:
            return 'Y'
        else:
            return 'N'


class ProjectAttach(models.Model):
    project = models.ForeignKey(Project, related_name='project_attach')
    file_type = models.CharField(max_length=50)
    file_type_name = models.CharField(null=True, max_length=100)
    file_name = models.CharField(max_length=100)
    new_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.file_name

    class Meta:
        db_table = 'project_projectAttach'


class ProjectOneclickAttach(models.Model):
    STATUS_TYPES = (
        (0, _('Pending')),
        (1, _('Not approved')),
        (2, _('Approved')),
        (3, _('Deleted')),
    )
    file_type = models.CharField(max_length=50)
    file_size = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    file_name = models.CharField(max_length=100)
    new_name = models.CharField(max_length=100)
    member = models.ForeignKey(Member, related_name='onclick_publisher')
    status = models.IntegerField(choices=STATUS_TYPES, default=0)
    project = models.ForeignKey(Project, related_name='project_oneclick_attach', null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(default=datetime.datetime.now(), auto_now=True)

    def __unicode__(self):
        return self.file_name

    class Meta:
        db_table = 'project_oneclickAttach'


class StockStructure(models.Model):
    TYPES = (
        (1, 'Management'),
        (2, 'Institutional'),
        (3, 'Personal'),
    )
    project = models.ForeignKey(Project, related_name='project_stock_structure')
    name_cn = models.CharField(max_length=255, null=True, default='')
    name_en = models.CharField(max_length=255, null=True, default='')
    type = models.IntegerField(choices=TYPES, default=1)
    rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'project_stockstructure'


class StatusProject(object):
    pending = 0
    not_approved = 1
    approved = 2
    offline = 3
    draft = 4
    deleted = 5


class ProjectServiceType(object):
    additonalIssue = 6


class ProjectViewLog(models.Model):
    member = models.ForeignKey(Member, related_name='project_view_log_member')
    project = models.ForeignKey(Project, related_name='project_view_log_project')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_view_log'


class ProjectCheckLog(models.Model):
    Results_Check = (
        (3, 'offline'),
        (2, 'Approve'),
        (1, 'Disapprove'),
    )
    adminuser = models.ForeignKey(AdminUser, related_name='project_check_log_adminuser')
    project = models.ForeignKey(Project, related_name='project_check_log_project')
    reason = models.TextField(null=True)
    result = models.IntegerField(default=1, choices=Results_Check)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_check_log'


class ResultsProjectCheck(object):
    offline = 3
    approve = 2
    disapprove = 1


class ProjectKeyword(models.Model):
    project = models.ForeignKey(Project, related_name='project_keyword')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'project_keyword'


class ProjectTag(models.Model):
    project = models.ForeignKey(Project, related_name='project_tag')
    tag = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'project_tag'


class ProjectKeywordEn(models.Model):
    project = models.ForeignKey(Project, related_name='project_keyword_en')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'project_keyword_en'


class ProjectKeywordAdmin(models.Model):
    project = models.ForeignKey(Project, related_name='project_keyword_admin')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'project_keyword_Admin'


class ProjectRecommondReasonAdmin(models.Model):
    project = models.ForeignKey(Project, related_name='project_recommond_reason_admin')
    reason = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'project_admin_recommond_reason'


class ProjectPrintLog(models.Model):
    member = models.ForeignKey(Member, related_name='project_print_log_member')
    project = models.ForeignKey(Project, related_name='project_print_log_project')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_print_log'


class ProjectDownloadLog(models.Model):
    member = models.ForeignKey(Member, related_name='project_download_log_member')
    project = models.ForeignKey(Project, related_name='project_download_log_project')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_download_log'


class ProjectRecommendLog(models.Model):
    TYPES = (
        (1, 'recommend'),
        (2, 'top'),
    )
    project = models.ForeignKey(Project, related_name='project_recommend_log_project')
    add_time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=TYPES, default=1)

    class Meta:
        db_table = 'project_recommend_log'


class TypeProjectRecommend(object):
    recommend = 1
    top = 2

