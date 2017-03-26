# -*- coding:utf-8 -*-
from django.db import models
from industry.models import Industry
from repository.models import Keyword

DEAL_TYPES = (
    (1, '控股权收购'),
    (2, '小股权投资'),
    (3, '老股转让(非并购)'),
    (4, '融资或并购'),
    (5, '资产转让'),
    (6, '增发'),
    (7, '企业债券'),
    (8, '可换公司债'),
    (9, 'IPO'),
)

SCENES = (
    (0, '国内事件'),
    (1, '国外事件'),
)

CURRENCY_TYPES = (
    (1, '人民币'),
    (2, '美元'),
    (3, '欧元'),
    (4, '英镑'),
    (5, '日元'),
    (6, '港币'),
    (7, '新台币'),
    (8, '韩元'),
    (9, '其他'),
    (10, '未披露'),
)

INVESTMENT_STAGE = (
    (1, '种子天使'),
    (2, 'Pre-A轮'),
    (3, 'A轮'),
    (4, 'B轮'),
    (5, 'C轮'),
    (6, 'D轮'),
    (7, 'E轮'),
    (8, 'F轮-PreIPO'),
    (9, 'IPO上市及以后'),
    (10, '不明确'),
    (11, '战略投资'),
    (12, '收购'),
    (13, '未披露'),
)

SCALE = (
    (1, '数十万'),
    (2, '数百万'),
    (3, '数千万'),
    (4, '亿元及以上'),
    (5, '未披露'),
)


class StockMarket(models.Model):
    market_name = models.CharField(max_length=20, blank=True, null=True)
    symbol = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.market_name


class ShanghaiShenzhenNoticeType(models.Model):
    type_name = models.CharField(max_length=40, blank=True, null=True)
    symbol = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.type_name


class InvestEvent(models.Model):
    investee_abbreviation = models.CharField(max_length=40)
    website_url = models.URLField()
    cv1 = models.ManyToManyField(Industry, blank=True, null=True, related_name="cv1")
    cv2 = models.ManyToManyField(Industry, blank=True, null=True, related_name="cv2")
    cv3 = models.ManyToManyField(Industry, blank=True, null=True, related_name="cv3")
    tag = models.CharField(max_length=40, default='')
    event_scene = models.IntegerField(choices=SCENES, default=0)
    continent = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=10, blank=True, null=True)
    province = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=10, blank=True, null=True)
    investee_fullname = models.CharField(max_length=40, default='')
    introduction = models.TextField()
    invest_phase = models.IntegerField(choices=INVESTMENT_STAGE, default=5)
    scale = models.IntegerField(choices=SCALE, default=1)
    currency = models.IntegerField(choices=CURRENCY_TYPES, default=1)
    investors = models.CharField(max_length=128)
    time = models.DateTimeField(blank=True, null=True)
    data_source = models.CharField(max_length=40, null=True)
    source_url = models.URLField(null=True)
    amount = models.BigIntegerField(blank=True, null=True)
    financial_advisor = models.CharField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        return self.investee_abbreviation


class ShanghaiShenzhenNotice(models.Model):
    market_type = models.ForeignKey(StockMarket, null=True, blank=True)
    symbol = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    notice_type = models.ForeignKey(ShanghaiShenzhenNoticeType, null=True, blank=True)
    published_date = models.DateTimeField(blank=True, null =True)
    body = models.TextField()
    pdf_url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.title


class HkNoticeType(models.Model):
    notice_type_name = models.CharField(max_length=60, null=True)
    code = models.CharField(max_length=8, null=True)
    level = models.IntegerField(null=True)
    parent_id = models.IntegerField(null=True)
    
    def __unicode__(self):
        return self.notice_type_name


class HkNotice(models.Model):
    MARKET_TYPE = (
        (0, '主板'),
        (1, '创业板'),
    )
    market_type = models.IntegerField(choices=MARKET_TYPE, default=0)
    time = models.DateTimeField(blank=True, null=True)
    symbol = models.CharField(max_length=10, blank=True, null=True)
    stock_name = models.CharField(max_length=20, blank=True, null=True)
    types =  models.ManyToManyField(HkNoticeType)
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.title


class DailyDeal(models.Model):
    company_short_name = models.CharField(max_length=20, blank=True, null=True)
    stock_symbol = models.CharField(max_length=20, blank=True, null=True)
    cv1 = models.ForeignKey(Industry, blank=True, null=True, related_name="daily_deal_cv1")
    cv2 = models.ForeignKey(Industry, blank=True, null=True, related_name="daily_deal_cv2")
    company_full_name = models.CharField(max_length=40, blank=True, null=True)
    target_company = models.CharField(max_length=40, blank=True, null=True)
    deal_type = models.IntegerField(choices=DEAL_TYPES, default=1)
    deal_currency = models.IntegerField(choices=CURRENCY_TYPES, default=1)
    deal_amount = models.BigIntegerField(blank=True, null=True)
    deal_ratio = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    deal_content = models.TextField()
    date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    financial_advisor = models.CharField(max_length=40, blank=True, null=True)
    target_company_tags = models.CharField(max_length=20, blank=True, null=True)
    investor_tags = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.company_short_name
