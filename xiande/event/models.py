#-*-encoding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User
import datetime

STATUS_TYPE = (
    (0, '待处理'),
    (1, '已审核'),
    (2, '审核不通过'),
    (3, '已删除'),
)       

SPENDING_TYPES = (
    (0, '未选择'),
    (1, '教育费'),
    (2, '医疗'),
    (3, '旅游'),
    (4, '保险'),
    (5, '还贷款'),
    (6, '理财'),
    (7, '未知'),
    (8, '其他'),
)

APPLY_TYPES = (
    (0, '未选择'),
    (1, '创业'),
    (2, '投资房产'),
    (3, '孩子海外留学'),
    (4, '移民'),
    (5, '其他'),
)
          
FOCUS_TYPES = (
    (0, '未选择'),
    (1, '产品的投资风险和收益'),
    (2, '工作人员是否专业'),
    (3, '该机构的品牌和收益'),
    (4, '媒体的投资建议'),

)
class CashEventInfo(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name='用户')

    event_amount = models.DecimalField('小金库本金', null=True, blank=True, max_digits=16, decimal_places=2)
    event_income = models.DecimalField('小金库收益', null=True, blank=True, max_digits=16, decimal_places=2)
    event_add_time = models.DateTimeField('参加小金库活动时间', null=True, blank=True)
    household_spending = models.IntegerField('家庭最大支出', choices=SPENDING_TYPES, default=0)
    investment_apply = models.IntegerField('资金配资安排', choices=APPLY_TYPES, default=0)
    investement_focus = models.IntegerField('选择理财产品关注点', choices=FOCUS_TYPES, default=0)
    apply_time = models.DateTimeField('创建时间', auto_now=True, null=True, blank=True)
    status = models.IntegerField('状态', choices=STATUS_TYPE, default=0)
    
    introducer = models.CharField('介绍人', max_length=255, null=True, blank=True)


    def __unicode__(self):
        return unicode(self.user.first_name)
    class Meta:
        verbose_name='小金库活动客户资料'
        verbose_name_plural = "小金库活动客户资料"
     
class CashEventRecommondInfo(models.Model):
    user = models.ForeignKey(User, verbose_name='用户',related_name='cash_event_user')
    introducer = models.ForeignKey(User, verbose_name='介绍人',related_name='cash_event_introducer') 
    amount = models.IntegerField('奖励金额', default=0)
    add_time = models.DateTimeField('参加小金库活动时间', default=datetime.datetime.now())
    
    def __unicode__(self):
        return unicode(self.user.first_name)
    class Meta:
        verbose_name='小金库活动客户推荐记录'
        verbose_name_plural = "小金库活动客户推荐记录"


EVENT_LIST = (
    (0, '未选择'),
    (1, '2月14情人节活动'),
    (2, '新年全家总动员'),
    (3, '私人游艇黄浦江年会'),
)                        
class EventApply(models.Model):
    username = models.CharField('姓名', max_length=255, null=True, blank=True)
    mobile = models.CharField('手机', max_length=255, null=True, blank=True)
    address = models.CharField('联系方式', max_length=255, null=True, blank=True)
    birthday = models.DateTimeField('生日', null=True, blank=True)
    event = models.IntegerField('活动名称', choices=EVENT_LIST, default=0)
    apply_time = models.DateTimeField('报名时间', auto_now=True, null=True, blank=True)
    status = models.IntegerField('状态', choices=STATUS_TYPE, default=0)

    def __unicode__(self):
        return unicode(self.username)
    class Meta:
        verbose_name='活动报名表'
        verbose_name_plural = "活动报名表"

BBB_STATUS_TYPE = (
    (0, '未支付'),
    (1, '已支付'),
    (2, '已过期'),
    (3, '删除'),
)   

class BBBEventInfo(models.Model):
    openid = models.CharField('微信OpenID', max_length=255)
    username = models.CharField('姓名', max_length=255, null=True, blank=True)
    mobile = models.CharField('手机', max_length=255, null=True, blank=True)
    amount = models.IntegerField('金额', default=0, null=True, blank=True)
    apply_time = models.DateTimeField('创建时间', auto_now=True, null=True, blank=True)
    apply_status = models.IntegerField('状态', choices=BBB_STATUS_TYPE, default=0)
    introducer = models.CharField('介绍人', max_length=255, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.username)
    class Meta:
        verbose_name='牛熊宝活动客户资料'
        verbose_name_plural = "牛熊宝活动客户资料"

EVENT_STATUS_TYPE = (
    (0, '正常'),
    (1, '停止'),
    (2, '已删除'),
)  

class Event(models.Model):
    name = models.CharField('活动名称', max_length=255)
    code = models.CharField('活动代码', max_length=255, null=True, blank=True)
    start_time = models.DateTimeField('创建时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    status = models.IntegerField('状态', choices=EVENT_STATUS_TYPE, default=0)


