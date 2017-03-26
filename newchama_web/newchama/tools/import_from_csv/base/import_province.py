# -*- coding: utf-8 -*-  
import pymysql
import csv


conn = pymysql.connect(host='newchama.mysql.rds.aliyuncs.com', port=3306,user='newchama', passwd='newchama1234',db='newchama',charset='utf8')
cur = conn.cursor()


fname = "city_data.csv"

for row in csv.reader(open(fname,'rU'), delimiter=';'):
	if row[4] !="":

		cur.execute("select count(*) from area_province where name_en='"+row[4].strip().replace("'","''")+"'")
		r = cur.fetchone()
		if r[0]==0:

			cur.execute("select id from area_country where name_en='"+row[2].strip().replace("'","''")+"'")
			t = cur.fetchone()
			fid=t[0]

			sql_str="insert into area_province values(null,%d,'%s','%s')" % (fid,row[4].strip().replace("'","''"),row[5].strip().replace("''","''"))

			print(sql_str)
			cur.execute(sql_str)		
			conn.commit()


'''

['040304', '\xe5\xba\x9f\xe7\x89\xa9\xe5\x8f\x8a\xe5\x8d\xb1\xe9\x99\xa9\xe5\x93\x81\xe6\xb2\xbb\xe7\x90\x86', '\xe4\xb8\x89\xe7\xba\xa7', '\xe8\x83\xbd\xe6\xba\x90\xe5\x8f\x8a\xe7\x9f\xbf\xe4\xb8\x9a', '\xe7\x8e\xaf\xe4\xbf\x9d\xe8\x8a\x82\xe8\x83\xbd', '\xe5\xba\x9f\xe7\x89\xa9\xe5\x8f\x8a\xe5\x8d\xb1\xe9\x99\xa9\xe5\x93\x81\xe6\xb2\xbb\xe7\x90\x86', 'Hazardous waste treatment  ', 'Energy and mining ', 'Green energy ', 'Hazardous waste treatment  ']
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

