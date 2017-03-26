# -*- coding: utf-8 -*-  
import pymysql
import csv
from datetime import *
import os,sys
sys.path.append(os.path.abspath('../../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings

_host=newchama.settings.DATABASES['default']['HOST']
_port=int(newchama.settings.DATABASES['default']['PORT'])
_user=newchama.settings.DATABASES['default']['USER']
_password=newchama.settings.DATABASES['default']['PASSWORD']
_dbname=newchama.settings.DATABASES['default']['NAME']


conn = pymysql.connect(host=_host, port=_port,user=_user, passwd=_password,db=_dbname,charset='utf8')
cur = conn.cursor()

cur.execute("select count(*) as num,stock_symbol from repository_listedcompany  group by stock_symbol order by num")
        
r = cur.fetchall()
m_list=[]
for row in r:
    if row[0]>1:
        m_list.append(row[1])

print len(m_list)

for item in m_list:
    print item
    cur.execute("select id,invest_field from repository_listedcompany  where stock_symbol='%s' order by id desc"%(item))
    r=cur.fetchall()
    has_field=False
    idx=1
    print r
    for row1 in r:
        
        if row1[1]:
            has_field=True
        else:
            if idx==len(r):
                if has_field:
                    cur.execute("delete from repository_listedcompany  where id=%d "%(row1[0]))
                    conn.commit()
                    print 'delete %d'%(row1[0])
            else:
                cur.execute("delete from repository_listedcompany  where id=%d "%(row1[0]))
                conn.commit()
                print 'delete %d'%(row1[0])
        idx+=1


cur.close()
conn.close()
