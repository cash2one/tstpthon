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


cur.execute('SELECT * FROM industry_industry')
r = cur.fetchall()

cv_map_dict={}

for row in r:
    print row[1],row[0]
    cv_map_dict[row[1]]=row[0]



map_list=[]

map_file="data/ciq2cv.csv"

map_dict={}
for row in csv.reader(open(map_file,'rU'),delimiter=','):
    name_idx=int(row[0])

    if row[11] !="":
        cvname=row[11].split('-')[-1].decode('utf8')
        print cvname
        cvid=cv_map_dict[cvname]
        map_dict[row[name_idx]]=cvid
        #print row[name_idx],cvname

print map_dict




fname = "data/usa.csv"

start_num=0
num=0

for row in csv.reader(open(fname,'rU'), delimiter=','):

    num+=1
    if num<start_num:
        print 'pass'
        continue
    
    #cv_name=''
    
    city_id=None
    province_id=None
    country_id=None

    stock_name=row[0].replace("'","''")
    stock_symbol=''
    stock_symbol_no_pre=''
    stock_exchange_id=None
    stock_exchange_code=''
    cv_id=map_dict.get(row[22].decode('utf8'),0)
    name_cn=row[8].replace("'","''")
    name_en=row[9].replace("'","''")
    short_name_cn=''
    short_name_en=row[0].replace("'","''")
    intro_cn=''
    intro_en=row[21].replace("'","''")
    address_cn=''
    address_en=row[20].replace("'","''")
    website=row[18].replace("'","''")
    tel=''
    fax=''
    postcode=''
   
    list3=[]
    for i in range(len(row[3].split(','))):

        list3.append(row[4+i].split(':'))
   
    for item in list3:
        stock_symbol_no_pre=item[1].strip().upper()
        stock_exchange_code=item[0].strip().upper()
        stock_symbol=stock_exchange_code+":"+stock_symbol_no_pre
        
        tempstr='null'
        if cv_id!=0:
            tempstr=str(cv_id)


        sql_str="update repository_listedcompany set industry_id="+tempstr+" WHERE stock_symbol='"+stock_symbol+"'"

        print("Line"+str(num)+":"+sql_str)

        cur.execute(sql_str)        
        conn.commit()
  

cur.close()
conn.close()
