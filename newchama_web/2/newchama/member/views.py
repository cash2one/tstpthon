#encoding:utf-8
from django.http import Http404
from django.shortcuts import render_to_response, redirect, HttpResponse, get_object_or_404, RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from models import Company, Member, EntryForm, InviteCode, StatusEntryForm, StatusMember, CVSourceContact,CompanyInvestmentHistory,CompanyInvestmentField,CompanyStockSymbol, MemberInvestmentField, BuyerDealCategory, DetailDealType, MemberCard,\
    RegionLevelOne, RegionLevelTwo, RegionLevelThree
from member_message.models import Message
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from area.models import Country, Province, City
from industry.models import Industry
from django.core import serializers
from newchama.helper import send_email_by_mq
from repository.models import StockExchange
import datetime
import os
from decimal import Decimal
from newchama import settings
from django.contrib import messages
import hashlib
from django.core.mail import send_mail, EmailMessage
from newchama.decorators import login_required, permission_required
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template import loader, Context
from newchama.settings import EMAIL_HOST_USER,IS_PRODUCT_HOST, TEST_EMAIL, MEDIA_ROOT
import random
import logging
from tracking.models import TrackingItem
from adminuser.models import AdminUser
from django.db.models import Q
from project.models import Project
from demand.models import Demand
from math import floor, log10, pow
from recommond.compute_member_recommend_new import calculate_matching_tables_score, access_project_tag_fuzzy_word

from recommond.util import get_single_member_value_dict
from django.db import transaction
from recommond.models import MemberRecommendScore

logger = logging.getLogger(__name__)

@login_required
@permission_required("member")
def index(request):
    c = {}
    download = request.GET.get("download", "")
    keyword = request.GET.get("keyword", "")
    type = request.GET.get("type", "")
    status = request.GET.get("status", "")
    data = Member.objects.all().order_by("-id")

    condition = Q()
    condition2 = Q()
    if status != "":
        condition = Q(status=status)
        c["status"] = int(status)

    if type != "":
        condition = Q(type=type)
        c["type"] = int(type)

    if keyword.strip() != "":
        condition2 = condition2 | Q(email__icontains=keyword.strip()) | Q(last_name__icontains=keyword.strip()) | Q(first_name__icontains=keyword.strip())
        c["keyword"] = keyword

    c["data"] = data.filter(condition & condition2)
    c["Types"] = Member.TYPES
    c["StatusType"] = Member.STATUS_TYPE
    c["total"] = data.count()


    if download != "":
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="member.csv"'
        t = loader.get_template('member/member_download_template.txt')
        d = Context({
            'data': data,
        })
        response.write(t.render(d))
        return response
    return render_to_response("member/list.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("member")
@csrf_protect
def add(request):
    c = {}
    c.update(csrf(request))
    u = Member()
    if request.method == 'POST':
            _bind_data_member(request, u)
            if u.email == "":
                messages.warning(request, "please input email")
            elif u.position_cn == "":
                messages.warning(request, "please input position")
            else:
                count = Member.objects.filter(email=u.email).count()
                if count > 0:
                    messages.warning(request, "email is exist")
                else:
                    try:
                        password = request.POST["password"]
                        u.make_password(password)
                        u.status=3
                        creator_id = request.session['uid']
                        creator = AdminUser.objects.get(pk=creator_id)
                        u.creator = creator
                        u.source_create = 'cms'
                        u.save()


                        #BD注册的用户发送邮件，暂时注释，请勿删除

                        if u.type == u'4':
                            mail_dic = dict()
                            mail_dic['username'] = u.first_name + " " + u.last_name
                            mail_dic['email'] = u.email
                            mail_dic['password'] = password
                            mail_dic['creator'] = creator.username

                            html_content = loader.render_to_string("member/email_member_bd_add.html",mail_dic)
                            msg = EmailMessage('NewChama 欢迎你 - 用户注册通知', html_content, EMAIL_HOST_USER, [u.email])
                            msg.content_subtype = "html"  # Main content is now text/html
                            msg.send()

                        return redirect("member.index")
                    except Exception, e:
                        messages.warning(request, e.message)
                        logging.error(e.message)
    c["u"] = u
    _load_data_member(c)
    return render_to_response("member/add.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("member")
@csrf_protect
def edit(request, id):
    c = {}
    c.update(csrf(request))
    msg = ""
    u = get_object_or_404(Member, pk=id)
    if request.method == 'POST':
            # id_post = request.POST["id"]
            # u = Member.objects.get(pk=id_post)
            b = _bind_data_member(request, u)
            if b:
                try:
                    u.save()
                    if u.position_cn == "":
                        messages.warning(request, "please input position")
                    else:
                        return redirect("member.index")
                except Exception, e:
                    messages.warning(request, e.message)
                    logging.error(e.message)

    c["u"] = u
    _load_data_member(c)
    business_cards = MemberCard.objects.filter(member=u, is_delete=False).order_by('-add_time')
    if len(business_cards) >= 1:
        c["card_file"] = business_cards[0].new_name

    c['project_list']=Project.objects.exclude(status=5).filter(member=u).order_by('-id')
    c['demand_list']=Demand.objects.exclude(status=5).filter(member=u).order_by('-id')
    c['trackingdata']=TrackingItem.objects.filter(tracking_type=1,tracking_id=id).order_by('-add_time')
    c['matchingdata'] = MemberInvestmentField.objects.filter(member=u).order_by('-add_time')
    return render_to_response("member/edit.html", c, context_instance=RequestContext(request))


def member_autocomplete_search(request, keyword):
    #auto complete param
    if keyword is not None and keyword != "":
        member_list = Member.objects.filter(email__contains=keyword)
        json_data = serializers.serialize('json', member_list, fields=('first_name', 'last_name'))
        return HttpResponse(json_data, mimetype='javascript/json')
    else:
        return HttpResponse("")


@login_required
@permission_required("member")
@csrf_protect
def reset_password(request, id):
    c = {}
    c.update(csrf(request))
    u = get_object_or_404(Member, pk=id)
    if request.method == 'POST':
        password = request.POST["password"]
        if password == "":
            messages.warning(request, "please input password")
        else:
            uid_post = request.POST["id"]
            try:
                u = Member.objects.get(pk=uid_post)
                u.make_password(password)
                u.save()
                messages.success(request, "success")
            except Exception, e:
                messages.warning(request, e.message)
                logging.error(e.message)
    c["u"] = u
    return render_to_response("member/resetpassword.html", c, context_instance=RequestContext(request))


def _bind_data_member(request, u):
    u.type = request.POST["type"]
    u.role = request.POST["role"]
    u.target_platform = request.POST['target_platform']
    company_id = request.POST["company"]
    if company_id > 0:
        u.company = Company.objects.get(pk=company_id)
    u.email = request.POST["email"]
    u.expire_date = request.POST["expire_date"]
    u.first_name = request.POST["first_name"]
    # u.last_name = request.POST["last_name"]
    #u.gender = request.POST["gender"]
    u.tel = request.POST["tel"]
    u.mobile = request.POST["mobile"]
    u.position_cn = request.POST["position_cn"]
    u.position_en = request.POST["position_en"]
    u.intro_cn = request.POST["intro_cn"]
    u.intro_en = request.POST["intro_en"]
    u.tel = request.POST["tel"]

    u.weibo_url = request.POST["weibo_url"]

    u.avatar = "default_male.jpg"

    if u.avatar == 2:
        u.avatar = "default_female.jpg"
    if u.status != int(request.POST["status"]):
        u.status = int(request.POST["status"])
        is_right = False
        reason = ''
        if u.status == 0 or u.status == 2:  # 0: authentication failure, 2: blacklist
            reason = request.POST.get('reason', '')
            is_right = False
        elif u.status == 1:  # 1: authentication success
            is_right = True
        if u.status in [0, 1, 2]:
            _send_account_email(is_right, u.email, u.company.name_cn, reason, u.first_name, u.add_time, u.role)

    owner_id = int(request.POST["owner"], 0)
    if owner_id > 0:
        u.owner = AdminUser.objects.get(pk=owner_id)
    else:
        messages.warning(request, "please select owner.")
        return False
    u.source_channel = request.POST.get('source_channel','')
    return True


def _load_data_member(c):
    c["companies"] = Company.objects.filter(Q(status=1) | Q(status=4)).order_by('short_name_cn')
    c["adminusers"] = AdminUser.objects.filter(isactive=0)
    c["MEMBER_TYPES"] = Member.TYPES


@login_required
@permission_required("member")
@csrf_protect
def invite(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        email = request.POST['email']
        if email == "":
            messages.warning(request, "please input email")
        else:
            count = Member.objects.filter(email=email).count()
            if count == 0:
                #invitecode = InviteCode()
                # sender is admin user
                #invitecode.invite_user = Member.objects.get(pk=1)
                #invitecode.email = email
                #code = str(random.randint(0, 99999999)).zfill(8)
                #invitecode.code = code
                #invitecode.save()
                html_content = loader.render_to_string("member/email_invite.html")
                msg = EmailMessage('NewChama Invite Message', html_content, EMAIL_HOST_USER, [email])
                msg.content_subtype = "html"  # Main content is now text/html
                try:
                    msg.send()
                    messages.success(request, "success")
                except Exception, e:
                    messages.error(request, e.message)
            else:
                messages.warning(request, "email is exist")
    return render_to_response("member/invite.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("member")
def entryforms(request):
    c = {}
    c.update(csrf(request))
    msg = ""
    download = request.GET.get("download", "")
    keyword = request.GET.get("keyword", "")
    data = EntryForm.objects.all().order_by("-id")
    if keyword != "":
        data = data.filter(email__contains=keyword)
        c["keyword"] = keyword
    c['data'] = data
    c['StatusEntryForm'] = StatusEntryForm
    if download != "":
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="entryforms.csv"'
        t = loader.get_template('member/entryform_download_template.txt')
        d = Context({
            'data': data,
        })
        response.write(t.render(d))
        return response
    return render_to_response("member/entryforms.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("member")
def entryform_check(request, id):
    c = {}
    c.update(csrf(request))
    msg = ""
    f = get_object_or_404(EntryForm, pk=id)
    if f.status == StatusEntryForm.approved:
        return HttpResponse("the entry form is approved")
    c['u'] = f
    isvalid = True
    if request.method == 'POST':
        id_post = request.POST["id"]
        status = StatusEntryForm.approved
        first_name = request.POST["first_name"]
        # last_name = request.POST["last_name"]
        intro_cn = request.POST["intro_cn"]
        intro_en = request.POST["intro_en"]
        expire_date = request.POST["expire_date"]
        position_cn = request.POST["position_cn"]
        position_en = request.POST["position_en"]
        type = request.POST["type"]
        reason = request.POST["reason"]
        c['first_name'] = first_name
        # c['last_name'] = last_name
        c['expire_date'] = expire_date
        c['intro_cn'] = intro_cn
        c['intro_en'] = intro_en
        c['expire_date'] = expire_date
        c['position_cn'] = position_cn
        c['position_en'] = position_en
        c['type'] = type
        c['reason'] = reason
        is_right = True
        member = Member()
        company_name = request.POST['company_name']

        if "btn_disapprove" in request.POST:
            status = StatusEntryForm.not_approved
            if reason == "":
                isvalid = False
                messages.warning(request, "please input reason")
            is_right = False
        else:
            company_id = request.POST['company']
            if company_id == "0" or company_id == "":
                isvalid = False
                messages.warning(request, "please select company")
            if request.POST["expire_date"] == "":
                isvalid = False
                messages.warning(request, "please select expire date")
            form = EntryForm.objects.get(pk=id_post)
            _member_num = Member.objects.filter(email=form.email).count()
            if _member_num > 0:
                messages.warning(request, "The email account is exsit.")
                isvalid = False
            if isvalid:
                member.company_id = company_id
                member.email = form.email
                member.expire_date = expire_date
                member.first_name = first_name
                # member.last_name = last_name
                member.gender = form.gender
                member.intro_cn = intro_cn
                member.intro_en = intro_en
                #member.invite_code = form.invite_code
                #member.invite_user = InviteCode.objects.get(code=form.invite_code).invite_user
                member.mobile = form.mobile
                member.tel = form.tel
                member.position_cn = position_cn
                member.position_en = position_en
                member.password = form.password
                member.add_time = form.add_time
                member.type = type
                member.status = StatusMember.normal
                member.avatar = "default_male.jpg"
                member.source_create = "web"
                if member.gender == 2:
                    member.avatar = "default_female.jpg"

                #when the account is approve then still generate active code  20150722
                member.activecode = hashlib.new('md5', str(datetime.datetime.now())+member.email).hexdigest()
                member.status = StatusMember.activing
                # end  20150722

                # company_name = member.company.name_cn
                Company.objects.filter(pk=company_id, status=4).update(status=1)         #make the company normal status

                # and send active email  20150722
                send_active(member.email, member.activecode, member.first_name)
                member.save()
        if isvalid:
            EntryForm.objects.filter(pk=id_post).update(status=status)

            # if account need active code valid, do not send the approve email
            # if IS_PRODUCT_HOST:
            #     _send_account_email(is_right, f.email, company_name, reason,member.first_name, member.add_time)
            # else:
            #     _send_account_email(is_right, TEST_EMAIL, company_name, reason,member.first_name, member.add_time)
            return redirect("entryform.list")
    _load_data_member(c)
    return render_to_response("member/entryform_check.html", c, context_instance=RequestContext(request))



def send_active(email, activecode, userName):
    if not IS_PRODUCT_HOST:
        email = TEST_EMAIL
    html_content = loader.render_to_string("member/email_active.html", {'username':userName,'activecode':activecode,'email':email})
    title = 'NewChama邀请信'
    try:
        send_email_by_mq('email', 'email', title,email, html_content)
    except Exception, e:
        logger.error(e.message, exc_info=True)


def _send_account_email(is_right, email, company, reason,name, add_time, role):
    if not IS_PRODUCT_HOST:
        email = TEST_EMAIL
    mail_dic = dict()
    mail_dic['is_right'] = is_right
    mail_dic['email'] = email
    mail_dic['company'] = company
    mail_dic['reason'] = reason
    mail_dic['name'] = name
    mail_dic['add_time'] = add_time
    mail_dic['role'] = role

    # mail_dic['sex'] = sex
    html_content = loader.render_to_string("member/email_message.html", mail_dic)
    msg = EmailMessage(u'NewChama用户注册通知', html_content, EMAIL_HOST_USER, [email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


@login_required
@permission_required("member")
def entryform_detail(request, id):
    c = {}
    c.update(csrf(request))
    f = get_object_or_404(EntryForm, pk=id)
    c['u'] = f
    return render_to_response("member/entryform_detail.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("company")
@csrf_protect
def add_company(request):
    c = {}
    c.update(csrf(request))
    u = Company()
    if request.method == 'POST':
        _bind_data_company(request, u)
        if u.name_cn == "":
            messages.warning(request, "请输入中文全称！")
        else:
            count = Company.objects.exclude(status=3).filter(name_cn=u.name_cn).count()
            if count > 0:
                messages.warning(request, "中文全称已存在！")
            else:
                try:
                    u.save()
                    intro_file = request.FILES.get("intro_file")
                    if intro_file is not None:
                        intro_file_name = _upload_company_file(intro_file, u.id, "file")
                        u.intro_file = intro_file_name
                    logo_file = request.FILES.get("logo")
                    if logo_file is not None:
                        logo_file_name = _upload_company_file(logo_file, u.id, "logo")
                        u.logo = logo_file_name
                    u.save()
                    return redirect("company.list")
                except Exception, e:
                    messages.warning(request, e.message)
                    logging.error(e.message)
    c['u'] = u
    _load_data_company(c)
    return render_to_response("member/add_company.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("company")
@csrf_protect
def edit_company(request, id):
    c = {}
    c.update(csrf(request))
    u = get_object_or_404(Company, pk=id)
    if request.method == 'POST':
        id_post = request.POST["id"]
        u = Company.objects.get(pk=id_post)
        _bind_data_company(request, u)
        if u.name_cn == "":
            messages.warning(request, "请输入中文全称！")
        else:
            count = Company.objects.filter(name_cn=u.name_cn).exclude(Q(pk=id_post)|Q(status=3)).count()
            if count > 0:
                messages.warning(request, "中文全称已存在！")
            else:
                try:
                    intro_file = request.FILES.get("intro_file")
                    if intro_file is not None:
                        intro_file_name = _upload_company_file(intro_file, u.id, "file")
                        u.intro_file = intro_file_name
                    logo_file = request.FILES.get("logo")
                    if logo_file is not None:
                        logo_file_name = _upload_company_file(logo_file, u.id, "logo")
                        u.logo = logo_file_name
                    u.save()
                    return redirect("company.list")
                except Exception, e:
                    messages.warning(request, e.message)
                    logging.error(e.message)
    c["u"] = u
    c['historydata'] = CompanyInvestmentHistory.objects.filter(company=u).order_by('-happen_date')
    c['matchingdata'] = CompanyInvestmentField.objects.filter(company=u).order_by('-add_time')
    c['memberdata'] = Member.objects.filter(company=u).order_by('-id')

    _load_data_company(c)
    return render_to_response("member/edit_company.html", c, context_instance=RequestContext(request))


@login_required
def company_autocomplete_search(request, keyword):
    #auto complete param
    if keyword is not None and keyword != "":
        company_list = Company.objects.filter(name_cn__contains=keyword)  #.only('id', 'short_name_en', 'name_en')
        json_data = serializers.serialize('json', company_list, fields=('short_name_cn', 'short_name_en', 'name_en', 'name_cn'))
        return HttpResponse(json_data, mimetype='javascript/json')
    else:
        return HttpResponse("")


def _bind_data_company(request, u):
    u.address_cn = request.POST['address_cn']
    u.address_en = request.POST['address_en']
    if request.POST.get('country', False):
        country_id = request.POST['country']
        u.country = Country.objects.get(id=country_id)

    if request.POST.get('regionlevelone', False):
        u.regionlevelone_id = request.POST.get('regionlevelone');

    if request.POST.get('regionleveltwo', False):
        u.regionleveltwo_id = request.POST.get('regionleveltwo');

    if request.POST.get('regionlevelthree', False):
        u.regionlevelthree_id = request.POST.get('regionlevelthree');

    industry_id = request.POST['industry_id']
    if industry_id != "0":
        u.industry = Industry.objects.get(id=industry_id)
    u.fax = request.POST['fax']
    u.tel = request.POST['tel']
    u.website = request.POST['website']
    u.name_cn = request.POST['name_cn']
    u.name_en = request.POST['name_en']
    u.short_name_cn = request.POST['short_name_cn']
    u.short_name_en = request.POST['short_name_en']
    u.intro_cn = request.POST['intro_cn']
    u.intro_en = request.POST['intro_en']
    u.investment_experience_cn = request.POST['investment_experience_cn']
    u.investment_experience_en = request.POST['investment_experience_en']
    u.postcode = request.POST['postcode']
    #u.type = request.POST['type']

    u.updated = datetime.datetime.now()
    u.capital_type = request.POST['capital_type']
    u.new_type = request.POST['new_type']
    u.is_list = int(request.POST.get("is_list", 0))




    u.status = request.POST['status']
    if request.POST['found_time']=="":
        u.found_time = None
    else:
        u.found_time = request.POST['found_time']
    u.memo = request.POST['memo']



@login_required
@permission_required("company")
def companies(request):
    c = {}
    keyword = request.GET.get("keyword", "")
    symbol = request.GET.get("symbol", "")
    type = request.GET.get("type", "")
    status = request.GET.get("status", "")
    if symbol.strip() =='':
        data = Company.objects.filter(status__lte=1).order_by("-id")

        condition = Q()
        condition2 = Q()
        if status != "":
            condition = Q(status=status)
            c["status"] = int(status)

        if type != "":
            condition2 = condition2 | Q(type=type)
            c["type"] = int(type)

        if keyword.strip() != "":
            condition2 = condition2 | Q(name_cn__icontains=keyword.strip()) | Q(name_en__icontains=keyword.strip()) | Q(short_name_cn__icontains=keyword.strip()) | Q(short_name_en__icontains=keyword.strip())
            c["keyword"] = keyword

        c["data"] = data.filter(condition & condition2)
        c["total"] = data.filter(condition & condition2).count()

    else:
        symbol_list=CompanyStockSymbol.objects.filter(stock_symbol__icontains=symbol.strip())
        company_list=list(set([item.company for item in symbol_list]))
        c["data"] = company_list
        c["total"] = len(company_list)

    c["Types"] = Company.TYPES
    c["Status"] = Company.STATUS_TYPES

    return render_to_response("member/company_list.html", c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required("company")
def remove_company(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Company.objects.filter(pk=id).update(status=3)
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@login_required
@permission_required("company")
def remove_company_file(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Company.objects.filter(pk=id).update(intro_file='')
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@login_required
@permission_required("company")
def remove_company_logo(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Company.objects.filter(pk=id).update(logo='')
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


def _load_data_company(c):
    c['countries'] = Country.objects.order_by("-sort").all()
    c['regionlevelones'] = RegionLevelOne.objects.order_by('-sort').all()
    if (c['u'].regionlevelone):
        c['regionleveltwos'] = c['u'].regionlevelone.regionleveltwo_set.all()
    if (c['u'].regionleveltwo):
        c['regionlevelthrees'] = c['u'].regionleveltwo.regionlevelthree_set.all()
    c['COMPANY_TYPES'] = Company.TYPES
    c['Capital_TYPES'] = Company.Capital_TYPES
    c['STATUS_TYPES'] = Company.STATUS_TYPES
    c['NEW_TYPES'] = Company.NEWTYPES


@login_required
def member_messages(request):
    c = {}
    data = Message.objects.all().order_by("-id")
    c["data"] = data
    download = request.GET.get("download", "")
    if download != "":
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="member_messages.csv"'
        t = loader.get_template('member/member_message_download_template.txt')
        d = Context({
            'data': data,
        })
        response.write(t.render(d))
        return response
    return render_to_response("member/messages.html", c, context_instance=RequestContext(request))


def _upload_company_file(f, id, type):
    file_name = ""
    path = settings.MEDIA_ROOT + "/companylogo/"
    if type == "file":
        path = settings.MEDIA_ROOT + "/companyfile/"
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        file_ext = os.path.splitext(f.name)[1]
        file_name = str(id) + file_ext
        destination = open(path + file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        #print file_name
    except Exception, e:
        print e
    return file_name


@login_required
def contact_cvsource(request):
    c = {}
    keyword = request.GET.get("keyword", "")
    if keyword != "":
        data = CVSourceContact.objects.filter(name__contains=keyword, is_delete=0).order_by("-count_project")
    else:
        data = CVSourceContact.objects.filter(is_delete=0)
    c["data"] = data
    return render_to_response("member/cvsources.html", c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
@permission_required("member")
def sendmail(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            is_right=True
            reason=''
            member=Member.objects.get(pk=id)
            if IS_PRODUCT_HOST:
                _send_account_email(is_right, member.email, member.company.name_cn, reason,member.first_name+member.last_name,member.gender, member.add_time, member.role)
            else:
                _send_account_email(is_right, 'jay.ying@newchama.com', member.company.name_cn, reason,member.first_name+member.last_name,member.gender, member.add_time, member.role)
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)



@login_required
@permission_required("company")
@csrf_protect
def add_company_investment_history(request,company_id):
    c = {}
    c.update(csrf(request))
    company = get_object_or_404(Company,pk=company_id)
    u = CompanyInvestmentHistory()
    u.company = company
    if request.method == 'POST':
            _bind_data_investement_history(request, u)
            if u.targetcompany_cn == "":
                messages.warning(request, "请输入目标公司中文全称！")
            else:
                count = CompanyInvestmentHistory.objects.filter(company=u.company,happen_date=u.happen_date,amount=u.amount).count()
                if count > 0:
                    messages.warning(request, "投资历史纪录已经存在!")
                else:
                    try:

                        u.save()
                        return redirect("/member/companies/edit/"+str(u.company.id))
                    except Exception, e:
                        messages.warning(request, e.message)
                        logging.error(e.message)
    c["u"] = u
    _load_data_investement_history(c)
    return render_to_response("member/add_investment_history.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("company")
@csrf_protect
def edit_company_investment_history(request, id):

    c = {}
    c.update(csrf(request))
    msg = ""
    u = get_object_or_404(CompanyInvestmentHistory, pk=id)
    if request.method == 'POST':

            _bind_data_investement_history(request, u)
            try:
                u.save()
                return redirect("/member/companies/edit/"+str(u.company.id))
            except Exception, e:
                messages.warning(request, e.message)
                logging.error(e.message)
    c["u"] = u
    _load_data_investement_history(c)
    return render_to_response("member/edit_investment_history.html", c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
@permission_required("company")
def remove_company_investment_history(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            CompanyInvestmentHistory.objects.filter(pk=id).delete()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


def _load_data_investement_history(c):
    c['countries'] = Country.objects.order_by("-sort").all()

currency_to_usd={
u'人民币':1/6.1306,
u'加元':1/1.0961,
u'台币':1/29.9790,
u'新元':1/1.2635,
u'新西兰元':0.8188,
u'日元':1/106.8900,
u'欧元':1.2911,
u'港元':1/7.7497,
u'澳元':0.9184,
u'美元':1,
u'英镑':1.6202,
u'韩元':1/1036
}

def _bind_data_investement_history(request, u):

    u.targetcompany_cn = request.POST['targetcompany_cn']
    u.targetcompany_en = request.POST['targetcompany_en']

    u.amount = float(request.POST['amount'])
    u.currency = request.POST['currency']
    u.invest_stage = request.POST['invest_stage']


    u.title_cn = request.POST['title_cn']
    u.title_en = request.POST['title_en']

    u.content_cn = request.POST['content_cn']
    u.content_en = request.POST['content_en']

    u.happen_date = request.POST['happen_date']
    u.person_cn = request.POST['person_cn']
    u.person_en = request.POST['person_en']
    industry_id = int(request.POST['industry_id'])

    city_id = int(request.POST['city_id'])
    province_id = int(request.POST['province_id'])
    country_id = int(request.POST['country'])
    print industry_id,country_id,province_id,city_id
    if industry_id and industry_id!=0:
        u.industry=get_object_or_404(Industry,pk=industry_id)

        if u.industry.level==1:
            u.cv1=u.industry.id
        if u.industry.level==2:
            u.cv1=u.industry.father.id
            u.cv2=u.industry.id
        if u.industry.level==3:
            u.cv1=u.industry.father.father.id
            u.cv2=u.industry.father.id
            u.cv3=u.industry.id

    if city_id and city_id !=0:
        u.city=get_object_or_404(City,pk=city_id)
    if province_id and province_id!=0:
        u.province=get_object_or_404(Province,pk=province_id)
    if country_id and country_id!=0:
        u.country=get_object_or_404(Country,pk=country_id)

    if u.currency and u.amount:
        u.usd=int(u.amount*currency_to_usd.get(u.currency,1))



@login_required
@permission_required("member")
@csrf_protect
def add_member_tracking(request,member_id):
    c = {}
    c.update(csrf(request))
    member = get_object_or_404(Member,pk=member_id)
    t = TrackingItem()

    uid = request.session['uid']
    admin_user=get_object_or_404(AdminUser,id=uid)
    t.user = admin_user
    if request.method == 'POST':
            _content=request.POST.get('content',None)
            if _content:
                t.content=_content
                t.tracking_type=1
                t.tracking_id=member.id
                t.tracking_name=member.first_name

                try:
                    t.save()
                    return redirect("/member/members/edit/"+str(member_id))
                except Exception, e:
                    messages.warning(request, e.message)
                    logging.error(e.message)
            else:
                messages.warning(request, "请输入内容！")
    c["t"] = t

    return render_to_response("member/add_tracking.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("company")
@csrf_protect
def matching(request):
    c = {}
    keyword = request.GET.get("keyword", "")

    _member_list=Member.objects.filter(status=1).order_by('-id').all()


    condition = Q()
    if keyword.strip() != "":
        condition = condition | Q(email__icontains=keyword.strip()) | Q(last_name__icontains=keyword.strip()) | Q(first_name__icontains=keyword.strip())
        c["keyword"] = keyword

    _member_list=_member_list.filter(condition)

    for _member in _member_list:
        _member.matching_list=CompanyInvestmentField.objects.filter(company=_member.company).all()


    c['member_list']=_member_list
    return render_to_response("member/member_matching.html", c, context_instance=RequestContext(request))



@login_required
@permission_required("company")
@csrf_protect
def matching_list(request):
    c = {}
    keyword = request.GET.get("keyword", "")

    matching_list=CompanyInvestmentField.objects.all()


    condition = Q()
    if keyword.strip() != "":
        condition = condition | Q(tags__icontains=keyword.strip())
        c["keyword"] = keyword

    matching_list=matching_list.filter(condition)
    for m in matching_list:
        m.user_list=Member.objects.filter(company=m.company,status=1).all()


    c['matching_list']=matching_list
    return render_to_response("member/member_matching_list.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("member")
@csrf_protect
def edit_member_matching(request, id):

    SCALE = (
        (0, "请选择"),
        (1000000, "百万"),
        (10000000, "千万"),
        (100000000, "亿"),
        (1000000000, "十亿"),
        (10000000000, "百亿"),
    )

    c = {}
    c.update(csrf(request))
    u = get_object_or_404(MemberInvestmentField, pk=id)
    if request.method == 'POST':
        _bind_data_member_matching(request, u)
        u.deal_size_min = Decimal(request.POST['deal_size_min']).quantize(Decimal('0.00'))
        u.deal_size_max = Decimal(request.POST['deal_size_max']).quantize(Decimal('0.00'))
        try:
            u.save()
            refresh_recommend_score(u.member.id)
            return redirect("/member/members/edit/"+str(u.member.id))
        except Exception, e:
            messages.warning(request, e.message)
            logging.error(e.message)
    if u.deal_size_min:
        c['deal_size_min_scale'] = int(pow(10, floor(log10(u.deal_size_min))))
        c['deal_size_min_digit'] = u.deal_size_min/c['deal_size_min_scale']
    else:
        c['deal_size_min_scale'] = 0
        c['deal_size_min_digit'] = 0

    if u.deal_size_max:
        c['deal_size_max_scale'] = int(pow(10, floor(log10(u.deal_size_max))))
        c['deal_size_max_digit'] = u.deal_size_max/c['deal_size_max_scale']
    else:
        c['deal_size_max_scale'] = 0
        c['deal_size_max_digit'] = 0

    c["u"] = u
    c["kv_list"] = u.tags.split(',')
    c['size_scale'] = SCALE
    c['deal_categories_list'] = [item.id for item in u.deal_category.all()]
    c['deal_types_list'] = [item.id for item in u.deal_type.all()]
    _load_data_member_matching(c)
    return render_to_response("member/edit_member_matching.html", c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
@permission_required("member")
def remove_member_matching(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            MemberInvestmentField.objects.filter(pk=id).delete()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@login_required
@permission_required("member")
@csrf_protect
def add_member_matching(request, member_id):
    c = {}
    c.update(csrf(request))
    member = get_object_or_404(Member, pk=member_id)
    u = MemberInvestmentField()
    u.member = member
    if request.method == 'POST':
        u.deal_size_min = Decimal(request.POST['deal_size_min']).quantize(Decimal('0.00'))
        u.deal_size_max = Decimal(request.POST['deal_size_max']).quantize(Decimal('0.00'))

        u.tags = request.POST.get('all_tags',None)
        u.revenue = int(request.POST['revenue'])
        u.growth = int(request.POST['growth'])
        u.net_income = int(request.POST['net_income'])
        u.ebita = int(request.POST['ebita'])
        u.deal_currency = int(request.POST['deal_currency'])
        u.multi_currency = request.POST['deal_currency']  # TODO: Jay.Ying:  multi-currency editing
        u.hot = int(request.POST['hot'])
        #if request.POST['country']:
        #    _country_id = int(request.POST['country'])
        #    if _country_id !=0:
        #        try:
        #            u.country = Country.objects.get(id=_country_id)
        #        except Exception, e:
        #            pass

        if request.POST.get('regionlevelone', False):
            u.regionlevelone_id = request.POST.get('regionlevelone');

        if request.POST.get('regionleveltwo', False):
            u.regionleveltwo_id = request.POST.get('regionleveltwo');

        if request.POST.get('regionlevelthree', False):
            u.regionlevelthree_id = request.POST.get('regionlevelthree');

        try:
            u.save()
            if request.POST.get('categories', False):
                u.deal_category.clear()
                for category in request.POST.getlist('categories'):
                    u.deal_category.add(BuyerDealCategory.objects.get(category=int(category)))
                    for _type in BuyerDealCategory.objects.get(category=int(category)).deal_types.all():
                        u.deal_type.add(DetailDealType.objects.get(deal_type=_type.deal_type))
            if request.POST.get('types', False):
                u.deal_type.clear()
                for category in u.deal_category.all():
                    if category.category != 6:
                        for _type in category.deal_types.all():
                            u.deal_type.add(DetailDealType.objects.get(deal_type=_type.deal_type))
                for _type in request.POST.getlist('types'):
                    u.deal_type.add(DetailDealType.objects.get(deal_type=int(_type)))
            #refresh_recommend_score(u.member.id)
            return redirect("/member/members/edit/"+str(u.member.id))
        except Exception, e:
            messages.warning(request, e.message)
            logging.error(e.message)
    c["u"] = u
    _load_data_member_matching(c)
    return render_to_response("member/add_member_matching.html", c, context_instance=RequestContext(request))


def refresh_recommend_score(member_id):
    member_info = get_single_member_value_dict(member_id)
    project_list = Project.objects.exclude(status=5).filter(member__id=member_id).order_by('-id')
    recommend_score_lst = []
    for project in project_list:
        fuzzy_words_lst = access_project_tag_fuzzy_word(project)
        res = calculate_matching_tables_score(project, member_info, fuzzy_words_lst)
        if res:
            recommend_score_lst.append(res)
    with transaction.atomic():
        """ delete old scores """
        MemberRecommendScore.objects.filter(member_id=member_id).delete()
        for score in recommend_score_lst:
            score.save()


def _load_data_member_matching(c):
    c['countries'] = Country.objects.order_by("-sort").all()
    c['regionlevelones'] = RegionLevelOne.objects.order_by('-sort').all()
    if (c['u'].regionlevelone):
        c['regionleveltwos'] = c['u'].regionlevelone.regionleveltwo_set.all()
    if (c['u'].regionleveltwo):
        c['regionlevelthrees'] = c['u'].regionleveltwo.regionlevelthree_set.all()
    c['revenue_types'] = MemberInvestmentField.FINANCE_TYPES
    c['currency_types'] = MemberInvestmentField.CURRENCY_TYPES
    c['growth_types'] = MemberInvestmentField.GROWTH_TYPES
    c['net_types'] = MemberInvestmentField.FINANCE_TYPES
    c['ebita_types'] = MemberInvestmentField.FINANCE_TYPES
    c['deal_categories'] = BuyerDealCategory.DEAL_CATEGORIES
    c['categories_others'] = DetailDealType.objects.filter(category=6)
    c['hot_score_list'] = range(0,11)


def _bind_data_member_matching(request, u):

    u.tags = request.POST.get('all_tags',None)
    u.revenue = int(request.POST['revenue'])
    u.growth = int(request.POST['growth'])
    u.net_income = int(request.POST['net_income'])
    u.ebita = int(request.POST['ebita'])
    u.deal_currency = int(request.POST['deal_currency'])  # TODO: Jay.Ying:  multi-currency editing
    u.multi_currency = request.POST['deal_currency']
    u.hot = int(request.POST['hot'])

    u.deal_category.clear()
    u.deal_type.clear()
    if request.POST.get('categories', False):
        for category_code in request.POST.getlist('categories'):
            category = BuyerDealCategory.objects.get(category=int(category_code))
            u.deal_category.add(category)
            if int(category_code) != 6:
                for _type in category.deal_types.all():
                    u.deal_type.add(DetailDealType.objects.get(deal_type=_type.deal_type))
    u.deal_type.remove(BuyerDealCategory.objects.get(category=6))
    if request.POST.get('types', False):
        # add category (others)
        u.deal_category.add(BuyerDealCategory.objects.get(category=6))
        for _type in request.POST.getlist('types'):
            u.deal_type.add(DetailDealType.objects.get(deal_type=int(_type)))
    if request.POST.get('country', False):
        _country_id = int(request.POST['country'])
        if _country_id !=0:
            try:
                u.country = Country.objects.get(id=_country_id)
            except Exception, e:
                pass

    if request.POST.get('regionlevelone', False):
        u.regionlevelone_id = request.POST.get('regionlevelone');

    if request.POST.get('regionleveltwo', False):
        u.regionleveltwo_id = request.POST.get('regionleveltwo');

    if request.POST.get('regionlevelthree', False):
        u.regionlevelthree_id = request.POST.get('regionlevelthree');



@login_required
@permission_required("company")
@csrf_protect
def add_company_matching(request,company_id):
    c = {}
    c.update(csrf(request))
    company = get_object_or_404(Company,pk=company_id)
    u = CompanyInvestmentField()
    u.company = company
    if request.method == 'POST':
            _bind_data_matching(request, u)
            u.deal_size_min = Decimal(request.POST['deal_size_min']).quantize(Decimal('0.00'))
            u.deal_size_max = Decimal(request.POST['deal_size_max']).quantize(Decimal('0.00'))
            try:
                u.save()
                return redirect("/member/companies/edit/"+str(u.company.id))
            except Exception, e:
                messages.warning(request, e.message)
                logging.error(e.message)
    c["u"] = u
    c['memberdata'] = Member.objects.filter(company=u.company).order_by('-id')
    _load_data_matching(c)
    return render_to_response("member/add_matching.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("company")

def edit_company_matching(request, id):

    SCALE = (
        (0, "请选择"),
        (1000000, "百万"),
        (10000000, "千万"),
        (100000000, "亿"),
        (1000000000, "十亿"),
        (10000000000, "百亿"),
    )

    c = {}
    c.update(csrf(request))
    msg = ""
    u = get_object_or_404(CompanyInvestmentField, pk=id)
    if request.method == 'POST':
        if 'btn_duplicate' in request.POST:
            company_id = u.company_id
            u = CompanyInvestmentField()
            u.company_id = company_id

        _bind_data_matching(request, u)
        u.deal_size_min = Decimal(request.POST['deal_size_min']).quantize(Decimal('0.00'))
        u.deal_size_max = Decimal(request.POST['deal_size_max']).quantize(Decimal('0.00'))
        try:
            u.save()
            return redirect("/member/companies/edit/"+str(u.company.id))
        except Exception, e:
            messages.warning(request, e.message)
            logging.error(e.message)
    if u.deal_size_min:
        c['deal_size_min_scale'] = int(pow(10, floor(log10(u.deal_size_min))))
        c['deal_size_min_digit'] = u.deal_size_min/c['deal_size_min_scale']
    else:
        c['deal_size_min_scale'] = 0
        c['deal_size_min_digit'] = 0

    if u.deal_size_max:
        c['deal_size_max_scale'] = int(pow(10, floor(log10(u.deal_size_max))))
        c['deal_size_max_digit'] = u.deal_size_max/c['deal_size_max_scale']
    else:
        c['deal_size_max_scale'] = 0
        c['deal_size_max_digit'] = 0

    c["u"] = u
    c["kv_list"] = u.tags.split(',')
    c['memberdata'] = Member.objects.filter(company=u.company).order_by('-id')
    c['size_scale'] = SCALE
    _load_data_matching(c)
    return render_to_response("member/edit_matching.html", c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required("company")
def remove_company_matching(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            CompanyInvestmentField.objects.filter(pk=id).delete()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


def _load_data_matching(c):
    c['countries'] = Country.objects.order_by("-sort").all()
    c['revenue_types'] = CompanyInvestmentField.FINANCE_TYPES
    c['currency_types'] = CompanyInvestmentField.CURRENCY_TYPES
    c['deal_types'] = CompanyInvestmentField.DEAL_TYPES
    c['growth_types'] = CompanyInvestmentField.GROWTH_TYPES
    c['net_types'] = CompanyInvestmentField.FINANCE_TYPES
    c['ebita_types'] = CompanyInvestmentField.FINANCE_TYPES
    c['size_types'] = CompanyInvestmentField.FINANCE_TYPES
    c['hot_score_list']=range(0,11)


def _bind_data_matching(request, u):

    u.tags = request.POST.get('all_tags',None)
    u.revenue = int(request.POST['revenue'])
    u.growth = int(request.POST['growth'])
    u.net_income = int(request.POST['net_income'])
    u.ebita = int(request.POST['ebita'])
    u.deal_type = int(request.POST['deal_type'])
    u.deal_currency = int(request.POST['deal_currency'])
    u.hot = int(request.POST['hot'])

    if 'member' in request.POST:
        u.member = Member.objects.get(pk=request.POST['member'])

    if request.POST['country']:
        _country_id = int(request.POST['country'])
        if _country_id !=0:
            try:
                u.country = Country.objects.get(id=_country_id)
            except Exception, e:
                pass

    if request.POST['deal_size']:
        _deal_size=int(request.POST['deal_size'])
        u.deal_size = _deal_size
        u.deal_size_min,u.deal_size_max = convert_finance_type_to_num(_deal_size)


def convert_finance_type_to_num(finance_type):

    if finance_type==99:
        num_min = 0
        num_max = 99999999999999
    elif finance_type==1:
        num_min = 0
        num_max = 10*10000000
    elif finance_type==2:
        num_min = 10*10000000
        num_max = 20*10000000
    elif finance_type==3:
        num_min = 20*10000000
        num_max = 50*10000000
    elif finance_type==4:
        num_min = 50*10000000
        num_max = 100*10000000
    elif finance_type==5:
        num_min = 100*10000000
        num_max = 200*10000000
    elif finance_type==6:
        num_min = 200*10000000
        num_max = 300*10000000
    elif finance_type==7:
        num_min = 300*10000000
        num_max = 500*10000000
    elif finance_type==8:
        num_min = 500*10000000
        num_max = 1000*10000000
    elif finance_type==9:
        num_min = 1000*10000000
        num_max = 2000*10000000
    elif finance_type==10:
        num_min = 2000*10000000
        num_max = 3000*10000000
    elif finance_type==11:
        num_min = 3000*10000000
        num_max = 99999999999999
    else:
        num_min=0
        num_max=0

    return num_min,num_max


def convert_growth_type_to_num(finance_type):

    if finance_type==99:
        num_min = 0
        num_max = 99999999999999
    elif finance_type==1:
        num_min = 0
        num_max = 10
    elif finance_type==2:
        num_min = 10
        num_max = 30
    elif finance_type==3:
        num_min = 30
        num_max = 50
    elif finance_type==4:
        num_min = 50
        num_max = 70
    elif finance_type==5:
        num_min = 70
        num_max = 100
    elif finance_type==6:
        num_min = 100
        num_max = 150

    elif finance_type==7:
        num_min = 150
        num_max = 99999999999999
    else:
        num_min=0
        num_max=0

    return num_min,num_max


def get_businesscard(request, file_name):
    file_path = '%s/card/' % (MEDIA_ROOT,)
    file_all_name = file_path+'%s' % (file_name)
    if os.path.isfile(file_all_name):
        f=open(file_all_name)
    else:
        raise Http404
    return HttpResponse(f, mimetype="image/jpeg")
