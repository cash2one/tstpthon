from django.db import models
from area.models import Country, Province, City
from industry.models import Industry
import datetime
from django.utils.translation import ugettext as _
# Create your models here.


class StockExchange(models.Model):
    name_cn = models.CharField(max_length=50, blank=True)
    name_en = models.CharField(max_length=50, blank=True)
    short_name_en = models.CharField(max_length=50, blank=True)
    short_name_cn = models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=20)

    def __unicode__(self):
        return self.short_name_en

    class Meta:
        db_table = 'repository_stockexchange'


class ListedCompany(models.Model):
    name_cn = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    short_name_cn = models.CharField(max_length=50, blank=True)
    short_name_en = models.CharField(max_length=50, blank=True)
    intro_cn = models.TextField(blank=True, null=True)
    intro_en = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    province = models.ForeignKey(Province, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    industry = models.ForeignKey(Industry, blank=True, null=True)
    address_cn = models.CharField(max_length=255, blank=True)
    address_en = models.CharField(max_length=255, blank=True)
    website = models.URLField(default='',blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    stock_exchange = models.ForeignKey(StockExchange)
    stock_symbol = models.CharField(max_length=50)
    stock_symbol_no_pre = models.CharField(max_length=20)
    stock_name = models.CharField(max_length=20)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    found_time = models.DateTimeField(null=True, blank=True)
    invest_field = models.TextField(blank=True, null=True)
    invest_type = models.TextField( blank=True, null=True)
    invest_size = models.TextField( blank=True, null=True)
    memo = models.TextField( blank=True, null=True)

    def __unicode__(self):
        return self.short_name_en

    class Meta:
        db_table = 'repository_listedcompany'


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
    website = models.URLField(default='',blank=True, null=True)
    stock_exchange = models.ForeignKey(StockExchange, null=True, blank=True)
    stock_symbol = models.CharField(max_length=20, blank=True, null=True)
    stock_symbol_no_pre = models.CharField(max_length=20, blank=True, null=True)
    capital_type = models.IntegerField(choices=Capital_TYPES, default=1)
    found_time = models.DateTimeField(null=True, blank=True)
    invest_field = models.TextField( blank=True, null=True)
    invest_type = models.TextField( blank=True, null=True)
    invest_size = models.TextField( blank=True, null=True)
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
        return self.targetcompany

    class Meta:
        db_table = 'repository_investmenthistory'


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


class Tag(models.Model):
    name = models.CharField(max_length=255, null=True, default='')
    sub_name = models.CharField(max_length=2000, null=True, default='')
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(default=datetime.datetime.now(), auto_now=True)
    is_hot = models.IntegerField(default=99)
    is_delete = models.BooleanField(default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'tag'