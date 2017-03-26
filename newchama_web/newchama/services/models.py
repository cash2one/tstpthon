# -*- coding: utf-8 -*-  
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
# Create your models here.


class Continent(models.Model):
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'area_continent'


class Country(models.Model):
    continent = models.ForeignKey(Continent)
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)
    intel_code = models.CharField(max_length=10, null=True)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'area_country'


class Province(models.Model):
    country = models.ForeignKey(Country)
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'area_province'


class City(models.Model):
    province = models.ForeignKey(Province)
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'area_city'


class Industry(models.Model):
    name_cn = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    level = models.IntegerField(default=0)
    father = models.ForeignKey('self', null=True, blank=True)
    is_display = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'industry_industry'


class StockExchange(models.Model):
    name_cn = models.CharField(max_length=50, blank=True)
    name_en = models.CharField(max_length=50, blank=True)
    short_name_en = models.CharField(max_length=50, blank=True)
    short_name_cn = models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'repository_stockexchange'


class ListedCompany(models.Model):
    name_cn = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    short_name_cn = models.CharField(max_length=20, blank=True)
    short_name_en = models.CharField(max_length=20, blank=True)
    intro_cn = models.TextField(blank=True, null=True)
    intro_en = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    province = models.ForeignKey(Province, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    industry = models.ForeignKey(Industry, blank=True, null=True)
    address_cn = models.CharField(max_length=255, blank=True)
    address_en = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    stock_exchange = models.ForeignKey(StockExchange)
    stock_symbol = models.CharField(max_length=50)
    stock_symbol_no_pre = models.CharField(max_length=20)
    stock_name = models.CharField(max_length=20)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    found_time = models.DateTimeField(null=True, blank=True)
    invest_field = models.TextField(blank=True, null=True)
    memo = models.TextField( blank=True, null=True)

    def __unicode__(self):
        return self.short_name_en

    class Meta:
        db_table = 'repository_listedcompany'


class CompanyWithPE(models.Model):
    name = models.CharField(max_length=100, blank=True)
    symbol = models.CharField(max_length=50, blank=True)
    exchange = models.CharField(max_length=50, blank=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    industry = models.ForeignKey(Industry, blank=True, null=True)
    pe = models.FloatField(default=0)
    pb = models.FloatField(default=0)
    ps = models.FloatField(default=0)
    marketCapital = models.BigIntegerField(default=0)

    def __unicode__(self):
        return self.exchange+":"+self.symbol

    class Meta:
        db_table = 'repository_compare_company'


class IndustryWithPE(models.Model):
    
    country = models.ForeignKey(Country, blank=True, null=True)
    industry = models.ForeignKey(Industry, blank=True, null=True)
    pe = models.FloatField(default=0)
    pb = models.FloatField(default=0)
    ps = models.FloatField(default=0)

    def __unicode__(self):
        return self.country.name_en+":"+self.industry.name_en

    class Meta:
        db_table = 'repository_industry_pe'


class AccountingFirm(models.Model):
    name_cn = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    short_name_cn = models.CharField(max_length=20, blank=True)
    short_name_en = models.CharField(max_length=20, blank=True)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.short_name_en

    class Meta:
        db_table = 'repository_accountingfirm'



class Company(models.Model):
    TYPES = (
        (1, _('Listed')),
        (2, _('UnListed')),
        (3, _('Investment')),
        (4, _('Service')),
        (6, _('Prvate Equity')),
        (7, _('Ventue Capital')),
        (5, _('Other')),
    )
    STATUS_TYPES = (
        (0, _('NotAccount')),
        (1, _('Normal')),
        (2, _('Abnormal')),
        (3, _('Deleted')),
    )
    Capital_TYPES = (
        (1, _('RMB Capital')),
        (2, _('USD Capital')),
        (3, _('EUR Capital')),
        (4, _('Other Currency Capital')),
        (5, _('Mixed Capital')),
    )
    name_cn = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    short_name_cn = models.CharField(max_length=255, null=True, blank=True)
    short_name_en = models.CharField(max_length=255, null=True, blank=True)
    intro_cn = models.TextField(null=True, blank=True)
    intro_en = models.TextField(null=True, blank=True)
    investment_experience_cn = models.TextField(null=True, blank=True)
    investment_experience_en = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    province = models.ForeignKey(Province, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    industry = models.ForeignKey(Industry, null=True, blank=True)
    address_cn = models.CharField(max_length=255, null=True, blank=True)
    address_en = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    
    postcode = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='companylogo/', blank=True, default='')
    type = models.IntegerField(choices=TYPES, default=0)
    intro_file = models.FileField(upload_to='companyfile/', blank=True, default='')
    add_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, default=datetime.datetime.now())
    status = models.IntegerField(choices=STATUS_TYPES, default=0)
    capital_type = models.IntegerField(choices=Capital_TYPES, default=1)
    found_time = models.DateTimeField(null=True, blank=True)
    parent_company = models.ForeignKey('self', null=True, blank=True)
    data_source = models.CharField(max_length=20, blank=True, null=True)
    memo = models.TextField( blank=True, null=True)

    def __unicode__(self):
        return self.short_name_cn

    @staticmethod
    def active_list():
        return Company.objects.filter(status=1).exclude(id=27).values("id",  "name_cn", "name_en", "short_name_cn", "short_name_en")

    class Meta:
        db_table = 'member_company'

class CompanyStockSymbol(models.Model):
    company = models.ForeignKey(Company)
    stock_exchange = models.ForeignKey(StockExchange, null=True, blank=True)
    stock_symbol = models.CharField(max_length=20, blank=True, null=True)
    stock_symbol_no_pre = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.stock_symbol
    class Meta:
        db_table = 'member_company_symbol'



class CompanyInvestmentField(models.Model):
    DEAL_TYPES = (
        (0, _('Unknow')),
        (99, _('Unlimited')),
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
        (0, _('Unknow')),
        (99, _('Unlimited')),
        (1, _('CNY')),
        (2, _('USD')),
        (3, _('EUR')),
        (4, _('OTHER')),
    )
   
    FINANCE_TYPES = (        
        (0, _('Unknow')),
        (99, _('Unlimited')),
        (1, _('Less than 10M')),
        (2, '10-20M'),
        (3, '20-50M'),
        (4, '50-100M'),
        (5, '100-200M'),
        (6, '200-300M'),
        (7, '300-500M'),
        (8, '500-1000M'),
        (9, '1000-2000M'),
        (10, '2000-3000M'),
        (11, _('More than 3000M')),
        
    )
    GROWTH_TYPES = (        
        (0, _('Unknow')),
        (99, _('Unlimited')),
        (1, _('Less than 10%')),
        (2, '10-30%'),
        (3, '30-50%'),
        (4, '50-70%'),
        (5, '70-100%'),
        (6, '100-150%'),
        (7, _('More than 150%')),
        
    )

    company = models.ForeignKey(Company)
    tags = models.CharField(max_length=400, blank=True, null=True)

    revenue=models.IntegerField(choices=FINANCE_TYPES, default=0)
    growth=models.IntegerField(choices=GROWTH_TYPES, default=0)
    net_income=models.IntegerField(choices=FINANCE_TYPES, default=0)
    ebita=models.IntegerField(choices=FINANCE_TYPES, default=0)


    deal_type = models.IntegerField(choices=DEAL_TYPES, default=0)
    deal_currency = models.IntegerField(choices=CURRENCY_TYPES, default=0)
    deal_size=models.IntegerField(choices=FINANCE_TYPES, default=0)
    deal_size_min =models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    deal_size_max =models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    country=models.ForeignKey(Country, null=True, blank=True)
    hot=models.IntegerField(default=5)

    add_time=models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.tags
    class Meta:
        db_table = 'member_companyinvestmentfield'



class CompanyInvestmentHistory(models.Model):
    
    company = models.ForeignKey(Company)
    country = models.ForeignKey(Country, null=True, blank=True)
    province = models.ForeignKey(Province, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    industry = models.ForeignKey(Industry, null=True, blank=True)
    happen_date = models.DateTimeField(null=True, blank=True)
    title_cn = models.CharField(max_length=200, blank=True, null=True)
    title_en = models.CharField(max_length=200, blank=True, null=True)
    content_cn = models.TextField(null=True, blank=True,default='')
    content_en = models.TextField(null=True, blank=True,default='')
    invest_type = models.CharField(max_length=50, blank=True, null=True)
    invest_stage = models.CharField(max_length=50, blank=True, null=True)
    targetcompany_cn = models.CharField(max_length=100, blank=True, null=True)
    targetcompany_en = models.CharField(max_length=100, blank=True, null=True)
    cv1 = models.IntegerField(blank=True, null=True)
    cv2 = models.IntegerField(blank=True, null=True)
    cv3 = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    person_cn = models.CharField(max_length=100, blank=True, null=True)
    person_en = models.CharField(max_length=100, blank=True, null=True)
    usd = models.IntegerField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.title_cn

    class Meta:
        db_table = 'member_companyinvestmenthistory'



class InvestmentCompany(models.Model):
    Capital_TYPES = (
        (1, _('Chinese Capital')),
        (2, _('Foreign Capital')),
        (3, _('Mixed Capital')),
    )
    name_cn = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    short_name_cn = models.CharField(max_length=50, blank=True)
    short_name_en = models.CharField(max_length=50, blank=True)
    intro_cn = models.TextField(blank=True, null=True)
    intro_en = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    province = models.ForeignKey(Province, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    
    address_cn = models.CharField(max_length=255, null=True, blank=True)
    address_en = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    stock_exchange = models.ForeignKey(StockExchange, null=True, blank=True)
    stock_symbol = models.CharField(max_length=20, blank=True, null=True)
    stock_symbol_no_pre = models.CharField(max_length=20, blank=True, null=True)
    capital_type = models.IntegerField(choices=Capital_TYPES, default=1)
    found_time = models.DateTimeField(null=True, blank=True)
    invest_field = models.TextField(blank=True, null=True)
    memo = models.TextField( blank=True, null=True)

    def __unicode__(self):
        return self.short_name_en

    class Meta:
        db_table = 'repository_investmentcompany'


class InvestmentHistory(models.Model):
    Capital_TYPES = (
        (1, _('Chinese Capital')),
        (2, _('Foreign Capital')),
        (3, _('Mixed Capital')),
    )
    company = models.ForeignKey(InvestmentCompany)
    happen_date = models.DateTimeField(null=True)
    content = models.TextField()
    type = models.CharField(max_length=50, null=True, blank=True)
    targetcompany = models.CharField(max_length=100, null=True, blank=True)
    cv1 = models.IntegerField(blank=True, null=True)
    cv2 = models.IntegerField(blank=True, null=True)
    cv3 = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    province_id = models.IntegerField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=50, null=True, blank=True)
    person = models.CharField(max_length=100, null=True, blank=True)
    usd = models.BigIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.content

    class Meta:
        db_table = 'repository_investmenthistory'



class StatusMember(object):
    normal = 1
    abnormal = 2
    mustchangepassword = 3
    activing = 4


class TypeMember(object):
    test = 1
    normal = 2
    useradd = 3
    bdadd = 4


class TypeGender(object):
    male = 1
    female = 2


class TypeFavorite(object):
    project = 1
    demand = 2
    company = 3
    member = 4
    data = 5
    news = 6


class StatusDemand(object):
    pending = 0
    not_approved = 1
    approved = 2
    offline = 3
    draft = 4
    deleted = 5


class StatusProject(object):
    pending = 0
    not_approved = 1
    approved = 2
    offline = 3
    draft = 4
    deleted = 5


class LoginType(object):
    weixin = 1
    weibo = 2
    linkedin = 3


class ProjectServiceType(object):
    additonalIssue = 6


class OtherLogin(models.Model):
    TYPES = (
        (1, _('weixin')),
        (2, _('weibo')),
        (3, _('linkedin')),
    )
    access_token = models.CharField(max_length=50, blank=True)
    uid = models.BigIntegerField(default=0)
    expires_in = models.BigIntegerField(default=0)
    login_type = models.IntegerField(default=0, choices=TYPES)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.access_token

    class Meta:
        db_table = 'other_login'


class Member(models.Model):
    GENDER_TYPE = (
        (1, _('Male')),
        (2, _('Female')),
    )
    TYPES = (
        (1, _('Test')),
        (2, _('Normal')),
        (3, _('UserAdd')),
        (4, _('BDAdd')),
    )
    STATUS_TYPE = (
        (1, _('Normal')),
        (2, _('Abnormal')),
        (3, _('MustChangePassword')),
        (4, _('Activing')),
    )
    company = models.ForeignKey(Company)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.IntegerField(default=0, choices=GENDER_TYPE)
    position_cn = models.CharField(max_length=20, blank=True)
    position_en = models.CharField(max_length=50, blank=True)
    tel_intel = models.CharField(max_length=10, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    mobile_intel = models.CharField(max_length=10, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    invite_user = models.ForeignKey('self', blank=True, null=True)
    invite_code = models.CharField(max_length=20, blank=True)
    type = models.IntegerField(default=0, choices=TYPES)
    expire_date = models.DateField(null=True, blank=True, default=None)
    status = models.IntegerField(default=0, choices=STATUS_TYPE)
    intro_cn = models.TextField(blank=True)
    intro_en = models.TextField(blank=True)
    last_login_time = models.DateTimeField(null=True)
    login_count = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to="avatars/origin/", blank=True, default='default.jpg')
    focus_aspect = models.ManyToManyField(Industry)
    activecode=models.CharField(max_length=50, blank=True,null=True)
    creator_id = models.IntegerField(blank=True, null=True)
    owner_id = models.IntegerField(blank=True, null=True)
    weixin = models.ForeignKey(OtherLogin, blank=True, null=True,related_name="weixin")
    weibo = models.ForeignKey(OtherLogin, blank=True, null=True,related_name="weibo")
    linkedin = models.ForeignKey(OtherLogin, blank=True, null=True,related_name="linkedin")

    def __unicode__(self):
        return self.last_name + " " + self.first_name

    @property
    def fullname(self):
        return self.last_name + " " + self.first_name

    def make_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def companyNameCn(self):
        return self.company.name_cn

    def company_address(self):
        return self.company.address_cn

    def company_website(self):
        return self.company.website

    def company_introduction_cn(self):
        return self.company.intro_cn

    def companyType(self):
        return self.company.type

    def company_introduction(self):
        return self.company.intro_cn

    def member_focus_aspect(self):
        fas = self.focus_aspect.all()
        aspects = {}
        if fas:
            for f in fas:
                aspects[f.id] = f.name_cn
        return aspects

    def view_project(self, project):
        if project.member_id != self.id:
            view_log = ProjectViewLog()
            view_log.project = project
            view_log.member = self
            view_log.save()
            project.pv += 1
            project.save()
            ProjectVisitor.objects.filter(project=project, member=self).delete()
            visitor = ProjectVisitor()
            visitor.member = self
            visitor.project = project
            visitor.save()

    def view_demand(self, demand):
        if demand.member_id != self.id:
            view_log = DemandViewLog()
            view_log.demand = demand
            view_log.member = self
            view_log.save()
            demand.pv += 1
            demand.save()
            DemandVisitor.objects.filter(demand=demand, member=self).delete()
            visitor = DemandVisitor()
            visitor.member = self
            visitor.demand = demand
            visitor.save()

    def print_project(self, project):
        if project.member_id != self.id:
            print_log = ProjectPrintLog()
            print_log.project = project
            print_log.member = self
            print_log.save()

    def download_project_attach(self, project):
        if project.member_id != self.id:
            download_log = ProjectDownloadLog()
            download_log.project = project
            download_log.member = self
            download_log.save()

    def print_demand(self, demand):
        if demand.member_id != self.id:
            print_log = DemandPrintLog()
            print_log.demand = demand
            print_log.member = self
            print_log.save()

    def download_demand_attach(self, demand):
        if demand.member_id != self.id:
            download_log = DemandDownloadLog()
            download_log.demand = demand
            download_log.member = self
            download_log.save()

    def add_project_to_favorites(self, project):
        self.remove_project_from_favorites(project)
        f = Favorites()
        f.project = project
        f.member = self
        f.type_relation = 1
        f.save()

    def add_demand_to_favorites(self, demand):
        self.remove_demand_from_favorites(demand)
        f = Favorites()
        f.demand = demand
        f.member = self
        f.type_relation = 2
        f.save()

    def add_company_to_favorites(self, company):
        self.remove_company_from_favorites(company)
        f = Favorites()
        f.company = company
        f.member = self
        f.type_relation = 3
        f.save()

    def add_member_to_favorites(self, member):
        self.remove_member_from_favorites(member)
        f = Favorites()
        f.receiver = member
        f.member = self
        f.type_relation = 4
        f.save()

    def add_data_to_favorites(self, data):
        self.remove_data_from_favorites(data)
        f = Favorites()
        f.data = data
        f.member = self
        f.type_relation = 5
        f.save()

    def add_news_to_favorites(self, news):
        self.remove_news_from_favorites(news)
        f = Favorites()
        f.news = news
        f.member = self
        f.type_relation = 6
        f.save()

    def remove_project_from_favorites(self, project):
        Favorites.objects.filter(member_id=self.id, project_id=project.id).delete()

    def remove_demand_from_favorites(self, demand):
        Favorites.objects.filter(member_id=self.id, demand_id=demand.id).delete()

    def remove_company_from_favorites(self, company):
        Favorites.objects.filter(member_id=self.id, company_id=company.id).delete()

    def remove_member_from_favorites(self, member):
        Favorites.objects.filter(member_id=self.id, receiver_id=member.id).delete()

    def remove_data_from_favorites(self, data):
        Favorites.objects.filter(member_id=self.id, data_id=data.id).delete()

    def remove_news_from_favorites(self, news):
        Favorites.objects.filter(member_id=self.id, news_id=news.id).delete()

    def is_added_project_to_favorites(self, project):
        return Favorites.objects.filter(member_id=self.id, project_id=project.id).count() > 0

    def is_added_demand_to_favorites(self, demand):
        return Favorites.objects.filter(member_id=self.id, demand_id=demand.id).count() > 0

    def is_added_company_to_favorites(self, company):
        return Favorites.objects.filter(member_id=self.id, company_id=company.id).count() > 0

    def is_added_member_to_favorites(self, member):
        return Favorites.objects.filter(member_id=self.id, receiver_id=member.id).count() > 0

    def is_added_news_to_favorites(self, news):
        return Favorites.objects.filter(member_id=self.id, news_id=news.id).count() > 0

    def is_added_deal_to_favorites(self, deal):
        return Favorites.objects.filter(member_id=self.id, deal_id=deal.id).count() > 0


    @staticmethod
    def active_list():
        return Member.objects.filter(status=1).values("id", "email", "first_name", "last_name")

    @staticmethod
    def login(username, password):
        try:
            m = Member.objects.get(Q(email=username) | Q(mobile=username))
            if m.check_password(password):
                if m.status == StatusMember.abnormal:
                    return _("Your account has bean locked. Please contact customer services."), False
                
                elif datetime.datetime.now().strftime("%Y-%m-%d") >= m.expire_date.strftime("%Y-%m-%d"):
                    return _("Your account has expired. Please contact customer services."), False
                return m, True
            else:
                return _("Login failed. Please confirm your password."), False
        except ObjectDoesNotExist:
            return _("Login failed. Please confirm your account."), False

    class Meta:
        db_table = 'member_member'


class MemberFocusKeyword(models.Model):
    member = models.ForeignKey(Member, related_name='member_focus_keyword')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'member_focus_keyword'


class AccessToken(models.Model):
    member = models.ForeignKey(Member, blank=True, null=True)
    access_token = models.CharField(max_length=50, blank=True)
    login_date = models.DateTimeField(default=datetime.datetime.now())
    class Meta:
        db_table = 'member_accesstoken'


class MobileValidCode(models.Model):
    mobile = models.CharField(max_length=20, blank=True)
    valid_code = models.CharField(max_length=6, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mobile_validcode'


class EntryForm(models.Model):
    GENDER_TYPE = (
        (1, _('Male')),
        (2, _('Female')),
    )
    STATUS_TYPE = (
        (0, _('Pending')),
        (1, _('Not approved')),
        (2, _('Approved')),
    )
    COMPANY_TYPE = (
        (1, _('Listed')),
        (2, _('UnListed')),
        (3, _('Investment')),
        (4, _('Service')),
        (5, _('Other')),
    )
    email = models.EmailField()
    invite_code = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    gender = models.IntegerField(default=0, choices=GENDER_TYPE)
    position = models.CharField(max_length=20, blank=True)
    tel_intel = models.CharField(max_length=10, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    mobile_intel = models.CharField(max_length=10, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    company_type = models.IntegerField(default=0, choices=COMPANY_TYPE)
    company = models.CharField(max_length=255)
    country = models.ForeignKey(Country, blank=True, null=True)
    province = models.ForeignKey(Province, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    industry = models.ForeignKey(Industry, blank=True, null=True)
    fullname = models.CharField(max_length=50)
    status = models.IntegerField(default=0, choices=STATUS_TYPE)

    def __unicode__(self):
        return self.fullname

    def make_password(self, raw_password):
        self.password = make_password(raw_password)

    class Meta:
        db_table = 'member_entryform'


class FindPasswordHistory(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=50)
    add_time = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    used_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.email

    class Meta:
        db_table = 'member_findpasswordhistory'


class InviteCode(models.Model):
    invite_user = models.ForeignKey(Member, blank=True, null=True)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    add_time = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    used_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.code

    class Meta:
        db_table = 'member_invitecode'


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
        # (0, _('No audited')),
        # (1, _('Big four')),
        # (2, _('Not big four')),
        (1, _('Audited')),
        (2, _('Reviewed')),
        (3, _('Compiled')),
        (0, _('Internal')),
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

    def is_push_to_member(self, member):
        try:
            is_target_member = self.target_members.filter(id=member.id).count() > 0
            condition_industry = Q(id=member.company.industry_id) | Q(father_id=member.company.industry_id) | Q(father__father_id=member.company.industry_id)
            is_target_industry = self.target_industries.filter(condition_industry).count() > 0
            is_target_company = self.target_companies.filter(id=member.company.id).count() > 0
            return is_target_member and is_target_industry and is_target_company
        except Exception, e:
            return False

    def member_name(self):
        return self.member.fullname

    def member_job_title(self):
        return self.member.position_cn

    def member_avatar(self):
        return unicode(self.member.avatar)

    def company_tag(self):
        return ProjectTag.objects.filter(project=self).all()

    def companyIndustry(self):
        industrys = DemandIndustry.objects.filter(demand=self).all()
        companyIndustry = ""
        a=0
        if industrys:
            for i in industrys:
                companyIndustry = 'cv1:'+str(i.cv1)+','+'cv2:'+str(i.cv2)+','+'cv3:'+str(i.cv3)
        return companyIndustry

    def new_employees_count_type(self):
        if self.employees_count_type == 0:
            self.employees_count_type = 1
        return self.employees_count_type

    def favorite_times(self):
        return Favorites.objects.filter(project=self).count()

    def message_times(self):
        return Message.objects.filter(project=self).count()

    class Meta:
        db_table = 'demand_demand'


class DemandRecommondReasonAdmin(models.Model):
    project = models.ForeignKey(Demand, related_name='demand_recommond_reason_admin')
    reason = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'demand_admin_recommond_reason'


class DemandKeyword(models.Model):
    demand = models.ForeignKey(Demand, related_name='demand_keyword')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'demand_keyword'


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


class Project(models.Model):
    PROJECT_RANGE = (
        ("0:500", _('Less than 500')),
        ("501:1000", '501-1000'),
        ("1001:2000", '1001-2000'),
        ("2001:3000", '2001-3000'),
        ("3001:4000", '3001-4000'),
        ("4001:5000", '4001-5000'),
        ("5001:0", _('More than 5001')),
    )
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
        (4, _('Buyout or Financing')),
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
        # (0, _('No audited')),
        # (1, _('Big four')),
        # (2, _('Not big four')),
        (1, _('Audited')),
        (2, _('Reviewed')),
        (3, _('Compiled')),
        (0, _('Internal')),
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
    currency_type_service = models.IntegerField(choices=CURRENCY_TYPES, null=True, blank=True,)
    company_symbol_en = models.CharField(null=True, max_length=50)
    company_name_en = models.CharField(null=True, max_length=255)
    company_symbol_cn = models.CharField(null=True, max_length=50)
    company_name_cn = models.CharField(null=True, max_length=255)
    is_list_company = models.BooleanField(default=0)
    company_country = models.ForeignKey(Country, null=True, blank=True)
    company_province = models.ForeignKey(Province, null=True, blank=True)
    company_cities = models.ForeignKey(City, null=True, blank=True)
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
    project_stage = models.IntegerField(choices=INVESTMENT_STAGE, null=True, blank=True)
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

    def __unicode__(self):
        return self.name_en

    def is_push_to_member(self, member):
        # is_target_member = self.target_members.filter(id=member.id).count() > 0
        # condition_industry = Q(id=member.company.industry_id) | Q(father_id=member.company.industry_id) | Q(father__father_id=member.company.industry_id)
        # is_target_industry = self.target_industries.filter(condition_industry).count() > 0
        # is_target_company = self.target_companies.filter(id=member.company.id).count() > 0
        # return is_target_member and is_target_company
        try:
            is_target_company = ProjectTargetCompanyDetail.objects.filter(company=member.company.id, project_id=self.id)
            return len(is_target_company) > 0
        except Exception, e:
            return False


    def member_name(self):
        return self.member.fullname

    def member_job_title(self):
        return self.member.position_cn

    def member_avatar(self):
        return unicode(self.member.avatar)

    def company_tag(self):
        tags = ProjectTag.objects.filter(project=self).all()
        company_tag = {}
        if tags:
            for t in tags:
                company_tag[t.id]=t.tag
        return company_tag

    def companyIndustry(self):
        if self.company_industry:
            return self.company_industry.name_cn
        else:
            return self.company_industry

    def companyCountry(self):
        if self.company_country:
            return self.company_country.name_cn
        else:
            return self.company_country

    def companyProvince(self):
        if self.company_province:
            return self.company_province.name_cn
        else:
            return self.company_province

    def companyCity(self):
        if self.company_cities:
            return self.company_cities.name_cn
        else:
            return self.company_cities

    def new_employees_count_type(self):
        if self.employees_count_type == 0:
            self.employees_count_type = 1
        return self.employees_count_type

    def favorite_times(self):
        return Favorites.objects.filter(project=self).count()

    def message_times(self):
        return Message.objects.filter(project=self).count()

    class Meta:
        db_table = 'project_project'

class ProjectTag(models.Model):
    project = models.ForeignKey(Project, related_name='project_tag')
    tag = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'project_tag'

class ProjectOtherTargetCompany(models.Model):
    TYPES = (
        (1, _('repository_investmentcompany')),
        (2, _('repository_listedcompany')),
    )
    project = models.ForeignKey(Project, related_name='project_other_company')
    name_cn = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    short_name_cn = models.CharField(max_length=20, blank=True)
    short_name_en = models.CharField(max_length=20, blank=True)
    table_name = models.IntegerField(choices=TYPES, default=1)
    company_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'project_other_target_company'


class ProjectRecommondReasonAdmin(models.Model):
    project = models.ForeignKey(Project, related_name='project_recommond_reason_admin')
    reason = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'project_admin_recommond_reason'


class ProjectKeyword(models.Model):
    project = models.ForeignKey(Project, related_name='project_keyword')
    keyword = models.CharField(max_length=255, null=True, default='')

    def __unicode__(self):
        return self.keyword

    def member_avatar(self):
        return unicode(self.project.member.avatar)

    def member_name(self):
        return self.project.member.fullname

    def company_name(self):
        return self.project.company_name_cn

    def member_job_title(self):
        return self.project.member.position_cn

    def company_tag(self):
        tags = ProjectTag.objects.filter(project=self).all()
        company_tag = {}
        if tags:
            for t in tags:
                company_tag[t.id]=t.tag
        return company_tag

    def project_name(self):
        return self.project.name_cn

    def company_industry(self):
        return self.project.companyIndustry()

    def pv(self):
        return self.project.pv

    def favorite_times(self):
        return self.project.favorite_times()

    def message_times(self):
        return self.project.message_times()

    def expected_enterprice_value(self):
        return self.project.expected_enterprice_value

    def stock_percent(self):
        return  self.project.stock_percent



    class Meta:
        db_table = 'project_keyword'


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


class ProjectAttach(models.Model):
    project = models.ForeignKey(Project, related_name='project_attach')
    file_type = models.CharField(max_length=50)
    file_type_name = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    new_name = models.CharField(max_length=100)

    def projectName(self):
        return self.project.name_cn

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
        (1, _('Management')),
        (2, _('Institutional')),
        (3, _('Personal')),
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


class Preference(models.Model):
    TITLE_PREFERENCE = (
        ("news", 'news'),
        ("project", 'project'),
        ("demand", 'demand'),
    )
    member = models.ForeignKey(Member, related_name='member_preference')
    title = models.CharField(max_length=255, null=True, default='')
    add_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(default=datetime.datetime.now(), auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'member_preference'


class PreferenceIndustry(models.Model):
    CURRENCY_TYPES = (
        (1, _('CNY')),
        (2, _('USD')),
        #(3, 'EUR'),
    )
    preference = models.ForeignKey(Preference, related_name='preference_industry')
    currency_type_financial = models.IntegerField(choices=CURRENCY_TYPES, default=1)
    industry = models.ForeignKey(Industry)
    country = models.ForeignKey(Country, null=True, blank=True)
    range_min = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    range_max = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    class Meta:
        db_table = 'member_preference_industry'


class PreferenceLocation(models.Model):
    preference = models.ForeignKey(Preference, related_name='preference_location')
    country = models.ForeignKey(Country, null=True, blank=True)
    province = models.ForeignKey(Province, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'member_preference_location'


class PreferenceKeyword(models.Model):
    preference = models.ForeignKey(Preference, related_name='preference_keyword')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'member_preference_keyword'


class Message(models.Model):
    TYPES_RELATION = (
        (0, 'Normal'),
        (1, 'Project'),
        (2, 'Demand'),
    )
    sender = models.ForeignKey(Member, related_name="member_sender")
    receiver = models.ForeignKey(Member, related_name="member_receiver")
    content = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)
    is_read = models.IntegerField(default=0)
    is_delete = models.IntegerField(default=0)
    project = models.ForeignKey(Project, null=True, blank=True)
    demand = models.ForeignKey(Demand, null=True, blank=True)
    type_relation = models.IntegerField(default=0, choices=TYPES_RELATION)

    def __unicode__(self):
        return self.content

    class Meta:
        db_table = 'member_message'


class Message_Log(models.Model):
    TYPES_RELATION = (
        (0, 'Normal'),
        (1, 'Project'),
        (2, 'Demand'),
    )
    sender = models.ForeignKey(Member, related_name="member_message_log_sender")
    receiver = models.ForeignKey(Member, related_name="member_message_log_receiver")
    message = models.ForeignKey(Message, related_name="member_message_detail")
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    item_type= models.IntegerField(default=0, choices=TYPES_RELATION)
    item_id = models.IntegerField(default=0)

    def __unicode__(self):
        return self.content

    class Meta:
        db_table = 'member_message_log'


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
    file_type_name = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    new_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.file_name

    class Meta:
        db_table = 'demand_demandAttach'


class DemandViewLog(models.Model):
    member = models.ForeignKey(Member, related_name='demand_view_log_member')
    demand = models.ForeignKey(Demand, related_name='demand_view_log_demand')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demand_view_log'


class DemandVisitor(models.Model):
    member = models.ForeignKey(Member, related_name='demand_visitor_member')
    demand = models.ForeignKey(Demand, related_name='demand_visitor_demand')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demand_visitor'


class ProjectViewLog(models.Model):
    member = models.ForeignKey(Member, related_name='project_view_log_member')
    project = models.ForeignKey(Project, related_name='project_view_log_project')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_view_log'


class ProjectVisitor(models.Model):
    member = models.ForeignKey(Member, related_name='project_visitor_member')
    project = models.ForeignKey(Project, related_name='project_visitor_project')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_visitor'


class CVSourceContact(models.Model):
    company_name = models.CharField(max_length=255, null=True, default='')
    contact_name = models.CharField(max_length=100, null=True, default='')
    contact_title = models.CharField(max_length=255, null=True, default='')
    contact_tel = models.CharField(max_length=25, null=True, default='')
    contact_email = models.CharField(max_length=255, null=True, default='')
    contact_desc = models.TextField(null=True)
    member = models.ForeignKey(Member, related_name="contactor")
    add_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.IntegerField(default=0)

    class Meta:
        db_table = 'cvsource_contact'


class Keyword(models.Model):
    name = models.CharField(max_length=255, null=True, default='')
    count_project = models.IntegerField(default=0)
    count_preference = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(default=datetime.datetime.now(), auto_now=True)
    is_delete = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'repository_keyword'


class News(models.Model):
    title =  models.CharField(max_length=200, blank=True, null=True)
    content =  models.TextField(blank=True, null=True)
    tag =  models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField(null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'cvsource_news'

   
DEAL_TYPES = (
        (0, _('List')),
        (1, _('Trans')),
        (2, _('BuyTogether')),
       
    )


class Deal(models.Model):
    deal_type = models.IntegerField(choices=DEAL_TYPES, default=2)
    title =  models.CharField(max_length=400, blank=True, null=True)
    content =  models.TextField(blank=True, null=True)
    amount_usd =models.BigIntegerField(blank=True, null=True)
    amount=models.DecimalField(max_digits=19, decimal_places=6, null=True)
    currency = models.CharField(max_length=20, blank=True, null=True)
    equity =models.FloatField(blank=True, null=True)
    happen_date = models.DateTimeField(null=True)
    country_id=models.IntegerField(blank=True, null=True)
    province_id=models.IntegerField(blank=True, null=True)
    city_id=models.IntegerField(blank=True, null=True)
    target_company=models.CharField(max_length=200, blank=True, null=True)
    cv1=models.IntegerField(blank=True, null=True)
    cv2=models.IntegerField(blank=True, null=True)
    cv3=models.IntegerField(blank=True, null=True)
    market_value=models.BigIntegerField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'cvsource_deals'


class ListDeal(Deal):
    list_time=models.DateTimeField(blank=True, null=True)
    stock_code=models.CharField(max_length=50, blank=True, null=True)
    stock_exchange=models.CharField(max_length=50, blank=True, null=True)
    list_type=models.CharField(max_length=50, blank=True, null=True)
    list_status=models.CharField(max_length=50, blank=True, null=True)
    advisor_firm=models.CharField(max_length=400, blank=True, null=True)
    acc_firm=models.CharField(max_length=400, blank=True, null=True)
    law_firm=models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        db_table = 'cvsource_deals_list'


class TransDeal(Deal):
    invest_company=models.CharField(max_length=400, blank=True, null=True)
    invest_type=models.CharField(max_length=50, blank=True, null=True)
    invest_stage=models.CharField(max_length=50, blank=True, null=True)
    finance_advisor=models.CharField(max_length=400, blank=True, null=True)
    class Meta:
        db_table = 'cvsource_deals_trans'


class BuyTogetherDeal(Deal):
    buy_company=models.CharField(max_length=200, blank=True, null=True)
    buy_company_intro=models.CharField(max_length=800, blank=True, null=True)
    sale_company=models.CharField(max_length=200, blank=True, null=True)
    sale_company_intro=models.CharField(max_length=800, blank=True, null=True)
    buy_type=models.CharField(max_length=50, blank=True, null=True)
    buy_way=models.CharField(max_length=50, blank=True, null=True)
    attitude_name=models.CharField(max_length=50, blank=True, null=True)
    state=models.CharField(max_length=50, blank=True, null=True)
    
    dstrict=models.CharField(max_length=50, blank=True, null=True)
    
    whether_trade=models.CharField(max_length=50, blank=True, null=True)
    
    pay_style=models.CharField(max_length=50, blank=True, null=True)
    before_equity=models.FloatField(blank=True, null=True)
    after_equity=models.FloatField(blank=True, null=True)
    end_time=models.DateTimeField(blank=True, null=True)
    sales_income=models.BigIntegerField(blank=True, null=True)
    total_assets=models.BigIntegerField(blank=True, null=True)   
    net_assets=models.BigIntegerField(blank=True, null=True)
    net_margin=models.BigIntegerField(blank=True, null=True)
    pe=models.FloatField(blank=True, null=True)
    pb=models.FloatField(blank=True, null=True)
    ps=models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'cvsource_deals_buytogether'


class TempUsDeal(models.Model):
    deal_type = models.IntegerField(blank=True, null=True)
    industry_id=models.IntegerField(blank=True, null=True)
    chart_type=models.IntegerField(blank=True, null=True)
    amount_usd =models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return str(self.industry_id)

    class Meta:
        db_table = 'cvsource_deals_temp_us'


class Favorites(models.Model):
    TYPES_RELATION = (
        (1, 'Project'),
        (2, 'Demand'),
        (3, 'Company'),
        (4, 'Member'),
        (5, 'Data'),
        (6, 'News'),
    )
    member = models.ForeignKey(Member)
    add_time = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, null=True, blank=True)
    demand = models.ForeignKey(Demand, null=True, blank=True)
    receiver = models.ForeignKey(Member, related_name="member_receiver_favorite", null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    news = models.ForeignKey(News, null=True, blank=True)
    data = models.ForeignKey(Deal, null=True, blank=True)
    type_relation = models.IntegerField(default=0, choices=TYPES_RELATION)

    def __unicode__(self):
        if self.project is None:
            return self.demand
        return self.project

    def user_fav_member_name(self):
        if self.receiver:
            return self.receiver.fullname
        else:
            return self.receiver
    def user_fav_member_image(self):
        if self.receiver:
            return self.receiver.avatar
        else:
            return self.receiver

    def user_fav_member_company_name(self):
        if self.receiver:
            return self.receiver.companyNameCn()
        else:
            return self.receiver

    def user_fav_pro_name(self):
        if self.project:
            return self.project.name_cn
        else:
            return self.project

    def user_fav_pro_status(self):
        if self.project:
            return self.project.status
        else:
            return self.project

    def user_fav_pro_add_time(self):
        if self.project:
            return self.project.add_time
        else:
            return self.project

    def user_fav_pro_expire_date(self):
        if self.project:
            return self.project.expire_date
        else:
            return self.project

    def user_fav_pro_pv(self):
        if self.project:
            return self.project.pv
        else:
            return self.project

    def user_fav_pro_favorite_times(self):
        return Favorites.objects.filter(project=self).count()

    def user_fav_pro_message_times(self):
        return Message.objects.filter(project=self).count()

    class Meta:
        db_table = 'member_favorites'


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


class ConditionDemand(object):
    type = 0
    industry = None
    country_id = 0
    province_id = 0
    keyword = ""
    member_id = 0
    status = -1


class ConditionProject(object):
    type = 0
    industry = None
    country_id = 0
    province_id = 0
    keyword = ""
    member_id = 0
    status = -1
    keywords = []
    dealsize_min = -1
    dealsize_max = -1
    service_type = 0
    project_stage = 0
    currency_type = 0

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
    time = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'project_customer_target_company'


RECOMMEND_PROCESS = (
    (0, _('UnPublished')),
    (1, _('Published')),
    (2, _('Remove')),
    (3, _('NDA Signed')),
    (4, _('TS Signed')),
    (5, _('Settlement')),
)


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

    def companyName(self):
        return self.company.name_cn.encode('utf-8')

    def companyAddress(self):
        return self.company.address_cn.encode('utf-8')

    def companyWebsite(self):
        return self.company.website.encode('utf-8')

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
        elif self.target_reason=='investor within the same industry':#allen add
            return '投资者在相同行业'

    class Meta:
        db_table = 'recommond_score'




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
    is_sender = models.BooleanField(default=0)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_target_company_detail'

    def companyName(self):
        return self.company.name_cn.encode('utf-8')

    def companyAddress(self):
        if not self.company.address_cn and self.company.address_cn is not None:
            return self.company.address_cn.encode('utf-8')
        else:
            return ""

    def companyWebsite(self):
        return self.company.website.encode('utf-8')

    def target_reason_cn(self):
        return self.recommondItem.target_reason_cn()


class TargetCompanyDetailHistory(models.Model):
    target_company_detail = models.ForeignKey(ProjectTargetCompanyDetail, related_name='target_company_detail')
    operate_status = models.IntegerField(choices=RECOMMEND_PROCESS, default=0)
    add_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'project_target_company_detail_history'


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


class DemandRecommendLog(models.Model):
    TYPES = (
        (1, 'recommend'),
        (2, 'top'),
    )
    demand = models.ForeignKey(Demand, related_name='demand_recommend_log_demand')
    add_time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=TYPES, default=1)

    class Meta:
        db_table = 'demand_recommend_log'


class TypeDemandRecommend(object):
    recommend = 1
    top = 2


class EditorSay(models.Model):
    add_time = models.DateTimeField(auto_now_add=True)
    content_cn = models.TextField()
    content_en = models.TextField()

    def __unicode__(self):
        return self.content_cn

    class Meta:
        db_table = 'editorsay'


class DTOTimeline(object):
    member_id = 0
    member_realname = ""
    member_avatar = ""
    member_link = ""
    content_link = ""
    content_cn_start_pre = ""
    content_cn_start = ""
    content_cn = ""
    content_cn_end = ""
    content_en_start = ""
    content_en = ""
    content_en_end = ""
    addtime = ""
    member_company = ""
    member_title = ""
    project_id = 1
    content_type = 0


class DTOMessage(object):
    update_time = ""
    item_object = ""