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

q = Queue()
thread_num = 10

getcookie_url = 'http://xueqiu.com'
#个股信息页面地址
data_url='http://xueqiu.com/stock/quote.json'
#股票代码列表页面地址

list_url = 'http://xueqiu.com/stock/cata/stocklist.json'

#美国212 中国84 香港69  英国144
country_id=69

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
    
    quote['exchange']='SEHK'
    quote_stock_symbol=quote['exchange']+':'+quote['symbol']

    cur.execute("select stock_symbol,country_id,industry_id from repository_listedcompany where stock_symbol='"+quote_stock_symbol.strip().replace("'","''")+"'")
    r = cur.fetchone()
    if r and r[2]:
        _country_id=country_id

        
        _industry_id=int(r[2])
       

        _time=parse(quote['time']).strftime('%Y-%m-%d %H:%M:%S')
        _afterHoursTime='null'

        

        sql_str="insert into repository_stock_quotes values(null,'%s','%s','%s','%s',%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s',%d,NOW())" % (quote['symbol'], quote['exchange'], quote['code'], quote['name'].strip().replace("'","''"),_industry_id,_country_id, quote['current'], quote['percentage'], quote['change'], quote['open'], quote['high'], quote['low'], quote['close'], quote['last_close'], quote['high52week'], quote['low52week'], quote['volume'], quote['volumeAverage'], quote['marketCapital'], quote['eps'], quote['pe_ttm'], quote['pe_lyr'], quote['beta'], quote['totalShares'], _time, quote['afterHours'], quote['afterHoursPct'], quote['afterHoursChg'], _afterHoursTime, quote['updateAt'], quote['dividend'], quote['yield'], quote['turnover_rate'], quote['instOwn'], quote['rise_stop'], quote['fall_stop'], quote['currency_unit'], quote['amount'], quote['net_assets'], quote['hasexist'], quote['type'], quote['flag'], quote['pb'], quote['benefit_before_tax'], quote['benefit_after_tax'], quote['float_shares'], quote['float_market_capital'], quote['psr'],getdata_idx)
        
        
        cur.execute(sql_str)        
        conn.commit()

    else:
        #print '>>>>>>>>>>>>>信息缺失>>>>>>>>>>>>>'
        stock_no_company_list.append(quote)

    pass


#具体的处理函数，负责处理单个任务
def get_single_stock_data(item,conn,cur):
    global current_idx
    current_idx+=1
    values = {'code':item['symbol'],'_':int(time.time())}
    data = urllib.urlencode(values)

    req = urllib2.Request(data_url+'?'+data)
    try:

        stock_data=json.loads(opener.open(req).read()) 

        quote=stock_data['quotes'][0]

        #print u'#%-6s%-20s 市盈率:%-15s 总市值:%s'%(str(current_idx),quote['exchange']+':'+quote['symbol'],quote['pe_ttm'],quote['marketCapital'])

        save_single_stock_data(quote,conn,cur)

    except Exception,e: 
        #print Exception,":",e
        error_list.append(item)

#这个是工作进程，负责不断从队列取数据并处理
def working():
    conn =  pymysql.connect(host=_host, port=_port,user=_user, passwd=_password,db=_dbname,charset='utf8')
    cur = conn.cursor()
    con_list.append(conn)
    cur_list.append(cur)

    #print '打开数据库连接'

    while True:
        item = q.get()
        get_single_stock_data(item,conn,cur)
        
        q.task_done()
'''
print '*'*80
print '开始登录系统'
print '*'*80
'''

#获取cookie
cookieJar=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

req=urllib2.Request(getcookie_url)
opener.addheaders=[('Host', 'xueqiu.com'),  
('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36'),  
('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),  
('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,fr;q=0.4,ja;q=0.2'),  
('Accept-Charset', 'utf-8;q=0.7,*;q=0.7'),   
('Connection', 'keep-alive'),   
('Referer', 'http://xueqiu.com/'),]

opener.open(req).read()



#获取数据
opener.addheaders=[('Host', 'xueqiu.com'),  
('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36'),  
('Accept', 'application/json, text/javascript, */*; q=0.01'),  
('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,fr;q=0.4,ja;q=0.2'),  
('Accept-Charset', 'utf-8;q=0.7,*;q=0.7'), 
('Connection', 'keep-alive'), 
('cache-control', 'no-cache'),  
('Referer', 'http://xueqiu.com/'),
('X-Requested-With', 'XMLHttpRequest'),]  
'''
print '*'*80
print '开始获取股票代码列表'
print '*'*80
'''
#获取页面数量
page_idx=1
page_size=90

values = {'page':page_idx,'size':page_size,'order':'desc','orderby':'percent','type':'30','_':int(time.time())}
data = urllib.urlencode(values)

req = urllib2.Request(list_url+'?'+data)

s = json.loads(opener.open(req).read())

page_num= int(math.ceil(float(s['count']['count'])/page_size))


m=0
#获取数据
for i in range(page_idx,page_num+1):
    page_idx=i
    values = {'page':page_idx,'size':page_size,'order':'desc','orderby':'percent','type':'30','_':int(time.time())}
    data = urllib.urlencode(values)
    
    req = urllib2.Request(list_url+'?'+data)

    s = json.loads(opener.open(req).read())
    for item in s['stocks']:
        m+=1
        #print '#%-6s%s%s'%(str(m),item['symbol'],item['name'])
        stock_list.append(item)



global_conn =  pymysql.connect(host=_host, port=_port,user=_user, passwd=_password,db=_dbname,charset='utf8')
global_cur = global_conn.cursor()


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
for item in stock_list:
    q.put(item)
#等待所有JOBS完成
q.join()



for cur in cur_list:
    cur.close()
for conn in con_list:
    conn.close()
    #print '关闭数据库连接'



f=open('no_company_hk.txt','w');

#打印上市公司列表中缺失的数据,用于补充新股资料
if len(stock_no_company_list)>0:
    '''
    print '*'*80
    print '打印缺失上市公司列表'
    print '*'*80
    '''

    for item in stock_no_company_list:
        f.write(item['exchange']+":"+item['symbol']+"\n")

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
        #print '#%-6s%s%s'%(str(m),item['symbol'],item['name'])

    #print '合计错误信息：%s条'%(len(error_list))


