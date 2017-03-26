# -*- coding: utf-8 -*-  
import pymysql
import csv
from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import datetime


conn = pymysql.connect(host='newchama.mysql.rds.aliyuncs.com', port=3306,user='newchama', passwd='newchama1234',db='newchama',charset='utf8')
cur = conn.cursor()



class VCItem(object):
    
    pass

db_config = {'host': 'newchama.mysql.rds.aliyuncs.com', 'port':3306, 'user': 'newchama', 'passwd': 'newchama1234', 'db':'newchama', 'charset':'utf8'}

engine = create_engine('mysql://%s:%s@%s/%s?charset=%s'%(db_config['user'], db_config['passwd'], db_config['host'], db_config['db'], db_config['charset']), echo=False)

metadata = MetaData(engine)

vc_table = Table('repository_investmentcompany', metadata, autoload=True)

mapper(VCItem, vc_table)
Session = sessionmaker(bind=engine)
session = Session()
query = session.query(VCItem)

vc_list=[]


fname = "vc.csv"
m=1
for row in csv.reader(open(fname,'rU'), delimiter=','):
    

    _vc=VCItem()
    _vc.name_cn=row[0]
    _vc.short_name_cn=row[1]
    _vc.name_en=row[2]
    _vc.short_name_en=row[3]

    found_time=None
    if row[4]!="":
        try:
            found_time=datetime.strptime(row[4], "%m/%d/%y")
        except:
            try:
                found_time=datetime.strptime(row[4], "%m/%d/%Y")
            except:
                try:
                    found_time=datetime.strptime(row[4], "%Y")
                except:
                    pass


    _vc.found_time=found_time
    #_vc.name_cn=row[5]
    
    if row[6]=='中资':
        _vc.capital_type=1
    if row[6]=='外资':
        _vc.capital_type=2
    if row[6]=='中/外资':
        _vc.capital_type=3


    _vc.website=row[10]
    

    city_id=None
    province_id=None
    country_id=None

    #获取地址id     
    address_list=row[11].strip().split(">")
    address_list.reverse()

    for address in address_list:
        if address != "":
            address=address.replace('Hong Kong','中国香港')
            address=address.replace('China','中国')
            cur.execute("select id,province_id from area_city where name_cn='"+address+"'")
            t = cur.fetchone()
            if t !=None:
                city_id=t[0]
                province_id=t[1]

                cur.execute("select country_id from area_province where id="+province_id)
                m = cur.fetchone()
                if m !=None:
                    country_id=m[0]

            else:
                cur.execute("select id,country_id from area_province where name_cn='"+address+"'")
                t = cur.fetchone()
                if t !=None:
                    province_id=t[0]
                    country_id=t[1]
                else:
                    cur.execute("select id from area_country where name_cn='"+address+"'")
                    t = cur.fetchone()
                    if t !=None:
                        country_id=t[0]

    _vc.country_id=country_id
    _vc.province_id=province_id
    _vc.city_id=city_id
                        
    _vc.intro_cn=row[13]
    _vc.intro_en=row[13]

    vc_list.append(_vc)
    #print '#%d 读取:%s'%(m,_vc.name_cn)

    c = query.filter_by(name_cn=_vc.name_cn).first()
    
    if c:
        print '#%d 存在:%s'%(m,_vc.name_cn)
    else:
        session.add(_vc)
        print '#%d 添加:%s'%(m,_vc.name_cn)
    
    session.flush()
    session.commit()
    m+=1
    



cur.close()
conn.close()



