# -*- coding: utf-8 -*-  
import os,sys,gc
sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

from services.models import ListedCompany,InvestmentCompany,Company



def saveCompanyFromListedCompany(item):
    if item.name_cn!="" or item.name_en!="":

        if item.name_cn!="":
            now_company_num=Company.objects.filter(name_cn=item.name_cn).count()
            _company_name=item.name_cn
        elif item.name_en!="":
            now_company_num=Company.objects.filter(name_en=item.name_en).count()
            _company_name=item.name_en
        
        if now_company_num ==0:
            _company=Company()
            _company.name_cn = _company_name
            _company.name_en = item.name_en
            _company.short_name_cn = item.short_name_cn
            _company.short_name_en = item.short_name_en
            _company.intro_cn = item.intro_cn
            _company.intro_en = item.intro_en
            _company.country = item.country
            _company.province = item.province
            _company.city = item.city
            _company.industry = item.industry
            _company.address_cn = item.address_cn
            _company.address_en = item.address_en
            _company.website = item.website
            _company.tel = item.tel
            _company.fax = item.fax        
            _company.postcode = item.postcode
            _company.type = 1
            _company.status = 0
            _company.found_time = item.found_time
            _company.data_source = "Xueqiu"
            _company.memo = item.memo

            _company.save()
            del _company
            gc.collect()
        


old_list=ListedCompany.objects.all().order_by('id')
idx=0
for item in old_list:
    idx+=1
    print '#%d %s'%(idx,item.name_cn)

    saveCompanyFromListedCompany(item)



