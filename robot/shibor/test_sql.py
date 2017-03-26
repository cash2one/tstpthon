from sqlalchemy import *
from sqlalchemy.orm import *
import pymysql

class ShiborItem(object):
    pass


db_config = {'host': 'newchama.mysql.rds.aliyuncs.com', 'port':3306, 'user': 'newchama', 'passwd': 'newchama1234', 'db':'newchama', 'charset':'utf8'}

engine = create_engine('mysql://%s:%s@%s/%s?charset=%s'%(db_config['user'], db_config['passwd'], db_config['host'], db_config['db'], db_config['charset']), echo=True)

metadata = MetaData(engine)

shibor_table = Table('repository_shibor', metadata, autoload=True)
print shibor_table.columns

mapper(ShiborItem, shibor_table)
Session = sessionmaker(bind=engine)
session = Session()
query = session.query(ShiborItem)

c = query.filter_by(id='2').first()
if c:
    print c.date
else:
    print '%%%%%%'