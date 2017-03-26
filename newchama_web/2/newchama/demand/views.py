#encoding:utf-8
from django.shortcuts import render_to_response, redirect, HttpResponse, RequestContext, get_object_or_404
from django.core.context_processors import csrf
from django.db.models import Max,Min
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from models import Demand, StatusDemand, DemandCheckLog, ResultsDemandCheck, DemandAttach, DemandIndustry, DemandKeyword, DemandKeywordEn, DemandKeywordAdmin,DemandRecommondReasonAdmin
from project.models import Project
from repository.models import AccountingFirm, ListedCompany, StockExchange, InvestmentHistory, InvestmentCompany
from industry.models import Industry
from area.models import Country, Province, City
from member.models import Member, Company
from adminuser.models import AdminUser
import datetime
from django.contrib import messages
from newchama.decorators import login_required, permission_required
from django.core.mail import send_mail, EmailMessage
from django.template import loader, Context
from newchama import settings
from newchama.settings import EMAIL_HOST_USER
from django.db.models import Q
from recommond.models import RecommondProjectItem
from recommond.compute_project_recommond import update_project_recommond_list
import random
import os
from django.utils import simplejson
# Create your views here.
import logging
from models import DemandRecommendLog, TypeDemandRecommend
logger = logging.getLogger(__name__)


@login_required
@permission_required("demand")
def index(request):
    c = {}
    download = request.GET.get("download", "")
    keyword = request.GET.get("keyword", "")
    status = request.GET.get("status", "")
    data = Demand.objects.all().order_by("-update_time")
    status = request.GET.get("status", "")

    condition = Q()
    condition2 = Q()
    if status != "":
        condition = Q(status=status)
        c["status"] = int(status)
    else:
        condition = ~Q(status=StatusDemand.deleted)

    if keyword.strip() != "":
        condition2 = condition2 | Q(name_cn__icontains=keyword.strip()) | Q(name_en__icontains=keyword.strip())
        c["keyword"] = keyword

    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    if start_date != "":
        condition = condition & Q(expire_date__gte=start_date)

    if end_date != "":
        condition = condition & Q(expire_date__lte=end_date)
    c['start_date'] = start_date
    c['end_date'] = end_date

    c["data"] = data.filter(condition & condition2)
    c['Status'] = StatusDemand
    c['StatusType'] = Demand.STATUS_TYPES
    c['total'] = data.count()
    if download != "":
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="demand.csv"'
        t = loader.get_template('demand/demand_download_template.txt')
        d = Context({
            'data': data,
        })
        response.write(t.render(d))
        return response
    return render_to_response("demand/list.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("demand")
@csrf_protect
def add(request):
    c = {}
    c.update(csrf(request))
    isvalid = True
    u = Demand
    if request.method == "POST":
        u = Demand()
        member_id = request.POST["member_id"]
        name_en = request.POST["name_en"]
        if member_id == "0" or member_id == "":
            isvalid = False
            messages.warning(request, "please select member")
        if name_en == "":
            isvalid = False
            messages.warning(request, "please input english name")
        # _bind_data(request, u)
        if isvalid:
            try:
                u.save()
                _save_items(request, u)
                return redirect("demand.index")
            except Exception, e:
                messages.warning(request, e.message)
                logging.error(e.message)
                logging.debug(e.message)
    c["u"] = u
    _load_types(c)
    c['readSuitorRelate'] = False
    return render_to_response("demand/add.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("demand")
@csrf_protect
def edit(request, id):
    c = {}
    c.update(csrf(request))
    isvalid = True
    u = get_object_or_404(Demand, pk=id)
    last_financial_year = u.financial_year-1
    c['last_financial_year'] = last_financial_year
    if request.method == "POST":
        id_post = request.POST["id"]
        u = Demand.objects.get(pk=id_post)
        member_id = request.POST["member_id"]
        name_en = request.POST["name_en"]
        if member_id == "0" or member_id == "":
            isvalid = False
            messages.warning(request, "please select member")
        if name_en == "":
            isvalid = False
            messages.warning(request, "please input english name")
        _bind_data(request, u)
        if isvalid:
            try:
                u.save()
                _clear_items(u)
                _save_items(request, u)
                return redirect("demand.index")
            except Exception, e:
                messages.warning(request, e.message)
                logging.error(e.message)
                logging.debug(e.message)
    _load_types(c)
    c["u"] = u
    c['attachments'] = u.demand_attach.all()
    # c["other_target_companies"] = DemandOtherTargetCompany.objects.filter(demand__id=u.id)
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
    mks = u.demand_keyword.all()
    c['readSuitorRelate'] = True
    c['mks'] = mks
    keywords = ""
    if len(mks) > 0:
        for m in mks:
            keywords += m.keyword + ","
        keywords = keywords[0 : len(keywords) - 1]
    c['keywords'] = keywords

    mks = u.demand_keyword_en.all()
    keywordsEn = ""
    if len(mks) > 0:
        for m in mks:
            keywordsEn += m.keyword + ","
        keywordsEn = keywordsEn[0 : len(keywordsEn) - 1]
    c['keywordsEn'] = keywordsEn

    mks = u.demand_keyword_admin.all()
    keywordsAdmin = ""
    if len(mks) > 0:
        for m in mks:
            keywordsAdmin += m.keyword + ","
        keywordsAdmin = keywordsAdmin[0 : len(keywordsAdmin) - 1]
    c['keywordsAdmin'] = keywordsAdmin


    admin_recommmond_reason=u.demand_recommond_reason_admin.all()


    c['isHasRecomond_1']=False
    c['isHasRecomond_2']=False
    c['isHasRecomond_3']=False
    c['isHasRecomond_4']=False
    c['isHasRecomond_5']=False
    c['isHasRecomond_6']=False
    c['isHasRecomond_7']=False

    for _recommond in admin_recommmond_reason:


        if _recommond.reason ==u'知名VC投资过':
            c['isHasRecomond_1']=True
        if _recommond.reason ==u'知名券商推介':
            c['isHasRecomond_2']=True
        if _recommond.reason ==u'知名投行推介':
            c['isHasRecomond_3']=True
        if _recommond.reason ==u'我的朋友的推介':
            c['isHasRecomond_4']=True
        if _recommond.reason ==u'最受关注交易':
            c['isHasRecomond_5']=True
        if _recommond.reason ==u'B轮／C轮':
            c['isHasRecomond_6']=True
        if _recommond.reason ==u'境外投资机会':
            c['isHasRecomond_7']=True


    return render_to_response("demand/add.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("demand")
@csrf_protect
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
                condition = Q(member_id=request.POST.get("member_id"))
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
                    # if submitStatus == "draft":
                    #     u.status = StatusDemand.draft
                    # else:
                    #     u.status = StatusDemand.pending
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


@login_required
@permission_required("demand")
def detail(request, id):
    c = {}
    _load_detail(request, c, id)
    return render_to_response("demand/detail.html", c, context_instance=RequestContext(request))


def _load_detail(request, c, id):
    c.update(csrf(request))
    u = get_object_or_404(Demand, pk=id)
    last_financial_year = u.financial_year-1
    c['last_financial_year'] = last_financial_year
    c["u"] = u
    c['attachments'] = u.demand_attach.all()
    # c["other_target_companies"] = DemandOtherTargetCompany.objects.filter(demand__id=u.id)
    countrySelected = u.company_countries.all()
    if countrySelected:
        c['company_country'] = countrySelected[0].name_cn
    provinceSelected = u.company_provinces.all()
    if provinceSelected:
        c['company_province'] = provinceSelected[0].name_cn
    industrySelected = u.demand_industries.all()
    if industrySelected:
        cvId = industrySelected[0].cv3
        if cvId is None:
            cvId = industrySelected[0].cv2
        if cvId is None:
            cvId = industrySelected[0].cv1
        if cvId:
            c['company_industry'] = Industry.objects.get(pk=cvId).name_cn
    c['target_companies_count'] = u.target_companies.all().count()
    mks = u.demand_keyword.all()
    c['readSuitorRelate'] = True
    c['mks'] = mks
    keywords = ""
    if len(mks) > 0:
        for m in mks:
            keywords += m.keyword + ","
        keywords = keywords[0 : len(keywords) - 1]
    c['keywords'] = keywords

    mks = u.demand_keyword_en.all()
    keywordsEn = ""
    if len(mks) > 0:
        for m in mks:
            keywordsEn += m.keyword + ","
        keywordsEn = keywordsEn[0 : len(keywordsEn) - 1]
    c['keywordsEn'] = keywordsEn

    mks = u.demand_keyword_admin.all()
    keywordsAdmin = ""
    if len(mks) > 0:
        for m in mks:
            keywordsAdmin += m.keyword + ","
        keywordsAdmin = keywordsAdmin[0 : len(keywordsAdmin) - 1]
    c['keywordsAdmin'] = keywordsAdmin


@login_required
@permission_required("demand")
@csrf_protect
def check(request, id):
    if request.method == "POST":
        isvalid = True
        id_post = request.POST["id"]
        u = Demand.objects.get(pk=id_post)
        status = StatusDemand.approved
        result_check = ResultsDemandCheck.approve
        reason = request.POST["reason"]
        is_right = True
        if 'btn_disapprove' in request.POST:
            if reason == "":
                isvalid = False
                messages.warning(request, "please input reason")
            status = StatusDemand.not_approved
            result_check = ResultsDemandCheck.disapprove
            is_right = False
        elif 'btn_offline' in request.POST:
            status = StatusDemand.offline
            Demand.objects.filter(pk=id_post).update(status=status)
            is_right = False
        if isvalid:
            try:
                Demand.objects.filter(pk=id_post).update(status=status)
                adminuser = AdminUser.objects.get(pk=request.session['uid'])
                _save_check_log(adminuser, reason, result_check, u)
                if u.status == StatusDemand.pending:
                    _send_check_email(u, is_right, reason)
                return redirect("demand.index")
            except Exception, e:
                messages.warning(request, e.message)
                logging.error(e.message)
                logging.debug(e.message)
    c = {}
    _load_detail(request, c, id)
    c['ischeck'] = True
    return render_to_response("demand/detail.html", c, context_instance=RequestContext(request))


def recommendProject(request, id):
    c = {}
    c.update(csrf(request))
    d = get_object_or_404(Demand, pk=id)
    c['demand']=d
    

    c['recommend_list_count']=RecommondProjectItem.objects.filter(demand=d,is_man=False).count()
    
    c['man_list'] = RecommondProjectItem.objects.filter(demand=d,is_man=True,is_delete=False).order_by('-rank')
    c['man_list_count'] = c['man_list'].count()
    _recommend_list = RecommondProjectItem.objects.filter(demand=d,is_man=False).order_by('-sum_project_score')
    
    c['recommend_list']=_recommend_list
    c['recommend_list_count']=len(c['recommend_list'])
    
    c['total_num']=c['man_list_count']+c['recommend_list_count']


    return render_to_response("demand/recommend.html", c, context_instance=RequestContext(request))


def recommendProjectAdd(request,id):
    
    recommend_project=get_object_or_404(RecommondProjectItem,pk=id)
    recommend_project.is_man=True
    recommend_project.is_delete=False
    recommend_project.save()
    return redirect("demand.recommend",recommend_project.demand.id) 


def recommendProjectDelete(request,id):

    recommend_project=get_object_or_404(RecommondProjectItem,pk=id)
    recommend_project.is_man=True
    recommend_project.is_delete=True
    recommend_project.save()
    return redirect("demand.recommend",recommend_project.demand.id) 


def recommendProjectRemove(request,id):


    recommend_project=get_object_or_404(RecommondProjectItem,pk=id)
    recommend_project.is_man=False
    recommend_project.is_delete=False
    recommend_project.save()
    return redirect("demand.recommend",recommend_project.demand.id) 




def recommendProjectStar(request,id):

    recommend_project=get_object_or_404(RecommondProjectItem,pk=id)
    recommend_project.is_star=True
    recommend_project.save()
    return redirect("demand.recommend",recommend_project.demand.id) 

def recommendProjectUnStar(request,id):

    recommend_project=get_object_or_404(RecommondProjectItem,pk=id)
    recommend_project.is_star=False
    recommend_project.save()
    return redirect("demand.recommend",recommend_project.demand.id) 

def recommendProjectTopRank(request,id):

    recommend_project=get_object_or_404(RecommondProjectItem,pk=id)

    max_rank=RecommondProjectItem.objects.filter(demand=recommend_project.demand,is_man=True,is_delete=False).aggregate(Max('rank'))
   
    recommend_project.rank=max_rank['rank__max']+1
    recommend_project.save()

    return redirect("demand.recommend",recommend_project.demand.id) 


def recommendProjectUpRank(request,id):

    recommend_project=get_object_or_404(RecommondProjectItem,pk=id)

    min_rank=RecommondProjectItem.objects.filter(demand=recommend_project.demand,is_man=True,is_delete=False,rank__gt=recommend_project.rank).aggregate(Min('rank'))
    if min_rank['rank__min']:
        recommend_project.rank=min_rank['rank__min']+1
    else:
        recommend_project.rank+=1
    recommend_project.save()
    return redirect("demand.recommend",recommend_project.demand.id) 

def recommendProjectDownRank(request,id):

    recommend_project=get_object_or_404(RecommondProjectItem,pk=id)

    max_rank=RecommondProjectItem.objects.filter(demand=recommend_project.demand,is_man=True,is_delete=False,rank__lt=recommend_project.rank).aggregate(Max('rank'))
    if max_rank['rank__max']:
        recommend_project.rank=max_rank['rank__max']-1
    else:
        recommend_project.rank-=1

    recommend_project.save()
    return redirect("demand.recommend",recommend_project.demand.id) 


def recommendProjectDetail(request,id):
    c={}
    recommend_project=get_object_or_404(RecommondProjectItem,pk=id)
    c['item']=recommend_project
    return render_to_response("demand/recommend_detail.html", c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
@permission_required("demand")
def approve(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Demand.objects.filter(pk=id).update(status=StatusDemand.approved)
            d = Demand.objects.filter(pk=id)
            old_status = d.status
            d.status = StatusDemand.approved
            adminuser = AdminUser.objects.get(pk=request.session['uid'])
            _save_check_log(adminuser, "", True, d)
            if old_status == StatusDemand.pending:
                _send_check_email(d, True, "")
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@login_required
@permission_required("demand")
def ban(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            d = Demand.objects.get(pk=id)
            d.status = StatusDemand.offline
            d.save()
            adminuser = AdminUser.objects.get(pk=request.session['uid'])
            _save_check_log(adminuser, u"管理员下线", False, d)
            # _send_check_email(d, False, u"资料不完整")
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@login_required
@permission_required("demand")
def setRecommend(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Demand.objects.filter(pk=id).update(is_recommend=1)
            d = Demand.objects.get(pk=id)
            log_recommend = DemandRecommendLog()
            log_recommend.demand = d
            log_recommend.type = TypeDemandRecommend.recommend
            log_recommend.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)

@csrf_exempt
@login_required
@permission_required("demand")
def cancelRecommend(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Demand.objects.filter(pk=id).update(is_recommend=0)
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@login_required
@permission_required("demand")
def setTop(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Demand.objects.filter(pk=id).update(is_top=1)
            d = Demand.objects.get(pk=id)
            log_recommend = DemandRecommendLog()
            log_recommend.demand = d
            log_recommend.type = TypeDemandRecommend.top
            log_recommend.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@login_required
@permission_required("demand")
def cancelTop(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Demand.objects.filter(pk=id).update(is_top=0)
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@login_required
@permission_required("demand")
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
    u.member_id = request.POST.get("member_id")
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
    u.demand_keyword.all().delete()
    if demand_keyword:
        integrity = integrity + 1
        mks = demand_keyword.split(",")
        for m in mks:
            k = DemandKeyword()
            k.keyword = m
            k.demand = u
            k.save()

    demand_keyword = request.POST.get("project_keyword_en", False)
    u.demand_keyword_en.all().delete()
    if demand_keyword:
        integrity = integrity + 1
        mks = demand_keyword.split(",")
        for m in mks:
            k = DemandKeywordEn()
            k.keyword = m
            k.demand = u
            k.save()

    demand_keyword = request.POST.get("project_keyword_admin", False)
    u.demand_keyword_admin.all().delete()
    if demand_keyword:
        mks = demand_keyword.split(",")
        for m in mks:
            k = DemandKeywordAdmin()
            k.keyword = m
            k.demand = u
            k.save()

    integrity = int(integrity * 100 / 21)
    u.integrity = integrity
    u.integrity_en = integrity



    admin_recommmond_reason = request.POST.getlist('project_recommond_reason_admin',[])
    u.demand_recommond_reason_admin.all().delete()
    if admin_recommmond_reason:
        for _reason in admin_recommmond_reason:
            r=DemandRecommondReasonAdmin()
            r.reason=_reason
            r.project=u

            r.save()
    u.save()

    return True, "ok"


@login_required
@permission_required("demand")
def sync_recommend(request, id):
    result = "success"
    try:
        d = Demand.objects.get(pk=id)
        project_list=Project.objects.filter(status=2).filter(expire_date__gt=datetime.datetime.now()).order_by('-id')
        update_project_recommond_list(d, project_list)
        result = "success"
    except Exception, e:
        print e.message
        logger.error(e.message)
    return HttpResponse(result)


def _save_items(request, u):
    countries_ids = request.POST.getlist("country", [])
    if countries_ids is not None:
        for id in countries_ids:
            if id != "0" and id != "":
                c = Country.objects.get(pk=id)
                u.company_countries.add(c)
    industries_ids = request.POST.getlist("industry", [])
    if industries_ids is not None:
        for id in industries_ids:
            if id != "0" and id != "":
                c = Industry.objects.get(pk=id)
                u.company_industries.add(c)
    provinces_ids = request.POST.getlist("province", [])
    if provinces_ids is not None:
        for id in provinces_ids:
            if id != "0" and id != "":
                c = Province.objects.get(pk=id)
                u.company_provinces.add(c)
    cities_ids = request.POST.getlist("city", [])
    if cities_ids is not None:
        for id in cities_ids:
            if id != "0" and id != "":
                c = City.objects.get(pk=id)
                u.company_cities.add(c)
    target_member_ids = request.POST.getlist("members")
    if target_member_ids is not None:
        for id in target_member_ids:
            if id != "0" and id != "":
                c = Member.objects.get(pk=id)
                u.target_members.add(c)
    target_companies_ids = request.POST.getlist("companies")
    if target_companies_ids is not None:
        for id in target_companies_ids:
            if id != "0" and id != "":
                c = Company.objects.get(pk=id)
                u.target_companies.add(c)
    target_industries_ids = request.POST.getlist("industry_sutior")
    if target_industries_ids is not None:
        for id in target_industries_ids:
            if id != "0" and id != "":
                c = Industry.objects.get(pk=id)
                u.target_industries.add(c)


def _clear_items(u):
    u.company_countries.clear()
    u.company_industries.clear()
    u.company_provinces.clear()
    u.target_members.clear()
    u.target_companies.clear()
    u.target_industries.clear()


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
    c["countries"] = Country.objects.all().order_by("-sort")
    c['industries'] = Industry.objects.filter(level=1, is_display=True)
    c["members"] = Member.objects.all()
    c["companies"] = Company.objects.all()


def _send_check_email(d, is_right, reason):
    mail_dic = dict()
    mail_dic['link'] = _get_demand_link(str(d.id))
    mail_dic['user_name'] = d.member.first_name
    mail_dic['name'] = d.name_cn
    mail_dic['is_right'] = is_right
    mail_dic['reason'] = reason
    mail_dic['year']=d.add_time.year
    mail_dic['month']=d.add_time.month
    mail_dic['day']=d.add_time.day

    html_content = loader.render_to_string("demand/email_message.html", mail_dic)
    msg = EmailMessage('NewChama项目审核结果通知', html_content, EMAIL_HOST_USER, [d.member.email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


def _save_check_log(adminuser, reason, result_check, d):
    check_log = DemandCheckLog()
    check_log.adminuser = adminuser
    check_log.demand = d
    check_log.reason = reason
    check_log.result = result_check
    check_log.save()


def _send_push_email(u):
    email = []
    if u.target_companies:
        for company in u.target_companies.all():
            members = Member.objects.filter(company__id=company.id)
            if members:
                for member in members:
                    if member.email:
                        email.append(member.email)
    if u.target_members:
        for member in u.target_members.all():
            if member.email:
                email.append(member.email)

    mail_dic = dict()
    mail_dic['link'] = _get_demand_link(str(u.id))
    mail_dic['name'] = u.name_cn

    html_content = loader.render_to_string("demand/email_push.html",mail_dic)

    if email:
        for e in set(email):
            msg = EmailMessage('NewChama项目推送通知', html_content, EMAIL_HOST_USER, [e])
            msg.content_subtype = "html"  # Main content is now text/html
    # msg.send()


def _get_demand_link(id):
    return 'http://www.newchama.com/purchase/detail/' + id + '/'


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
