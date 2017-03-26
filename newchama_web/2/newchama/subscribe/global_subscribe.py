#encoding:utf-8
from collections import namedtuple
import os, sys, datetime

sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/adminnewchama/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
import traceback
from django.template.loader import get_template
from project.models import Project, StatusProject
from member.models import Member, MemberInvestmentField, GlobalRecommendProjectLog
from django.db.models import Q
from newchama.helper import send_email_by_mq
from django.core.mail import send_mail, EmailMessage
from newchama.settings import EMAIL_HOST_USER, IS_PRODUCT_HOST, TEST_EMAIL
from django.template import loader
from repository import custom_crypto
from project.views import handle_dynamic_email_module
import logging

logger = logging.getLogger(__name__)

# logging.basicConfig(level=logging.INFO,
#                 # format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 # filename='global_subscribe_error.log',
#                 filemode='a')

ch = logging.StreamHandler()
fh = logging.FileHandler('global_subscribe_error.log')
logger.addHandler(ch)
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s') #logging.Formatter(%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.setLevel(logging.INFO)

def run_subscribe():
    #select user and user,s match_table and get industry, keyword and tags
    start_time = datetime.date.today() + datetime.timedelta(hours=-624)
    end_time = datetime.date.today()
    projects = Project.objects.filter(add_time__range=(start_time, end_time), status=2)
    if len(projects) == 0:
        return
    new_projects = []
    new_project = namedtuple("new_project", ["project", "project_tags", "project_industries"])
    for project in projects:
        project_industries, project_tags = find_project_tags(project)
        new_projects.append(new_project(project, project_tags, project_industries))

    members = Member.objects.filter(status=1, is_subscribe_push=True).order_by("first_name").exclude(company_id__in=[27, 24933, 24765])
    for member in members:
        member_industries, member_tags = find_member_tags(member)
        member_already_recommend_projects = find_member_already_send(member)
        if member_tags is None:
            continue
        for newp in new_projects:
            project = newp.project
            if project.member == member or project in member_already_recommend_projects:
                continue
            project_tags = newp.project_tags
            project_industries = newp.project_industries
            match_result = False
            if len(member_industries) > 0 and len(project_industries) > 0:
                industry_include = False                       #is industry in project_industry
                for project_industry in project_industries:
                    if project_industry in member_industries:
                        logger.debug("count user " + str(member.id) + " " + member.first_name + " member_industries = " + str(member_industries) + " member_tags = " + str(member_tags))
                        logger.debug("matching industry success project_industry = " + project_industry + " project_industries has "  + str(project_tags))
                        industry_include = True
                        break
                if industry_include and len(member_tags) > 0 and len(project_tags) > 0:
                    for project_tag in project_tags:
                        if project_tag in member_tags:
                            match_result = True
                            break
            if match_result:
                send_subscribe_mail(project, member)
                break


def find_member_tags(member):
    matchings = member.member_match_table.all()
    keywords = member.member_focus_keyword.all()
    industries = member.focus_aspect.all()
    if len(matchings) == 0 and len(keywords) == 0 and len(industries) == 0:
        return None, None
    member_tags = ''
    if len(matchings) > 0:
        for matching in matchings:
            member_tags += matching.tags.strip() + ","
    if len(keywords) > 0:
        for keyword in keywords:
            member_tags += keyword.keyword.strip() + ","
    if len(member_tags) > 0:
        member_tags = member_tags[:-1]

    member_industries = ''
    if len(industries) > 0:
        for industry in industries:
            member_industries += industry.name_cn.strip() + ","
        member_industries = member_industries[:-1]

    industries = []
    if len(member_industries) > 0:
        industries = set(member_industries.split(","))
    tags = []
    if len(member_tags) > 0:
        tags = set(member_tags.split(","))
    return industries, tags


def find_member_already_send(member):
    recommends = member.member_global_recommend_project.all()
    projects = []
    if len(recommends) == 0:
        return projects

    for recommend in recommends:
        projects.append(recommend.project)
    return projects


def find_project_tags(project):
    keywords = project.project_keyword.all()
    project_tags = ''
    if len(keywords) > 0:
        for keyword in keywords:
            project_tags += keyword.keyword.strip() + ","
        project_tags = project_tags[:-1]

    project_industries = ''
    industry = project.company_industry
    if industry:
        project_industries += industry.name_cn
        if industry.level == 2:
            project_industries += "," + industry.father.name_cn

    industries = []
    if len(project_industries) > 0:
        industries = set(project_industries.split(","))
    tags = []
    if len(project_tags) > 0:
        tags = set(project_tags.split(","))
    return industries, tags


def send_subscribe_mail(p, member):
    logger.debug("---------------------------match result " + p.name_cn + " member id = " + member.first_name)
    recommend = GlobalRecommendProjectLog()
    recommend.member_id = member.id
    recommend.project_id = p.id
    recommend.email = member.email
    recommend.save()
    try:
        email = member.email
        mail_dic = dict()
        mail_dic['p'] = p
        mail_dic['username'] = member.first_name
        mail_dic['publisher_name'] = p.member.first_name
        mail_dic['subscribe_name'] = p.name_cn
        handle_dynamic_email_module(mail_dic, p)

        key = "global subscribe"
        member_info = str(member.id) + "," + member.email
        encrypt_result = custom_crypto.encrypt(key, member_info)
        mail_dic['disable_push_link'] = _get_disable_push_link(encrypt_result)

        html_content = loader.render_to_string("subscribe/email_send_global_subscribe.html", mail_dic)
        title = u'Newchama项目推荐'
        logger.info("sending email " + email)
        if not IS_PRODUCT_HOST:
            email = TEST_EMAIL
        send_email_by_mq('email', 'email', title, email, html_content)
        # msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [email])
        # msg.content_subtype = "html"  # Main content is now text/html
        # msg.send()
    except Exception, e:
        logger.error(e.message, exc_info=True)


def _get_disable_push_link(encrypt_result):
    return 'http://www.newchama.com/account/disable_push_confirm/' + encrypt_result

if __name__=="__main__":
    try:
        logger.info("---------------start global subscribe----------------------")
        run_subscribe()
        logger.info("---------------end global subscribe----------------------")
    except Exception, e:
        logger.error(e.message, exc_info=True)
