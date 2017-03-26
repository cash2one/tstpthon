# -*- coding: utf-8 -*-  
import pymysql
import csv
from datetime import *

conn = pymysql.connect(host='newchama.mysql.rds.aliyuncs.com', port=3306,user='newchama', passwd='newchama1234',db='newchama',charset='utf8')
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
        ciq_name=row[name_idx].replace("'","''")
        cvname=row[11].split('-')[-1].decode('utf8')
        print ciq_name,cvname
        cvid=cv_map_dict[cvname]

        cur.execute("select count(*) from repository_ciq2cv where ciq_name='"+ciq_name+"'")
        r = cur.fetchone()
          
        if r[0]==0:

            sql_str="insert into repository_ciq2cv values(null,'%s','%s','%d')" % (ciq_name,cvname,cvid)

            print sql_str
            cur.execute(sql_str)        
            conn.commit()
        

cur.close()
conn.close()
