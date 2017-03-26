# -*- coding: utf-8 -*-  
import os,sys
sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

from services.models import ListedCompany,InvestmentCompany,Company,CompanyStockSymbol



def saveCompanySymbol(item):
    _s_list=ListedCompany.objects.filter(name_cn=item.name_cn)
    for _s in _s_list:
        print _s.stock_symbol
        _t_num=CompanyStockSymbol.objects.filter(company=item,stock_symbol=_s.stock_symbol).count()
        if _t_num==0:
            _t=CompanyStockSymbol()
            _t.company=item
            _t.stock_exchange=_s.stock_exchange
            _t.stock_symbol=_s.stock_symbol
            _t.stock_symbol_no_pre=_s.stock_symbol_no_pre

            _t.save()

        


old_list=Company.objects.filter(type=1).order_by('id')[10000:]
idx=0
for item in old_list:
    idx+=1
    print '#%d %s'%(idx,item.name_cn)

    saveCompanySymbol(item)



