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
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import urllib2
import json
from api.models import IpRecord

def GetRemoteIpAddress(request):
    ip=""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def RemoveCityAndCounty(txt):
    if(len(txt.strip())>0):
        if (txt[-1]==u"市" or txt[-1]==u"县"):
            txt = txt[0:-1]
    return txt

def GetIpInfoJson(ip):
    url="http://ip.taobao.com/service/getIpInfo.php?ip="+ip
    return json.loads(urllib2.urlopen(url).read())  

def ip2city(request):
    html=""
    ip=GetRemoteIpAddress(request)
    if len(ip.strip()) >0 :
        try:
            record = IpRecord.objects.get(ip=ip)
            html=RemoveCityAndCounty(record.city)
            
        except IpRecord.DoesNotExist:
            
            txt=GetIpInfoJson(ip)
        
            if txt["code"]==0:
                record=IpRecord(ip=ip,
                  country=txt["data"]["country"],
                  area=txt["data"]["area"],
                  region=txt["data"]["region"],
                  county=txt["data"]["county"],
                  isp=txt["data"]["isp"],
                  city=txt["data"]["city"])
                record.save()
                html=RemoveCityAndCounty(record.city)

    if(request.GET.__contains__("callback")):
        callback=request.GET["callback"]    
        html = callback+'("'+html+'")'
    
    return HttpResponse(html)

def index(request):
    return render_to_response('api/index.html')
