#encoding:utf-8
from django.db import models


class AnalysisUserTotal(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    user_num = models.IntegerField(default=0,blank=True, null=True)
    project_num = models.IntegerField(default=0,blank=True, null=True)
    demand_num = models.IntegerField(default=0,blank=True, null=True)
    listed_user_num = models.IntegerField(default=0,blank=True, null=True)
    unlisted_user_num = models.IntegerField(default=0,blank=True, null=True)
    vc_user_num = models.IntegerField(default=0,blank=True, null=True)
    fa_user_num = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return self.time


class AnalysisUser(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    logined_user_num = models.IntegerField(default=0,blank=True, null=True)
    add_user_num = models.IntegerField(default=0,blank=True, null=True)
    created_project_user_num = models.IntegerField(default=0,blank=True, null=True)
    created_demand_user_num = models.IntegerField(default=0,blank=True, null=True)
    unpublish_user_num = models.IntegerField(default=0,blank=True, null=True)
    sendmail_user_num = models.IntegerField(default=0,blank=True, null=True)
    visited_index_user_num = models.IntegerField(default=0,blank=True, null=True)
    active_user_num = models.IntegerField(default=0,blank=True,null=True)
    target_user_num = models.IntegerField(default=0,blank=True,null=True)
    def __unicode__(self):
        return self.time


PROJECTTYPE = (
       (0, '项目'),
       (1, '需求'),
       
   )

class AnalysisProject(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(choices=PROJECTTYPE, default=0)
    all_num = models.IntegerField(default=0,blank=True, null=True)
    valid_num = models.IntegerField(default=0,blank=True, null=True)
    created_num = models.IntegerField(default=0,blank=True, null=True)
    audit_num = models.IntegerField(default=0,blank=True, null=True)
    offline_num = models.IntegerField(default=0,blank=True, null=True)
    pendding_num = models.IntegerField(default=0,blank=True, null=True)
    draft_num = models.IntegerField(default=0,blank=True, null=True)
    user_add_num = models.IntegerField(default=0,blank=True, null=True)
    bd_add_num = models.IntegerField(default=0,blank=True, null=True)
    target_num = models.IntegerField(default=0,blank=True, null=True)
    public_num = models.IntegerField(default=0,blank=True, null=True)

    def __unicode__(self):
        return self.time

class AnalysisProjectFinish(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(choices=PROJECTTYPE, default=0)
    all_num = models.IntegerField(default=0,blank=True, null=True)
    rang_num_1_cn = models.IntegerField(default=0,blank=True, null=True)
    rang_num_2_cn = models.IntegerField(default=0,blank=True, null=True)
    rang_num_3_cn = models.IntegerField(default=0,blank=True, null=True)
    rang_num_4_cn = models.IntegerField(default=0,blank=True, null=True)
    rang_num_1_en = models.IntegerField(default=0,blank=True, null=True)
    rang_num_2_en = models.IntegerField(default=0,blank=True, null=True)
    rang_num_3_en = models.IntegerField(default=0,blank=True, null=True)
    rang_num_4_en = models.IntegerField(default=0,blank=True, null=True)

    def __unicode__(self):
        return self.time
