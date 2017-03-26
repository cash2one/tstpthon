#-*-encoding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User
import datetime

GENDER_TYPES = (
    (0, '未选择'),
    (1, '男'),
    (2, '女'),
)
CUSTOMER_TYPES = (
    (0, '非基金客户'),
    (1, '基金客户'),
)

SOURCE_TYPES = (
    (0, '未选择'),
    (1, '原有'),
    (2, '线下'),
    (3, '微信公众号直接报名'),
    (4, '小金库活动'),
)

CURRENCY_TYPES = (
    (0, '未选择'),
    (1, '人民币'),
    (2, '美元'),
    (3, '港币'),
    (4, '日元'),
    (5, '欧元'),
    (6, '英镑'),
    (7, '新加坡元'),
    (8, '澳元'),
    (9, '新西兰元'),
    (10, '加元'),
    (11, '其他'),
)

ASSING_TYPES = (
    (0, '未选择'),
    (1, '16%+超额红利'),
)

ID_TYPES = (
    (0, '未选择'),
    (1, '居民身份证'),
    (2, '护照'),
    (3, '外国人居留证'),
    (4, '港澳同胞回乡证'),
    (5, '港澳居民来往内地通行证'),
    (6, '台湾居民来往大陆通行证'),
    (7, '大陆居民往来台湾通行证'),
    (8, '外国人出入境证'),
    (9, '外交官证'),
    (10, '领事馆证'),
    (11, '临时身份证'),
    (12, '外国人居留证'),
    (13, '军官证'),
    (14, '武警警官证'),
    (15, '士兵证'),
    (16, '军队学员证'),
    (17, '军队文职干部证'),
    (18, '军队离退休干部证和军队职工证'),
    (19, '海员证'),
    (19, '其他'),

)

BORROWED_TYPES = (
    (0, '未选择'),
    (1, '银行转账'),
    (2, '电汇'),
    (3, '现金'),
    (4, '其他'),
)
 
             
class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True, verbose_name='用户')
    is_investment = models.BooleanField('客户类型',  choices=CUSTOMER_TYPES, default=0)
    gender = models.IntegerField('性别', choices=GENDER_TYPES, default=0)
    contract_no = models.CharField('合同编号', max_length=255, null=True, blank=True)
    fund_customer_number = models.CharField('基金客户编号', max_length=255, null=True, blank=True)
    fund_item_number = models.CharField('基金项目编号', max_length=255, null=True, blank=True)
    amount = models.DecimalField('本金', null=True, blank=True, max_digits=16, decimal_places=2)
    income = models.DecimalField('收益', null=True, blank=True, max_digits=16, decimal_places=2)
    currency = models.IntegerField('币种', choices=CURRENCY_TYPES, default=0)
    assign_type = models.IntegerField('收益/分配类型', choices=ASSING_TYPES, default=0)
    id_type = models.IntegerField('证件类型', choices=ID_TYPES, default=0)
    id_no = models.CharField('证件号码', max_length=50, null=True, blank=True)
    address = models.CharField('地址', max_length=255, null=True, blank=True)
    postcode = models.CharField('邮编', max_length=50, null=True, blank=True)
    birthday = models.DateTimeField('生日', null=True, blank=True)
    contact = models.CharField('联系人', max_length=255, null=True, blank=True)
    mobile = models.CharField('手机', max_length=255, null=True, blank=True)
    tel = models.CharField('电话', max_length=255, null=True, blank=True)
    bank_name = models.CharField('开户银行', max_length=255, null=True, blank=True)
    bank_account = models.CharField('银行账号', max_length=255, null=True, blank=True)
    borrowed_time = models.DateTimeField('入款时间', null=True, blank=True)
    borrowed_type = models.IntegerField('入款类型', choices=BORROWED_TYPES, default=0)
    family = models.TextField('家庭及子女情况', null=True, blank=True)
    hobby = models.TextField('爱好', null=True, blank=True)
    company = models.CharField('公司', max_length=255, null=True, blank=True)
    job_title = models.CharField('职位', max_length=255, null=True, blank=True)
    signed_time = models.DateTimeField('签约时间', null=True, blank=True)
    contract_start_time = models.DateTimeField('合约开始时间', null=True, blank=True)
    contract_end_time = models.DateTimeField('合约结束时间', null=True, blank=True)
    
    wx_username = models.CharField('微信用户名', max_length=255, null=True, blank=True)
    wx_openid = models.CharField('微信OPENID', max_length=255, null=True, blank=True)
    introducer = models.ForeignKey('self', null=True, blank=True)

    source = models.IntegerField('客户来源', choices=SOURCE_TYPES, default=0)
    memo = models.TextField('备注', null=True, blank=True)
    

    def __unicode__(self):
        return self.user.first_name
    class Meta:
        verbose_name='用户资料'
        verbose_name_plural = "用户资料"

class Income(models.Model):
    amount = models.DecimalField('总本金', max_digits=16, decimal_places=2)
    income = models.DecimalField('总收益', max_digits=16, decimal_places=2)
    assign_time = models.DateTimeField('结算月份')
    add_time = models.DateTimeField('添加时间', auto_now=True, default=datetime.datetime.now())
    is_active = models.BooleanField('是否有效', default=True)

    def __unicode__(self):
        return str(self.add_time)
    class Meta:
        verbose_name='用户收益'
        verbose_name_plural = "用户收益"

PROJECT_LIST = (
    (0, '未选择'),
    (1, '显德量化对冲基金1期'),
    (2, '显德量化对冲基金2期'),
    (3, '显德量化对冲基金3期'),
)  
STATUS_TYPE = (
    (0, '待处理'),
    (1, '已审核'),
    (2, '审核不通过'),
    (3, '已删除'),
)   
class Apply(models.Model):
    user = models.ForeignKey(User, verbose_name='用户')
    amount = models.DecimalField('理财金额', max_digits=16, decimal_places=2)
    project = models.IntegerField('项目', choices=PROJECT_LIST, default=0)
    apply_time = models.DateTimeField('报名时间', auto_now=True, null=True, blank=True)
    status = models.IntegerField('状态', choices=STATUS_TYPE, default=0)

    def __unicode__(self):
        return str(self.username)
    class Meta:
        verbose_name='理财报名表'
        verbose_name_plural = "理财报名表"

