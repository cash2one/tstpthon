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

import pymysql


conn = pymysql.connect(host=_host, port=_port,user=_user, passwd=_password,db=_dbname,charset='utf8')
cur = conn.cursor()


compare_num=10

#获取最近期数
getdata_idx=1
cur.execute('select max(getdata_index) from repository_stock_quotes')
result = cur.fetchone()
if result:
    getdata_idx=int(result[0])
'''
print '*'*80
print '开始统计第'+str(getdata_idx)+'期数据'
print '*'*80
'''
#美国212 中国84 香港69  英国144
country_list=[212,84,69,144]


#获取一级行业id及其子行业id
cv_level1_list={}

cur.execute('select * from industry_industry where level=1')
result_list = cur.fetchall()
for result in result_list:
    cv_level1_list.update({result[0]:[result[0]]})

cur.execute('select * from industry_industry')
result_list = cur.fetchall()
for result in result_list:
    if result[4]==2:
        cv_level1_list[result[5]].append(result[0])
    elif result[4]==3:
        cur.execute('select * from industry_industry where id='+str(result[5]))
        r = cur.fetchone()
        if r:
            cv_level1_list[r[5]].append(result[0])



#统计数据
f_dict={}

for country in country_list:
    f_dict.update({country:{}})

    for cv_level1 in cv_level1_list:
        f_dict[country].update({cv_level1:[]})

        str1='('
        for s in cv_level1_list[cv_level1]:
            str1 +=str(s)+','
        str1=str1[:-1]+')'
        
        #中国按ps排序，其他pe
        if country==84:
        
            q_str='select symbol,exchange,name,marketCapital,pe_ttm,pb,psr from repository_stock_quotes where hasexist=0 and getdata_index=%d and country_id=%d and cv_id in %s order by psr desc limit %d' % (getdata_idx,country,str1,compare_num)
        else:
            q_str='select symbol,exchange,name,marketCapital,pe_ttm,pb,psr from repository_stock_quotes where hasexist=0 and getdata_index=%d and country_id=%d and cv_id in %s order by pe_ttm desc limit %d' % (getdata_idx,country,str1,compare_num)
        

        cur.execute(q_str)
        
        r_list = cur.fetchall()

        for item in r_list:

            f_dict[country][cv_level1].append([country,cv_level1,item[0],item[1],item[2],item[4],item[5],item[6],item[3]])



#清空数据表   
cur.execute('delete from repository_compare_company')        
conn.commit()

for country_item in f_dict:
    for cv_item in f_dict[country_item]:
        

        for company in f_dict[country_item][cv_item]:


            sql_str="insert into repository_compare_company values(null,%d,%d,'%s','%s','%s',%f,%f,%f,%d)" % (company[0],company[1],company[2],company[3],company[4].strip().replace("'","''"),company[5],company[6],company[7],company[8])
            
            cur.execute(sql_str)        
            conn.commit()
            
            #print u'添加 %s %s %s 国家:%d 行业:%d PE:%f PB:%f PS:%f 市值:%d' % (company[2],company[3],company[4],company[0],company[1],company[5],company[6],company[7],company[8])


cur.close()
conn.close()