# -*- coding: utf-8 -*- 
from django.http import Http404
from django.shortcuts import render,render_to_response, get_object_or_404, redirect, HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext,Context
from django.template.loader import get_template
import os, sys
from newchama import settings
from newchama.helper import member_login_required
from xhtml2pdf import pisa
import StringIO
import datetime
from services.models import Deal,CompanyWithPE,Demand, Country, Industry, Member, Company, StatusDemand, Province, City, DemandAttach, DemandIndustry, InvestmentCompany, DemandOtherTargetCompany, ListedCompany
from services.models import DemandViewLog, Message, DemandViewLog, Favorites, TypeFavorite, DemandVisitor, Project,News, StatusProject,Preference, PreferenceIndustry, PreferenceLocation, PreferenceKeyword
from services.models import ConditionDemand, DemandKeyword, DemandKeywordEn
from services.helper import Helper
from recommond.views import update_project_recommond_list
from recommond.models import RecommondProjectItem
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
import logging
import random
import zipfile
from django.db.models import Q, Sum, connection
from sets import Set as set
from django.utils import simplejson
from log.views import *

logger = logging.getLogger(__name__)


@member_login_required
def addsuccess(request):
    c = {}
    c['title'] = _("Buyer Recommended")
    c['member'] = request.session.get('member', None)

    return render_to_response("purchase/"+request.lang+"/add_success.html", c, context_instance=RequestContext(request))


def _is_has_condition(condition):
    return condition != "" and condition != "0"


@member_login_required
def search(request):
    c = {}
    c.update(request)
    c['title'] = _("Purchase Search")
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    is_search = request.GET.get("is_search", "")

    if is_search == '1':
        is_has_condition = False
        condition = ConditionDemand()
        condition.status = StatusDemand.approved
        demands = Demand.objects.filter(status=StatusDemand.approved)
        keyword = request.GET.get("keyword", "")
        country = request.GET.get("country", "")
        #province = request.GET.get("province", "")
        #city = request.GET.get("city", "")
        type = request.GET.get("type", "")
        industry_first = request.GET.get("industry_first", "")
        industry_second = request.GET.get("industry_second", "")
        industry_third = request.GET.get("industry_third", "")
        if keyword != "":
            c["keyword"] = keyword
            is_has_condition = True
        if type != "":
            c["type"] = int(type)
            is_has_condition = True
        country_id = 0
        #province_id = 0
        #city_id = 0
        if _is_has_condition(country):
            country_id = int(country)
            c["country"] = country_id
            is_has_condition = True
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
            condition.industry = industry_condition
            is_has_condition = True
        condition.country_id = country_id
        condition.keyword = keyword
        condition.type = type
        sort = "time_desc"
        if is_has_condition:
            data, total = find_demands(condition, 1, 5, sort)
            c['has_more'] = total > 5
            c['demands'] = data
            c['favorites_demand_ids'] = Helper.find_member_favorite_demand_ids(member_id)
        c['is_search'] = True
        c['is_has_condition'] = is_has_condition
    c["SERVICE_TYPES"] = Demand.SERVICE_TYPES
    c["countries"] = Helper.find_countries()
    c["industries"] = Helper.find_industries_level1()
    return render_to_response("purchase/"+request.lang+"/search.html", c, context_instance=RequestContext(request))


@member_login_required
def search_keyword(request):
    c = {}
    c['title'] = _("Search")
    keyword = request.GET.get("keyword", '')
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    member = get_object_or_404(Member,pk=member_id)
    c["keyword"] = keyword
    demands = Demand.objects.filter(Q(status=StatusDemand.approved) & (Q(name_cn__contains=keyword) | Q(name_en__contains=keyword)))
    c['demands'] = demands[0:5]
    c['total_project'] = Project.objects.filter(Q(status=StatusProject.approved) & (Q(name_cn__contains=keyword) | Q(name_en__contains=keyword))).count()
    c['total_demand'] = demands.count()
    c['total_news'] = News.objects.filter(Q(title__contains=keyword) | Q(tag__contains=keyword)).count()
    c['total_company'] = Company.objects.filter(Q(short_name_cn__contains=keyword) | Q(short_name_en__contains=keyword)).exclude(id=27).count()
    c['total_member'] = Member.objects.filter(Q(last_name__contains=keyword) | Q(first_name__contains=keyword)).count()
    c['favorites_demand_ids'] = Helper.find_member_favorite_demand_ids(member_id)

    write_search_demand_log(request,member,keyword)
    return render_to_response("purchase/"+request.lang+"/search_keyword.html", c, context_instance=RequestContext(request))


@member_login_required
def new(request):
    c = {}
    c['title'] = _("New Purchase")
    c['member'] = request.session.get('member', None)
    # member_id = request.session['member']['id']
    # demands = Demand.objects.filter(status=StatusDemand.approved)
    # sort = request.GET.get("sort", "time_desc")
    # c['sort'] = sort
    # c[sort] = "active"
    # if sort == "time_desc":
    #     demands = demands.order_by("-id")
    # elif sort == "time_asc":
    #     demands = demands.order_by("id")
    # check the preference is setting
    # pi = PreferenceIndustry.objects.filter(preference__member__id=member_id, preference__title="demand")
    # pn = PreferenceKeyword.objects.filter(preference__member__id=member_id, preference__title="demand")
    # pl = PreferenceLocation.objects.filter(preference__member__id=member_id, preference__title="demand")
    # if len(pi) == 0 and len(pl) == 0 and len(pn) == 0:
    #     c['need_preference'] = True
    #     c['demands'] = demands[0:50]
    # else:
    #     c['need_preference'] = False
    #     c['demands'] = demands[0:10]
    # check finish
    member_id = request.session['member']['id']
    type = request.GET.get('type', 0)
    keyword = request.GET.get('keywords', '')
    country_id = request.GET.get('country_id', 0)
    province_id = request.GET.get('province_id', 0)
    industry_id = request.GET.get('industry_id', 0)
    sort = request.GET.get('sort', 'time_desc')
    condition = ConditionDemand()
    condition.country_id = country_id
    condition.keyword = keyword
    condition.status = StatusDemand.approved
    condition.province_id = province_id
    condition.type = type
    level = 1
    if industry_id != "" and industry_id != "0" and industry_id != 0:
        condition.industry = Industry.objects.get(pk=industry_id)
        level = condition.industry.level
    pagesize = 10
    data, total = find_demands(condition, 1, pagesize, sort)

    c["have_more_data"] = len(data) == int(pagesize)
    c['demands'] = data
    c['favorites_demand_ids'] = Helper.find_member_favorite_demand_ids(member_id)

    c['countries'] = Helper.find_countries()
    c['industries'] = Helper.find_industries_level1()
    c['total'] = total
    return render_to_response("purchase/"+request.lang+"/new.html", c, context_instance=RequestContext(request))


@member_login_required
def banking_genius(request, id_post):
    c = {}
    c['title'] = _("New Purchase")
    c['member'] = request.session.get('member', None)
    try:
        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 10)
        condition = recommendCondiction(request, id_post)
        c["totalRecommend"] = RecommondProjectItem.objects.filter(condition).count()
        c["recommendList"] = list(RecommondProjectItem.objects.filter(condition).order_by('-id'))[page : pagesize]
    except Exception, e:
        logger.error(e.message)
    c["id"] = id_post
    c["countries"] = Helper.find_countries()
    c["industries"] = Helper.find_industries_level1()
    c["project_title"] = Demand.objects.get(pk=id_post).name_cn
    member_id = request.session['member']['id']
    c['favorites_project_ids'] = Helper.find_member_favorite_project_ids(member_id)
    return render_to_response("purchase/"+request.lang+"/banking_genius.html", c, context_instance=RequestContext(request))


@member_login_required
def json_recommend(request):
    c = {}
    id_post = request.POST.get("id", False)
    if request.method == "POST":
        try:
            page = request.POST.get('page', 1)
            pagesize = request.POST.get('pagesize', 10)
            if page <= 1:
                page = 1
            if pagesize <= 1:
                pagesize = 1
            start_record = (int(page)-1) * int(pagesize)
            end_record = int(start_record) + int(pagesize)

            if id_post:
                condition = recommendCondiction(request, id_post)
                c["recommendList"] = list(RecommondProjectItem.objects.filter(condition).order_by('-id'))[start_record : end_record]
                member_id = request.session['member']['id']
                c['favorites_project_ids'] = Helper.find_member_favorite_project_ids(member_id)
        except Exception, e:
            logger.error(e. message)
    return render_to_response("purchase/"+request.lang+"/json_recommend.html", c, context_instance=RequestContext(request))


@member_login_required
def json_recommend_count(request):
    count = 0
    id_post = request.POST.get("id", False)
    if request.method == "POST":
        try:
            if id_post:
                condition = recommendCondiction(request, id_post)
                count = RecommondProjectItem.objects.filter(condition).count()
                print count
        except Exception, e:
            logger.error(e. message)
    return HttpResponse(count)


@member_login_required
def sync_recommond(request):
    result = "success"
    try:
        if request.method == "POST":
            id_post = request.POST.get("id", False)
            if id_post:
                d = Demand.objects.get(pk=id_post)
                project_list=Project.objects.filter(status=2).filter(expire_date__gt=datetime.datetime.now()).order_by('-id')
                update_project_recommond_list(d, project_list)
                result = "success"
    except Exception, e:
        print e.message
        logger.error(e.message)
    return HttpResponse(result)


def recommendCondiction(request, id):
    condition = Q(demand_id=id, is_delete=False)
    condition2 = Q()

    target_location_id = request.POST.get('target_location_id', 0)
    target_industry_id = request.POST.get('target_industry_id', 0)
    target_location_type = request.POST.get('target_location_type', 0)
    if target_location_id != "0" and target_location_id != 0:
        if target_location_type == "province":
            condition2 = condition2 | Q (company_province=target_location_id)
        else:
            condition2 = condition2 | Q (company_country=target_location_id)
    if target_industry_id != "0" and target_industry_id != 0:
        condition2 = condition2 | Q (company_industry=target_industry_id)

    if target_location_id != "0" or target_industry_id != "0":
        p = Project.objects.filter(condition2)
        condition = condition & Q (project=p)

    return condition


def preferenceByMemberId(c, member_id):
    list = []
    preferences = Preference.objects.filter(member_id=member_id, title="demand")[0: 1]
    condition = Q(status=StatusDemand.approved)
    if len(preferences) > 0:
        condition2 = Q()
        p = preferences[0]
        c['preference_demand_id'] = p.id
        preference_project_industries = p.preference_industry.all() #PreferenceIndustry.objects.filter(preference__member__id=member['id'])

        c['pre_demand_indusrtis'] = preference_project_industries
        if len(preference_project_industries) > 0:
            for ppi in preference_project_industries:
                condition2 = condition2 | Q (company_industries=ppi.industry_id)
        preference_project_location = p.preference_location.all()

        c['pre_demand_locations'] = preference_project_location
        if len(preference_project_location):
            for ppl in preference_project_location:
                condition2 = condition2 | Q (company_countries=ppl.country_id)

        condition = condition & condition2
        list = Demand.objects.filter(condition).order_by("-id").distinct()[0: 3]
    return list


def demandByMemberId(member_Id):
    demands = Demand.objects.filter(member_id=member_Id, status=StatusDemand.approved).order_by("-id")[0: 5]
    list_demand = []
    for demand in demands:
        count_message = Message.objects.filter(type_relation=2, demand=demand.id, is_read=0).count()
        count_favor = Favorites.objects.filter(type_relation=1, demand=demand.id).count()
        company_industries = demand.company_industries.all()
        count_company = 0
        count_industry = 0
        if company_industries:
            industry_ids = []
            industry_level_1_id = []
            for c in company_industries:
                industry_ids.append(c.id)
                industry_level = c.level
                industry_id = c.id
                if industry_level == 2:
                    industry_id = c.father_id
                elif industry_level == 3:
                    industry_id = c.father.father_id
                industry_level_1_id.append(industry_id)
            count_company = Company.objects.filter(industry__in=industry_ids, status=1).exclude(id=27).count()
            #start_date = datetime.date(datetime.datetime.today().year, datetime.datetime.today().month - 3, datetime.datetime.today().day)
            start_date = datetime.datetime.today()-datetime.timedelta(days=90)
            count_industry = Deal.objects.filter(cv1__in=industry_level_1_id, happen_date__gt=start_date).count()
        pro = {}
        pro["demand"] = demand
        pro["count_message"] = count_message
        pro["count_favor"] = count_favor
        pro["count_industry"] = count_industry
        pro["count_company"] = count_company
        list_demand.append(pro)
    return list_demand


def countDemandStuffTotal(member_id):
    pvs = Demand.objects.filter(member_id=member_id, status=StatusDemand.approved).aggregate(sum_pv=Sum('pv'))
    messages = 0#Message.objects.filter(type_relation=2, demand__member__id=member_id, is_read=0, is_delete=0).count()
    favorites = Favorites.objects.filter(type_relation=2, demand__member__id=member_id).count()
    cursor = connection.cursor()


    demands = Demand.objects.filter(member_id=member_id, status=StatusDemand.approved)
    industry_ids = []
    industry_ids_cv1 = []
    if demands:
        for d in demands:
            for cv1 in d.demand_industries.all():
                industry_ids_cv1.append(cv1.cv1)
            for industry in d.company_industries.all():
                industry_ids.append(industry.id)
    recommend_companies = Company.objects.filter(industry__in=set(industry_ids), status=1).exclude(id=27).count()

    #start_date = datetime.date(datetime.datetime.today().year, datetime.datetime.today().month - 3, datetime.datetime.today().day)
    start_date = datetime.datetime.today()-datetime.timedelta(days=90)
    recommend_industries = Deal.objects.filter(cv1__in=set(industry_ids_cv1), happen_date__gt=start_date).count()
    count_demand_all = {}
    count_demand_all["pvs"] = pvs["sum_pv"]
    count_demand_all["messages"] = messages
    count_demand_all["favorites"] = favorites
    count_demand_all["recommend_companies"] = recommend_companies
    count_demand_all["recommend_industries"] = recommend_industries
    return count_demand_all


@csrf_exempt
@member_login_required
def json_index(request):
    c = {}
    member_id = request.session['member']['id']
    if request.method == 'POST':
        try:
            condition = Q(status=StatusDemand.approved)
            condition2 = Q()
            industryIds = request.GET.get("industryId", False)
            if industryIds and industryIds != "0":
                ids = industryIds.split(",")
                for id in ids:
                    condition2 = condition2 | Q(company_industries=id)

            locationIds = request.GET.get("locationId", False)
            if locationIds and locationIds != "0":
                ids = locationIds.split(",")
                for id in ids:
                    condition2 = condition2 | Q(company_countries=id)
            condition = condition & condition2

            if industryIds == False and locationIds == False:
                result_list = preferenceByMemberId(c, member_id)
            else:
                result_list = Demand.objects.filter(condition).order_by("-id").distinct()[0 : 3]

            c["result_list"] = result_list
            list_demand_preference_plus = 3 - len(result_list)
            if list_demand_preference_plus > 0:
                c['recent_demand'] = Demand.objects.filter(status=StatusDemand.approved).order_by("-id")[0: list_demand_preference_plus]
        except Exception, e:
            # print e.message
            logger.error('show demand json error!' + e.message)
    c['favorites_demand_ids'] = Helper.find_member_favorite_demand_ids(member_id)
    return render_to_response("purchase/"+request.lang+"/json_index.html", c, context_instance=RequestContext(request))


def countResult(result):
    resultList = {}
    # total_recommends = RecommondItem.objects.filter(is_delete=0, project__id=result.id).count()
    total_favorites = Favorites.objects.filter(type_relation=2, demand__id=result.id).count()
    not_read_messages = Message.objects.filter(type_relation=2, demand__id=result.id, is_read=0).count()
    resultList['total_recommends'] = RecommondProjectItem.objects.filter(demand=result, project__status=StatusProject.approved).count()
    resultList['total_target'] = 0
    resultList['total_favorites'] = total_favorites
    resultList['not_read_messages'] = not_read_messages
    resultList['id'] = result.id
    resultList['name_cn'] = result.name_cn
    resultList['name_en'] = result.name_en
    resultList['status'] = result.status
    resultList['statusName'] = result.get_status_display
    resultList['processName'] = result.get_process_display
    resultList['add_time'] = result.add_time
    resultList['pvs'] = result.pv
    resultList['integrity'] = result.integrity
    return resultList


@member_login_required
def mylist(request, type):
    c = {}
    c.update(request)
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    demands = Demand.objects.filter(member_id=member_id).exclude(status=StatusDemand.deleted).order_by("-id")
    c['total_all'] = demands.count()
    result_list_2 = []
    for result in demands:
        result_list_2.append(countResult(result))
    c['demands'] = result_list_2
    c[type] = "active"
    c['type'] = type
    '''
    demands_release = demands.filter(status=StatusDemand.approved)
    demands_draft = demands.filter(status=StatusDemand.draft)
    demands_pending = demands.filter(status=StatusDemand.pending)
    demands_not_approved = demands.filter(status=StatusDemand.not_approved)
    demands_offline = demands.filter(status=StatusDemand.offline)
    demands_expired = demands.filter(expire_date__gt=datetime.datetime.today).exclude(status=StatusDemand.deleted)
    d_list = {"release": demands_release, "draft": demands_draft, "pending": demands_pending, "not_approved": demands_not_approved, "expired": demands_expired}
    d_list.update({"offline": demands_offline, "all": demands})
    result_list = d_list.get(type, demands)
    result_list_2 = []
    for result in result_list:
        result_list_2.append(countResult(result))
    c['result_list'] = result_list_2
    total_all = demands.count()
    total_release = demands_release.count()
    total_pending = demands_pending.count()
    total_draft = demands_draft.count()
    total_offline = demands_offline.count()
    total_not_approved = demands_not_approved.count()
    c['total_all'] = total_all
    c['total_release'] = total_release
    c['total_pending'] = total_pending
    c['total_offline'] = total_offline
    c['total_not_approved'] = total_not_approved
    c['total_draft'] = total_draft
    total_project = Project.objects.filter(member_id=member_id).exclude(status=StatusDemand.deleted).count()
    c['total_project'] = total_project
    c[type] = "active"
    c['type'] = type
    c['demands'] = result_list_2
    '''
    return render_to_response("purchase/"+request.lang+"/mylist.html", c, context_instance=RequestContext(request))

'''
@member_login_required
def mylist(request, type, id=0):
    c = {}
    c.update(request)
    c['title'] = _("My Purchases")
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    demands = Demand.objects.filter(member_id=member_id).exclude(status=StatusDemand.deleted).order_by("-update_time")
    demands_public = demands.filter(target_members=None, target_companies=None, target_industries=None)
    demands_private = demands.exclude(target_members=None, target_companies=None, target_industries=None)
    demands_release = demands.filter(status=StatusDemand.approved)
    demands_draft = demands.filter(status=StatusDemand.draft)
    demands_pending = demands.filter(status=StatusDemand.pending)
    demands_not_approved = demands.filter(status=StatusDemand.not_approved)
    demands_offline = demands.filter(status=StatusDemand.offline)
    demands_expired = demands.filter(expire_date__gt=datetime.datetime.today).exclude(status=StatusDemand.deleted)
    d_list = {"release": demands_release, "draft": demands_draft, "pending": demands_pending, "not_approved": demands_not_approved, "expired": demands_expired}
    d_list.update({"offline": demands_offline, "all": demands, "public": demands_public, "private": demands_private})
    result_list = d_list.get(type, demands)
    total = result_list.count()
    c['total'] = total
    total_all = demands.count()
    total_public = demands_public.count()
    total_private = demands_private.count()
    total_draft = demands_draft.count()
    c['total_all'] = total_all
    c['total_public'] = total_public
    c['total_private'] = total_private
    c['total_draft'] = total_draft
    total_project = Project.objects.filter(member_id=member_id).exclude(status=StatusDemand.deleted).count()
    c['total_project'] = total_project
    if total == 0:
        return render_to_response("purchase/"+request.lang+"/mylist_empty.html", c, context_instance=RequestContext(request))
    ids = []
    for m in result_list:
        ids.append(m.id)
    id_current = int(id)
    if id_current == 0:
        demand = result_list[0]
        id_current = demand.id
    else:
        if id_current not in ids:
            raise Http404
        pageIndex = ids.index(id_current)+1
        demand = result_list[pageIndex-1]
    pageIndex = ids.index(id_current)+1
    #c['result_list'] = result_list
    pageTotal = total
    c['pageTotal'] = pageTotal
    page_start = 1
    page_end = 10
    if pageIndex >= 5:
        page_start = pageIndex - 4
        page_end = pageIndex + 5
    if page_end > pageTotal:
        page_end = pageTotal
    pages = ids[page_start-1:page_end]
    id_list_top = enumerate(pages, start=page_start)
    id_list = enumerate(pages, start=page_start)
    c['id_list_top'] = id_list_top
    c['id_list'] = id_list
    c['page_start'] = page_start
    c['page_end'] = page_end
    c[type] = "active"
    c['type'] = type
    c['d'] = demand
    c['pageIndex'] = pageIndex
    c['id_current'] = id_current
    c['first_id'] = ids[0]
    c['end_id'] = ids[total-1]
    if pageIndex > 1:
        c['pre_id'] = ids[pageIndex-1]
    if pageIndex < pageTotal:
        c['next_id'] = ids[pageIndex]
    if page_end < pageTotal:
        c['next_id_page_end'] = ids[page_end]
    visitors = DemandVisitor.objects.filter(demand_id=demand.id).order_by("-add_time")
    c['visitors'] = visitors
    c['visitors_count'] = visitors.count()
    followers = Favorites.objects.filter(demand_id=demand.id).order_by("-add_time")
    c['followers'] = followers
    message_list = Message.objects.filter(demand_id=demand.id).order_by("-add_time")
    c['message_list'] = message_list
    
    if len(demand.company_industries.all())>0:
        #之后用cv1替代
        if demand.company_industries.all()[0].level==3:
            c['deal_list_more_id']=demand.company_industries.all()[0].father.father.id

        elif demand.company_industries.all()[0].level==2:
            c['deal_list_more_id']=demand.company_industries.all()[0].father.id
            
        else:
            c['deal_list_more_id']=demand.company_industries.all()[0].id

        c['deal_list'] =Deal.objects.filter(cv1=c['deal_list_more_id']).order_by('-update_time')[0:10]

        c['compare_cn']= CompanyWithPE.objects.filter(country__name_en='China',industry__id=c['deal_list_more_id']).order_by('-ps')[0:5]
        
        c['compare_usa']= CompanyWithPE.objects.filter(country__name_en='United States of America',industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]
        
        c['compare_hk']= CompanyWithPE.objects.filter(country__name_en='Hong Kong',industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]
        
        c['compare_uk']= CompanyWithPE.objects.filter(country__name_en='United Kingdom',industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]

    return render_to_response("purchase/"+request.lang+"/mylist.html", c, context_instance=RequestContext(request))
'''

@member_login_required
def mydetail(request, id):
    c = {}
    member = request.session.get('member', None)
    c['member'] = member
    member_id = request.session['member']['id']
    demand = get_object_or_404(Demand, pk=id, member_id=member_id)

    # c['d'] = demand
    m = countResult(demand)
    c['process'] = Demand.PROCESS
    c['d'] = m
    _visitors = DemandVisitor.objects.filter(demand_id=demand.id).order_by("-add_time")[0:8]
    visitors=[]
    c['recommendList'] = RecommondProjectItem.objects.filter(demand=demand, project__status=StatusProject.approved).order_by("project__update")[0:5]
    for v in _visitors:
        if v.member.email.find('@newchama.com')==-1:
            visitors.append(v)
    
    c['visitors'] = visitors
    c['visitors_count'] = len(visitors)
    followers = Favorites.objects.filter(demand_id=demand.id).order_by("-add_time")
    c['followers'] = followers
    message_list = Message.objects.filter(demand_id=demand.id).order_by("-add_time")
    c['message_list'] = message_list
    if len(demand.company_industries.all()) > 0:
        #之后用cv1替代
        if demand.company_industries.all()[0].level == 3:
            c['deal_list_more_id'] = demand.company_industries.all()[0].father.father.id

        elif demand.company_industries.all()[0].level == 2:
            c['deal_list_more_id'] = demand.company_industries.all()[0].father.id

        else:
            c['deal_list_more_id'] = demand.company_industries.all()[0].id

        c['deal_list'] = Deal.objects.filter(cv1=c['deal_list_more_id']).order_by('-update_time')[0:10]

        c['compare_cn'] = CompanyWithPE.objects.filter(country__name_en='China', industry__id=c['deal_list_more_id']).order_by('-ps')[0:5]

        c['compare_usa'] = CompanyWithPE.objects.filter(country__name_en='United States of America', industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]

        c['compare_hk'] = CompanyWithPE.objects.filter(country__name_en='Hong Kong', industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]

        c['compare_uk'] = CompanyWithPE.objects.filter(country__name_en='United Kingdom', industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]
    return render_to_response("purchase/"+request.lang+"/mydetail.html", c, context_instance=RequestContext(request))


def ajax_more(request):
    c = {}
    member = request.session.get('member', None)
    if member is None:
        return None
    member_id = request.session['member']['id']
    page = request.GET.get('page', 1)
    pagesize = request.GET.get('pagesize', 10)
    type = request.GET.get('type', 0)
    keyword = request.GET.get('keywords', '')
    country_id = request.GET.get('country_id', 0)
    province_id = request.GET.get('province_id', 0)
    industry_id = request.GET.get('industry_id', 0)
    sort = request.GET.get('sort', 'time_desc')
    condition = ConditionDemand()
    condition.country_id = country_id
    condition.keyword = keyword
    condition.status = StatusDemand.approved
    condition.province_id = province_id
    condition.type = type
    level = 1
    if industry_id != "" and industry_id != "0" and industry_id != 0:
        condition.industry = Industry.objects.get(pk=industry_id)
        level = condition.industry.level
    data, total = find_demands(condition, page, pagesize, sort)

    c['demands'] = data
    c["have_more_data"] = len(data) == int(pagesize)
    c['favorites_demand_ids'] = Helper.find_member_favorite_demand_ids(member_id)
    return render_to_response("purchase/"+request.lang+"/ajax_list.html", c, context_instance=RequestContext(request))


@member_login_required
@csrf_protect
def add(request):
    c = {}
    c.update(csrf(request))
    c['title'] = _("Add Purchase")
    c['member'] = request.session.get('member', None)
    u = Demand()
    u.valid_day = 60
    # if request.method == "POST":
    #     u = Demand()
    #     name_en = request.POST["name_en"]
    #     name_cn = request.POST["name_cn"]
    #     if name_en == "" and name_cn == "":
    #         isvalid = False
    #         messages.warning(request, _("please input demand name"))
    #     submitStatus = request.POST["submitStatus"]
    #     redirect_url = "purchase.mylist_pending"
    #     if submitStatus == "draft":
    #         u.status = StatusDemand.draft
    #         redirect_url = "purchase.mylist_draft"
    #     else:
    #         u.status = StatusDemand.pending
    #     _bind_data(request, u)
    #     if isvalid:
    #         try:
    #             u.financial_year = datetime.datetime.today().year
    #             u.save()
    #             _save_items(request, u)
    #             return redirect(redirect_url)
    #         except Exception, e:
    #             messages.warning(request, e.message)
    #             logging.error(e.message)
    c['target_companies_count'] = 0
    c["u"] = u
    c['readSuitorRelate'] = False
    _load_types(c)
    return render_to_response("purchase/"+request.lang+"/add.html", c, context_instance=RequestContext(request))


@member_login_required
@csrf_protect
def edit(request, id):
    c = {}
    c.update(csrf(request))
    c['title'] = _("Edit Purchase")
    c['member'] = request.session.get('member', None)
    member_id = c['member']['id']
    isvalid = True
    u = get_object_or_404(Demand, pk=id, member_id=member_id)
    c['attachments'] = u.demand_attach.all()
    c['u'] = u

    c["other_target_companies"] = DemandOtherTargetCompany.objects.filter(demand__id=u.id)
    countrySelected = u.company_countries.all()
    if countrySelected:
        c['company_country'] = countrySelected[0]
    provinceSelected = u.company_provinces.all()
    if provinceSelected:
        c['company_province'] = provinceSelected[0]
    industrySelected = u.demand_industries.all()
    if industrySelected:
        c['company_industry'] = industrySelected[0]
    c['target_companies_count'] = u.target_companies.all().count()
    c['readSuitorRelate'] = True
    if request.lang == "en-us":
        mks = u.demand_keyword_en.all()
    else:
        mks = u.demand_keyword.all()
    c['mks'] = mks
    keywords = ""
    if len(mks) > 0:
        for m in mks:
            keywords += m.keyword + ","
        keywords = keywords[0 : len(keywords) - 1]
    c['keywords'] = keywords
    _load_types(c)
    member = get_object_or_404(Member,id=member_id)
    write_demand_edit_log(request,member,u)
    return render_to_response("purchase/"+request.lang+"/add.html", c, context_instance=RequestContext(request))


@member_login_required
def detail(request, id):
    c = {}
    c['title'] = _("Purchase Detail")
    member = request.session.get('member', None)
    c['member'] = member
    member_id = request.session['member']['id']
    if Helper.hasAgentRole(member['company_type']):
        messages.warning(request, _("You have no permission to visit this page"))
        return render_to_response("services/error_message.html", c, context_instance=RequestContext(request))
    demand = get_object_or_404(Demand, pk=id)
    if demand.status != StatusDemand.approved and demand.member_id != member_id:
        raise Http404
    if demand.is_suitor:
        if demand.is_push_to_member(member) is False and demand.member_id != member_id:
            messages.warning(request, _("not target"))
            return render_to_response("services/error_message.html", c, context_instance=RequestContext(request))
            # return HttpResponse(_("not target"))
    c['d'] = demand
    #c['last_year'] = demand.financial_year-1

    #demands_other = Demand.objects.filter(member_id=demand.member_id, status=StatusDemand.approved, is_anonymous=False).exclude(id=id)[0:5]
    #c['demands_other'] = demands_other
    #demands_recommend = Demand.objects.filter(service_type=demand.service_type, status=StatusDemand.approved).exclude(id=id).order_by("-pv")[0:5]
    #c['demands_recommend'] = demands_recommend
    c['message_list'] = Message.objects.filter(type_relation=2, demand=demand, is_delete=0).order_by('-add_time')
    if demand.member_id == member_id:
        c['is_own'] = True
    member = Member.objects.get(id=member_id)
    member.view_demand(demand)

    if request.lang == "en-us":
        mks = demand.demand_keyword_en.all()
    else:
        mks = demand.demand_keyword.all()

    keywords = ""
    if len(mks) > 0:
        for m in mks:
            keywords += m.keyword + ","
        keywords = keywords[0 : len(keywords) - 1]
    c['keywords'] = keywords

    c['is_added_favorite'] = member.is_added_demand_to_favorites(demand)
    c['is_expired']=datetime.date.today() > demand.expire_date

    url = "/detail.html"
    type = request.GET.get("type", "")
    c['type'] = type
    if type == "1":
        url = "/view.html"
    else:
        write_demand_view_log(request,member,demand, type)
    return render_to_response("purchase/"+request.lang+ url, c, context_instance=RequestContext(request))


@member_login_required
def pdf(request, id):
    reload(sys)
    sys.setdefaultencoding('utf8')
    c = {}
    c['title'] = _("Purchase Detail")
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    demand = get_object_or_404(Demand, pk=id)
    member = Member.objects.get(pk=member_id)
    if demand.status != StatusDemand.approved and demand.member_id != member_id:
        raise Http404
    if demand.is_suitor:
        if demand.is_push_to_member(member) is False and demand.member_id != member_id:
            return HttpResponse(_("not target"))
    c['d'] = demand
    c['last_year'] = demand.financial_year-1
    c['static_root'] = settings.STATICFILES_DIRS[0]
    template = get_template("purchase/"+request.lang+"/detail_pdf.html")
    html = template.render(Context(c))

    #print(html)
    file = StringIO.StringIO()
    #file = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file)

    # Return PDF document through a Django HTTP response
    file.seek(0)
    pdf = file.read()
    file.close()            # Don't forget to close the file handle
    member.print_demand(demand)
    write_demand_teaser_view_log(request,member,demand)
    return HttpResponse(pdf, mimetype='application/pdf')


@member_login_required
def save(request):
    response_data = {}
    response_data['result'] = 'failed'
    if request.method == "POST":
        try:
            name_en = request.POST["name_en"]
            name_cn = request.POST["name_cn"]
            if name_en == "" and name_cn == "":
                response_data['message'] = _("please input demand name")
            else:
                #check stock_symbol is correct
                company_stock_symbol = request.POST.get("company_stock_symbol", False)
                is_list_company = int(request.POST.get("is_list_company", 0))
                if company_stock_symbol and is_list_company == 1:
                    checksymbolExsit = ListedCompany.objects.filter(stock_symbol=company_stock_symbol)
                    if len(checksymbolExsit) == 0:
                        response_data['message'] = 'symbolNotExsit'
                        return HttpResponse(simplejson.dumps(response_data), content_type="text/plain")
                submitStatus = request.POST["submitStatus"]
                u = Demand()
                isExsit = False
                id_post = request.POST.get("id", False)
                #check the demand is exsit with member_id
                condition = Q(member_id=request.session["member"]["id"])
                condition2 = Q()
                if id_post:
                    condition = condition & ~Q(pk=id_post)
                if name_cn.strip() != "":
                    condition2 = condition2 | Q(name_cn=name_cn.strip())

                if name_en.strip() != "":
                    condition2 = condition2 | Q(name_en=name_en.strip())

                project = Demand.objects.filter(condition & condition2)
                if project:
                    isExsit = True
                    response_data['message'] = "demandExsit"

                if isExsit is False:
                    if id_post:
                        u = Demand.objects.get(pk=id_post)
                    if u.status != StatusDemand.approved:               #Terry mark, when the project is approved then do not reset the pending status
                        if submitStatus == "draft":
                            u.status = StatusDemand.draft
                        else:
                            u.status = StatusDemand.pending
                    bool, msg = _bind_data(request, u)
                    if bool:
                        response_data['result'] = 'success'
                        response_data['id'] = u.id
                        response_data['message'] = '操作成功'
                    else:
                        response_data['message'] = msg

        except Exception, e:
            logger.error(e.message)
            response_data['message'] = e.message
    return HttpResponse(simplejson.dumps(response_data), content_type="text/plain")

def _load_types(c):
    c["current_year"] = datetime.datetime.today().year
    c["last_year"] = datetime.datetime.today().year-1
    c["FINANCIAL_TYPES"] = Demand.FINANCIAL_TYPES
    c["FINANCIAL_TYPES_2"] = Demand.FINANCIAL_TYPES_2
    c["STOCK_STRUCTURE_PERCENTAGE_TYPES"] = Demand.STOCK_STRUCTURE_PERCENTAGE_TYPES
    c["CURRENCY_TYPES"] = Demand.CURRENCY_TYPES
    c["EMPLOYEES_COUNT_TYPES"] = Demand.EMPLOYEES_COUNT_TYPES
    c["SERVICE_TYPES"] = Demand.SERVICE_TYPES
    c["SERVICE_TYPES_2"] = Demand.SERVICE_TYPES_2
    c["countries"] = Helper.find_countries()
    c["industries"] = Helper.find_industries_level1()
    c["members"] = Member.objects.all()
    c["companies"] = Company.objects.all().exclude(id=27)


def _bind_data(request, u):
    has_attach = False
    upload_types = request.POST.getlist("upload_types", [])
    for ut in upload_types:
        uf = request.FILES.get("upload_file_" + ut, False)
        if uf:
            file_ext = os.path.splitext(uf.name)[1].lower()
            if uf.size > 20000000:
                return False, "tooBig"
                #return _("The file cannot be more than 20M")
            if file_ext != ".doc" and file_ext != ".docx" and file_ext != ".pdf" and file_ext != ".ppt" and file_ext != ".pptx":
                return False, "typeError"
                #return _("The file must be 'doc|docx|pdf'")
            has_attach = True

    integrity = 0
    u.name_cn = request.POST.get("name_cn", None)
    u.name_en = request.POST.get("name_en", None)
    if request.POST.get("name_cn", False) or request.POST.get("name_en", False):
        integrity = integrity + 1

    if request.POST.get("service_type", False):
        u.service_type = request.POST["service_type"]
        integrity = integrity + 1

    pay_currency = request.POST.get("pay_currency", False)
    if pay_currency and pay_currency != "":
        u.pay_currency = pay_currency.replace(",", "")
        integrity = integrity + 1

    u.is_list_company = int(request.POST.get("is_list_company", 0))
    integrity = integrity + 1

    project_relation = request.POST.get("project_relation", False)
    if project_relation and project_relation != "":
        u.project_relation = project_relation.replace(",", "")
        integrity = integrity + 1

    valid_day = int(request.POST.get("valid_day", 0))
    u.valid_day = valid_day

    u.expire_date = datetime.datetime.today() + datetime.timedelta(days=int(valid_day))
    integrity = integrity + 1

    u.is_anonymous = int(request.POST.get("is_anonymous", "0"))
    integrity = integrity + 1

    exist_upload_names = request.POST.getlist("exist_upload_names", [])
    if has_attach or exist_upload_names:
        integrity = integrity + 1
        u.has_attach = True
    else:
        u.has_attach = False

    #country
    #industry
    #project_keyword

    u.employees_count_type = request.POST.get("employees_count_type", None)
    if request.POST.get("employees_count_type", False):
        integrity = integrity + 1

    if request.POST.get("stock_structure_percentage_type_institutional", False):
        u.stock_structure_percentage_type_institutional = request.POST["stock_structure_percentage_type_institutional"]
    if request.POST.get("stock_structure_percentage_type_management", False):
        u.stock_structure_percentage_type_management = request.POST["stock_structure_percentage_type_management"]
    if request.POST.get("stock_structure_percentage_type_private", False):
        u.stock_structure_percentage_type_private = request.POST["stock_structure_percentage_type_private"]

    if request.POST.get("stock_structure_percentage_type_institutional", False) or request.POST.get("stock_structure_percentage_type_institutional", False) or request.POST.get("stock_structure_percentage_type_private", False):
        integrity = integrity + 1

    u.currency_type_financial = request.POST.get("currency_type", None)
    integrity = integrity + 1

    expected_enterprice_value_enter = request.POST.get("expected_enterprice_value_enter", False)
    if expected_enterprice_value_enter and expected_enterprice_value_enter != "":
        u.expected_enterprice_value_enter = expected_enterprice_value_enter.replace(",", "")
        integrity = integrity + 1

    #new column
    stock_percent = request.POST.get("stock_percent", False)
    if stock_percent and stock_percent != "":
        u.stock_percent = stock_percent
        integrity = integrity + 1

    deal_size_enter = request.POST.get("deal_size_enter", False)
    if deal_size_enter and deal_size_enter != "":
        u.deal_size_enter = deal_size_enter.replace(",", "")
        integrity = integrity + 1

    income_last_phase_enter = request.POST.get("income_last_phase_enter", False)
    if income_last_phase_enter and income_last_phase_enter != "":
        u.income_last_phase_enter = income_last_phase_enter.replace(",", "")
        integrity = integrity + 1

    profit_last_phase_enter = request.POST.get("profit_last_phase_enter", False)
    if profit_last_phase_enter and profit_last_phase_enter != "":
        u.profit_last_phase_enter = profit_last_phase_enter.replace(",", "")
        integrity = integrity + 1

    ebitda = request.POST.get("ebitda", False)
    if ebitda and ebitda != "":
        u.ebitda = ebitda.replace(",", "")
        integrity = integrity + 1

    u.audit_status = int(request.POST.get("audit_status", 0))
    integrity = integrity + 1

    u.process = request.POST.get("process", 0)

    '''
        no input start
    '''
    member_id = request.session["member"]["id"]
    if member_id != "0" and member_id != "":
        u.member = Member.objects.get(pk=member_id)
    u.business_cn = request.POST.get("business_cn", None)
    u.business_en = request.POST.get("business_en", None)
    # if request.POST.get("business_cn", False) or request.POST.get("business_en", False):
    #     integrity = integrity + 1
    u.company_stock_symbol = request.POST.get("company_stock_symbol", None)
    #u.company_symbol = request.POST["company_symbol"]

    financial_is_must_audit = int(request.POST.get("financial_is_must_audit", 0))
    u.financial_is_must_audit = financial_is_must_audit
    if financial_is_must_audit == 1:
        u.financial_audit_company_is_must_default = True
    elif financial_is_must_audit == 2:
        u.financial_audit_company_is_must_default = False

    # if request.POST["growth_three_year"] != "":
    #     u.growth_three_year = request.POST["growth_three_year"]
    #     integrity = integrity + 1

    deal_size = request.POST.get("deal_size", False)
    if deal_size and deal_size != "":
        u.deal_size = deal_size
        # integrity = integrity + 1

    if request.POST.get("income", False):
        u.income = request.POST["income"]
    if request.POST.get("income_last_phase", False):
        u.income_last_phase = request.POST["income_last_phase"]
        # integrity = integrity + 1
    u.intro_cn = request.POST.get("intro_cn", None)
    u.intro_en = request.POST.get("intro_en", None)
    # if request.POST.get("intro_cn", False) or request.POST.get("intro_en", False):
    #     integrity = integrity + 1
    u.is_suitor = int(request.POST.get("is_suitor", "0"))
    # u.net_assets = request.POST["net_assets"]
    if request.POST.get("profit", False):
        u.profit = request.POST["profit"]
    if request.POST.get("profit_last_phase", False):
        u.profit_last_phase = request.POST["profit_last_phase"]
    if request.POST.get("registered_capital", False):
        u.registered_capital = request.POST["registered_capital"]

    total_assets_last_phase = request.POST.get("total_assets_last_phase", False)
    if total_assets_last_phase and total_assets_last_phase != "":
        u.total_assets_last_phase = total_assets_last_phase.replace(",", "")

    # u.remark_cn = request.POST["remark_cn"]
    # u.remark_en = request.POST["remark_en"]
    # u.financial_audit_company_name = request.POST["financial_audit_company_name"]
    if request.POST.get("expected_enterprice_value", False):
        u.expected_enterprice_value = request.POST["expected_enterprice_value"]
        # integrity = integrity + 1
    name_project_cn = request.POST.get("name_project_cn", False)
    if name_project_cn:
        u.name_project_cn = name_project_cn
    else:
        u.name_project_cn = ""

    name_project_en = request.POST.get("name_project_en", False)
    if name_project_en:
        u.name_project_en = name_project_en
    else:
        u.name_project_en = ""
    # if request.POST.get("name_project_cn", False) or request.POST.get("name_project_en", False):
    #     integrity = integrity + 1

    project_stage = request.POST.get("project_stage", False)
    if project_stage and project_stage != "":
        u.project_stage = project_stage.replace(",", "")

    pay_way = request.POST.get("pay_way", False)
    if pay_way and pay_way != "":
        u.pay_way = pay_way.replace(",", "")

    income_enter = request.POST.get("income_enter", False)
    if income_enter and income_enter != "":
        u.income_enter = income_enter.replace(",", "")

    profit_enter = request.POST.get("profit_enter", False)
    if profit_enter and profit_enter != "":
        u.profit_enter = profit_enter.replace(",", "")

    # if request.POST.get("income", False) or request.POST.get("income_enter", False):
    #     integrity = integrity + 1
    #
    # if request.POST.get("profit", False) or request.POST.get("profit_enter", False):
    #     integrity = integrity + 1

    total_assets = request.POST.get("total_assets", False)
    if total_assets and total_assets != "":
        u.total_assets = total_assets.replace(",", "")
        # integrity = integrity + 1

    total_profit = request.POST.get("total_profit", False)
    if total_profit and total_profit != "":
        u.total_profit = total_profit.replace(",", "")
        # integrity = integrity + 1
    '''
        no input end
    '''

    #new column end
    u.save()

    u.demand_attach.all().delete()
    exist_upload_names = request.POST.getlist("exist_upload_names", [])
    exist_upload_newNames = request.POST.getlist("exist_upload_newNames", [])
    upload_type_names = request.POST.getlist("upload_type_names", [])
    upload_types = request.POST.getlist("upload_types", [])
    for ut, tn in zip(upload_types, upload_type_names):
        uf = request.FILES.get("upload_file_" + ut, False)
        if uf:
            # if uf.size > 2000000:
            #     messages.error(request, _("The file cannot be more than 2M"))
            #     return
            da = DemandAttach()
            da.demand = u
            da.file_name = uf.name
            da.file_type = ut
            da.file_type_name = tn
            da.new_name = _upload_project_file(uf)
            da.save()
        else:
            for t, f, n in zip(upload_types, exist_upload_names, exist_upload_newNames):       #if upload not exsit, check the file that has already exsit file
                if t == ut:
                    da = DemandAttach()
                    da.demand = u
                    da.file_name = f
                    da.file_type = ut
                    da.file_type_name = tn
                    da.new_name = n
                    da.save()
                    break

    countries_ids = request.POST.getlist("country", [])
    if countries_ids is not None:
        integrity = integrity + 1
        for id in countries_ids:
            if id != "0" and id != "":
                u.company_countries = countries_ids

    provinces_ids = request.POST.getlist("province", [])
    if provinces_ids is not None:
        for id in provinces_ids:
            if id != "0" and id != "":
                c = Province.objects.get(pk=id)
                u.company_provinces.add(c)
    targetCompanies = request.POST.getlist("target_companies", [])
    if targetCompanies:
        u.target_companies = request.POST.getlist("target_companies", [])

    # industries_ids = request.POST.getlist("industry", [])
    industries_ids = request.POST.getlist("industry_id", [])
    u.company_industries.clear()
    DemandIndustry.objects.filter(demand_id=u.id).delete();
    if industries_ids is not None:
        integrity = integrity + 1
        for id in industries_ids:
            if id != "0" and id != "":
                c = Industry.objects.get(pk=id)
                u.company_industries.add(c)
                di = DemandIndustry()
                di.demand = u
                if c.level == 3:
                    di.cv3 = c.id
                    di.cv2 = c.father_id
                    di.cv1 = c.father.father_id
                elif c.level == 2:
                    di.cv2 = c.id
                    di.cv1 = c.father_id
                else:
                    di.cv1 = c.id
                di.save()

    demand_keyword = request.POST.get("project_keyword", False)
    if request.lang == "en-us":
        u.demand_keyword_en.all().delete()
    else:
        u.demand_keyword.all().delete()
    if demand_keyword:
        integrity = integrity + 1
        mks = demand_keyword.split(",")
        for m in mks:
            if request.lang == "en-us":
                k = DemandKeywordEn()
            else:
                k = DemandKeyword()
            k.keyword = m
            k.demand = u
            k.save()

    integrity = int(integrity * 100 / 21)
    if request.lang == "zh-cn":
        u.integrity = integrity
    else:
        u.integrity_en = integrity
    u.save()

    return True, "ok"

def _clear_items(u):
    u.company_countries.clear()
    u.company_industries.clear()
    u.company_provinces.clear()
    u.target_members.clear()
    u.target_companies.clear()
    u.target_industries.clear()

@csrf_exempt
def delete(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        member = request.session.get('member', None)
        member_id = request.session['member']['id']
        if member is None:
            msg = "nologon"
        else:
            try:
                member=get_object_or_404(Member,id=member_id)
               
                d=Demand.objects.get(pk=id, member_id=member_id)
                d.status=StatusDemand.deleted
                d.save()

                # terry 20150204 remark
                write_demand_delete_log(request, member, d)

                msg = "success"
            except Exception, e:
                msg = e.message
    return HttpResponse(msg)


@csrf_exempt
def offline(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        member = request.session.get('member', None)
        member_id = request.session['member']['id']
        if member is None:
            msg = "nologon"
        else:
            try:
                member=get_object_or_404(Member,id=member_id)

                d=Demand.objects.get(pk=id, member_id=member_id)
                d.status=StatusDemand.offline
                d.save()

                write_demand_offline_log(request, member, d)
                

                msg = "success"
            except Exception, e:
                msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@member_login_required
def get_list_for_home(request):
    c = {}
    if request.method == 'GET':
        try:
            type = request.GET.get("type", "")
            id = request.GET.get("id", "")
            q1 = Q(status=StatusDemand.approved)
            if type == "industry":
                q2 = Q(company_industries=None) | Q(company_industries=id)
            else:
                q2 = Q(company_countries=None, company_provinces=None, company_cities=None)
                location = request.GET.get("location", "")
                if location == "city":
                    q2 = q2 | Q(company_cities=id)
                elif location == "province":
                    q2 = q2 | Q(company_provinces=id)
                else:
                    q2 = q2 | Q(company_countries=id)
            if len(q2) > 0:
                q1 = q1 & q2
            demands = Demand.objects.filter(q1).order_by("-id")[0:10]
            c['data'] = demands
        except Exception, e:
            logger.error(e.message)
    return render_to_response("purchase/"+request.lang+"/list_for_home.html", c, context_instance=RequestContext(request))


@member_login_required
def download_attach(request, id):
    reload(sys)
    sys.setdefaultencoding('utf8')
    demand = get_object_or_404(Demand, pk=id)
    member_id = request.session['member']['id']
    member = Member.objects.get(pk=member_id)
    if demand.status != StatusDemand.approved and demand.member_id != member_id:
        raise Http404
    if demand.demand_attach.count() == 0:
        return HttpResponse(_("no attach"))
    if demand.is_suitor:
        if demand.is_push_to_member(member) is False and demand.member_id != member_id:
            return HttpResponse(_("not target"))
    path = settings.MEDIA_ROOT + "/demand/"
    #please view: http://stackoverflow.com/questions/12881294/django-create-a-zip-of-multiple-files-and-make-it-downloadable
    # Files (local path) to put in the .zip
    # FIXME: Change this (get paths from DB etc)
    #filenames = ["/tmp/file1.txt", "/tmp/file2.txt"]
    filenames = []
    for attach in demand.demand_attach.all():
        filenames.append(path+attach.new_name+"/"+attach.file_name)
    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    #zip_subdir = "somefiles"
    zip_subdir = demand.name_cn
    if request.lang == "en-us":
        zip_subdir = demand.name_en
    zip_filename = "%s.zip" % zip_subdir
    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")
    for fpath in filenames:
        # Calculate path for file in zip
        #fdir, fname = os.path.split(fpath)
        fnewname, fname = os.path.split(fpath)
        if os.path.isfile(fnewname) is False:
            break
        #zip_path = os.path.join(zip_subdir, fname)
        zip_path = os.path.join(zip_subdir, fname)
        # Add file, at correct path
        #zf.write(fpath, zip_path)
        zf.write(fnewname, zip_path)

    # Must close zip for all contents to be written
    zf.close()
    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename.encode("utf8")

    member.download_demand_attach(demand)
    return resp


def _upload_project_file(f):
    file_name = ""
    path = settings.MEDIA_ROOT + "/demand/"
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        file_ext = os.path.splitext(f.name)[1]
        random_no = str(random.randint(0, 99999999)).zfill(8)
        # print random_no
        file_name = random_no + file_ext
        destination = open(path + file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    except Exception, e:
        logger.error(e.message)
        # print e
    return file_name


def find_demands(condition, page, pagesize, sort):
    demands = Demand.objects.all()
    if condition.keyword != "":
        demands = demands.filter(Q(name_cn__contains=condition.keyword) | Q(name_en__contains=condition.keyword))
    if condition.type != "" and condition.type != "0" and condition.type != 0:
        demands = demands.filter(service_type=condition.type)
    if condition.country_id != 0 and condition.country_id != "" and condition.country_id != "0":
        demands = demands.filter(Q(company_countries__id=condition.country_id))     #Q(company_countries=None) |
    if condition.province_id != 0 and condition.province_id != "" and condition.province_id != "0":
        demands = demands.filter(Q(company_provinces__id=condition.province_id))    #Q(company_provinces=None) |
    if condition.industry is not None:
        demands = demands.filter(Q(company_industries=condition.industry) | Q(company_industries__father=condition.industry) | Q(company_industries__father__father=condition.industry)) #Q(company_industries=None) |
    if condition.member_id != 0 and condition.member_id != "":
        demands = demands.filter(member_id=condition.member_id)
    if condition.status != -1 and condition.status != "":
        demands = demands.filter(status=condition.status)
    if page <= 1:
        page = 1
    if pagesize <= 1:
        pagesize = 1
    start_record = (int(page)-1) * int(pagesize)
    end_record = int(start_record) + int(pagesize)
    if sort == "":
        sort = "time_desc"
    if sort == "time_desc":
        demands = demands.order_by("-id")
    elif sort == "time_asc":
        demands = demands.order_by("id")
    elif sort == "size_desc":
        demands = demands.order_by("-deal_size")
    elif sort == "size_asc":
        demands = demands.order_by("deal_size")
    elif sort == "hot_desc":
        demands = demands.order_by("-pv")

    total = demands.count()
    data = demands[start_record:end_record]
    return data, total
