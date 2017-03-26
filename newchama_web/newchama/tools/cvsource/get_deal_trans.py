#-*-encoding:utf-8-*-
import os,sys
sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('/var/www/newchama'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
#from django.conf import settings
#settings.configure()

from services.models import TransDeal
import csv
from decimal import Decimal

import datetime
import json
import urllib2
from api import buildRequestString,AppKeyid,AppKey,initDB,convert_time,get_country_province_city,get_cvid,currency_to_usd

import logging

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='deal_error.log',
                filemode='a')

date_str = (datetime.datetime.now()+datetime.timedelta(days=-2)).strftime('%Y-%m-%d')



current_pageNo=0

request_dic = {'sysAppkey':AppKeyid, 'sysMethod':'cv.web.event.financing.list', 'sysV':'1.0', 'searchDate':date_str, 'sysFormat':'json','pageNo':current_pageNo}
pre_url=r'http://openapi.chinaventure.com.cn/router?'



def saveRecord(item):

   
    _item=TransDeal()

    _item.deal_type=1  
    _item.content=item['cnDesc']
    _item.happen_date=convert_time(item['happenDate'])

    _item.target_company=item['enterpriseCnName']
    

    _item.cv1=get_cvid(item['cvIndustryCnNameONE'],1)
    _item.cv2=get_cvid(item['cvIndustryCnNameTWO'],2)
    _item.cv3=get_cvid(item['cvIndustryCnNameTHREE'],3)



    _item.currency=item['currencyCnName']

    if item['realityMoney'] and item['realityMoney'].isdigit():
        _item.amount=Decimal(item['realityMoney'].replace(',',''))

    if _item.amount:
        _item.amount_usd=int(float(_item.amount)*currency_to_usd.get(_item.currency,1)*10000) 

    _item.country_id,_item.province_id,_item.city_id=get_country_province_city(item['districtName'])

    _item.invest_company=item['investOrgCnName']
    _item.invest_stage=item['developmentStage']
    _item.invest_type=item['financingRounds']

    if item['equity']:
        _item.equity=float(item['equity'])

    if item['businessValuation']:
        _item.market_value=float(item['businessValuation'].replace(',',''))*1000000

    _item.update_time=convert_time(item['updateTime'])
    _item.add_time=datetime.datetime.now()
    _item.finance_advisor=item['financingLinehelpNames']

    _item.title=u"%s融资%s%s"%(_item.target_company,_item.amount,_item.currency)
    
    


    old_buy_record=TransDeal.objects.filter(happen_date=_item.happen_date,target_company=_item.target_company)
    if len(old_buy_record) == 0:
        _item.save()
        
        #print('%s saved!' % (_item))
    else:
        pass
        #print('%s is existed!' % (_item))



def getRecordByNO(pageNo):

    request_dic['pageNo']=current_pageNo
    url=buildRequestString(AppKeyid,AppKey,request_dic,pre_url)
    html = urllib2.urlopen(url)

    jsonobj = json.loads(html.read().decode('utf-8'))
   
    if pageNo==0:
        '''
        print("="*80)
        print("date:"+date_str+"   total page count:"+str(jsonobj['page']['totalCount']))
        print("="*80)
        '''

    for item in jsonobj['list']:
        saveRecord(item)
        
    return jsonobj['page']['totalPages']


if __name__=="__main__":

    try:    
        totlePageNum=getRecordByNO(current_pageNo)

        if totlePageNum>1:
            for i in range(1,totlePageNum):
                current_pageNo=i
                getRecordByNO(current_pageNo)

    except Exception,e:
        print e
        logging.error(e)





