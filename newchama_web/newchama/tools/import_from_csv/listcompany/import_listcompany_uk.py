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

map_file="../data/ciq2cv.csv"

map_dict={}
for row in csv.reader(open(map_file,'rU'),delimiter=','):
    name_idx=int(row[0])

    if row[11] !="":
        cvname=row[11].split('-')[-1].decode('utf8')
        print cvname
        cvid=cv_map_dict[cvname]
        map_dict[row[name_idx]]=cvid
        #print row[name_idx],cvname



fname = "../data/uk.csv"

start_num=0
num=0

for row in csv.reader(open(fname,'rU'), delimiter=','):

	num+=1
	if num<start_num:
		print 'pass'
		continue
	
	
	
	city_id=None
	province_id=None
	country_id=None

	stock_name=row[0].replace("'","''")
	stock_symbol=''
	stock_symbol_no_pre=''
	stock_exchange_id=None
	stock_exchange_code=''
	

	cv_id=map_dict.get(row[19].decode('utf8'),0)
	cv_name='null'
	if cv_id!=0:
		cv_name=str(cv_id)

	name_cn=row[6].replace("'","''")
	name_en=row[6].replace("'","''")
	short_name_cn=row[0].replace("'","''")
	short_name_en=row[0].replace("'","''")
	intro_cn=row[18].replace("'","''")
	intro_en=row[18].replace("'","''")
	address_cn=row[17].replace("'","''")
	address_en=row[17].replace("'","''")
	website=row[15].replace("'","''")
	tel=''
	fax=''
	postcode=''
	
	found_time=None
	if row[14]!="":
		try:
			found_time=datetime.strptime(row[14], "%m/%d/%y")
		except:
			try:
				found_time=datetime.strptime(row[14], "%m/%d/%Y")
			except:
				try:
					found_time=datetime.strptime(row[14], "%Y")
				except:
					pass
	
	list3=[]
	for row1 in row[3].split(';'):

		list3.append(row1.split(':'))

	print list3	


	
	#获取地址id		
	address_list=row[16].strip().split(">")
	print address_list
	address_list.reverse()

	for address in address_list:
		if address != "":
			address=address.replace('United States','United States of America')
			
			cur.execute("select id,province_id from area_city where name_en='"+address+"'")
			t = cur.fetchone()
			if t !=None:
				city_id=t[0]
				province_id=t[1]

				cur.execute("select country_id from area_province where id="+str(province_id))
				m = cur.fetchone()
				if m !=None:
					country_id=m[0]

			else:
				cur.execute("select id,country_id from area_province where name_en='"+address+"'")
				t = cur.fetchone()
				if t !=None:
					province_id=t[0]
					country_id=t[1]
				else:
					cur.execute("select id from area_country where name_en='"+address+"'")
					t = cur.fetchone()
					if t !=None:
						country_id=t[0]

	
	
	for item in list3:
		print item
		stock_symbol_no_pre=item[1].strip().upper()
		stock_exchange_code=item[0].strip().upper()
		stock_symbol=stock_exchange_code+":"+stock_symbol_no_pre

		
		cur.execute("select count(*) from repository_listedcompany where stock_symbol='"+stock_symbol+"'")
		r = cur.fetchone()
		
		
		if r[0]==0:
			print item[0].strip().upper()
			cur.execute("select id from repository_stockexchange where code='"+item[0].strip().upper()+"'")
			t = cur.fetchone()
			if t:
				stock_exchange_id=t[0]
			else:
				sql_str="insert into repository_stockexchange values(null,'%s','%s','%s','%s','%s')" % (item[0].strip().upper(),'-',item[0].strip().upper(),'-',item[0].strip().upper())

				print(sql_str)
				cur.execute(sql_str)		
				conn.commit()
				cur.execute("select id from repository_stockexchange where code='"+item[0].strip().upper()+"'")
				t = cur.fetchone()
				stock_exchange_id=t[0]



			sql_str="insert into repository_listedcompany values(null,'%s','%s','%s','%s','%s','%s',%s,%s,%s,'%s','%s','%s','%s','%s','%s','%s',%s,'%s',%s,'%s','%s','%s',null,null,null)" % (name_cn,name_en,short_name_cn,short_name_en,intro_cn,intro_en,country_id or 'NULL',province_id or 'NULL',cv_name,address_cn,address_en,website,tel,fax,stock_symbol,postcode,stock_exchange_id or 'NULL',stock_exchange_code,city_id or 'NULL',stock_name,found_time,stock_symbol_no_pre)

			print("Line"+str(num)+":"+sql_str)

			cur.execute(sql_str)		
			conn.commit()
		else:

			print("Line"+str(num)+": pass!")




cur.close()
conn.close()

