# -*- coding: utf-8 -*-  
from django.http import Http404
from django.shortcuts import render_to_response, redirect, RequestContext, get_object_or_404, HttpResponse
from django.template.loader import get_template
from django.template import Context
from services.helper import Helper
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from newchama.helper import member_login_required
from services.models import Project, Country, StatusProject, ConditionProject
from subscribe.models import Subscribe, SubscribeKeyword, SubscribeSendRecord
from django.utils import simplejson
from sales.views import find_projects
from django.utils.translation import ugettext, ugettext_lazy as _
import logging

from log.views import *

logger = logging.getLogger(__name__)

@member_login_required
def index(request):
    c = {}
    c['member']=request.session.get('member', None)
    member_id = request.session['member']['id']
    data = Subscribe.objects.filter(member_id=member_id, is_delete=0).order_by("-id")
    if data:
        for d in data:
            d.total_match = match_project(d)
    c['data'] = data
    return render_to_response("subscribe/"+request.lang+"/index.html", c, context_instance=RequestContext(request))


def json(request):
    c = {}
    member_id = request.session['member']['id']
    data = Subscribe.objects.filter(member_id=member_id, is_delete=0).order_by("-id")
    c['data'] = data
    return render_to_response("subscribe/"+request.lang+"/json.html", c, context_instance=RequestContext(request))


@member_login_required
def add(request):
    c = {}
    c['member'] = request.session.get('member', None)
    _load_types(c)
    return render_to_response("subscribe/"+request.lang+"/edit.html", c, context_instance=RequestContext(request))


def _load_types(c):
    c['countries'] = Helper.find_countries()
    c['industries'] = Helper.find_industries_level1()
    p = Project()
    c['service_type'] = p.SERVICE_TYPES
    c['investment_stage'] = p.INVESTMENT_STAGE
    c['currency_type'] = p.PAY_CURRENCY


@member_login_required
def edit(request, id):
    c = {}
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    _load_types(c)
    s = Subscribe.objects.get(pk=id, member_id=member_id)
    mks = s.subscribe_keyword.all()
    c['mks'] = mks
    keywords = ""
    if len(mks) > 0:
        for m in mks:
            keywords += m.keyword + ","
        keywords = keywords[0 : len(keywords) - 1]
    c['keywords'] = keywords
    c['u'] = s
    return render_to_response("subscribe/"+request.lang+"/edit.html", c, context_instance=RequestContext(request))


def match_project(s):
    condition = ConditionProject()
    condition.keywords = []
    condition.status = StatusProject.approved
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
    data, total = find_projects(condition, 1, 1, "")
    return total


@member_login_required
def interval(request, id, interval):
    response_data = {}
    response_data["status"] = "error"
    if request.method == "POST":
        member_id = request.session['member']['id']
        s = Subscribe.objects.get(pk=id, member_id=member_id)
        s.tip_interval = interval
        s.save()
        response_data["status"] = "success"
    return HttpResponse(simplejson.dumps(response_data), content_type="text/plain")


@member_login_required
def delete(request, id):
    c = {}
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    del_subscribe = Subscribe.objects.get(pk=id, member_id=member_id)
    if del_subscribe:
        del_subscribe.is_delete = 1
        del_subscribe.save()
    return redirect("subscribe.index")


@csrf_exempt
@member_login_required
def save(request):
    response_data = {}
    response_data['result'] = 'failed'
    if request.method == "POST":
        try:
            name_cn = request.POST["name_cn"]
            if name_cn == "":
                response_data['message'] = _("please input project name")
            else:
                id_post = request.POST.get("id", '')
                s = Subscribe()
                if id_post != '':
                    s = Subscribe.objects.get(pk=id_post)
                s.name_cn = request.POST["name_cn"]

                if request.POST.get("service_type", False):
                    s.service_type = request.POST["service_type"]

                if request.POST.get("project_stage", False):
                    s.project_stage = request.POST["project_stage"]

                if request.POST.get("currency_type", False):
                    s.currency_type = request.POST["currency_type"]

                company_country = request.POST.get("country", False)
                if company_country and company_country != "0":
                    s.company_countries_id = company_country
                else:
                    s.company_countries = None

                company_province = request.POST.get("province", False)
                if company_province and company_province != "0":
                    s.company_provinces_id = company_province
                else:
                    s.company_provinces_id = None

                industry_id = request.POST.get("industry_id", False)
                if industry_id != "0" and industry_id:
                    s.company_industries_id = industry_id
                else:
                    s.company_industries_id = None

                company_industry_2 = request.POST.get("company_industry_2", False)
                if company_industry_2 != "0" and company_industry_2:
                    s.cv3 = company_industry_2
                else:
                    s.cv3 = None

                company_industry_1 = request.POST.get("company_industry_1", False)
                if company_industry_1 != "0" and company_industry_1:
                    s.cv2 = company_industry_1
                else:
                    s.cv2 = None

                company_industry_0 = request.POST.get("company_industry_0", False)
                if company_industry_0 != "0" and company_industry_0:
                    s.cv1 = company_industry_0
                else:
                    s.cv1 = None

                s.deal_size_min = request.POST.get("deal_size_min")
                s.deal_size_max = request.POST.get("deal_size_max")
                s.member_id = request.session["member"]["id"]
                s.save()
                project_keyword = request.POST.get("project_keyword", False)
                s.subscribe_keyword.all().delete()
                if project_keyword:
                    mks = project_keyword.split(",")
                    for m in mks:
                        k = SubscribeKeyword()
                        k.keyword = m
                        k.subscribe_id = s.id
                        k.save()
                # total_match = match_project(s)
                # s.total_match = total_match
                # s.save()

                response_data['result'] = 'success'
                response_data['id'] = s.id
                response_data['message'] = '操作成功'
        except Exception, e:
            logger.error(e.message)
            response_data['message'] = e.message
    return HttpResponse(simplejson.dumps(response_data), content_type="text/plain")