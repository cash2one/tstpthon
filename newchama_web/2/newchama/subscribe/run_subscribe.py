#encoding:utf-8
import os,sys,datetime

sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/adminnewchama/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
import traceback
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from project.models import Project, Country, StatusProject
from subscribe.models import Subscribe, SubscribeKeyword, SubscribeSendRecord
from django.utils import simplejson
import logging
from django.db.models import Q
from newchama.helper import send_email_by_mq
from django.core.mail import send_mail, EmailMessage
from newchama.settings import EMAIL_HOST_USER, IS_PRODUCT_HOST, TEST_EMAIL
from django.template import loader
from repository import custom_crypto
import logging
from project.views import handle_dynamic_email_module

logger = logging.getLogger(__name__)

# logging.basicConfig(level=logging.ERROR,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename='subscribe_error.log',
#                 filemode='a')

ch = logging.StreamHandler()
fh = logging.FileHandler('subscribe_error.log')
logger.addHandler(ch)
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s') #logging.Formatter(%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.setLevel(logging.INFO)


def run_subscribe():
    #_sql = "select * from project_subscribe where is_delete = 0 and tip_interval > 0 and DATE_FORMAT(now(), '%%Y%%m%%d') = DATE_FORMAT(DATE_ADD(last_send_time, INTERVAL tip_interval DAY), '%%Y%%m%%d') order by id desc"
    #_sql = "select * from project_subscribe where is_delete = 0 and is_push = 1 and DATE_FORMAT(now(), '%%Y%%m%%d') = DATE_FORMAT(DATE_ADD(last_send_time, INTERVAL tip_interval DAY), '%%Y%%m%%d') order by id desc"
    _sql = "select * from newchama.project_subscribe where is_delete = 0 and is_push = 1 order by id desc"
    sl = Subscribe.objects.raw(_sql)
    if sl:
        for s in sl:
            project = find_match_project(s)
            srs = SubscribeSendRecord.objects.filter(subscribe_id=s.id)
            projectIds = []
            if srs:
                for sr in srs:
                    projectIds.append(sr.project_id)
            project = project.exclude(id__in=projectIds).order_by("-id")[:1]
            ssr = SubscribeSendRecord()
            if project:
                for p in project:
                    ssr.project_id = p.id
                    ssr.subscribe_id = s.id
                    ssr.save()
                    #send mail
                    send_subscribe_mail(p, s)
            s.last_send_time = datetime.datetime.now()
            s.save()


def find_match_project(s):
    project = Project.objects.filter(status=StatusProject.approved).all()
    sks = s.subscribe_keyword.all()
    if sks:
        condition2 = Q()
        for k in sks:
            condition2 = condition2 | Q (Q(name_cn__contains=k) | Q(name_en__contains=k))
        project = project.filter(condition2)
    if s.company_countries_id!= 0 and s.company_countries_id!= "" and s.company_countries_id!= "0" and s.company_countries_id:
        project = project.filter(Q(company_country__id=s.company_countries_id))
    if s.company_provinces_id != 0 and s.company_provinces_id != "" and s.company_provinces_id != "0" and s.company_provinces_id:
        project = project.filter(Q(company_province__id=s.company_provinces_id))
    if s.company_industries_id != 0 and s.company_industries_id != "" and s.company_industries_id is not None:
        project = project.filter(Q(company_industry_id=s.company_industries_id) | Q(company_industry__father_id=s.company_industries_id) | Q(company_industry__father__father_id=s.company_industries_id))
    if s.deal_size_min != -1 and s.deal_size_min != "" and s.deal_size_min != "0" and s.deal_size_min != 0 and s.deal_size_min:
        dealsize_min = int(s.deal_size_min) #* 1000000
        project = project.filter(deal_size__gte = s.deal_size_min)
    if s.deal_size_max != -1 and s.deal_size_max != "" and s.deal_size_max != "0" and s.deal_size_max != 0 and s.deal_size_max:
        dealsize_max = int(s.deal_size_max) #* 1000000
        project = project.filter(deal_size__lte = s.deal_size_max)
    if s.service_type != 0 and s.service_type != "" and s.service_type != "0" and s.service_type:
        project = project.filter(Q(service_type = s.service_type))
    if s.project_stage != 0 and s.project_stage != "" and s.project_stage != "0" and s.project_stage:
        project = project.filter(Q(project_stage = s.project_stage))
    if s.currency_type != 0 and s.currency_type != "" and s.currency_type != "0" and s.currency_type:
        project = project.filter(Q(pay_currency = s.currency_type))
    return project



def send_subscribe_mail(p, subscribe):
    try:
        email = subscribe.member.email
        mail_dic = dict()
        mail_dic['p'] = p
        mail_dic['username'] = subscribe.member.first_name
        mail_dic['publisher_name'] = p.member.first_name
        mail_dic['subscribe_name'] = subscribe.name_cn
        handle_dynamic_email_module(mail_dic, p)

        key = "global subscribe"
        assert isinstance(subscribe.id, object)
        member_info = str(subscribe.member.id) + "," + subscribe.member.email + "," + str(subscribe.id)
        encrypt_result = custom_crypto.encrypt(key, member_info)

        mail_dic['disable_push_link'] = _get_disable_push_link(encrypt_result)

        html_content = loader.render_to_string("subscribe/email_send_subscribe.html", mail_dic)
        title = u'订阅项目推荐'
        logger.info("sending email " + email)
        if not IS_PRODUCT_HOST:
            email = TEST_EMAIL
        # send_email_by_mq('email', 'email', title, email, html_content)
        msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
    except Exception, ex:
        logger.error(e.message, exc_info=True)


def _get_disable_push_link(encrypt_result):
    return 'http://www.newchama.com/subscribe/disable_push_confirm/' + encrypt_result

if __name__=="__main__":
    try:
        logger.info("---------------start subscribe ----------------------")
        run_subscribe()
        logger.info("---------------end subscribe search----------------------")
    except Exception,e:
        logger.error(e, exc_info=True)
