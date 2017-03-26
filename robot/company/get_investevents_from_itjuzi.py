# -*- coding: utf-8 -*- 
import datetime
from api import get_html,bind_db,init_logging,Item

def mapper_item(soup):
    item=Item()
    
    _time=unicode(soup.select('#company-member-list tr')[0].select('td')[1].get_text())
    item.happen_time=datetime.datetime.strptime(_time,'%Y.%m.%d')

    item.company=soup.select('#company-member-list tr')[1].select('td')[1].get_text()

    item.field=soup.select('#company-member-list tr')[2].select('td')[1].get_text()
    item.money=soup.select('#company-member-list tr')[3].select('td')[1].get_text()
    item.round=soup.select('#company-member-list tr')[4].select('td')[1].get_text()
    _invest_company_list=soup.select('#company-member-list tr')[5].select('td a')
    if _invest_company_list and len(_invest_company_list)<=1:
        item.invest_company=_invest_company_list[0].get_text()
    else:
        item.invest_company=','.join([_company.get_text() for _company in _invest_company_list])


    item.desc=soup.select('#company-member-list tr')[7].select('td')[1].get_text()

    
    return item


def save_item(session,query,item):
    c = query.filter_by(company=item.company,round=item.round,money=item.money).first()
    
    if c:
        item.id=c.id
        session.merge(item)
        print u'更新:%s'%(item.company)

    else:
        session.add(item)
        print u'添加:%s'%(item.company)
        
    session.flush()
    session.commit()

logging=init_logging()
session,query=bind_db('itjuzi_investevents')


start_id=6767
end_id=6936

for num in range(start_id,end_id+1):
    print num
    try:
        _soup=get_html('http://itjuzi.com/investevents/'+str(num))
        _item=mapper_item(_soup)
        print _item.happen_time,_item.company,_item.invest_company
        save_item(session,query,_item)
    
    except Exception,e:
        print e
        logging.error(e)

