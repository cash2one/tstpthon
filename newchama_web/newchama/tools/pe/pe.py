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


#获取最近期数
getdata_idx=1
cur.execute('select max(getdata_index) from repository_stock_quotes')
result = cur.fetchone()
if result:
    getdata_idx=int(result[0])
'''
print '*'*80
print 'Start No:'+str(getdata_idx)+'Data'
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
        
        q_str='select marketCapital,pe_ttm,pb,psr from repository_stock_quotes where hasexist=0 and getdata_index=%d and country_id=%d and cv_id in %s' % (getdata_idx,country,str1)
        cur.execute(q_str)
        
        r_list = cur.fetchall()

        all_pe,agv_pe,all_pe_marketCapital=0,0,0

        all_pb,agv_pb,all_pb_marketCapital=0,0,0

        all_ps,agv_ps,all_ps_marketCapital=0,0,0

        for item in r_list:
            
            
            if item[0]>0 and item[1]>0:
                all_pe_marketCapital+=item[0]
                all_pe+=item[1]*item[0]
            
            if item[0]>0 and item[2]!=0:    
                all_pb_marketCapital+=item[0]
                all_pb+=item[2]*item[0]
            
            if item[0]>0 and item[3]!=0: 
                all_ps_marketCapital+=item[0]
                all_ps+=item[3]*item[0]

        if all_pe_marketCapital>0:
            agv_pe=all_pe/all_pe_marketCapital

        if all_pb_marketCapital>0:
            agv_pb=all_pb/all_pb_marketCapital
            
        if all_ps_marketCapital>0:
            agv_ps=all_ps/all_ps_marketCapital
            

        f_dict[country][cv_level1]=[agv_pe,agv_pb,agv_ps]


for country_item in f_dict:
    for cv_item in f_dict[country_item]:
        #print country_item,cv_item,f_dict[country_item][cv_item]

        sql_str="update repository_industry_pe set pe=%f,pb=%f,ps=%f where industry_id=%d and country_id=%d " % (f_dict[country_item][cv_item][0],f_dict[country_item][cv_item][1],f_dict[country_item][cv_item][2],cv_item,country_item)
        
        cur.execute(sql_str)        
        conn.commit()


cur.close()
conn.close()