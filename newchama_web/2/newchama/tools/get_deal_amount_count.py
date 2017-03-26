#encoding:utf-8
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

from analysis.models import AnalysisUserTotal,AnalysisUser,AnalysisProject
import datetime
from prettytable import PrettyTable  
from colorama import Fore

num=30

_list=AnalysisUserTotal.objects.order_by('-time')[0:num]
table = PrettyTable([Fore.RED+"日期", "用户总数","项目数","需求数","上市公司用户数","非上市公司用户数","PE/VC用户数","FA用户数"+Fore.GREEN])  

for item in _list:
     
    table.add_row([item.time.strftime("%Y-%m-%d"), item.user_num,item.project_num,item.demand_num,item.listed_user_num,item.unlisted_user_num,item.vc_user_num,item.fa_user_num])  


table.sort_key("日期")  
table.reversesort = True  
print '用户总表'
print table
