# -*- coding: utf-8 -*- 
import datetime
from api import get_html,bind_db,init_logging,Item,save_item

def mapper_item(soup):
    item=Item()

   
    _img_list=soup.select('#company_big_show')
        

    if len(_img_list)>0:
        item.images=_img_list[0]['src']
        
    
    _name_list=soup.select('#com_id_value')
    
    if len(_name_list)>0:
        item.name=_name_list[0].get_text().strip()
    
    
    _fund_status_list=soup.select('#company-fund-status')
    if len(_fund_status_list)>0:
        
        item.fund_status=_fund_status_list[0].get_text().strip()
    list1 = soup.select('.detail-info > li')
    
    for _item in list1:
        inner_list=_item.get_text().replace(u'：',':').split(':')
        if len(inner_list)>0:
            _inner_label=inner_list[0].strip()
            _inner_text=u''
            if len(inner_list)>1:
                _inner_text=unicode(inner_list[1].strip())
        if _inner_label ==u'网址':
            if len(inner_list)>2:
                item.website=inner_list[2].replace('//','').strip()
        if _inner_label ==u'公司':
            item.company_name=_inner_text
        if _inner_label ==u'时间':
            _time=unicode(_inner_text).replace(u'年','-').replace(u'月','-')
            item.foundation_time=datetime.datetime.strptime(_time,'%Y-%m-')
        if _inner_label ==u'状态':
            item.status=_inner_text
        if _inner_label ==u'阶段':
            item.stage=_inner_text
        if _inner_label ==u'领域':
            item.field=_inner_text
        
        if _inner_label ==u'地点':
            _local=_inner_text.split(',')
            if _local[0].strip() in [u'南美洲',u'大洋洲',u'北美洲',u'欧洲',u'国外']:
                item.continent=_local[0].strip()
                item.country=_local[1].strip()
            else:   
                item.continent="亚洲"
                item.country="中国"
                item.province=_local[0].strip()
                item.city=_local[1].strip()
        if _inner_label ==u'简介':
            item.desc=_inner_text
                
        if _inner_label ==u'Tag标签':
            item.tags=_inner_text.replace(' ','')


    return item

logging=init_logging()
session,query=bind_db('itjuzi_company')


start_id=16676
end_id=17089

for num in range(start_id,end_id+1):
    print num
    try:
        _soup=get_html('http://itjuzi.com/company/'+str(num))
        _item=mapper_item(_soup)
        print _item.name,_item.desc
        save_item(session,query,_item)
    
    except Exception,e:
        print e
        logging.error(e)

