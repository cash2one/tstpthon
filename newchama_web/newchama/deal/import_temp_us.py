#-*-encoding:utf-8-*-
import os,sys
sys.path.append(os.path.abspath('..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
#from django.conf import settings
#settings.configure()


from datetime import datetime
from services.models import TempUsDeal
import csv
from decimal import Decimal
from tools.lib.helper import currency_to_usd,convert_time,get_cvid,get_country_province_city


def  saveListItem(item):
    old_record=TempUsDeal.objects.filter(industry_id=item.industry_id,deal_type=item.deal_type,chart_type=item.chart_type)
    if len(old_record) == 0:
        item.save()
        
        print('saved!')
    else:
        print('is existed!')


def buildListItemFromRow(row):

    _item=TempUsDeal()


    _temp = row[0].split('-')

    _item.industry_id=int(_temp[0])
    _item.deal_type=int(_temp[1])
    _item.chart_type=int(_temp[2])

    _item.amount_usd=float(row[1])

    return _item




if __name__=="__main__":
    m=0
    _file="../tools/data/temp_us.csv"
    for row in csv.reader(open(_file,'rU'),delimiter=','):
        _record=buildListItemFromRow(row)
        m+=1
        print '#%d'%(m)
        saveListItem(_record)

    
    
        




