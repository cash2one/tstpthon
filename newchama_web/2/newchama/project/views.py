#encoding:utf-8
import random
from django.shortcuts import render_to_response, redirect, RequestContext, get_object_or_404, HttpResponse
from django.db.models import Max,Min
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from models import Project, Country, Province, Company, Member, StockStructure, ProjectKeyword, ProjectKeywordAdmin, ProjectKeywordEn, \
    ProjectAttach, Industry, City, ResultsProjectCheck, StatusProject, ProjectCheckLog, ProjectServiceType, ProjectKeyword, ProjectOneclickAttach, ProjectRecommondReasonAdmin, \
    RegionLevelOne, RegionLevelTwo, RegionLevelThree
from demand.models import Demand, StatusDemand
from repository.models import AccountingFirm, ListedCompany, StockExchange, InvestmentHistory, InvestmentCompany
from adminuser.models import AdminUser
from django.core import serializers
import simplejson as json
import datetime
import os
from newchama import settings
from django.contrib import messages
from newchama.decorators import login_required, permission_required
from recommond.models import RecommondItem,PROJECT_SCORE_LEVEL, ProjectTargetCompanyDetail, MemberRecommendScore, ProjectTargetMemberDetail
from django.core.mail import send_mail, EmailMessage
from django.template import loader, Context
from newchama.settings import EMAIL_HOST_USER,IS_PRODUCT_HOST, TEST_EMAIL, BD_EMAIL, DOMAIN
from django.db.models import Q
from django.utils import simplejson
from models import ProjectRecommendLog, TypeProjectRecommend
from recommond.compute_member_recommend_new import compute_score, commit_project_recommends
from member_message.models import Message
from member.models import MemberInvestmentField, SellerDealCategory, DetailDealType, SubDetailDealType
from newchama.helper import send_email_by_mq, send_email_by_mq_multiple
from member_message.views import update_message_log
from repository.templatetags import myTags
from project.models import ProjectOtherTargetCompany
from django.core.exceptions import ObjectDoesNotExist
from log.models import EmailTracking
# Create your views here.
import logging
from recommond.compute_member_recommend_new import calculate_matching_tables_score, access_project_tag_fuzzy_word
from recommond.util import get_single_member_value_dict
from django.db import transaction
from recommond.models import MemberRecommendScore
from repository import custom_crypto
import base64

logger = logging.getLogger(__name__)


@login_required
@permission_required("project")
def index(request):
    c = {}
    download = request.GET.get("download", "")
    keyword = request.GET.get("keyword", "")
    data = Project.objects.all().order_by("-id")
    # data = Project.objects.filter(id__gte=468, id__lte=469).order_by("-id")
    status = request.GET.get("status", "")

    condition = Q()
    condition2 = Q()
    if status != "":
        condition = Q(status=status)
        c["status"] = int(status)
    else:
        condition = ~Q(status=StatusProject.deleted)

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

    c["result_list"] = data.filter(condition & condition2)
    c['Status'] = StatusProject
    c['StatusType'] = Project.STATUS_TYPES
    c['total'] = data.count()
    if download != "":
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="project.csv"'
        t = loader.get_template('project/project_download_template.txt')
        d = Context({
            'data': data,
        })
        response.write(t.render(d).encode('gb18030'))
        return response
    return render_to_response("project/list.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("project")
def list_oneclick(request):
    c = {}
    c['oneclickList'] = ProjectOneclickAttach.objects.all().order_by("-id")
    return render_to_response("project/list_onclick.html", c, context_instance=RequestContext(request))



@login_required
@permission_required("project")
@csrf_protect
def add(request):
    c = {}
    c.update(csrf(request))
    p = Project()
    if request.method == "POST":
        try:

            _bind_data(request, p)

            return redirect("project.index")
        except Exception, e:
            messages.warning(request, e.message)
    p.create_source = 2  # CURRENCY_TYPES CMS: 2
    c['u'] = p
    _load_types(c)
    c["curr_year"] = datetime.datetime.today().year
    c["last_year"] = datetime.datetime.today().year - 1
    c['readSuitorRelate'] = False
    c['categories'] = SellerDealCategory.objects.all()
    c['sub_categories'] = DetailDealType.objects.all()
    c['sub_deal_types'] = SubDetailDealType.objects.all()
    c['sub_categories_selected'] = []

    return render_to_response("project/add.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("project")
@csrf_protect
def edit(request, id):
    c = {}
    c.update(csrf(request))
    p = get_object_or_404(Project, pk=id)
    if request.method == "POST":
        try:
            id_post = request.POST["id"]
            u = Project.objects.get(pk=id_post)
            if _bind_data(request, u):
                return redirect("project.index")
            else:
                return render_to_response("project/add.html", c, context_instance=RequestContext(request))
        except Exception, e:
            messages.warning(request, e.message)
    c['u'] = p
    _load_types(c)
    if p.financial_year:
        c["curr_year"] = p.financial_year
        c["last_year"] = p.financial_year - 1
    else:
        c["curr_year"] = None
        c["last_year"] = None

    ss = p.project_stock_structure.all()
    c['stockST'] = ss
    c['stockST_len'] = len(ss)
    c['attachments'] = p.project_attach.all()

    mks = p.project_keyword.all()
    keywords = ""
    if len(mks) > 0:
        for m in mks:
            keywords += m.keyword + ","
        keywords = keywords[0 : len(keywords) - 1]
    c['keywords'] = keywords

    mks = p.project_keyword_en.all()
    keywordsEn = ""
    if len(mks) > 0:
        for m in mks:
            keywordsEn += m.keyword + ","
        keywordsEn = keywordsEn[0 : len(keywordsEn) - 1]
    c['keywordsEn'] = keywordsEn

    mks = p.project_keyword_admin.all()
    keywordsAdmin = ""
    if len(mks) > 0:
        for m in mks:
            keywordsAdmin += m.keyword + ","
        keywordsAdmin = keywordsAdmin[0 : len(keywordsAdmin) - 1]
    c['keywordsAdmin'] = keywordsAdmin
    c['readSuitorRelate'] = True


    admin_recommmond_reason=p.project_recommond_reason_admin.all()


    c['isHasRecomond_1']=False
    c['isHasRecomond_2']=False
    c['isHasRecomond_3']=False
    c['isHasRecomond_4']=False
    c['isHasRecomond_5']=False
    c['isHasRecomond_6']=False
    c['isHasRecomond_7']=False

    for _recommond in admin_recommmond_reason:


        if _recommond.reason ==u'知名PE/VC背书':
            c['isHasRecomond_1']=True
        if _recommond.reason ==u'细分领域龙头企业':
            c['isHasRecomond_2']=True
        if _recommond.reason ==u'市场热点企业':
            c['isHasRecomond_3']=True
        if _recommond.reason ==u'高净利润/营业额':
            c['isHasRecomond_4']=True
        if _recommond.reason ==u'与行业巨头企业战略合作':
            c['isHasRecomond_5']=True
        if _recommond.reason ==u'业内领先技术实力':
            c['isHasRecomond_6']=True
        if _recommond.reason ==u'创始团队有丰富投资创业经验（优秀团队）':
            c['isHasRecomond_7']=True

    c['categories'] = SellerDealCategory.objects.all()
    c['sub_categories'] = DetailDealType.objects.all()
    c['sub_deal_types'] = SubDetailDealType.objects.all()
    c['sub_categories_selected'] = p.deal_type.all()


    return render_to_response("project/add.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("project")
@csrf_protect
def save(request):
    response_data = {}
    response_data['result'] = 'failed'
    if request.method == "POST":
        try:
            name_en = request.POST["name_en"]
            name_cn = request.POST["name_cn"]
            if name_en == "" and name_cn == "":
                response_data['message'] = "please input project name"
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
                condition = Q(member_id=request.POST.get("member_id"))
                condition2 = Q()
                if id_post:
                    condition = condition & ~Q(pk=id_post)
                if name_cn.strip() != "":
                    condition2 = condition2 | Q(name_cn=name_cn.strip())

                if name_en.strip() != "":
                    condition2 = condition2 | Q(name_en=name_en.strip())

                project = Project.objects.filter(condition & condition2)
                #if project:
                #    isExsit = True
                #    response_data['message'] = "projectExsit"

                if isExsit is False:
                    if id_post:
                        p = Project.objects.get(pk=id_post)
                    if submitStatus == "draft":
                        p.status = StatusProject.draft
                    else:
                        if p.status != StatusProject.approved:
                            p.status = StatusProject.pending
                    bool, msg = _bind_data(request, p)

                    if bool:

                        response_data['result'] = 'success'
                        response_data['id'] = p.id
                        response_data['message'] = 'Successfully'
                    else:
                        response_data['message'] = msg
        except Exception, e:
            logger.error(e.message, exc_info=True)
            response_data['message'] = e.message
    return HttpResponse(simplejson.dumps(response_data), content_type="text/plain")



def _get_project_link(id):
    return 'http://www.newchama.com/sales/detail/' + id + '/'


def _send_check_email(p, is_right, reason):
    mail_dic = dict()
    mail_dic['link'] = _get_project_link(str(p.id))
    mail_dic['user_name'] = p.member.first_name
    mail_dic['name'] = p.name_cn
    mail_dic['is_right'] = is_right
    mail_dic['reason'] = reason
    mail_dic['year']=p.add_time.year
    mail_dic['month']=p.add_time.month
    mail_dic['day']=p.add_time.day

    html_content = loader.render_to_string("project/email_message.html", mail_dic)
    msg = EmailMessage('NewChama项目审核结果通知', html_content, EMAIL_HOST_USER, [p.member.email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


def _send_push_email(project):
    ptcds = ProjectTargetMemberDetail.objects.filter(project_id=project.id) #, is_sender=0)            #add is_sender
    needSendEmailMember = []       #need send email company
    if len(ptcds) > 0:
        for pt in ptcds:
            ProjectTargetMemberDetail.objects.filter(pk=pt.id).update(is_sender=1)
            member = Member.objects.filter(id=pt.member_id).values("id", "email", "first_name", "last_name")
            needSendEmailMember.append(member)

    if needSendEmailMember:
        for mrs in set(needSendEmailMember):
            if len(mrs) > 0:
                for mr in mrs:
                    if mr["email"]:
                        dic = {}
                        handle_dynamic_email_module(dic, project, mr)
                        html_content = loader.render_to_string("project/email_push.html", dic)

                        emailAccount = mr["email"]
                        if not IS_PRODUCT_HOST:
                            emailAccount = TEST_EMAIL
                        title = '%s-%s %s' % (project.member.company.short_name_cn, project.member.first_name, project.name_cn)

                        try:
                            send_email_by_mq('email', 'email', title, emailAccount, html_content)
                        except Exception, e:
                            msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [emailAccount])
                            msg.content_subtype = "html"  # Main content is now text/html
                            msg.send()

                    _save_message(project, mr)
                    _save_email_tracking(project, mr, 'cms_deal_to_buyer')

'''
def _send_push_email(project):
    ptcds = ProjectTargetCompanyDetail.objects.filter(project_id=project.id) #, is_sender=0)            #add is_sender
    needSendEmailMember = []       #need send email company
    noteBDToFollow = []
    if len(ptcds) > 0:
        for pt in ptcds:
            company_id = pt.company.id
            members = Member.objects.filter(company__id=company_id).values("id", "email", "first_name", "last_name")
            ProjectTargetCompanyDetail.objects.filter(pk=pt.id).update(is_sender=1)
            if members:
                needSendEmailMember.append(members)
            else:
                noteBDToFollow.append(company_id)

    if needSendEmailMember:
        # email_list=[]
        # content_list=[]

        for mrs in set(needSendEmailMember):
            if len(mrs) > 0:
                for mr in mrs:
                    if mr["email"]:
                        dic = {}
                        handle_dynamic_email_module(dic, project, mr)
                        html_content = loader.render_to_string("project/email_push.html", dic)

                        emailAccount = mr["email"]
                        if not IS_PRODUCT_HOST:
                            emailAccount = TEST_EMAIL
                        title = '%s-%s %s' % (project.member.company.short_name_cn, project.member.first_name, project.name_cn)
                        try:
                            send_email_by_mq('email', 'email', title, emailAccount, html_content)
                        except Exception, e:
                            msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [emailAccount])
                            msg.content_subtype = "html"  # Main content is now text/html
                            msg.send()

                    _save_message(project, mr)
                    _save_email_tracking(project, mr, 'cms_deal_to_buyer')

    if len(noteBDToFollow) > 0:
        noEmailcompanies = Company.objects.filter(id__in=noteBDToFollow)
        dic = {'link': _get_project_link(str(project.id)), 'noEmailcompanies': noEmailcompanies, 'projectName': project.name_cn}
        html_content = loader.render_to_string("project/email_not_push.html", dic)
        # noPublishemail = "Terry@newchama.com"
        noPublishemail = BD_EMAIL
        #logger.debug("send email to " + str(emailAccount))
        title = "Newchama未成功推送项目提醒"
        try:
            send_email_by_mq('email', 'email', title, noPublishemail, html_content)
        except Exception, e:
            msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [noPublishemail])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
'''

def _save_check_log(adminuser, reason, result_check, p):
    check_log = ProjectCheckLog()
    check_log.adminuser = adminuser
    check_log.project = p
    check_log.reason = reason
    check_log.result = result_check
    check_log.save()


@login_required
@permission_required("project")
@csrf_protect
def check(request, id):
    if request.method == "POST":
        isvalid = True
        id_post = request.POST["id"]
        u = Project.objects.get(pk=id_post)
        status = StatusProject.approved
        result_check = ResultsProjectCheck.approve
        reason = request.POST["reason"]
        is_right = True
        if 'btn_disapprove' in request.POST:
            if reason == "":
                isvalid = False
                messages.warning(request, "please input reason")
            status = StatusProject.not_approved
            result_check = ResultsProjectCheck.disapprove
            is_right = False
        elif 'btn_offline' in request.POST:
            status = StatusProject.offline
            Project.objects.filter(pk=id_post).update(status=status)
            is_right = False
        if isvalid:
            try:
                Project.objects.filter(pk=id_post).update(status=status)
                adminuser = AdminUser.objects.get(pk=request.session['uid'])
                _save_check_log(adminuser, reason, result_check, u)
                if u.status == StatusProject.pending:
                    _send_check_email(u, is_right, reason)
                    if 'btn_approve' in request.POST:
                        _send_push_email(u)
                return redirect("project.index")
            except Exception, e:
                messages.warning(request, e.message)
                logging.error(e.message)
                logging.debug(e.message)
    c = {}
    _load_detail(request, c, id)
    c['ischeck'] = True
    return render_to_response("project/detail.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("project")
def detail(request, id):
    c = {}
    _load_detail(request, c, id)
    return render_to_response("project/detail.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("project")
def _load_detail(request, c, id):
    c.update(csrf(request))
    p = get_object_or_404(Project, pk=id)
    keywords_list=[]
    for kv in ProjectKeyword.objects.filter(project=p):
        keywords_list.append(kv.keyword)
    p.keywords=','.join(keywords_list)

    mks = p.project_keyword_en.all()
    keywordsEn = ""
    if len(mks) > 0:
        for m in mks:
            keywordsEn += m.keyword + ","
        keywordsEn = keywordsEn[0 : len(keywordsEn) - 1]
    c['keywordsEn'] = keywordsEn

    mks = p.project_keyword_admin.all()
    keywordsAdmin = ""
    if len(mks) > 0:
        for m in mks:
            keywordsAdmin += m.keyword + ","
        keywordsAdmin = keywordsAdmin[0 : len(keywordsAdmin) - 1]
    c['keywordsAdmin'] = keywordsAdmin

    c['u'] = p
    ss = p.project_stock_structure.all()
    if p.financial_year:
        c['curr_year'] = p.financial_year
        c['last_year'] = p.financial_year - 1
        c['last_year_before'] = p.financial_year - 2
    else:
        c['curr_year'] = None
        c['last_year'] = None
        c['last_year_before'] = None

    c['stockST'] = ss
    c['attachments'] = p.project_attach.all()
    project_category_lst = []
    for deal_type in p.deal_type.all():
        if deal_type.category.name_cn not in project_category_lst:
            project_category_lst.append(deal_type.category.name_cn)
    c['project_category_lst'] = project_category_lst

@csrf_exempt
@login_required
@permission_required("project")
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


@csrf_exempt
@login_required
@permission_required("project")
def setRecommend(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Project.objects.filter(pk=id).update(is_recommend=1)
            d = Project.objects.get(pk=id)
            log_recommend = ProjectRecommendLog()
            log_recommend.project = d
            log_recommend.type = TypeProjectRecommend.recommend
            log_recommend.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@login_required
@permission_required("project")
def cancelRecommend(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Project.objects.filter(pk=id).update(is_recommend=0)
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@login_required
@permission_required("project")
def setTop(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Project.objects.filter(pk=id).update(is_top=1)
            d = Project.objects.get(pk=id)
            log_recommend = ProjectRecommendLog()
            log_recommend.project = d
            log_recommend.type = TypeProjectRecommend.top
            log_recommend.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@login_required
@permission_required("project")
def cancelTop(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Project.objects.filter(pk=id).update(is_top=0)
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


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
        p.member_id = request.POST.get("member_id")
        p.name_cn = request.POST["name_cn"]
        p.name_en = request.POST["name_en"]
        if request.POST.get("name_cn", False) or request.POST.get("name_en", False):
            integrity = integrity + 1

        if request.POST.get("service_type", False):
            p.service_type = request.POST["service_type"]
            integrity = integrity + 1

        pay_currency = request.POST.get("pay_currency", False)
        if pay_currency and pay_currency != "":
            p.pay_currency = pay_currency.replace(",", "")
            p.multi_currency = pay_currency.replace(",", "")  # TODO: Jay.Ying:  multi-currency editing
            integrity = integrity + 1

        project_relation = request.POST.get("project_relation", False)
        if project_relation and project_relation != "":
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

        if request.POST.get('regionlevelone', False):
            p.regionlevelone_id = request.POST.get('regionlevelone');
            integrity = integrity + 1
        else:
            return False, "region error"

        if request.POST.get('regionleveltwo', False):
            p.regionleveltwo_id = request.POST.get('regionleveltwo');
            integrity = integrity + 1
        else:
            return False, "region error"

        if request.POST.get('regionlevelthree', False):
            p.regionlevelthree_id = request.POST.get('regionlevelthree');
            integrity = integrity + 1
        else:
            return False, "region error"

        if request.POST.get("company_country", False):
            p.company_country = Country.objects.get(id=request.POST["company_country"])
            integrity = integrity + 1

        company_province = request.POST.get("company_province", False)
        if company_province and company_province != "0":
            p.company_province = Province.objects.get(id=company_province)


        #if class3 got a result then industry_id value is company_industry_2
        #else if class2 got a result then industry_id value is company_industry_1
        #else class industry_id value is company_industry_0
        industry_id = request.POST.get("industry_id", False)
        if industry_id != "0" and industry_id:
            p.company_industry = Industry.objects.get(id=industry_id)
            integrity = integrity + 1

        company_industry_2 = request.POST.get("company_industry_2", False)
        if company_industry_2 != "0" and company_industry_2:
            p.cv3 = company_industry_2

        company_industry_1 = request.POST.get("company_industry_1", False)
        if company_industry_1 != "0" and company_industry_1:
            p.cv2 = company_industry_1

        company_industry_0 = request.POST.get("company_industry_0", False)
        if company_industry_0 != "0" and company_industry_0:
            p.cv1 = company_industry_0

        #keywords in the end of function

        employees_count_type = request.POST.get("employees_count_type", False)
        if employees_count_type and employees_count_type != "":
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
        if not project_stage:
            p.project_stage = None

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
        #    integrity = integrity + 1推送至机
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
        p.project_keyword.all().delete()
        if project_keyword:
            integrity = integrity + 1
            mks = project_keyword.split(",")
            for m in mks:
                k = ProjectKeyword()
                k.keyword = m
                k.project = p
                k.save()

        project_keyword = request.POST.get("project_keyword_en", False)
        p.project_keyword_en.all().delete()
        if project_keyword:
            integrity = integrity + 1
            mks = project_keyword.split(",")
            for m in mks:
                k = ProjectKeywordEn()
                k.keyword = m
                k.project = p
                k.save()

        project_keyword = request.POST.get("project_keyword_admin", False)
        p.project_keyword_admin.all().delete()
        if project_keyword:
            mks = project_keyword.split(",")
            for m in mks:
                k = ProjectKeywordAdmin()
                k.keyword = m
                k.project = p
                k.save()
        integrity = int(integrity * 100 / 31)
        # if request.lang == "zh-cn":
        p.integrity = integrity
        # else:
        p.integrity_en = integrity

        admin_recommmond_reason = request.POST.getlist('project_recommond_reason_admin',[])
        p.project_recommond_reason_admin.all().delete()
        if admin_recommmond_reason:
            for _reason in admin_recommmond_reason:
                r=ProjectRecommondReasonAdmin()
                r.reason=_reason
                r.project=p

                r.save()
        p.deal_type = request.POST.getlist("sub_categories", [])
        p.target_platform = int(request.POST.get("target_platform", 0))
        p.save()
        return True, "ok"


@login_required
@permission_required("project")
def sync_recommend(request, id):
    result = "success"
    try:
        p = Project.objects.get(pk=id)
        commit_project_recommends(compute_score(p))
        result = "success"
    except Exception, e:
        print e.message
        logger.error(e.message, exc_info=True)
    return HttpResponse(result)


@login_required
@permission_required("project")
def recommend_members(request, id):
    c = {}
    c.update(csrf(request))
    p = get_object_or_404(Project, pk=id)
    c['project'] = p
    project_category_lst = []
    for deal_type in p.deal_type.all():
        if deal_type.category.name_cn not in project_category_lst:
            project_category_lst.append(deal_type.category.name_cn)
    c['project_category_lst'] = project_category_lst

    if request.method == "POST":
        _member_id = int(request.POST['addmember_id'])
        _member = get_object_or_404(Member,id=_member_id)

        _record_num = MemberRecommendScore.objects.filter(project=p, member=_member).count()
        if _record_num == 0:
            _record = MemberRecommendScore()
            _record.project = p
            _record.member = _member
            _record.is_man = True
            _record.save()
        else:
            _record=MemberRecommendScore.objects.filter(project=p, member=_member).first()
            _record.is_man = True
            _record.is_delete = False
            _record.save()

    c['recommend_list_count'] = MemberRecommendScore.objects.filter(project=p, is_man=False, is_in_control_panel=False).count()


    _man_list = MemberRecommendScore.objects.filter((Q(project=p) & Q(is_delete=False) ) & (Q(is_man=True) | Q(is_in_control_panel=True))).order_by('-rank')
    _matching_table_man_list = []
    for score in _man_list:
        if score.need_id:
            try:
                _matching_table_man_list.append(MemberInvestmentField.objects.get(pk=score.need_id))
            except MemberInvestmentField.DoesNotExist:
                _matching_table_man_list.append(MemberInvestmentField())
        else:
            _matching_table_man_list.append(MemberInvestmentField())

    c['man_list'] = zip(_man_list, _matching_table_man_list)
    c['man_list_count'] = _man_list.count()
    _recommend_list = MemberRecommendScore.objects.filter(project=p, is_man=False, is_delete=False, is_in_control_panel=False).order_by('-is_man', '-sum_member_score')
    _matching_table_list = []
    for score  in _recommend_list:
        if score.need_id:
            try:
                _matching_table_list.append(MemberInvestmentField.objects.get(pk=score.need_id))
            except MemberInvestmentField.DoesNotExist:
                _matching_table_list.append(MemberInvestmentField())
        else:
            _matching_table_list.append(MemberInvestmentField())

    c['recommend_list'] = zip(_recommend_list, _matching_table_list)
    c['recommend_list_count'] = len(c['recommend_list'])

    c['total_num'] = c['man_list_count']+c['recommend_list_count']
    c['curr_page'] = request.GET.get("page", 1)

    return render_to_response("project/recommend_members.html", c, context_instance=RequestContext(request))


def recommend_member_detail(request, id):
    c = {}
    if request.method == "POST":
        score_id = refresh_recommend_score(int(request.POST['project_id']), int(request.POST['member_id']))
        if score_id:
            return redirect("project.recommend_member_detail", score_id)
        else:
            project = Project.objects.get(int(request.POST['project_id']))
            return redirect("project.recommend_members", project.id)
    recommend_score = get_object_or_404(MemberRecommendScore, pk=id)
    c['item'] = recommend_score
    return render_to_response("project/recommend_member_detail.html", c, context_instance=RequestContext(request))


def recommend_member_delete(request, id):
    recommend_member = get_object_or_404(MemberRecommendScore, pk=id)
    recommend_member.is_man = True
    recommend_member.is_delete = True
    recommend_member.save()
    c = {}
    page = request.GET.get("page", 1)
    c["url"] = "/project/recommend_members/" + str(recommend_member.project.id) + "?page=" + str(page)
    return render_to_response("project/jump.html", c, context_instance=RequestContext(request))


def recommend_member_add(request, id):
    recommend_member = get_object_or_404(MemberRecommendScore, pk=id)
    recommend_member.is_man = True
    recommend_member.is_delete = False
    recommend_member.save()
    c = {}
    page = request.GET.get("page", 1)
    c["url"] = "/project/recommend_members/" + str(recommend_member.project.id) + "?page=" + str(page)
    return render_to_response("project/jump.html", c, context_instance=RequestContext(request))


def recommend_member_remove(request, id):
    recommend_member = get_object_or_404(MemberRecommendScore, pk=id)
    recommend_member.is_man = False
    recommend_member.is_delete = False
    recommend_member.save()
    c = {}
    page = request.GET.get("page", 1)
    c["url"] = "/project/recommend_members/" + str(recommend_member.project.id) + "?page=" + str(page)
    return render_to_response("project/jump.html", c, context_instance=RequestContext(request))


def recommend_member_star(request, id):
    recommend_member = get_object_or_404(MemberRecommendScore, pk=id)
    recommend_member.is_star = True
    recommend_member.save()
    return redirect("project.recommend_members", recommend_member.project.id)


def recommend_member_unstar(request, id):
    recommend_member = get_object_or_404(MemberRecommendScore, pk=id)
    recommend_member.is_star = False
    recommend_member.save()
    return redirect("project.recommend_members", recommend_member.project.id)


def recommend_member_toprank(request,id):
    recommend_member = get_object_or_404(MemberRecommendScore, pk=id)
    max_rank=MemberRecommendScore.objects.filter(project=recommend_member.project, is_man=True, is_delete=False).aggregate(Max('rank'))
    recommend_member.rank=max_rank['rank__max']+1
    recommend_member.save()
    return redirect("project.recommend_members", recommend_member.project.id)


def recommend_member_uprank(request, id):
    recommend_member = get_object_or_404(MemberRecommendScore, pk=id)
    min_rank = MemberRecommendScore.objects.filter(project=recommend_member.project, is_man=True, is_delete=False,rank__gt= recommend_member.rank).aggregate(Min('rank'))
    if min_rank['rank__min']:
        recommend_member.rank = min_rank['rank__min']+1
    else:
        recommend_member.rank += 1
    recommend_member.save()
    return redirect("project.recommend_members", recommend_member.project.id)


def recommend_member_downrank(request, id):
    recommend_member = get_object_or_404(MemberRecommendScore, pk=id)
    max_rank=MemberRecommendScore.objects.filter(project=recommend_member.project, is_man=True, is_delete=False, rank__lt=recommend_member.rank).aggregate(Max('rank'))
    if max_rank['rank__max']:
        recommend_member.rank=max_rank['rank__max']-1
    else:
        recommend_member.rank -= 1
    recommend_member.save()
    return redirect("project.recommend_members", recommend_member.project.id)


def refresh_recommend_score(project_id, member_id):
    project = Project.objects.get(pk=project_id)
    member_info = get_single_member_value_dict(member_id)
    fuzzy_words_lst = access_project_tag_fuzzy_word(project)
    recommend_score_new = calculate_matching_tables_score(project, member_info, fuzzy_words_lst)
    if recommend_score_new:
        with transaction.atomic():
            """ delete old scores """
            MemberRecommendScore.objects.filter(member_id=member_id, project=project).delete()
            recommend_score_new.save()
        return recommend_score_new.id


def recommendCampany(request, id):
    c = {}
    c.update(csrf(request))
    p = get_object_or_404(Project, pk=id)
    c['project']=p
    if request.method == "POST":


        _company_id=int(request.POST['addcompany_id'])
        _project_id=int(request.POST['addcompany_project_id'])
        _add_reason=request.POST['recommend_reason']

        _company=get_object_or_404(Company,id=_company_id)
        _user_num=Member.objects.filter(company=_company).count()
        if _user_num>0:
            has_user=True
        else:
            has_user=False

        _record_num=RecommondItem.objects.filter(project=p,company=_company).count()
        if _record_num==0:

            _record=RecommondItem()
            _record.project=p
            _record.company=_company
            _record.target_reason=_add_reason
            _record.is_man=True
            _record.has_user=has_user
            _record.save()

        else:

            _record=RecommondItem.objects.filter(project=p,company=_company).first()
            _record.is_man=True
            _record.is_delete=False
            _record.target_reason=_add_reason
            _record.has_user=has_user
            _record.save()


    c['recommend_list_count']=RecommondItem.objects.filter(project=p,is_man=False, is_in_control_panel=False, target_reason__isnull=False).count()


    c['man_list'] = RecommondItem.objects.filter((Q(project=p) & Q(is_delete=False) ) & (Q(is_man=True) | Q(is_in_control_panel=True))).order_by('-rank')
    c['man_list_count'] = c['man_list'].count()
    _recommend_list = RecommondItem.objects.filter(project=p, is_man=False, is_delete=False, target_reason__isnull=False, is_in_control_panel=False).order_by('-is_man', '-has_user', '-sum_score','-company_score_has_invest_field','-project_score_local','-company_score_local')#('-sum_score','-company_score_has_invest_field','-project_score_local','-company_score_local')

    c['recommend_list']=_recommend_list#[item for item in _recommend_list if item.target_reason !=None]
    c['recommend_list_count']=len(c['recommend_list'])

    c['total_num']=c['man_list_count']+c['recommend_list_count']
    c['curr_page'] = request.GET.get("page", 1)

    return render_to_response("project/recommend_new.html", c, context_instance=RequestContext(request))


@login_required
def recommendCampanyDetail(request,id):
    c={}
    recommend_company=get_object_or_404(RecommondItem,pk=id)
    c['item']=recommend_company
    return render_to_response("project/recommend_detail.html", c, context_instance=RequestContext(request))


@login_required
def recommendCampanyAdd(request,id):
    recommend_company=get_object_or_404(RecommondItem,pk=id)
    recommend_company.is_man=True
    recommend_company.is_delete=False
    recommend_company.save()
    c={}
    page = request.GET.get("page", 1)
    c["url"] = "/project/recommend/" + str(recommend_company.project.id) + "?page=" + str(page)
    return render_to_response("project/jump.html", c, context_instance=RequestContext(request))
    #return redirect("project.recommend",recommend_company.project.id)


@login_required
def recommendCampanyDelete(request,id):
    recommend_company=get_object_or_404(RecommondItem,pk=id)
    recommend_company.is_man=True
    recommend_company.is_delete=True
    recommend_company.save()
    c={}
    page = request.GET.get("page", 1)
    c["url"] = "/project/recommend/" + str(recommend_company.project.id) + "?page=" + str(page)
    return render_to_response("project/jump.html", c, context_instance=RequestContext(request))
    # return redirect("project.recommend",recommend_company.project.id)


@login_required
def recommendCampanyRemove(request,id):
    recommend_company=get_object_or_404(RecommondItem,pk=id)
    recommend_company.is_man=False
    recommend_company.is_delete=False
    recommend_company.save()
    c={}
    page = request.GET.get("page", 1)
    c["url"] = "/project/recommend/" + str(recommend_company.project.id) + "?page=" + str(page)
    return render_to_response("project/jump.html", c, context_instance=RequestContext(request))
    # return redirect("project.recommend",recommend_company.project.id)


@login_required
def recommendCampanyStar(request,id):

    recommend_company=get_object_or_404(RecommondItem,pk=id)
    recommend_company.is_star=True
    recommend_company.save()
    return redirect("project.recommend",recommend_company.project.id)


@login_required
def recommendCampanyUnStar(request,id):

    recommend_company=get_object_or_404(RecommondItem,pk=id)
    recommend_company.is_star=False
    recommend_company.save()
    return redirect("project.recommend",recommend_company.project.id)


@login_required
def recommendCampanyTopRank(request,id):

    recommend_company=get_object_or_404(RecommondItem,pk=id)

    max_rank=RecommondItem.objects.filter(project=recommend_company.project,is_man=True,is_delete=False).aggregate(Max('rank'))

    recommend_company.rank=max_rank['rank__max']+1
    recommend_company.save()

    return redirect("project.recommend",recommend_company.project.id)


@login_required
def recommendCampanyUpRank(request,id):

    recommend_company=get_object_or_404(RecommondItem,pk=id)

    min_rank=RecommondItem.objects.filter(project=recommend_company.project,is_man=True,is_delete=False,rank__gt=recommend_company.rank).aggregate(Min('rank'))
    if min_rank['rank__min']:
        recommend_company.rank=min_rank['rank__min']+1
    else:
        recommend_company.rank+=1
    recommend_company.save()
    return redirect("project.recommend",recommend_company.project.id)


@login_required
def recommendCampanyDownRank(request,id):

    recommend_company=get_object_or_404(RecommondItem,pk=id)

    max_rank=RecommondItem.objects.filter(project=recommend_company.project,is_man=True,is_delete=False,rank__lt=recommend_company.rank).aggregate(Max('rank'))
    if max_rank['rank__max']:
        recommend_company.rank=max_rank['rank__max']-1
    else:
        recommend_company.rank-=1

    recommend_company.save()
    return redirect("project.recommend",recommend_company.project.id)


@login_required
def recommendCampanyCount(request, id):
    is_english = False
    project = get_object_or_404(Project, pk=id)
    #search member_company according to the industry exclude exist industry
    resultList = {}
    resultList["m"] = project
    companyResultList = []
    if project.company_industry:
        totalCount =0
        searchCondition = ""
        if project.cv3:
            searchCondition = project.cv3
        elif project.cv2:
            searchCondition = project.cv2
        elif project.cv1:
            searchCondition = project.cv1

        if is_english:
            orient_investmentCompany = InvestmentCompany.objects.filter(invest_field__contains=searchCondition).values("name_cn").distinct()
            orient_investcompany_count = InvestmentCompany.objects.filter(invest_field__contains=searchCondition).values("name_cn").distinct().count()
        else:
            orient_investmentCompany = InvestmentCompany.objects.filter(invest_field__contains=searchCondition).values("name_cn").exclude(name_cn="-").distinct().exclude(name_cn="")
            orient_investcompany_count = InvestmentCompany.objects.filter(invest_field__contains=searchCondition).values("name_cn").exclude(name_cn="-").distinct().exclude(name_cn="").count()
        resultList["orient_investmentCompany"] = orient_investmentCompany
        resultList["orient_investcompany_count"] = orient_investcompany_count
        totalCount = totalCount + orient_investcompany_count

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
            companyList_demand = Company.objects.filter(member__in=set(memberIds)).exclude(id__in=project.target_companies.all()).values("name_cn").exclude(id=project.member.company.id)
            resultList["companyList_demand"] = companyList_demand
            companyList_demandCount = Company.objects.filter(member__in=set(memberIds)).exclude(id__in=project.target_companies.all()).values("name_cn").exclude(id=project.member.company.id).count()

            resultList["demand_count"] = companyList_demandCount
            totalCount = totalCount + companyList_demandCount

        q1 = Q(status=1) #Company().STATUS_TYPES["1"]
        q2 = Q()
        if project.cv3:
            q2 = q2 | Q(industry__id=project.cv3)
        elif project.cv2:
            q2 = q2 | Q(industry__id=project.cv2)
        elif project.cv1:
            q2 = q2 | Q(industry__id=project.cv1)

        q1 = q1 & q2
        exsitCompany = []
        if companyResultList:
            for rl in companyResultList:
                exsitCompany.append(rl["id"])

        member_companyList_notexsit_same_count = Company.objects.filter(q1).exclude(id__in=project.target_companies.all()).exclude(id=project.member.company.id).exclude(id__in=exsitCompany).count()
        totalCount = totalCount + member_companyList_notexsit_same_count

        member_companyList = Company.objects.filter(q1).exclude(id__in=project.target_companies.all()).exclude(id=project.member.company.id)
        resultList["member_companyList"] = member_companyList
        member_companyListCount = Company.objects.filter(q1).exclude(id__in=project.target_companies.all()).exclude(id=project.member.company.id).count()
        resultList["industry_company_count"] = member_companyListCount

        q3 = Q()
        if project.cv3:
            q3 = q3 | Q(cv3=project.cv3)
        elif project.cv1:
            q3 = q3 | Q(cv1=project.cv1)
        elif project.cv2:
            q3 = q3 | Q(cv2=project.cv2)

        exsitInvestmentCompany = ProjectOtherTargetCompany.objects.filter(project__id=project.id, table_name=2)
        companyList = InvestmentHistory.objects.filter(q3).values("company").exclude(company=exsitInvestmentCompany)
        if is_english:
            investmentCompany = InvestmentCompany.objects.filter(id__in=companyList).values("name_cn").distinct()
            investmentCompanyCount = InvestmentCompany.objects.filter(id__in=companyList).distinct().values("name_cn").distinct().count()
        else:
            investmentCompany = InvestmentCompany.objects.filter(id__in=companyList).exclude(name_cn="-").exclude(name_cn="").values("name_cn").distinct()
            investmentCompanyCount = InvestmentCompany.objects.filter(id__in=companyList).exclude(name_cn="-").exclude(name_cn="").values("name_cn").distinct().count()
        resultList["investmentCompany"] = investmentCompany
        resultList["industry_investcompany_count"] = investmentCompanyCount
        totalCount = totalCount + investmentCompanyCount

        exsitListedCompany = ProjectOtherTargetCompany.objects.filter(project__id=project.id, table_name=1)
        if is_english:
            listedCompanyList = ListedCompany.objects.filter(q2).exclude(industry=exsitListedCompany).values("name_cn").distinct()
            listedCompanyListCount = ListedCompany.objects.filter(q2).exclude(industry=exsitListedCompany).exclude(name_cn="").values("name_cn").distinct().count()
        else:
            listedCompanyList = ListedCompany.objects.filter(q2).exclude(industry=exsitListedCompany).exclude(name_cn="-").distinct().values("name_cn").exclude(name_cn="").distinct()
            listedCompanyListCount = ListedCompany.objects.filter(q2).exclude(industry=exsitListedCompany).exclude(name_cn="-").distinct().values("name_cn").exclude(name_cn="").distinct().count()
        resultList["listedCompanyList"] = listedCompanyList
        resultList["list_company_count"] = listedCompanyListCount
        totalCount = totalCount + listedCompanyListCount
        resultList["total_count"] = totalCount
    return render_to_response("project/recommend.html", resultList, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required("project")
def approve(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            p = Project.objects.get(pk=id)
            old_status = p.status
            p.status = StatusProject.approved
            p.save()
            adminuser = AdminUser.objects.get(pk=request.session['uid'])
            _save_check_log(adminuser, "", ResultsProjectCheck.approve, p)
            if old_status == StatusProject.pending:
                _send_check_email(p, True, "")
                _send_push_email(p)
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@login_required
@permission_required("project")
def ban(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            p = Project.objects.get(pk=id)
            p.status = StatusProject.offline
            p.save()
            adminuser = AdminUser.objects.get(pk=request.session['uid'])
            _save_check_log(adminuser, u"管理员下线", ResultsProjectCheck.offline, p)
            # _send_check_email(p, False, u"完善资料")
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


def _load_types(c):
    curr_year = datetime.datetime.today().year
    history_year = []
    for i in range(curr_year):
        if i == 4:
            break
        history_year.append(curr_year - i)
    c["history_year"] = history_year
    c["members"] = Member.objects.all()
    c['countries'] = Country.objects.order_by("-sort").all()
    c['regionlevelones'] = RegionLevelOne.objects.order_by('-sort').all()
    if (c['u'].regionlevelone):
        c['regionleveltwos'] = c['u'].regionlevelone.regionleveltwo_set.all()
    if (c['u'].regionleveltwo):
        c['regionlevelthrees'] = c['u'].regionleveltwo.regionlevelthree_set.all()
    c["companies"] = Company.active_list()
    c['industries'] = Industry.objects.filter(level=1, is_display=True)
    c['audits'] = AccountingFirm.objects.all()
    c['stockStructureType'] = StockStructure.TYPES
    c['projectServiceType'] = ProjectServiceType


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



@login_required
def get_companies(request, kv):
    companies = Company.objects.filter(name_cn__contains=kv,status__lte=1)[0:10]
    _list=[]
    for item in companies:
        _obj={}
        _obj['id']=item.id

        _obj['company_type_cn']=item.get_type_display()
        _obj['name_cn']=item.name_cn
        _list.append(_obj)



    data = json.dumps(_list)
    return HttpResponse(data, mimetype='javascript/json')


@login_required
def get_members(request, kv):
    members = Member.objects.filter(first_name__contains=kv, status=1)[0:10]
    _list = []
    for item in members:
        _obj = {}
        _obj['id']=item.id
        _obj['first_name'] = item.first_name
        _list.append(_obj)
    data = json.dumps(_list)
    return HttpResponse(data, mimetype='javascript/json')

@login_required
def get_company(request, type_id,id):
    try:
        if type_id==0:
            company = Company.objects.filter(pk=id,status=1)[0:1]
        elif type_id==1:
            company = InvestmentCompany.objects.filter(pk=id)[0:1]
        else:
            company = ListedCompany.objects.filter(pk=id)[0:1]

        data = serializers.serialize('json', company)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return None


@csrf_exempt
@login_required
@permission_required("project")
def bankingGenuisSaveNew(request):
    response_data = {}
    response_data['result'] = 'error'
    if request.method == "POST":
        try:
            operate = int(request.POST.get('operate', 99))          #99 表示異常傳遞數據
            itemIds = request.POST.get('itemIds', False)            #recommend　ｉｄ

            memberIds = request.POST.get('memberIds', False)      #用户　ｉｄ
            project_id = request.POST.get('project_id', False)
            needSendEmailMember = []       #need send email company
            project = Project.objects.get(id=project_id)
            if operate < 6:
                mids = memberIds.split(",")
                if itemIds:
                    iids = itemIds.split(",")
                    #check if recommendid is exsit in target company detail
                    exsitPtods = ProjectTargetMemberDetail.objects.filter(recommondItem__in=iids, project_id=project_id)

                    exsitItemIds = []
                    if exsitPtods.count() > 0:
                        for e in exsitPtods:
                            exsitItemIds.append(e.recommondItem_id)
                    #check if recommendid is exsit in target company detail end
                    for itemId, member_id in zip(iids, mids):
                        if int(itemId) not in exsitItemIds:
                            ptod = ProjectTargetMemberDetail()
                            ptod.project_id = project_id
                            ptod.member_id = member_id
                            ptod.recommondItem_id = itemId
                            ptod.recommend_type = 2
                            ptod.status = operate
                            if project.status == StatusProject.approved:
                                ptod.is_sender = 1
                            ptod.save()
                            ri = MemberRecommendScore.objects.get(id=itemId)
                            ri.is_in_control_panel = True
                            ri.save()
                        if operate == 1:
                            member = Member.objects.filter(id=member_id).values("id", "email", "first_name", "last_name")
                            if member:
                                needSendEmailMember.append(member)
                else:
                    for member_id in mids:
                        ptod = ProjectTargetMemberDetail()
                        ptod.project_id = project_id
                        ptod.company_id = member_id
                        ptod.recommend_type = 2
                        ptod.status = operate
                        if project.status == StatusProject.approved:
                            ptod.is_sender = 1
                        ptod.save()
                        response_data['editId'] = ptod.id
                        if operate == 1:
                            member = Member.objects.filter(id=member_id).values("id", "email", "first_name", "last_name")
                            if member:
                                needSendEmailMember.append(member)
                response_data['result'] = 'success'

            if operate == 1 and project.status == StatusProject.approved:
                if needSendEmailMember:
                    for mrs in needSendEmailMember:
                        if len(mrs) > 0:
                            for mr in mrs:
                                if mr["email"]:

                                    publisher_company = "NewChama DealGenius"
                                    #publisher = Member.objects.get(pk=project.member.id)
                                    #if publisher:
                                    #    publisher_company = Company.objects.get(pk=publisher.company.id)
                                    emailAccount = ""
                                    dic = {}
                                    handle_dynamic_email_module(dic, project, mr)

                                    html_content = loader.render_to_string("project/email_push.html", dic)
                                    emailAccount = mr["email"]
                                    if not IS_PRODUCT_HOST:
                                        emailAccount = TEST_EMAIL
                                    title = '%s-%s %s' % (project.member.company.short_name_cn, project.member.first_name, project.name_cn)
                                    try:
                                        send_email_by_mq('email', 'email', title, emailAccount, html_content)
                                    except Exception, e:
                                        msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [emailAccount])
                                        msg.content_subtype = "html"  # Main content is now text/html
                                        msg.send()

                                _save_message(project, mr)
                                _save_email_tracking(project, mr, 'cms_deal_to_buyer')
        except Exception, e:
            logger.error(e.message, exc_info=True)
            response_data['message'] = e.message
    return HttpResponse(simplejson.dumps(response_data), content_type="text/plain")


@csrf_exempt
@login_required
@permission_required("project")
def bankingGenuisSave(request):
    response_data = {}
    response_data['result'] = 'error'
    if request.method == "POST":
        try:
            operate = int(request.POST.get('operate', 99))          #99 表示異常傳遞數據
            itemIds = request.POST.get('itemIds', False)            #recommend　ｉｄ

            companyIds = request.POST.get('companyIds', False)      #公司　ｉｄ
            project_id = request.POST.get('project_id', False)
            needSendEmailMember = []       #need send email company
            noteBDToFollow = []
            project = Project.objects.get(id=project_id)

            if operate < 6:
                cids = companyIds.split(",")
                if itemIds:
                    iids = itemIds.split(",")
                    #check if recommendid is exsit in target company detail
                    exsitPtods = ProjectTargetCompanyDetail.objects.filter(recommondItem__in=iids, project_id=project_id)
                    exsitItemIds = []
                    if exsitPtods:
                        for e in exsitPtods:
                            exsitItemIds.append(e.recommondItem_id)
                    #check if recommendid is exsit in target company detail end
                    for itemId, company_id in zip(iids, cids):
                        if int(itemId) not in exsitItemIds:
                            ptod = ProjectTargetCompanyDetail()
                            ptod.project_id = project_id
                            ptod.company_id = company_id
                            ptod.recommondItem_id = itemId
                            ptod.member_id = project.member.id
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
                        ptod.member_id = project.member.id
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
                if needSendEmailMember:
                    # email_list=[]
                    # content_list=[]
                    for mrs in needSendEmailMember:
                        if len(mrs) > 0:
                            for mr in mrs:
                                if mr["email"]:

                                    publisher_company = "NewChama DealGenius"
                                    #publisher = Member.objects.get(pk=project.member.id)
                                    #if publisher:
                                    #    publisher_company = Company.objects.get(pk=publisher.company.id)
                                    emailAccount = ""
                                    dic = {}
                                    handle_dynamic_email_module(dic, project, mr)

                                    html_content = loader.render_to_string("project/email_push.html", dic)

                                    emailAccount = mr["email"]
                                    if not IS_PRODUCT_HOST:
                                        emailAccount = TEST_EMAIL
                                    title = '%s-%s %s' % (project.member.company.short_name_cn, project.member.first_name, project.name_cn)
                                    try:
                                        send_email_by_mq('email', 'email', title, emailAccount, html_content)
                                    except Exception, e:
                                        msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [emailAccount])
                                        msg.content_subtype = "html"  # Main content is now text/html
                                        msg.send()

                                _save_message(project, mr)
                                _save_email_tracking(project, mr, 'cms_deal_to_buyer')

                if noteBDToFollow:
                    noEmailcompanies = Company.objects.filter(id__in=noteBDToFollow)
                    dic = {'link': _get_project_link(project_id), 'noEmailcompanies': noEmailcompanies, 'projectName': project.name_cn}
                    html_content = loader.render_to_string("project/email_not_push.html", dic)
                    noPublishemail = BD_EMAIL
                    if not IS_PRODUCT_HOST:
                        noPublishemail = TEST_EMAIL
                    #
                    #logger.debug("send email to " + str(emailAccount))
                    title='Newchama未成功推送项目提醒'
                    try:
                        send_email_by_mq('email', 'email', title, noPublishemail, html_content)
                    except Exception, e:
                        msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [noPublishemail])
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()
            #add to favorite
            # elif operate == 2:
            result = 'success'
            # response_data['id'] = p.id
        except Exception, e:
            logger.error(e.message, exc_info=True)
            response_data['message'] = e.message
    return HttpResponse(simplejson.dumps(response_data), content_type="text/plain")


def handle_dynamic_email_module(dic, project, mr={}):
    publisher_company = "未公布"
    publisher_company = project.member.company.name_cn
    dic["publisher_company"] = publisher_company
    dic["publisher_name"] = project.member.first_name
    dic["link"] = _get_project_link(str(project.id))
    dic["p"] = project

    currency_type = project.get_currency_type_financial_display()
    i = 2
    if project.deal_size and currency_type:
        dic["table_head_" + str(i)] = "融资规模"
        dic["table_column_" + str(i)] = myTags.formatCurrency2(project.deal_size, currency_type)
        i = i + 1
    #else:
    #    dic["table_head_2"] = "所在行业"
    #    industry_name = "N/A"
    #    if project.company_industry:
    #        industry_name = project.company_industry.name_cn
    #    dic["table_column_2"] = industry_name

    if project.project_stage and project.service_type == 2:
        dic["table_head_" + str(i)] = "融资阶段"
        project_stage_name = SubDetailDealType.objects.get(pk=project.project_stage).name_cn
        dic["table_column_" + str(i)] = project_stage_name
        i = i + 1

    if project.regionlevelone :
        dic["table_head_" + str(i)] = "所在地域"
        dic["table_column_" + str(i)] = str(project.regionlevelone) + str(project.regionleveltwo) + str(project.regionlevelthree)
        i = i + 1

    if project.multi_currency :
        dic["table_head_" + str(i)] = "交易币种"
        dic["table_column_" + str(i)] = project.project_multi_currency
        i = i + 1

    mks = project.project_keyword.all()
    keywords = []
    if len(mks) > 0:
        for m in mks:
            keywords.append(m.keyword)
        dic["keywords"] = keywords[0]
        if len(keywords) >= 2:
            if (len(keywords[0]) + len(keywords[1])) < 16:
                dic["keywords"] = keywords[0] + "  " + keywords[1]

    if ('first_name' in mr and mr["first_name"].strip()) \
            or ('last_name' in mr and mr["last_name"].strip()):
        dic["user_name"] = mr["first_name"] + " " + mr["last_name"]

    query = ProjectAttach.objects.filter(project = project).order_by('-id')
    if len(query) > 0:
        dic["attach_link"] = settings.DOMAIN + settings.MEDIA_URL + '/project/' + query[0].new_name
    try:
        email_tracking_id = EmailTracking.objects.latest('pk').pk + 1
    except Exception, e:
        email_tracking_id = 1

    tracking_url = DOMAIN + 'account/email_log/tracking_%d.png' % email_tracking_id
    dic["log_email_tracking_url"] = tracking_url

    #key = 'some member uninterest a project'
    #token = base64.encodestring(custom_crypto.encrypt(key, '%d,%d,%d,%s' \
    #    % (email_tracking_id, project.id, mr.get('id', 0), mr.get('email', ''))))

    #for i in range(6):
    #    dic['uninteresting_' + str(i)] = '%saccount/uninteresting/%s/%d' % ( DOMAIN, token, i)

    return dic


def _save_message(project, mr):

    autoMsg = Message()
    autoMsg.project_id = project.id
    autoMsg.type_relation = 1
    autoMsg.sender_id = project.member.id
    autoMsg.receiver_id = mr["id"]
# autoMsg.is_read = 1             #set is_read has already read when use recommond click
    autoMsg.content = "[推送]您好，这是我的项目Teaser。若您对此感兴趣，欢迎与我取得联系。"
#autoMsg.content = loader.render_to_string("sales/"+request.lang+"/message.html", dic)
    autoMsg.save()
    update_message_log(autoMsg)


def _save_email_tracking(project, mr, action):
    email_tracking = EmailTracking()
    email_tracking.action = action
    if 'id' in mr:
        email_tracking.buyer_id = mr['id']
    email_tracking.receiver_email = mr['email']
    if 'seller_id' in mr:
        email_tracking.seller_id = mr['seller_id']
    email_tracking.item_type = 'project'
    email_tracking.item_id = project.id
    email_tracking.status = 1
    email_tracking.save()

