#encoding:utf-8
import os,sys,datetime
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/adminnewchama/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
import traceback
from member_message.models import Message, Message_Log
import logging

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='subscribe_error.log',
                filemode='a')


def init_message_log():
    Message_Log.objects.filter().delete()
    _sql = "select max(id) id,sender_id, receiver_id, project_id  from member_message where project_id is not null group by sender_id, receiver_id, project_id order by id desc"
    _message_list = Message.objects.raw(_sql)
    for m in _message_list:
        newst_message = Message.objects.get(pk=m.id)
        update_message_log(newst_message)

    _sql = "select max(id) id,sender_id, receiver_id, demand_id  from member_message where demand_id is not null group by sender_id, receiver_id, demand_id order by id desc"
    _message_list = Message.objects.raw(_sql)
    for m in _message_list:
        newst_message = Message.objects.get(pk=m.id)
        update_message_log(newst_message)


def update_message_log(message):
    ms_logs = Message_Log.objects.filter(sender=message.sender, receiver=message.receiver, item_type=message.type_relation).order_by("-id")
    if message.type_relation == 1:
        ms_logs = ms_logs.filter(item_id=message.project_id)
    elif message.type_relation == 2:
        ms_logs = ms_logs.filter(item_id=message.demand_id)
    if len(ms_logs) > 0:
        ms_log = ms_logs[0]
        ms_log.message = message
        ms_log.update_time = datetime.datetime.now()
        ms_log.save()
    else:
        ms_log = Message_Log()
        ms_log.sender = message.sender
        ms_log.receiver = message.receiver
        ms_log.message = message
        ms_log.item_type = message.type_relation
        ms_log.update_time = message.add_time
        if ms_log.item_type == 1:
            ms_log.item_id = message.project_id
        elif ms_log.item_type == 2:
            ms_log.item_id = message.demand_id
        ms_log.save()


if __name__=="__main__":
    try:
        print "---------------start auto subscribe search----------------------"
        init_message_log()
        print "---------------end auto subscribe search----------------------"
    except Exception,e:
        traceback.print_exc()
        logging.error(e)