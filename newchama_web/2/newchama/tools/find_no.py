#encoding:utf-8
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

import csv
from member.models import CompanyInvestmentField,Company
from area.models import Country

f1=open('no.txt','a')

fname = "111.csv"
num=0
for row in csv.reader(open(fname,'rU'), delimiter=','):

    company_name = row[0].strip()
    company_num=Company.objects.filter(name_cn=company_name).count()
    
    if company_num==0:
        num+=1
        print num
        print company_name
        f1.write(company_name+'\n\r')

print num
f1.close()