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

class IpRecord(models.Model):
	ip=models.CharField(max_length=50)
	country=models.CharField(max_length=50,blank=True, null=True)
	area=models.CharField(max_length=50,blank=True, null=True)
	region=models.CharField(max_length=50,blank=True, null=True)
	city=models.CharField(max_length=50,blank=True, null=True)
	county=models.CharField(max_length=50,blank=True, null=True)
	address=models.CharField(max_length=100,blank=True, null=True)
	isp=models.CharField(max_length=100,blank=True, null=True)
	add_time = models.DateField("添加时间",default=datetime.datetime.now())
	def __unicode__(self):
		return self.ip+":"+self.city
	class Meta:
		verbose_name = "IP查询记录"
		verbose_name_plural = "IP查询记录"