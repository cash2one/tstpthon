#encoding:utf-8
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

from django.core.mail import send_mail, EmailMessage
from newchama.settings import EMAIL_HOST_USER
from member.models import Member
from django.template import loader, Context

import pika
import pickle
import logging

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='email.log',
                filemode='a')

host_name='test.newchama.com'

if IS_PRODUCT_HOST:
    host_name='www.newchama.com'
connection = pika.BlockingConnection(pika.ConnectionParameters(host_name))
channel = connection.channel()
 
channel.queue_declare(queue='email')

def sendmail(title,email,content):
   
    msg = EmailMessage(title, content, EMAIL_HOST_USER, [email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


def callback(ch, method, properties, body):
    try:
        c=pickle.loads(body)
        sendmail(c['title'],c['email'],c['content'])
        logging.info("[x] Send mail %r for %r" % (c['email'],c['title']))

    except Exception,e:
        logging.error(e)
        
 
channel.basic_consume(callback, queue='email', no_ack=True)
 
print ' [*] Waiting for messages. To exit press CTRL+C'


#产生子进程，而后父进程退出
pid = os.fork()
if pid > 0:
    sys.exit(0)
 
#修改子进程工作目录
os.chdir("/")
#创建新的会话，子进程成为会话的首进程
os.setsid()
#修改工作目录的umask
os.umask(0)
 
#创建孙子进程，而后子进程退出
pid = os.fork()
if pid > 0:
    sys.exit(0)
 
#重定向标准输入流、标准输出流、标准错误
sys.stdout.flush()
sys.stderr.flush()
si = file("/dev/null", 'r')
so = file("/dev/null", 'a+')
se = file("/dev/null", 'a+', 0)
os.dup2(si.fileno(), sys.stdin.fileno())
os.dup2(so.fileno(), sys.stdout.fileno())
os.dup2(se.fileno(), sys.stderr.fileno())


channel.start_consuming()


