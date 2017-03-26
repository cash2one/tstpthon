#-*-encoding:utf-8-*-
import os,sys
sys.path.append(os.path.abspath('..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
#from django.conf import settings
#settings.configure()


from datetime import datetime
from services.models import BuyTogetherDeal
import csv
from decimal import Decimal
from tools.lib.helper import currency_to_usd,convert_time,get_cvid,get_country_province_city


def  saveTransItem(item):
    old_buy_record=BuyTogetherDeal.objects.filter(happen_date=item.happen_date,target_company=item.target_company)
    if len(old_buy_record) == 0:
        item.save()
        
        print('%s saved!' % (item))
    else:
        print('%s is existed!' % (item))


def buildTransItemFromRow(row):

    _item=BuyTogetherDeal()
    _item.deal_type=2
    _item.title=row[0].decode('utf-8')
    _item.content=row[22].decode('utf-8')

    _item.happen_date=convert_time(row[1])
    _item.end_time=convert_time(row[2])
    _item.target_company=row[3]
    _item.cv1=get_cvid(row[4],1)
    _item.cv2=get_cvid(row[5],2)
    _item.cv3=get_cvid(row[6],3)

    _item.buy_type=row[18]
    _item.dstrict=row[19]
    _item.state=row[20]
    _item.buy_way=row[21]
    _item.attitude_name=row[23]
    _item.whether_trade=row[24]
    _item.pay_style=row[25]

    _item.country_id,_item.province_id,_item.city_id=get_country_province_city(row[26])

    _item.buy_company=row[27].decode('utf-8')
    _item.sale_company=row[28].decode('utf-8')

    _item.currency=row[30]

    if row[29]!='':
        _item.amount=Decimal(row[29].replace(',',''))

    if row[31]!='':
        _item.amount_usd=float(row[31].replace(',',''))*1000000

  

    if row[32]!='':
        _item.equity=float(row[32])

    if row[33]!='':
        _item.market_value=float(row[33].replace(',',''))*1000000

    _item.update_time=convert_time(row[34])
    _item.add_time=datetime.now()


    if row[35]!='':
        _item.sales_income=float(row[35].replace(',',''))*10000

    if row[36]!='':
        _item.total_assets=float(row[36].replace(',',''))*10000

    if row[37]!='':
        _item.net_assets=float(row[37].replace(',',''))*10000

    if row[38]!='':
        _item.net_margin=float(row[38].replace(',',''))*10000


    if row[39]!='':
        _item.pe=float(row[39])

    if row[40]!='':
        _item.ps=float(row[40])

    if row[41]!='':
        _item.pb=float(row[41])

    if row[42]!='':
        _item.before_equity=float(row[42].replace('%','').replace(',','').replace('·','').replace(' ',''))

    if row[43]!='':
        _item.after_equity=float(row[43].replace('%','').replace(',','').replace('·','').replace(' ',''))

    _item.buy_company_intro=row[45]
    _item.sale_company_intro=row[44]


    return _item




if __name__=="__main__":
    m=0
    start_idx=42450
    _file="../tools/data/cvsource_buy.csv"
    for row in csv.reader(open(_file,'rU'),delimiter=','):
        m+=1
        if m<start_idx:
            continue
        _record=buildTransItemFromRow(row)
        
        print '#%d'%(m),_record
        saveTransItem(_record)

    
    
        




