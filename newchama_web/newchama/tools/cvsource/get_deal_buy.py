#-*-encoding:utf-8-*-
import os,sys
sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('/var/www/newchama'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
#from django.conf import settings
#settings.configure()

from services.models import BuyTogetherDeal
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

request_dic = {'sysAppkey':AppKeyid, 'sysMethod':'cv.web.event.buytogether.list', 'sysV':'1.0', 'searchDate':date_str, 'sysFormat':'json','pageNo':current_pageNo}
pre_url=r'http://openapi.chinaventure.com.cn/router?'



def saveRecord(item):
    
    

    _item =BuyTogetherDeal()
    _item.deal_type=2

    _item.title=item['cnName']
    _item.content=item['desc']

    _item.happen_date=convert_time(item['happenDate'])
    
    _item.end_time=convert_time(item['endDate'])
    _item.target_company=item['epCnName']
    

    _item.cv1=get_cvid(item['cvIndustryOne'],1)
    _item.cv2=get_cvid(item['cvIndustryTwo'],2)
    _item.cv3=get_cvid(item['cvIndustryThree'],3)

    _item.buy_type=item['type']
    _item.dstrict=item['dstrict']
    _item.state=item['state']
    _item.buy_way=item['tBuyWay']
    _item.attitude_name=item['attitudeName']
    _item.whether_trade=item['whetherTrade']
    _item.pay_style=item['payStyle']

    _item.country_id,_item.province_id,_item.city_id=get_country_province_city(item['epAddress'])

    
    if item.has_key('buyEpList') and item['buyEpList']:
        _item.buy_company=item['buyEpList'][0]['cnName']
        
    
    if item.has_key('sellEpList') and item['sellEpList']:
        _item.sale_company=item['sellEpList'][0]['cnName']

    _item.currency=item['currency']

    if item['money'] and item['money'].isdigit():
        _item.amount=Decimal(item['money'].replace(',',''))

    if _item.amount:
        _item.amount_usd=int(float(_item.amount)*currency_to_usd.get(_item.currency,1)*10000) 

 

    if item['stockRight']:
        _item.equity=float(item['stockRight'])

    
    _item.update_time=convert_time(item['updateTime'])
    _item.add_time=datetime.datetime.now()


    if item['sellerIncome']:
        _item.sales_income=float(item['sellerIncome'].replace(',',''))*10000

    if item['totalAssets']:
        _item.total_assets=float(item['totalAssets'].replace(',',''))*10000

    if item['netAsset']:
        _item.net_assets=float(item['netAsset'].replace(',',''))*10000

    if item['net']:
        _item.net_margin=float(item['net'].replace(',',''))*10000


    if item['PRATIO']:
        _item.pe=float(item['PRATIO'])

    if item['sellsRates']:
        _item.ps=float(item['sellsRates'])

    if item['cleanRates']:
        _item.pb=float(item['cleanRates'])
    
    if item['tradeFrontStock']:
        _item.before_equity=float(item['tradeFrontStock'])
          
    if item['tradeLaterStock']:
        _item.after_equity=float(item['tradeLaterStock'])

    _item.buy_company_intro=item['buyerDESC']
    _item.sale_company_intro=item['enterpriseCnDESC']


    old_buy_record=BuyTogetherDeal.objects.filter(happen_date=_item.happen_date,target_company=_item.target_company)
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
        pass

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





