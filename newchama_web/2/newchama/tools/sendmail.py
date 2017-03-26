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

def sendmail(email,name,template_name):
    mail_dic = dict()
    mail_dic['email'] = email
    mail_dic['name'] = name

    html_content = loader.render_to_string(template_name, mail_dic)
    msg = EmailMessage(u'NewChama用户通知', html_content, EMAIL_HOST_USER, [email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()

member_list=Member.objects.filter(status=1)

for item in member_list:
    print item.first_name + item.last_name
    print item.email
    try:
        sendmail(item.email,item.first_name + item.last_name,'tools/update_mail.html')
    except Exception, e:
        print e
