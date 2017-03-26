#encoding:utf-8
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
from member_message.models import Message

import datetime
from prettytable import PrettyTable  


_list=Message.objects.order_by('-add_time')
table = PrettyTable(["时间", "发送人","接受人","项目类型","项目名称"])  

for item in _list:
    sender_name= item.sender.first_name+item.sender.last_name
    receiver_name = item.receiver.first_name+item.receiver.last_name
    project_name=''
    if item.type_relation == 1:
        project_name =item.project.name_cn

    if item.type_relation == 2:
        project_name =item.demand.name_cn

    table.add_row([item.add_time.strftime("%Y-%m-%d %H:%M:%S"),sender_name,receiver_name,item.get_type_relation_display(),project_name[0:20]])  


table.sort_key("日期")  
table.reversesort = True  
print '用户消息表'
print table
