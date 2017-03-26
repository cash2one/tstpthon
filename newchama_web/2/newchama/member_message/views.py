from django.shortcuts import render

# Create your views here.
from member_message.models import Message_Log
import datetime


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
        if ms_log.item_type == 1:
            ms_log.item_id = message.project_id
        elif ms_log.item_type == 2:
            ms_log.item_id = message.demand_id
        ms_log.save()