# -*- coding: utf-8 -*-  
from django.http import Http404
from django.shortcuts import render_to_response, redirect, RequestContext, get_object_or_404, HttpResponse
from django.template.loader import get_template
from django.template import Context
from xhtml2pdf import pisa
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from newchama.helper import member_login_required, send_email_by_mq, send_email_by_mq_multiple
from django.utils.translation import ugettext_lazy as _
from recommond.views import update_recommond_list as update_recommond_project
from services.models import Favorites, AccountingFirm, ListedCompany, StockExchange, Project, Country, Province, Preference, ProjectKeywordEn
from services.models import Company, Member, StockStructure, Industry, StatusProject, Message, ProjectViewLog, ProjectTargetCompanyDetail, ProjectOneclickAttach, TargetCompanyDetailHistory
from services.models import ProjectServiceType, City,ProjectKeyword, ProjectAttach, ConditionProject, InvestmentCompany, InvestmentHistory, CompanyInvestmentHistory, ProjectOtherTargetCompany
from services.models import ProjectCustomerTargetCompany,TypeFavorite, ProjectVisitor, Demand, StatusDemand,Deal,CompanyWithPE, News, PreferenceKeyword, PreferenceIndustry, PreferenceLocation
from services.models import RecommondItem
from services.helper import Helper
from django.template import loader
from services.templatetags import myTags
from subscribe.models import Subscribe, SubscribeKeyword
from newchama.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMessage
import datetime
import StringIO
import os
from newchama import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q, Sum, connection
import random
import logging
import zipfile
from django.utils import simplejson

from log.views import *

logger = logging.getLogger(__name__)


def _is_has_condition(condition):
    return condition != "" and condition != "0"


@member_login_required
def search(request):
    c = {}
    c['title']=_("Search")
    c['member']=request.session.get('member', None)
    member_id = request.session['member']['id']
    is_search = request.GET.get("is_search", "")
    if is_search == '1':
        is_has_condition = False
        type = request.GET.get('serviceType', 0)
        keyword = request.GET.get('keywords', '')
        country = request.GET.get("country", "")
        industry_id = request.GET.get('industry_id', 0)
        dealsize_min = request.GET.get('rangeMin', -1)
        dealsize_max = request.GET.get('rangeMax', -1)
        sort = request.GET.get('sort', 'time_desc')
        industry_first = request.GET.get("industry_first", "")
        industry_second = request.GET.get("industry_second", "")
        industry_third = request.GET.get("industry_third", "")
        projectRange = request.GET.get("projectRange", "")
        c['projectRange'] = projectRange
        condition = ConditionProject()
        condition.keywords = []                 #Terry mark 20150529, not fixed that when click the subscribe then the search btn return result has keywords
        if keyword != "":
            c["keyword"] = keyword
            is_has_condition = True
        if type != "":
            c["type"] = int(type)
            is_has_condition = True
        country_id = 0
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
            condition.industry = industry
            is_has_condition = True

        condition.country_id = country_id
        condition.keyword = keyword
        condition.status = StatusDemand.approved
        condition.type = type

        #level = 1
        #if industry_id != 0 and industry_id != "0":
        #    condition.industry = Industry.objects.get(pk=industry_id)
        #    level = condition.industry.level
        if dealsize_max != 0 and dealsize_max != "0" and dealsize_max != "":
            condition.dealsize_max = int(dealsize_max)
        if dealsize_min != "":
            condition.dealsize_min = int(dealsize_min)
        #condition.dealsize_max = dealsize_max
        #condition.dealsize_min = dealsize_min
        if is_has_condition:
            data, total = find_projects(condition, 1, 5, sort)
            c['has_more'] = total > 5
            for result in data:
                keywords_list=[]
                for kv in ProjectKeyword.objects.filter(project=result):
                    keywords_list.append(kv.keyword)
                result.keywords=','.join(keywords_list)

            c['data'] = data
            c['favorites_project_ids'] = Helper.find_member_favorite_project_ids(member_id)
        c['is_search'] = True
        c['is_has_condition'] = is_has_condition
    c["SERVICE_TYPES"] = Project.SERVICE_TYPES
    c["PROJECT_RANGE"] = Project.PROJECT_RANGE
    c["countries"] = Helper.find_countries()
    c["industries"] = Helper.find_industries_level1()
    return render_to_response("sales/"+request.lang+"/search.html", c, context_instance=RequestContext(request))

@member_login_required
def one_click(request):
    return render_to_response("sales/"+request.lang+"/one_click.html")

@member_login_required
def search_keyword(request):
    c = {}
    c['title'] = _("Search")
    keyword = request.GET.get("keyword", '')
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    member = get_object_or_404(Member,pk=member_id)
    c["keyword"] = keyword
    result_list = Project.objects.filter(Q(status=StatusProject.approved) & (Q(name_cn__contains=keyword) | Q(name_en__contains=keyword))).order_by("-id")
    for result in result_list:
        keywords_list=[]
        for kv in ProjectKeyword.objects.filter(project=result):
            keywords_list.append(kv.keyword)
        result.keywords=','.join(keywords_list)

    c['data'] = result_list[0:5]
    c['total_project'] = result_list.count()
    c['total_demand'] = Demand.objects.filter(Q(status=StatusDemand.approved) & (Q(name_cn__contains=keyword) | Q(name_en__contains=keyword))).count()
    c['total_news'] = News.objects.filter(Q(title__contains=keyword) | Q(tag__contains=keyword)).count()
    c['total_company'] = Company.objects.filter(Q(short_name_cn__contains=keyword) | Q(short_name_en__contains=keyword)).exclude(id=27).count()
    c['total_member'] = Member.objects.filter(Q(last_name__contains=keyword) | Q(first_name__contains=keyword)).count()
    c['favorites_project_ids'] = Helper.find_member_favorite_project_ids(member_id)

    write_search_project_log(request,member,keyword)

    return render_to_response("sales/"+request.lang+"/search_keyword.html", c, context_instance=RequestContext(request))


@member_login_required
def new(request, id=0):
    c = {}
    c['title']=_("New")
    c['member']=request.session.get('member', None)
    member_id = request.session['member']['id']
    sort = request.GET.get("sort", "time_desc")
    c[sort] = "active"
    c['sort'] = sort
    c['countries'] = Helper.find_countries()
    c['industries'] = Helper.find_industries_level1()

    condition = ConditionProject()
    condition.keywords = []                 #Terry mark 20150529, not fixed that when click the subscribe then the search btn return result has keywords
    condition.status = StatusProject.approved
    condition.type = ''
    subscribe_id = id
    if subscribe_id == 0:
        subscribe_id = request.GET.get('subscribe_id', False)
    c["subscribe_id"] = 0
    if subscribe_id and subscribe_id != "0":
        c["subscribe_id"] = subscribe_id
        s = Subscribe.objects.get(id=subscribe_id)
        if s:
            condition.country_id = s.company_countries_id
            condition.province_id = s.company_provinces_id
            condition.industry = s.company_industries_id
            condition.dealsize_min = s.deal_size_min
            condition.dealsize_max = s.deal_size_max
            condition.service_type = s.service_type
            condition.project_stage = s.project_stage
            condition.currency_type = s.currency_type
            sks = s.subscribe_keyword.all()
            if sks:
                for k in sks:
                    condition.keywords.append(k.keyword)
            else:
                 condition.keywords = []
    pagesize = 10
    result_list, total = find_projects(condition, 1, pagesize, sort)
    '''
    for result in result_list:
        keywords_list=[]
        if request.lang == "en-us":
            for kv in ProjectKeywordEn.objects.filter(project=result):
                keywords_list.append(kv.keyword)
        else:
            for kv in ProjectKeyword.objects.filter(project=result):
                keywords_list.append(kv.keyword)

        result.keywords=','.join(keywords_list)
    '''
    c["have_more_data"] = len(result_list) == int(pagesize)
    c["subscribe"] = Subscribe.objects.filter(member_id=member_id, is_delete=0).order_by("-id")
    c['need_preference'] = False
    c['data'] = result_list
    c['total'] = total
    c['favorites_project_ids'] = Helper.find_member_favorite_project_ids(member_id)
    return render_to_response("sales/"+request.lang+"/new.html", c, context_instance=RequestContext(request))


@member_login_required
def ajax_more(request):
    c = {}
    member = request.session.get('member', None)
    if member == None:
        return None
    member_id = request.session['member']['id']
    page = request.GET.get('page', 1)
    pagesize = request.GET.get('pagesize', 10)
    type = request.GET.get('type', 0)
    keyword = request.GET.get('keywords', '')
    country_id = request.GET.get('country_id', 0)
    province_id = request.GET.get('province_id', 0)
    industry_id = request.GET.get('industry_id', 0)
    dealsize_min = request.GET.get('dealsize_min', -1)
    dealsize_max = request.GET.get('dealsize_max', -1)
    sort = request.GET.get('sort', 'time_desc')
    condition = ConditionProject()
    condition.keywords = []                 #Terry mark 20150529, not fixed that when click the subscribe then the search btn return result has keywords
    condition.status = StatusProject.approved
    subscribe_id = int(request.GET.get('subscribe_id'), 0)
    s = None
    if subscribe_id > 0:
        s = Subscribe.objects.get(id=subscribe_id)
    if s:
        condition.country_id = s.company_countries_id
        condition.province_id = s.company_provinces_id
        condition.industry = s.company_industries_id
        condition.dealsize_min = s.deal_size_min
        condition.dealsize_max = s.deal_size_max
        condition.service_type = s.service_type
        condition.project_stage = s.project_stage
        condition.currency_type = s.currency_type
        sks = s.subscribe_keyword.all()
        if sks:
            for k in sks:
                condition.keywords.append(k.keyword)
        else:
             condition.keywords = []
    else:
        condition.country_id = country_id
        condition.province_id = province_id
        condition.keyword = keyword
        condition.type = type
        level = 1
        if industry_id != 0 and industry_id != "0" and industry_id != "":
            condition.industry = industry_id
            industry = Industry.objects.get(pk=industry_id)
            level = industry.level
        if dealsize_max != 0 and dealsize_max != "0" and dealsize_max != "":
            condition.dealsize_max = int(dealsize_max)
        if dealsize_min != "":
            condition.dealsize_min = int(dealsize_min)
    data, total = find_projects(condition, page, pagesize, sort)

    #if industry level is 3, and query data count is 0, then search the data which is the father industry level
    #if industry_id != 0 and industry_id != "0" and total == 0 and level != 1:
    #    condition.industry = Industry.objects.get(pk=condition.industry.father_id)
    #    try:
    #        level = condition.industry.father.level
    #    except Exception:
    #        level = 1
    #    data, total = Helper.find_projects(condition, page, pagesize, sort)
    #if industry level is 2, and query data count is 0, then search the data which is the father industry level
    #if industry_id != 0 and industry_id != "0" and total == 0 and level != 1:
    #    condition.industry = condition.industry.father
    #    data, total = Helper.find_projects(condition, page, pagesize, sort)
    for result in data:
        keywords_list=[]
        for kv in ProjectKeyword.objects.filter(project=result):
            keywords_list.append(kv.keyword)
        result.keywords=','.join(keywords_list)

    c['data'] = data
    c["have_more_data"] = len(data) == int(pagesize)
    c['favorites_project_ids'] = Helper.find_member_favorite_project_ids(member_id)
    return render_to_response("sales/"+request.lang+"/ajax_list.html", c, context_instance=RequestContext(request))


@csrf_exempt
@member_login_required
def json_index(request):
    c = {}
    member_id = request.session['member']['id']
    if request.method == 'POST':
        try:
            member_id = request.session['member']['id']
            condition = Q(status=StatusProject.approved)
            condition2 = Q()
            industryIds = request.GET.get("industryId", False)
            if industryIds and industryIds != "0":
                ids = industryIds.split(",")
                for id in ids:
                    condition2 = condition2 | Q (company_industry=id)

            locationIds = request.GET.get("locationId", False)
            if locationIds and locationIds != "0":
                ids = locationIds.split(",")
                for id in ids:
                    condition2 = condition2 | Q (company_country=id)
            condition = condition & condition2

            if industryIds == False and locationIds == False:
                result_list = preferenceByMemberId(c, member_id)
            else:
                result_list = Project.objects.filter(condition).order_by("-id")[0 : 3]

            c["result_list"] = result_list
            list_project_preference_plus = 3 - len(result_list)
            if list_project_preference_plus > 0:
                c["recent_project"] = Project.objects.filter(status=StatusProject.approved).order_by("-id")[0: list_project_preference_plus]
        except Exception, e:
            logger.error('show project json error!' + e.message)
    c['favorites_project_ids'] = Helper.find_member_favorite_project_ids(member_id)
    return render_to_response("sales/"+request.lang+"/json_index.html", c, context_instance=RequestContext(request))


def preferenceByMemberId(c, member_id):
    list = []
    preferences = Preference.objects.filter(member_id=member_id, title="project")[0 : 1]
    condition = Q(status=StatusProject.approved)
    if len(preferences) > 0:
        condition2 = Q()
        p = preferences[0]
        c['preference_project_id'] = p.id
        preference_project_industries = p.preference_industry.all().distinct() #.values("industry") #PreferenceIndustry.objects.filter(preference__member__id=member['id'])
        c['pre_project_indusrtis'] = preference_project_industries
        if len(preference_project_industries) > 0:
            for ppi in preference_project_industries:
                condition2 = condition2 | Q (company_industry=ppi.industry.id)
        preference_project_location = p.preference_location.all().distinct()

        c['pre_project_locations'] = preference_project_location
        if len(preference_project_location):
            for ppl in preference_project_location:
                condition2 = condition2 | Q (company_country=ppl.country_id)

        condition = condition & condition2
        list = Project.objects.filter(condition).order_by("-id")[0: 3]
    return list


def projectByMemberId(member_id):
    projects = Project.objects.filter(member_id=member_id, status=StatusProject.approved).order_by("-id")[0: 5]
    list_project = []
    for project in projects:
        count_message = Message.objects.filter(type_relation=1, project=project.id, is_read=0).count()
        count_favor = Favorites.objects.filter(type_relation=1, project=project.id).count()
        count_company = Company.objects.filter(industry=project.company_industry, status=1).exclude(id=27).count()
        count_industry = 0
        industry_id = 0
        industry = project.company_industry
        if industry is not None:
            industry_level = industry.level
            industry_id = industry.id
            if industry_level == 2:
                industry_id = industry.father_id
            elif industry_level == 3:
                industry_id = industry.father.father_id
        #start_date = datetime.date(datetime.datetime.today().year, datetime.datetime.today().month - 3, datetime.datetime.today().day)
        start_date = datetime.datetime.today()-datetime.timedelta(days=90)
        count_industry = Deal.objects.filter(cv1=industry_id, happen_date__gt=start_date).count()
        pro = {}
        pro["project"] = project
        pro["count_message"] = count_message
        pro["count_favor"] = count_favor
        pro["count_industry"] = count_industry
        pro["count_company"] = count_company
        list_project.append(pro)
    
    return list_project


def countProjectStuffTotal(member_id):
    pvs = Project.objects.filter(member_id=member_id, status=StatusProject.approved).aggregate(sum_pv=Sum('pv'))
    messages = 0#Message.objects.filter(type_relation=1, project__member__id=member_id, is_read=0, is_delete=0).count()
    favorites = Favorites.objects.filter(type_relation=1, project__member__id=member_id).count()
    cursor = connection.cursor()

    sql_ = "select count(id) from member_company where industry_id in (select distinct company_industry_id from project_project where member_id = " + str(member_id) + " and status = " + str(StatusProject.approved) + ")"
    cursor.execute(sql_)
    recommend_companies = cursor.fetchone()

    #start_date = datetime.date(datetime.datetime.today().year, datetime.datetime.today().month - 3, datetime.datetime.today().day)
    start_date = datetime.datetime.today()-datetime.timedelta(days=90)
    projects = Project.objects.filter(member_id=member_id, status=StatusProject.approved, cv1__isnull=False).values("cv1").distinct()
    industry_ids = []
    if projects:
        for p in projects:
            industry_ids.append(p["cv1"])

    recommend_industries = Deal.objects.filter(cv1__in=industry_ids, happen_date__gt=start_date).count()
    count_project_all = {}
    count_project_all["pvs"] = pvs["sum_pv"]
    count_project_all["messages"] = messages
    count_project_all["favorites"] = favorites
    count_project_all["recommend_companies"] = recommend_companies[0]
    count_project_all["recommend_industries"] = recommend_industries
    return count_project_all

@member_login_required
def mylist(request, type):
    c = {}
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    projects = Project.objects.filter(member_id=member_id).exclude(status=StatusProject.deleted).order_by("-id")
    total_all = projects.count()
    c['total_all'] = total_all
    '''
    result_release = projects.filter(status=StatusProject.approved)
    result_draft = projects.filter(status=StatusProject.draft)
    result_pending = projects.filter(status=StatusProject.pending)
    result_not_approved = projects.filter(status=StatusProject.not_approved)
    result_offline = projects.filter(status=StatusProject.offline)
    result_expired = projects.filter(expire_date__gt=datetime.datetime.today)
    d_list = {"release": result_release, "draft": result_draft, "pending": result_pending, "not_approved": result_not_approved, "expired": result_expired}
    d_list.update({"offline": result_offline, "all": projects})
    result_list = d_list.get(type, projects)
    total_release = result_release.count()
    total_offline = result_offline.count()
    total_pending = result_pending.count()
    total_draft = result_draft.count()
    total_not_approved = result_not_approved.count()
    total_all = projects.count()
    c['total_all'] = total_all
    c['total_release'] = total_release
    c['total_offline'] = total_offline
    c['total_pending'] = total_pending
    c['total_draft'] = total_draft
    c['total_not_approved'] = total_not_approved
    total_demand = Demand.objects.filter(member_id=member_id).exclude(status=StatusDemand.deleted).count()
    c['total_demand'] = total_demand
    '''
    result_list_2 = []
    for result in projects:
        result_list_2.append(countResult(result))
    c['result_list'] = result_list_2
    c[type] = "active"
    c['type'] = type
    return render_to_response("sales/"+request.lang+"/mylist.html", c, context_instance=RequestContext(request))


def countResult(result):
    resultList = {}
    total_recommends = RecommondItem.objects.filter(is_delete=0, project__id=result.id).count()
    total_recommends = Helper.checkCountMatch(total_recommends)
    total_favorites = Favorites.objects.filter(type_relation=1, project__id=result.id).count()
    not_read_messages = Message.objects.filter(type_relation=1, project__id=result.id, is_read=0).count()
    resultList['total_recommends'] = total_recommends
    resultList['total_favorites'] = total_favorites
    resultList['not_read_messages'] = not_read_messages
    resultList['id'] = result.id
    resultList['name_cn'] = result.name_cn
    resultList['name_en'] = result.name_en
    resultList['status'] = result.status
    resultList['processName'] = result.get_process_display
    resultList['add_time'] = result.add_time
    resultList['statusName'] = result.get_status_display
    resultList['total_target'] = result.target_companies.count()
    resultList['pvs'] = result.pv
    resultList['integrity'] = result.integrity
    return resultList

'''
@member_login_required
def mylist(request, type, id=0):
    c = {}
    c['title']=_("MyList")
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    projects = Project.objects.filter(member_id=member_id).exclude(status=StatusProject.deleted).order_by("-update_time")
    result_public = projects.filter(is_public=True)
    result_private = projects.filter(is_suitor=True)
    result_release = projects.filter(status=StatusProject.approved)#, expire_date__gt=datetime.datetime.today, is_suitor=True)
    result_draft = projects.filter(status=StatusProject.draft)
    result_pending = projects.filter(status=StatusProject.pending)
    result_not_approved = projects.filter(status=StatusProject.not_approved)
    result_offline = projects.filter(status=StatusProject.offline)
    result_expired = projects.filter(expire_date__gt=datetime.datetime.today)
    d_list = {"release": result_release, "draft": result_draft, "pending": result_pending, "not_approved": result_not_approved, "expired": result_expired}
    d_list.update({"offline": result_offline, "all": projects, "public": result_public, "private": result_private})
    result_list = d_list.get(type, projects)
    total = result_list.count()
    total_all = projects.count()
    total_public = result_public.count()
    total_private = result_private.count()
    total_draft = result_draft.count()
    c['total_all'] = total_all
    c['total_public'] = total_public
    c['total_private'] = total_private
    c['total_draft'] = total_draft
    c['total'] = total
    total_demand = Demand.objects.filter(member_id=member_id).exclude(status=StatusDemand.deleted).count()
    c['total_demand'] = total_demand
    if total == 0:
        return render_to_response("sales/"+request.lang+"/mylist_empty.html", c, context_instance=RequestContext(request))
    ids = []
    for m in result_list:
        ids.append(m.id)
    id_current = int(id)
    if id_current == 0:
        project = result_list[0]
        id_current = project.id
    else:
        if id_current not in ids:
            raise Http404
        pageIndex = ids.index(id_current)+1
        project = result_list[pageIndex-1]
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
    c['m'] = project
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
    visitors = ProjectVisitor.objects.filter(project_id=project.id)
    c['visitors'] = visitors.order_by("-add_time")[0:5]
    c['visitors_count'] = visitors.count()
    followers = Favorites.objects.filter(project_id=project.id)
    c['followers'] = followers.order_by("-add_time")[0:5]
    c['followers_count'] = followers.count()
    c['message_list'] = Message.objects.filter(type_relation=1, project_id=project.id, is_delete=0).order_by('-add_time')[0:5]

    #之后用cv1替代
    if project.company_industry:
        if project.company_industry.level==3:
            c['deal_list_more_id']=project.company_industry.father.father.id
            
        elif project.company_industry.level==2:
            c['deal_list_more_id']=project.company_industry.father.id
            
        else:
            c['deal_list_more_id']=project.company_industry.id

        c['deal_list'] =Deal.objects.filter(cv1=c['deal_list_more_id']).order_by('-update_time')[0:10]

        c['compare_cn']= CompanyWithPE.objects.filter(country__name_en='China',industry__id=c['deal_list_more_id']).order_by('-ps')[0:5]
        
        c['compare_usa']= CompanyWithPE.objects.filter(country__name_en='United States of America',industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]
        
        c['compare_hk']= CompanyWithPE.objects.filter(country__name_en='Hong Kong',industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]
        
        c['compare_uk']= CompanyWithPE.objects.filter(country__name_en='United Kingdom',industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]

    c['recommend_of_project'] = Member.objects.filter(member_demand_publisher__company_industries=project.company_industry).order_by('id')[0:5]
    c['recommend_of_industry_investment'] = Member.objects.filter(company__companyinvestmenthistory__industry_id=project.company_industry).order_by('id')[0:5]
    c['recommend_of_industry_follow'] = Member.objects.filter(member_preference__preference_industry__industry_id=project.company_industry).order_by('id')[0:5]
    return render_to_response("sales/"+request.lang+"/mylist.html", c, context_instance=RequestContext(request))
'''

@member_login_required
def mydetail(request, id):
    c = {}
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    project = get_object_or_404(Project, pk=id, member_id=member_id)
    # c['m'] = project
    m = countResult(project)
    c['m'] = m
    c['process'] = Project.PROCESS
    members = Member.objects.filter(company_id=27)
    _visitors = ProjectVisitor.objects.filter(project_id=project.id).exclude(member=members).order_by("-add_time")[0:8]

    visitors=[]

    for v in _visitors:
        if v.member.email.find('@newchama.com')==-1:
            visitors.append(v)


    c['visitors'] = visitors
    c['visitors_count'] = len(visitors)
    followers = Favorites.objects.filter(project_id=project.id)
    c['followers'] = followers.order_by("-add_time")[0:5]
    c['followers_count'] = followers.count()
    c['message_list'] = Message.objects.filter(type_relation=1, project_id=project.id, receiver_id=member_id, is_delete=0).order_by('-add_time')[0:5]
    #之后用cv1替代
    if project.company_industry:
        if project.company_industry.level==3:
            c['deal_list_more_id']=project.company_industry.father.father.id

        elif project.company_industry.level==2:
            c['deal_list_more_id']=project.company_industry.father.id

        else:
            c['deal_list_more_id']=project.company_industry.id

        c['deal_list'] =Deal.objects.filter(cv1=c['deal_list_more_id']).order_by('-update_time')[0:10]

        c['compare_cn']= CompanyWithPE.objects.filter(country__name_en='China',industry__id=c['deal_list_more_id']).order_by('-ps')[0:5]

        c['compare_usa']= CompanyWithPE.objects.filter(country__name_en='United States of America',industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]

        c['compare_hk']= CompanyWithPE.objects.filter(country__name_en='Hong Kong',industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]

        c['compare_uk']= CompanyWithPE.objects.filter(country__name_en='United Kingdom',industry__id=c['deal_list_more_id']).order_by('-pe')[0:5]

    targetCompanList = project.target_companies.all()
    if targetCompanList:
        company_list = []
        for t in targetCompanList:
            company = {}
            company["logo"] = t.logo
            company["short_name_cn"] = t.short_name_cn
            company["id"] = t.id
            # company["messageCount"] = findNotification(t.id, project.id, project.member_id)
            company_list.append(company)
        c["recommend_company_list"] = company_list
        c["is_recommend_company"] = True
    else:
        c["is_recommend_company"] = False
    #search member_company, repository_investmentcompany, repository_listedcompany according to industry
    #c["recommendList"] = recommendCampany(request.lang == "en-us", project)
    # c["countRecommend"] = recommendCampanyCount(request.lang == "en-us", project)
    _recommendList=list(RecommondItem.objects.filter(project=project,is_man=True,is_delete=False).exclude(company__in=targetCompanList).order_by('-rank'))
    _recommendList+=list(RecommondItem.objects.filter(project=project,is_man=False,sum_project_score__gte=50).exclude(company__in=targetCompanList).order_by('-sum_project_score'))
    if len(_recommendList)<24:
        _recommendList +=list(RecommondItem.objects.filter(project=project,is_man=False,sum_project_score__lt=50).exclude(company__in=targetCompanList).order_by('-sum_company_score')[:24-len(_recommendList)])

    c["recommendList"] =_recommendList
    return render_to_response("sales/"+request.lang+"/mydetail.html", c, context_instance=RequestContext(request))


def findNotification(company_id, project_id, member_id):
    members = Member.objects.filter(company_id=company_id)
    if members:
        ms = []
        for m in members:
            ms.append(m)
        return Message.objects.filter(sender_id=member_id,is_read=0,is_delete=0,receiver__in=ms, project_id=project_id).count()
    else:
        return 0


def recommendCampanyCount(is_english, project):
    #search member_company according to the industry exclude exist industry
    search_result = 8
    resultCount = 0
    resultList = {}
    companyResultList = []
    if project.company_industry is None:
        return resultList
    totalCount =0
    #according to the
    demandCondition = Q(status=StatusDemand.approved)
    dc = Q()
    if project.cv1:
        dc = dc | Q(company_industries__id=project.cv1)
    if project.cv2:
        dc = dc | Q(company_industries__id=project.cv2)
    if project.cv3:
        dc = dc | Q(company_industries__id=project.cv3)
    demandCondition = demandCondition & dc
    demandMemberList = Demand.objects.filter(demandCondition).exclude(member_id=project.member_id).values("member")
    if demandMemberList:
        memberIds = []
        for m in demandMemberList:
            memberIds.append(m["member"])
        companyList_demand = Company.objects.filter(member__in=set(memberIds)).exclude(id__in=project.target_companies.all()).exclude(id=project.member.company.id).exclude(id=27)
        resultList["companyList_demand"] = companyList_demand
        companyList_demandCount = Company.objects.filter(member__in=set(memberIds)).exclude(id__in=project.target_companies.all()).exclude(id=project.member.company.id).exclude(id=27).count()
        if companyList_demand:
            for c in companyList_demand:
                companyInfo = {}
                companyInfo["type"] = 0
                companyInfo["id"] = c.id
                companyInfo["name_cn"] = c.name_cn
                companyInfo["short_name_cn"] = c.short_name_cn
                companyInfo["name_en"] = c.name_en
                companyInfo["short_name_en"] = c.short_name_en
                companyInfo["logo"] = c.logo
                companyInfo["recommendReason"] = "relate buy-side mandate"
                companyResultList.append(companyInfo)
        resultList["demand_count"] = companyList_demandCount
        totalCount = totalCount + companyList_demandCount

    q1 = Q(status=1) #Company().STATUS_TYPES["1"]
    q2 = Q()
    # condition["expire_date__gt"]=datetime.datetime.today
    if project.cv1:
        q2 = q2 | Q(industry__id=project.cv1)
    if project.cv2:
        q2 = q2 | Q(industry__id=project.cv2)
    if project.cv3:
        q2 = q2 | Q(industry__id=project.cv3)
    q1 = q1 & q2
    exsitCompany = []
    if companyResultList:
        for rl in companyResultList:
            exsitCompany.append(rl["id"])
    # member_companyList_notexsit_same = Company.objects.filter(q1).exclude(id__in=project.target_companies.all()).exclude(id=project.member.company.id).exclude(id__in=exsitCompany).order_by("?")[:search_result]
    member_companyList_notexsit_same_count = Company.objects.filter(q1).exclude(id__in=project.target_companies.all()).exclude(id=project.member.company.id).exclude(id__in=exsitCompany).exclude(id=27).count()
    totalCount = totalCount + member_companyList_notexsit_same_count

    member_companyList = Company.objects.filter(q1).exclude(id__in=project.target_companies.all()).exclude(id=project.member.company.id).exclude(id=27)
    resultList["member_companyList"] = member_companyList
    member_companyListCount = Company.objects.filter(q1).exclude(id__in=project.target_companies.all()).exclude(id=project.member.company.id).exclude(id=27).count()
    resultList["industry_company_count"] = member_companyListCount

    q3 = Q()
    if project.cv1:
        q3 = q3 | Q(cv1=project.cv1)
    if project.cv2:
        q3 = q3 | Q(cv2=project.cv2)
    if project.cv3:
        q3 = q3 | Q(cv3=project.cv3)
    plusCount = search_result - resultCount
    exsitInvestmentCompany = ProjectOtherTargetCompany.objects.filter(project__id=project.id, table_name=2)
    companyList = InvestmentHistory.objects.filter(q3).values("company").exclude(company=exsitInvestmentCompany)
    if is_english:
        investmentCompany = InvestmentCompany.objects.filter(id__in=companyList)
        investmentCompanyCount = InvestmentCompany.objects.filter(id__in=companyList).count()
    else:
        investmentCompany = InvestmentCompany.objects.filter(id__in=companyList).exclude(name_cn="-").exclude(name_cn="")
        investmentCompanyCount = InvestmentCompany.objects.filter(id__in=companyList).exclude(name_cn="-").exclude(name_cn="").count()
    resultList["investmentCompany"] = investmentCompany
    resultList["industry_investcompany_count"] = investmentCompanyCount
    totalCount = totalCount + investmentCompanyCount

    exsitListedCompany = ProjectOtherTargetCompany.objects.filter(project__id=project.id, table_name=1)
    if is_english:
        listedCompanyList = ListedCompany.objects.filter(q2).exclude(industry=exsitListedCompany)
        listedCompanyListCount = ListedCompany.objects.filter(q2).exclude(industry=exsitListedCompany).exclude(name_cn="").count()
    else:
        listedCompanyList = ListedCompany.objects.filter(q2).exclude(industry=exsitListedCompany).exclude(name_cn="-").exclude(name_cn="")
        listedCompanyListCount = ListedCompany.objects.filter(q2).exclude(industry=exsitListedCompany).exclude(name_cn="-").exclude(name_cn="").count()
    resultList["listedCompanyList"] = listedCompanyList
    resultList["list_company_count"] = listedCompanyListCount
    totalCount = totalCount + listedCompanyListCount
    resultList["total_count"] = totalCount
    return resultList


def recommendCampany(is_english, project,num=24):
    #search member_company according to the industry exclude exist industry
    search_result = num
    resultCount = 0
    resultList = []
    if project.company_industry is None:
        return resultList

    #according to the
    demandCondition = Q(status=StatusDemand.approved)
    dc = Q()
    if project.cv3:
        dc = dc | Q(company_industries__id=project.cv3)
    elif project.cv2:
        dc = dc | Q(company_industries__id=project.cv2)
    elif project.cv1:
        dc = dc | Q(company_industries__id=project.cv1)
    demandCondition = demandCondition & dc
    demandMemberList = Demand.objects.filter(demandCondition).exclude(member_id=project.member_id).values("member")
    if demandMemberList:
        memberIds = []
        for m in demandMemberList:
            memberIds.append(m["member"])
        companyList_demand = Company.objects.filter(member__in=set(memberIds)).exclude(id__in=project.target_companies.all()).exclude(id=project.member.company.id).exclude(id=27).order_by("?")[:search_result]
        if companyList_demand:
            for c in companyList_demand:
                companyInfo = {}
                companyInfo["type"] = 0
                companyInfo["id"] = c.id
                companyInfo["name_cn"] = c.name_cn
                companyInfo["short_name_cn"] = c.short_name_cn
                companyInfo["name_en"] = c.name_en
                companyInfo["short_name_en"] = c.short_name_en
                companyInfo["logo"] = c.logo
                companyInfo["company_field"] = ''

                user_count=Member.objects.filter(company=c,status=1,type=2).count()
                companyInfo["has_user"] = user_count>0
                
                companyInfo["recommendReason"] = "relate buy-side mandate"
                resultList.append(companyInfo)
                resultCount = resultCount + 1

    q1 = Q(status=1) #Company().STATUS_TYPES["1"]
    q2 = Q()
    # condition["expire_date__gt"]=datetime.datetime.today
    if project.cv3:
        q2 = q2 | Q(industry__id=project.cv3)
    elif project.cv2:
        q2 = q2 | Q(industry__id=project.cv2)
    elif project.cv1:
        q2 = q2 | Q(industry__id=project.cv1)
    q1 = q1 & q2
    exsitCompany = []
    if resultList:
        for rl in resultList:
            exsitCompany.append(rl["id"])
    member_companyList = Company.objects.filter(q1).exclude(id__in=project.target_companies.all()).exclude(id=project.member.company.id).exclude(id__in=exsitCompany).order_by("?").exclude(id=27)[:search_result]
    if member_companyList:
        for c in member_companyList:
            companyInfo = {}
            companyInfo["type"] = 0
            companyInfo["id"] = c.id
            companyInfo["name_cn"] = c.name_cn
            companyInfo["short_name_cn"] = c.short_name_cn
            companyInfo["name_en"] = c.name_en
            companyInfo["short_name_en"] = c.short_name_en
            companyInfo["logo"] = c.logo
            companyInfo["company_field"] = ''
            companyInfo["has_user"] = True
            companyInfo["recommendReason"] = "investor within the same industry"
            resultList.append(companyInfo)
            resultCount = resultCount + 1

    #if the search result still less than 6 then search investment company according to the invert history's industry exclude exist industry
    # InvestmentHistory
    if resultCount < search_result:
        q3 = Q()
        if project.cv3:
            q3 = q3 | Q(cv3=project.cv3)
        elif project.cv2:
            q3 = q3 | Q(cv2=project.cv2)
        elif project.cv1:
            q3 = q3 | Q(cv1=project.cv1)
        plusCount = search_result - resultCount
        exsitInvestmentCompany = ProjectOtherTargetCompany.objects.filter(project__id=project.id, table_name=2)
        companyList = InvestmentHistory.objects.filter(q3).values("company").exclude(company=exsitInvestmentCompany)#.distinct("company")
        if is_english:
            investmentCompany = InvestmentCompany.objects.filter(id__in=companyList).order_by("?")[:plusCount]
        else:
            investmentCompany = InvestmentCompany.objects.filter(id__in=companyList).exclude(name_cn="-").exclude(name_cn="").order_by("?")[:plusCount]
        if investmentCompany:
            for c in investmentCompany:
                companyInfo = {}
                companyInfo["type"] = 1
                companyInfo["id"] = c.id
                companyInfo["name_cn"] = c.name_cn
                companyInfo["short_name_cn"] = c.short_name_cn
                companyInfo["name_en"] = c.name_en
                companyInfo["short_name_en"] = c.short_name_en
                companyInfo["logo"] = ""
                companyInfo["company_field"] = c.invest_field
                companyInfo["has_user"] = False
                companyInfo["recommendReason"] = _("invested in similar companies")
                resultList.append(companyInfo)
                resultCount = resultCount + 1

    #according to the invest direct to search the same investmentCompany
    # InvestmentHistory
    if resultCount < search_result:
        searchCondition = ""
        if project.cv3:
            searchCondition = project.cv3
        elif project.cv2:
            searchCondition = project.cv2
        elif project.cv1:
            searchCondition = project.cv1
        plusCount = search_result - resultCount
        if is_english:
            investmentCompany = InvestmentCompany.objects.filter(invest_field__contains=searchCondition).order_by("?")[:plusCount]
        else:
            investmentCompany = InvestmentCompany.objects.filter(invest_field__contains=searchCondition).exclude(name_cn="-").exclude(name_cn="").order_by("?")[:plusCount]
        if investmentCompany:
            for c in investmentCompany:
                companyInfo = {}
                companyInfo["type"] = 1
                companyInfo["id"] = c.id
                companyInfo["name_cn"] = c.name_cn
                companyInfo["short_name_cn"] = c.short_name_cn
                companyInfo["name_en"] = c.name_en
                companyInfo["short_name_en"] = c.short_name_en
                companyInfo["logo"] = ""
                companyInfo["company_field"] = c.invest_field
                companyInfo["has_user"] = False
                companyInfo["recommendReason"] = _("investment orientation")
                resultList.append(companyInfo)
                resultCount = resultCount + 1

    #if the search result is less than 6 then search repository_listedcompany according to the invert history's industry exclude exist industry
    if resultCount < search_result:
        plusCount = search_result - resultCount
        exsitListedCompany = ProjectOtherTargetCompany.objects.filter(project__id=project.id, table_name=1)
        if is_english:
            listedCompanyList = ListedCompany.objects.filter(q2).exclude(industry=exsitListedCompany).order_by("?")[:plusCount]
        else:
            listedCompanyList = ListedCompany.objects.filter(q2).exclude(industry=exsitListedCompany).exclude(name_cn="-").exclude(name_cn="").order_by("?")[:plusCount]
        if listedCompanyList:
            for c in listedCompanyList:
                companyInfo = {}
                companyInfo["type"] = 2
                companyInfo["id"] = c.id
                companyInfo["name_cn"] = c.name_cn
                companyInfo["short_name_cn"] = c.short_name_cn
                companyInfo["name_en"] = c.name_en
                companyInfo["short_name_en"] = c.short_name_en
                companyInfo["logo"] = ""
                companyInfo["company_field"] = c.invest_field
                companyInfo["has_user"] = False
                companyInfo["recommendReason"] = _("public company within the same industry")
                resultList.append(companyInfo)
                resultCount = resultCount + 1

    return resultList


@member_login_required
def add(request, follow_id):
    c = {}
    c['title'] = _("Add")
    c['member'] = request.session.get('member', None)
    c.update(csrf(request))
    p = Project()
    if follow_id == "1":
        p.is_follow = True
    else:
        p.is_follow = False
    _load_types(c)
    p.valid_day = 60
    c['u'] = p
    c['readSuitorRelate'] = False
    c['target_companies_count'] = 0
    c["curr_year"] = datetime.datetime.today().year
    c["last_year"] = datetime.datetime.today().year - 1
    return render_to_response("sales/"+request.lang+"/add.html", c, context_instance=RequestContext(request))
    # if request.method == "POST":
    #     try:
    #         name_en = request.POST["name_en"]
    #         name_cn = request.POST["name_cn"]
    #         if name_en == "" and name_cn == "":
    #             isvalid = False
    #             messages.warning(request, _("please input project name"))
    #         redirect_url = "sales.mylist_pending"
    #         submitStatus = request.POST["submitStatus"]
    #         if submitStatus == "draft":
    #             p.status = StatusProject.draft
    #             redirect_url = "sales.mylist_draft"
    #         else:
    #             p.status = StatusProject.pending
    #         if _bind_data(request, p):
    #             return redirect(redirect_url)
    #     except Exception, e:
    #         messages.error(request, e.message)
    #         logger.error('add project error!' + e.message)


@member_login_required
def detail(request,id):
    c = {}
    c['title'] = _("Detail")
    member = request.session.get('member', None)
    c['member'] = member
    member_id = request.session["member"]["id"]
    if Helper.hasAgentRole(member['company_type']):
        total = Project.objects.filter(status=StatusProject.approved, member_id=member_id).count()
        if total <= 0:
            messages.warning(request, _("Please submit a project before you visit the detail"))
            return render_to_response("services/error_message.html", c, context_instance=RequestContext(request))
    p = get_object_or_404(Project, pk=id)
    if p.status != StatusProject.approved and p.member_id != member_id:
        raise Http404
    member_id = request.session['member']['id']
    member = Member.objects.get(id=member_id)
    if p.is_suitor:
        if p.is_push_to_member(member) is False and p.member_id != member_id:
            messages.warning(request, _("not target"))
            return render_to_response("services/error_message.html", c, context_instance=RequestContext(request))
            # return HttpResponse(_("not target"))
    if p.member_id == member_id:
        c['is_own'] = True
    member.view_project(p)
    # _load_types(c)

    keywords_list=[]
    if request.lang == "en-us":
        for kv in ProjectKeywordEn.objects.filter(project=p):
            keywords_list.append(kv.keyword)
    else:
        for kv in ProjectKeyword.objects.filter(project=p):
            keywords_list.append(kv.keyword)

    p.keywords=','.join(keywords_list)

    c['u'] = p
    ss = p.project_stock_structure.all()
    c['curr_year'] = p.financial_year
    c['last_year'] = p.financial_year - 1
    c['last_year_before'] = p.financial_year - 2
    c['stockST'] = ss
    c['stockST_len'] = len(ss)
    # condition_1 = Q(status=StatusProject.approved)
    # condition_2 = Q(company_industry=p.company_industry)
    # if p.company_industry:
    #     if p.company_industry.level == 3:
    #         condition_2 = condition_2 | Q(company_industry=p.company_industry.father) | Q(company_industry=p.company_industry.father.father)
    #     elif p.company_industry.level == 2:
    #         condition_2 = condition_2 | Q(company_industry=p.company_industry.father)
    #
    # condition_2 = condition_1 & condition_2
    # c['recommend_list'] = Project.objects.values("id", "name_en", "name_cn", "features_cn", "features_en", "add_time").order_by("-pv", "-update_time").exclude(pk=id).filter(condition_2)[0 : 5]
    c['history_list'] = Project.objects.exclude(pk=id).filter(member_id=p.member_id, status=StatusProject.approved, is_anonymous=False).order_by("-id")[0 : 5]
    c['message_list'] = Message.objects.filter(type_relation=1, project=p, is_delete=0).order_by('-add_time')
    c['is_added_favorite'] = member.is_added_project_to_favorites(p)
    c['is_expired']=datetime.date.today() > p.expire_date

    url = "/detail.html"
    type = request.GET.get("type", "")
    c['type'] = type
    if type == "1":
        url = "/view.html"
    else:
        write_project_view_log(request,member,p, type)
    return render_to_response("sales/"+request.lang+ url, c, context_instance=RequestContext(request))


@member_login_required
def pdf(request,id):
    c = {}
    c['title']=_("Detail")

    c['member']=request.session.get('member', None)
    member_id = request.session['member']['id']
    member = Member.objects.get(pk=member_id)
    c.update(csrf(request))
    p = get_object_or_404(Project, pk=id)
    if p.status != StatusProject.approved and p.member_id != member_id:
        raise Http404
    if p.is_suitor:
        if p.is_push_to_member(member) is False and p.member_id != member_id:
            return HttpResponse(_("not target"))
    _load_types(c)
    line_text_num=68
    if request.is_cn:
        if p.company_intro_cn:
            n1=len(p.company_intro_cn)/line_text_num
            _temp_str_list=[]
            for i in range(0,n1+1):
                _temp_str_list.append(p.company_intro_cn[i*line_text_num:(i+1)*line_text_num])
            p.company_intro_cn='<br/>'.join(_temp_str_list)
        if p.features_cn:
            n1=len(p.features_cn)/line_text_num
            _temp_str_list=[]
            for i in range(0,n1+1):
                _temp_str_list.append(p.features_cn[i*line_text_num:(i+1)*line_text_num])
            p.features_cn='<br/>'.join(_temp_str_list)
        if p.company_industry_intro_cn:
            n1=len(p.company_industry_intro_cn)/line_text_num
            _temp_str_list=[]
            for i in range(0,n1+1):
                _temp_str_list.append(p.company_industry_intro_cn[i*line_text_num:(i+1)*line_text_num])
            p.company_industry_intro_cn='<br/>'.join(_temp_str_list)


    c['u'] = p
    keywords_list=[]
    if request.lang == "en-us":
        for kv in ProjectKeywordEn.objects.filter(project=p):
            keywords_list.append(kv.keyword)
    else:
        for kv in ProjectKeyword.objects.filter(project=p):
            keywords_list.append(kv.keyword)

    p.keywords=','.join(keywords_list)
    ss = p.project_stock_structure.all()
    c['curr_year'] = p.financial_year
    c['last_year'] = p.financial_year - 1
    c['stockST'] = ss
    c['stockST_len'] = len(ss)
    c['static_root']=settings.STATICFILES_DIRS[0]
    template = get_template("sales/"+request.lang+"/detail_pdf.html")
    html = template.render(Context(c))

   
    file = StringIO.StringIO()
    #file = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file)

    # Return PDF document through a Django HTTP response
    file.seek(0)
    pdf = file.read()
    file.close()            # Don't forget to close the file handle
    member.print_project(p)
    write_project_teaser_view_log(request,member,p)
    return HttpResponse(pdf, mimetype='application/pdf')


@member_login_required
def edit(request,id):
    c = {}
    c['title']=_("Edit")
    c['status'] = request.GET.get("status", 0)
    c['member']=request.session.get('member', None)
    member_id = c['member']['id']
    c.update(csrf(request))
    p = get_object_or_404(Project, pk=id, member_id=member_id)
    if p.financial_year is None and p.financial_year > 0:
        c['curr_year'] = p.financial_year
        c['last_year'] = p.financial_year - 1
    else:
        c["curr_year"] = datetime.datetime.today().year
        c["last_year"] = datetime.datetime.today().year - 1
    _load_types(c)
    c['u'] = p

    ss = p.project_stock_structure.all()
    c['target_companies_count'] = p.target_companies.all().count()
    c['readSuitorRelate'] = True
    c['stockST'] = ss
    c['stockST_len'] = len(ss)
    c['attachments'] = p.project_attach.all()

    if request.lang == "en-us":
        mks = p.project_keyword_en.all()
    else:
        mks = p.project_keyword.all()
    c['mks'] = mks
    keywords = ""
    if len(mks) > 0:
        for m in mks:
            keywords += m.keyword + ","
        keywords = keywords[0 : len(keywords) - 1]
    c['keywords'] = keywords

    members = Member.objects.filter(company_id=27)
    _visitors = ProjectVisitor.objects.filter(project_id=id).exclude(member=members).order_by("-add_time")[0:5]
    visitors=[]
    for v in _visitors:
        if v.member.email.find('@newchama.com')!=0:
            visitors.append(v)

    c['visitors'] = visitors
    followers = Favorites.objects.filter(project_id=id)
    c['followers'] = followers.order_by("-add_time")[0:5]
    c['followers_count'] = followers.count()

    member =get_object_or_404(Member,id=member_id)
    write_project_edit_log(request,member,p)
    return render_to_response("sales/"+request.lang+"/add.html", c, context_instance=RequestContext(request))


def handle_dynamic_email_module(dic, project):
    publisher_company = "未公布"
    publisher_company = project.member.company.name_cn
    dic["publisher_company"] = publisher_company
    dic["link"] = _get_project_link(str(project.id))
    dic["p"] = project

    currency_type = project.get_currency_type_service_display
    if project.deal_size and currency_type:
        dic["table_head_2"] = "融资规模"
        dic["table_column_2"] = myTags.formatCurrency2(project.deal_size, project.currency_type_service)
    else:
        dic["table_head_2"] = "所在行业"
        industry_name = "N/A"
        if project.company_industry:
            industry_name = project.company_industry.name_cn
        dic["table_column_2"] = industry_name

    if project.project_stage and project.service_type == 2:
        dic["table_head_3"] = "融资阶段"
        dic["table_column_3"] = project.get_project_stage_display
    else:
        mks = project.project_keyword.all()
        keywords = []
        if len(mks) > 0:
            dic["table_head_3"] = "关键词"
            for m in mks:
                keywords.append(m.keyword)
            dic["table_column_3"] = keywords[0]
            if len(keywords) >= 2:
                if (len(keywords[0]) + len(keywords[1])) < 16:
                    dic["table_column_3"] = keywords[0] + "," + keywords[1]

    return dic


@member_login_required
def view_email(request, id):
    dic = {}
    dic['member']=request.session.get('member', None)
    member_id = dic['member']['id']
    project = get_object_or_404(Project, pk=id, member_id=member_id)
    dic = handle_dynamic_email_module(dic, project)

    dic["user_name"] = "某某用户"

    return render_to_response("sales/"+request.lang+"/view_email.html", dic, context_instance=RequestContext(request))


@member_login_required
def save(request):
    response_data = {}
    response_data['result'] = 'failed'
    if request.method == "POST":
        try:
            name_en = request.POST["name_en"]
            name_cn = request.POST["name_cn"]
            if name_en == "" and name_cn == "":
                response_data['message'] = _("please input project name")
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
                p = Project()
                isExsit = False
                id_post = request.POST.get("id", False)
                #check the project is exsit
                condition = Q(member_id=request.session["member"]["id"])
                condition2 = Q()
                if id_post:
                    condition = condition & ~Q(pk=id_post)
                if name_cn.strip() != "":
                    condition2 = condition2 | Q(name_cn=name_cn.strip())

                if name_en.strip() != "":
                    condition2 = condition2 | Q(name_en=name_en.strip())

                project = Project.objects.filter(condition & condition2)
                if project:
                    isExsit = True
                    response_data['message'] = "projectExsit"

                if isExsit is False:
                    if id_post:
                        p = Project.objects.get(pk=id_post)
                    if p.status != StatusProject.approved:              #Terry mark, when the project is approved then do not reset the pending status
                        if submitStatus == "draft":
                            p.status = StatusProject.draft
                        else:
                            p.status = StatusProject.pending
                    bool, msg = _bind_data(request, p)
                    if bool:
                        response_data['result'] = 'success'
                        response_data['project_title'] = p.name_cn
                        response_data['id'] = p.id
                        response_data['message'] = '操作成功'
                        # need_match = int(request.POST["need_match"], 0)
                        # if need_match == 1:
                        #     update_recommond_project(p)
                    else:
                        response_data['message'] = msg
        except Exception, e:
            logger.error(e.message)
            response_data['message'] = e.message
    return HttpResponse(simplejson.dumps(response_data), content_type="text/plain")


@member_login_required
def sync_recommond(request):
    result = "success"
    try:
        if request.method == "POST":
            id_post = request.POST.get("id", False)
            if id_post:
                p = Project.objects.get(pk=id_post)
                # ProjectTargetCompanyDetail.objects.filter(project=p).delete()         #delete the forignkey first
                update_recommond_project(p)
                result = "success"
    except Exception, e:
        print e.message
        logger.error(e.message)
    return HttpResponse(result)


@member_login_required
def json_recommend(request):
    c = {}
    c["have_more_data"] = False
    id_post = request.POST.get("id", False)
    url = "/json_recommend.html"
    if request.method == "POST":
        try:
            page = request.POST.get('page', 1)
            pagesize = int(request.POST.get('pagesize', 10))
            position = request.POST.get('position', False)

            if page <= 1:
                page = 1
            if pagesize <= 1:
                pagesize = 1
            start_record = (int(page)-1) * pagesize
            end_record = int(start_record) + pagesize

            if position == "control":
                url = "/json_control_panel.html"
                recommendList = list(ProjectTargetCompanyDetail.objects.filter(project_id=id_post, is_delete=False).exclude(status=StatusProject.approved).order_by('-id'))[start_record : end_record]
                c["recommendList"] = recommendList
                c["have_more_data"] = len(recommendList) == pagesize
            else:
                ptc = ProjectTargetCompanyDetail.objects.filter(project_id=id_post, is_delete=False)
                potentialNum = int(request.POST.get('potentialNum', 0))
                if end_record > potentialNum and start_record < potentialNum and potentialNum != 0:
                    end_record = potentialNum
                elif start_record > potentialNum and potentialNum != 0:
                    start_record = 0
                    end_record = 0
                if start_record == 0 and end_record == 0:
                    c["rcommendList"] = None
                else:
                    condition = json_recommend_condition(request, id_post)
                    recommendList = list(RecommondItem.objects.filter(condition).exclude(project_recommond_item=ptc).order_by('-is_man', '-sum_score','-company_score_has_invest_field','-project_score_local','-company_score_local'))[start_record : end_record]
                    c["recommendList"] = recommendList
                    c["have_more_data"] = len(recommendList) == pagesize
                for rc_item in c["recommendList"]:
                    if rc_item.target_reason=="Relevant Portfolio Company":
#                        rc_item.investment_history=CompanyInvestmentHistory.objects.filter(company=rc_item.company).values('targetcompany_cn').distinct().order_by('-id')[:3]
                        rc_item.investment_history=CompanyInvestmentHistory.objects.filter(company=rc_item.company).exclude(targetcompany_cn__isnull=True, targetcompany_cn='N/A').values('targetcompany_cn').distinct().order_by('targetcompany_cn')[:3]

            # _recommendList = list(RecommondItem.objects.filter(project=project,is_man=True,is_delete=False).order_by('-rank'))[0:5]
            #_recommendList += list(RecommondItem.objects.filter(project=project,is_man=False,sum_project_score__gte=50).order_by('-sum_project_score'))[0:5]
        except Exception, e:
            logger.error(e.message)
    return render_to_response("sales/"+request.lang+url, c, context_instance=RequestContext(request))


@member_login_required
def json_recommend_count(request):
    count = 0
    id_post = request.POST.get("id", False)
    if request.method == "POST":
        try:
            if id_post:
                ptc = ProjectTargetCompanyDetail.objects.filter(project_id=id_post, is_delete=False)
                condition = json_recommend_condition(request, id_post)
                count = RecommondItem.objects.filter(condition).exclude(project_recommond_item=ptc).count()
                count = Helper.checkCountMatch(count)
        except Exception, e:
            logger.error(e. message)
    return HttpResponse(count)


@member_login_required
def json_recommend_condition(request, id_post):
    condition = Q(project_id=id_post, is_delete=False, target_reason__isnull=False)
    condition2 = Q()

    target_location_id = request.POST.get('target_location_id', 0)
    target_industry_id = request.POST.get('target_industry_id', 0)
    target_location_type = request.POST.get('target_location_type', 0)
    target_reasons = request.POST.get('target_reasons', False)
    if target_location_id != "0":
        if target_location_type == "province":
            condition2 = condition2 | Q (province_id=target_location_id)
        else:
            condition2 = condition2 | Q (country_id=target_location_id)
    if target_industry_id != "0":
        condition2 = condition2 | Q (industry_id=target_industry_id)
    company = Company.objects.filter(condition2).exclude(id=27)
    if target_reasons:
        trs = target_reasons.split(",")
        condition = condition & Q (target_reason__in=trs)
    if target_location_id != "0" or target_industry_id != "0":
        condition = condition & Q (company=company)
    return condition

@member_login_required
def bankingGenuisSave(request):
    response_data = {}
    response_data['result'] = 'error'
    if request.method == "POST":
        try:
            operate = int(request.POST.get('operate', 99))          #99 表示異常傳遞數據
            itemIds = request.POST.get('itemIds', False)            #recommend　ｉｄ
            companyIds = request.POST.get('companyIds', False)      #公司　ｉｄ
            project_id = request.POST.get('projectId', False)
            needSendEmailMember = []       #need send email company
            noteBDToFollow = []

            project = Project.objects.get(id=project_id)
            if operate < 6:
                cids = companyIds.split(",")
                if itemIds:
                    iids = itemIds.split(",")
                    for itemId, company_id in zip(iids, cids):
                        ptod = ProjectTargetCompanyDetail()
                        ptod.project_id = project_id
                        ptod.company_id = company_id
                        ptod.recommondItem_id = itemId
                        ptod.member_id = request.session['member']['id']
                        ptod.recommend_type = 2
                        ptod.status = operate
                        if project.status == StatusProject.approved:
                            ptod.is_sender = 1
                        ptod.save()
                        ri = RecommondItem.objects.get(id=itemId)
                        ri.is_in_control_panel = True
                        ri.save()
                        if operate == 1:
                            members = Member.objects.filter(company__id=company_id).values("id", "email", "first_name", "last_name")
                            if members:
                                needSendEmailMember.append(members)
                            else:
                                noteBDToFollow.append(company_id)
                else:
                    for company_id in cids:
                        ptod = ProjectTargetCompanyDetail()
                        ptod.project_id = project_id
                        ptod.company_id = company_id
                        ptod.member_id = request.session['member']['id']
                        ptod.recommend_type = 2
                        ptod.status = operate
                        if project.status == StatusProject.approved:
                            ptod.is_sender = 1
                        ptod.save()
                        response_data['editId'] = ptod.id
                        if operate == 1:
                            members = Member.objects.filter(company__id=company_id).values("id", "email", "first_name", "last_name")
                            if members:
                                needSendEmailMember.append(members)
                            else:
                                noteBDToFollow.append(company_id)
                response_data['result'] = 'success'

            if operate == 1 and project.status == StatusProject.approved:
                send_push_email(request, needSendEmailMember, noteBDToFollow, project)
            #add to favorite
            # elif operate == 2:
            result = 'success'
            # response_data['id'] = p.id
        except Exception, e:
            logger.error(e.message)
            response_data['message'] = e.message
    return HttpResponse(simplejson.dumps(response_data), content_type="text/plain")


def send_push_email(request, needSendEmailMember, noteBDToFollow, project):
    if needSendEmailMember:
        for mrs in needSendEmailMember:
            if len(mrs) > 0:
                for mr in mrs:
                    if mr["email"]:
                        dic = {}
                        dic = handle_dynamic_email_module(dic, project)
                        if mr["first_name"].strip() or mr["last_name"].strip():
                            dic["user_name"] = mr["first_name"]# + " " + mr["last_name"]
                        html_content = loader.render_to_string("sales/"+request.lang+"/email_push.html", dic)

                        #emailAccount.append("richard@newchama.com")
                        emailAccount = mr["email"]
                        title = "Newchama用户项目推荐"
                        try:
                            send_email_by_mq('email', 'email', title, emailAccount, html_content)
                        except Exception, e:
                            msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [emailAccount])
                            msg.content_subtype = "html"  # Main content is now text/html
                            msg.send()

                    autoMsg = Message()
                    autoMsg.project_id = project.id
                    autoMsg.type_relation = 1
                    autoMsg.sender_id = request.session['member']['id']
                    autoMsg.receiver_id = mr["id"]
                    # autoMsg.is_read = 1             #set is_read has already read when use recommond click
                    autoMsg.content = "[推送]您好，这是我的项目Teaser。若您对此感兴趣，欢迎与我取得联系。"
                    #autoMsg.content = loader.render_to_string("sales/"+request.lang+"/message.html", dic)
                    autoMsg.save()
                    Helper.update_message_log(autoMsg)
    if noteBDToFollow:
        noEmailcompanies = Company.objects.filter(id__in=noteBDToFollow)
        dic = {'link': _get_project_link(project_id), 'noEmailcompanies': noEmailcompanies, 'projectName': project.name_cn}
        html_content = loader.render_to_string("sales/"+request.lang+"/email_not_push.html", dic)
        # noPublishemail = "Terry@newchama.com"
        noPublishemail = "paul@newchama.com"
        #logger.debug("send email to " + str(emailAccount))
        title='Newchama未成功推送项目提醒'
        try:
            _send_email_by_mq('email', 'email', title, noPublishemail, html_content)
        except Exception, e:
            msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [noPublishemail])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()


@member_login_required
def bankingGenuisExcute(request):
    result = "error"
    if request.method == "POST":
        try:
            operate = int(request.POST.get('operate', 99))          #99 表示異常傳遞數據
            ptodId = request.POST.get('ptodId', False)
            if ptodId and operate != 99:
                ptod = ProjectTargetCompanyDetail.objects.get(pk=ptodId)
                ptod.status = operate
                ptod.save()
                result = 'success'
                if operate == 1:
                    project = Project.objects.get(pk=ptod.project_id)
                    if project.status == StatusProject.approved:
                        needSendEmailMember = []       #need send email company
                        noteBDToFollow = []
                        company_id = ptod.company_id
                        members = Member.objects.filter(company__id=company_id).values("id", "email", "first_name", "last_name")
                        if members:
                            needSendEmailMember.append(members)
                        else:
                            noteBDToFollow.append(company_id)
                        send_push_email(request, needSendEmailMember, noteBDToFollow, project)
            # response_data['id'] = p.id
        except Exception, e:
            logger.error(e.message)
    return HttpResponse(result)


@member_login_required
def send_extenal_email(request):
    result = "success"
    if request.method == "POST":
        email_list = []
        html_content = ""
        title = "Newchama用户项目推荐"
        try:
            id_post = request.POST.get("id", False)
            emails = request.POST.get("other_email")
            if id_post:
                p = Project.objects.get(pk=id_post)
                if p.status != StatusProject.approved:
                    result = "not approved"
                    return HttpResponse(result)
                dic = {}
                dic = handle_dynamic_email_module(dic, p)
                html_content = loader.render_to_string("sales/"+request.lang+"/email_extenal.html", dic)
                email_list = emails.split(";")
                for e in email_list:
                    send_email_by_mq('email', 'email', title, e, html_content)
        except Exception, e:
            try:
                for item in email_list:
                    msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [item[0]])
                    msg.content_subtype = "html"
                    msg.send()
                    logger.debug("send email successfully.")
            except Exception, e:
                logger.error(e.message)
            logger.error(e.message)
        member_id = request.session['member']['id']
        member = get_object_or_404(Member, id=member_id)
        if len(email_list) > 0:
            write_extenal_mail_log(request, member, p, email_list)
    return HttpResponse(result)


@member_login_required
def _bind_data(request, p):
    # try:
        has_attach = False
        upload_types = request.POST.getlist("upload_types", [])
        for ut in upload_types:
            uf = request.FILES.get("upload_file_" + ut, False)
            if uf:
                file_ext = os.path.splitext(uf.name)[1].lower()
                if uf:
                    if uf.size > 20000000:
                        return False, "tooBig"
                        # msg = _("The file cannot be more than 20M")
                    if file_ext != ".doc" and file_ext != ".docx" and file_ext != ".pdf" and file_ext != ".ppt" and file_ext != ".pptx":
                        # msg = _("The file must be 'doc|docx|pdf'")
                        return False, "typeError"
                    has_attach = True

        integrity = 0
        if request.session.get('member'):
            p.member_id = request.session["member"]["id"]
        p.name_cn = request.POST["name_cn"]
        p.name_en = request.POST["name_en"]
        if request.POST.get("name_cn", False) or request.POST.get("name_en", False):
            integrity = integrity + 1

        service_type = int(request.POST.get("service_type"), 0)
        if service_type != 0:
            p.service_type = service_type
            integrity = integrity + 1

        pay_currency = int(request.POST.get("pay_currency"), 0)
        if pay_currency != 0:
            p.pay_currency = pay_currency
            integrity = integrity + 1

        project_relation = int(request.POST.get("project_relation"), 0)
        if project_relation != 0:
            p.project_relation = project_relation
            integrity = integrity + 1

        p.features_cn = request.POST.get("features_cn", None)
        p.features_en = request.POST.get("features_en", None)
        if request.POST.get("features_cn", False) or request.POST.get("features_en", False):
            integrity = integrity + 1

        valid_day = int(request.POST.get("valid_day", 0))
        p.valid_day = valid_day

        p.expire_date = datetime.datetime.today() + datetime.timedelta(days=int(valid_day))
        integrity = integrity + 1

        p.is_anonymous = int(request.POST.get("is_anonymous", 0))#request.POST.get("is_anonymous", False)
        integrity = integrity + 1

        exist_upload_names = request.POST.getlist("exist_upload_names", [])
        if has_attach or exist_upload_names:
            integrity = integrity + 1
            p.has_attach = True
        else:
            p.has_attach = False

        if request.POST.get("company_name_cn", False) or request.POST.get("company_name_en", False):
            p.company_name_cn = request.POST["company_name_cn"]
            p.company_name_en = request.POST.get("company_name_en", None)
            integrity = integrity + 1

        company_country = request.POST.get("company_country", False)
        if company_country != 0 and company_country and company_country != "0":
            p.company_country_id = company_country
            integrity = integrity + 1

        company_province = request.POST.get("company_province", False)
        if company_province != 0 and company_province and company_province != "0":
            p.company_province_id = company_province

        #if class3 got a result then industry_id value is company_industry_2
        #else if class2 got a result then industry_id value is company_industry_1
        #else class industry_id value is company_industry_0
        industry_id = request.POST.get("industry_id", False)
        if industry_id != 0 and industry_id and industry_id != "0":
            p.company_industry_id = industry_id
            integrity = integrity + 1

        company_industry_2 = request.POST.get("company_industry_2", False)
        if company_industry_2 != 0 and company_industry_2 and company_industry_2 != "0":
            p.cv3 = company_industry_2

        company_industry_1 = request.POST.get("company_industry_1", False)
        if company_industry_1 != 0 and company_industry_1 and company_industry_1 != "0":
            p.cv2 = company_industry_1

        company_industry_0 = request.POST.get("company_industry_0", False)
        if company_industry_0 != 0 and company_industry_0 and company_industry_0 != "0":
            p.cv1 = company_industry_0

        #keywords in the end of function

        employees_count_type = request.POST.get("employees_count_type", False)
        if employees_count_type != 0 and employees_count_type and employees_count_type != "0":
            p.employees_count_type = employees_count_type
            integrity = integrity + 1

        p.is_list_company = int(request.POST.get("is_list_company", 0))#request.POST.get("is_list_company", False)

        if request.POST.get("company_stock_symbol", False):
            p.company_stock_symbol = request.POST.get("company_stock_symbol", False)
        integrity = integrity + 1

        #s_rate
        p.currency_type_financial = request.POST.get("currency_type_financial", None)
        integrity = integrity + 1

        expected_enterprice_value = request.POST.get("expected_enterprice_value", False)
        if expected_enterprice_value and expected_enterprice_value != "":
            p.expected_enterprice_value = expected_enterprice_value.replace(",", "")
            integrity = integrity + 1

        stock_percent = request.POST.get("stock_percent", False)
        if stock_percent and stock_percent != "":
            p.stock_percent = stock_percent
            integrity = integrity + 1

        deal_size = request.POST.get("deal_size", False)
        if deal_size and deal_size != "":
            p.deal_size = deal_size.replace(",", "")
            integrity = integrity + 1

        p.financial_year = request.POST.get("financial_year", datetime.datetime.today().year)

        income_last_phase = request.POST.get("income_last_phase", False)
        if income_last_phase and income_last_phase != "":
            p.income_last_phase = income_last_phase.replace(",", "")
            integrity = integrity + 1

        income_last_phase_2 = request.POST.get("income_last_phase_2", False)
        if income_last_phase_2 and income_last_phase_2 != "":
            p.income_last_phase_2 = income_last_phase_2.replace(",", "")
            integrity = integrity + 1

        income_last_phase_3 = request.POST.get("income_last_phase_3", False)
        if income_last_phase_3 and income_last_phase_3 != "":
            p.income_last_phase_3 = income_last_phase_3.replace(",", "")
            integrity = integrity + 1

        profit_last_phase = request.POST.get("profit_last_phase", False)
        if profit_last_phase and profit_last_phase != "":
            p.profit_last_phase = profit_last_phase.replace(",", "")
            integrity = integrity + 1

        profit_last_phase_2 = request.POST.get("profit_last_phase_2", False)
        if profit_last_phase_2 and profit_last_phase_2 != "":
            p.profit_last_phase_2 = profit_last_phase_2.replace(",", "")
            integrity = integrity + 1

        profit_last_phase_3 = request.POST.get("profit_last_phase_3", False)
        if profit_last_phase_3 and profit_last_phase_3 != "":
            p.profit_last_phase_3 = profit_last_phase_3.replace(",", "")
            integrity = integrity + 1

        ebitda = request.POST.get("ebitda", False)
        if ebitda and ebitda != "":
            p.ebitda = ebitda.replace(",", "")
            integrity = integrity + 1

        ebitda_2 = request.POST.get("ebitda_2", False)
        if ebitda_2 and ebitda_2 != "":
            p.ebitda_2 = ebitda_2.replace(",", "")
            integrity = integrity + 1

        ebitda_3 = request.POST.get("ebitda_3", False)
        if ebitda_3 and ebitda_3 != "":
            p.ebitda_3 = ebitda_3.replace(",", "")
            integrity = integrity + 1

        p.audit_status = int(request.POST.get("audit_status", 0))
        integrity = integrity + 1

        p.audit_status_2 = int(request.POST.get("audit_status_2", 0))
        integrity = integrity + 1

        p.audit_status_3 = int(request.POST.get("audit_status_3", 0))
        integrity = integrity + 1

        p.is_suitor = int(request.POST.get("is_suitor", 0))
        p.process = request.POST.get("process", 0)

        '''
            no input start
       '''
        #是否需要审计、上市公司、匿名发布和财务货币单位为三个必填项+3
        financial_is_audit = int(request.POST.get("financial_is_audit", 0))
        if financial_is_audit == 0:
            p.financial_is_audit = False
        else:
            p.financial_is_audit = True
        if financial_is_audit == 1:
            p.financial_audit_company_is_default = True
        elif financial_is_audit == 2:
            p.financial_audit_company_is_default = False

        p.financial_audit_company_name = request.POST.get("financial_audit_company_name", None)

        price_min = request.POST.get("price_min", False)
        if price_min and price_min != "":
            p.price_min = price_min.replace(",", "")

        price_max = request.POST.get("price_max", False)
        if price_max and price_max != "":
            p.price_max = price_max.replace(",", "")

        income = request.POST.get("income", False)
        if income and income != "":
            p.income = income.replace(",", "")

        profit = request.POST.get("profit", False)
        if profit:
            p.profit = profit.replace(",", "")

        registered_capital = request.POST.get("registered_capital", False)
        if registered_capital and registered_capital != "":
            p.registered_capital = registered_capital.replace(",", "")

        growth_three_year = request.POST.get("growth_three_year", False)
        if growth_three_year and growth_three_year != "":
            p.growth_three_year = growth_three_year

        p.company_intro_cn = request.POST.get("company_intro_cn", None)
        p.company_intro_en = request.POST.get("company_intro_en", None)
        #if request.POST.get("company_intro_cn", False) or request.POST.get("company_intro_en", False):
        #    integrity = integrity + 1

        p.company_industry_intro_cn = request.POST.get("company_industry_intro_cn", None)
        p.company_industry_intro_en = request.POST.get("company_industry_intro_en", None)
        #if request.POST.get("company_industry_intro_cn", False) or request.POST.get("company_industry_intro_en", False):
        #    integrity = integrity + 1

        p.lock_date = request.POST.get("lock_date", None)
        #if request.POST.get("lock_date", False):
        #    integrity = integrity + 1

        p.is_public = int(request.POST.get("is_public", 0))
        p.is_agent_project = int(request.POST.get("is_agent_project", 0))

        project_stage = request.POST.get("project_stage", False)
        if project_stage and project_stage != "":
            p.project_stage = project_stage

        income_type = request.POST.get("income_type", False)
        if income_type and income_type != "":
            p.income_type = income_type

        profit_type = request.POST.get("profit_type", False)
        if profit_type and profit_type != "":
            p.profit_type = profit_type

        total_assets_last_phase = request.POST.get("total_assets_last_phase", False)
        if total_assets_last_phase and total_assets_last_phase != "":
            p.total_assets_last_phase = total_assets_last_phase.replace(",", "")

        total_assets_last_phase_2 = request.POST.get("total_assets_last_phase_2", False)
        if total_assets_last_phase_2 and total_assets_last_phase_2 != "":
            p.total_assets_last_phase_2 = total_assets_last_phase_2.replace(",", "")

        total_assets_last_phase_3 = request.POST.get("total_assets_last_phase_3", False)
        if total_assets_last_phase_3 and total_assets_last_phase_3 != "":
            p.total_assets_last_phase_3 = total_assets_last_phase_3.replace(",", "")

        #if total_assets_last_phase or total_assets_last_phase_2 or total_assets_last_phase_3:
        #    integrity = integrity + 1

        target_companies = request.POST.getlist("target_companies", [])
        if target_companies:
            p.target_companies = target_companies
        #    integrity = integrity + 1
        '''
            no input end
        '''
        p.save()

        p.project_attach.all().delete()
        exist_upload_newNames = request.POST.getlist("exist_upload_newNames", [])
        upload_type_names = request.POST.getlist("upload_type_names", [])
        # upload_types = request.POST.getlist("upload_types", [])
        for ut, tn in zip(upload_types, upload_type_names):
            uf = request.FILES.get("upload_file_" + ut, False)
            if uf:
                # if uf.size > 2000000:
                #     messages.error(request, _("The file cannot be more than 2M"))
                #     return
                pa = ProjectAttach()
                pa.project = p
                pa.file_name = uf.name
                pa.file_type = ut
                pa.file_type_name = tn
                pa.new_name = _upload_project_file(uf)
                pa.save()
            else:
                for t, f, n in zip(upload_types, exist_upload_names, exist_upload_newNames):    #if upload not exsit, check the file that has already exsit file
                    if t == ut:
                        pa = ProjectAttach()
                        pa.project = p
                        pa.file_name = f
                        pa.file_type = ut
                        pa.file_type_name = tn
                        pa.new_name = n
                        pa.save()
                        break

        s_rate = request.POST.getlist("s_rate", [])
        p.project_stock_structure.all().delete()
        if s_rate is not None:
            integrity = integrity + 1
            for i in s_rate:
                s = StockStructure()
                s.project = p
                if i:
                    s.rate = i
                s.save()

        project_keyword = request.POST.get("project_keyword", False)
        if request.lang == "en-us":
            p.project_keyword_en.all().delete()
        else:
            p.project_keyword.all().delete()
        if project_keyword:
            integrity = integrity + 1
            mks = project_keyword.split(",")
            for m in mks:
                if request.lang == "en-us":
                    k = ProjectKeywordEn()
                else:
                    k = ProjectKeyword()
                k.keyword = m
                k.project = p
                k.save()
        integrity = int(integrity * 100 / 31)
        if request.lang == "zh-cn":
            p.integrity = integrity
        else:
            p.integrity_en = integrity
        p.save()
        return True, "ok"


def _get_project_link(id):
    return 'http://www.newchama.com/sales/detail/' + id + '/'

'''
def save_recommend_company(request):
    msg = ""
    try:
        if request.method == 'POST':
            ids = request.POST.get("id", "").split(",")
            projectId = request.POST.get("projectId")
            project = Project.objects.get(id=projectId)
            targetCompanyIds = []           #the exsit company in exsit project
            needSendEmailMember = []       #need send email company
            noteBDToFollow = []

            exsitTargetCompanies = project.target_companies.all()
            for tp in exsitTargetCompanies:
                targetCompanyIds.append(tp.id)
            for id in ids:
                if checkTargetCompanyIsExsit(id, exsitTargetCompanies) is not True:
                    targetCompanyIds.append(id)
                    ptod = ProjectTargetCompanyDetail()
                    ptod.project = project
                    ptod.member_id = request.session['member']['id']
                    ptod.company_id = id
                    ptod.recommend_type = 2
                    ptod.save()
                    members = Member.objects.filter(company__id=id).values("id", "email", "first_name", "last_name")
                    if members:
                        needSendEmailMember.append(members)
                    else:
                        noteBDToFollow.append(id)

            project.target_companies = set(targetCompanyIds)
            project.save()

            #start send email
            if project.status == StatusProject.approved:
                if needSendEmailMember:
                    email_list=[]
                    content_list=[]
                    for mrs in needSendEmailMember:
                        if len(mrs) > 0:
                            for mr in mrs:
                                if mr["email"]:
                                    emailAccount = []
                                    dic = {}
                                    if mr["first_name"].strip() or mr["last_name"].strip():
                                        dic["userName"] = mr["first_name"] + "" + mr["last_name"]
                                    dic["link"] = _get_project_link(projectId)
                                    if project.name_cn.strip() != "":
                                        dic["projectName"] = project.name_cn
                                    else:
                                        dic["projectName"] = project.name_en

                                    html_content = loader.render_to_string("sales/"+request.lang+"/email_push.html", dic)
                                    content_list.append(html_content)
                                    
                                    emailAccount.append(mr["email"])
                                    email_list.append(emailAccount)
                                    
                                autoMsg = Message()
                                autoMsg.project_id = projectId
                                autoMsg.type_relation = 1
                                autoMsg.sender_id = request.session['member']['id']
                                autoMsg.receiver_id = mr["id"]
                                autoMsg.is_read = 1             #set is_read has already read when use recommond click
                                autoMsg.content = "您好，这是我的项目Teaser。若您对此感兴趣，欢迎与我取得联系。"
                                #autoMsg.content = loader.render_to_string("sales/"+request.lang+"/message.html", dic)
                                autoMsg.add_time = datetime.datetime.now()
                                autoMsg.save()

                    title=_('NewChama Project Message')
                    try:
                       
                        send_email_by_mq_multiple('email','email',title,email_list,content_list)

                    except Exception, e:
                        for item in zip(email_list,content_list):
                            msg = EmailMessage(title, item[1], EMAIL_HOST_USER, item[0])
                            msg.content_subtype = "html"  # Main content is now text/html
                            msg.send()
                            logger.debug("send email successfully.")


                if noteBDToFollow:
                    noEmailcompanies = Company.objects.filter(id__in=noteBDToFollow)
                    dic = {'link': _get_project_link(projectId), 'noEmailcompanies': noEmailcompanies, 'projectName': project.name_cn}
                    html_content = loader.render_to_string("sales/"+request.lang+"/email_not_push.html", dic)
                    noPublishemail = []
                    # noPublishemail.append("Terry@newchama.com")
                    noPublishemail.append("paul@newchama.com")
                    #logger.debug("send email to " + str(emailAccount))
                    
                    title=_('NewChama unsuccess push Message')
                    try:
                       
                        send_email_by_mq('email','email',title,set(noPublishemail),html_content)

                    except Exception, e:
                        msg = EmailMessage(title, html_content, EMAIL_HOST_USER, set(noPublishemail))
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()

                    logger.debug("send email successfully.")
                # send email end
            msg = "success"
        else:
            msg = _("error")
    except Exception, e:
        logger.error(e.message)
        msg = _("error")
    return HttpResponse(msg)
'''

def checkTargetCompanyIsExsit(id, exsitTargetCompanies):
    for etc in exsitTargetCompanies:
        if id == etc.id:
            return True
    else:
        return False


def _load_types(c):
    curr_year = datetime.datetime.today().year
    history_year = []
    for i in range(curr_year):
        if i == 4:
            break
        history_year.append(curr_year - i)
    c["history_year"] = history_year
    c["members"] = Member.active_list()
    c['countries'] = Helper.find_countries()
    c['industries'] = Helper.find_industries_level1()
    c["companies"] = Company.active_list()
    c['audits'] = AccountingFirm.objects.all()
    c['stockStructureType'] = StockStructure.TYPES
    c['projectServiceType'] = ProjectServiceType
    c['list_companies'] = ListedCompany.objects.all().values("id", "stock_symbol", "stock_exchange", "name_cn", "name_en", "short_name_cn", "short_name_en")


@csrf_exempt
@member_login_required
def remove_file(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Project.objects.filter(pk=id).update(upload_file='', is_public=0)
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


def _upload_project_file(f):
    file_name = ""
    path = settings.MEDIA_ROOT + "/project/"
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


@csrf_exempt
@member_login_required
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
                
                p=Project.objects.get(pk=id, member_id=member_id)
                p.status=StatusProject.deleted
                p.save()

                write_project_delete_log(request, member, p)
                msg = "success"
            except Exception, e:
                logger.error(e.message)
                print e
                msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@member_login_required
def pending(request):
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

                p=Project.objects.get(pk=id, member_id=member_id)
                p.status=StatusProject.pending
                p.save()

                write_project_pending_log(request, member, p)
                msg = "success"
            except Exception, e:
                logger.error(e.message)
                print e
                msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@member_login_required
def offline(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        member = request.session.get('member', None)
        if member is None:
            msg = "nologon"
        else:
            try:
                member_id = request.session['member']['id']
                member=get_object_or_404(Member,id=member_id)
                
                p=Project.objects.get(pk=id, member_id=member_id)
                p.status=StatusProject.offline
                p.save()
                write_project_offline_log(request, member, p)

                msg = "success"
            except Exception, e:
                msg = e.message
    return HttpResponse(msg)


@member_login_required
def download_attach(request, id):
    project = get_object_or_404(Project, pk=id)
    member_id = request.session['member']['id']
    member = Member.objects.get(pk=member_id)
    if project.status != StatusProject.approved and project.member_id != member_id:
        raise Http404
    if project.project_attach.count() == 0:
        return HttpResponse(_("no attach"))
    if project.is_suitor:
        if project.is_push_to_member(member) is False and project.member_id != member_id:
            return HttpResponse(_("not target"))

    path = settings.MEDIA_ROOT + "/project/"
    #please view: http://stackoverflow.com/questions/12881294/django-create-a-zip-of-multiple-files-and-make-it-downloadable
    # Files (local path) to put in the .zip
    # FIXME: Change this (get paths from DB etc)
    #filenames = ["/tmp/file1.txt", "/tmp/file2.txt"]
    filenames = []
    for attach in project.project_attach.all():
        filenames.append(path+attach.new_name+"/"+attach.file_name)
    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    #zip_subdir = "somefiles"
    zip_subdir = project.name_cn
    if request.lang == "en-us":
        zip_subdir = project.name_en
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
    member.download_project_attach(project)
    return resp

@csrf_exempt
@member_login_required
def upload_file(request):
    path = settings.MEDIA_ROOT + "/sales/oneclick/"
    try:
        uploadfile = request.FILES.get("uploadFile")
        if uploadfile.size > 20000000:
            #return HttpResponse('{"status": "error", "message": " %s "}' % ugettext("The file cannot be more than 500K"))
            return HttpResponse('{"status": "error", "message": "tooBig"}')
        if not os.path.exists(path):
            os.makedirs(path)
        file_ext = os.path.splitext(uploadfile.name)[1].lower()
        if file_ext != ".doc" and file_ext != ".docx" and file_ext != ".pdf" and file_ext != ".ppt" and file_ext != ".pptx":
            return HttpResponse('{"status": "error", "message": "typeError"}')
        else:
            random_no = str(random.randint(0, 99999999)).zfill(8)
            # print random_no
            new_name = random_no + file_ext
            destination = open(path + new_name, 'wb+')
            for chunk in uploadfile.chunks():
                destination.write(chunk)
            destination.close()
            po = ProjectOneclickAttach()
            po.file_type = file_ext.lower()[1:]
            po.file_name = uploadfile.name
            po.new_name = new_name
            po.file_size = uploadfile.size
            po.member_id = request.session['member']['id']
            po.save()
            return HttpResponse('{"status": "success", "id": "' + str(po.id) + '"}')
    except Exception, e:
        logger.error('one click uploadfile error! ' + e.message)
        return HttpResponse('{"status": "error", "message": "operateError"}')

# @staticmethod
def find_projects(condition, page, pagesize, sort):
    project = Project.objects.all()
    if condition.keyword != "":
        project = project.filter(Q(name_cn__contains=condition.keyword) | Q(name_en__contains=condition.keyword))
        # logger.error("...........................condition.keyword = " + str(condition.keyword))
    if condition.keywords:
        condition2 = Q()
        for k in condition.keywords:
            condition2 = condition2 | Q (Q(name_cn__contains=k) | Q(name_en__contains=k))
            # logger.error("...........................condition.keywords = " + str(k))
        project = project.filter(condition2)
    if condition.type != 0 and condition.type != "" and condition.type != "0" and condition.type:
        project = project.filter(service_type=condition.type)
        # logger.error("...........................condition.type = " + str(condition.type))
    if condition.country_id != 0 and condition.country_id != "" and condition.country_id != "0" and condition.country_id:
        project = project.filter(Q(company_country__id=condition.country_id))
        # logger.error("...........................condition.country_id = " + str(condition.country_id))
    if condition.province_id != 0 and condition.province_id != "" and condition.province_id != "0" and condition.province_id:
        project = project.filter(Q(company_province__id=condition.province_id))
        # logger.error("...........................condition.province_id = " + str(condition.province_id))
    if condition.industry != 0 and condition.industry != "" and condition.industry is not None:
        project = project.filter(Q(company_industry_id=condition.industry) | Q(company_industry__father_id=condition.industry) | Q(company_industry__father__father_id=condition.industry))
        # logger.error("...........................condition.industry = " + str(condition.industry))
    if condition.member_id != 0 and condition.member_id != "":
        project = project.filter(member_id=condition.member_id)
        # logger.error("...........................condition.member_id = " + str(condition.member_id))
    if condition.status != -1 and condition.status != "":
        project = project.filter(status=condition.status)
        # logger.error("...........................condition.status = " + str(condition.status))
    if condition.dealsize_min != -1 and condition.dealsize_min != "" and condition.dealsize_min:
        condition.dealsize_min = int(condition.dealsize_min) #* 1000000
        project = project.filter(deal_size__gte=condition.dealsize_min)
        # logger.error("...........................condition.dealsize_min = " + str(condition.dealsize_min))
    if condition.dealsize_max != -1 and condition.dealsize_max != "" and condition.dealsize_max != "0" and condition.dealsize_max != 0 and condition.dealsize_max:
        condition.dealsize_max = int(condition.dealsize_max) #* 1000000
        project = project.filter(deal_size__lte=condition.dealsize_max)
        # logger.error("...........................condition.dealsize_max = " + str(condition.dealsize_max))
    if condition.service_type != 0 and condition.service_type != "" and condition.service_type != "0" and condition.service_type:
        project = project.filter(Q(service_type=condition.service_type))
        # logger.error("...........................condition.service_type = " + str(condition.service_type))
    if condition.project_stage != 0 and condition.project_stage != "" and condition.project_stage != "0" and condition.project_stage:
        project = project.filter(Q(project_stage=condition.project_stage))
        # logger.error("...........................condition.project_stage = " + str(condition.project_stage))
    if condition.currency_type != 0 and condition.currency_type != "" and condition.currency_type != "0" and condition.currency_type:
        project = project.filter(Q(pay_currency=condition.currency_type))
        # logger.error("...........................condition.currency_type = " + str(condition.currency_type))
    if page <= 1:
        page = 1
    if pagesize <= 1:
        pagesize = 1
    start_record = (int(page)-1) * int(pagesize)
    end_record = int(start_record) + int(pagesize)
    if sort == "":
        sort = "time_desc"
    if sort == "time_desc":
        project = project.order_by("-id")
    elif sort == "time_asc":
        project = project.order_by("id")
    elif sort == "size_desc":
        project = project.order_by("-deal_size")
    elif sort == "size_asc":
        project = project.order_by("deal_size")
    elif sort == "hot_desc":
        project = project.order_by("-pv")
    # logger.error(">>>>>>>>>>>>>>>>>> page = " + str(page) + "   pagesize=" + str(pagesize))
    total = project.count()
    # logger.error(">>>>>>>>>>>>>>>>>> start_record = " + str(start_record) + "   end_record=" + str(end_record))
    data = project[start_record:end_record]
    #logger.error(str(data))
    return data, total

