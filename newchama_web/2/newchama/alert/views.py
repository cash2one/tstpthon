from django.shortcuts import render
from django.core import serializers
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
import commands
import json

def index(request):
    outstr = commands.getstatusoutput('rabbitmqctl list_queues')
    data={}
    print outstr[0]
    if outstr[0]==0:

        _list=[]
        out=outstr[1].split('\n')
        if len(out)>2:
            out2=out[1:-1]
            for item in out2:
                c={}
                item_list=item.split('\t')
                c[item_list[0]]=item_list[1]
                _list.append(c)
        data['ok']='1'
        data['messages']=_list

        
    else:
        
        data['ok']='0'
        data['messages']=outstr[1]
    return HttpResponse(json.dumps(data), mimetype='javascript/json')
    