# -*- coding: utf-8 -*-  
from django.http import Http404
from django.shortcuts import render_to_response, redirect, RequestContext, get_object_or_404, HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from newchama.decorators import login_required, permission_required
from subscribe.models import Subscribe, SubscribeKeyword, SubscribeSendRecord
from member.models import Member
import run_subscribe
from django.db.models import Q
import logging

from log.views import *

logger = logging.getLogger(__name__)

@login_required
@permission_required("subscribe")
def index(request):
    c = {}
    keyword = request.GET.get("keyword", "")
    #tip_interval = request.GET.get("tip_interval", "")
    member = request.GET.get("member", "")
    condition = Q(is_delete=0)
    condition2 = Q()
    if keyword != "":
        condition2 = condition2 | Q (name_cn__icontains=keyword) #| Q(member__icontains=members)   #| Q (member.first_name__in=keyword) | Q (member.last_name__in=keyword)
    if member != "":
        members = Member.objects.filter(Q (first_name__icontains=keyword) | Q (last_name__icontains=keyword))
        condition2 = condition2 | Q(member__icontains=members)
    #if tip_interval != "":
    #    condition2 = condition2 | Q (tip_interval=tip_interval)

    c['keyword'] = keyword
    c['member'] = member
    #c['tip_interval'] = tip_interval
    c["data"] = Subscribe.objects.filter(condition & condition2).order_by("-id")
    return render_to_response("subscribe/index.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("subscribe")
def add(request):
    c = {}
    return render_to_response("subscribe/edit.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("subscribe")
def edit(request):
    c = {}
    return render_to_response("subscribe/edit.html", c, context_instance=RequestContext(request))


def match_project(request, id):
    c = {}
    s = Subscribe.objects.get(pk=id)
    if s:
        srs = run_subscribe.find_match_project(s).order_by("-id")
        c["result_list"] = srs
    srs = SubscribeSendRecord.objects.filter(subscribe_id=s.id)
    srs_ids = []
    for sr in srs:
        srs_ids.append(sr.subscribe_id)
    c['srs'] = srs_ids
    c['s'] = s
    return render_to_response("subscribe/project_list.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("subscribe")
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

                company_province = request.POST.get("province", False)
                if company_province and company_province != "0":
                    s.company_provinces_id = company_province

                industry_id = request.POST.get("industry_id", False)
                if industry_id != "0" and industry_id:
                    s.company_industries_id = industry_id

                company_industry_2 = request.POST.get("company_industry_2", False)
                if company_industry_2 != "0" and company_industry_2:
                    s.cv3 = company_industry_2

                company_industry_1 = request.POST.get("company_industry_1", False)
                if company_industry_1 != "0" and company_industry_1:
                    s.cv2 = company_industry_1

                company_industry_0 = request.POST.get("company_industry_0", False)
                if company_industry_0 != "0" and company_industry_0:
                    s.cv1 = company_industry_0

                s.deal_size_min = request.POST.get("deal_size_min")
                s.deal_size_max = request.POST.get("deal_size_max")
                s.member_id = request.session["member"]["id"]
                s.save()
                total_match = match_project(s)
                s.total_match = total_match
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

                response_data['result'] = 'success'
                response_data['id'] = s.id
                response_data['message'] = '操作成功'
        except Exception, e:
            logger.error(e.message)
            response_data['message'] = e.message
    return HttpResponse(simplejson.dumps(response_data), content_type="text/plain")
