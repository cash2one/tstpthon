# -*- coding: utf-8 -*-  
import datetime
import json
import urllib2
from api import buildRequestString,AppKeyid,AppKey,initDB,convert_time,get_country_province_city

import logging

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='vc_error.log',
                filemode='a')

date_str = (datetime.datetime.now()+datetime.timedelta(days=-2)).strftime('%Y-%m-%d')

class VCItem(object):   
    pass


current_pageNo=1

request_dic = {'sysAppkey':AppKeyid, 'sysMethod':'cv.web.event.organization.list', 'sysV':'1.0', 'searchDate':date_str, 'sysFormat':'json','pageNo':current_pageNo}
pre_url=r'http://openapi.chinaventure.com.cn/router?'

session,query = initDB('repository_investmentcompany',VCItem)


def saveRecord(item):
    
    _vc=VCItem()
    _vc.name_cn=item['organizationCnName']
    _vc.short_name_cn=item['organizationCnShort']
    _vc.name_en=item['organizationEnName']
    _vc.short_name_en=item['organizationEnShort']

    _vc.found_time=convert_time(item['organizationSetUpTime'])
   

    if item['capitalRCnName']==u'中资':
        _vc.capital_type=1
    elif item['capitalRCnName']==u'外资':
        _vc.capital_type=2
    elif item['capitalRCnName']==u'中/外资':
        _vc.capital_type=3
    else:
        _vc.capital_type=0

    _vc.website=item['organizationWeb']
    
    _vc.country_id, _vc.province_id, _vc.city_id=get_country_province_city(item['organizationCity'])

    _vc.address_cn=item['organizationContactCnName']
    _vc.address_en=item['organizationContactCnName']                    
    _vc.intro_cn=item['organizationCnDESC']
    _vc.intro_en=item['organizationCnDESC']

    
    c = query.filter_by(name_cn=_vc.name_cn).first()
    
    if c:
        pass
        #print 'Exist:',_vc.name_cn
    else:
        session.add(_vc)
        #print 'Add:',_vc.name_cn 
    
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
        print e
        logging.error(e)





