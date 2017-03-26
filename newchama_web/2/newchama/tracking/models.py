#encoding:utf-8
from django.db import models
import datetime
from adminuser.models import AdminUser

TRACK_TYPE = (
        (1,'用户'),
        (2,'公司'),
        (3,'申请表'),
        (4,'项目'),
        (5,'需求'),
    )

class TrackingItem(models.Model):
    user = models.ForeignKey(AdminUser)
    tracking_type = models.IntegerField(choices=TRACK_TYPE, default=0,null=True)
    tracking_id = models.IntegerField(default=0,null=True)
    tracking_name = models.CharField(max_length=255,null=True)
    content = models.TextField(null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tracking_tracking'
