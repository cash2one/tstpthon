#encoding:utf-8
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")


from newchama.settings import EMAIL_HOST_USER
from member.models import Member


f=open('user_list.txt')

for item in f:
    print item.strip()
    try:
        member = Member.objects.get(email=item.strip())
        member.make_password('newchama111111')
        member.save()
        print member

    except Exception, e:
        print e


