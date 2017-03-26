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

    print row[0]
    print row[1]
    print row[2]
    try:
        item=CompanyInvestmentField()
        item.company_id=int(row[1])
        item.tags=row[2].replace('，',',').replace('、',',').replace('；',',')
        item.deal_type=int(row[3])
        item.deal_currency=int(row[4])
        item.deal_size_min=int(row[5])
        item.deal_size_max=int(row[6])

        item.revenue=int(row[8])
        item.net_income=int(row[9])
        item.ebita=int(row[10])
        item.country_id=int(row[11])
        item.deal_size=int(row[12])
        item.growth=int(row[13])
        item.hot=int(row[14])

        item.save()

    except Exception, e:
        print e
