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
import datetime

class Site(models.Model):
    name=models.CharField("网站名称",max_length=100)
    url=models.URLField("网站地址",max_length=400,blank=True, null=True)
    enable = models.BooleanField("可用",default=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "网站"
        verbose_name_plural = "网站" 

class SiteEditor(models.Model):
    name=models.CharField("编辑名称",max_length=100)
    password = models.CharField("密码",max_length=50)
    site=models.ForeignKey(Site,verbose_name="所属网站")
    enable = models.BooleanField("可用",default=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "编辑"
        verbose_name_plural = "编辑"

class SiteAdminUser(models.Model):
    name=models.CharField("管理员名称",max_length=100)
    password = models.CharField("密码",max_length=50)
    site=models.ForeignKey(Site,verbose_name="所属网站")
    enable = models.BooleanField("可用",default=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "网站管理员"
        verbose_name_plural = "网站管理员"


class Category(models.Model):
    name=models.CharField("分类名称",max_length=100)
    parentCategory=models.ForeignKey('self',verbose_name="父分类",null=True,blank=True)
    site=models.ForeignKey(Site,verbose_name="所属网站")
    enable = models.BooleanField("可用",default=True)
    is_show = models.BooleanField("上线显示",default=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"


class Article(models.Model):
    title=models.CharField("标题",max_length=200)
    content=models.TextField("内容",max_length=800,blank=True, null=True)
    url=models.URLField("外部地址",max_length=400,blank=True, null=True)
    add_time = models.DateField("添加时间",default=datetime.datetime.now())
    edit_time = models.DateField("修改时间",default=datetime.datetime.now())
    category = models.ForeignKey(Category,verbose_name="分类")
    auther = models.ForeignKey(SiteEditor,verbose_name="发布者")
    enable = models.BooleanField("可用",default=True)
    is_show = models.BooleanField("上线显示",default=True)

    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
