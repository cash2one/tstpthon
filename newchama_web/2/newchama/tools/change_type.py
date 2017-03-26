#encoding:utf-8
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

from member.models import Company


company_list=Company.objects.all();


for company in company_list:
    print company.name_cn
    if company.type==1:
        company.is_list=True
        company.new_type=6

    if company.capital_type==1:
        company.new_type=7

    if company.capital_type==2:
        company.new_type=8

    if company.capital_type==3:
        company.new_type=9

    company.save()


