#encoding:utf-8
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
import pika
import pickle
from django.template import loader, Context


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
 
channel.queue_declare(queue='email')

email="richard@newchama.com"

mail_dic = dict()
mail_dic['email'] = email
mail_dic['name'] = 'richard'
html_content = loader.render_to_string('tools/update_mail.html', mail_dic)


c={}

c['title']=u'NewChama用户通知'
c['email']=email
c['content']=html_content
channel.basic_publish(exchange='', routing_key='email', body=pickle.dumps(c))
print " [x] Sent 'Hello World!'"
connection.close()