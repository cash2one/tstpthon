# -*- coding: utf-8 -*-  
import os,sys
sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

from services.models import ListedCompany,InvestmentCompany,Company,InvestmentHistory,CompanyInvestmentHistory,Country,Province,City,Industry



def saveItem(item):
    

    company=Company.objects.filter(name_cn=item.company.name_cn).first()
    now_company_num=CompanyInvestmentHistory.objects.filter(company=company,happen_date=item.happen_date,targetcompany_cn=item.targetcompany).count()

    if now_company_num ==0:
        _recode=CompanyInvestmentHistory()
        _recode.company=company

        if item.country_id:
            _recode.country=Country.objects.get(pk=item.country_id)
        if item.province_id:
            _recode.province=Province.objects.get(pk=item.province_id)
        if item.city_id:
            _recode.city=City.objects.get(pk=item.city_id)

        _recode.cv1 = item.cv1
        _recode.cv2 = item.cv2
        _recode.cv3 = item.cv3
        if _recode.amount:
            _recode.amount = item.amount*10000
        if _recode.currency:
            _recode.currency = item.currency.replace(u'万','')
            if _recode.currency==u'元':
                _recode.currency=u"人民币"

        _recode.person_cn = item.person
        _recode.person_en = item.person
        
        _recode.usd = item.usd
        _recode.targetcompany_cn = item.targetcompany
        _recode.targetcompany_en = item.targetcompany
     
        _recode.invest_stage=item.type
        _recode.content_cn=item.content
        _recode.content_en=item.content

        if item.cv3:
            _recode.industry=Industry.objects.get(pk=item.cv3)
        elif item.cv2:
            _recode.industry=Industry.objects.get(pk=item.cv2)
        elif item.cv1:
            _recode.industry=Industry.objects.get(pk=item.cv1)

        _recode.happen_date=item.happen_date


        _recode.save()

        


old_list=InvestmentHistory.objects.all().order_by('id')
idx=0
for item in old_list:
    idx+=1
    print '#%d %s'%(idx,item.company.name_cn)

    saveItem(item)



