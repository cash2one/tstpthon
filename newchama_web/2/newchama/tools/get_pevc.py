#encoding:utf-8
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

import csv
from member.models import Company


fname = "pevc1.csv"

for row in csv.reader(open(fname,'rU'), delimiter=','):

    print row[0]
    print row[5]


    _investment_type=0

    if row[5]=='VC/':
        _investment_type=1

    if row[5]=='PE/':
        _investment_type=2

    if row[5]=='VC/PE/':
        _investment_type=3

    if row[5]=='战略投资者/':
        _investment_type=4
    
    try:
        company_num = Company.objects.filter(name_cn=row[0]).count()
        if company_num>0:
            company = Company.objects.filter(name_cn=row[0]).first()

            company.investment_type=_investment_type
            company.save()

    except Exception, e:
        print e
