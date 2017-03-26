#-*-encoding:utf-8-*-
import os,sys
sys.path.append(os.path.abspath('../../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings

_host=newchama.settings.DATABASES['default']['HOST']
_port=int(newchama.settings.DATABASES['default']['PORT'])
_user=newchama.settings.DATABASES['default']['USER']
_password=newchama.settings.DATABASES['default']['PASSWORD']
_dbname=newchama.settings.DATABASES['default']['NAME']

import urllib2,urllib,cookielib
import time,datetime
import json
import math
from threading import Thread
from Queue import Queue
from time import sleep
import pymysql
from decimal import *
from dateutil.parser import parse
from bs4 import BeautifulSoup


q = Queue()
thread_num = 10

#个股信息页面地址http://finance.yahoo.com/q?s=KFX.L&ql=0
data_url='http://finance.yahoo.com/q/ks'

#美国212 中国84 香港69  英国144
country_id=144

stock_list=[]
#获取数据错误列表
error_list=[]
#上市公司列表缺少的stock
stock_no_company_list=[] 
#当前处理条数
current_idx=0


getdata_idx=int(datetime.datetime.strftime(datetime.datetime.now(),'%y%m%d'))



con_list=[]
cur_list=[]



#保存个股信息
def save_single_stock_data(quote,conn,cur):

   
    
    _country_id=country_id
   


    sql_str="insert into repository_stock_quotes values(null,'%s','%s','%s','%s','%s',%d,null,null,null,null,null,null,null,null,null,null,null,null,'%s',null,'%s',null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,'USD',null,null,0,null,null,'%s',null,null,null,null,'%s',%d,NOW())" % (quote['symbol'], quote['exchange'], quote['code'], quote['name'].strip().replace("'","''"),quote['industry_id'], _country_id,quote['marketCapital'], quote['pe_ttm'].replace(',',''),quote['pb'].replace(',',''), quote['psr'].replace(',',''),getdata_idx)
    
    
    cur.execute(sql_str)        
    conn.commit()



#具体的处理函数，负责处理单个任务
def get_single_stock_data(stock,conn,cur):
    global current_idx
    current_idx+=1

    values = {'s':stock[0]+'.L'}
    data = urllib.urlencode(values)
    req = urllib2.Request(data_url+'?'+data)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36')
    

    quote={}


    try:
        res=urllib2.urlopen(req)
        

        soup = BeautifulSoup(res.read())

        list1=soup.find_all(name="td", attrs={"class":"yfnc_tabledata1"})

        if len(list1)>0:
            
            quote.update({'exchange':'LSE'})
            quote.update({'symbol':stock[0]})
            quote.update({'code':stock[0]})
            quote.update({'name':stock[2]})
            quote.update({'marketCapital':0})
            
            mc=list1[0].get_text().replace('N/A','')
            if len(mc)>0 and mc[-1]=="B":
                quote['marketCapital']=float(mc[0:-1])*100000000

            quote.update({'pe_ttm':list1[3].get_text().replace('N/A','')}) 
            quote.update({'pb':list1[6].get_text().replace('N/A','')})      
            quote.update({'psr':list1[5].get_text().replace('N/A','')})

            quote.update({'industry_id':stock[1]})

            #print u'#%-6s%-20s 市盈率:%-15s 总市值:%s'%(str(current_idx),quote['exchange']+':'+quote['symbol'],quote['pe_ttm'],quote['marketCapital'])    
            
            save_single_stock_data(quote,conn,cur)

        else:
            #print 'LSE:'+stock[0]+u'>>>>>>>>>>>>Lost>>>>>>>>>>>>>'
            stock_no_company_list.append('LSE:'+stock[0])
        
    except Exception,e: 
        #print Exception,":",e
        error_list.append('LSE:'+stock[0])

#这个是工作进程，负责不断从队列取数据并处理
def working():
    conn = pymysql.connect(host=_host, port=_port,user=_user, passwd=_password,db=_dbname,charset='utf8')
    cur = conn.cursor()
    con_list.append(conn)
    cur_list.append(cur)

    #print '打开数据库连接'

    while True:
        stock = q.get()
        get_single_stock_data(stock,conn,cur)
        
        q.task_done()




global_conn =  pymysql.connect(host=_host, port=_port,user=_user, passwd=_password,db=_dbname,charset='utf8')
global_cur = global_conn.cursor()
'''
print '*'*80
print '开始获取股票代码列表'
print '*'*80
'''
global_cur.execute("select stock_symbol_no_pre,industry_id,short_name_en from repository_listedcompany where stock_exchange_code='LSE'")
r = global_cur.fetchall()

for item in r:
    stock_list.append(item)



global_cur.execute("delete from repository_stock_quotes where country_id="+str(country_id)+" and getdata_index="+str(getdata_idx))
global_conn.commit()


global_cur.close()
global_conn.close()


'''
print '*'*80
print '开始获取个股数据'
print '*'*80
'''

#fork NUM个线程等待队列
for i in range(thread_num):
    t = Thread(target=working)
    t.setDaemon(True)
    t.start()

#把JOBS排入队列
for stock in stock_list:
    q.put(stock)
#等待所有JOBS完成
q.join()



for cur in cur_list:
    cur.close()
for conn in con_list:
    conn.close()
    #print '关闭数据库连接'


f=open('no_company_uk.txt','w');

#打印上市公司列表中缺失的数据,用于补充新股资料
if len(stock_no_company_list)>0:
    '''
    print '*'*80
    print '打印缺失上市公司列表'
    print '*'*80
    '''
    for item in stock_no_company_list:
        f.write(item+"\n")
        #print item

    #print '合计缺失数据：%s条'%(len(stock_no_company_list))

f.close()

#打印错误信息
if len(error_list)>0:
    '''
    print '*'*80
    print '打印错误列表'
    print '*'*80
    '''
    for item in error_list:
        pass
        #print item

    #print '合计错误信息：%s条'%(len(error_list))


