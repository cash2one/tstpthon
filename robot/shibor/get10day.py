# -*- coding: utf-8 -*- 
import chardet
import urllib2
import zlib
from bs4 import BeautifulSoup
from sqlalchemy import *
from sqlalchemy.orm import *
import pymysql
import datetime,time

import logging

logging.basicConfig(level=logging.INFO ,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='log/shibor.log',
                filemode='a')

def auto_decode_html(response):
    html=response.read()

    respInfo = response.info()
    if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")) :
        html = zlib.decompress(html, 16+zlib.MAX_WBITS);

    encoding =chardet.detect(html)
    
    if encoding['encoding']=='GB2312':
        html=html.decode('GBK')
    elif encoding['encoding']=='utf-8':
        html=html.decode('utf-8')

    return html

class ShiborItem(object):
    
    pass

db_config = {'host': 'olive2014.mysql.rds.aliyuncs.com', 'port':3306, 'user': 'stock', 'passwd': 'olive2014', 'db':'stock', 'charset':'utf8'}

engine = create_engine('mysql://%s:%s@%s/%s?charset=%s'%(db_config['user'], db_config['passwd'], db_config['host'], db_config['db'], db_config['charset']), echo=False)

metadata = MetaData(engine)

shibor_table = Table('shibor', metadata, autoload=True)

mapper(ShiborItem, shibor_table)
Session = sessionmaker(bind=engine)
session = Session()
query = session.query(ShiborItem)




shibor_list=[]

url='http://www.shibor.org/shibor/ShiborTendaysShow.do'
req = urllib2.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36')
try:
    res=urllib2.urlopen(req)
    html=auto_decode_html(res)

    soup = BeautifulSoup(html)
    list1 = soup.select('.shiborquxian2 > tr')

    for item in list1:
        data_list=[]
        for item1 in item.select('td'):
            data_list.append(item1.get_text())
        

        _shibor_item=ShiborItem()
        _shibor_item.date=datetime.datetime.strptime(data_list[0],'%Y-%m-%d')
        _shibor_item.on=data_list[1]
        _shibor_item.w1=data_list[2]
        _shibor_item.w2=data_list[3]
        _shibor_item.m1=data_list[4]
        _shibor_item.m3=data_list[5]
        _shibor_item.m6=data_list[6]
        _shibor_item.m9=data_list[7]
        _shibor_item.y1=data_list[8]

        shibor_list.append(_shibor_item)

    last_date=datetime.datetime.strptime('2000-01-01','%Y-%m-%d')

    c = query.order_by(desc(ShiborItem.date)).first()
    if c:
        last_date=c.date


    for shibor in shibor_list:
        if shibor.date > last_date:
            print shibor.date,shibor.on

            session.add(shibor)

    session.flush()
    session.commit()
    logging.info('update is ok!')

except Exception,e:
    print e
    logging.error(e)


