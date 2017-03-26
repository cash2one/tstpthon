#-*-encoding:utf-8-*-
from django.http import Http404
from django.shortcuts import render,render_to_response, redirect, get_object_or_404, HttpResponse
from django.core.context_processors import csrf
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.urlresolvers import reverse
from services.models import Member, StatusMember, InviteCode, EntryForm, FindPasswordHistory, InvestmentCompany, InvestmentHistory, ListedCompany, LoginType, \
    Message_Log, MemberFocusKeyword
from services.models import Country, Industry, Province, Company, Message, City, Project, Demand, StatusProject, StatusDemand, News
from services.models import IndustryWithPE,Preference, PreferenceIndustry, PreferenceKeyword, PreferenceLocation, Favorites, Deal, TypeFavorite
from services.models import DTOTimeline
from services.helper import Helper
from newchama.helper import member_login_required, buildMemberForFront,send_email_by_mq, checkOtherLogin
from newchama.settings import EMAIL_HOST_USER,MEDIA_ROOT
from django.utils import simplejson
from django.core import serializers
from log.views import write_login_log,write_company_view_recommond_man_log,write_company_view_recommond_machine_log
import os, random
import cStringIO
from django.template import loader
from newchama import settings
import datetime
import hashlib
import random
from django.core.mail import send_mail,EmailMessage
from django.db.models import Q, Count,Sum
import uuid
import logging
from sales.views import preferenceByMemberId as preference_project
from sales.views import countProjectStuffTotal as stuff_project
from sales.views import projectByMemberId as my_project
from purchase.views import preferenceByMemberId as preference_demand
from purchase.views import demandByMemberId as my_demand
from purchase.views import countDemandStuffTotal as stuff_demand
from log.views import save_dynamic
from hashlib import md5
from PIL import Image,ImageDraw, ImageFont  
from django.db.models import Q
from log.views import *
import time
from services.templatetags.myTags import caculate
logger = logging.getLogger(__name__)


@member_login_required
def index(request):
    c={}
    list1 = Member.objects.all()
    c["list"] = list1
    member = request.session.get('member', None)
    member_id = member['id']

    sp = stuff_project(member_id)
    sd = stuff_demand(member_id)
    count_all_relation_stuff = {}
    pvs = 0
    if sp["pvs"]:
        pvs = pvs + int(sp["pvs"])
    if sd["pvs"]:
        pvs = pvs + int(sd["pvs"])
    count_all_relation_stuff["pvs"] = pvs
    # mgs = int(sp["messages"]) + int(sd["messages"])
    mgs = Helper.find_not_read_message(member_id)
    favorites = int(sp["favorites"]) + int(sd["favorites"])
    recommend_companies = int(sp["recommend_companies"]) + int(sd["recommend_companies"])
    recommend_industries = int(sp["recommend_industries"]) +  int(sd["recommend_industries"])
    count_all_relation_stuff["messages"] = mgs
    count_all_relation_stuff["favorites"] = favorites
    count_all_relation_stuff["recommend_companies"] = recommend_companies
    count_all_relation_stuff["recommend_industries"] = recommend_industries
    c["count_all_relation_stuff"] = count_all_relation_stuff

    c['p_list'] = Favorites.objects.filter(type_relation=TypeFavorite.project, project__status=StatusProject.approved, member_id=member_id).order_by("-id")[0 : 5]
    c['d_list'] = Favorites.objects.filter(type_relation=TypeFavorite.demand, demand__status=StatusDemand.approved, member_id=member_id).order_by("-id")[0 : 5]
    preferenceKeywords = PreferenceKeyword.objects.filter(preference__member__id=member_id, preference__title="news")#Preference().TITLE_PREFERENCE["news"]
    if len(preferenceKeywords) > 0:
        tags = []
        for k in preferenceKeywords:
            tags.append(k.keyword)
        news_list_preference = News.objects.filter(tag__in=tags).order_by('-add_time')[0 : 5]
        c['news_list_preference'] = news_list_preference

    c['member'] = member
    active_company = Member.objects.filter().order_by("-last_login_time").values("company").distinct()[0: 8]
    company_ids = []
    if active_company:
        for m in active_company:
            print str(m)
            company_ids.append(m["company"])
    c['companies_active'] = Company.objects.filter(id__in=company_ids).exclude(id=27)
    c['hot_projects'] = Project.objects.filter(status=StatusProject.approved).order_by("-pv")[0:10]
    #can be change to by time
    c['timelines'] = handleDynamic(member_id, 1, 5)
    m = Member.objects.get(pk=member_id)
    write_view_index_log(request, m, 'view_index')
    return render_to_response("account/"+request.lang+"/index.html", c, context_instance=RequestContext(request))


@member_login_required
def json_dynamic(request):
    c={}
    page = request.GET.get('page', 1)
    pagesize = request.GET.get('pagesize', 5)
    member = request.session.get('member', None)
    member_id = member['id']
    c['timelines'] = handleDynamic(member_id, page, pagesize)
    return render_to_response("account/"+request.lang+"/index_timeline.html", c, context_instance=RequestContext(request))


def handleDynamic(member_id, page, pagesize):       #handleDynamic
    #can be change to by time
    if page <= 1:
        page = 1
    if pagesize <= 1:
        pagesize = 1
    start_record = (int(page)-1) * int(pagesize)
    end_record = int(start_record) + int(pagesize)
    timeline_project_favorite = Helper.find_timeline_project_favorite(member_id, start_record, end_record)
    timeline_demand_favorite = Helper.find_timeline_demand_favorite(member_id, start_record, end_record)
    timeline_message = Helper.find_timeline_message(member_id, start_record, end_record)
    timeline_project_recommned = Helper.find_timeline_project_recommed(member_id, start_record, end_record)
    timeline_demand_recommend = Helper.find_timeline_demand_recommend(member_id, start_record, end_record)
    timeline_project_top = Helper.find_timeline_project_top(member_id, start_record, end_record)
    timeline_demand_top = Helper.find_timeline_demand_top(member_id, start_record, end_record)
    timeline_newchamasay = Helper.find_timeline_newchamasay(start_record, end_record)

    own_approve_project = Helper.find_own_approve_project(member_id, start_record, end_record)
    own_approve_demand = Helper.find_own_approve_demand(member_id, start_record, end_record)
    own_log_project = Helper.find_own_log_project(member_id, start_record, end_record)
    own_log_demand = Helper.find_own_log_demand(member_id, start_record, end_record)
    own_favorite_project = Helper.find_own_favorite_project(member_id, start_record, end_record)
    own_favorite_demand = Helper.find_own_favorite_demand(member_id, start_record, end_record)

    timelines = []

    if page == 1:
        project_list = Helper.find_timeline_project(0, 8)
        demand_list = Helper.find_timeline_demand(0, 5)
        for t in project_list:
            dto = _mapperDTOTimeLineByproject(t)
            timelines.append(dto)
        for t in demand_list:
            dto = _mapperDTOTimeLineBydemand(t)
            timelines.append(dto)
    for t in timeline_project_favorite:
        dto = _mapperDTOTimeLineByproject_favorite(t)
        timelines.append(dto)
    for t in timeline_demand_favorite:
        dto = _mapperDTOTimeLineBydemand_favorite(t)
        timelines.append(dto)
    for t in timeline_message:
        dto = _mapperDTOTimeLineBymessage(t)
        timelines.append(dto)
    for t in timeline_project_recommned:
        dto = _mapperDTOTimeLineByproject_recommned(t)
        timelines.append(dto)
    for t in timeline_demand_recommend:
        dto = _mapperDTOTimeLineBydemand_recommend(t)
        timelines.append(dto)
    for t in timeline_project_top:
        dto = _mapperDTOTimeLineByproject_top(t)
        timelines.append(dto)
    for t in timeline_demand_top:
        dto = _mapperDTOTimeLineBydemand_top(t)
        timelines.append(dto)
    for t in timeline_newchamasay:
        dto = _mapperDTOTimeLineBynewchamasay(t)
        timelines.append(dto)
    for t in own_approve_project:
        dto = _mapperDTOTimeLineByown_approve_project(t)
        timelines.append(dto)
    for t in own_approve_demand:
        dto = _mapperDTOTimeLineByown_approve_demand(t)
        timelines.append(dto)
    for t in own_log_project:
        dto = _mapperDTOTimeLineByown_log_project(t)
        timelines.append(dto)
    for t in own_log_demand:
        dto = _mapperDTOTimeLineByown_log_demand(t)
        timelines.append(dto)
    for t in own_favorite_project:
        dto = _mapperDTOTimeLineByown_favorite_project(t)
        timelines.append(dto)
    for t in own_favorite_demand:
        dto = _mapperDTOTimeLineByown_favorite_demand(t)
        timelines.append(dto)
    timelines.sort(key=lambda x: x.addtime, reverse=True)
    return timelines


def _mapperDTOTimeLineByproject(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_id = t.member.id
        dto.member_realname = t.member.fullname
        dto.content_link = reverse('sales.detail', args=(t.id, ))
        if t.is_anonymous:
            dto.content_cn_start_pre = t.member.company.get_type_display() + u"用户"
            dto.content_cn_start = u"发布了 "
            dto.member_avatar = reverse('account.avatar', args=(80, 80, "default.jpg"))
            dto.member_link = "###"
        else:
            #peter damiziben | bd
            if t.member.id == 6:
                dto.content_cn_start_pre = t.member.fullname
            else:
                dto.content_cn_start_pre = t.member.fullname + " " + t.member.company.name_cn
                if len(t.member.position_cn) > 0:
                    dto.content_cn_start_pre = dto.content_cn_start_pre + " | " + t.member.position_cn
            dto.content_cn_start = u"发布了 "
            dto.member_avatar = reverse('account.avatar', args=(80, 80, t.member.avatar))
            dto.member_link = reverse('account.profile', args=(t.member.id,))
        dto.content_cn = t.name_cn
        dto.content_cn_end = u" 项目"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = t.member.companyNameCn()
        dto.member_title = t.member.position_cn
        dto.project_id = t.id
        dto.content_type = 1
        return dto


def _mapperDTOTimeLineBydemand(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_id = t.member.id
        dto.member_realname = t.member
        dto.content_link = reverse('purchase.detail', args=(t.id, ))
        if t.is_anonymous:
            dto.content_cn_start_pre = t.member.company.get_type_display() + u"用户"
            dto.content_cn_start = u"发布了 "
            dto.member_avatar = reverse('account.avatar', args=(80, 80, "default.jpg"))
            dto.member_link = "###"
        else:
            if t.member.id == 6:
                dto.content_cn_start_pre = t.member.fullname
            else:
                dto.content_cn_start_pre = t.member.fullname + " " + t.member.company.name_cn
                if len(t.member.position_cn) > 0:
                    dto.content_cn_start_pre = dto.content_cn_start_pre + " | " + t.member.position_cn
            dto.content_cn_start = u"发布了 "
            dto.member_avatar = reverse('account.avatar', args=(80, 80, t.member.avatar))
            dto.member_link = reverse('account.profile', args=(t.member.id,))
        dto.content_cn = t.name_cn
        dto.content_cn_end = u" 需求"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = t.member.companyNameCn()
        dto.member_title = t.member.position_cn
        dto.project_id = t.id
        dto.content_type = 2
        return dto


def _mapperDTOTimeLineByproject_favorite(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, t.member.avatar))
        dto.member_id = t.member.id
        dto.member_realname = t.member.fullname
        dto.member_link = reverse('account.profile', args=(t.member.id,))
        dto.content_link = reverse('sales.detail', args=(t.project.id, ))
        if t.member.id == 6:
            dto.content_cn_start_pre = t.member.fullname
        else:
            dto.content_cn_start_pre = t.member.fullname + " " + t.member.company.name_cn
            if len(t.member.position_cn) > 0:
                dto.content_cn_start_pre = dto.content_cn_start_pre + " | " + t.member.position_cn
        dto.content_cn_start =u"关注了您的 "
        dto.content_cn = t.project.name_cn
        dto.content_cn_end = u" 项目"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = t.member.companyNameCn()
        dto.member_title = t.member.position_cn
        dto.project_id = t.project.id
        dto.content_type = 3
        return dto


def _mapperDTOTimeLineBydemand_favorite(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, t.member.avatar))
        dto.member_id = t.member.id
        dto.member_realname = t.member
        dto.member_link = reverse('account.profile', args=(t.member.id,))
        dto.content_link = reverse('purchase.detail', args=(t.demand.id, ))
        if t.member.id == 6:
            dto.content_cn_start_pre = t.member.fullname
        else:
            dto.content_cn_start_pre = t.member.fullname + " " + t.member.company.name_cn
            if len(t.member.position_cn) > 0:
                dto.content_cn_start_pre = dto.content_cn_start_pre + " | " + t.member.position_cn
        dto.content_cn_start = u"关注了您的"
        dto.content_cn = t.demand.name_cn
        dto.content_cn_end = u" 需求"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = t.member.companyNameCn()
        dto.member_title = t.member.position_cn
        dto.project_id = t.demand.id
        dto.content_type = 4
        return dto


def _mapperDTOTimeLineBymessage(t):
        dto = DTOTimeline()
        dto.addtime = t.update_time
        # sender = Helper.find_dynamic_member(t.type, t.item_id)
        # if sender:
        #     dto.member_avatar = reverse('account.avatar', args=(80, 80, sender.avatar))
        #     dto.member_id = sender.id
        #     dto.member_realname = sender.fullname
        #     dto.member_link = reverse('account.profile', args=(sender.id,))
        # else:
        dto.member_avatar = reverse('account.avatar', args=(80, 80, "default.jpg"))
        dto.member_id = ""
        dto.member_realname = ""
        dto.member_link = "###"
        dto.content_link = reverse('account.messages', args=())
        dto.content_cn_start = ""
        dto.content_cn = t.memo
        '''
        dto.addtime = t["add_time"]
        dto.member_avatar = reverse('account.avatar', args=(80, 80, t["sender__avatar"]))
        dto.member_id = t["sender__id"]
        dto.member_realname = t["sender__last_name"] + t["sender__first_name"]
        dto.member_link = reverse('account.profile', args=(t["sender__id"],))
        dto.content_link = reverse('account.messages', args=())
        dto.content_cn_start = ""
        dto.content_cn = t["sender__last_name"] + t["sender__first_name"]+u"给您发了一条消息"
        '''
        dto.content_cn_end = ""
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = t.member.companyNameCn()
        dto.member_title = t.member.position_cn
        dto.project_id = 0
        dto.content_type = 5
        return dto


def _mapperDTOTimeLineByproject_recommned(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, "default.jpg"))
        dto.member_id = 0
        dto.member_realname = ""
        dto.member_link = ""
        dto.content_link = reverse('sales.detail', args=(t.project.id, ))
        dto.content_cn_start_pre = u"NewChama "
        dto.content_cn_start = u"通知您的"
        dto.content_cn = t.project.name_cn
        dto.content_cn_end = u" 项目被推荐了"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = ""
        dto.member_title = ""
        dto.project_id = t.project.id
        dto.content_type = 6
        return dto

def _mapperDTOTimeLineBydemand_recommend(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, "default.jpg"))
        dto.member_id = 0
        dto.member_realname = ""
        dto.member_link = ""
        dto.content_link = reverse('purchase.detail', args=(t.demand.id, ))
        dto.content_cn_start_pre = u"NewChama "
        dto.content_cn_start=u"通知您的"
        dto.content_cn = t.demand.name_cn
        dto.content_cn_end = u" 需求被推荐了"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = ""
        dto.member_title = ""
        dto.project_id = t.demand.id
        dto.content_type = 7
        return dto


def _mapperDTOTimeLineByproject_top(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, "default.jpg"))
        dto.member_id = 0
        dto.member_realname = ""
        dto.member_link = ""
        dto.content_link = reverse('sales.detail', args=(t.project.id, ))
        dto.content_cn_start_pre = u"NewChama"
        dto.content_cn_start=u"通知您的"
        dto.content_cn = t.project.name_cn
        dto.content_cn_end = u"项目被置顶了"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = ""
        dto.member_title = ""
        dto.project_id = t.project.id
        dto.content_type = 8
        return dto


def _mapperDTOTimeLineBydemand_top(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, "default.jpg"))
        dto.member_id = 0
        dto.member_realname = ""
        dto.member_link = ""
        dto.content_link = reverse('purchase.detail', args=(t.demand.id, ))
        dto.content_cn_start_pre = u"NewChama "
        dto.content_cn_start=u"通知您的"
        dto.content_cn = t.demand.name_cn
        dto.content_cn_end = u"需求被置顶了"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = ""
        dto.member_title = ""
        dto.project_id = t.demand.id
        dto.content_type = 9
        return dto


def _mapperDTOTimeLineBynewchamasay(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, "default.jpg"))
        dto.member_id = 0
        dto.member_realname = "NewChama"
        dto.member_link = "###"
        dto.content_cn_start_pre = "NewChama"
        dto.content_cn_start = t.content_cn
        dto.content_en = t.content_en
        dto.member_company = ""
        dto.member_title = ""
        dto.project_id = 0
        dto.content_type = 10
        return dto


def _mapperDTOTimeLineByown_approve_project(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, "default.jpg"))
        dto.member_id = 0
        dto.member_realname = ""
        dto.member_link = ""
        dto.content_link = reverse('sales.detail', args=(t.id, ))
        dto.content_cn_start_pre = u"NewChama "
        dto.content_cn_start=u"通知您的"
        dto.content_cn = t.name_cn
        dto.content_cn_end = u"项目已审核通过"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = ""
        dto.member_title = ""
        dto.project_id = t.id
        dto.content_type = 11
        return dto


def _mapperDTOTimeLineByown_approve_demand(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, "default.jpg"))
        dto.member_id = 0
        dto.member_realname = ""
        dto.member_link = ""
        dto.content_link = reverse('purchase.detail', args=(t.id, ))
        dto.content_cn_start_pre = u"NewChama "
        dto.content_cn_start=u"通知您的"
        dto.content_cn = t.name_cn
        dto.content_cn_end = u"需求已审核通过"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = ""
        dto.member_title = ""
        dto.project_id = t.id
        dto.content_type = 12
        return dto


def _mapperDTOTimeLineByown_log_project(t):
        dto = DTOTimeline()
        dto.addtime = t.update_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, t.member.avatar))
        dto.member_id = t.member.id
        dto.member_realname = t.member
        dto.member_link = reverse('account.profile', args=(t.member.id,))
        dto.content_link = reverse('sales.detail', args=(t.item_id, ))
        dto.content_cn_start = u"您查看了 "
        dto.content_cn = t.memo
        dto.content_cn_end = u" 项目"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = t.member.companyNameCn()
        dto.member_title = t.member.position_cn
        dto.project_id = t.item_id
        dto.content_type = 13
        return dto


def _mapperDTOTimeLineByown_log_demand(t):
        dto = DTOTimeline()
        dto.addtime = t.update_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, t.member.avatar))
        dto.member_id = t.member.id
        dto.member_realname = t.member
        dto.member_link = reverse('account.profile', args=(t.member.id,))
        dto.content_link = reverse('purchase.detail', args=(t.item_id, ))
        dto.content_cn_start = u"您查看了 "
        dto.content_cn = t.memo
        dto.content_cn_end = u" 需求"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = t.member.companyNameCn()
        dto.member_title = t.member.position_cn
        dto.project_id = t.item_id
        dto.content_type = 14
        return dto


def _mapperDTOTimeLineByown_favorite_project(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, t.member.avatar))
        dto.member_id = t.member.id
        dto.member_realname = t.member
        dto.member_link = reverse('account.profile', args=(t.member.id,))
        dto.content_link = reverse('sales.detail', args=(t.project.id, ))
        dto.content_cn_start = u"您关注了 "
        dto.content_cn = t.project.name_cn
        # dto.content_cn_end = t.member.fullname+u" 的项目"
        dto.content_cn_end = u" 项目"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = t.member.companyNameCn()
        dto.member_title = t.member.position_cn
        dto.project_id = t.project.id
        dto.content_type = 15
        return dto


def _mapperDTOTimeLineByown_favorite_demand(t):
        dto = DTOTimeline()
        dto.addtime = t.add_time
        dto.member_avatar = reverse('account.avatar', args=(80, 80, t.member.avatar))
        dto.member_id = t.member.id
        dto.member_realname = t.member
        dto.member_link = reverse('account.profile', args=(t.member.id,))
        dto.content_link = reverse('purchase.detail', args=(t.demand.id, ))
        dto.content_cn_start = u"您关注了 "
        dto.content_cn = t.demand.name_cn
        # dto.content_cn_end = t.member.fullname+u" 的需求"
        dto.content_cn_end = u" 需求"
        dto.content_en_start = ""
        dto.content_en = ""
        dto.content_en_end = ""
        dto.member_company = t.member.companyNameCn()
        dto.member_title = t.member.position_cn
        dto.project_id = t.demand.id
        dto.content_type = 16
        return dto


@csrf_protect
def login(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        checkcode =request.POST['checkcode']
        if checkcode !=request.session['checkcode']:
            messages.error(request,_('Active code is error'))
        else:
            #role = request.POST['role']
            role = ""
            m, bool = Member.login(username, password)
            if bool is False:
                messages.error(request, m)
            else:
                if m.status ==4:
                    request.session["member"] = buildMemberForFront(request, m, role)
                    write_login_log(request,m,'active_error')
                    return redirect('account.active_error')

                if m.status ==3:
                    request.session["member"] = buildMemberForFront(request, m, role)
                    write_login_log(request,m,'must_change_password')
                    return redirect('account.must_change_password')

                request.session["member"] = buildMemberForFront(request, m, role)

                m.last_login_time = datetime.datetime.now()
                login_count = m.login_count
                m.login_count += 1
                m.save()
                if login_count == 0:
                    write_login_log(request,m,'setting_first')
                    return redirect("account.setting_first")
                
                if request.GET.get('back_url',None):
                    write_login_log(request,m,request.GET['back_url'])
                    return redirect(request.GET['back_url'])
                else:
                    write_login_log(request,m,'index')
                    return redirect('account.index')
            
        c['username'] = username
    c['title'] = _("Login")
    response = render_to_response("account/"+request.lang+"/login.html", c, context_instance=RequestContext(request))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, request.lang)
    return response

person_email=['163.com','126.com','qq.com','sina.com','sohu.com','me.com','hotmail.com','yahoo.com.cn','tom.com','hexun.com','21cn.com','sohu.com','sogou.com','56.com','3126.com','mail.china.com','china.com','gmail.com','139.com','5ydns.com','263.com','yahoo.fr', 'outlook.com']


@csrf_protect
def signup(request):
    c = {}
    c.update(csrf(request))
    c['title'] = _("Signup")
    # ... view code here
    isvalid = True
    form = EntryForm()
    
    is_cn = request.lang == 'zh-cn'
    
    mobile_intel = 86
    if is_cn is False:
        
        mobile_intel = 1
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['confirm_password']
        company_type = request.POST.get('company_type', "")
        company = request.POST['company']
        
        fullname = request.POST['fullname']
        mobile = request.POST['mobile']
        mobile_intel = request.POST['mobile_intel']
        checkcode = request.POST['checkcode']

        if email.strip() == "":
            isvalid = False
            messages.warning(request, _("please input your email"))
        if password.strip() == "":
            isvalid = False
            messages.warning(request, _("please input your password"))
        if password_confirm != password:
            isvalid = False
            messages.warning(request, _("please confirm your password"))
        #if company_type == "":
        #   isvalid = False
        #   messages.warning(request, _("please select your company type"))
        if company.strip() == "":
            isvalid = False
            messages.warning(request, _("please input your company"))
        
        if fullname.strip() == "":
            isvalid = False
            messages.warning(request, _("please input your fullname"))
        
        if mobile.strip() == "":
            isvalid = False
            messages.warning(request, _("please input your mobile"))
        
                
        if checkcode !=request.session['checkcode']:
            isvalid = False
            messages.warning(request,_('Active code is error'))

        # form.company_type = company_type
        form.email = email
        form.fullname = fullname
        form.mobile = mobile
        form.mobile_intel = mobile_intel
        form.company = company

        if isvalid:
            is_exist = False
            count_email = Member.objects.filter(email=email).count()
            if count_email > 0:
                is_exist = True
                messages.warning(request, _("the email is exist"))
            
            count_mobile = Member.objects.filter(mobile=mobile).count()
            if count_mobile > 0:
                is_exist = True
                messages.warning(request, _("the mobile is exist"))
            
            if is_exist is False:
                if len(form.email.split('@'))>1:
                    # email_domain=form.email.split('@')[1]
                    # if email_domain in person_email:
                    #     form.make_password(password)
                    #     form.save()
                    #     return redirect("account.signup_success")
                    # else:

                    _company_num=Company.objects.filter(name_cn=form.company).count()
                    if _company_num==0:
                        _new_company=Company()
                        _new_company.name_cn=form.company
                        #_new_company.type=int(form.company_type)

                        _new_company.data_source='User add'
                        form.make_password(password)
                        _new_company.status=4
                        _new_company.save()
                        form.save()
                        return redirect("account.signup_success")
                    else:
                        # _new_company=get_object_or_404(Company,name_cn=form.company)
                        # if _new_company.status == 4:                  #if company status = 4 then pass the user register
                        form.make_password(password)
                        form.save()
                        return redirect("account.signup_success")
                    '''
                    _new_user=Member()
                    _new_user.company=_new_company
                    _new_user.type=3
                    _new_user.status=4
                    _new_user.first_name=form.fullname
                    _new_user.mobile_intel=form.mobile_intel
                    _new_user.mobile=form.mobile
                    _new_user.email=form.email
                    _tmp_code = hashlib.new('md5', str(datetime.datetime.now())+email).hexdigest()
                    _new_user.activecode=_tmp_code

                    _new_user.make_password(form.password)
                    _new_user.expire_date=datetime.datetime.now()+datetime.timedelta(days=365)
                    otherLogin = request.session.get('other_login', None)
                    if otherLogin is not None:
                        ol = checkOtherLogin(otherLogin)
                        if ol:
                            if ol.login_type == LoginType.weixin:
                                _new_user.weixin_id = ol.id
                            elif ol.login_type == LoginType.weibo:
                                _new_user.weibo_id = ol.id
                            elif ol.login_type == LoginType.linkedin:
                                _new_user.linkedin_id = ol.id

                    _new_user.save()
                    try:
                        html_content = loader.render_to_string("account/"+request.lang+"/email_active.html", {'username':_new_user.first_name,'activecode':_new_user.activecode,'email':_new_user.email})

                        title=ugettext('NewChama users active messages')
                        try:
                            send_email_by_mq('email', 'email', title, _new_user.email, html_content)
                        except Exception, e:
                            msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [_new_user.email])
                            msg.content_subtype = "html"  # Main content is now text/html
                            msg.send()

                    except Exception, e:
                        pass
                    '''

                return redirect("account.signup_success_company")

    c['countries'] = Helper.find_countries()
    c['f'] = form
    c['mobile_intel'] = mobile_intel
    return render_to_response("account/"+request.lang+"/signup.html", c, context_instance=RequestContext(request))


def signup_success(request):
    return render_to_response("account/"+request.lang+"/signup_success.html")

def signup_success_company(request):
    return render_to_response("account/"+request.lang+"/signup_success_company.html")


def active(request):
    email = request.GET['email']
    active_code = request.GET['active_code']

    
    try:
        user = Member.objects.get(email=email,status=4)
       
    except ObjectDoesNotExist:
        # return HttpResponse(_('Active is error'))
        return redirect("account.login")

    
    if user.activecode != active_code:
        return HttpResponse(_('Active code is error'))
    else:
        user.status=1
        user.activecode=''

        role=""
        request.session["member"] = buildMemberForFront(request, user, role)
        user.last_login_time = datetime.datetime.now()
        user.login_count += 1
        user.save()

        company=get_object_or_404(Company,pk=user.company.id)
        company.status=1
        company.save()

        return redirect("account.setting_first")

@member_login_required
def active_error(request):
    c={}
    member_id = request.session["member"]["id"]
    c['member_id']=member_id
    return render_to_response("account/"+request.lang+"/active_error.html", c, context_instance=RequestContext(request))


@member_login_required
def send_active(request):
    c={}
    member_id = request.session["member"]["id"]
    member=get_object_or_404(Member,id=member_id)
    member.activecode = hashlib.new('md5', str(datetime.datetime.now())+member.email).hexdigest()
    member.status=4
    member.save()
    html_content = loader.render_to_string("account/"+request.lang+"/email_active.html", {'username':member.first_name,'activecode':member.activecode,'email':member.email})
    
    title=ugettext('NewChama users active messages')
    try:      
        send_email_by_mq('email','email',title,member.email,html_content)

    except Exception, e:
        msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [member.email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()


    return render_to_response("account/"+request.lang+"/email_resend_success.html", c, context_instance=RequestContext(request))



@member_login_required
def must_change_password(request):
    c = {}
    c.update(csrf(request))
    c['title'] = _("Account Settings")
    c['member'] = request.session.get('member', None)
    member_id = request.session["member"]["id"]
    u = Member.objects.get(pk=member_id)
    c['u'] = u
    if request.method == 'POST':
        is_valid = True
        
        new_password = request.POST["password"]
        new_password_confirm = request.POST["password_confirm"]
        
        if new_password == "":
            is_valid = False
            messages.warning(request, _("please input new password"))
        if new_password_confirm != new_password:
            is_valid = False
            messages.warning(request, _("please confirm new password"))
        if is_valid:
            u.make_password(new_password)
            u.status=1
            u.save()
            #return redirect('account.index')
            return redirect("account.setting_first") # BD open account, required finish the profile
        
    return render_to_response("account/"+request.lang+"/must_change_password.html", c, context_instance=RequestContext(request))


def forgot_sendmail_success(request):

    return render_to_response("account/"+request.lang+"/forgot_sendmail_success.html")

def forgot_change_success(request):

    return render_to_response("account/"+request.lang+"/forgot_change_success.html")

@csrf_protect
def forgot(request):
    c = {}
    c.update(csrf(request))
    isvalid = True
    c['title'] = _("Forgot password")
    if request.method == 'POST':

        checkcode = request.POST['checkcode']
        email = request.POST['email']

        if checkcode !=request.session['checkcode']:
            isvalid = False
            messages.warning(request,_('Active code is error'))

        if email.strip() == "":
            isvalid = False
            messages.warning(request, _("please input your email"))

        
        if isvalid:
            try:

                m = Member.objects.get(email=email)
                findpassword = FindPasswordHistory()
                findpassword.email = email
                code = hashlib.new('md5', str(datetime.datetime.now())+email).hexdigest()
                findpassword.code = code
                findpassword.save()
                url_reset_password = "http://"+request.META['HTTP_HOST']+reverse("account.reset_password", args=[email, code])
                html_content = loader.render_to_string("account/"+request.lang+"/email_findpassword.html", {'url':url_reset_password,'name':m})
                
                title=ugettext('NewChama Reset Password')
                try:
                   
                    send_email_by_mq('email','email',title,email,html_content)

                except Exception, e:
                    msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [email])
                    msg.content_subtype = "html"  # Main content is now text/html
                    msg.send()

                return redirect('account.forgot_sendmail_success')
                #print url_reset_password
            except ObjectDoesNotExist:
                messages.error(request, _("the email is not exist"))
    return render_to_response("account/"+request.lang+"/forgot.html", c, context_instance=RequestContext(request))


@csrf_protect
def reset_password(request, email, code):
    c = {}
    c.update(csrf(request))
    c['title'] = _("Reset password")

    findpassword = get_object_or_404(FindPasswordHistory, code=code)
    if findpassword.email != email:
        return HttpResponse(_("email error"))
    if findpassword.is_used:
        return HttpResponse(_("the code is used"))
    try:
        u = Member.objects.get(email=email)
        c['u'] = u
        c['code'] = code
        c['email'] = email
    except ObjectDoesNotExist:
        return HttpResponse(_("the email is not exist"))

    if request.method == 'POST':
        id_post = request.POST['id']
        code_post = request.POST['code']
        email_post = request.POST['email']
        new_password = request.POST["password"]
        new_password_confirm = request.POST["password_confirm"]
        isvalid = True
        if new_password == "":
            isvalid = False
            messages.warning(request, _("please input your new password"))
        if new_password_confirm != new_password:
            isvalid = False
            messages.warning(request, _("please confirm your new password"))
        if isvalid:
            try:
                findpassword_temp = FindPasswordHistory.objects.get(code=code_post)
                findpassword_temp.is_used = True
                findpassword_temp.used_time = datetime.datetime.now()
                findpassword_temp.save()
                member_temp = Member.objects.get(pk=id_post)
                member_temp.make_password(new_password)
                member_temp.save()
                
                m=get_object_or_404(Member,email=email_post)
                role=""
                request.session["member"] = buildMemberForFront(request, m, role)
                m.last_login_time = datetime.datetime.now()
                login_count = m.login_count
                m.login_count += 1
                m.save()
                

                return redirect("account.forgot_change_success")
            except Exception, e:
                messages.error(request, e.message)
    return render_to_response("account/"+request.lang+"/reset_password.html", c, context_instance=RequestContext(request))


def logout(request):
    if request.session.get('member', None) is not None:
        del request.session["member"]
    return redirect("home.index")


@member_login_required
def profile(request,user_id):
    c = {}
    c['title'] = _("Profile")
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    member = Member.objects.get(pk=member_id)
    u = get_object_or_404(Member, pk=user_id)
    c['user'] = u
    u_other = Member.objects.filter(company_id=u.company_id).exclude(id=u.id)
    c['users_other'] = u_other
    projects = Project.objects.filter(member_id=user_id,status=StatusProject.approved, is_anonymous=False).order_by("-update_time")[0:5]
    c['data'] = projects
    c['is_added_to_favorite'] = member.is_added_member_to_favorites(u)
    c['favorites_project_ids'] = Helper.find_member_favorite_project_ids(member_id)
    write_member_view_log(request,member,u)
    return render_to_response("account/"+request.lang+"/profile.html", c, context_instance=RequestContext(request))


@member_login_required
def company(request, company_id):
    c = {}
    c['title'] = _("Company")
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    member = Member.objects.get(pk=member_id)
    company = get_object_or_404(Company, pk=company_id)
    c['company'] = company
    projects = Project.objects.filter(member__company_id=company_id, status=StatusProject.approved, is_anonymous=False).order_by("-update_time")[0:5]
    c['projects'] = projects
    c['otherCompany'] = True
    c['is_added_to_favorite'] = member.is_added_company_to_favorites(company)
    c['favorites_project_ids'] = Helper.find_member_favorite_project_ids(member_id)
    c['historyList'] = InvestmentHistory.objects.filter(company__id=company_id).order_by("-happen_date")[0:10]

    resource=request.GET.get('s',None)
    pid=request.GET.get('p',None)
    is_man=request.GET.get('m',None)

    if resource=='recommond':
        if is_man=='man':
            write_company_view_recommond_man_log(request,member,company,pid)
        else:
            write_company_view_recommond_machine_log(request,member,company,pid)
    else:
        write_company_view_log(request,member,company,'')
    return render_to_response("account/"+request.lang+"/company.html", c, context_instance=RequestContext(request))


@member_login_required
def o_company(request, company_id, company_type):
    c = {}
    c['title'] = _("Company")
    c['member'] = request.session.get('member', None)
    if company_type == "1":
        company = get_object_or_404(InvestmentCompany, pk=company_id)
        # historyList = InvestmentHistory.objects.filter(company__id=company_id).order_by("-happen_date")[0:10]
        _sql = "select ih.id, ih.targetcompany, ih.type, ih.happen_date, ih.amount, ih.currency, ih.person, ih.usd," \
               "i1.name_cn cv1_cn, i1.name_en cv1_en, i2.name_cn cv2_cn, i2.name_en cv2_en, i3.name_cn cv3_cn, i3.name_en cv3_en," \
               "ac.name_cn country_cn, ac.name_en country_en, ap.name_cn province_cn, ap.name_en province_en," \
               "aci.name_cn city_cn, aci.name_en city_en " \
               "from repository_investmenthistory ih " \
               "left join industry_industry i1 on i1.id = ih.cv1 " \
               "left join industry_industry i2 on i2.id = ih.cv2 " \
               "left join industry_industry i3 on i3.id = ih.cv3 " \
               "left join area_country ac on ac.id = ih.country_id " \
               "left join area_province ap on ap.id = ih.province_id " \
               "left join area_city aci on aci.id = ih.city_id where company_id = " + company_id + " order by happen_date desc"
        historyList = InvestmentHistory.objects.raw(_sql)[0 : 10]
        c["historyList"] = historyList
    else:
        company = get_object_or_404(ListedCompany, pk=company_id)
    c['company'] = company
    c['otherCompany'] = True
    return render_to_response("account/"+request.lang+"/company.html", c, context_instance=RequestContext(request))


@member_login_required
def invitation(request):
    c = {}
    c['title']=_("Invitation")
    c['member']=request.session.get('member', None)
    return render_to_response("account/"+request.lang+"/invitation.html", c, context_instance=RequestContext(request))


@member_login_required
@csrf_protect
def ajax_preference(request):
    if request.method == 'POST':
        try:
            member_id = request.session.get('member', None)['id']
            preferenceIsExist = False
            type_public = request.POST.get("type_public", False)    #public type for project, demand or keyword
            type_category = request.POST.get("type_category", False)    #preference type for industry or location
            if type_category == "industry":
                member_industry_id = request.POST.get("member_industry_id", False)
                member_industry_countryId = request.POST.get("member_industry_countryId", False)
                piy = PreferenceIndustry.objects.filter(preference__member__id=member_id, preference__title=type_public, industry_id=member_industry_id, country_id=member_industry_countryId)#Preference().TITLE_PREFERENCE["news"]

                if piy:
                    return HttpResponse("exist")

                id_post = request.POST.get("id", False)
                p = Preference()
                if id_post:
                    p = Preference.objects.get(pk=id_post)
                else:
                    p.title = type_public
                    p.member_id = member_id
                    p.save()

                member_range_min = request.POST.get("member_range_min", False)
                member_range_max = request.POST.get("member_range_max", False)
                member_currency = request.POST.get("member_currency", False)

                pi = PreferenceIndustry()
                pi.preference = p
                pi.industry_id = member_industry_id
                pi.range_min = member_range_min
                pi.range_max = member_range_max
                pi.country_id = member_industry_countryId
                pi.currency_type_financial = member_currency
                pi.save()
            elif type_category == "location":
                member_country_id = request.POST.get("member_country_id", False)
                member_title = request.POST.get("member_title", False)
                pln = PreferenceLocation.objects.filter(preference__member__id=member_id, preference__title=type_public, country_id=member_country_id)
                if pln:
                    return HttpResponse("exist")

                id_post = request.POST.get("id", False)
                p = Preference()
                if id_post:
                    p = Preference.objects.get(pk=id_post)
                else:
                    p.title = type_public
                    p.member_id = member_id
                    p.save()

                pl = PreferenceLocation()
                pl.preference = p
                pl.title = member_title
                pl.country_id = member_country_id
                pl.save()
            elif type_category == "keyword":
                keyword = request.POST.get("keyword", False)
                plk = PreferenceKeyword.objects.filter(preference__member__id=member_id, keyword=keyword)
                if plk:
                    return HttpResponse("exist")

                id_post = request.POST.get("id", False)
                p = Preference()
                if id_post:
                    p = Preference.objects.get(pk=id_post)
                else:
                    p.title = type_public
                    p.member_id = member_id
                    p.save()

                pk = PreferenceKeyword()
                pk.preference = p
                pk.keyword = keyword
                pk.save()

            return HttpResponse("success")
        except Exception, e:
            return HttpResponse(e)

    return HttpResponse("error")


@member_login_required
@csrf_protect
def ajax_preference_remove(request):
    if request.method == 'POST':
        try:
            id_post = request.POST.get("id", False)
            type_post = request.POST.get("type", False)
            if type_post == "industry":
                PreferenceIndustry.objects.get(pk=id_post).delete()
            elif type_post == "location":
                PreferenceLocation.objects.get(pk=id_post).delete()
            elif type_post == "keyword":
                PreferenceKeyword.objects.get(pk=id_post).delete()

            return HttpResponse("success")

        except Exception, e:
            return HttpResponse(e)

    return HttpResponse("error")


@member_login_required
@csrf_protect
def ajax_preference_news(request):
    if request.method == 'POST':
        try:
            member_id = request.session.get('member', None)["id"]
            type_public = request.POST.get("type_public", False)    #public type for project, demand or keyword
            tag = request.POST.get("tag", False)
            pk = PreferenceKeyword.objects.filter(preference__member__id=member_id, preference__title=type_public, keyword=tag)#Preference().TITLE_PREFERENCE["news"]
            if pk:
                return HttpResponse("exist")
            try:
                p = Preference.objects.get(member_id=member_id, title=type_public)
            except:
                p = Preference()
                p.member_id = member_id
                p.title = type_public
                p.save()

            newPk = PreferenceKeyword()
            newPk.preference = p
            newPk.keyword = tag
            newPk.save()
            return HttpResponse("success")

        except Exception, e:
            return HttpResponse(e)

    return HttpResponse("error")


@member_login_required
@csrf_protect
def preference(request, type, isfirst=False):
    c = {}
    c['title'] = _("Preference")
    c.update(csrf(request))
    member = request.session.get('member', None)
    c['member'] = member
    if member:
        member_id = request.session['member']['id']
    if request.method == "POST":
        try:
            id_post = request.POST.get("id", "")
            if id_post != "":
                p = Preference.objects.get(pk=id_post)
                p.title = type
            else:
                p = Preference()
                p.title = type
            if member:
                p.member_id = member_id
            p.save()

            if type != "news":
                member_industry_ids = request.POST.getlist("member_industry_ids", [])
                member_range_mins = request.POST.getlist("member_range_mins", [])
                member_range_maxs = request.POST.getlist("member_range_maxs", [])
                member_industry_countryIds = request.POST.getlist("member_industry_countryIds", [])
                member_currencys = request.POST.getlist("member_currencys", [])
                p.preference_industry.all().delete()
                if member_industry_ids is not None:
                    for i, j, k, m, n in zip(member_industry_ids, member_range_mins, member_range_maxs, member_industry_countryIds, member_currencys):
                        pi = PreferenceIndustry()
                        pi.preference = p
                        pi.industry_id = i
                        pi.range_min = j
                        pi.range_max = k
                        pi.country_id = m
                        pi.currency_type_financial = n
                        pi.save()

                member_country_ids = request.POST.getlist("member_country_ids", [])
                member_titles = request.POST.getlist("member_titles", [])
                p.preference_location.all().delete()
                if member_country_ids is not None:
                    for i, m in zip(member_country_ids, member_titles):
                        pl = PreferenceLocation()
                        pl.preference = p
                        pl.title = m
                        pl.country_id = i
                        pl.save()

            member_keywords = request.POST.getlist("member_keywords", [])
            p.preference_keyword.all().delete()
            if member_keywords is not None:
                for m in member_keywords:
                    k = PreferenceKeyword()
                    k.keyword = m
                    k.preference = p
                    k.save()

            messages.success(request, _("success"))
            if isfirst:
                return redirect("account.index")
            else:
                return redirect("account.preference_" + type)
        except Exception, e:
            messages.error(request, e.message)
            logger.error(e.message)
    else:
        preferences = Preference.objects.filter(member_id=member_id, title=type)[0 : 1]
        if len(preferences) > 0:
            p = preferences[0]
            c['p'] = p
            c['indusrtis'] = p.preference_industry.all()
            c['locations'] = p.preference_location.all()
            c['keywords'] = p.preference_keyword.all()
    c['countries'] = Helper.find_countries()
    c['industry1'] = Helper.find_industries_level1()
    c['currencyTypes'] = PreferenceIndustry.CURRENCY_TYPES
    c['type'] = type
    template_name = "account/"+request.lang+"/preference.html"
    if isfirst:
        template_name = "account/"+request.lang+"/first_preference.html"
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@csrf_exempt
@member_login_required
def ajax_project(request):
    c = {}
    if request.method == 'POST':
        try:
            type = request.POST.get("type", "")
            id = request.POST.get("id", "")
            #Terry 20140904
            condition = {}
            # condition["is_anonymous"]=False
            condition["status"]=StatusProject.approved
            condition["expire_date__gt"]=datetime.datetime.today
            condition["is_suitor"]=True
            if type == "industry":
                condition["company_industry"]=id
                rangeMin = request.POST.get("rangemin", "")
                rangeMax = request.POST.get("rangemax", "")
                condition["expected_enterprice_value__gte"] = rangeMin
                condition["expected_enterprice_value__lte"] = rangeMax
            else:
                location = request.POST.get("location", "")
                if location == "city":
                    condition["company_cities"]=id
                elif location == "province":
                    condition["company_province"]=id
                else:
                    condition["company_country"]=id
            projects = Project.objects.filter(**condition).order_by("-update_time")[0 : 10]

        except Exception, e:
            logger.error(e.message)

    c['data'] = projects
    return render_to_response("account/"+request.lang+"/ajax_project.html", c, context_instance=RequestContext(request))



@member_login_required
@csrf_protect
def setting(request, isfirst=False):
    c = {}
    c.update(csrf(request))
    c['title'] = _("Account Settings")
    c['member'] = request.session.get('member', None)
    c["industrys"] = Helper.find_industries_level1()
    member_id = request.session["member"]["id"]
    u = Member.objects.get(pk=member_id)
    mks = u.member_focus_keyword.all()
    c['focus_keywords'] = mks
    keywords = ""
    if len(mks) > 0:
        for m in mks:
            keywords += m.keyword + ","
        keywords = keywords[0 : len(keywords) - 1]
    c['keywords'] = keywords
    c['u'] = u
    if request.method == 'POST':
        is_english = (request.lang == "en-us")
        tel = request.POST.get("tel",'')
        mobile = request.POST["mobile"]
        tel_intel = request.POST.get("tel_intel",'')
        mobile_intel = request.POST["mobile_intel"]
        u.tel_intel = tel_intel
        u.mobile_intel = mobile_intel
        u.tel = tel
        u.mobile = mobile
        u.focus_aspect = request.POST.getlist("industrys", [])
        if is_english:
            intro_en = request.POST["intro_en"]
            position_en = request.POST.get('position_en','')
            u.intro_en = intro_en
            u.position_en = position_en
        else:
            intro_cn = request.POST["intro_cn"]
            position_cn = request.POST.get('position_cn','')
            u.intro_cn = intro_cn
            u.position_cn = position_cn

        temp_pic_name = request.POST["imgName"]
        is_new_avatar = False
        if temp_pic_name != "":
            is_new_avatar = True
        try:
            if is_new_avatar:
                x1 = int(request.POST["x1"])
                y1 = int(request.POST["y1"])
                x2 = int(request.POST["x2"])
                y2 = int(request.POST["y2"])
                w = int(request.POST["imgWidth"])
                h = int(request.POST["imgHeight"])
                temp_path = MEDIA_ROOT + "/temp/"
                temp_pic = os.path.join(temp_path+temp_pic_name)

                pic_uuid_name = str(uuid.uuid1())+'.jpg'

                file_origin_name = '%s/avatars/%s/%s' % (MEDIA_ROOT, 'origin', pic_uuid_name)

                im = Image.open(temp_pic)

                w0 = im.size[0]
                h0 = im.size[1]

                rate = float(w0)/float(w)
                temp_im = im.crop((int(x1*rate), int(y1*rate), int(x2*rate), int(y2*rate)))
                #im.crop((100,100,200,200))
                #im.save(file_origin_name)
                temp_im.thumbnail((400, 400), Image.ANTIALIAS)

                temp_im.save(file_origin_name, "JPEG")

                u.avatar = pic_uuid_name
                request.session["member"]["avatars"] = pic_uuid_name
            u.save()

            project_keyword = request.POST.get("project_keyword", False)
            u.member_focus_keyword.all().delete()
            if project_keyword:
                mks = project_keyword.split(",")
                for m in mks:
                    k = MemberFocusKeyword()
                    k.keyword = m
                    k.member = u
                    k.save()

            #temp_im.close()
            #im.close()
            if isfirst:
                return redirect("account.index")
            messages.success(request, _("success"))
        except Exception, e:
            messages.error(request, e.message)
            logger.error(e.message)
    template_name = "account/"+request.lang+"/setting.html"
    if isfirst:
        current_member = Member.objects.get(pk=member_id)
        if current_member.login_count == 0:
            current_member.login_count += 1
            current_member.save()

        industry_list=Industry.objects.filter(level=1,is_display=True).all()

        template_name = "account/"+request.lang+"/first_setting.html"
    c['countries'] = Helper.find_countries()
    c["industries"] = Helper.find_industries_level1()
    c["industries2"] = Helper.find_industries_level2()
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@member_login_required
def focus(request, isfirst=False):
    c = {}
    c.update(csrf(request))
    c['title'] = _("Focus Aspect")
    c['member'] = request.session.get('member', None)
    member_id = request.session["member"]["id"]
    if request.method == 'POST':
        u = Member.objects.get(pk=member_id)
        industrys = request.POST.getlist("industrys", [])
        u.focus_aspect = industrys
        u.save()
        return redirect("account.index")
    c["industrys"] = Helper.find_industries_level1()
    return render_to_response("account/"+request.lang+"/focus.html", c, context_instance=RequestContext(request))


@member_login_required
def changepassword(request):
    c = {}
    c.update(csrf(request))
    c['title'] = _("Account Settings")
    c['member'] = request.session.get('member', None)
    member_id = request.session["member"]["id"]
    u = Member.objects.get(pk=member_id)
    c['u'] = u
    if request.method == 'POST':
        is_valid = True
        old_password = request.POST["old-password"]
        new_password = request.POST["new-password-1"]
        new_password_confirm = request.POST["new-password-2"]
        if old_password == "":
            is_valid = False
            messages.warning(request, _("please input old password"))
        if new_password == "":
            is_valid = False
            messages.warning(request, _("please input new password"))
        if new_password_confirm != new_password:
            is_valid = False
            messages.warning(request, _("please confirm new password"))
        if is_valid:
            if u.check_password(old_password):
                u.make_password(new_password)
                u.save()
                messages.success(request, _("success"))
            else:
                messages.error(request, _("The old password is incorrect"))
    return render_to_response("account/"+request.lang+"/changepassword.html", c, context_instance=RequestContext(request))






@member_login_required
def search_keyword_message(request):
   
    c = {}
    c['title']=_("Notifications")
    keyword = request.GET.get("keyword", '')
    c['member']=request.session.get('member', None)
    # current_member=get_object_or_404(Member,pk=c['member']['id'])
    current_member=request.session["member"]["id"]

    message_list=Message.objects.filter(

        (Q(sender_id=current_member)| Q(receiver_id=current_member))&

        (Q(content__contains=keyword)| Q(sender__first_name__contains=keyword) |  Q(receiver__first_name__contains=keyword)| Q(sender__last_name__contains=keyword) |  Q(receiver__last_name__contains=keyword) |  Q(project__name_cn__contains=keyword) |  Q(project__name_en__contains=keyword)|  Q(demand__name_cn__contains=keyword) |  Q(demand__name_en__contains=keyword)),is_delete=0).order_by('-id')
    
    c['message_list']=message_list[:10]

    c['keyword']=keyword
    return render_to_response("account/"+request.lang+"/search_message_center.html", c, context_instance=RequestContext(request))






@member_login_required
def ajax_search_message_more(request,page=1,pagesize=10):
    template_name="ajax_search_message_more.html"
    
    c = {}
    c['title']=_("Notifications")
    keyword = request.GET.get("keyword", '')
    c['member']=request.session.get('member', None)
    # current_member=get_object_or_404(Member,pk=c['member']['id'])
    current_member=request.session["member"]["id"]
    start_idx=(int(page)-1)*int(pagesize)
    end_idx=int(page)*int(pagesize)
    message_list=Message.objects.filter(

        (Q(sender_id=current_member)| Q(receiver_id=current_member))&

        (Q(content__contains=keyword)| Q(sender__first_name__contains=keyword) |  Q(receiver__first_name__contains=keyword)| Q(sender__last_name__contains=keyword) |  Q(receiver__last_name__contains=keyword) |  Q(project__name_cn__contains=keyword) |  Q(project__name_en__contains=keyword)|  Q(demand__name_cn__contains=keyword) |  Q(demand__name_en__contains=keyword)),is_delete=0).order_by('-id')[start_idx:end_idx]
    
    c['message_list']=message_list


    return render_to_response("account/"+request.lang+"/"+template_name, c, context_instance=RequestContext(request))






@member_login_required
def ajax_message_center_person_more(request,page=1,pagesize=10):
    template_name="message_center_person_more.html"
    c = {}
    c['title']=_("Notifications")
    c['member']=request.session.get('member', None)
    # current_member=get_object_or_404(Member,pk=c['member']['id'])
    current_member=request.session["member"]["id"]
    message_list=[]
    


    #_sql="select sender_id,receiver_id, max(id) id from member_message where (receiver_id ="+str(current_member)+"  or sender_id ="+str(current_member)+")and is_delete =0 group by sender_id,receiver_id order by id desc"
    _sql="select sender_id,receiver_id, max(id) id from member_message_log where (receiver_id ="+str(current_member)+" or sender_id ="+str(current_member)+") and item_type=0 group by sender_id,receiver_id order by update_time desc"
    _message_list=Message.objects.raw(_sql)
    _message_id_list=[]
                
    for m in _message_list:
            
        print m.sender_id,m.receiver_id
        if m.sender_id==current_member:
            if m.receiver_id not in _message_id_list:
                _message_id_list.append(m.receiver_id)
                message_list.append(m)
        if m.receiver_id==current_member:
            if m.sender_id not in _message_id_list:
                _message_id_list.append(m.sender_id)
                message_list.append(m)

    
    start_idx=(int(page)-1)*int(pagesize)
    end_idx=int(page)*int(pagesize)

    c['message_list']=message_list[start_idx:end_idx]
    
    return render_to_response("account/"+request.lang+"/"+template_name, c, context_instance=RequestContext(request))


@member_login_required
def message_center(request, sort_type):
    template_name="message_center.html"
    c = {}
    c['title']=_("Notifications")
    c['member']=request.session.get('member', None)
    # current_member=get_object_or_404(Member,pk=c['member']['id'])
    current_member=request.session["member"]["id"]
    message_list=[]
    total_list = []
    # project_message_list=[]
    # demand_message_list=[]
    if sort_type == "person":
        
        #_sql="select sender_id,receiver_id, max(id) id from member_message where (receiver_id ="+str(current_member)+"  or sender_id ="+str(current_member)+")and is_delete =0 group by sender_id,receiver_id order by id desc"
        #_sql="select * from (select sender_id,receiver_id,message_id id from member_message_log where (receiver_id ="+str(current_member)+" or sender_id ="+str(current_member)+") group by sender_id,receiver_id order by update_time desc"
        #_message_list=Message.objects.raw(_sql)
        _sql = "select sender_id,receiver_id, message_id, max(id) id from member_message_log "\
               "where (receiver_id ="+str(current_member)+" or sender_id ="+str(current_member)+") group by message_id, sender_id,receiver_id order by message_id desc"
        _message_list=Message_Log.objects.raw(_sql)
        _message_id_list=[]
                
        for m in _message_list:
            
            print m.sender_id,m.receiver_id
            if m.sender_id==current_member:
                if m.receiver_id not in _message_id_list:
                    _message_id_list.append(m.receiver_id)
                    message_list.append(m)
            if m.receiver_id==current_member:
                if m.sender_id not in _message_id_list:
                    _message_id_list.append(m.sender_id)
                    message_list.append(m)

    else:

        project_list= Message_Log.objects.exclude(item_id=None).filter(Q(receiver_id=current_member) | Q(sender_id=current_member),item_type=1).values('item_id').distinct()
        demand_list= Message_Log.objects.exclude(item_id=None).filter(Q(receiver_id=current_member) | Q(sender_id=current_member),item_type=2).values('item_id').distinct()
        for p in project_list:
            data = {}
            #_sql="select sender_id,receiver_id, max(id) id from member_message where (receiver_id ="+str(current_member)+"  or sender_id ="+str(current_member)+") and project_id ="+str(p['project_id'])+" and is_delete =0 group by sender_id,receiver_id order by id desc"
            _sql="select update_time,sender_id,receiver_id, max(id) id from member_message_log where (receiver_id ="+str(current_member)+"  or sender_id ="+str(current_member)+") and item_id ="+str(p['item_id'])+" and item_type =1 group by sender_id,receiver_id order by update_time desc"

            #_message_list=Message.objects.raw(_sql)
            _message_list = Message_Log.objects.raw(_sql)
            _message_id_list=[]

            p_message_list=[]

            for i, m in enumerate(_message_list):
                if i == 0:
                    data['message_time'] = m.update_time
                    #print type(m.update_time)
                    data['compare_time'] = int(time.mktime(m.update_time.timetuple()))
                if m.sender_id==current_member:
                    if m.receiver_id not in _message_id_list:
                        _message_id_list.append(m.receiver_id)
                        p_message_list.append(m)
                if m.receiver_id==current_member:
                    if m.sender_id not in _message_id_list:
                        _message_id_list.append(m.sender_id)
                        p_message_list.append(m)

            data['messages_list']=p_message_list[:10]
            project = Project.objects.filter(id=p['item_id']).first()
            if project:
                data['item_name']=project.name_cn
                data['item_id'] = project.id
                data['item_type'] = 1               #1 = project ; 2 = demand
                data['item_time'] = project.update_time

            # project_message_list.append(p)
            total_list.append(data)

        for d in demand_list:
            data = {}
            #_sql="select sender_id,receiver_id, max(id) id from member_message where (receiver_id ="+str(current_member)+"  or sender_id ="+str(current_member)+") and demand_id ="+str(d['demand_id'])+" and is_delete =0 group by sender_id,receiver_id order by id desc"
            _sql="select update_time, sender_id,receiver_id, max(id) id from member_message_log where (receiver_id ="+str(current_member)+"  or sender_id ="+str(current_member)+") and item_id ="+str(d['item_id'])+" and item_type =2 group by sender_id,receiver_id order by update_time desc"
            #_sql_update_time =
            #_message_list=Message.objects.raw(_sql)
            _message_list = Message_Log.objects.raw(_sql)
            _message_id_list=[]

            d_message_list=[]
                    
            for i, m in enumerate(_message_list):
                if i == 0:
                    data['message_time'] = m.update_time
                    data['compare_time'] = int(time.mktime(m.update_time.timetuple()))
                if m.sender_id==current_member:
                    if m.receiver_id not in _message_id_list:
                        _message_id_list.append(m.receiver_id)
                        d_message_list.append(m)
                if m.receiver_id==current_member:
                    if m.sender_id not in _message_id_list:
                        _message_id_list.append(m.sender_id)
                        d_message_list.append(m)

            data['messages_list']=d_message_list[:10]
            demand = Demand.objects.filter(id=d['item_id']).first()
            if demand:
                data['item_name']=demand.name_cn
                data['item_id'] = demand.id
                data['item_type'] = 1               #1 = project ; 2 = demand
                data['item_time'] = demand.update_time

            total_list.append(data)


        template_name="message_center_project.html"
    c['sort_type']=sort_type
    c['message_list']=message_list[:10]

    #res = Message.objects.filter(receiver_id=current_member, is_read=0).update(is_read=1) #将未读变成已读，后期要调整
    total_list.sort(key=lambda compare_time: compare_time, reverse=True)
    c['total_list'] = total_list
    # c['project_message_list']=project_message_list
    # c['demand_message_list']=demand_message_list
    return render_to_response("account/"+request.lang+"/"+template_name, c, context_instance=RequestContext(request))


@member_login_required
def notifications(request, message_type, company_id=0, project_id=0):

    c = {}
    c['title']=_("Notifications")
    c['member']=request.session.get('member', None)
    # current_member=get_object_or_404(Member,pk=c['member']['id'])
    current_member=request.session["member"]["id"]
    message_list=[]

    if message_type == "read":
        message_list = Message.objects.filter(receiver_id=current_member,is_delete=0,is_read__gt=0).order_by('-add_time')[0:10]

    elif message_type == "send":
        message_list = Message.objects.filter(sender_id=current_member).order_by('-add_time')[0:10]

    elif message_type == "user":
        members = Member.objects.filter(company_id=company_id)
        ms = []
        if members:
            for m in members:
                ms.append(m)
        message_list = Message.objects.filter(sender_id=current_member,is_read=0,is_delete=0,receiver__in=ms, project_id=project_id).order_by('-add_time')[0:10]

    else:
        message_list = Message.objects.filter(receiver_id=current_member,is_read=0,is_delete=0).order_by('-add_time')[0:10]

    c['message_type']=message_type
    c['message_list']=message_list

    return render_to_response("account/"+request.lang+"/notifications.html", c, context_instance=RequestContext(request))


@member_login_required
def ajax_notifications(request):
    c = {}
    c['member']=request.session.get('member', None)
    # current_member=get_object_or_404(Member,pk=c['member']['id'])
    current_member=request.session["member"]["id"]
    message_type = request.GET.get("message_type", "")
    page = request.GET.get('page', 1)
    pagesize = request.GET.get('pagesize', 10)
    start_record = (int(page)-1) * int(pagesize)
    end_record = int(start_record) + int(pagesize)
    if message_type == "read":
        total = Message.objects.filter(receiver_id=current_member,is_delete=0, is_read__gt=0).count()
        message_list = Message.objects.filter(receiver_id=current_member,is_delete=0, is_read__gt=0).order_by('-add_time')[start_record: end_record]
    elif message_type == "send":
        total = Message.objects.filter(receiver_id=current_member).count()
        message_list = Message.objects.filter(sender_id=current_member).order_by('-add_time')[start_record: end_record]
    else:
        total = Message.objects.filter(receiver_id=current_member, is_read=0, is_delete=0).count()
        message_list = Message.objects.filter(receiver_id=current_member, is_read=0, is_delete=0).order_by('-add_time')[start_record: end_record]

    c['message_list'] = message_list
    c['message_type'] = message_type
    return render_to_response("account/"+request.lang+"/ajax_notifications.html", c)


@member_login_required
def myfavorite(request, type):
    c = {}
    c['member'] = request.session.get('member', None)
    member_id = request.session["member"]['id']
    favorites = Favorites.objects.filter(member_id=member_id).order_by("-add_time")
    favorites_project = favorites.filter(type_relation=TypeFavorite.project, project__status=StatusProject.approved)
    favorites_demand = favorites.filter(type_relation=TypeFavorite.demand, demand__status=StatusDemand.approved)
    favorites_company = favorites.filter(type_relation=TypeFavorite.company)
    favorites_member = favorites.filter(type_relation=TypeFavorite.member)
    favorites_data = favorites.filter(type_relation=TypeFavorite.data)
    favorites_news = favorites.filter(type_relation=TypeFavorite.news)
    f_list = {"project": favorites_project, "demand": favorites_demand, "company": favorites_company, "member": favorites_member,"news": favorites_news, "data": favorites_data}
    c['favorites'] = f_list.get(type, favorites_project)[0:12]
    total_project = favorites_project.count()
    total_demand = favorites_demand.count()
    total_company = favorites_company.count()
    total_member = favorites_member.count()
    total_data = favorites_data.count()
    total_news = favorites_news.count()
    c['total_project'] = total_project
    c['total_demand'] = total_demand
    c['total_company'] = total_company
    c['total_member'] = total_member
    c['total_data'] = total_data
    c['total_news'] = total_news
    c['type'] = type
    return render_to_response("account/"+request.lang+"/myfavorite_"+type+".html", c, context_instance=RequestContext(request))


def ajax_more_favorite(request):
    c = {}
    member = request.session.get('member', None)
    if member is None:
        return None
    member_id = request.session["member"]['id']
    type = request.GET.get('type', 'project')
    page = request.GET.get('page', 1)
    pagesize = request.GET.get('pagesize', 12)
    start_record = (int(page)-1) * int(pagesize)
    end_record = int(start_record) + int(pagesize)
    favorites = Favorites.objects.filter(member_id=member_id).order_by("-add_time")
    favorites_project = favorites.filter(type_relation=TypeFavorite.project, project__status=StatusProject.approved)
    favorites_demand = favorites.filter(type_relation=TypeFavorite.demand, demand__status=StatusDemand.approved)
    favorites_company = favorites.filter(type_relation=TypeFavorite.company)
    favorites_member = favorites.filter(type_relation=TypeFavorite.member)
    favorites_data = favorites.filter(type_relation=TypeFavorite.data)
    favorites_news = favorites.filter(type_relation=TypeFavorite.news)
    f_list = {"project": favorites_project, "demand": favorites_demand, "company": favorites_company, "member": favorites_member,"news": favorites_news, "data": favorites_data}
    c['favorites'] = f_list.get(type, favorites_project)[start_record:end_record]
    return render_to_response("account/"+request.lang+"/more_favorite_"+type+".html", c, context_instance=RequestContext(request))

def addfavorite(request, type):
    member_id = request.session["member"]['id']
    member = Member.objects.get(pk=member_id)
    id = request.POST.get('id', 0)
    if type == "member":
        reciver = Member.objects.get(pk=id)
        member.add_member_to_favorites(reciver)
        write_member_favorite_log(request,member,reciver)

    elif type == "project":
        project = Project.objects.get(pk=id)
        member.add_project_to_favorites(project)
        write_project_favorite_log(request,member,project)

    elif type == "demand":
        demand = Demand.objects.get(pk=id)
        member.add_demand_to_favorites(demand)
        write_demand_favorite_log(request,member,demand)

    elif type == "company":
        company = Company.objects.get(pk=id)
        member.add_company_to_favorites(company)
        write_company_favorite_log(request,member,company)

    elif type == "news":
        news = News.objects.get(pk=id)
        member.add_news_to_favorites(news)
        write_news_favorite_log(request,member,news)

    elif type == "data":
        data = Deal.objects.get(pk=id)
        member.add_data_to_favorites(data)
    return HttpResponse("success")


def removefavorite(request, type):
    member_id = request.session["member"]['id']
    member = Member.objects.get(pk=member_id)
    id = request.POST.get('id', 0)
    if type == "member":
        reciver = Member.objects.get(pk=id)
        member.remove_member_from_favorites(reciver)
        write_member_remove_favorite_log(request,member,reciver)

    elif type == "project":
        project = Project.objects.get(pk=id)
        member.remove_project_from_favorites(project)
        write_project_remove_favorite_log(request,member,project)

    elif type == "demand":
        demand = Demand.objects.get(pk=id)
        member.remove_demand_from_favorites(demand)
        write_demand_remove_favorite_log(request,member,demand)

    elif type == "company":
        company = Company.objects.get(pk=id)
        member.remove_company_from_favorites(company)
        write_company_remove_favorite_log(request,member,company)

    elif type == "news":
        news = News.objects.get(pk=id)
        member.remove_news_from_favorites(news)
        write_news_remove_favorite_log(request,member,news)

    elif type == "data":
        data = Deal.objects.get(pk=id)
        member.remove_data_from_favorites(data)
    return HttpResponse("success")


@member_login_required
def home(request, role_type):
    c = {}
    member_id = request.session["member"]['id']
    industries = {}
    locations = {}
    try:
        p = Preference.objects.get(member_id=member_id)
        industries = p.preference_industry.all()
        locations = p.preference_location.all()
        keywords = p.preference_keyword.all();
    except ObjectDoesNotExist:
        industries = PreferenceIndustry.objects.annotate(dcount=Count('industry')).order_by("-dcount")[0:5]
        locations = PreferenceLocation.objects.annotate(dcount=Count('country')).order_by("-dcount")[0:5]
        # keywords = PreferenceLocation.objects.annotate(dcount=Count('country')).order_by("-dcount")[0:5]
    c['industries'] = industries
    c['locations'] = locations
    if role_type == 'seller':
        request.session["member"]['role'] = u'seller'
        c['title'] = _("Seller Home")
        q1 = Q(status=StatusDemand.approved)
        q2 = Q()
        # if len(keywords) > 0:
        #     for i in keywords:
        #         q2 = q2 | Q(company_industries=i)
        if len(industries) > 0:
            q2 = Q(company_industries=None)
            for i in industries:
                q2 = q2 | Q(company_industries=i.industry_id)
        if len(locations) > 0:
            q2 = q2 | Q(company_countries=None, company_provinces=None, company_cities=None)
            for l in locations:
                if l.city_id:
                    q2 = q2 | Q(company_cities=l.city_id)
                elif l.province_id:
                    q2 = q2 | Q(company_provinces=l.province_id)
                else:
                    q2 = q2 | Q(company_countries=l.country_id)
        if len(q2) > 0:
            q2 = q1 & q2
            demands = Demand.objects.filter(q2).order_by("-id")[0:10]
        else:
            demands = Demand.objects.filter(q1).order_by("-id")[0:10]
        c['data'] = demands
        c['hot_list'] = Demand.objects.order_by("-pv", "-id")[0:5]
    else:
        request.session["member"]['role'] = u'buyer'
        # q1 = Q(is_anonymous=False)
        q1 = Q(status=StatusProject.approved)#, expire_date__gt=datetime.datetime.today, is_suitor=True)
        q2 = Q()
        if len(industries) > 0:
            for i in industries:
                q2 = q2 | Q(company_industry=i.industry_id)
        #Terry 20140904
        if len(locations) > 0:
            for l in locations:
                if l.city_id:
                    q2 = q2 | Q(company_cities=l.city_id)
                elif l.province_id:
                    q2 = q2 | Q(company_province=l.province_id)
                else:
                    q2 = q2 | Q(company_country=l.country_id)
        if len(q2) > 0:
            q2 = q1 & q2
            c['data'] = Project.objects.filter(q2).order_by("-id")[0:10]
        else:
            c['data'] = Project.objects.filter(q1).order_by("-id")[0:10]
        c['hot_list'] = Project.objects.order_by("-pv", "-id")[0:5]
        c['title'] = _("Buyer Home")

    c['member'] = request.session.get('member', None)

    request.session.modified = True

    return render_to_response("account/"+request.lang+"/"+c['member']['role']+".html", c, context_instance=RequestContext(request))


def get_logo(request,width,height,file_name,type):

    allow_size=['30x30','48x48','60x60','64x64','80x80','158x158','180x180','200x200','238x238','480x480']
    file_size=width+'x'+height
    if file_size not in allow_size :
        file_size=allow_size[0]

    file_path = '%s/avatars/%s/' % (MEDIA_ROOT,file_size)
    file_all_name = file_path+'%s' % (file_name)
    file_origin_name='%s/avatars/%s/%s' % (MEDIA_ROOT,'origin',file_name)
    #print file_all_name
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    if os.path.isfile(file_all_name):
        f=open(file_all_name)
    else:
        if os.path.isfile(file_origin_name):
            im=Image.open(file_origin_name)

            im.thumbnail(tuple([int(i) for i in file_size.split('x')]),Image.ANTIALIAS)
            im.save(file_all_name,"JPEG")
            f=open(file_all_name)
        else:
            raise Http404


    return HttpResponse(f, mimetype="image/jpeg")


@csrf_protect
@member_login_required
def get_new_message(request):

    result={'is_ok':0,'error':'','new_message_list':None,'num':0}
    member = request.session.get('member', None)
    if member != None:
        try:
            current_member=Member.objects.get(pk=member['id'])
            messagelist=Message.objects.filter(receiver=current_member,is_read=0,is_delete=0).order_by('-add_time')
            result['is_ok']=1
            result['new_message_list']=serializers.serialize("json",messagelist)
            result['num']=len(messagelist)
        except ObjectDoesNotExist:
            result['error']=ugettext('User is not exist!')

    return HttpResponse(simplejson.dumps(result))

@csrf_protect
@member_login_required
def get_new_message_by_id(request):
    receiver_id=int(request.GET.get('receiver_id',0))
    sender_id=int(request.GET.get('sender_id',0))

    result={'is_ok':0,'error':'','new_message_list':None,'num':0}

    member = request.session.get('member', None)
    if member != None:
        try:
            current_member=Member.objects.get(pk=member['id'])
            other_number=Member.objects.get(pk=receiver_id)
            if sender_id ==current_member.id:
                messagelist = Message.objects.filter(Q(receiver=current_member,sender=other_number,is_delete=0) | Q(receiver=other_number,sender=current_member,is_delete=0)).order_by('add_time')
                format_date = []
                for m in messagelist:
                    if m.receiver_id == current_member.id:
                        m.is_read = True
                        m.save()
                    format_date.append(caculate(m.add_time))
                result['is_ok'] = 1
                result['new_message_list'] = serializers.serialize("json",messagelist)
                result['format_date'] = format_date
                result['num'] = len(messagelist)
            else:
                result['error'] = ugettext('User error!')

        except ObjectDoesNotExist:
            result['error'] = ugettext('User is not exist!')

    return HttpResponse(simplejson.dumps(result))


@csrf_protect
@member_login_required
def get_new_message_num(request):

    result={'is_ok':0,'error':'','num':0}
    member = request.session.get('member', None)
    if member != None:
        try:
            num=Helper.find_not_read_message(member['id'])
            result['is_ok']=1

            result['num']=num
        except ObjectDoesNotExist:
            result['error']=ugettext('User is not exist!')

    return HttpResponse(simplejson.dumps(result))


@csrf_protect
@member_login_required
def get_new_message_html(request):
    c={}
    c['member']=request.session.get('member', None)
    current_member=get_object_or_404(Member,pk=c['member']['id'])
    c['new_message_list']=Message.objects.filter(receiver=current_member,is_read=0,is_delete=0).order_by('-add_time')[0:3]

    return render_to_response("account/"+request.lang+"/newmessage.html", c ,context_instance=RequestContext(request))

@csrf_protect
@member_login_required
def send_message(request):
    result = {'is_ok':0,'message':''}
    if request.is_ajax():
        member = request.session.get('member', None)
        if member != None:
            if request.method == 'POST':
                try:
                    receiver_id = request.POST['recipient_id']  #may be the projectId when receiver_type is 1 or is the demandId when receiver_type is 2
                    receiver_type = request.POST['recipient_type_id']
                    reply_id = request.POST.get('reply_id', None)

                    #member id when reply the message, this is the member id who contact you, only the receiver_type is 1 or 2
                    content = request.POST['content']
                    sender = Member.objects.get(pk=member['id'])
                    receiver = None
                    p = None
                    d = None
                    if receiver_type == '0':
                        receiver = Member.objects.get(pk=receiver_id)
                    elif receiver_type == '1':
                        p = Project.objects.get(pk=receiver_id)
                        if reply_id is not None and reply_id != "":            #while the reply_id is not null, it means it is a reply message
                            receiver = Member.objects.get(pk=reply_id)
                        else:
                            receiver = p.member
                    else:
                        d = Demand.objects.get(pk=receiver_id)
                        if reply_id is not None and reply_id != "":            #while the reply_id is not null, it means it is a reply message
                            receiver = Member.objects.get(pk=reply_id)
                        else:
                            receiver = d.member
                    save_dynamic(sender, 1, receiver.id, sender.fullname + u"给您发了一条消息")
                    #oldmessage_num = Message.objects.filter(content=content,receiver=receiver).count()
                    oldmessage_num = 0
                    if oldmessage_num==0:
                        m=Message()
                        m.sender=sender
                        m.receiver=receiver
                        m.content=content
                        m.add_time=datetime.datetime.now()
                        email_item = None
                        if receiver_type=='1':
                            m.project=p
                            m.type_relation=1
                            email_item=p

                        elif receiver_type=='2':
                            m.demand=d
                            m.type_relation=2
                            email_item=d
                        else:
                            m.type_relation=0
                            
                        m.save()

                        Helper.update_message_log(m)

                        result['is_ok']=1
                        result['message'] = ugettext('Message send success!')
                        message_id = request.POST.get('message_id', False)
                        if message_id and message_id != u"0" and message_id != "0" and message_id != 0:
                            msg = Message.objects.get(pk=message_id)
                            msg.is_read = 1
                            msg.save()

                        #print("%s send message to %s : %s" % (m,receiver,content))
                        send_have_message_email(request, receiver.email, receiver.first_name, email_item, sender)

                    else:
                        result['message']=ugettext("Can't send same message to a receiver!")
                except Exception,ex:
                    logger.error(ex)
                    result['message']=ugettext('Message send fail!')
    return HttpResponse(simplejson.dumps(result))


def send_have_message_email(request, email, name, email_item, sender):
    is_ok=False
    try:
        html_content = loader.render_to_string("account/"+request.lang+"/email_have_message.html", {'item':email_item,'name':name, 'sender_name':sender.first_name, 'sender_company': sender.company.name_cn})
        title = "Newchama未读留言提醒"
        try:
            send_email_by_mq('email','email',title,email,html_content)
        except Exception, e:
            msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()

        is_ok=True
    except Exception,ex:
        logger.error("send_have_message_email error" + ex)
        pass
    
    return is_ok


@csrf_protect
@member_login_required
def read_message(request):
    result={'is_ok':0,'message':''}
    if request.is_ajax():
        member = request.session.get('member', None)
        if member != None:

            if request.method == 'POST':
                message_id = request.POST['message_id']

                try:

                    message=Message.objects.get(pk=message_id)
                    if message.receiver.id==member['id']:

                        message.is_read=1

                        message.save()

                        result['is_ok']=1
                        result['message']=ugettext('Message set read success!')

                    else:
                        result['message']=ugettext("Can't set read  message without receiver!")

                except:
                    result['message']=ugettext('Message is not exist!')

    return HttpResponse(simplejson.dumps(result))

@csrf_protect
@member_login_required
def remove_message(request):
    result={'is_ok':0,'message':''}

    if request.is_ajax():

        member = request.session.get('member', None)
        if member != None:

            if request.method == 'POST':
                message_id = request.POST['message_id']

                try:

                    message=Message.objects.get(pk=message_id)
                    if message.receiver.id==member['id']:


                        message.is_delete=1

                        message.save()

                        result['is_ok']=1
                        result['message']=ugettext('Message remove success!')


                    else:
                        result['message']=ugettext("Can't remove  message without receiver!")

                except:
                    result['message']=ugettext('Message is not exist!')

    return HttpResponse(simplejson.dumps(result))


@csrf_protect
@member_login_required
def remove_message_project(request):
    result={'is_ok':0,'message':''}

    if request.is_ajax():

        member = request.session.get('member', None)
        if member != None:

            if request.method == 'POST':
                message_id = request.POST['message_id']

                try:

                    message=Message.objects.get(pk=message_id)
                    
                    message_list=Message.objects.filter(Q(project=message.project,receiver=message.receiver,sender=message.sender,is_delete=0)|Q(project=message.project,sender=message.receiver,receiver=message.sender,is_delete=0))

                    for m in message_list:
                        m.is_delete=1
                        m.save()

                    result['is_ok']=1
                    result['message']=ugettext('Message remove success!')

                except:
                    result['message']=ugettext('Message is not exist!')

    return HttpResponse(simplejson.dumps(result))


@csrf_protect
@member_login_required
def remove_message_demand(request):
    result={'is_ok':0,'message':''}

    if request.is_ajax():

        member = request.session.get('member', None)
        if member != None:

            if request.method == 'POST':
                message_id = request.POST['message_id']

                try:

                    message=Message.objects.get(pk=message_id)
                    message_list=Message.objects.filter(Q(demand=message.demand,receiver=message.receiver,sender=message.sender,is_delete=0)|Q(demand=message.demand,sender=message.receiver,receiver=message.sender,is_delete=0))

                    for m in message_list:
                        m.is_delete=1
                        m.save()

                    result['is_ok']=1
                    result['message']=ugettext('Message remove success!')

                except:
                    result['message']=ugettext('Message is not exist!')

    return HttpResponse(simplejson.dumps(result))


@csrf_protect
@member_login_required
def remove_message_person(request):
    result={'is_ok':0,'message':''}

    if request.is_ajax():

        member = request.session.get('member', None)
        if member != None:

            if request.method == 'POST':
                message_id = request.POST['message_id']

                try:

                    message=Message.objects.get(pk=message_id)
                    message_list=Message.objects.filter(Q(receiver=message.receiver,sender=message.sender,is_delete=0)|Q(sender=message.receiver,receiver=message.sender,is_delete=0))

                    for m in message_list:
                        m.is_delete=1
                        m.save()

                    result['is_ok']=1
                    result['message']=ugettext('Message remove success!')

                except:
                    result['message']=ugettext('Message is not exist!')

    return HttpResponse(simplejson.dumps(result))


@csrf_protect
@member_login_required
def remove_message_project_all(request):
    result={'is_ok':0,'message':''}

    if request.is_ajax():

        member = request.session.get('member', None)
        if member != None:

            if request.method == 'POST':
                
                message_list = request.POST['message_list_up'].split(',')

                try:
                    for message_id in message_list:
                        message=Message.objects.get(pk=int(message_id))

                        if message.type_relation==1:
                            message_list=Message.objects.filter(Q(receiver=message.receiver,sender=message.sender,is_delete=0,project=message.project)|Q(sender=message.receiver,receiver=message.sender,is_delete=0,project=message.project))

                            for m in message_list:
                                m.is_delete=1
                                m.save()
                        elif message.type_relation==2:
                            message_list=Message.objects.filter(Q(receiver=message.receiver,sender=message.sender,is_delete=0,demand=message.demand)|Q(sender=message.receiver,receiver=message.sender,is_delete=0,demand=message.demand))

                            for m in message_list:
                                m.is_delete=1
                                m.save()


                    result['is_ok']=1
                    result['message']=ugettext('Message remove success!')

                except:
                    result['message']=ugettext('Message is not exist!')
                
                    
    return HttpResponse(simplejson.dumps(result))


@csrf_protect
@member_login_required
def remove_message_person_all(request):
    result={'is_ok':0,'message':''}

    if request.is_ajax():

        member = request.session.get('member', None)
        if member != None:

            if request.method == 'POST':
                
                message_list = request.POST['message_list_up'].split(',')

                try:
                    for message_id in message_list:
                        message=Message.objects.get(pk=int(message_id))
                        message_list=Message.objects.filter(Q(receiver=message.receiver,sender=message.sender,is_delete=0)|Q(sender=message.receiver,receiver=message.sender,is_delete=0))

                        for m in message_list:
                            m.is_delete=1
                            m.save()

                    result['is_ok']=1
                    result['message']=ugettext('Message remove success!')

                except:
                    result['message']=ugettext('Message is not exist!')
                
                    
    return HttpResponse(simplejson.dumps(result))

@csrf_protect
@member_login_required
def send_invitecode(request):

    result={'is_ok':0,'message':''}

    if request.is_ajax():

        member = request.session.get('member', None)
        if member != None:
            print str(member)
            if request.method == 'POST':
                email = request.POST['invite_email']

                try:
                    #sender = Member.objects.get(pk=member['id'])

                    #invite =InviteCode()
                    #invite.invite_user=sender
                    #invite.email=email
                    #invite.code = str(random.randint(0,99999999)).zfill(8)
                    #invite.save()
                    mail_dic = dict()
                    mail_dic['username'] = member['username']
                    mail_dic['company_name'] = member['company_name']

                    html_content = loader.render_to_string("account/"+request.lang+"/email_invite.html",mail_dic)
                    
                    title=ugettext('NewChama InviteCode Message')
                    try:
                       
                        send_email_by_mq('email','email',title,email,html_content)

                    except Exception, e:
                        msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [email])
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()


                    result['is_ok']=1
                    result['message']=ugettext('Invite send success!')

                except Exception, e:
                    result['message']=ugettext('Invite send fault!')


    return HttpResponse(simplejson.dumps(result))


def _upload_member_avatar(f, id):
    c = {}
    file_name = ""
    msg = ""
    result = False
    path = settings.MEDIA_ROOT + "/avatars/origin/"
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        file_ext = os.path.splitext(f.name)[1]
        if file_ext.lower() != '.jpg':
            msg = _("avatar file format not jpg")
        else:
            file_name = str(id) + file_ext
            destination = open(path + file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            result = True
            msg = _("success")
    except Exception, e:
        msg = e.message
    c['file_name'] = file_name
    c['msg'] = msg
    c['result'] = result
    return c

'''
@member_login_required
def search_company(request):
    c = {}
    c.update(request)
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    is_search = request.GET.get("is_search", "")
    if is_search == '1':
        companies = Company.objects.all()
        keyword = request.GET.get("keyword", "")
        country = request.GET.get("country", "")
        industry_first = request.GET.get("industry_first", "")
        industry_second = request.GET.get("industry_second", "")
        industry_third = request.GET.get("industry_third", "")
        if keyword != "":
            companies = companies.filter(Q(short_name_cn__contains=keyword) | Q(short_name_en__contains=keyword))
            c["keyword"] = keyword
        country_id = 0
        if _is_has_condition(country):
            country_id = int(country)
            c["country"] = country_id
            companies = companies.filter(country_id=country_id)
        industry = ""
        if _is_has_condition(industry_first):
            industry = industry_first
            c["industry_first"] = int(industry_first)
        if _is_has_condition(industry_second):
            industry = industry_second
            c["industry_second"] = int(industry_second)
        if _is_has_condition(industry_third):
            industry = industry_third
            c["industry_third"] = int(industry_third)
        if industry != "":
            industry_condition = Industry.objects.get(pk=industry)
            companies = companies.filter(Q(industry=industry_condition) | Q(industry__father=industry_condition) | Q(industry__father__father=industry_condition))
        c['companies'] = companies
        c['is_search'] = True
    c["countries"] = Country.objects.all().order_by('name_en', 'name_cn')
    c["industries"] = Industry.objects.filter(level=1)
    return render_to_response("account/"+request.lang+"/search_company.html", c, context_instance=RequestContext(request))

@member_login_required
def search_keyword_company(request, keyword):
    c = {}
    c['member'] = request.session.get('member', None)
    c["keyword"] = keyword
    companies = Company.objects.filter(Q(short_name_cn__contains=keyword) | Q(short_name_en__contains=keyword)).order_by("-id")
    c['companies'] = companies
    c['total_project'] = Project.objects.filter(Q(status=StatusProject.approved) & (Q(name_cn__contains=keyword) | Q(name_en__contains=keyword))).count()
    c['total_demand'] = Demand.objects.filter(Q(status=StatusDemand.approved) & (Q(name_cn__contains=keyword) | Q(name_en__contains=keyword))).count()
    c['total_news'] = News.objects.filter(Q(title__contains=keyword) | Q(tag__contains=keyword)).count()
    c['total_company'] = companies.count()
    c['total_member'] = Member.objects.filter(Q(last_name__contains=keyword) | Q(first_name__contains=keyword)).count()
    return render_to_response("account/"+request.lang+"/search_keyword_company.html", c, context_instance=RequestContext(request))

@member_login_required
def search_keyword_member(request, keyword):
    c = {}
    c['member'] = request.session.get('member', None)
    c["keyword"] = keyword
    members = Member.objects.filter(Q(last_name__contains=keyword) | Q(first_name__contains=keyword)).order_by("-id")
    c['members'] = members
    c['total_project'] = Project.objects.filter(Q(status=StatusProject.approved) & (Q(name_cn__contains=keyword) | Q(name_en__contains=keyword))).count()
    c['total_demand'] = Demand.objects.filter(Q(status=StatusDemand.approved) & (Q(name_cn__contains=keyword) | Q(name_en__contains=keyword))).count()
    c['total_news'] = News.objects.filter(Q(title__contains=keyword) | Q(tag__contains=keyword)).count()
    c['total_company'] = Company.objects.filter(Q(short_name_cn__contains=keyword) | Q(short_name_en__contains=keyword)).count()
    c['total_member'] = members.count()
    return render_to_response("account/"+request.lang+"/search_keyword_member.html", c, context_instance=RequestContext(request))

@member_login_required
def search_member(request):
    c = {}
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    is_search = request.GET.get("is_search", "")
    if is_search == '1':
        members = Member.objects.all()
        keyword = request.GET.get("keyword", "")
        country = request.GET.get("country", "")
        industry_first = request.GET.get("industry_first", "")
        industry_second = request.GET.get("industry_second", "")
        industry_third = request.GET.get("industry_third", "")
        if keyword != "":
            members = members.filter(Q(first_name__contains=keyword) | Q(last_name__contains=keyword))
            c["keyword"] = keyword
        country_id = 0
        if _is_has_condition(country):
            country_id = int(country)
            c["country"] = country_id
            members = members.filter(company__country_id=country_id)
        industry = ""
        if _is_has_condition(industry_first):
            industry = industry_first
            c["industry_first"] = int(industry_first)
        if _is_has_condition(industry_second):
            industry = industry_second
            c["industry_second"] = int(industry_second)
        if _is_has_condition(industry_third):
            industry = industry_third
            c["industry_third"] = int(industry_third)
        if industry != "":
            industry_condition = Industry.objects.get(pk=industry)
            members = members.filter(Q(company__industry=industry_condition) | Q(company__industry__father=industry_condition) | Q(company__industry__father__father=industry_condition))
        c['members'] = members
        c['is_search'] = True
    c["countries"] = Country.objects.all().order_by('name_en', 'name_cn')
    c["industries"] = Industry.objects.filter(level=1)
    return render_to_response("account/"+request.lang+"/search_member.html", c, context_instance=RequestContext(request))
'''

def _is_has_condition(condition):
    return condition != "" and condition != "0"


def first_confirm(request):
    return render_to_response("account/"+request.lang+"/first_confirm.html")


def privacy(request):
    return render_to_response("account/"+request.lang+"/privacy.html")

def user(request):
    return render_to_response("account/"+request.lang+"/user.html")

def gohome(request):
    if request.session.get('member', False):
        return redirect("account.index")
    else:
        return redirect("home.index")

def get_check_code_image(request):    
    image=settings.MEDIA_ROOT+'/img/checkcode.gif'  

    im = Image.open(image)      
    draw = ImageDraw.Draw(im)      
    mp = md5()      
    mp_src = mp.update(str(datetime.datetime.now()))      
    mp_src = mp.hexdigest()      
    rand_str = mp_src[0:4]
    font=ImageFont.truetype(settings.STATICFILES_DIRS[0]+"fonts/Arial.ttf", 24)
    draw.text((0,0), rand_str[0],font=font,fill=random.randint(200, 255))      
    draw.text((20,0), rand_str[1], font=font,fill=random.randint(200, 255))      
    draw.text((40,0), rand_str[2], font=font,fill=random.randint(200, 255))      
    draw.text((60,0), rand_str[3], font=font,fill=random.randint(200, 255))      
    del draw      
    request.session['checkcode'] = rand_str      
    buf = cStringIO.StringIO()      
    im.save(buf, 'gif')      
    return HttpResponse(buf.getvalue(),'image/gif')


# def email_log(request, e_type, e_date, e_title, e_email):
def email_log(request, e_type, e_date, e_title):
    image = settings.BASE_DIR + '/static/img/email/logonew.png'
    im = Image.open(image)
    buf = cStringIO.StringIO()
    im.save(buf, 'png')
    item = {}
    if not e_type:
        e_type = 23
    item["type"] = e_type     #request.GET.get("type", "23")
    item["id"] = 0              #request.GET.get("id", "0")
    item["title"] = e_title   #request.GET.get("title", "")
    item["date"] = e_date       #request.GET.get("d", "")
    e_email = request.GET.get("e", "paul@newchama.com")
    user = Member()
    if e_email:
        try:
            user = Member.objects.get(email=e_email)
        except Exception, e:
            user = Member.objects.get(pk=6)             #paul's member information

    write_email_log(request, user, item)
    return HttpResponse(buf.getvalue(),'image/png')
