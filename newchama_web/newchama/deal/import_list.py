#-*-encoding:utf-8-*-
import os,sys
sys.path.append(os.path.abspath('..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
#from django.conf import settings
#settings.configure()


from datetime import datetime
from services.models import ListDeal,DEAL_TYPES
import csv
from decimal import Decimal
from tools.lib.helper import currency_to_usd,convert_time,get_cvid,get_country_province_city


def  saveListItem(item):
    old_buy_record=ListDeal.objects.filter(happen_date=item.happen_date,target_company=item.target_company)
    if len(old_buy_record) == 0:
        item.save()
        
        print('%s saved!' % (item))
    else:
        print('%s is existed!' % (item))


def buildListItemFromRow(row):

    _item=ListDeal()
    _item.happen_date=convert_time(row[0])
    _item.list_type=row[1].decode('utf-8')
    _item.target_company=row[2].decode('utf-8')
    _item.title=u"%s%s"%(_item.target_company,_item.list_type)
    _item.deal_type=0

    _item.country_id,_item.province_id,_item.city_id=get_country_province_city(row[13])

    _item.cv1=get_cvid(row[3],1)
    _item.cv2=get_cvid(row[4],2)
    _item.cv3=get_cvid(row[5],3)

    if row[16]!='':
        _item.amount_usd=float(row[16].replace(',',''))*1000000
    if row[11]!='':
        _item.amount=Decimal(row[11].replace(',',''))
    if row[17]!='':
        _item.equity=float(row[17])
    if row[18]!='':
        _item.market_value=float(row[18].replace(',',''))*1000000

    _item.update_time=convert_time(row[22])
    _item.add_time=datetime.now()

    _item.stock_code=row[12]
    _item.stock_exchange=row[14]
    _item.list_time=convert_time(row[0])
    
    _item.list_status=row[15]
    _item.advisor_firm=row[19]
    _item.acc_firm=row[20]
    _item.law_firm=row[21]


    return _item




if __name__=="__main__":
    m=0
    _file="../tools/data/cvsource_list.csv"
    for row in csv.reader(open(_file,'rU'),delimiter=','):
        _record=buildListItemFromRow(row)
        m+=1
        print '#%d'%(m)
        saveListItem(_record)

    
    
        




