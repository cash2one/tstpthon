#-*-encoding:utf-8-*-
import os,sys
sys.path.append(os.path.abspath('..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
#from django.conf import settings
#settings.configure()


from datetime import datetime
from services.models import TransDeal,DEAL_TYPES
import csv
from decimal import Decimal
from tools.lib.helper import currency_to_usd,convert_time,get_cvid,get_country_province_city


def  saveTransItem(item):
    old_buy_record=TransDeal.objects.filter(happen_date=item.happen_date,target_company=item.target_company)
    if len(old_buy_record) == 0:
        item.save()
        
        print('%s saved!' % (item))
    else:
        print('%s is exit!' % (item))


def buildTransItemFromRow(row):

    _item=TransDeal()
    _item.deal_type=1
    _item.title=row[0].decode('utf-8')
    _item.content=row[1].decode('utf-8')
    _item.happen_date=convert_time(row[2])
    _item.target_company=row[4]
    _item.cv1=get_cvid(row[5],1)
    _item.cv2=get_cvid(row[6],2)
    _item.cv3=get_cvid(row[7],3)

    _item.currency=row[13]

    if row[12]!='':
        _item.amount=Decimal(row[12].replace(',',''))

    if row[17]!='':
        _item.amount_usd=float(row[17].replace(',',''))*1000000

    _item.country_id,_item.province_id,_item.city_id=get_country_province_city(row[14])

    _item.invest_company=row[15]
    _item.invest_stage=row[16]
    _item.invest_type=row[3]

    if row[18]!='':
        _item.equity=float(row[18])

    if row[19]!='':
        _item.market_value=float(row[19].replace(',',''))*1000000

    _item.update_time=convert_time(row[21])
    _item.add_time=datetime.now()
    _item.finance_advisor=row[20]


    return _item




if __name__=="__main__":
    m=0
    start_idx=0
    _file="../tools/data/cvsource_trans.csv"
    for row in csv.reader(open(_file,'rU'),delimiter=','):
        m+=1
        if m<start_idx:
            continue
        _record=buildTransItemFromRow(row)
        
        print '#%d'%(m)
        saveTransItem(_record)

    
    
        




