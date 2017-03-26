#encoding:utf-8
from django.db import models
from services.models import Member
import datetime
from django.utils.translation import ugettext as _

class Log(models.Model):
    OPERTATION_TYPES = (
        (0, _('Unknow')),
        (1, _('Login')),
        (2, _('Views')),
        (3, _('Edit')),
        (4, _('Offline')),
        (5, _('Favorite')),
        (6, _('Unfavorite')),
        (7, _('Delete')),
        (8, _('Click')),
        (9, _('Search')),
        (10, _('Pending')),
    )
    TARGET_TYPES = (
        (0, _('Unknow')),
        (1, _('Member')),
        (2, _('Project')),
        (3, _('Demand')),
        (4, _('Company')),
        (5, _('Recommond Company')),
        (6, _('News')),
        (7, _('ExtenalMail')),
        (8, _('Index')),
        (9, _('Email')),
    )
    DETAIL_TYPES = (
        (0, _('Unknow')),
        (1, _('Page')),#普通页面
        (2, _('Teaser')),#Teaser页面
        (3, _('Left')),#向左
        (4, _('Right')),#向右
        (5, _('Man')),#人工
        (6, _('Machine')),#机器或系统
        (21, _('user_recommond')),#用户推荐
        (22, _('admin_recommond')),#管理员推荐
        (23, _('other')),#管理员推荐
    )
    user = models.ForeignKey(Member)
    time = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    operation_type = models.IntegerField(choices=OPERTATION_TYPES,default=0)
    target_type = models.IntegerField(choices=TARGET_TYPES,default=0)
    detail_type = models.IntegerField(choices=DETAIL_TYPES,default=0)
    
    item_id = models.IntegerField(default=0)
    item_name = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    request_url = models.CharField(max_length=400, blank=True, null=True)
    memo = models.CharField(max_length=200, blank=True, null=True)

    def user_name(self):
        return self.user.fullname

    def user_image(self):
        return self.user.avatar


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
    add_time = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    update_time = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.pk

    class Meta:
        db_table = 'member_dynamic'
