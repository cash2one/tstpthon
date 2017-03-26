#encoding:utf-8
from django.db import models
from area.models import Continent, Country, Province, City, RegionLevelOne, RegionLevelTwo, RegionLevelThree
from industry.models import Industry
from adminuser.models import AdminUser
from repository.models import StockExchange, Tag
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.utils.translation import ugettext as _
# Create your models here.

class BuyerDealCategory(models.Model):
    DEAL_CATEGORIES = (
        (0, _('Unlimited')),
        (1, _('Venture Capital')),
        (2, _('Merger')),
        (3, _('PE Investment & Pre IPO')),
        (4, _('Three Board Pre IPO')),
        (5, _('Project Financing')),
        (6, _('Others')),
    )
    category = models.IntegerField(choices=DEAL_CATEGORIES, default=0)
    name_cn = models.CharField(max_length=40, null=True, blank=True)
    name_en = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        db_table = 'member_buyerdealcategory'

class Company(models.Model):
    TYPES = (
        (1, _('Listed')),
        (2, _('UnListed')),
        (3, _('Investment')),
        (4, _('Service')),
        (5, _('Other')),
    )


    NEWTYPES = (
        (1, _('Brokerage')),
        (2, _('Investment Bank')),
        (3, _('Financial Advisory')),
        (4, _('Accounting Firm')),
        (5, _('Family Office')),
        (6, _('Listed Companies')),
        (7, _('VC')),
        (8, _('PE')),
        (9, _('VC/PE')),
        (10, _('Law Firm')),
        (12, _('Company')),
        (13, _('Commercial Bank')),
        (14, _('Trust')),
        (11, _('Other')),
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
    INVESTMENT_TYPES = (
        (0, _('N/A')),
        (1, _('VC')),
        (2, _('PE')),
        (3, _('VC/PE')),
        (4, _('Strategic investor')),

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
    regionlevelone = models.ForeignKey(RegionLevelOne, null=True, blank=True)
    regionleveltwo = models.ForeignKey(RegionLevelTwo, null=True, blank=True)
    regionlevelthree = models.ForeignKey(RegionLevelThree, null=True, blank=True)
    industry = models.ForeignKey(Industry, null=True, blank=True)
    address_cn = models.CharField(max_length=255, null=True, blank=True)
    address_en = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)

    postcode = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='companylogo/', blank=True, default='')
    type = models.IntegerField(choices=TYPES, default=0)#逐步废除
    new_type = models.IntegerField(choices=NEWTYPES, default=0)
    is_list=models.BooleanField(default=False)
    investment_type = models.IntegerField(choices=INVESTMENT_TYPES, default=0)

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
        return self.name_cn

    @staticmethod
    def active_list():
        return Company.objects.filter(status=1).values("id",  "name_cn", "name_en", "short_name_cn", "short_name_en")

    class Meta:
        db_table = 'member_company'

class CompanyStockSymbol(models.Model):
    company = models.ForeignKey(Company,related_name="stock_symbols")
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
        (4, _('Buyour or Financing')),
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

    add_time=models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey('member.Member',  blank=True, null=True, related_name='member_companyinvestfield')

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
        (0, _('AuthenticationFailure')),
        (1, _('AuthenticationOk')),
        (2, _('Blacklist')),
        (3, _('MustChangePassword')),
        (4, _('Activating')),
        (5, _('AuthenticationPending')),
        (6, _('Unauthorized')),
    )
    ROLE_TYPE = (
        (0, _('Unknown Role Identity')),
        (1, _('Advisory')),
        (2, _('Investor')),
    )
    CURRENCY_TYPES = (
        (1, _('CNY')),
        (2, _('USD')),
        (3, _('EUR')),
        (4, _('OTHER')),
    )
    TARGET_PLATFORM = (
        (0, _('Display in Web')),
        (1, _('Display in App')),
        (2, _('Display in Both')),
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
    creator = models.ForeignKey(AdminUser, blank=True, null=True,related_name="creator")
    owner = models.ForeignKey(AdminUser, blank=True, null=True,related_name="owner")
    weixin = models.ForeignKey(OtherLogin, blank=True, null=True,related_name="weixin")
    weibo = models.ForeignKey(OtherLogin, blank=True, null=True,related_name="weibo")
    linkedin = models.ForeignKey(OtherLogin, blank=True, null=True,related_name="linkedin")
    weibo_url = models.CharField(max_length=200, blank=True)
    is_subscribe_push = models.BooleanField(default=True)
    not_push_reason = models.CharField(max_length=255, null=True, default='')
    role = models.IntegerField(default=0, choices=ROLE_TYPE)
    deal_currency = models.IntegerField(choices=CURRENCY_TYPES, default=0)
    deal_size_min = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    deal_size_max = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    summary = models.CharField(max_length=200, blank=True)
    investment = models.CharField(max_length=1000, blank=True)
    focus_investor_type = models.ForeignKey(BuyerDealCategory, blank=True, null=True)
    source_create = models.CharField(max_length=255, blank=True, null=True)
    source_channel = models.CharField(max_length=255, blank=True, null=True)
    target_platform = models.IntegerField(choices=TARGET_PLATFORM,  default=0)


    def __unicode__(self):
        return self.first_name + self.last_name

    def make_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @staticmethod
    def active_list():
        return Member.objects.order_by("first_name").all() #.values("id", "email", "first_name", "last_name")

    class Meta:
        db_table = 'member_member'


class MemberFocusKeyword(models.Model):
    member = models.ForeignKey(Member,  blank=True, null=True,related_name='member_focus_keyword')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'member_focus_keyword'


class AccessToken(models.Model):
    member = models.ForeignKey(Member, blank=True, null=True)
    access_token = models.CharField(max_length=50, blank=True)
    login_date = models.DateTimeField(default=datetime.datetime.now())
    device_token = models.CharField(max_length=255, blank=True, null=True)

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
        (3, _('Not applicable')),
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
    used_time = models.DateTimeField(null=True, blank=True, default=None)

    def __unicode__(self):
        return self.email

    class Meta:
        db_table = 'member_findpasswordhistory'


class InviteCode(models.Model):
    invite_user = models.ForeignKey(Member)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    add_time = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    used_time = models.DateTimeField(null=True, blank=True, default=None)

    def __unicode__(self):
        return self.code

    class Meta:
        db_table = 'member_invitecode'


class Preference(models.Model):
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


class StatusEntryForm:
    pending = 0
    not_approved = 1
    approved = 2


class StatusMember:
    normal = 1
    abnormal = 2
    activing = 4


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


class SellerDealCategory(models.Model):
    DEAL_CATEGORIES = (
        (0, _('Unlimited')),
        (1, _('Minority Interest')),
        (2, _('Majority Interest')),
        (3, _('Others')),
    )
    category = models.IntegerField(choices=DEAL_CATEGORIES, default=0)
    name_cn = models.CharField(max_length=40, null=True, blank=True)
    name_en = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        db_table = 'member_sellerdealcategory'


class DetailDealType(models.Model):
    DEAL_TYPES = (
        (0, _('Unlimited')),
        (1, _('Minority Recapitalization')),
        (2, _('Growth Capital')),
        (3, _('Venture Capital (Angel/Series A)')),
        (4, _('Pre IPO')),
        (5, _('Three Board Pre IPO')),
        (6, _('Convertible Debt')),
        (7, _('Senior Debt')),
        (8, _('Junior/Mezzanine Debt')),
        (9, _('Buyout / Company Sale')),
        (10, _('Management Buyout')),
        (11, _('Majority Recapitalization')),
        (12, _('Project Financing')),
        (13, _('Joint Venture / Partner')),
        (14, _('Asset Disposition')),
        (15, _('Distressed Situations')),
        (16, _('Real Estate')),
        (17, _('PIPE')),
        (18, _('Public Offering')),
        (19, _('IPO')),
    )
    deal_type = models.IntegerField(choices=DEAL_TYPES, default=0)
    category = models.ForeignKey(BuyerDealCategory, related_name='deal_types')
    seller_category = models.ForeignKey(SellerDealCategory, null=True, blank=True, related_name='seller_deal_types')
    name_cn = models.CharField(max_length=40, null=True, blank=True)
    name_en = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        db_table = 'member_detaildealtype'


class SubDetailDealType(models.Model):
    deal_type = models.ForeignKey(DetailDealType, related_name='detail_deal_type')
    name_cn = models.CharField(max_length=40, null=True, blank=True)
    name_en = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        db_table = 'member_subdetaildealtype'


class MemberInvestmentField(models.Model):

    CURRENCY_TYPES = (
        (0, _('Unknown')),
        (99, _('Unlimited')),
        (1, _('CNY')),
        (2, _('USD')),
        (3, _('EUR')),
        (4, _('OTHER')),
    )
    FINANCE_TYPES = (
        (0, _('Unknown')),
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
        (0, _('Unknown')),
        (99, _('Unlimited')),
        (1, _('Less than 10%')),
        (2, '10-30%'),
        (3, '30-50%'),
        (4, '50-70%'),
        (5, '70-100%'),
        (6, '100-150%'),
        (7, _('More than 150%')),

    )

    member = models.ForeignKey(Member, related_name='member_match_table')
    tags = models.CharField(max_length=400, blank=True, null=True)

    revenue = models.IntegerField(choices=FINANCE_TYPES, default=0)
    growth = models.IntegerField(choices=GROWTH_TYPES, default=0)
    net_income = models.IntegerField(choices=FINANCE_TYPES, default=0)
    ebita = models.IntegerField(choices=FINANCE_TYPES, default=0)

    deal_category = models.ManyToManyField(BuyerDealCategory)
    deal_type = models.ManyToManyField(DetailDealType)
    deal_currency = models.IntegerField(choices=CURRENCY_TYPES, default=0)
    deal_size_min = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    deal_size_max = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    country = models.ForeignKey(Country, null=True, blank=True)
    regionlevelone = models.ForeignKey(RegionLevelOne, null=True, blank=True)
    regionleveltwo = models.ForeignKey(RegionLevelTwo, null=True, blank=True)
    regionlevelthree = models.ForeignKey(RegionLevelThree, null=True, blank=True)
    hot = models.IntegerField(default=5)
    add_time = models.DateTimeField(auto_now_add=True)
    is_user = models.BooleanField(default=0)
    is_delete = models.BooleanField(default=0)
    multi_currency = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.tags

    class Meta:
        db_table = 'member_memberinvestmentfield'


class MemberDynamic(models.Model):
    TYPES = (
        (1, _('Message')),
        (2, _('Project')),
        (3, _('Demand')),
    )
    member = models.ForeignKey(Member)
    type = models.IntegerField(choices=TYPES, default=0)
    item_id = models.IntegerField(default=0)
    memo = models.CharField(max_length=255, blank=True, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.pk

    class Meta:
        db_table = 'member_dynamic'


class GlobalRecommendProjectLog(models.Model):
    member = models.ForeignKey(Member, related_name='member_global_recommend_project')
    project = models.ForeignKey('project.Project', related_name='project_global_recommend')
    email = models.EmailField()
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'global_recommend_project_log'


class CardMember(models.Model):
    GENDER_TYPE = (
        (1, _('Male')),
        (2, _('Female')),
    )

    company = models.ForeignKey(Company)
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
    intro_cn = models.TextField(blank=True)
    intro_en = models.TextField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    weibo_url = models.CharField(max_length=200, blank=True)
    qq = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=200, blank=True)
    source_url =models.CharField(max_length=200, blank=True)
    focus=models.CharField(max_length=800, blank=True)

    def __unicode__(self):
        return self.first_name + self.last_name

    class Meta:
        db_table = 'member_cardmember'



class CardMemberInvestmentField(models.Model):
    DEAL_TYPES = (
        (0, _('Unknow')),
        (99, _('Unlimited')),
        (1, _('Buyout')),
        (2, _('Growth Capital/Financing')),
        (3, _('Old stock transfer(not buyout)')),
        (4, _('Buyour or Financing')),
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

    member = models.ForeignKey(CardMember)
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

    add_time=models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tags
    class Meta:
        db_table = 'member_cardmemberinvestmentfield'


class Hobby(models.Model):
    CURRENCY_TYPES = (
        (1, _('CNY')),
        (2, _('USD')),
        (3, _('EUR')),
        (99, _('Unlimited')),
    )
    member = models.ForeignKey(Member, related_name='member_hobby')
    deal_currency = models.IntegerField(choices=CURRENCY_TYPES, default=0)
    deal_size_min = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    deal_size_max = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=2)
    add_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(default=datetime.datetime.now(), auto_now=True)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'member_hobby'


class HobbyTag(models.Model):
    hobby = models.ForeignKey(Hobby, related_name='hobby_tag')
    tag = models.ForeignKey(Tag)

    class Meta:
        db_table = 'member_hobby_tag'


class HobbyTagCustom(models.Model):
    hobby = models.ForeignKey(Hobby, related_name='hobby_tag_custom')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'member_hobby_tag_custom'


class HobbyCategory(models.Model):
    hobby = models.ForeignKey(Hobby, related_name='hobby_category')
    deal_category = models.ForeignKey(BuyerDealCategory)
    deal_type = models.ForeignKey(DetailDealType)

    class Meta:
        db_table = 'member_hobby_category'


class MemberCard(models.Model):
    member = models.ForeignKey(Member, related_name='member_card')
    file_type = models.CharField(max_length=50)
    file_type_name = models.CharField(null=True, max_length=100)
    file_name = models.CharField(max_length=100)
    new_name = models.CharField(max_length=100)
    add_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=0)

    def __unicode__(self):
        return self.file_name

    class Meta:
        db_table = 'member_card'

class Uninteresting(models.Model):
    member = models.ForeignKey(Member, blank = True, null = True)
    project = models.ForeignKey('project.Project')
    email_tracking = models.ForeignKey('log.EmailTracking', null = True)
    email = models.CharField(max_length=100, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())

    class Meta:
       db_table = 'member_uninteresting'

class UninterestingReason(models.Model):
    uninteresting = models.ForeignKey(Uninteresting)
    reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'member_uninteresting_reason'

