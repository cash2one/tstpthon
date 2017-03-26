#-*-encoding:utf-8-*-
import os,sys
sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('/var/www/newchama'))


import newchama.settings



_host=newchama.settings.DATABASES['default']['HOST']
_port=int(newchama.settings.DATABASES['default']['PORT'])
_user=newchama.settings.DATABASES['default']['USER']
_password=newchama.settings.DATABASES['default']['PASSWORD']
_dbname=newchama.settings.DATABASES['default']['NAME']

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")



from datetime import datetime
from services.models import Industry,Country,Province,City
import hashlib
from sqlalchemy import *
from sqlalchemy.orm import *

currency_to_usd={
u'万元':1/6.1306,
u'万加元':1/1.0961,
u'万台币':1/29.9790,
u'万新元':1/1.2635,
u'万新西兰元':0.8188,
u'万日元':1/106.8900,
u'万欧元':1.2911,
u'万港元':1/7.7497,
u'万澳元':0.9184,
u'万美元':1,
u'万英镑':1.6202,
u'万韩元':1/1036
}

AppKeyid='00004'
AppKey='D03D17C25A9A1F4B'

def buildRequestString(keyid,key,dic,pre_url):
    
    sort_list = sorted(dic.iteritems(), key=lambda d:d[0], reverse = False ) 
    code=''
    for item in sort_list: 
        code+=str(item[0])+str(item[1])

    request_str = ''
    for item in dic:
        request_str+=item+'='+str(dic[item])+'&'
   
    request_str += 'sysSign='+str.upper(hashlib.sha1(key+code+key).hexdigest())
    #print pre_url+request_str
    return pre_url+request_str

def convert_time(str_time):
    _date=None
    if str_time!="":
        try:
            _date=datetime.strptime(str_time, "%m/%d/%y %H:%M")
        except:
            try:
                _date=datetime.strptime(str_time, "%m/%d/%y")
            except:
                try:
                    _date=datetime.strptime(str_time, "%m/%d/%Y")
                except:
                    try:
                        _date=datetime.strptime(str_time, "%Y-%m-%d")
                    except:
                        try:
                            _date=datetime.strptime(str_time, "%y-%m-%d")
                        except:
                            try:
                                _date=datetime.strptime(str_time, "%Y")
                            except:
                                pass
    
    return _date

def get_cvid(cvstr,level):
    cv_id=None
    if cvstr !='':
        try:
            cv_id=Industry.objects.get(level=level,name_cn=cvstr).id
        except:
            pass
    return cv_id

def get_country_province_city(region_str):
    #获取地址id     

    city_id=None
    province_id=None
    country_id=None

    address_list=region_str.strip().split(">")
    address_list.reverse()

    for address in address_list:
        if address != "":
            try:
                _city=City.objects.get(name_cn=address)
                city_id=_city.id
                province_id=_city.province_id
                try:
                    _province=Province.objects.get(id=province_id)
                    country_id=_province.country_id
                except:
                    pass
            except:
                try:
                    _province=Province.objects.get(name_cn=address)
                    province_id=_province.id
                    country_id=_province.country_id
                except:
                    try:
                        _country=Country.objects.get(name_cn=address)
                        country_id=_country.id
                    except:
                        pass

    return country_id,province_id,city_id


def initDB(table_name,object_class):
    db_config = {'host': _host, 'port':_port, 'user': _user, 'passwd': _password, 'db':_dbname, 'charset':'utf8'}
    engine = create_engine('mysql://%s:%s@%s/%s?charset=%s'%(db_config['user'], db_config['passwd'], db_config['host'], db_config['db'], db_config['charset']), echo=False)
    metadata = MetaData(engine)
    _table = Table(table_name, metadata, autoload=True)
    mapper(object_class, _table)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(object_class)

    return session,query

