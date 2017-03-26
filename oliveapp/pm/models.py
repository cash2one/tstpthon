#-*- coding:utf-8 -*-

          #################            #
       ######################         #
      #########################      #
    ############################
   ##############################
   ###############################
  ###############################
  ##############################
                  #    ########   #
     ##        ###        ####   ##
                          ###   ###
                        ####   ###
   ####          ##########   ####
   #######################   ####
     ####################   ####
      ##################  ####
        ############      ##
           ########        ###
          #########        #####
        ############      ######
       ########      #########
         #####       ########
           ###       #########
          ######    ############
         #######################
         #   #   ###  #   #   ##
         ########################
          ##     ##   ##     ##
          
#--------------------------------------#
#         copyright  olive.fm          #
#--------------------------------------#

from django.db import models
from django.conf import settings
import datetime
from django.utils.html import format_html

class Customer(models.Model):
    name=models.CharField("客户名称",max_length=50)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "客户"
        verbose_name_plural = "客户"

class Project(models.Model):
    name=models.CharField("项目名称",max_length=100)
    url=models.URLField("正式地址",max_length=400,blank=True, null=True)
    test_url=models.URLField("测试地址",max_length=400,blank=True, null=True)
    customer = models.ForeignKey(Customer,verbose_name="客户")
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目"

class Task(models.Model):
    TASK_TYPE = (
        (1, '内容制作'),
        (2, '程序开发'),
        (3, '数据处理'),
        (4, '设计'),
        (5, '服务器维护'),
        (6, '其它'),
    )

    TASK_STATUS = (
        (1, '未开始'),
        (2, '处理中'),
        (3, '测试中'),
        (4, '已完成'),
    )

    TASK_MONEY_STATUS = (
        (1, '未开票'),
        (2, '已开票'),
        (3, '已付款'),
    )

    name=models.CharField("任务单名称",max_length=100)
    desc=models.TextField("备注",max_length=800,blank=True, null=True)
    task_type = models.IntegerField("任务类型",choices=TASK_TYPE,default=1)
    task_status = models.IntegerField("执行状态",choices=TASK_STATUS,default=1)
    task_money_status = models.IntegerField("收款状态",choices=TASK_MONEY_STATUS,default=1)

    project = models.ForeignKey(Project,verbose_name="所属项目")
    money=models.IntegerField("金额",default=0)
    start_time = models.DateField("开始时间",default=datetime.datetime.now())
    end_time = models.DateField("结束时间",default=datetime.datetime.now() + datetime.timedelta(days=7))
    add_time = models.DateField("添加时间",default=datetime.datetime.now())
    operator = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="操作人员")

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "任务单"
        verbose_name_plural = "任务单"

    def colored_status(self):
        return '<span class="status_color_'+str(self.task_status)+'">'+self.get_task_status_display()+'</span>'

    colored_status.allow_tags = True
    colored_status.short_description ="执行状态"

    def colored_money_status(self):
        return '<span class="status_money_color_'+str(self.task_money_status)+'">'+self.get_task_money_status_display()+'</span>'

    colored_money_status.allow_tags = True
    colored_money_status.short_description ="收款状态"
   