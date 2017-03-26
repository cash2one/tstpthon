#encoding:utf-8
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

import csv
from member.models import CompanyInvestmentField,Company
from area.models import Country

fname = "111.csv"

for row in csv.reader(open(fname,'rU'), delimiter=','):

    cif=CompanyInvestmentField()
    company_name = row[0].strip()
    company_num=Company.objects.filter(name_cn=company_name).count()
    
    if company_num>0:
        company=Company.objects.filter(name_cn=company_name).first()
        cif.company=company

        is_num=0

        tags = row[1].strip().replace('，',',').replace('、',',').replace('；',',').replace('不明','')
        tags2 = row[2].strip().replace('，',',').replace('、',',').replace('；',',').replace('不明','')

        
        
        if tags !='' and tags != '不明':
            if tags2 !='' and tags2 != '不明':
                tags =tags +','+tags2

            tags_list=tags.split(',')
            cif.tags = ','.join(set(tags_list))
            is_num+=1


        deal_type = row[3].strip()

        if deal_type=='融资或并购皆可':
            cif.deal_type=4
            is_num+=1

        if deal_type=='控股权收购':
            cif.deal_type=1
            is_num+=1

        deal_currency = row[5].strip()

        if deal_currency=='RMB':
            cif.deal_currency=1
            is_num+=1

        country = row[11].strip()

        if country=='中国':
            cif.country=Country.objects.get(id=84)
            is_num+=1

        if is_num >0:
            print company_name
            cif.save()

