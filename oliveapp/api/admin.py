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
from django.contrib import admin
from api.models import IpRecord

class IpRecordAdmin(admin.ModelAdmin):
    list_filter = ('country',)
    search_fields = ['ip']
    list_display = ('ip', 'country', 'area', 'region', 'city', 'county','isp')

admin.site.register(IpRecord, IpRecordAdmin)