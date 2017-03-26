# -*- coding: utf-8 -*- 
import chardet
import urllib2
import zlib
from bs4 import BeautifulSoup
from sqlalchemy import *
from sqlalchemy.orm import *
import pymysql
import datetime,time

db_config = {'host': 'olive2014.mysql.rds.aliyuncs.com', 'port':3306, 'user': 'stock', 'passwd': 'olive2014', 'db':'stock', 'charset':'utf8'}


import logging
def init_logging():
    logging.basicConfig(level=logging.INFO ,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='itjuzi.log',
                    filemode='a')
    return logging

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

class Item(object):
    pass

def bind_db(table_name):

    engine = create_engine('mysql://%s:%s@%s/%s?charset=%s'%(db_config['user'], db_config['passwd'], db_config['host'], db_config['db'], db_config['charset']), echo=False)

    metadata = MetaData(engine)

    _table = Table(table_name, metadata, autoload=True)

    mapper(Item, _table)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Item)
    return session,query

def get_html(url):
       
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36')

    res=urllib2.urlopen(req)
    html=auto_decode_html(res)
        
    soup = BeautifulSoup(html)
    return soup

def save_item(session,query,item):
    c = query.filter_by(name=item.name).first()
    
    if c:
        item.id=c.id
        session.merge(item)
        print u'更新:%s'%(item.name)

    else:
        session.add(item)
        print u'添加:%s'%(item.name)
        
    session.flush()
    session.commit()
