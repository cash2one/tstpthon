# -*- coding: utf-8 -*-  
import pymysql
import csv


conn = pymysql.connect(host='newchama.mysql.rds.aliyuncs.com', port=3306,user='newchama', passwd='newchama1234',db='newchama',charset='utf8')
cur = conn.cursor()

currency_to_usd={
'万元':1/6.1306,
'万加元':1/1.0961,
'万台币':1/29.9790,
'万新元':1/1.2635,
'万新西兰元':0.8188,
'万日元':1/106.8900,
'万欧元':1.2911,
'万港元':1/7.7497,
'万澳元':0.9184,
'万美元':1,
'万英镑':1.6202,
'万韩元':1/1036
}

for k,v in currency_to_usd.items():
	cur.execute("update cvsource_deals set amount_usd=10000*amount*"+str(v)+" WHERE currency='"+k+"'")
	conn.commit()



'''
#cur.execute("insert into industry_industry values(null,'a','a','10001',1,null)")
#cur.execute("delete from industry_industry where name_cn='a'")
#cur.execute("update industry_industry set code='100003' WHERE name_cn='Energy_2'")


#cur.execute('select * from industry_industry')
#r = cur.fetchall()
#print r

#cur.execute('select count(*) from industry_industry')
#cur.execute('select * from industry_industry where id=7')
#r = cur.fetchone()
#print r
#conn.commit()
'''



cur.close()
conn.close()

