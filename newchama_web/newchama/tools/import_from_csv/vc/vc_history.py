# -*- coding: utf-8 -*-  
import pymysql
import csv
from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import datetime

class City(object):  
    pass

class Province(object):  
    pass

class Country(object):  
    pass

class VCItem(object):  
    pass

class VCHistoryItem(object):  
    pass

class IndustryItem(object):  
    pass

        

db_config = {'host': 'newchama.mysql.rds.aliyuncs.com', 'port':3306, 'user': 'newchama', 'passwd': 'newchama1234', 'db':'newchama', 'charset':'utf8'}

engine = create_engine('mysql://%s:%s@%s/%s?charset=%s'%(db_config['user'], db_config['passwd'], db_config['host'], db_config['db'], db_config['charset']), echo=False)

metadata = MetaData(engine)

vc_table = Table('repository_investmentcompany', metadata, autoload=True)
vc_history_table = Table('repository_investmenthistory', metadata, autoload=True)
city_table = Table('area_city', metadata, autoload=True)
province_table = Table('area_province', metadata, autoload=True)
country_table = Table('area_country', metadata, autoload=True)
industry_table = Table('industry_industry', metadata, autoload=True)


mapper(VCItem, vc_table)
mapper(VCHistoryItem, vc_history_table)
mapper(City, city_table)
mapper(Province, province_table)
mapper(Country, country_table)
mapper(IndustryItem,industry_table)
Session = sessionmaker(bind=engine)
session = Session()


query1 = session.query(VCItem)
query2 = session.query(VCHistoryItem)
query3 = session.query(City)
query4 = session.query(Province)
query5 = session.query(Country)
query6 = session.query(IndustryItem)

currency_to_usd={
u'万元':1/6.1306,
u'万加元':1/1.0961,
u'万台币':1/29.9790,
u'万新元':1/1.2635,
u'万新西兰元':0.8188,
u'万日元':1/106.8900,
u'万欧元':1.2911,
u'万港元':1/7.7497,
u'万澳元':0.9184,
u'万美元':1,
u'万英镑':1.6202,
u'万韩元':1/1036,
}




fname = "vc_history.csv"
m=0
start_idx=0
for row in csv.reader(open(fname,'rU'), delimiter=','):
    m+=1
    if m<start_idx:

        continue
    c1 = query1.filter_by(name_cn=row[0]).first()
    
    if c1:


        _history=VCHistoryItem()

        _history.company_id=c1.id
        _history.targetcompany=row[1]

        _history.type=row[8]

        if row[9].isdigit():
            _history.amount=float(row[9])
            _history.currency=unicode(row[10].strip().decode('utf-8'))
        
            _history.usd=int(_history.amount*currency_to_usd.get(_history.currency,1)*10000)
        _history.person=row[6]

        happen_date=None
        if row[7]!="":
            try:
                happen_date=datetime.strptime(row[7], "%m/%d/%y")
            except:
                try:
                    happen_date=datetime.strptime(row[7], "%m/%d/%Y")
                except:
                    try:
                        happen_date=datetime.strptime(row[7], "%Y")
                    except:
                        pass


        _history.happen_date=happen_date
       

        city_id=None
        province_id=None
        country_id=None

        #获取地址id     
        address_list=row[5].strip().split(">")
        address_list.reverse()

        for address in address_list:
            if address != "":
                address=address.replace('Hong Kong','中国香港')
                address=address.replace('China','中国')
                c3 = query3.filter_by(name_cn=address).first()
                if c3:
                    city_id=c3.id
                    province_id=c3.province_id

                    c4 = query4.filter_by(id=province_id).first()

                    if c4:
                        country_id=c4.country_id

                else:
                    c4 = query4.filter_by(name_cn=address).first()

                    if c4:
                        province_id=c4.id
                        country_id=c4.country_id
                    else:
                        
                        c5 = query5.filter_by(name_cn=address).first()

                        if c5:
                            country_id=c5.id

        _history.country_id=country_id
        _history.province_id=province_id
        _history.city_id=city_id
        
        if row[2]!='':
            c6 = query6.filter_by(name_cn=row[2],level=1).first()
            if c6:
               _history.cv1=c6.id
        
        if row[3]!='':
            c6 = query6.filter_by(name_cn=row[3],level=2).first()
            if c6:
               _history.cv2=c6.id

        if row[4]!='':
            c6 = query6.filter_by(name_cn=row[4],level=3).first()
            if c6:
               _history.cv3=c6.id


        
        

        c2 = query2.filter_by(targetcompany=_history.targetcompany,company_id=_history.company_id,happen_date=_history.happen_date,amount=_history.amount).first()
        
        if c2:
            print '#%d 存在:%s-$%s'%(m,_history.targetcompany,_history.usd)
        else:
            session.add(_history)
            print '#%d 添加:%s-$%s'%(m,_history.targetcompany,_history.usd)
        
        session.flush()
        session.commit()
    
    




