# -*- coding: utf-8 -*-  
import pymysql



conn = pymysql.connect(host='222.73.18.55', port=3306,user='urara', passwd='urara',db='urara',charset='utf8')
cur = conn.cursor()


f=open("keyword.txt",'r')


for row in f:

	print row

	cur.execute("select count(*) from keyword where name='"+row.strip()+"'")
	r = cur.fetchone()
	if r[0]==0:

		sql_str="insert into keyword values(null,'%s')" % (row.strip())

		print(sql_str)
		cur.execute(sql_str)		
		conn.commit()



cur.close()
conn.close()

