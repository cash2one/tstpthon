#-*-encoding:utf-8-*-
import pika
import pickle
from newchama.settings import EMAIL_HOST_USER,IS_PRODUCT_HOST
from newchama import settings
import logging
import re
from services.models import OtherLogin

logger = logging.getLogger(__name__)

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.http import urlquote

def member_login_required(func):
    def check_login(request,*args,**nargs):
        if(request.session.get('member', None)==None):
            
            return redirect(reverse('account.login')+'?back_url='+urlquote(request.get_full_path()))
        return func(request,*args,**nargs)
    return check_login


def buildMemberForFront(request,current_member,role):
    member={}
    member["id"]=current_member.id
    member["email"]=current_member.email
    member["username"]=current_member.first_name
    member["company_type"]=current_member.company.type
    member["company_id"]=current_member.company.id
    if request.is_cn:
        member["company_name"]=current_member.company.short_name_cn
    else:
        member["company_name"]=current_member.company.short_name_en
    
    print(current_member.avatar)

    if current_member.avatar:
        member["avatars"]=unicode(current_member.avatar)
    else:
        member["avatars"]="avatar-1-md.jpg"

    member["role"]=role

    return member


def saveOtherLogin(access_token, id, expires_in, type):
    ol = {}
    ol["access_token"] = access_token
    ol["id"] = id
    ol['expires_in'] = expires_in
    return ol


def checkOtherLogin(otherLogin):
    access_token = otherLogin['access_token']
    oid = otherLogin['id']
    expires_in = otherLogin['expires_in']
    ol = OtherLogin.objects.get(pk=oid, access_token=access_token, expires_in=expires_in)
    return ol


def send_email_by_mq(queue,routing_key,title,email,html_content):
    if IS_PRODUCT_HOST:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    else:
        connection = pika.BlockingConnection(pika.ConnectionParameters('test.newchama.com'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    c={}
    c['title']=str(title)
    c['email']=email
    c['content']=html_content
    channel.basic_publish(exchange='', routing_key=routing_key, body=pickle.dumps(c))
    channel.close()
    connection.close()


def send_email_by_mq_multiple(queue,routing_key,title,email_list,html_content_list):
    if IS_PRODUCT_HOST:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    else:
        connection = pika.BlockingConnection(pika.ConnectionParameters('test.newchama.com'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    for item in zip(email_list,html_content_list):

        c={}
        c['title']=str(title)
        c['email']=item[0]
        c['content']=item[1]

        channel.basic_publish(exchange='', routing_key=routing_key, body=pickle.dumps(c))
        #Terry logo todo
    channel.close()
    connection.close()

class IgnoreCrsfMiddleware(object):
     def process_request(self, request, **karg):
         URL_LIST = [r'^/a/b/$', r'^/c/d/$']
         for u in URL_LIST:
             if re.match(u, request.path):
                 request.csrf_processing_done = True
                 return None

