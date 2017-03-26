# -*- coding: utf-8 -*-  
import datetime
import json
import urllib2
from api import buildRequestString,AppKeyid,AppKey,initDB,convert_time,get_country_province_city,currency_to_usd,get_cvid

import logging

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='vc_error.log',
                filemode='a')

date_str = (datetime.datetime.now()+datetime.timedelta(days=-2)).strftime('%Y-%m-%d')

class VCItem(object):  
    pass

class VCHistoryItem(object):  
    pass


current_pageNo=1

request_dic = {'sysAppkey':AppKeyid, 'sysMethod':'cv.web.event.organizationHistory.list', 'sysV':'1.0', 'searchDate':date_str, 'sysFormat':'json','pageNo':current_pageNo}
pre_url=r'http://openapi.chinaventure.com.cn/router?'

session,query = initDB('repository_investmenthistory',VCHistoryItem)
session_vc,query_vc = initDB('repository_investmentcompany',VCItem)

def saveRecord(item):


    vc = query_vc.filter_by(name_cn=item['organizationCnName']).first()

    if vc :
        
        
        _history=VCHistoryItem()

        _history.company_id=vc.id
        _history.targetcompany=item['enterpriseCnShort']

        _history.type=item['FinancingeventCnName']

        if item['realityMoney'].isdigit():
            _history.amount=float(item['realityMoney'])            
            _history.currency=item['currencyCnName'].strip()            
            _history.usd=int(_history.amount*currency_to_usd.get(_history.currency,1)*10000)
       
        _history.person=item['personageName']

        
        _history.happen_date=convert_time(item['happenDate'])
       

     
        _history.country_id, _history.province_id, _history.city_id=get_country_province_city(item['district'])
        
        if item['cvIndustryOne']!='':
            _history.cv1=get_cvid(item['cvIndustryOne'],1)
        
        if item['cvIndustryTwo']!='':
            _history.cv2=get_cvid(item['cvIndustryTwo'],2)

        if item['cvIndustryThree']!='':
            _history.cv3=get_cvid(item['cvIndustryThree'],3)



        c2 = query.filter_by(targetcompany=_history.targetcompany,company_id=_history.company_id,happen_date=_history.happen_date,amount=_history.amount).first()
        
        if c2:
            pass
            #print 'Exist:',_history.targetcompany,_history.usd
        else:
            session.add(_history)
            #print 'Add:',_history.targetcompany,_history.usd
        
        session.flush()
        session.commit()
    

    

def getRecordByNO(pageNo):

    request_dic['pageNo']=current_pageNo
    url=buildRequestString(AppKeyid,AppKey,request_dic,pre_url)
    
    html = urllib2.urlopen(url)

    jsonobj = json.loads(html.read().decode('utf-8'))
   
    if pageNo==1:
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
            for i in range(2,totlePageNum+1):
                current_pageNo=i
                getRecordByNO(current_pageNo)

    except Exception,e:
        
        logging.error(e)





