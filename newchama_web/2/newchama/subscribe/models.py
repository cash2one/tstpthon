#encoding:utf-8
from django.db import models
from member.models import Member, Company
from area.models import Country, Province, City
from project.models import Project
from industry.models import Industry
from adminuser.models import AdminUser
from django.utils.translation import ugettext as _
import datetime

# Create your models here.
class Subscribe(models.Model):
    name_cn = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    member = models.ForeignKey(Member, related_name='member_subscribe_publisher')
    service_type = models.IntegerField(choices=Project.SERVICE_TYPES, null=True, blank=True)
    project_stage = models.IntegerField(choices=Project.INVESTMENT_STAGE, null=True, blank=True)
    currency_type = models.IntegerField(choices=Project.CURRENCY_TYPES, null=True, blank=True)
    company_countries = models.ForeignKey(Country, null=True, blank=True)
    company_provinces = models.ForeignKey(Province, null=True, blank=True)
    company_cities = models.ForeignKey(City, null=True, blank=True)
    company_industries = models.ForeignKey(Industry, null=True, blank=True)
    cv1 = models.IntegerField(blank=True, null=True)
    cv2 = models.IntegerField(blank=True, null=True)
    cv3 = models.IntegerField(blank=True, null=True)
    deal_size_min = models.BigIntegerField(null=True, blank=True)
    deal_size_max = models.BigIntegerField(null=True, blank=True)
    total_match = models.IntegerField(null=True, blank=True)
    tip_interval = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(default=datetime.datetime.now(), auto_now=True)
    last_send_time = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    is_push = models.BooleanField(default=1)
    not_push_reason = models.CharField(max_length=255, null=True, default='')

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'project_subscribe'


class SubscribeKeyword(models.Model):
    subscribe = models.ForeignKey(Subscribe, related_name='subscribe_keyword')
    keyword = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'project_subscribe_keyword'


class SubscribeSendRecord(models.Model):
    project = models.ForeignKey(Project, related_name='subscribe_project')
    subscribe = models.ForeignKey(Subscribe, related_name='subscribe_send')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_subscribe_send_record'
