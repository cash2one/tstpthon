from django.db import models
import datetime
from django.utils.translation import ugettext as _

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
    add_time = models.DateTimeField(default=datetime.datetime.now(), auto_now=True)

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


