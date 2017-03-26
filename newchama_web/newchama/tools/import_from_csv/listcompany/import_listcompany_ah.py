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


fname = "../data/ah.csv"

start_num=0
num=0

for row in csv.reader(open(fname,'rU'), delimiter=','):

	num+=1
	if num<start_num:
		print 'pass'
		continue
	
	cv_name=''
	city_id=None
	province_id=None
	country_id=None

	stock_name=row[0].replace("'","''")
	stock_symbol=''
	stock_symbol_no_pre=''
	stock_exchange_id=None
	stock_exchange_code=''

	name_cn=row[8].replace("'","''")
	name_en=row[9].replace("'","''")
	short_name_cn=row[0].replace("'","''")
	short_name_en=row[0].replace("'","''")
	intro_cn=row[21].replace("'","''")
	intro_en=row[21].replace("'","''")
	address_cn=row[20].replace("'","''")
	address_en=row[20].replace("'","''")
	website=row[18].replace("'","''")
	tel=''
	fax=''
	postcode=''
	
	found_time=None
	if row[17]!="":
		try:
			found_time=datetime.strptime(row[17], "%m/%d/%y")
		except:
			try:
				found_time=datetime.strptime(row[17], "%m/%d/%Y")
			except:
				try:
					found_time=datetime.strptime(row[17], "%Y")
				except:
					pass
	

	list1=row[1].split(',')
	list2=row[3].split(',')
	list3=zip(list1,list2)

	
	#获取CV分类
	if row[12] !="":
		cv_name=row[12]
	elif row[11] !="":
		cv_name=row[11]
	elif row[10] !="":
		cv_name=row[10]


	cv_id=None
	if cv_name !="":
		cur.execute("select id from industry_industry where name_cn='"+cv_name+"'")
		t = cur.fetchone()
		if t !=None:
			cv_id=t[0]
			
	
	#获取地址id		
	address_list=row[19].strip().split(">")
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

	
	
	for item in list3:
		
		stock_symbol_no_pre=item[1].strip().upper()
		stock_exchange_code=item[0].strip().upper()
		stock_symbol=stock_exchange_code+":"+stock_symbol_no_pre

		
		cur.execute("select count(*) from repository_listedcompany where stock_symbol='"+stock_symbol+"'")
		r = cur.fetchone()
		
		
		if r[0]==0:

			cur.execute("select id from repository_stockexchange where code='"+item[0].strip().upper()+"'")
			t = cur.fetchone()
			stock_exchange_id=t[0]
			
			sql_str="insert into repository_listedcompany values(null,'%s','%s','%s','%s','%s','%s',%s,%s,%s,'%s','%s','%s','%s','%s','%s','%s',%s,'%s',%s,'%s','%s','%s',null,null,null)" % (name_cn,name_en,short_name_cn,short_name_en,intro_cn,intro_en,country_id or 'NULL',province_id or 'NULL',cv_id or 'NULL',address_cn,address_en,website,tel,fax,stock_symbol,postcode,stock_exchange_id or 'NULL',stock_exchange_code,city_id or 'NULL',stock_name,found_time,stock_symbol_no_pre)

			print("Line"+str(num)+":"+sql_str)

			cur.execute(sql_str)		
			conn.commit()
		else:

			print("Line"+str(num)+": pass!")





cur.close()
conn.close()

